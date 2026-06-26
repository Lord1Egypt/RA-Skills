#!/usr/bin/env python3
"""
Whisper 转录共享模块

供 fetch_douyin_video.py（抖音 URL）和 transcribe_local.py（本地文件）共用。
不包含任何抖音特定逻辑，仅提供通用的媒体文件 → Whisper 转录 → 输出功能。

依赖 (首次使用请先运行 scripts/setup_env.py)：
    pip install requests "imageio[ffmpeg]" playwright "numpy<2" openai-whisper
"""

import os
import sys
import json
import shutil
import time
from datetime import datetime

# Windows 下强制 UTF-8 输出，避免 GBK 控制台中文乱码
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        os.environ.setdefault("PYTHONIOENCODING", "utf-8")


def check_dependencies(require_douyin=False):
    """启动前检查所有依赖是否可用，不可用时给出明确修复指引。

    Args:
        require_douyin: 如果为 True，额外检查 playwright（仅抖音模式需要）。
    """
    # 核心依赖（本地和抖音模式都需要）
    core_deps = [
        ("whisper", "openai-whisper"),
        ("requests", "requests"),
        ("imageio_ffmpeg", "imageio[ffmpeg]"),
    ]

    # 可选依赖（仅抖音模式需要）
    optional_deps = [
        ("playwright", "playwright"),
    ]

    missing = []
    for mod_name, display in core_deps:
        try:
            __import__(mod_name)
        except ImportError as e:
            missing.append(f"  - {display}: {e}")

    if require_douyin:
        for mod_name, display in optional_deps:
            try:
                __import__(mod_name)
            except ImportError as e:
                missing.append(f"  - {display}: {e}")

    if missing:
        print("[ERROR] 缺少依赖包，请先运行环境配置脚本：")
        print("  python scripts/setup_env.py")
        if not require_douyin:
            print("  提示：本地转录模式只需核心依赖，抖音模式需额外安装 playwright")
        print()
        print("缺失项：")
        for m in missing:
            print(m)
        print()
        sys.exit(1)

    # 额外检查 torch（whisper 的底层依赖）
    try:
        import torch
        _ = torch.__version__
    except Exception as e:
        print("[ERROR] torch 加载失败（Whisper 必需）")
        print(f"  错误: {e}")
        if "DLL load failed" in str(e) or "c10" in str(e):
            print("  可能原因: VC++ Redistributable 未安装")
            print("  下载: https://aka.ms/vs/17/release/vc_redist.x64.exe")
            print("  安装后可能需要重启系统")
        if "numpy" in str(e).lower():
            print("  可能原因: numpy >= 2 不兼容，需要 numpy < 2")
            print("  修复: pip install 'numpy<2' --force-reinstall")
        sys.exit(1)


# 延迟导入 Whisper（依赖检查通过后才导入）
def _get_whisper():
    import whisper
    return whisper


# ── 时间戳 ────────────────────────────────────────────────────────────────────

def make_timestamp() -> str:
    """生成当前时间戳字符串，格式：20260618_112500"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


# ── FFmpeg ─────────────────────────────────────────────────────────────────────

def ensure_ffmpeg():
    """确保 ffmpeg 通过 imageio_ffmpeg 可用。"""
    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    ffmpeg_dir = os.path.dirname(ffmpeg_exe)
    os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
    ffmpeg_dest = os.path.join(ffmpeg_dir, "ffmpeg.exe")
    if not os.path.exists(ffmpeg_dest) and os.path.exists(ffmpeg_exe):
        shutil.copy(ffmpeg_exe, ffmpeg_dest)
    return ffmpeg_exe


# ── Whisper 模型加载 ───────────────────────────────────────────────────────────

def clean_corrupted_model_cache(model_name: str) -> bool:
    """删除可能损坏的 Whisper 模型缓存文件。返回是否执行了删除。"""
    cache_dir = os.path.expanduser("~/.cache/whisper")
    model_path = os.path.join(cache_dir, f"{model_name}.pt")
    if os.path.exists(model_path):
        size = os.path.getsize(model_path)
        if size < 500_000_000:  # medium 应该 >1.4GB，小于 500MB 肯定损坏
            print(f"[Whisper] 检测到疑似损坏的模型缓存 ({size/1024/1024:.0f}MB)，正在删除...")
            os.remove(model_path)
            print(f"[Whisper] 已删除 {model_path}")
            return True
    return False


def load_whisper_safe(model_name: str = "medium"):
    """
    安全加载 Whisper 模型，自动处理缓存损坏的情况。
    如果加载时崩溃（SIGABRT）或抛出异常，删除缓存后重试一次。
    """
    print(f"[Whisper] 加载模型: {model_name}（首次下载约 1.4GB）")

    # 先清理明显损坏的缓存
    clean_corrupted_model_cache(model_name)

    whisper = _get_whisper()
    try:
        model = whisper.load_model(model_name)
        return model
    except Exception as e:
        err_str = str(e)
        if "SIGABRT" in err_str or "corrupt" in err_str.lower() or "load" in err_str.lower():
            print(f"[Whisper] 模型加载失败 ({e})，可能是缓存损坏，正在清理后重试...")
            if clean_corrupted_model_cache(model_name):
                try:
                    model = whisper.load_model(model_name)
                    print("[Whisper] 重试成功")
                    return model
                except Exception as e2:
                    print(f"[Whisper] 重试仍然失败: {e2}")
                    raise
        raise


def _estimate_transcribe_time(duration_sec: float, device: str, model_name: str) -> str:
    """
    根据音频时长、设备类型和模型名预估转录耗时。

    参考值（基于实测）：
    - CPU + medium: ~1分钟音频 ≈ 2-3 分钟转录
    - GPU + medium: ~1分钟音频 ≈ 10-15 秒转录
    - CPU + large:  ~1分钟音频 ≈ 5-8 分钟转录
    - GPU + large:  ~1分钟音频 ≈ 20-30 秒转录

    返回人类可读的时间字符串，如 "约 2-3 分钟"。
    """
    if duration_sec <= 0:
        return "未知"

    # CPU/GPU 倍率范围（每分钟音频对应的转录分钟数）
    multipliers = {
        ("cpu", "tiny"):   (0.2, 0.4),
        ("cpu", "base"):   (0.4, 0.7),
        ("cpu", "small"):  (0.8, 1.2),
        ("cpu", "medium"): (2.0, 3.0),
        ("cpu", "large"):  (5.0, 8.0),
        ("cuda", "tiny"):   (0.03, 0.05),
        ("cuda", "base"):   (0.05, 0.1),
        ("cuda", "small"):  (0.1, 0.2),
        ("cuda", "medium"): (0.15, 0.25),
        ("cuda", "large"):  (0.3, 0.5),
    }

    audio_min = duration_sec / 60.0
    key = (device, model_name)
    low_m, high_m = multipliers.get(key, (2.0, 3.0))  # 默认按 CPU medium

    low = audio_min * low_m
    high = audio_min * high_m

    if high < 1:
        return f"约 {int(low*60)}-{int(high*60)} 秒"
    elif high < 5:
        return f"约 {low:.0f}-{high:.0f} 分钟"
    else:
        low_str = f"{low:.0f}" if low == int(low) else f"{low:.1f}"
        high_str = f"{high:.0f}" if high == int(high) else f"{high:.1f}"
        return f"约 {low_str}-{high_str} 分钟"


def _get_media_duration(media_path: str) -> float:
    """使用 ffprobe 获取媒体文件时长（秒）。失败时返回 0。"""
    import subprocess
    try:
        import imageio_ffmpeg
        ffprobe_exe = imageio_ffmpeg.get_ffmpeg_exe().replace("ffmpeg", "ffprobe")
        if not os.path.exists(ffprobe_exe):
            # ffprobe 不存在时用 ffmpeg 自带的信息探测
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            result = subprocess.run(
                [ffmpeg_exe, "-i", media_path, "-f", "null", "-"],
                capture_output=True, text=True, timeout=30,
            )
            # ffmpeg 的 stderr 输出中包含 Duration 行
            for line in result.stderr.splitlines():
                if "Duration" in line:
                    # 格式: Duration: 00:01:23.45, ...
                    dur_str = line.split("Duration:")[1].split(",")[0].strip()
                    h, m, s = dur_str.split(":")
                    return float(h) * 3600 + float(m) * 60 + float(s)
            return 0

        result = subprocess.run(
            [ffprobe_exe, "-v", "quiet", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", media_path],
            capture_output=True, text=True, timeout=30,
        )
        dur = float(result.stdout.strip())
        return dur if dur > 0 else 0
    except Exception:
        return 0


def _format_duration(seconds: float) -> str:
    """将秒数格式化为可读时长，如 "1分23秒" 或 "23秒"。"""
    if seconds <= 0:
        return "未知"
    m = int(seconds // 60)
    s = int(seconds % 60)
    if m > 0:
        return f"{m}分{s}秒"
    return f"{s}秒"


# ── 转录 ──────────────────────────────────────────────────────────────────────

# 设默认模型和语言为模块级变量，允许外部覆盖
WHISPER_MODEL = "medium"
WHISPER_LANGUAGE = "zh"
WHISPER_INITIAL_PROMPT = "以下是普通话的句子。"  # 提升中文识别准确率


def transcribe(
    media_path: str,
    output_dir: str = ".",
    timestamp: str = "",
    model_name: str | None = None,
    language: str | None = None,
    initial_prompt: str | None = None,
) -> tuple[dict, str, str]:
    """
    对视频或音频文件执行 Whisper 转录。

    Args:
        media_path:      视频或音频文件路径
        output_dir:      输出目录
        timestamp:       时间戳字符串（统一命名用）
        model_name:      Whisper 模型名（默认 "medium"）
        language:        语言代码（默认 "zh"）
        initial_prompt:  Whisper 提示文本（提升识别准确率，默认含中文提示）

    Returns:
        (result_dict, txt_path, json_path)
    """
    model_name = model_name or WHISPER_MODEL
    language = language or WHISPER_LANGUAGE
    initial_prompt = initial_prompt or WHISPER_INITIAL_PROMPT

    ffmpeg_path = ensure_ffmpeg()
    print(f"[转录] ffmpeg: {ffmpeg_path}")

    # 检测 GPU 加速
    device = "cpu"
    try:
        import torch
        if torch.cuda.is_available():
            device = "cuda"
            print(f"[转录] GPU 加速: CUDA {torch.cuda.get_device_name(0)}")
        else:
            print("[转录] GPU: 不可用，使用 CPU（较慢）")
    except Exception:
        print("[转录] GPU: torch 未安装，使用 CPU")

    # 获取媒体时长并预估转录时间
    duration = _get_media_duration(media_path)
    if duration > 0:
        print(f"[转录] 媒体时长: {_format_duration(duration)}")
        est = _estimate_transcribe_time(duration, device, model_name)
        print(f"[转录] 预估耗时: {est} (模型={model_name}, 设备={device})")
    else:
        print("[转录] 媒体时长: 无法获取")

    # 加载模型（首次可能需要下载，不计入转录耗时）
    model = load_whisper_safe(model_name)

    print(f"[转录] ========== 开始转录 ========== ")

    # 计时从模型加载完毕后开始（模型加载不应计入转录耗时）
    start_time = time.time()

    print(f"[转录] 处理中: {os.path.basename(media_path)}")

    result = model.transcribe(
        media_path,
        language=language,
        verbose=True,
        task="transcribe",
        initial_prompt=initial_prompt,
    )

    elapsed = time.time() - start_time
    print(f"[转录] ========== 转录完成 ========== ")
    print(f"[转录] 实际耗时: {_format_duration(elapsed)}")
    if duration > 0 and elapsed > 0:
        ratio = elapsed / duration
        print(f"[转录] 转录速度: {ratio:.1f}x 音频时长 ({device}/{model_name})")

    # 带时间戳的文件名，防止覆盖
    suffix = f"_{timestamp}" if timestamp else ""
    transcript_txt_path = os.path.join(output_dir, f"transcript{suffix}.txt")
    transcript_json_path = os.path.join(output_dir, f"transcript{suffix}.json")

    # 保存文本 + 时间段
    with open(transcript_txt_path, "w", encoding="utf-8") as f:
        f.write("=== 完整文字稿 ===\n\n")
        f.write(result["text"].strip())
        f.write("\n\n=== 带时间戳分段 ===\n\n")
        for seg in result["segments"]:
            start = seg["start"]
            end = seg["end"]
            text = seg["text"].strip()
            start_str = f"{int(start//60):02d}:{start%60:05.2f}"
            end_str = f"{int(end//60):02d}:{end%60:05.2f}"
            f.write(f"[{start_str} --> {end_str}]  {text}\n")

    # 保存原始 JSON
    with open(transcript_json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"[转录] 已保存: {transcript_txt_path}")
    print(f"[转录] 已保存: {transcript_json_path}")
    char_count = len(result['text'].replace(' ', '').replace('\n', '').strip())
    print(f"[转录] 共 {char_count} 字, {len(result['segments'])} 段")
    return result, transcript_txt_path, transcript_json_path


# ── 保存整理后的 Markdown ─────────────────────────────────────────────────────

def write_cleaned_md(
    cleaned_text: str,
    source: str,
    source_type: str = "douyin",
    timestamp: str = "",
    output_dir: str = ".",
) -> str:
    """
    将 agent 整理好的文本写入带时间戳的 Markdown 文件。

    此函数不做任何 LLM 调用——整理纠错由外部 agent 完成后，
    把结果传入 cleaned_text 即可。

    Args:
        cleaned_text:  agent 整理纠错后的正文文本
        source:        来源描述（URL 或文件路径/文件名）
        source_type:   "douyin" 或 "local"
        timestamp:     时间戳字符串（与产出物保持一致）
        output_dir:    输出目录

    Returns:
        md_path: 写入的 .md 文件路径
    """
    suffix = f"_{timestamp}" if timestamp else ""
    md_path = os.path.join(output_dir, f"transcript{suffix}.md")

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if source_type == "local":
        title = "# 媒体文件转录文本"
        meta = (
            f"> **源文件：** {source}\n"
            f"> **转录时间：** {date_str}\n"
            f"> **说明：** 本文由 Whisper 语音识别后经整理纠错，原文内容未做删改。"
        )
    else:
        title = "# 抖音视频转录文本"
        meta = (
            f"> **来源：** {source}\n"
            f"> **转录时间：** {date_str}\n"
            f"> **说明：** 本文由 Whisper 语音识别后经整理纠错，原文内容未做删改。"
        )

    footer = "*由 douyin-transcribe-lz 技能自动生成*"

    md_content = f"{title}\n\n{meta}\n\n---\n\n{cleaned_text}\n\n---\n\n{footer}\n"

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"[MD] 已保存整理后 Markdown: {md_path}")
    return md_path


# ── 支持的媒体格式 ─────────────────────────────────────────────────────────────

SUPPORTED_VIDEO_EXTENSIONS = {
    ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".ts",
}

SUPPORTED_AUDIO_EXTENSIONS = {
    ".mp3", ".wav", ".flac", ".m4a", ".ogg", ".aac", ".wma", ".opus",
}

SUPPORTED_EXTENSIONS = SUPPORTED_VIDEO_EXTENSIONS | SUPPORTED_AUDIO_EXTENSIONS


def validate_media_file(file_path: str) -> str:
    """
    验证文件是否存在且格式受支持。返回标准化后的绝对路径。
    """
    if not os.path.exists(file_path):
        print(f"[ERROR] 文件不存在: {file_path}")
        sys.exit(1)

    abs_path = os.path.abspath(file_path)
    ext = os.path.splitext(abs_path)[1].lower()

    if ext not in SUPPORTED_EXTENSIONS:
        print(f"[ERROR] 不支持的格式: {ext}")
        print(f"  支持的视频格式: {', '.join(sorted(SUPPORTED_VIDEO_EXTENSIONS))}")
        print(f"  支持的音频格式: {', '.join(sorted(SUPPORTED_AUDIO_EXTENSIONS))}")
        sys.exit(1)

    file_type = "视频" if ext in SUPPORTED_VIDEO_EXTENSIONS else "音频"
    size_mb = os.path.getsize(abs_path) / 1024 / 1024
    print(f"[文件] {file_type}: {os.path.basename(abs_path)} ({size_mb:.1f} MB)")
    return abs_path
