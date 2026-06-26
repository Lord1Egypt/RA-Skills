"""环境检测测试"""

import json
import os
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from env_detect import (
    detect_gpu,
    detect_tools,
    detect_api_keys,
    detect_disk_space,
    recommend_backends,
    run_full_detection,
)


def test_detect_gpu():
    """测试 GPU 检测返回正确结构。"""
    result = detect_gpu()

    assert isinstance(result, dict), "GPU 检测应返回字典"
    assert "type" in result, "缺少 type 字段"
    assert "vram_mb" in result, "缺少 vram_mb 字段"
    assert "cuda_available" in result, "缺少 cuda_available 字段"
    assert result["type"] in ("nvidia", "amd", "apple_silicon", "none"), \
        f"未知的 GPU 类型: {result['type']}"

    print(f"GPU 检测: PASS (类型: {result['type']})")
    return True


def test_detect_tools():
    """测试工具检测返回正确结构。"""
    result = detect_tools()

    assert isinstance(result, dict), "工具检测应返回字典"
    assert "ffmpeg" in result, "缺少 ffmpeg 检测"
    assert "python" in result, "缺少 python 检测"
    assert "git" in result, "缺少 git 检测"
    assert "comfyui" in result, "缺少 comfyui 检测"
    assert "python_packages" in result, "缺少 python_packages 检测"

    # Python 应该始终被检测到
    assert result["python"]["installed"] is True, "Python 应该已安装"

    print(f"工具检测: PASS (ffmpeg: {result['ffmpeg']['installed']})")
    return True


def test_detect_api_keys():
    """测试 API 密钥检测（仅检测存在性）。"""
    result = detect_api_keys()

    assert isinstance(result, dict), "API 密钥检测应返回字典"

    expected_keys = [
        "LUMAAI_API_KEY", "RUNWAY_API_KEY", "REPLICATE_API_TOKEN",
        "OPENAI_API_KEY", "KLING_API_KEY",
    ]
    for key in expected_keys:
        assert key in result, f"缺少 {key} 检测"
        assert isinstance(result[key], bool), f"{key} 应为布尔值"

    print(f"API 密钥检测: PASS")
    return True


def test_detect_disk_space():
    """测试磁盘空间检测。"""
    result = detect_disk_space()

    assert isinstance(result, dict), "磁盘检测应返回字典"
    assert "total_gb" in result, "缺少 total_gb"
    assert "free_gb" in result, "缺少 free_gb"
    assert "sufficient_for_models" in result, "缺少 sufficient_for_models"
    assert result["total_gb"] > 0, "总空间应大于 0"

    print(f"磁盘空间: PASS ({result['free_gb']}GB 可用)")
    return True


def test_recommend_backends_no_resources():
    """测试无资源时的推荐。"""
    gpu = {"type": "none", "vram_mb": 0, "cuda_available": False}
    tools = {
        "ffmpeg": {"installed": False},
        "comfyui": {"installed": False},
    }
    api_keys = {k: False for k in [
        "LUMAAI_API_KEY", "RUNWAY_API_KEY", "REPLICATE_API_TOKEN",
        "OPENAI_API_KEY", "KLING_API_KEY",
    ]}
    disk = {"sufficient_for_models": False}

    recommendations = recommend_backends(gpu, tools, api_keys, disk)
    assert len(recommendations) > 0, "应至少有一条推荐"
    assert recommendations[0]["backend"] == "none", "无资源时应推荐 none"
    assert recommendations[0]["status"] == "需配置", "状态应为需配置"

    print("无资源推荐: PASS")
    return True


def test_recommend_backends_with_api():
    """测试有 API 密钥时的推荐。"""
    gpu = {"type": "none", "vram_mb": 0, "cuda_available": False}
    tools = {
        "ffmpeg": {"installed": True},
        "comfyui": {"installed": False},
    }
    api_keys = {
        "LUMAAI_API_KEY": True,
        "RUNWAY_API_KEY": False,
        "REPLICATE_API_TOKEN": True,
        "OPENAI_API_KEY": True,
        "KLING_API_KEY": False,
    }
    disk = {"sufficient_for_models": False}

    recommendations = recommend_backends(gpu, tools, api_keys, disk)
    assert len(recommendations) >= 2, "应有多个推荐"

    # Replicate 应排在 LumaAI 前面（优先级更高）
    backends = [r["backend"] for r in recommendations]
    assert "replicate" in backends, "应包含 replicate"
    assert "lumaai" in backends, "应包含 lumaai"

    print("有 API 推荐: PASS")
    return True


def test_full_detection_structure():
    """测试完整检测报告的结构。"""
    report = run_full_detection()

    assert "system" in report, "缺少 system"
    assert "gpu" in report, "缺少 gpu"
    assert "tools" in report, "缺少 tools"
    assert "api_keys" in report, "缺少 api_keys"
    assert "disk" in report, "缺少 disk"
    assert "network" in report, "缺少 network"
    assert "recommendations" in report, "缺少 recommendations"

    # 验证 JSON 序列化
    json_str = json.dumps(report, ensure_ascii=False)
    assert len(json_str) > 100, "报告内容太少"

    print("完整检测结构: PASS")
    return True


if __name__ == "__main__":
    print("=== 环境检测测试 ===\n")

    tests = [
        test_detect_gpu,
        test_detect_tools,
        test_detect_api_keys,
        test_detect_disk_space,
        test_recommend_backends_no_resources,
        test_recommend_backends_with_api,
        test_full_detection_structure,
    ]

    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"  FAIL: {test.__name__}: {e}")
            results.append(False)

    passed = sum(results)
    total = len(results)
    print(f"\n总计: {passed}/{total} 通过")
    sys.exit(0 if passed == total else 1)
