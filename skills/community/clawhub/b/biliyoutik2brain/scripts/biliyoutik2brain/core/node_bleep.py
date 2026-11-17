"""
BiliYouTik2Brain — BLEEP音频消音检测节点

职责：
  1. 在 assess 完成后与转录/OCR并行
  2. 检测音频中的BLEEP（哔声）段
  3. 轻量节点 ~2s，continue_on_error=True
"""

import os
from typing import Dict


def _node_bleep_detect(**kw) -> str:
    """节点（轻量）：音频消音检测，与转录并行
    
    检测 bleep（哔声），返回文本标记供 prompt 使用
    """
    assess_result = kw.get("assess", {})
    audio_file = ""
    if isinstance(assess_result, dict):
        audio_file = assess_result.get("audio_file", "")
    
    if not audio_file or not os.path.exists(audio_file):
        return ""
    
    print(f"  [BLEEP] 🔇 扫描消音...", end="", flush=True)
    try:
        from biliyoutik2brain.extra.audio_detector import mark_bleeps_in_text
        result = mark_bleeps_in_text(audio_file, [])
        print(f" ✅ 完成")
        return result
    except Exception as e:
        print(f" ⚠️ {e}")
        return ""
