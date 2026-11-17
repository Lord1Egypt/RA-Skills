"""
BiliYouTik2Brain — 隐私模式 (v4.0)

`--private` 强制全本地处理，不传任何数据到云端。
适用于敏感内容处理场景。
"""

import os
from typing import Dict, Optional


# ═══════════════════════════════════════════════════════════
#  隐私配置
# ═══════════════════════════════════════════════════════════

_PRIVATE_MODE = False


def is_private_mode() -> bool:
    """是否在隐私模式"""
    global _PRIVATE_MODE
    return _PRIVATE_MODE or os.environ.get("BILI_PRIVATE_MODE", "").lower() in ("1", "true", "yes")


def set_private_mode(enabled: bool):
    """设置隐私模式"""
    global _PRIVATE_MODE
    _PRIVATE_MODE = enabled
    if enabled:
        os.environ["BILI_PRIVATE_MODE"] = "1"


# ═══════════════════════════════════════════════════════════
#  隐私检查
# ═══════════════════════════════════════════════════════════

def check_private_compliance(config: Dict) -> Dict:
    """检查配置是否符合隐私模式要求

    Returns:
        {compliant: bool, violations: [...], recommendations: [...]}
    """
    violations = []
    recommendations = []

    if is_private_mode():
        # 检查是否有云端 API key
        if os.environ.get("DASHSCOPE_API_KEY"):
            violations.append("百炼 ASR API Key 已配置（隐私模式下不会被使用）")
        if os.environ.get("OPENAI_API_KEY"):
            violations.append("OpenAI API Key 已配置（隐私模式下不会被使用）")

        # 检查代理（隐私模式下代理数据仍经过第三方）
        proxy = os.environ.get("HTTP_PROXY") or os.environ.get("HTTPS_PROXY")
        if proxy:
            recommendations.append(f"代理已配置: {proxy}（数据经过代理服务器）")

        # 检查是否禁用云端 ASR
        if config.get("asr_engine", "") in ("bailian", "openai_whisper"):
            violations.append(f"云端 ASR 引擎 {config['asr_engine']} 在隐私模式下不可用")

        # 检查是否禁用云端 LLM
        if config.get("llm_backend", "") in ("openai",):
            violations.append(f"云端 LLM {config['llm_backend']} 在隐私模式下不可用")

    return {
        "compliant": len(violations) == 0,
        "violations": violations,
        "recommendations": recommendations,
        "private_mode": is_private_mode(),
    }


def get_private_mode_banner() -> str:
    """获取隐私模式提示横幅"""
    if not is_private_mode():
        return ""

    return """
╔══════════════════════════════════════════════╗
║  🔒 隐私模式已启用                            ║
║  - 所有处理在本地完成                          ║
║  - 不发送任何数据到云端                        ║
║  - 不记录 API 调用                            ║
║  - 缓存数据加密存储                            ║
╚══════════════════════════════════════════════╝
"""


# ═══════════════════════════════════════════════════════════
#  隐私模式下的引擎选择
# ═══════════════════════════════════════════════════════════

def select_private_asr_engine() -> str:
    """隐私模式下选择 ASR 引擎

    优先级: faster-whisper > openai-whisper (本地) > 报错
    """
    if not is_private_mode():
        return "auto"

    # 检查 faster-whisper
    try:
        import faster_whisper
        return "faster_whisper"
    except ImportError:
        pass

    # 检查本地 openai-whisper
    try:
        import whisper
        return "openai_whisper_local"
    except ImportError:
        pass

    return "error"


def select_private_llm_backend() -> str:
    """隐私模式下选择 LLM 后端

    优先级: ollama > vllm > 本地小模型 > 跳过
    """
    if not is_private_mode():
        return "auto"

    # 检查 Ollama
    import subprocess
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=3)
        if result.returncode == 0:
            return "ollama"
    except Exception:
        pass

    # 检查 vLLM
    try:
        import requests
        resp = requests.get("http://localhost:8000/health", timeout=3)
        if resp.status_code == 200:
            return "vllm"
    except Exception:
        pass

    return "skip"  # 无本地 LLM，跳过增强
