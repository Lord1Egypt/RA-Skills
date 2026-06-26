#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audio_tools.py - 音视频处理工具集
支持功能：
  1. extract - 从视频中提取音频并保存为 WAV
  2. clip    - 截取音频片段（指定开始时间和时长）
  3. play    - 调用系统默认播放器播放媒体文件
  4. transcribe - 语音识别转文字（Whisper）
  5. metadata   - 提取音视频元数据

工具优先级：ffmpeg > moviepy（自动检测）
工作目录：D:\\workbuddy
"""

import argparse
import os
import sys
import subprocess
import shutil
import re
import json
from pathlib import Path

# ─────────────────────────────────────────
# 环境预检
# ─────────────────────────────────────────

def check_python_version():
    """检查 Python 版本（要求 3.8+）"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("[ERROR] Python version too old!")
        print(f"        Current: {version.major}.{version.minor}.{version.micro}")
        print("        Required: Python 3.8 or higher")
        print("\n[SOLUTION] Please upgrade Python:")
        print("           https://www.python.org/downloads/")
        sys.exit(1)


def check_pip_available():
    """检查 pip 是否可用"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError("pip not available")
    except Exception:
        print("[ERROR] pip is not available!")
        print("\n[SOLUTION] Please ensure pip is installed:")
        print("           python -m ensurepip --upgrade")
        sys.exit(1)


def check_ffmpeg_or_moviepy():
    """检查 ffmpeg 或 moviepy 是否可用"""
    # 检查 ffmpeg
    ffmpeg_path = shutil.which("ffmpeg")
    local_ffmpeg = Path(__file__).parent.parent / "bin" / "ffmpeg.exe"
    
    has_ffmpeg = ffmpeg_path is not None or local_ffmpeg.exists()
    
    # 检查 moviepy
    try:
        import moviepy.editor  # noqa
        has_moviepy = True
    except ImportError:
        has_moviepy = False
    
    if not has_ffmpeg and not has_moviepy:
        print("[WARN] No media processing tool found!")
        print("\n[SOLUTION] Choose one of the following:")
        print("\n  Option 1 - Bundled ffmpeg (Recommended):")
        print("           Download ffmpeg from https://ffmpeg.org/download.html")
        print(f"           Place ffmpeg.exe in: {local_ffmpeg.parent}")
        print("\n  Option 2 - System ffmpeg:")
        print("           Windows: winget install ffmpeg")
        print("           macOS:   brew install ffmpeg")
        print("           Linux:   sudo apt install ffmpeg")
        print("\n  Option 3 - MoviePy (Python fallback):")
        print("           pip install moviepy")
        print("\n[NOTE] ffmpeg is recommended for better performance and format support.")
        return False
    
    return True


def print_env_status():
    """打印环境状态摘要"""
    print("=" * 50)
    print("Audio Tools - Environment Check")
    print("=" * 50)
    
    # Python 版本
    print(f"[OK] Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # ffmpeg
    ffmpeg_path = shutil.which("ffmpeg")
    local_ffmpeg = Path(__file__).parent.parent / "bin" / "ffmpeg.exe"
    if local_ffmpeg.exists():
        print(f"[OK] ffmpeg (bundled): {local_ffmpeg}")
    elif ffmpeg_path:
        print(f"[OK] ffmpeg (system): {ffmpeg_path}")
    else:
        print("[--] ffmpeg: not found (will use moviepy fallback)")
    
    # ffprobe
    ffprobe_path = shutil.which("ffprobe")
    local_ffprobe = Path(__file__).parent.parent / "bin" / "ffprobe.exe"
    if local_ffprobe.exists():
        print(f"[OK] ffprobe (bundled): {local_ffprobe}")
    elif ffprobe_path:
        print(f"[OK] ffprobe (system): {ffprobe_path}")
    else:
        print("[--] ffprobe: not found")
    
    # ffplay
    ffplay_path = shutil.which("ffplay")
    local_ffplay = Path(__file__).parent.parent / "bin" / "ffplay.exe"
    if local_ffplay.exists():
        print(f"[OK] ffplay (bundled): {local_ffplay}")
    elif ffplay_path:
        print(f"[OK] ffplay (system): {ffplay_path}")
    else:
        print("[--] ffplay: not found (will use system player)")
    
    # moviepy
    try:
        import moviepy.editor  # noqa
        print("[OK] moviepy: installed")
    except ImportError:
        print("[--] moviepy: not installed (auto-install on first use)")
    
    # whisper
    try:
        import whisper  # noqa
        print("[OK] openai-whisper: installed")
    except ImportError:
        print("[--] openai-whisper: not installed (auto-install on first use)")
    
    print("=" * 50)
    print()


# 执行环境预检
check_python_version()
check_pip_available()

WORK_DIR = Path(r"D:\workbuddy")

# Skill 本地 bin 目录（用于 bundled ffmpeg）
SKILL_DIR = Path(__file__).parent.parent
LOCAL_BIN = SKILL_DIR / "bin"


def get_ffmpeg_path() -> str | None:
    """
    查找 ffmpeg 路径，优先级：
    1. Skill 本地 bin/ffmpeg.exe
    2. 系统 PATH
    3. 返回 None（未找到）
    """
    # 1. 优先检查本地 bin 目录
    local_ffmpeg = LOCAL_BIN / "ffmpeg.exe"
    if local_ffmpeg.exists():
        return str(local_ffmpeg)
    
    # 2. 检查系统 PATH
    system_ffmpeg = shutil.which("ffmpeg")
    return system_ffmpeg


def get_ffprobe_path() -> str | None:
    """查找 ffprobe 路径（与 ffmpeg 同逻辑）"""
    local_ffprobe = LOCAL_BIN / "ffprobe.exe"
    if local_ffprobe.exists():
        return str(local_ffprobe)
    return shutil.which("ffprobe")


def get_ffplay_path() -> str | None:
    """查找 ffplay 路径（与 ffmpeg 同逻辑）"""
    local_ffplay = LOCAL_BIN / "ffplay.exe"
    if local_ffplay.exists():
        return str(local_ffplay)
    return shutil.which("ffplay")


def check_ffmpeg() -> bool:
    """检测 ffmpeg 是否可用（本地或系统）"""
    return get_ffmpeg_path() is not None


def ensure_moviepy():
    """确保 moviepy 已安装，否则自动安装"""
    try:
        import moviepy.editor  # noqa
        return True
    except ImportError:
        print("⚙️  moviepy 未安装，正在自动安装...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "moviepy"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("✅ moviepy 安装成功")
            return True
        else:
            print(f"❌ moviepy 安装失败：{result.stderr}")
            return False


# ─────────────────────────────────────────
# 路径处理
# ─────────────────────────────────────────

def resolve_path(path_str: str) -> Path:
    """
    将路径解析为绝对路径：
    - 已是绝对路径 → 直接使用
    - 相对路径 → 拼接工作目录
    """
    p = Path(path_str)
    if p.is_absolute():
        return p
    return WORK_DIR / p


def default_output(input_path: Path, suffix: str = None, extra: str = "") -> Path:
    """生成默认输出路径（同目录，可修改后缀或添加标识）"""
    stem = input_path.stem + extra
    ext = suffix if suffix else input_path.suffix
    return WORK_DIR / f"{stem}{ext}"


def parse_time(time_str: str) -> float:
    """
    将时间字符串转为秒数
    支持：
      - 纯数字（如 "30" → 30.0 秒）
      - HH:MM:SS 或 MM:SS（如 "00:01:30" → 90.0 秒）
    """
    time_str = str(time_str).strip()
    if re.match(r'^\d+(\.\d+)?$', time_str):
        return float(time_str)
    parts = time_str.split(":")
    parts = [float(p) for p in parts]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    elif len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    else:
        raise ValueError(f"无法解析时间格式：{time_str}，支持格式：秒数 或 HH:MM:SS")


def file_size_str(path: Path) -> str:
    """返回文件大小的可读字符串"""
    size = path.stat().st_size
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


# ─────────────────────────────────────────
# 功能 1：提取音频
# ─────────────────────────────────────────

def extract_audio(input_path: Path, output_path: Path):
    """从视频文件提取音频并保存为 WAV"""
    if not input_path.exists():
        print(f"❌ 输入文件不存在：{input_path}")
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    ffmpeg_path = get_ffmpeg_path()

    if ffmpeg_path:
        print(f"🔧 使用 ffmpeg 提取音频（{ffmpeg_path}）")
        cmd = [
            ffmpeg_path, "-y",
            "-i", str(input_path),
            "-vn",                   # 不包含视频流
            "-acodec", "pcm_s16le",  # WAV 标准编码
            "-ar", "44100",          # 采样率 44100Hz
            "-ac", "2",              # 双声道
            str(output_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ ffmpeg 执行失败：\n{result.stderr}")
            sys.exit(1)
    else:
        print(f"⚠️  ffmpeg 未找到，降级使用 moviepy")
        if not ensure_moviepy():
            print("❌ 无法使用 moviepy，请安装 ffmpeg 或 moviepy")
            sys.exit(1)
        from moviepy.editor import VideoFileClip
        clip = VideoFileClip(str(input_path))
        if clip.audio is None:
            print(f"❌ 该视频文件不包含音频轨道：{input_path}")
            sys.exit(1)
        clip.audio.write_audiofile(str(output_path), codec="pcm_s16le", fps=44100)
        clip.close()

    if output_path.exists():
        print(f"✅ 提取完成：{output_path}（大小：{file_size_str(output_path)}）")
    else:
        print(f"❌ 输出文件未生成，请检查错误信息")
        sys.exit(1)


# ─────────────────────────────────────────
# 功能 2：截取音频片段
# ─────────────────────────────────────────

def clip_audio(input_path: Path, start: float, duration: float, output_path: Path):
    """截取音频片段（指定开始时间和时长）"""
    if not input_path.exists():
        print(f"❌ 输入文件不存在：{input_path}")
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    ffmpeg_path = get_ffmpeg_path()

    if ffmpeg_path:
        print(f"🔧 使用 ffmpeg 截取音频（开始：{start}s，时长：{duration}s）")
        cmd = [
            ffmpeg_path, "-y",
            "-i", str(input_path),
            "-ss", str(start),       # 开始时间
            "-t", str(duration),     # 截取时长
            "-acodec", "copy",       # 无损复制，速度快
            str(output_path)
        ]
        # 若输出为 wav 需要重编码
        if output_path.suffix.lower() == ".wav":
            cmd = [
                ffmpeg_path, "-y",
                "-i", str(input_path),
                "-ss", str(start),
                "-t", str(duration),
                "-acodec", "pcm_s16le",
                "-ar", "44100",
                "-ac", "2",
                str(output_path)
            ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ ffmpeg 执行失败：\n{result.stderr}")
            sys.exit(1)
    else:
        print(f"⚠️  ffmpeg 未找到，降级使用 moviepy")
        if not ensure_moviepy():
            print("❌ 无法使用 moviepy，请安装 ffmpeg 或 moviepy")
            sys.exit(1)
        from moviepy.editor import AudioFileClip
        clip = AudioFileClip(str(input_path))
        end = start + duration
        if end > clip.duration:
            print(f"⚠️  截取结束时间（{end}s）超过文件时长（{clip.duration:.1f}s），将截取到结尾")
            end = clip.duration
        sub = clip.subclip(start, end)
        sub.write_audiofile(str(output_path), codec="pcm_s16le", fps=44100)
        clip.close()

    if output_path.exists():
        print(f"✅ 截取完成：{output_path}（时长：{duration}s，大小：{file_size_str(output_path)}）")
    else:
        print(f"❌ 输出文件未生成，请检查错误信息")
        sys.exit(1)


# ─────────────────────────────────────────
# 功能 3：播放媒体文件
# ─────────────────────────────────────────

def play_media(input_path: Path, use_ffplay: bool = True):
    """
    播放媒体文件
    优先级：ffplay（bundled）> 系统默认播放器
    """
    if not input_path.exists():
        print(f"❌ 文件不存在：{input_path}")
        sys.exit(1)

    ffplay_path = get_ffplay_path()

    # 优先使用 ffplay（如果存在且用户未禁用）
    if use_ffplay and ffplay_path:
        print(f"▶️  使用 ffplay 播放：{input_path}")
        cmd = [
            ffplay_path,
            "-autoexit",           # 播放完自动退出
            "-nodisp",             # 不显示视频画面（纯音频模式）
            str(input_path)
        ]
        # 如果是视频文件，去掉 -nodisp 显示画面
        video_exts = {'.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm'}
        if input_path.suffix.lower() in video_exts:
            cmd = [ffplay_path, "-autoexit", str(input_path)]

        try:
            subprocess.Popen(cmd)
            print(f"✅ 已启动 ffplay 播放：{input_path}")
            return
        except Exception as e:
            print(f"⚠️  ffplay 启动失败（{e}），回退到系统播放器")

    # 回退到系统默认播放器
    print(f"▶️  使用系统默认播放器打开：{input_path}")
    if sys.platform == "win32":
        os.startfile(str(input_path))
    elif sys.platform == "darwin":
        subprocess.Popen(["open", str(input_path)])
    else:
        subprocess.Popen(["xdg-open", str(input_path)])
    print(f"✅ 已调用系统默认播放器打开：{input_path}")


# ─────────────────────────────────────────
# 功能 4：语音识别转文字（Whisper）
# ─────────────────────────────────────────

def ensure_whisper():
    """确保 openai-whisper 已安装，否则自动安装"""
    try:
        import whisper
        return True
    except ImportError:
        print("[INFO] openai-whisper not installed, installing...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-U", "openai-whisper"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("[OK] openai-whisper installed successfully")
            return True
        else:
            print(f"[ERROR] openai-whisper installation failed: {result.stderr}")
            return False


def transcribe_audio(input_path: Path, output_path: Path, model: str = "small", language: str = None):
    """
    使用 Whisper 将音频转录为文字
    输出 JSON 格式：包含文字、时间戳、置信度
    """
    if not input_path.exists():
        print(f"❌ 输入文件不存在：{input_path}")
        sys.exit(1)

    if not ensure_whisper():
        print("❌ 无法加载 Whisper，请检查 Python 环境")
        sys.exit(1)

    import whisper
    import json

    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Loading Whisper model: {model}")
    print(f"[INFO] Transcribing: {input_path}")
    if language:
        print(f"[INFO] Language: {language}")

    try:
        # 加载模型
        model_obj = whisper.load_model(model)

        # 执行转录
        result = model_obj.transcribe(
            str(input_path),
            language=language,
            verbose=False
        )

        # 构建 JSON 输出
        output_data = {
            "text": result["text"].strip(),
            "language": result.get("language", "auto"),
            "duration": result.get("duration", 0),
            "segments": []
        }

        # 处理每个片段，包含时间戳和置信度
        for seg in result.get("segments", []):
            output_data["segments"].append({
                "id": seg.get("id"),
                "start": round(seg.get("start", 0), 3),
                "end": round(seg.get("end", 0), 3),
                "text": seg.get("text", "").strip(),
                "confidence": round(seg.get("avg_logprob", 0), 4),
                "no_speech_prob": round(seg.get("no_speech_prob", 0), 4)
            })

        # 保存 JSON
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        # 同时输出纯文本版本（同名 .txt）
        txt_path = output_path.with_suffix(".txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(output_data["text"])

        print(f"[OK] Transcription completed:")
        print(f"   JSON: {output_path}")
        print(f"   Text: {txt_path}")
        print(f"   Duration: {output_data['duration']:.1f}s")
        print(f"   Language: {output_data['language']}")
        print(f"   Segments: {len(output_data['segments'])}")

    except Exception as e:
        print(f"[ERROR] Transcription failed: {e}")
        sys.exit(1)


# ─────────────────────────────────────────
# 功能 5：提取音频元数据
# ─────────────────────────────────────────

def extract_metadata(input_path: Path, output_path: Path = None):
    """
    提取音频/视频文件的元数据信息
    使用 ffprobe 或 moviepy 作为备选
    """
    if not input_path.exists():
        print(f"❌ 文件不存在：{input_path}")
        sys.exit(1)

    import json

    metadata = {
        "file_path": str(input_path),
        "file_name": input_path.name,
        "file_size": file_size_str(input_path),
        "file_size_bytes": input_path.stat().st_size
    }

    ffprobe_path = get_ffprobe_path()

    # 优先使用 ffprobe 获取详细信息
    if ffprobe_path:
        print(f"[INFO] Using ffprobe to extract metadata")
        cmd = [
            ffprobe_path,
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            str(input_path)
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                ffprobe_data = json.loads(result.stdout)
                metadata["ffprobe"] = ffprobe_data

                # 提取常用字段
                fmt = ffprobe_data.get("format", {})
                metadata["duration"] = float(fmt.get("duration", 0))
                metadata["bitrate"] = int(fmt.get("bit_rate", 0))
                metadata["format_name"] = fmt.get("format_name", "")

                # 提取音频流信息
                for stream in ffprobe_data.get("streams", []):
                    if stream.get("codec_type") == "audio":
                        metadata["audio"] = {
                            "codec": stream.get("codec_name"),
                            "sample_rate": int(stream.get("sample_rate", 0)),
                            "channels": int(stream.get("channels", 0)),
                            "channel_layout": stream.get("channel_layout"),
                            "bits_per_sample": stream.get("bits_per_sample")
                        }
                        break

                # 提取视频流信息
                for stream in ffprobe_data.get("streams", []):
                    if stream.get("codec_type") == "video":
                        metadata["video"] = {
                            "codec": stream.get("codec_name"),
                            "width": int(stream.get("width", 0)),
                            "height": int(stream.get("height", 0)),
                            "fps": eval(stream.get("r_frame_rate", "0/1")),  # 如 "30/1" -> 30.0
                            "pixel_format": stream.get("pix_fmt")
                        }
                        break

        except Exception as e:
            print(f"[WARN] ffprobe failed ({e}), trying fallback")

    # ffprobe 失败或无信息，使用 moviepy 作为备选
    if "duration" not in metadata:
        print(f"[INFO] Using moviepy to extract basic metadata")
        if not ensure_moviepy():
            print("[ERROR] Cannot get metadata")
            sys.exit(1)

        try:
            from moviepy.editor import AudioFileClip, VideoFileClip

            # 尝试作为视频打开
            try:
                clip = VideoFileClip(str(input_path))
                metadata["duration"] = clip.duration
                metadata["fps"] = clip.fps
                metadata["size"] = clip.size  # [width, height]
                if clip.audio:
                    metadata["has_audio"] = True
                    metadata["audio_fps"] = clip.audio.fps
                clip.close()
            except:
                # 作为纯音频打开
                clip = AudioFileClip(str(input_path))
                metadata["duration"] = clip.duration
                metadata["audio_fps"] = clip.fps
                metadata["has_audio"] = True
                clip.close()

        except Exception as e:
            print(f"[ERROR] Cannot read file: {e}")
            sys.exit(1)

    # 输出结果
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        print(f"[OK] Metadata saved: {output_path}")
    else:
        print(json.dumps(metadata, ensure_ascii=False, indent=2))

    # 打印关键信息摘要
    print(f"\n[Summary]")
    print(f"   File: {metadata['file_name']}")
    print(f"   Size: {metadata['file_size']}")
    if "duration" in metadata:
        print(f"   Duration: {metadata['duration']:.2f}s")
    if "bitrate" in metadata:
        print(f"   Bitrate: {metadata['bitrate'] // 1000} kbps")
    if "audio" in metadata:
        audio = metadata["audio"]
        print(f"   Audio: {audio.get('codec', 'N/A')} | {audio.get('sample_rate', 0)}Hz | {audio.get('channels', 0)}ch")
    if "video" in metadata:
        video = metadata["video"]
        print(f"   Video: {video.get('codec', 'N/A')} | {video.get('width', 0)}x{video.get('height', 0)} | {video.get('fps', 0):.1f}fps")


# ─────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="音视频处理工具集 - 提取/截取/播放/转录/元数据",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例：
  # 检查环境
  python audio_tools.py --check

  # 提取视频音频
  python audio_tools.py extract --input video.mp4
  python audio_tools.py extract --input video.mp4 --output output.wav

  # 截取音频片段（从第30秒开始，截取60秒）
  python audio_tools.py clip --input audio.wav --start 30 --duration 60
  python audio_tools.py clip --input audio.wav --start 00:00:30 --duration 60 --output clip.wav

  # 播放媒体文件
  python audio_tools.py play --input video.mp4
  python audio_tools.py play --input audio.wav

  # 语音识别转文字（Whisper）
  python audio_tools.py transcribe --input audio.wav
  python audio_tools.py transcribe --input audio.wav --model small --language zh

  # 提取音频/视频元数据
  python audio_tools.py metadata --input video.mp4
  python audio_tools.py metadata --input audio.wav --output meta.json
        """
    )
    
    parser.add_argument("--check", action="store_true", help="检查环境依赖并退出")
    parser.add_argument("--no-check", action="store_true", help="跳过环境检查（静默模式）")

    subparsers = parser.add_subparsers(dest="command", required=False)

    # ── extract 子命令 ──
    p_extract = subparsers.add_parser("extract", help="从视频提取音频（WAV格式）")
    p_extract.add_argument("--input", "-i", required=True, help="输入视频文件路径")
    p_extract.add_argument("--output", "-o", help="输出WAV文件路径（默认：同名.wav）")

    # ── clip 子命令 ──
    p_clip = subparsers.add_parser("clip", help="截取音频片段")
    p_clip.add_argument("--input", "-i", required=True, help="输入音频文件路径")
    p_clip.add_argument("--start", "-s", required=True, help="开始时间（秒 或 HH:MM:SS）")
    p_clip.add_argument("--duration", "-d", required=True, type=float, help="截取时长（秒）")
    p_clip.add_argument("--output", "-o", help="输出文件路径（默认：原文件名_clip.wav）")

    # ── play 子命令 ──
    p_play = subparsers.add_parser("play", help="播放媒体文件")
    p_play.add_argument("--input", "-i", required=True, help="媒体文件路径（视频或音频）")

    # ── transcribe 子命令 ──
    p_trans = subparsers.add_parser("transcribe", help="语音识别转文字（Whisper）")
    p_trans.add_argument("--input", "-i", required=True, help="输入音频文件路径")
    p_trans.add_argument("--output", "-o", help="输出JSON路径（默认：同名.json）")
    p_trans.add_argument("--model", "-m", default="small",
                         choices=["tiny", "base", "small", "medium", "large"],
                         help="Whisper模型大小（默认：small）")
    p_trans.add_argument("--language", "-l", help="语言代码（如 zh, en, ja，默认自动检测）")

    # ── metadata 子命令 ──
    p_meta = subparsers.add_parser("metadata", help="提取音频/视频元数据")
    p_meta.add_argument("--input", "-i", required=True, help="输入文件路径")
    p_meta.add_argument("--output", "-o", help="输出JSON路径（默认：终端输出）")

    args = parser.parse_args()
    
    # ── 环境检查模式 ──
    if args.check:
        print_env_status()
        sys.exit(0)
    
    # ── 静默模式（跳过环境检查输出）──
    if not args.no_check:
        print_env_status()
        check_ffmpeg_or_moviepy()
    
    # ── 检查是否有子命令 ──
    if args.command is None:
        parser.print_help()
        sys.exit(0)
    
    # ── 路由到对应功能 ──
    if args.command == "extract":
        input_path = resolve_path(args.input)
        output_path = resolve_path(args.output) if args.output else default_output(input_path, ".wav")
        extract_audio(input_path, output_path)

    elif args.command == "clip":
        input_path = resolve_path(args.input)
        start = parse_time(args.start)
        duration = args.duration
        output_path = resolve_path(args.output) if args.output else default_output(input_path, extra="_clip")
        clip_audio(input_path, start, duration, output_path)

    elif args.command == "play":
        input_path = resolve_path(args.input)
        play_media(input_path)

    elif args.command == "transcribe":
        input_path = resolve_path(args.input)
        output_path = resolve_path(args.output) if args.output else default_output(input_path, ".json")
        transcribe_audio(input_path, output_path, model=args.model, language=args.language)

    elif args.command == "metadata":
        input_path = resolve_path(args.input)
        output_path = resolve_path(args.output) if args.output else None
        extract_metadata(input_path, output_path)


if __name__ == "__main__":
    main()
