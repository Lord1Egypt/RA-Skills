"""文件上传处理 - 接收用户上传的视频并转为流水线输入"""
import asyncio
import logging
import shutil
from pathlib import Path
from config import settings

logger = logging.getLogger(__name__)


async def save_uploaded_video(content: bytes, filename: str, task_id: str) -> Path:
    """保存用户上传的视频文件，提取音频，返回音频路径"""
    output_dir = settings.DOWNLOAD_DIR / task_id
    output_dir.mkdir(parents=True, exist_ok=True)

    # 保存视频
    video_path = output_dir / f"source{Path(filename).suffix}"
    video_path.write_bytes(content)
    logger.info(f"Uploaded video saved: {video_path} ({len(content)/1024:.0f} KB)")

    # 提取音频
    audio_path = output_dir / "audio.mp3"
    proc = await asyncio.create_subprocess_exec(
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vn", "-acodec", "libmp3lame",
        "-q:a", "2",
        str(audio_path),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await proc.communicate()

    if not audio_path.exists():
        logger.warning(f"FFmpeg audio extraction failed, using video as-is: {video_path}")
        return video_path

    logger.info(f"Audio extracted: {audio_path} ({audio_path.stat().st_size/1024:.0f} KB)")
    return audio_path


async def save_uploaded_audio(content: bytes, filename: str, task_id: str) -> Path:
    """保存用户上传的音频文件"""
    audio_dir = settings.AUDIO_DIR
    audio_dir.mkdir(parents=True, exist_ok=True)
    audio_path = audio_dir / f"{task_id}.mp3"

    # 如果上传的不是 mp3，用 ffmpeg 转
    if filename.lower().endswith((".mp3", ".wav", ".m4a", ".ogg", ".flac")):
        audio_path.write_bytes(content)
        logger.info(f"Uploaded audio saved: {audio_path}")
        return audio_path
    else:
        tmp_path = audio_dir / f"{task_id}_raw{Path(filename).suffix}"
        tmp_path.write_bytes(content)
        proc = await asyncio.create_subprocess_exec(
            "ffmpeg", "-y", "-i", str(tmp_path),
            "-acodec", "libmp3lame", "-q:a", "2",
            str(audio_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.communicate()
        tmp_path.unlink(missing_ok=True)
        return audio_path
