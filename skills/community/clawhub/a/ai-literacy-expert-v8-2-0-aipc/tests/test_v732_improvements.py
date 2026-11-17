"""
test_v732_improvements.py - V7.3.2 5 项改进的单元测试

覆盖：
  改进1：_default_http_transport 多 provider 适配
  改进2：connect_timeout / read_timeout 拆分
  改进3：hardware_probe 自动硬件调度
  改进4：llm_cache SQLite 缓存
  改进5：degradation_level 上报
"""
import sys
import os
import json
import tempfile
import unittest
from pathlib import Path

_scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
sys.path.insert(0, _scripts_dir)


# ============================================================================
# 改进 1 + 2：_default_http_transport 多 provider + timeout 拆分
# ============================================================================
class TestDefaultTransportProvider(unittest.TestCase):
    """改进1：多 provider 适配。"""

    def test_resolve_provider_openai(self):
        from edge_cloud_dispatch import _resolve_provider, _PROVIDER_OPENAI
        os.environ["EDGE_CLOUD_PROVIDER"] = "openai"
        self.assertEqual(_resolve_provider("https://api.openai.com"), _PROVIDER_OPENAI)
        self.assertEqual(_resolve_provider("https://api.deepseek.com/v1"), _PROVIDER_OPENAI)

    def test_resolve_provider_anthropic(self):
        from edge_cloud_dispatch import _resolve_provider, _PROVIDER_ANTHROPIC
        os.environ["EDGE_CLOUD_PROVIDER"] = "anthropic"
        self.assertEqual(_resolve_provider("https://api.anthropic.com"), _PROVIDER_ANTHROPIC)
        del os.environ["EDGE_CLOUD_PROVIDER"]
        # URL 推断
        self.assertEqual(_resolve_provider("https://anthropic.example.com/v1"), _PROVIDER_ANTHROPIC)

    def test_v7_to_openai_request(self):
        from edge_cloud_dispatch import _v7_to_openai_request
        v7_req = {
            "intent": "生成课件",
            "abstract": {
                "task_type": "courseware_design",
                "context": "高一 AI 课",
                "abstract_data": {"kp": ["机器学习"]},
            },
            "request": {"decision_type": "creative", "max_tokens": 500},
        }
        result = _v7_to_openai_request(v7_req)
        self.assertIn("model", result)
        self.assertIn("messages", result)
        self.assertEqual(result["max_tokens"], 500)
        self.assertEqual(result["temperature"], 0.3)
        # 验证 system 消息包含 V7 协议
        system_msg = result["messages"][0]["content"]
        self.assertIn("V7 端云协同协议", system_msg)

    def test_v7_to_anthropic_request(self):
        from edge_cloud_dispatch import _v7_to_anthropic_request
        v7_req = {
            "intent": "教学策略",
            "abstract": {"task_type": "pedagogy_recommendation", "context": "", "abstract_data": {}},
            "request": {"decision_type": "educational", "max_tokens": 800},
        }
        result = _v7_to_anthropic_request(v7_req)
        self.assertIn("model", result)
        self.assertEqual(result["max_tokens"], 800)
        self.assertIn("system", result)
        self.assertIn("messages", result)

    def test_estimate_openai_cost(self):
        from edge_cloud_dispatch import _estimate_openai_cost
        os.environ["EDGE_CLOUD_MODEL"] = "gpt-4o-mini"
        usage = {"prompt_tokens": 1000, "completion_tokens": 500}
        cost = _estimate_openai_cost(usage, {})
        # 1000 * 0.00015/1000 + 500 * 0.0006/1000 = 0.00015 + 0.0003 = 0.00045
        self.assertAlmostEqual(cost, 0.00045, places=6)

    def test_openai_to_v7_response(self):
        from edge_cloud_dispatch import _openai_to_v7_response
        openai_resp = {
            "id": "chatcmpl-123",
            "model": "gpt-4o-mini",
            "choices": [{"message": {"role": "assistant", "content": "建议采用 5E 教学法"}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
        }
        v7_req = {
            "request_id": "test-req-001",
            "request": {"decision_type": "educational"},
        }
        result = _openai_to_v7_response(openai_resp, v7_req)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["request_id"], "test-req-001")
        self.assertEqual(result["data"]["decision"], "建议采用 5E 教学法")
        self.assertIn("usage", result)
        self.assertIn("cost_usd", result["usage"])

    def test_anthropic_to_v7_response(self):
        from edge_cloud_dispatch import _anthropic_to_v7_response
        anthropic_resp = {
            "id": "msg-01",
            "model": "claude-3-5-sonnet",
            "content": [{"type": "text", "text": "应当采用项目式学习"}],
            "usage": {"input_tokens": 200, "output_tokens": 100},
        }
        v7_req = {"request_id": "test-req-002"}
        result = _anthropic_to_v7_response(anthropic_resp, v7_req)
        self.assertEqual(result["status"], "success")
        self.assertIn("项目式学习", result["data"]["decision"])


class TestTransportTimeoutSplit(unittest.TestCase):
    """改进2：connect_timeout / read_timeout 拆分。"""

    def setUp(self):
        from edge_cloud_dispatch import EdgeCloudClient
        self.client_cls = EdgeCloudClient

    def test_default_timeouts(self):
        client = self.client_cls(transport=lambda r: {"status": "success"})
        # 默认 connect_timeout=5s, read_timeout=30s
        self.assertEqual(client.connect_timeout, 5.0)
        self.assertEqual(client.read_timeout, 30.0)

    def test_custom_request_timeout_compat(self):
        # 兼容旧的 request_timeout 参数（映射到 read_timeout）
        client = self.client_cls(
            transport=lambda r: {"status": "success"},
            request_timeout=10.0,
        )
        self.assertEqual(client.read_timeout, 10.0)


# ============================================================================
# 改进 3：hardware_probe 自动硬件调度
# ============================================================================
class TestHardwareProbe(unittest.TestCase):
    """改进3：自动硬件探测。"""

    def test_probe_result_dataclass(self):
        from hardware_probe import ProbeResult
        r = ProbeResult(device="GPU", npu=True, igpu=True, cpu=True, source="openvino")
        self.assertEqual(r.device, "GPU")
        self.assertTrue(r.npu)
        self.assertTrue(r.igpu)
        self.assertEqual(r.source, "openvino")

    def test_probe_returns_probe_result(self):
        from hardware_probe import probe_hardware, ProbeResult
        result = probe_hardware()
        self.assertIsInstance(result, ProbeResult)
        self.assertIn(result.device, ("NPU", "GPU", "CPU"))
        self.assertIn(result.source, ("openvino", "powershell", "static", "default"))

    def test_probe_static_env_override(self):
        from hardware_probe import probe_hardware
        # 强制 disable PowerShell 探测路径以测试静态兜底
        os.environ["AI_LITERACY_DEVICE"] = "CPU"
        os.environ["AI_LITERACY_NO_IGPU"] = "1"
        os.environ["AI_LITERACY_NO_NPU"] = "1"
        result = probe_hardware()
        # 静态路径仅在 OpenVINO + PowerShell 都失败时触发
        # 在 Windows 上可能命中 PowerShell，但仍应包含 CPU 在探测结果中
        self.assertIn(result.device, ("NPU", "GPU", "CPU"))
        if result.source == "static":
            self.assertEqual(result.device, "CPU")
        del os.environ["AI_LITERACY_DEVICE"]
        del os.environ["AI_LITERACY_NO_IGPU"]
        del os.environ["AI_LITERACY_NO_NPU"]

    def test_auto_select_with_prefer(self):
        from hardware_probe import auto_select_device
        device = auto_select_device(prefer="GPU")
        self.assertIn(device, ("NPU", "GPU", "CPU"))

    def test_auto_select_ignores_unavailable(self):
        from hardware_probe import auto_select_device
        # NPU unavailable 标记
        os.environ["AI_LITERACY_NO_NPU"] = "1"
        device = auto_select_device(prefer="NPU")
        # 即便 prefer=NPU，也应回退
        self.assertIn(device, ("GPU", "CPU"))
        del os.environ["AI_LITERACY_NO_NPU"]


# ============================================================================
# 改进 4：llm_cache SQLite 缓存
# ============================================================================
class TestLLMCache(unittest.TestCase):
    """改进4：LLM 推理结果缓存。"""

    def setUp(self):
        from llm_cache import LLMCache
        self.tmpdir = tempfile.mkdtemp(prefix="llm_cache_test_")
        self.cache = LLMCache(
            db_path=Path(self.tmpdir) / "cache.db",
            ttl_seconds=3600,
        )

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_put_and_get(self):
        abstract = {"kp": ["机器学习"], "duration_min": 45}
        result = {"decision": "建议探究式", "score": 0.95}
        self.cache.put(abstract, "educational", "gpt-4o-mini", result, cost_usd=0.001)
        cached = self.cache.get(abstract, "educational", "gpt-4o-mini")
        self.assertEqual(cached, result)

    def test_miss_returns_none(self):
        result = self.cache.get({"kp": ["未缓存"]}, "educational", "model")
        self.assertIsNone(result)

    def test_different_models_different_keys(self):
        abstract = {"kp": ["x"]}
        r1 = {"model": "gpt"}
        r2 = {"model": "claude"}
        self.cache.put(abstract, "educational", "gpt", r1)
        self.cache.put(abstract, "educational", "claude", r2)
        self.assertEqual(self.cache.get(abstract, "educational", "gpt"), r1)
        self.assertEqual(self.cache.get(abstract, "educational", "claude"), r2)

    def test_dict_order_independent(self):
        """相同内容不同 dict 顺序应命中同一缓存键。"""
        a1 = {"a": 1, "b": 2, "c": 3}
        a2 = {"c": 3, "a": 1, "b": 2}
        result = {"hit": True}
        self.cache.put(a1, "educational", "m", result)
        cached = self.cache.get(a2, "educational", "m")
        self.assertEqual(cached, result)

    def test_ttl_expiry(self):
        """TTL 过期后应自动清理。"""
        from llm_cache import LLMCache
        short_cache = LLMCache(
            db_path=Path(self.tmpdir) / "short.db",
            ttl_seconds=1,
        )
        short_cache.put({"x": 1}, "e", "m", {"v": 1})
        self.assertIsNotNone(short_cache.get({"x": 1}, "e", "m"))
        import time
        time.sleep(2.0)  # 2s > ttl 1s 触发过期
        # 过期
        self.assertIsNone(short_cache.get({"x": 1}, "e", "m"))

    def test_stats(self):
        self.cache.put({"a": 1}, "educational", "m", {"r": 1}, cost_usd=0.001)
        self.cache.put({"b": 2}, "educational", "m", {"r": 2}, cost_usd=0.002)
        self.cache.get({"a": 1}, "educational", "m")  # 1 hit
        stats = self.cache.stats()
        self.assertEqual(stats["total_entries"], 2)
        self.assertEqual(stats["total_hits"], 1)
        self.assertAlmostEqual(stats["total_cost_usd"], 0.003, places=5)

    def test_prune_and_clear(self):
        self.cache.put({"a": 1}, "e", "m", {"r": 1})
        self.cache.put({"b": 2}, "e", "m", {"r": 2})
        n = self.cache.clear()
        self.assertEqual(n, 2)
        self.assertEqual(self.cache.stats()["total_entries"], 0)


# ============================================================================
# 改进 5：degradation_level 上报
# ============================================================================
class TestDegradationReporting(unittest.TestCase):
    """改进5：degradation_level 上报到 cost_monitor。"""

    def setUp(self):
        from cost_monitor import CostMonitor
        self.tmpdir = tempfile.mkdtemp(prefix="cost_test_")
        self.monitor = CostMonitor(monthly_budget_usd=10.0, storage_dir=Path(self.tmpdir))

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_record_degradation_l4(self):
        event = self.monitor.record_degradation(
            level=4, source="edge_cloud", reason="npu_unavailable", request_id="req-001"
        )
        self.assertEqual(event["level"], 4)
        self.assertEqual(event["source"], "edge_cloud")
        self.assertEqual(event["reason"], "npu_unavailable")
        # L4+ 应写入 history
        self.assertGreaterEqual(len(self.monitor.history), 1)

    def test_record_degradation_l1(self):
        event = self.monitor.record_degradation(
            level=1, source="edge_cloud", reason="normal"
        )
        self.assertEqual(event["level"], 1)
        # L1-L3 不写入 history（避免噪声）
        # 但 degradation_log.jsonl 应有记录
        log_path = Path(self.tmpdir) / "degradation_log.jsonl"
        self.assertTrue(log_path.exists())

    def test_get_degradation_history(self):
        for i in range(5):
            self.monitor.record_degradation(
                level=4, source="edge_cloud", reason=f"event_{i}"
            )
        history = self.monitor.get_degradation_history(limit=10)
        self.assertEqual(len(history), 5)
        for e in history:
            self.assertEqual(e["source"], "edge_cloud")
            self.assertEqual(e["level"], 4)

    def test_degradation_log_jsonl_format(self):
        """验证 degradation_log.jsonl 格式正确（每行一个 JSON）。"""
        self.monitor.record_degradation(level=3, source="analyze", reason="consecutive_timeouts=2")
        self.monitor.record_degradation(level=4, source="edge_cloud", reason="npu_unavailable")
        log_path = Path(self.tmpdir) / "degradation_log.jsonl"
        self.assertTrue(log_path.exists())
        lines = log_path.read_text(encoding="utf-8").strip().split("\n")
        self.assertEqual(len(lines), 2)
        for line in lines:
            obj = json.loads(line)
            self.assertIn("timestamp", obj)
            self.assertIn("level", obj)
            self.assertIn("source", obj)


class TestEdgeCloudClientDegradationReporting(unittest.TestCase):
    """EdgeCloudClient 与 degradation 上报集成。"""

    def test_init_with_npu_unavailable_reports(self):
        from edge_cloud_dispatch import EdgeCloudClient
        from cost_monitor import CostMonitor

        tmpdir = tempfile.mkdtemp(prefix="e2e_test_")
        try:
            monitor = CostMonitor(monthly_budget_usd=10.0, storage_dir=Path(tmpdir))
            client = EdgeCloudClient(
                transport=lambda r: {"status": "success", "data": {}},
                cost_monitor=monitor,
                npu_available=False,  # 触发 L4
            )
            self.assertEqual(client.degradation_level, 4)
            # degradation_log.jsonl 应有记录
            log_path = Path(tmpdir) / "degradation_log.jsonl"
            self.assertTrue(log_path.exists())
        finally:
            import shutil
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_init_with_npu_available_no_report(self):
        from edge_cloud_dispatch import EdgeCloudClient
        from cost_monitor import CostMonitor

        tmpdir = tempfile.mkdtemp(prefix="e2e_test_")
        try:
            monitor = CostMonitor(monthly_budget_usd=10.0, storage_dir=Path(tmpdir))
            client = EdgeCloudClient(
                transport=lambda r: {"status": "success", "data": {}},
                cost_monitor=monitor,
                npu_available=True,
            )
            # L1 不应上报（避免噪声）
            self.assertEqual(client.degradation_level, 1)
            log_path = Path(tmpdir) / "degradation_log.jsonl"
            self.assertFalse(log_path.exists())
        finally:
            import shutil
            shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
