"""
tests/test_new_endpoints.py — v1.2.31 新端点测试
覆盖: P1-2 (/config/embedding) / P2-2 (/patterns) / P2-3 (/sync/pull) / P2-1 (/extract/auto)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from unittest.mock import patch, MagicMock


class TestConfigEmbedding:
    """P1-2: /config/embedding 端点"""

    def test_get_embedding_requires_auth(self, test_client):
        """无 token 时应返回 401"""
        response = test_client.get("/config/embedding")
        assert response.status_code in (401, 403)

    def test_get_embedding_returns_config(self, test_client):
        """返回当前 embedding 配置字段"""
        import amber_hunter
        with patch.object(amber_hunter, 'get_api_token', return_value="test-token"):
            response = test_client.get(
                "/config/embedding",
                headers={"Authorization": "Bearer test-token"}
            )
        assert response.status_code == 200
        data = response.json()
        assert "provider" in data
        assert "model" in data
        assert "dimension" in data

    def test_update_embedding_config(self, test_client):
        """更新 embedding 配置"""
        import amber_hunter
        with patch.object(amber_hunter, 'get_api_token', return_value="test-token"):
            response = test_client.put(
                "/config/embedding",
                json={"provider": "openai", "model": "text-embedding-ada-002"},
                headers={"Authorization": "Bearer test-token"}
            )
        assert response.status_code == 200
        data = response.json()
        assert data["ok"] is True
        assert data["provider"] == "openai"


class TestPatternsEndpoint:
    """P2-2: /patterns 端点"""

    def test_patterns_requires_auth(self, test_client):
        """无 token 时应返回 401"""
        response = test_client.get("/patterns")
        assert response.status_code in (401, 403)

    def test_patterns_returns_structure(self, test_client):
        """返回 patterns 结构（correction_log 统计）"""
        import amber_hunter
        with patch.object(amber_hunter, 'get_api_token', return_value="test-token"):
            response = test_client.get(
                "/patterns",
                headers={"Authorization": "Bearer test-token"}
            )
        assert response.status_code == 200
        data = response.json()
        # 结构应为 {patterns: [...], summary: str, total_corrections: int}
        assert "patterns" in data
        assert "summary" in data
        assert "total_corrections" in data


class TestSyncPull:
    """P2-3: /sync/pull 端点"""

    def test_sync_pull_requires_auth(self, test_client):
        """无 token 时应返回 401"""
        response = test_client.get("/sync/pull")
        assert response.status_code in (401, 403)

    def test_sync_pull_no_master_password(self, test_client):
        """未设置 master_password 时返回 400"""
        import amber_hunter
        with patch.object(amber_hunter, 'get_api_token', return_value="test-token"):
            with patch.object(amber_hunter, 'get_master_password', return_value=None):
                response = test_client.get(
                    "/sync/pull",
                    headers={"Authorization": "Bearer test-token"}
                )
        assert response.status_code == 400
        assert "master_password" in response.json().get("error", "").lower()


class TestSyncResolve:
    """P2-3: /sync/resolve 端点"""

    def test_sync_resolve_requires_auth(self, test_client):
        """无 token 时应返回 401"""
        response = test_client.post(
            "/sync/resolve",
            json={"capsule_id": "test", "decision": "keep_local"}
        )
        assert response.status_code in (401, 403)

    def test_sync_resolve_invalid_decision(self, test_client):
        """无效 decision 时返回 400"""
        import amber_hunter
        with patch.object(amber_hunter, 'get_api_token', return_value="test-token"):
            with patch.object(amber_hunter, 'get_master_password', return_value="pw"):
                response = test_client.post(
                    "/sync/resolve",
                    json={"capsule_id": "test-capsule", "decision": "invalid"},
                    headers={"Authorization": "Bearer test-token"}
                )
        assert response.status_code == 400


class TestExtractAuto:
    """P2-1: /extract/auto 端点"""

    def test_extract_auto_returns_status(self, test_client):
        """extract/auto 不需要认证（内部 proactive hook 调用）"""
        # 不传 token 也应返回 200
        response = test_client.post("/extract/auto")
        assert response.status_code == 200
        data = response.json()
        # 状态应为 no_session（无活跃session）或 ok
        assert data["status"] in ("no_session", "ok", "too_few_messages")

    def test_extract_auto_no_session(self, test_client):
        """无活跃 session 时返回 no_session"""
        import amber_hunter
        with patch.object(amber_hunter, 'get_current_session_key', return_value=None):
            response = test_client.post("/extract/auto")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "no_session"


class TestExtractStatus:
    """P2-1: /extract/status 端点"""

    def test_extract_status_no_auth_required(self, test_client):
        """extract/status 不需要认证（内部 proactive hook 调用）"""
        response = test_client.get("/extract/status")
        assert response.status_code == 200
        data = response.json()
        assert "last_run" in data
        assert "total_extracted" in data


class TestNotifyEndpoint:
    """Push Notifications: /notify 端点"""

    def test_notify_requires_auth(self, test_client):
        """无 token 时应返回 401"""
        response = test_client.post(
            "/notify",
            json={"title": "Test", "body": "Test body"}
        )
        assert response.status_code in (401, 403)

    @pytest.mark.skip(reason="notify 端点依赖 httpx 发起真实 HTTP 请求到 huper.org，Starlette TestClient 内部绑定 httpx 导致无法 mock。改为集成测试或使用 respx 库。")
    def test_notify_returns_ok_on_success(self, test_client):
        """mock huper.org 成功时返回 ok"""
        import amber_hunter
        import httpx  # 先导入，确保 sys.modules['httpx'] 已填充

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_instance = MagicMock()
        mock_instance.post.return_value = mock_response
        mock_instance.__enter__ = MagicMock(return_value=mock_instance)
        mock_instance.__exit__ = MagicMock(return_value=False)
        mock_client_cls = MagicMock(return_value=mock_instance)

        with patch.object(amber_hunter, 'get_api_token', return_value="test-token"):
            with patch.object(amber_hunter, 'get_huper_url', return_value="https://huper.org/api"):
                with patch.object(httpx, 'Client', mock_client_cls):
                    response = test_client.post(
                        "/notify",
                        json={"title": "Test", "body": "Hello"},
                        headers={"Authorization": "Bearer test-token"}
                    )
        assert response.status_code == 200
        assert response.json().get("ok") is True


class TestReviewEndpoint:
    """Queue Terminal Format: /-review?format=json"""

    def test_review_requires_auth(self, test_client):
        """无 token 时应返回 401"""
        response = test_client.get("/-review")
        assert response.status_code in (401, 403)

    def test_review_empty_returns_count_zero(self, test_client):
        """无待审队列时返回 count=0"""
        import amber_hunter
        with patch.object(amber_hunter, 'get_api_token', return_value="test-token"):
            response = test_client.get(
                "/-review",
                headers={"Authorization": "Bearer test-token"}
            )
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0

    def test_review_json_format(self, test_client):
        """format=json 时返回完整 items 字段（空队列时 items 可能不存在）"""
        import amber_hunter
        with patch.object(amber_hunter, 'get_api_token', return_value="test-token"):
            response = test_client.get(
                "/-review?format=json",
                headers={"Authorization": "Bearer test-token"}
            )
        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert "lines" in data
        assert data["count"] == 0
