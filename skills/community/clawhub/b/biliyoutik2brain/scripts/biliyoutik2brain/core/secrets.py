"""
BiliYouTik2Brain — 统一机密管理器

所有外部服务的 API Key / Secret 从这里获取，不硬编码、不留痕。
- DeepSeek / 类OpenAI推理模型
- DashScope (百炼ASR)

启动时检测可用性，返回状态。

**使用示例**:
    from .secrets import get_llm_config, get_dashscope_key
    key, base, model = get_llm_config()
"""

import os
import sys
from typing import Optional, Tuple

# ── DashScope (百炼ASR) ──
DASHSCOPE_BASE_URL = "https://dashscope.aliyuncs.com"
DASHSCOPE_MULTIMODAL_URL = DASHSCOPE_BASE_URL + "/api/v1/services/aigc/multimodal-generation/generation"


def get_dashscope_key() -> Optional[str]:
    """
    获取百炼/ModelStudio API Key。
    优先从环境变量 DASHSCOPE_API_KEY 读取，返回 None 表示不可用。
    """
    key = os.environ.get("DASHSCOPE_API_KEY")
    if key:
        return key
    return None


def get_dashscope_available() -> bool:
    """百炼ASR是否可用（有key且网络可达）"""
    key = get_dashscope_key()
    if not key:
        return False
    try:
        import requests
        r = requests.get(DASHSCOPE_BASE_URL, timeout=3)
        return r.status_code < 500
    except Exception:
        return False


# ── DeepSeek / 通用LLM推理 ──
# 加载优先级: (1) 本地 extra/ transcription_enhancer (旧配置兜底)
#             (2) 环境变量 LLM_API_KEY + LLM_BASE_URL + LLM_MODEL

_EXTRA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "extra")


def get_llm_config() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    获取 LLM 推理配置。
    
    Returns:
        (api_key, base_url, model_name) 三元组
        全部为 None 表示不可用
    """
    # 1) 优先环境变量（最新的配置）
    key = os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
    base = os.environ.get("LLM_BASE_URL") or os.environ.get("OPENAI_BASE_URL") or "https://api.deepseek.com/v1"
    model = os.environ.get("LLM_MODEL", "deepseek-v4-flash")
    
    if key:
        return key, base, model
    
    # 2) 兜底 local extra/ transcription_enhancer
    if _EXTRA_DIR not in sys.path:
        sys.path.insert(0, _EXTRA_DIR)
    try:
        from transcription_enhancer import (
            DEEPSEEK_API_KEY as _key,
            DEEPSEEK_BASE as _base,
            LLM_MODEL as _model,
        )
        return _key, _base, _model
    except ImportError:
        pass
    
    return None, None, None


def get_llm_available() -> bool:
    """LLM服务是否可用"""
    key, base, model = get_llm_config()
    return bool(key and base and model)
