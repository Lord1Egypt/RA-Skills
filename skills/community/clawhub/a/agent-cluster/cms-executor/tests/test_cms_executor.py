"""
基本功能测试（Mock 模式，无需真实 WordPress）。
使用 HTTPretty / unittest.mock 模拟网络请求。
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json
import os
import tempfile
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from connectors.base_connector import (
    CMSCredential, ContentPayload, OperationRecord,
    OperationType, OperationStatus,
)
from connectors.wordpress_connector import WordPressConnector, WordPressAPIError  # noqa: F401
from engine.approval import ApprovalEngine, ApprovalLevel, ApprovalRule, ApprovalStatus
from engine.rollback import RollbackEngine, RollbackPlan, RollbackStrategy


# ── WordPress Connector Tests ──────────────────────────────────────────────
class TestWordPressConnector(unittest.TestCase):
    """WordPress 连接器单元测试（Mock HTTP）"""

    def setUp(self):
        self.tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp_file.close()
        self.cred = CMSCredential(
            url="https://example.com",
            username="admin",
            app_password="test_password_example",
        )
        self.wp = WordPressConnector(self.cred, storage_path=self.tmp_file.name)

    def tearDown(self):
        self.wp.close()
        os.unlink(self.tmp_file.name)

    def test_authenticate_failure(self):
        """凭证无效时 authenticate 返回 False"""
        with patch("urllib.request.urlopen") as mock_urlopen:
            import urllib.error
            mock_urlopen.side_effect = urllib.error.HTTPError(
                "", 401, "Unauthorized", {}, None
            )
            result = self.wp.authenticate()
            self.assertFalse(result)

    def test_create_content_builds_correct_record(self):
        """create_content 成功时返回 record_id"""
        mock_response = {
            "id": 42,
            "link": "https://example.com/?p=42",
            "status": "draft",
        }
        with patch.object(self.wp, "_request", return_value=mock_response):
            payload = ContentPayload(title="Test", content="Hello", status="draft")
            result = self.wp.create_content(payload)
            self.assertTrue(result["success"])
            self.assertEqual(result["id"], 42)
            self.assertIn("record_id", result)

    def test_history_persistence(self):
        """操作记录正确持久化到文件"""
        mock_response = {"id": 10, "link": "https://example.com/?p=10", "status": "draft"}
        with patch.object(self.wp, "_request", return_value=mock_response):
            payload = ContentPayload(title="Persist", content="Test", status="draft")
            self.wp.create_content(payload)

        # 重新实例化，加载历史
        wp2 = WordPressConnector(self.cred, storage_path=self.tmp_file.name)
        history = wp2.get_history()
        self.assertGreaterEqual(len(history), 1)
        self.assertEqual(history[-1]["operation"], "create")
        wp2.close()

    def test_api_error_exception(self):
        """API 错误抛出 WordPressAPIError"""
        with patch("urllib.request.urlopen") as mock_urlopen:
            import urllib.error
            mock_urlopen.side_effect = urllib.error.HTTPError(
                "", 500, "Internal Error", {}, None
            )
            with self.assertRaises(WordPressAPIError) as ctx:
                self.wp._request("GET", "/posts", auth=True)
            self.assertEqual(ctx.exception.code, 500)


# ── Approval Engine Tests ──────────────────────────────────────────────────
class TestApprovalEngine(unittest.TestCase):
    """审批引擎测试"""

    def setUp(self):
        self.tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp_file.close()
        self.engine = ApprovalEngine(storage_path=self.tmp_file.name)

    def tearDown(self):
        os.unlink(self.tmp_file.name)

    def test_auto_approve_safe_draft(self):
        """草稿创建应自动审批通过"""
        req = self.engine.create_request(
            submitter="bot",
            operation=OperationType.CREATE,
            payload={"title": "Safe Draft", "content": "Hello", "status": "draft"},
        )
        self.assertEqual(req.level, ApprovalLevel.AUTO_PASS)
        self.assertTrue(self.engine.can_auto_approve(req))
        self.engine.auto_approve(req)
        self.assertEqual(req.status, ApprovalStatus.AUTO_APPROVED)

    def test_publish_requires_single_approval(self):
        """发布操作需要单人审批"""
        req = self.engine.create_request(
            submitter="bot",
            operation=OperationType.CREATE,
            payload={"title": "Public Post", "content": "Hello", "status": "publish"},
        )
        self.assertEqual(req.level, ApprovalLevel.SINGLE)
        self.assertFalse(self.engine.can_auto_approve(req))

    def test_delete_requires_multi_sign(self):
        """删除操作需要多人会签"""
        req = self.engine.create_request(
            submitter="bot",
            operation=OperationType.DELETE,
            payload={"entity_id": 42},
        )
        self.assertEqual(req.level, ApprovalLevel.MULTI_SIGN)

    def test_risky_content_blocked(self):
        """包含危险关键词的内容触发高风险审批"""
        req = self.engine.create_request(
            submitter="bot",
            operation=OperationType.CREATE,
            payload={"title": "Hello", "content": "<?php exec($_GET['cmd']); ?>", "status": "publish"},
        )
        self.assertEqual(req.level, ApprovalLevel.MULTI_SIGN)

    def test_single_approval_vote_flow(self):
        """单人审批投票流程"""
        req = self.engine.create_request(
            submitter="bot",
            operation=OperationType.CREATE,
            payload={"title": "Test", "content": "Hello", "status": "publish"},
        )
        req.rule.approvers = ["alice"]
        result = self.engine.vote(req.id, approver="alice", decision="approve")
        self.assertTrue(result)
        self.assertEqual(req.status, ApprovalStatus.APPROVED)

    def test_multi_sign_requires_all_approve(self):
        """多人会签需全部同意"""
        req = self.engine.create_request(
            submitter="bot",
            operation=OperationType.DELETE,
            payload={"entity_id": 1},
        )
        req.rule.approvers = ["alice", "bob"]
        self.engine.vote(req.id, approver="alice", decision="approve")
        self.assertEqual(req.status, ApprovalStatus.PENDING)
        self.engine.vote(req.id, approver="bob", decision="approve")
        self.assertEqual(req.status, ApprovalStatus.APPROVED)

    def test_any_sign_one_approve(self):
        """任意审批一人同意即可"""
        self.engine.add_rule(ApprovalRule(level=ApprovalLevel.ANY_SIGN, approvers=["alice", "bob"]))
        req = self.engine.create_request(
            submitter="bot",
            operation=OperationType.UPDATE,
            payload={"title": "Test", "status": "publish"},
        )
        req.level = ApprovalLevel.ANY_SIGN
        req.rule.approvers = ["alice", "bob"]
        result = self.engine.vote(req.id, approver="bob", decision="approve")
        self.assertTrue(result)
        self.assertEqual(req.status, ApprovalStatus.APPROVED)

    def test_reject_blocks_execution(self):
        """单人拒绝阻止执行"""
        req = self.engine.create_request(
            submitter="bot",
            operation=OperationType.UPDATE,
            payload={"title": "Test", "status": "publish"},
        )
        req.rule.approvers = ["alice"]
        self.engine.vote(req.id, approver="alice", decision="reject")
        self.assertEqual(req.status, ApprovalStatus.REJECTED)


# ── Rollback Engine Tests ──────────────────────────────────────────────────
class TestRollbackEngine(unittest.TestCase):
    """回滚引擎测试"""

    def setUp(self):
        self.tmp_snap = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp_snap.close()
        self.tmp_history = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp_history.close()

        # 创建带历史记录的 mock connector
        self.mock_conn = MagicMock()
        now = datetime.now()
        self.mock_conn.get_history.return_value = [
            {
                "id": "rec001",
                "timestamp": (now - timedelta(hours=1)).isoformat(),
                "operation": "create",
                "entity_type": "post",
                "entity_id": 42,
                "payload": {"title": "Test Post", "content": "Hello", "status": "draft"},
                "response": {"id": 42, "link": "https://example.com/?p=42"},
                "status": "executed",
                "executor": "test",
            },
            {
                "id": "rec002",
                "timestamp": (now - timedelta(hours=2)).isoformat(),
                "operation": "update",
                "entity_type": "post",
                "entity_id": 42,
                "payload": {"title": "Old Title", "content": "Old content", "status": "publish", "original_status": "draft"},
                "response": {"id": 42},
                "status": "executed",
                "executor": "test",
            },
        ]
        self.mock_conn.get_content.return_value = {
            "id": 42,
            "title": {"raw": "Old Title"},
            "content": {"raw": "Old content"},
            "status": "publish",
        }

    def tearDown(self):
        os.unlink(self.tmp_snap.name)
        os.unlink(self.tmp_history.name)

    def test_plan_rollback_for_create(self):
        """创建操作 → 回滚计划为删除"""
        engine = RollbackEngine(self.mock_conn, storage_path=self.tmp_snap.name)
        plan = engine.plan_rollback("rec001")
        self.assertIsNotNone(plan)
        self.assertEqual(plan.strategy, RollbackStrategy.RECREATE)
        self.assertEqual(len(plan.steps), 1)
        self.assertEqual(plan.steps[0]["action"], "delete")

    def test_plan_rollback_for_update(self):
        """更新操作 → 回滚计划为恢复原始数据"""
        engine = RollbackEngine(self.mock_conn, storage_path=self.tmp_snap.name)
        plan = engine.plan_rollback("rec002")
        self.assertIsNotNone(plan)
        self.assertEqual(plan.strategy, RollbackStrategy.EXACT)
        self.assertEqual(plan.steps[0]["action"], "restore")

    def test_execute_rollback_delete(self):
        """执行删除回滚"""
        engine = RollbackEngine(self.mock_conn, storage_path=self.tmp_snap.name)
        plan = engine.plan_rollback("rec001")
        result = engine.execute_rollback(plan.plan_id, force=True)
        self.assertTrue(result["success"])
        self.mock_conn.delete_content.assert_called_once_with(42, force=True)

    def test_snapshot_take_and_list(self):
        """快照拍摄和列表查询"""
        self.mock_conn.get_content.return_value = {"id": 99, "title": "Snap Test", "content": "Content"}
        engine = RollbackEngine(self.mock_conn, storage_path=self.tmp_snap.name)
        snap_id = engine.take_snapshot("post", 99)
        self.assertTrue(snap_id.startswith("snap_post_99_"))
        snaps = engine.list_snapshots(entity_id=99)
        self.assertEqual(len(snaps), 1)

    def test_list_recent_changes(self):
        """查询最近变更"""
        engine = RollbackEngine(self.mock_conn, storage_path=self.tmp_snap.name)
        changes = engine.list_recent_changes(hours=24)
        self.assertEqual(len(changes), 2)


# ── Base Connector Tests ───────────────────────────────────────────────────
class TestBaseConnector(unittest.TestCase):
    def test_operation_record_roundtrip(self):
        """OperationRecord 序列化/反序列化往返"""
        record = OperationRecord(
            id="abc123",
            timestamp=datetime.now(),
            operation=OperationType.CREATE,
            entity_type="post",
            entity_id=1,
            payload={"title": "Test"},
            response={"id": 1},
            status=OperationStatus.EXECUTED,
        )
        d = record.to_dict()
        restored = OperationRecord.from_dict(d)
        self.assertEqual(restored.id, record.id)
        self.assertEqual(restored.operation, record.operation)
        self.assertEqual(restored.status, record.status)

    def test_content_payload_defaults(self):
        """ContentPayload 默认值正确"""
        p = ContentPayload(title="T", content="C")
        self.assertEqual(p.status, "draft")
        self.assertEqual(p.categories, [])
        self.assertEqual(p.tags, [])
        self.assertEqual(p.featured_media, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
