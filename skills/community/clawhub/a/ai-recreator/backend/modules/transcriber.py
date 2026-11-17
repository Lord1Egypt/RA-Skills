"""语音转写模块 - Whisper"""
import asyncio
import logging
from pathlib import Path
from typing import Optional
from config import settings

logger = logging.getLogger(__name__)

# 懒加载 Whisper（模型大，首次加载较慢）
_whisper_model = None


def _get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        import whisper
        logger.info(f"Loading Whisper model: {settings.WHISPER_MODEL}")
        _whisper_model = whisper.load_model(settings.WHISPER_MODEL)
        logger.info("Whisper model loaded")
    return _whisper_model


class Transcriber:
    """语音转文字"""

    async def transcribe(self, audio_path: Path, task_id: str) -> str:
        """
        转写音频为文本
        返回完整文本
        """
        output_path = settings.TRANSCRIPT_DIR / f"{task_id}.txt"

        # 如果已缓存，直接返回
        if output_path.exists():
            return output_path.read_text(encoding="utf-8")

        def _run_whisper():
            model = _get_whisper_model()
            result = model.transcribe(
                str(audio_path),
                language="zh",
                task="transcribe",
                verbose=False,
            )
            return result["text"]

        loop = asyncio.get_event_loop()
        try:
            text = await asyncio.wait_for(
                loop.run_in_executor(None, _run_whisper),
                timeout=settings.PROCESS_TIMEOUT,
            )
        except asyncio.TimeoutError:
            raise RuntimeError(f"语音转写超时（{settings.PROCESS_TIMEOUT}s），请尝试更小的 Whisper 模型")

        # 写入缓存
        output_path.write_text(text, encoding="utf-8")
        logger.info(f"Transcribed: {len(text)} chars")
        return text
