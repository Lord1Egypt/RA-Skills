#!/usr/bin/env python3
"""阶段 2：转录音频为带时间戳的 segments。

核心设计：
- faster-whisper (small, CPU int8) 本地转录
- ★ 保留 segments 的 start/end/text（时间戳是语义边界对齐的基础）
- opencc t2s 繁简转换（Whisper small 默认输出繁体）
- 错字修正字典（同音错字）
- 输出 transcript_N.json（带时间戳的 segments 数组）
"""
from __future__ import annotations
import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from common import write_json, read_json, apply_error_corrections


# HuggingFace 镜像（国内加速）
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")


# 全局模型缓存（v3.1：避免每次循环重新加载，11 个视频省 5-10 分钟）
_MODEL_CACHE: dict = {}


def _get_model(model_size: str = "small"):
    """加载 faster-whisper 模型（带缓存）。"""
    if model_size not in _MODEL_CACHE:
        try:
            from faster_whisper import WhisperModel
        except ImportError:
            print("❌ 未安装 faster-whisper，请运行: pip install faster-whisper", file=sys.stderr)
            sys.exit(1)
        print(f"📥 加载模型 {model_size} (CPU int8)...", flush=True)
        _MODEL_CACHE[model_size] = WhisperModel(model_size, device="cpu", compute_type="int8")
    return _MODEL_CACHE[model_size]


def transcribe_audio(audio_path: Path, model_size: str = "small") -> dict:
    """用 faster-whisper 转录音频，返回带时间戳的 segments。

    v3.1：模型从全局缓存取，不再每次重新加载。

    Returns:
        {
            "segments": [{"start": float, "end": float, "text": str}, ...],
            "language": str,
            "model": str,
        }
    """
    model = _get_model(model_size)

    print(f"🎙️ 转录中: {audio_path.name}", flush=True)
    segments_gen, info = model.transcribe(
        str(audio_path),
        language="zh",
        beam_size=5,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 500},
    )

    segments = []
    for seg in segments_gen:
        text = seg.text.strip()
        if text:
            segments.append({
                "start": round(seg.start, 3),
                "end": round(seg.end, 3),
                "text": text,
            })

    print(f"   ✅ {len(segments)} 个 segments, 语言={info.language}", flush=True)
    return {
        "segments": segments,
        "language": info.language,
        "model": model_size,
    }


def convert_t2s(text: str) -> str:
    """繁体转简体。Whisper small 默认输出繁体。"""
    try:
        from opencc import OpenCC
        converter = OpenCC("t2s")
        return converter.convert(text)
    except ImportError:
        print("⚠️ 未安装 opencc-python-reimplemented，跳过繁简转换", file=sys.stderr)
        return text
    except Exception as e:
        print(f"⚠️ opencc 转换失败: {e}", file=sys.stderr)
        return text


def process_transcript(
    metadata_item: dict,
    audio_dir: Path,
    output_dir: Path,
    model_size: str = "small",
) -> dict:
    """处理单个视频的转录。"""
    idx = metadata_item["idx"]
    title = metadata_item.get("title") or f"video_{idx}"

    # v3.0: YouTube 字幕路径，跳过 Whisper（transcript 已在阶段 1 生成）
    if metadata_item.get("skip_transcribe"):
        transcript_path = metadata_item.get("transcript_path")
        if transcript_path and Path(transcript_path).is_file():
            print(f"⏭️ [{idx}] 跳过 Whisper（字幕已由 {metadata_item.get('transcript_source', 'API')} 生成）", flush=True)
            return {**metadata_item, "transcript_success": True, "transcript_path": transcript_path}
        return {**metadata_item, "transcript_success": False, "error": "skip_transcribe=True 但 transcript_path 不存在"}

    audio_path = Path(metadata_item["audio_path"])

    if not audio_path.is_file():
        return {**metadata_item, "transcript_success": False, "error": f"音频文件不存在: {audio_path}"}

    # 转录
    result = transcribe_audio(audio_path, model_size)

    # 繁简转换 + 错字修正
    print(f"🔄 繁简转换 + 错字修正...", flush=True)
    for seg in result["segments"]:
        seg["text"] = convert_t2s(seg["text"])
        seg["text"] = apply_error_corrections(seg["text"])

    # 构造完整 transcript 对象
    transcript = {
        "video_id": str(idx),
        "title": title,
        "author": metadata_item.get("author", "未知作者"),
        "source_url": metadata_item.get("source_url", ""),
        "duration_sec": metadata_item.get("duration_sec", 0),
        "model": result["model"],
        "language": result["language"],
        "segments": result["segments"],
    }

    # 写入 transcript_N.json
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"transcript_{idx}.json"
    write_json(out_path, transcript)

    word_count = sum(len(s["text"]) for s in transcript["segments"])
    print(f"✅ 转录完成: {out_path.name} ({word_count} 字)", flush=True)

    return {**metadata_item, "transcript_success": True, "transcript_path": str(out_path)}


def main() -> None:
    parser = argparse.ArgumentParser(description="阶段 2：转录音频")
    parser.add_argument("--metadata", type=Path, required=True, help="阶段 1 输出的 metadata.json")
    parser.add_argument("--output-dir", type=Path, required=True, help="输出根目录（transcript/ 子目录）")
    parser.add_argument("--model", default="small", help="Whisper 模型大小 (tiny/base/small/medium)")
    args = parser.parse_args()

    meta = read_json(args.metadata)
    items = [m for m in meta["items"] if m.get("success")]
    print(f"📋 待转录: {len(items)} 个音频", flush=True)

    transcript_dir = args.output_dir / "transcript"
    results = []
    for item in items:
        result = process_transcript(item, args.output_dir / "audio", transcript_dir, args.model)
        results.append(result)

    success = sum(1 for r in results if r.get("transcript_success"))
    print(f"\n📊 转录完成: {success}/{len(results)}", flush=True)


if __name__ == "__main__":
    main()
