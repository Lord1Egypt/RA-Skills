"""CyberHorn 音频核心：TTS (ElevenLabs / Edge) + FFmpeg 转 Opus。"""
import subprocess
import sys
import tempfile
from pathlib import Path

from config import get_edge_config, get_eleven_config, get_ffmpeg_path, get_tts_provider


def tts_to_mp3(text: str, api_key: str, voice_id: str, out_path: str | Path) -> None:
    """
    使用 ElevenLabs 将文本转为 MP3，完整写入 out_path 后再返回。
    流式接口会在内存中收集完整数据后一次性写入，确保文件完整再给 ffmpeg。
    """
    try:
        from elevenlabs.client import ElevenLabs
    except ImportError:
        print("[CyberHorn] 未安装 elevenlabs，请执行: pip install elevenlabs", file=sys.stderr)
        raise

    client = ElevenLabs(api_key=api_key)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        audio_bytes = client.text_to_speech.convert(
            voice_id=voice_id,
            text=text,
        )
    except Exception as e:
        # 打印 API 错误码，便于排查余额、权限、voice_id 等
        err_detail = str(e)
        if hasattr(e, "body"):
            err_detail += f" | body: {getattr(e, 'body', '')}"
        if hasattr(e, "status_code"):
            err_detail += f" | status_code: {getattr(e, 'status_code', '')}"
        print(f"[CyberHorn] ElevenLabs API 错误: {err_detail}", file=sys.stderr)
        raise

    # 兼容返回 bytes 或流式迭代器
    if hasattr(audio_bytes, "__iter__") and not isinstance(audio_bytes, (bytes, bytearray)):
        audio_bytes = b"".join(audio_bytes)
    if not audio_bytes:
        raise RuntimeError("ElevenLabs 返回空音频，请检查余额或 voice_id。")

    with open(out_path, "wb") as f:
        f.write(audio_bytes)


def edge_tts_to_mp3(text: str, voice: str, out_path: str | Path) -> None:
    """
    使用 Edge 在线 TTS 将文本转为 MP3。
    依赖 edge-tts 库。
    """
    try:
        import edge_tts
    except ImportError:
        print("[CyberHorn] 未安装 edge-tts，请执行: pip install edge-tts", file=sys.stderr)
        raise

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # 使用同步保存接口，避免在调用方处理异步
    communicate = edge_tts.Communicate(text, voice)
    try:
        communicate.save_sync(str(out_path))
    except Exception as e:
        print(f"[CyberHorn] Edge TTS 错误: {e}", file=sys.stderr)
        raise


def mp3_to_opus_16000(mp3_path: str | Path, opus_path: str | Path) -> None:
    """
    使用 ffmpeg 将 MP3 转为飞书语音条要求的 Opus：单声道 16kHz。
    命令: -acodec libopus -ac 1 -ar 16000
    """
    mp3_path = Path(mp3_path)
    opus_path = Path(opus_path)
    if not mp3_path.exists():
        raise FileNotFoundError(f"MP3 文件不存在: {mp3_path}")

    ffmpeg = get_ffmpeg_path()
    cmd = [
        ffmpeg,
        "-y",
        "-i", str(mp3_path),
        "-acodec", "libopus",
        "-ac", "1",
        "-ar", "16000",
        str(opus_path),
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        err = (result.stderr or result.stdout or "").strip()
        raise RuntimeError(f"FFmpeg 转码失败 (exit {result.returncode}): {err}")
    if not opus_path.exists():
        raise RuntimeError(f"FFmpeg 未生成文件: {opus_path}")


def text_to_opus_file(
    text: str,
    *,
    keep_mp3_path: str | Path | None = None,
    keep_opus_path: str | Path | None = None,
) -> tuple[Path, Path]:
    """
    文本 → TTS MP3 → Opus，返回 (mp3_path, opus_path)。
    若 keep_* 为 None 则使用临时文件；调用方负责在不用时删除。
    """
    if keep_mp3_path is None:
        fd_mp3, keep_mp3_path = tempfile.mkstemp(suffix=".mp3")
        keep_mp3_path = Path(keep_mp3_path)
        try:
            import os
            os.close(fd_mp3)
        except Exception:
            pass
    else:
        keep_mp3_path = Path(keep_mp3_path)

    if keep_opus_path is None:
        fd_opus, keep_opus_path = tempfile.mkstemp(suffix=".opus")
        keep_opus_path = Path(keep_opus_path)
        try:
            import os
            os.close(fd_opus)
        except Exception:
            pass
    else:
        keep_opus_path = Path(keep_opus_path)

    # 根据 TTS_PROVIDER 选择不同的引擎
    provider = get_tts_provider()
    if provider in ("ELEVEN", "ELEVENLABS"):
        eleven = get_eleven_config()
        tts_to_mp3(text, eleven["api_key"], eleven["voice_id"], keep_mp3_path)
    elif provider == "EDGE":
        edge = get_edge_config()
        edge_tts_to_mp3(text, edge["voice"], keep_mp3_path)
    else:
        raise RuntimeError(f"不支持的 TTS_PROVIDER: {provider}")

    mp3_to_opus_16000(keep_mp3_path, keep_opus_path)
    return keep_mp3_path, keep_opus_path
