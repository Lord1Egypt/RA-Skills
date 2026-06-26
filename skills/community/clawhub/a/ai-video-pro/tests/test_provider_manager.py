"""Provider 管理器测试"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from provider_manager import (
    _PROVIDER_REGISTRY,
    _BACKEND_PRIORITY,
    select_best_provider,
    VideoResult,
    JobStatus,
)


def test_provider_registry():
    """测试 Provider 注册表完整性。"""
    expected = ["lumaai", "runway", "replicate", "dalle_ffmpeg"]

    for name in expected:
        assert name in _PROVIDER_REGISTRY, f"缺少 Provider: {name}"

    # 验证所有 Provider 都有必需的方法
    for name, cls in _PROVIDER_REGISTRY.items():
        assert hasattr(cls, "generate"), f"{name} 缺少 generate 方法"
        assert hasattr(cls, "check_status"), f"{name} 缺少 check_status 方法"
        assert hasattr(cls, "download"), f"{name} 缺少 download 方法"
        assert hasattr(cls, "name"), f"{name} 缺少 name 属性"
        assert hasattr(cls, "max_duration"), f"{name} 缺少 max_duration 属性"

    print(f"Provider 注册表: PASS ({len(_PROVIDER_REGISTRY)} 个)")
    return True


def test_backend_priority():
    """测试后端优先级配置。"""
    assert len(_BACKEND_PRIORITY) >= 4, "优先级列表太短"
    assert _BACKEND_PRIORITY[0] == "comfyui", "ComfyUI 应排第一（免费）"
    assert _BACKEND_PRIORITY[-1] == "dalle_ffmpeg", "DALL-E+FFmpeg 应排最后（兜底）"

    print("后端优先级: PASS")
    return True


def test_video_result_dataclass():
    """测试 VideoResult 数据类。"""
    # 成功结果
    result = VideoResult(
        success=True,
        video_path="/tmp/test.mp4",
        provider="lumaai",
        duration_seconds=5.0,
    )
    assert result.success is True
    assert result.video_path == "/tmp/test.mp4"
    assert result.metadata == {}  # 默认空字典

    # 失败结果
    result = VideoResult(
        success=False,
        provider="runway",
        error_message="API 额度用尽",
    )
    assert result.success is False
    assert result.error_message == "API 额度用尽"

    print("VideoResult 数据类: PASS")
    return True


def test_job_status_dataclass():
    """测试 JobStatus 数据类。"""
    status = JobStatus(state="processing", progress=50.0, message="生成中")
    assert status.state == "processing"
    assert status.progress == 50.0
    assert status.result_url is None

    status = JobStatus(
        state="completed",
        progress=100.0,
        result_url="https://example.com/video.mp4",
    )
    assert status.state == "completed"
    assert status.result_url is not None

    print("JobStatus 数据类: PASS")
    return True


def test_select_best_provider_no_keys():
    """测试无 API 密钥时的选择。"""
    # 清除所有相关环境变量
    keys_to_clear = [
        "LUMAAI_API_KEY", "RUNWAY_API_KEY", "REPLICATE_API_TOKEN",
        "OPENAI_API_KEY", "KLING_API_KEY",
    ]
    original_values = {}
    for key in keys_to_clear:
        original_values[key] = os.environ.pop(key, None)

    try:
        result = select_best_provider()
        assert result is None, "无 API 密钥时应返回 None"
        print("无密钥选择: PASS")
        return True
    finally:
        # 恢复环境变量
        for key, value in original_values.items():
            if value is not None:
                os.environ[key] = value


def test_select_best_provider_with_keys():
    """测试有 API 密钥时的选择。"""
    # 设置测试环境变量
    os.environ["LUMAAI_API_KEY"] = "test_key"
    os.environ["OPENAI_API_KEY"] = "test_key"

    try:
        result = select_best_provider()
        # 应该选择优先级更高的可用 Provider
        assert result is not None, "有密钥时应返回 Provider"
        assert result in _PROVIDER_REGISTRY, f"返回的 Provider '{result}' 不在注册表中"
        print(f"有密钥选择: PASS (选择: {result})")
        return True
    finally:
        os.environ.pop("LUMAAI_API_KEY", None)
        os.environ.pop("OPENAI_API_KEY", None)


def test_provider_max_duration():
    """测试各 Provider 的最大时长配置。"""
    for name, cls in _PROVIDER_REGISTRY.items():
        # 不实例化（避免凭证检查），直接检查类属性
        assert hasattr(cls, "max_duration"), f"{name} 缺少 max_duration"
        duration = cls.max_duration
        assert isinstance(duration, int), f"{name}.max_duration 应为 int"
        assert duration > 0, f"{name}.max_duration 应大于 0"

    print("Provider 最大时长: PASS")
    return True


if __name__ == "__main__":
    print("=== Provider 管理器测试 ===\n")

    tests = [
        test_provider_registry,
        test_backend_priority,
        test_video_result_dataclass,
        test_job_status_dataclass,
        test_select_best_provider_no_keys,
        test_select_best_provider_with_keys,
        test_provider_max_duration,
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
