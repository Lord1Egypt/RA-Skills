"""数字人视频生成模块"""
import asyncio
import logging
import subprocess
from pathlib import Path
from typing import Optional
from config import settings

logger = logging.getLogger(__name__)


class DigitalHuman:
    """数字人口播视频生成"""

    async def generate(
        self,
        audio_path: Path,
        task_id: str,
        mode: str = "",
        ref_image: str = "",
    ) -> Path:
        """
        生成数字人口播视频

        Args:
            audio_path: 语音音频文件
            task_id: 任务 ID
            mode: sadtalker | wav2lip | api
            ref_image: 参考图片路径

        Returns:
            生成视频路径
        """
        mode = mode or settings.DIGITAL_HUMAN_MODE
        output_path = settings.OUTPUT_DIR / f"{task_id}.mp4"

        if mode == "sadtalker":
            await self._sadtalker(audio_path, output_path, ref_image)
        elif mode == "wav2lip":
            await self._wav2lip(audio_path, output_path, ref_image)
        elif mode == "api":
            raise NotImplementedError("云端数字人 API 待接入")
        else:
            raise ValueError(f"不支持的数��人模式: {mode}")

        if not output_path.exists():
            raise RuntimeError(f"数字人视频生成失败：未生成文件")

        logger.info(f"Digital human video: {output_path} ({output_path.stat().st_size / 1024:.0f} KB)")
        return output_path

    async def _sadtalker(self, audio_path: Path, output_path: Path, ref_image: str):
        """SadTalker - 单图生成口播视频"""
        # 检查 SadTalker 是否已克隆
        sadtalker_dir = Path("/opt/SadTalker")
        if not sadtalker_dir.exists():
            # 无 SadTalker 时，生成占位/演示视频
            logger.warning("SadTalker not found, generating placeholder video")
            await self._generate_placeholder(audio_path, output_path)
            return

        ref_img = ref_image or settings.SADTALKER_REF_IMAGE or ""

        cmd = [
            "python", str(sadtalker_dir / "inference.py"),
            "--driven_audio", str(audio_path),
            "--result_dir", str(output_path.parent),
            "--name", output_path.stem,
            "--size", "256",
            "--batch_size", "2",
        ]
        if ref_img:
            cmd.extend(["--source_image", ref_img])
        else:
            # 使用 SadTalker 默认图片
            cmd.extend(["--source_image", str(sadtalker_dir / "examples/source_image/full_body_2.png")])

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=settings.PROCESS_TIMEOUT,
            )
        except asyncio.TimeoutError:
            process.kill()
            raise RuntimeError(f"SadTalker 生成超时")

        if process.returncode != 0:
            error = stderr.decode()[:500]
            logger.error(f"SadTalker failed: {error}")
            # fallback 到占位视频
            await self._generate_placeholder(audio_path, output_path)

    async def _wav2lip(self, audio_path: Path, output_path: Path, ref_video: str):
        """Wav2Lip - 唇同步（需参考视频）"""
        raise NotImplementedError("Wav2Lip 需参考视频，暂未实现")

    async def _generate_placeholder(self, audio_path: Path, output_path: Path):
        """
        生成占位视频 - 音频 + 静态图
        当数字人引擎不可用时，使用 ffmpeg 生成简单视频
        """
        # 使用一张默认图片 + 音频生成视频
        default_img = Path(__file__).parent.parent / "assets/default_avatar.png"
        if not default_img.exists():
            # 生成纯色背景
            default_img.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run([
                "ffmpeg", "-y",
                "-f", "lavfi", "-i", "color=c=#2D3748:s=720x1080:d=1",
                "-frames:v", "1",
                str(default_img),
            ], check=True, capture_output=True)

        # 用图片 + 音频生成视频
        subprocess.run([
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", str(default_img),
            "-i", str(audio_path),
            "-c:v", "libx264",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            "-pix_fmt", "yuv420p",
            str(output_path),
        ], check=True, capture_output=True, timeout=120)
