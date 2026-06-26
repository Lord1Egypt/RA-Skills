#!/usr/bin/env python3
"""
本地媒体文件转录器

支持视频和音频文件 → Whisper 转录 → agent 整理 → 保存 Markdown

用法：
    python transcribe_local.py <媒体文件路径> [--output OUTPUT_DIR]
    python transcribe_local.py video.mp4
    python transcribe_local.py audio.mp3 --output ./output

支持的视频格式：MP4, AVI, MKV, MOV, WMV, FLV, WEBM, M4V, TS
支持的音频格式：MP3, WAV, FLAC, M4A, OGG, AAC, WMA, OPUS

LLM 整理说明：
    脚本本身不调用任何外部 LLM API。
    转录完成后输出原始文本，由调用方（agent）负责整理纠错，
    再调用 write_cleaned_md() 将整理后的文本写入 .md 文件。
"""

import os
import sys
from pathlib import Path

# Windows 下强制 UTF-8 输出
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        os.environ.setdefault("PYTHONIOENCODING", "utf-8")

# ── 导入共享模块 ──────────────────────────────────────────────────────────────

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from transcribe import (                  # noqa: E402
    check_dependencies,
    make_timestamp,
    validate_media_file,
    transcribe,
    write_cleaned_md,
)

check_dependencies(require_douyin=False)


# ── 配置 ──────────────────────────────────────────────────────────────────────

OUTPUT_DIR = "."


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("用法: python transcribe_local.py <媒体文件路径> [--output OUTPUT_DIR]")
        print()
        print("示例:")
        print("  python scripts/transcribe_local.py video.mp4")
        print("  python scripts/transcribe_local.py audio.mp3 --output ./output")
        print()
        print("支持的视频格式: MP4, AVI, MKV, MOV, WMV, FLV, WEBM, M4V, TS")
        print("支持的音频格式: MP3, WAV, FLAC, M4A, OGG, AAC, WMA, OPUS")
        sys.exit(1)

    # 解析参数
    args = sys.argv[1:]
    output_dir = OUTPUT_DIR

    if "--output" in args:
        idx = args.index("--output")
        if idx + 1 < len(args):
            output_dir = args.pop(idx + 1)
        args.pop(idx)

    if not args:
        print("[ERROR] 请提供媒体文件路径")
        sys.exit(1)

    file_path = args[0]

    # 验证文件
    abs_path = validate_media_file(file_path)

    ts = make_timestamp()
    print(f"[Info] 时间戳: {ts}")
    print("[Info] 流程: Step1 验证文件 -> Step2 Whisper转录 -> Step3 整理输出")

    # Whisper 转录（共享模块，使用默认 medium 模型）
    print("\n[Step 2/3] 正在转录（Whisper medium 模型，耗时取决于音频长度）...")
    result, txt_path, json_path = transcribe(abs_path, output_dir, timestamp=ts)

    raw_text = result["text"].strip()

    # 输出原始文本，由 agent 整理后调用 write_cleaned_md()
    print("\n[Step 3/3] 转录完成，请 agent 整理后调用 write_cleaned_md() 写入 MD")
    print(f"RAW_TRANSCRIPT_START\n{raw_text}\nRAW_TRANSCRIPT_END")

    print("\n[Done] 转录完毕")
    print(f"  文本:   {txt_path}")
    print(f"  JSON:   {json_path}")
    print(f"  时间戳: {ts}")
    print(f"\n预览: {raw_text[:200]}...")

    # 返回数据供外部使用
    return {
        "timestamp": ts,
        "source_path": abs_path,
        "source_name": os.path.basename(abs_path),
        "txt_path": txt_path,
        "json_path": json_path,
        "raw_text": raw_text,
        "segments": result["segments"],
    }


if __name__ == "__main__":
    main()
