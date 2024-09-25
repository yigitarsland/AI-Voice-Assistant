import asyncio

from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero
from api import AssistantFnc

load_dotenv()

async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are a voice assistant created by LiveKit. Your interface with users will be voice. "
            "You should use short and concise responses, and avoiding usage of unpronouncable punctuation."
        )
    )
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    fnc_ctx = AssistantFnc()

    assistant=VoiceAssistant(
        vad=silero.VAD.load(), # Voice Activity Detection Model
        stt=openai.STT(), # Speech to Text Model
        llm=openai.LLM(), # Large Language Model
        tts=openai.TTS(), # Text to Speech Model
        chat_ctx=initial_ctx, # Chat Context
        fnc_ctx=fnc_ctx # Assistant Functionality
    )
    assistant.start(ctx.room)

    await asyncio.sleep(1)
    await assistant.say("How can I help you today?", allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))