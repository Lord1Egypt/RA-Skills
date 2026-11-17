"""流水线编排引擎"""
import asyncio
import logging
import time
from pathlib import Path
from typing import Optional, Callable
from config import settings
from task_manager import task_manager, TaskStatus

logger = logging.getLogger(__name__)


class PipelineOrchestrator:
    """5 步流水线编排 — 仅执行 Phase 1（下载→转写→改写→等待审核）"""

    def __init__(self):
        from modules.downloader import Downloader
        from modules.transcriber import Transcriber
        from modules.rewriter import Rewriter
        from modules.tts_engine import TTSEngine
        from modules.digital_human import DigitalHuman

        self.downloader = Downloader()
        self.transcriber = Transcriber()
        self.rewriter = Rewriter()
        self.tts = TTSEngine()
        self.dh = DigitalHuman()

    async def run(self, task_id: str, video_url: str, custom_prompt: str = ""):
        """Phase 1: 下载 → 转写 → 改写 → 等待用户审核"""
        try:
            # Step 1: 下载音频
            await self._step(
                task_id, 1, 5, TaskStatus.DOWNLOADING, "正在下载视频音频...", 15,
                lambda: self.downloader.download_audio(video_url, task_id),
            )

            audio_path = settings.DOWNLOAD_DIR / task_id / "audio.mp3"
            if not audio_path.exists():
                dl_dir = settings.DOWNLOAD_DIR / task_id
                files = list(dl_dir.glob("*"))
                if files:
                    audio_path = files[0]

            # Step 2: 语音转写
            transcript = await self._step(
                task_id, 2, 5, TaskStatus.TRANSCRIBING, "正在转写语音为文字...", 35,
                lambda: self.transcriber.transcribe(audio_path, task_id),
            )
            await task_manager.update(task_id, original_text=transcript)

            # Step 3: AI 自动改写（提供建议稿）
            rewritten = await self._step(
                task_id, 3, 5, TaskStatus.REWRITING, "AI 正在生成改写建议...", 55,
                lambda: self.rewriter.rewrite(transcript, task_id, custom_prompt),
            )
            await task_manager.update(task_id, rewritten_text=rewritten)

            # ⏸ 等待用户审核
            await task_manager.update(
                task_id,
                status=TaskStatus.AWAITING_REVIEW,
                progress=60,
                message="文案已就绪，请确认或编辑后点击「合成语音」",
            )
            logger.info(f"Phase 1 complete, awaiting review: {task_id}")

        except Exception as e:
            logger.exception(f"Phase 1 failed: {task_id}")
            await task_manager.update(
                task_id,
                status=TaskStatus.FAILED,
                message=f"处理失败: {str(e)[:200]}",
            )

    async def _step(
        self,
        task_id: str,
        step: int,
        total: int,
        status: TaskStatus,
        message: str,
        progress: int,
        fn: Callable,
    ):
        """执行单个步骤并更新进度"""
        await task_manager.update(
            task_id,
            status=status,
            message=message,
            current_step=step,
            total_steps=total,
            progress=progress,
        )
        return await fn()


orchestrator = PipelineOrchestrator()
