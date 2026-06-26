"""
环境检测模块 - ai-drama-review

检测运行环境，确定可用的分析能力。
"""

import json
import os
import platform
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from credential_manager import _AI_PROVIDER_KEYS


def detect_python_version() -> dict:
    """检测 Python 版本。"""
    version = sys.version_info
    return {
        "version": f"{version.major}.{version.minor}.{version.micro}",
        "major": version.major,
        "minor": version.minor,
        "meets_minimum": version >= (3, 8),
    }


def detect_api_keys() -> dict:
    """检测 AI API 密钥可用性（仅检测存在性，不打印值）。"""
    return {
        env_var: bool(os.environ.get(env_var))
        for env_var in _AI_PROVIDER_KEYS.values()
    }


def detect_python_packages() -> dict:
    """检测可选 Python 包。"""
    packages = {}

    # jieba - 中文分词
    try:
        import jieba
        packages["jieba"] = {"installed": True, "version": jieba.__version__}
    except ImportError:
        packages["jieba"] = {"installed": False, "note": "可选，提升中文版权检测精度"}

    return packages


def detect_network() -> dict:
    """检测网络连通性。"""
    result = {"internet": False}

    try:
        import urllib.request
        urllib.request.urlopen("https://api.openai.com", timeout=5)
        result["internet"] = True
        result["openai_reachable"] = True
    except Exception:
        try:
            import urllib.request
            urllib.request.urlopen("https://www.baidu.com", timeout=5)
            result["internet"] = True
            result["openai_reachable"] = False
        except Exception:
            pass

    return result


def determine_run_mode(api_keys: dict) -> str:
    """
    确定运行模式。

    Args:
        api_keys: detect_api_keys() 的结果

    Returns:
        "hybrid" 或 "local_only"
    """
    if any(api_keys.values()):
        return "hybrid"
    return "local_only"


def run_full_detection() -> dict:
    """执行完整环境检测，返回 JSON 报告。"""
    python_info = detect_python_version()
    api_keys = detect_api_keys()
    packages = detect_python_packages()
    network = detect_network()
    run_mode = determine_run_mode(api_keys)

    report = {
        "system": {
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
        },
        "python": python_info,
        "api_keys": api_keys,
        "packages": packages,
        "network": network,
        "run_mode": run_mode,
        "capabilities": {
            "copyright_detection": True,
            "age_rating_scan": True,
            "adaptation_detection": True,
            "ai_deep_analysis": run_mode == "hybrid",
            "chinese_segmentation": packages.get("jieba", {}).get("installed", False),
        },
    }

    return report


if __name__ == "__main__":
    report = run_full_detection()
    print(json.dumps(report, indent=2, ensure_ascii=False))
