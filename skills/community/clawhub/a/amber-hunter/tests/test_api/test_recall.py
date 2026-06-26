"""
tests/test_api/test_recall.py — recall 端点测试
重点验证 keyword 模式两阶段解密逻辑
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest
from unittest.mock import patch


class TestRecallTwoPhaseDecrypt:
    """
    recall keyword 模式应在 Stage 1 仅用 memo+tags 预筛，
    Stage 2 只解密 top-N 候选（默认 50 条），而非全量解密。
    """

    def test_keyword_mode_only_decrypts_top_n(self, test_client, test_db):
        """
        验证 keyword 模式两阶段解密：
        - Stage 1：所有胶囊只按 memo+tags 打分，不解密
        - Stage 2：只解密分数 top-N 的候选
        通过 mock decrypt_content 计数来验证。
        """
        from core import crypto
        import amber_hunter

        decrypt_count = 0
        original_decrypt = crypto.decrypt_content

        def counting_decrypt(*args, **kwargs):
            nonlocal decrypt_count
            decrypt_count += 1
            return original_decrypt(*args, **kwargs)

        # 准备测试胶囊（插入 60 条，每条有不同的 memo）
        from core.db import insert_capsule
        import time
        for i in range(60):
            insert_capsule(
                capsule_id=f"test-capsule-{i}",
                memo=f"test keyword {i}",
                content=f"content {i}",
                tags=f"tag{i}",
                session_id=None,
                window_title=None,
                url=None,
                created_at=time.time(),
                salt=None,
                nonce=None,
                encrypted_len=None,
                content_hash=None,
            )

        # mock amber_hunter.get_api_token 和 _semantic_available
        with patch.object(amber_hunter, 'get_api_token', return_value="test-token-12345"):
            with patch.object(amber_hunter, '_semantic_available', return_value=False):
                with patch('amber_hunter.decrypt_content', side_effect=counting_decrypt):
                    response = test_client.get(
                        "/recall",
                        params={
                            "q": "keyword test query",
                            "mode": "keyword",
                            "token": "test-token-12345",
                        },
                    )

        # 验证响应成功
        assert response.status_code == 200, f"recall failed: {response.text}"
        data = response.json()

        # keyword 模式
        assert data.get("mode") == "keyword", f"expected keyword mode, got {data.get('mode')}"

        # 关键断言：解密调用次数应 ≤ 50（top-N 限制）
        assert decrypt_count <= 50, (
            f"keyword 模式解密了 {decrypt_count} 条胶囊，"
            f"超过预定义的 top-N 限制（50）"
        )

    def test_recall_requires_auth(self, test_client):
        """recall 端点需要认证"""
        response = test_client.get("/recall?q=test&mode=keyword")
        # 无 token 时应返回 401 或 403
        assert response.status_code in (401, 403)

    def test_recall_keyword_returns_memories(self, test_client, test_db):
        """keyword 模式应返回 memories 列表"""
        import amber_hunter
        with patch.object(amber_hunter, 'get_api_token', return_value="test-token-12345"):
            with patch.object(amber_hunter, '_semantic_available', return_value=False):
                response = test_client.get(
                    "/recall",
                    params={
                        "q": "test query",
                        "mode": "keyword",
                        "token": "test-token-12345",
                    },
                )
        assert response.status_code == 200
        data = response.json()
        # memories 列表应存在
        assert "memories" in data
