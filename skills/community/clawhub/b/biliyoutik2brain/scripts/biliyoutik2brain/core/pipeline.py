"""
pipeline.py — thin wrapper for backward compatibility

v3: 所有逻辑已迁入:
  core/process.py        — process(), process_linear()
  core/builder.py        — build_pipeline_graph()
  core/node_collect.py   — collect(), _node_collect()
  core/node_transcribe.py — transcribe(), _node_transcribe()
  core/node_enhance.py   — _node_enhance(), enhance(), analyze()
  core/node_assess.py    — _node_assess()
  core/node_ocr.py       — _node_ocr()
  core/node_bleep.py     — _node_bleep_detect()
  core/node_save.py      — save_result(), _node_save_result()
  core/enhance_engine.py — enhance_and_analyze()
"""

import os, sys, json, time, re
from typing import Dict, Optional, List, Tuple

# ── 从新模块 re-export 核心接口 ──
from .process import process, process_linear, _extract_context_from_graph
from .builder import build_pipeline_graph
from .node_collect import collect, _node_collect
from .node_transcribe import (
    _node_transcribe, transcribe, _vad_transcribe,
    _smart_correct, _mark_low_confidence, _format_confidence_notes,
)
from .node_enhance import _node_enhance, enhance, analyze
from .node_assess import _node_assess
from .node_ocr import _node_ocr
from .node_bleep import _node_bleep_detect
from .node_save import (
    _node_save_result, _node_update_knowledge, _node_auto_archive,
    _node_record_task, save_result,
)
from .enhance_engine import enhance_and_analyze
from .config import PlatformRegistry, record_task
from .secrets import get_llm_config

# ── 版本号 ──
__version__ = "v1.8.1 (v3 refactor)"

# ── 存储路径（保持向后兼容） ──
from .paths import TRANSCRIPTS_DIR as STORAGE_DIR  # 统一路径管理
os.makedirs(STORAGE_DIR, exist_ok=True)

# ── LLM配置（旧接口 re-export） ──
DEEPSEEK_API_KEY = None
DEEPSEEK_BASE = None
LLM_MODEL = None

def _get_deepseek_config():
    """延迟加载DeepSeek配置（旧接口兼容）"""
    global DEEPSEEK_API_KEY, DEEPSEEK_BASE, LLM_MODEL
    if DEEPSEEK_API_KEY:
        return
    key, base, model = get_llm_config()
    DEEPSEEK_API_KEY = key
    DEEPSEEK_BASE = base
    LLM_MODEL = model
