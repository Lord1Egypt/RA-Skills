"""
test_edge_cloud.py - 端云协同 SDK 单元测试（4 项）

覆盖：
  7. build_request 构建 6 段请求
  8. validate_request schema 校验
  9. EdgeCloudClient 降级状态机（NPU 不可用 → Level 4）
  10. EdgeCloudClient PII 脱敏集成
"""
import sys
import os
import unittest

_scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
sys.path.insert(0, _scripts_dir)

from edge_cloud_dispatch import (
    build_request, validate_request, EdgeCloudClient,
    PROTOCOL_VERSION, check_abstract_data_size,
)


class TestBuildRequest(unittest.TestCase):
    """测试 build_request 构建 6 段请求。"""

    def test_build_request_structure(self):
        """构建的请求应包含 8 个必填字段。"""
        req = build_request(
            intent="测试请求",
            task_type="pedagogy_recommendation",
            context="机器学习入门",
            abstract_data={"segments": []},
            decision_type="educational",
            max_tokens=500,
            max_cost_usd=0.001,
        )
        required = ["protocol_version", "request_id", "timestamp", "source",
                     "intent", "abstract", "request", "callback"]
        for k in required:
            self.assertIn(k, req, f"缺少必填字段：{k}")
        self.assertEqual(req["protocol_version"], PROTOCOL_VERSION)
        self.assertIn("abstract_data", req["abstract"])
        self.assertIn("pii_detected", req["abstract"])


class TestValidateRequest(unittest.TestCase):
    """测试 validate_request schema 校验。"""

    def test_valid_request_passes(self):
        """合法请求应通过校验。"""
        req = build_request(
            intent="测试",
            task_type="pedagogy_recommendation",
            context="上下文",
            abstract_data={"note": "test"},
            decision_type="educational",
            max_tokens=100,
            max_cost_usd=0.001,
        )
        passed, errors = validate_request(req)
        self.assertTrue(passed, f"合法请求应通过校验，错误：{errors}")

    def test_missing_field_fails(self):
        """缺少必填字段应校验失败。"""
        req = {"protocol_version": "1.0"}  # 缺少大部分字段
        passed, errors = validate_request(req)
        self.assertFalse(passed)
        self.assertGreater(len(errors), 0)


class TestDegradationStateMachine(unittest.TestCase):
    """测试 EdgeCloudClient 降级状态机。"""

    def test_npu_unavailable_degrades_to_level4(self):
        """NPU 不可用时降级级别应为 4。"""
        client = EdgeCloudClient(npu_available=False)
        self.assertEqual(client.degradation_level, 4,
                         "NPU 不可用时应自动降级到 Level 4")

    def test_npu_available_stays_level1(self):
        """NPU 可用时应保持 Level 1。"""
        client = EdgeCloudClient(npu_available=True)
        self.assertEqual(client.degradation_level, 1)


class TestPIIRedactionIntegration(unittest.TestCase):
    """测试 EdgeCloudClient PII 脱敏集成。"""

    def test_pii_redaction_in_exchange(self):
        """exchange 流程中应自动执行 PII 脱敏。"""
        def mock_transport(req):
            return {"status": "success", "data": {}}

        client = EdgeCloudClient(
            transport=mock_transport,
            npu_available=True,
        )
        req = build_request(
            intent="测试",
            task_type="pedagogy_recommendation",
            context="学生张三的记录",
            abstract_data={"student": "张三", "phone": "13812345678"},
            decision_type="educational",
            max_tokens=100,
            max_cost_usd=0.001,
        )
        resp = client.exchange(req)
        # 脱敏后 pii_detected 应为 False（已脱敏）
        self.assertEqual(resp.get("status"), "success")
        abstract = req.get("abstract", {})
        self.assertFalse(abstract.get("pii_detected", True),
                         "脱敏后 pii_detected 应为 False")


if __name__ == "__main__":
    unittest.main()
