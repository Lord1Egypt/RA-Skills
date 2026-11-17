#!/usr/bin/env python3
"""
faster-transcriber → openai-whisper 包装器（Windows 兼容版）

用 openai-whisper (torch) 替换 faster-whisper (ctranslate2)，
因为 Windows 上 ctranslate2 4.7.1 加载模型会 segment fault。
保持函数签名完全一致，管线其他部分无需改动。
"""

import os
import tempfile
from typing import List, Tuple, Optional, Dict
import sys
import numpy as np

# ── 模型缓存位置 ──
MODEL_DIR = "base"  # openai-whisper 自动管理模型下载缓存

# ── 繁转简 ──
_cc = None

def _to_simplified(text: str) -> str:
    """繁体中文转简体"""
    global _cc
    if _cc is None:
        try:
            from opencc import OpenCC
            _cc = OpenCC('t2s')
        except ImportError:
            return text
    return _cc.convert(text)


# ── 懒加载单例（openai-whisper） ──
_model = None

def _get_model():
    """获取 whisper 模型（懒加载）"""
    global _model
    if _model is None:
        import whisper
        _model = whisper.load_model(MODEL_DIR, device="cpu")
    return _model


# ── 兼容接口 ──

def transcribe_audio_segment(
    audio_path: str,
    start_time: float = 0.0,
    end_time: Optional[float] = None,
    language: str = "zh",
    model_size: str = "base",
) -> str:
    """
    转录音频段（兼容 old API）
    注意：openai-whisper 没有内置 VAD，用截取片段 + 全量转录模拟。
    """
    import subprocess as sp

    if not os.path.exists(audio_path):
        return ""

    tmpdir = tempfile.gettempdir()
    # 提取音频段
    duration = (end_time - start_time) if end_time else 0
    seg_path = os.path.join(tmpdir, f"bili_work", f"fw_seg_{int(start_time)}_{int(end_time or 0)}.wav")
    os.makedirs(os.path.dirname(seg_path), exist_ok=True)

    if duration > 0:
        sp.run(
            ["ffmpeg", "-i", audio_path, "-ss", str(start_time),
             "-t", str(duration), "-ar", "16000", "-ac", "1",
             "-sample_fmt", "s16", "-y", seg_path],
            capture_output=True, text=True, timeout=30
        )
    else:
        seg_path = audio_path

    try:
        model = _get_model()
        result = model.transcribe(
            seg_path,
            language=language,
            beam_size=5,
            fp16=False,
        )
        text = result.get("text", "").strip()
        return _to_simplified(text)
    except Exception as e:
        return f"[whisper错误: {e}]"
    finally:
        if duration > 0 and os.path.exists(seg_path) and seg_path != audio_path:
            os.remove(seg_path)


def transcribe_full_audio(audio_path: str, language: str = "zh") -> str:
    """
    转录完整音频，返回纯文本
    """
    if not os.path.exists(audio_path):
        return ""

    try:
        model = _get_model()
        result = model.transcribe(
            audio_path,
            language=language,
            beam_size=5,
            fp16=False,
        )
        text = result.get("text", "").strip()
        return _to_simplified(text)
    except Exception as e:
        return f"[whisper错误: {e}]"


def transcribe_full_audio_detailed(
    audio_path: str,
    language: str = "zh",
    confidence_threshold: float = 0.5
) -> Tuple[str, List[Tuple[str, float]], List[Dict]]:
    """
    转录完整音频 → (full_text, low_confidence_words, raw_segments)
    
    openai-whisper 不提供词级置信度，因此 low_confidence_words 始终为空。
    raw_segments 包含每条段的起止时间和文本。
    """
    if not os.path.exists(audio_path):
        return "", [], []

    try:
        model = _get_model()
        result = model.transcribe(
            audio_path,
            language=language,
            beam_size=5,
            fp16=False,
        )

        segments = result.get("segments", [])
        text_parts = []
        raw_segments = []

        for seg in segments:
            seg_text = seg.get("text", "").strip()
            text_parts.append(seg_text)
            raw_segments.append({
                "start": round(seg.get("start", 0), 2),
                "end": round(seg.get("end", 0), 2),
                "text": seg_text,
            })

        full_text = _to_simplified("\n".join(text_parts))
        # openai-whisper 不提供词级置信度 → low_confidence_words 留空
        return full_text, [], raw_segments

    except Exception as e:
        return f"[whisper错误: {e}]", [], []


def model_available() -> bool:
    """检查模型是否可用"""
    try:
        _get_model()
        return True
    except Exception:
        return False


if __name__ == "__main__":
    # 自测
    print(f"模型可用: {model_available()}")
    if len(sys.argv) > 1:
        audio = sys.argv[1]
        print(f"转录: {audio}")
        text = transcribe_full_audio(audio)
        print(f"结果 ({len(text)}字):")
        print(text[:500])
