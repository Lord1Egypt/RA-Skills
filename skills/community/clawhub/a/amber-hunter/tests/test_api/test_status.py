"""
tests/test_api/test_status.py — /status 端点测试
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def test_status_returns_version_and_model_state(test_client):
    """status 端点应返回版本和语义模型状态"""
    response = test_client.get("/status")
    assert response.status_code == 200
    data = response.json()

    # v1.2.41 版本
    assert data["version"] == "1.2.41"

    # 语义模型状态字段
    assert "semantic_model_state" in data
    assert "semantic_model_error" in data
    # state 应为 loading/ready/error/unavailable 之一
    assert data["semantic_model_state"] in ("loading", "ready", "error", "unavailable")


def test_status_returns_basic_info(test_client):
    """status 端点应返回服务基本信息"""
    response = test_client.get("/status")
    assert response.status_code == 200
    data = response.json()

    assert data["running"] is True
    assert "platform" in data
    assert "capsule_count" in data
    assert "queue_pending" in data
