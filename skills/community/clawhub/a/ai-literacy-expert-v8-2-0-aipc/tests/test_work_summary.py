"""
test_work_summary.py - V7-AIPC 新增：work_summary 模块单元测试

覆盖：
  1. WorkRecord dataclass 序列化/反序列化
  2. WorkSummaryRecorder 生命周期（begin → record → finish）
  3. 成本对比计算（local_cost=0 vs cloud_cost）
  4. 延迟对比计算（端云协同 vs 纯云端）
  5. JSONL 持久化与回读
  6. 隐私字段记录
  7. 渲染函数（控制台 / Markdown）
  8. 集成测试：完整 begin→finish 流程 + 持久化 + 读取
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

_scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
sys.path.insert(0, _scripts_dir)

from work_summary import (
    WorkRecord,
    WorkSummaryRecorder,
    render_markdown_table,
    render_console_table,
    _make_work_id,
    _now_iso,
    get_recorder,
)


class TestWorkRecordDataclass(unittest.TestCase):
    """WorkRecord dataclass 序列化/反序列化。"""

    def test_to_from_dict_roundtrip(self):
        record = WorkRecord(
            timestamp="2026-08-18T12:00:00Z",
            work_id="abc123",
            work_type="pipeline",
            theme="机器学习",
            local={"used": True, "model": "DeepSeek-R1", "device": "GPU"},
            cloud={"used": True, "model": "gpt-4o-mini", "cost_usd": 0.0008},
        )
        d = record.to_dict()
        self.assertEqual(d["work_id"], "abc123")
        self.assertEqual(d["local"]["device"], "GPU")
        # 反序列化
        record2 = WorkRecord.from_dict(d)
        self.assertEqual(record2.theme, "机器学习")
        self.assertEqual(record2.cloud["cost_usd"], 0.0008)

    def test_default_empty_dicts(self):
        record = WorkRecord(
            timestamp="2026-08-18T12:00:00Z",
            work_id="x",
            work_type="analyze",
        )
        self.assertEqual(record.local, {})
        self.assertEqual(record.cloud, {})
        self.assertEqual(record.privacy, {})


class TestMakeWorkId(unittest.TestCase):
    """work_id 生成稳定性。"""

    def test_work_id_uniqueness(self):
        id1 = _make_work_id("pipeline", "机器学习", "2026-08-18T12:00:00Z")
        id2 = _make_work_id("pipeline", "机器学习", "2026-08-18T12:00:00Z")
        self.assertEqual(id1, id2)
        id3 = _make_work_id("pipeline", "深度学习", "2026-08-18T12:00:00Z")
        self.assertNotEqual(id1, id3)
        id4 = _make_work_id("exchange", "机器学习", "2026-08-18T12:00:00Z")
        self.assertNotEqual(id1, id4)

    def test_work_id_length(self):
        wid = _make_work_id("test", "t", "ts")
        self.assertEqual(len(wid), 16)  # SHA256[:16]


class TestRecorderLifecycle(unittest.TestCase):
    """WorkSummaryRecorder 完整生命周期。"""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="work_summary_test_")
        self.path = Path(self.tmpdir) / "history.jsonl"
        self.recorder = WorkSummaryRecorder(history_path=self.path)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_begin_returns_record(self):
        r = self.recorder.begin("pipeline", theme="机器学习")
        self.assertEqual(r.work_type, "pipeline")
        self.assertEqual(r.theme, "机器学习")
        self.assertEqual(len(r.work_id), 16)
        self.assertIsNotNone(self.recorder._current)

    def test_record_local_and_cloud(self):
        self.recorder.begin("pipeline", theme="t")
        self.recorder.record_local(
            model="DeepSeek-R1-Distill-Qwen-1.5B-int4-cw-ov",
            device="GPU",
            tokens_in=350, tokens_out=200,
            latency_ms=2400.0,
            cache_hit=False,
            abstract_data_bytes=4096,
        )
        self.recorder.record_cloud(
            model="gpt-4o-mini",
            tokens_in=150, tokens_out=80,
            latency_ms=1200.0,
            cost_usd=0.0008,
            pii_detected=False,
            degradation_level=1,
        )
        record = self.recorder._current
        self.assertTrue(record.local["used"])
        self.assertEqual(record.local["tokens_in"], 350)
        self.assertEqual(record.cloud["cost_usd"], 0.0008)

    def test_record_privacy(self):
        self.recorder.begin("pipeline")
        self.recorder.record_privacy(
            raw_pii_count=4, redacted_pii_count=4, zero_upload_proof=True
        )
        self.assertEqual(self.recorder._current.privacy["raw_pii_count"], 4)
        self.assertTrue(self.recorder._current.privacy["zero_upload_proof"])

    def test_finish_computes_comparison(self):
        self.recorder.begin("pipeline", theme="t")
        self.recorder.record_local(tokens_in=100, tokens_out=50, latency_ms=2000.0)
        self.recorder.record_cloud(tokens_in=50, tokens_out=20, latency_ms=1000.0, cost_usd=0.001)
        record = self.recorder.finish()
        # 成本对比
        self.assertEqual(record.cost["local_cost_usd"], 0.0)
        self.assertEqual(record.cost["cloud_cost_usd"], 0.001)
        self.assertEqual(record.cost["saved_usd"], 0.001)
        # 延迟对比
        self.assertEqual(record.latency["local_ms"], 2000.0)
        self.assertEqual(record.latency["cloud_ms"], 1000.0)
        self.assertEqual(record.latency["edge_cloud_ms"], 3000.0)
        # finish 后 _current 应重置
        self.assertIsNone(self.recorder._current)

    def test_finish_persists_to_jsonl(self):
        self.recorder.begin("analyze", theme="t1")
        self.recorder.record_local(tokens_in=10, tokens_out=5)
        self.recorder.record_cloud(tokens_in=5, tokens_out=2, cost_usd=0.0001)
        self.recorder.finish()
        self.assertTrue(self.path.exists())
        lines = self.path.read_text(encoding="utf-8").strip().split("\n")
        self.assertEqual(len(lines), 1)
        obj = json.loads(lines[0])
        self.assertEqual(obj["work_type"], "analyze")

    def test_record_local_without_begin_warns(self):
        # 不调用 begin() 直接 record_local 不应抛异常
        self.recorder.record_local(tokens_in=10)
        self.assertIsNone(self.recorder._current)  # current 仍为 None

    def test_finish_without_begin_raises(self):
        with self.assertRaises(RuntimeError):
            self.recorder.finish()


class TestRecorderHistory(unittest.TestCase):
    """JSONL 历史读写。"""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="work_summary_history_")
        self.path = Path(self.tmpdir) / "history.jsonl"
        self.recorder = WorkSummaryRecorder(history_path=self.path)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_get_recent_empty(self):
        records = self.recorder.get_recent(5)
        self.assertEqual(records, [])

    def test_get_recent_n_records(self):
        for i in range(3):
            self.recorder.begin(f"work_{i}")
            self.recorder.record_local(tokens_in=i)
            self.recorder.record_cloud(cost_usd=0.001 * (i + 1))
            self.recorder.finish()
        records = self.recorder.get_recent(10)
        self.assertEqual(len(records), 3)
        # 验证 work_type 顺序
        self.assertEqual(records[0].work_type, "work_0")
        self.assertEqual(records[2].work_type, "work_2")

    def test_clear(self):
        for i in range(2):
            self.recorder.begin(f"work_{i}")
            self.recorder.finish()
        self.assertTrue(self.path.exists())
        n = self.recorder.clear()
        self.assertEqual(n, 2)
        self.assertFalse(self.path.exists())

    def test_corrupted_line_skipped(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # 写入 1 行正常 + 1 行损坏 + 1 行正常
        with self.path.open("w", encoding="utf-8") as f:
            f.write(json.dumps({"timestamp": "t1", "work_id": "a", "work_type": "x"}) + "\n")
            f.write("{corrupted line\n")
            f.write(json.dumps({"timestamp": "t2", "work_id": "b", "work_type": "y"}) + "\n")
        records = self.recorder.get_recent(10)
        self.assertEqual(len(records), 2)  # 损坏行被跳过


class TestRendering(unittest.TestCase):
    """渲染函数。"""

    def _make_record(self, work_type="pipeline", **overrides) -> WorkRecord:
        defaults = dict(
            timestamp="2026-08-18T12:00:00Z",
            work_id="test123",
            work_type=work_type,
            theme="测试主题",
            local={
                "used": True,
                "model": "DeepSeek-R1-Distill-Qwen-1.5B-int4-cw-ov",
                "device": "GPU",
                "tokens_in": 350, "tokens_out": 200,
                "latency_ms": 2400.0, "cache_hit": False,
                "abstract_data_bytes": 4096, "cost_usd": 0.0,
            },
            cloud={
                "used": True,
                "model": "gpt-4o-mini",
                "tokens_in": 150, "tokens_out": 80,
                "latency_ms": 1200.0, "cost_usd": 0.0008,
                "pii_detected": False, "degradation_level": 1,
            },
            privacy={
                "raw_pii_count": 4, "redacted_pii_count": 4,
                "zero_upload_proof": True,
                "upload_abstract_data_bytes": 4096,
            },
            cost={
                "local_cost_usd": 0.0, "cloud_cost_usd": 0.0008,
                "saved_usd": 0.0008, "saved_ratio_pct": 100.0,
            },
            latency={
                "local_ms": 2400.0, "cloud_ms": 1200.0,
                "edge_cloud_ms": 3600.0, "cloud_only_ms": 1200.0,
                "speedup_vs_cloud_only_pct": 0.0,
            },
        )
        defaults.update(overrides)
        return WorkRecord(**defaults)

    def test_render_markdown_table_empty(self):
        md = render_markdown_table([])
        self.assertIn("暂无工作记录", md)

    def test_render_markdown_table_one_record(self):
        r = self._make_record()
        md = render_markdown_table([r])
        self.assertIn("V7-AIPC 工作报告", md)
        self.assertIn("DeepSeek", md)
        self.assertIn("gpt-4o-mini", md)
        self.assertIn("测试主题", md)
        self.assertIn("$0.0008", md)

    def test_render_markdown_table_with_local_only(self):
        r = self._make_record()
        r.cloud = {}  # 没有云端
        md = render_markdown_table([r])
        self.assertIn("—", md)  # 云端字段显示 —

    def test_render_console_table_empty(self):
        text = render_console_table([])
        self.assertIn("暂无", text)

    def test_render_console_table_one_record(self):
        r = self._make_record()
        text = render_console_table([r])
        self.assertIn("V7-AIPC", text)
        self.assertIn("本地模型", text)
        self.assertIn("云端模型", text)
        self.assertIn("gpt-4o-mini", text)
        self.assertIn("L1", text)  # 降级等级

    def test_render_includes_privacy_field(self):
        r = self._make_record()
        text = render_console_table([r])
        self.assertIn("隐私保护", text)
        self.assertIn("PII", text)


class TestIntegration(unittest.TestCase):
    """端到端集成测试：完整流程 + 持久化 + 读取 + 渲染。"""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="work_summary_e2e_")
        self.path = Path(self.tmpdir) / "history.jsonl"
        self.recorder = WorkSummaryRecorder(history_path=self.path)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_full_pipeline_to_cloud_workflow(self):
        # 模拟 4 阶段流水线：本地推理 + 云端决策
        self.recorder.begin("pipeline", theme="机器学习", metadata={"work_dir": "/tmp/test"})
        # 阶段 2: 本地推理
        self.recorder.record_local(
            model="DeepSeek-R1-Distill-Qwen-1.5B-int4-cw-ov",
            device="GPU",
            tokens_in=500, tokens_out=300,
            latency_ms=3500.0,
            abstract_data_bytes=4096,
        )
        # 隐私：4 项 PII 全部脱敏
        self.recorder.record_privacy(
            raw_pii_count=4, redacted_pii_count=4, zero_upload_proof=True
        )
        # 阶段 4: 云端决策
        self.recorder.record_cloud(
            model="gpt-4o-mini",
            tokens_in=200, tokens_out=100,
            latency_ms=1500.0,
            cost_usd=0.0012,
            pii_detected=False,
            degradation_level=1,
        )
        record = self.recorder.finish()

        # 验证成本对比
        self.assertAlmostEqual(record.cost["saved_usd"], 0.0012, places=5)
        self.assertAlmostEqual(record.cost["saved_ratio_pct"], 100.0, places=1)
        # 验证持久化
        records = self.recorder.get_recent(1)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].work_type, "pipeline")
        self.assertEqual(records[0].theme, "机器学习")
        # 验证渲染
        md = render_markdown_table(records)
        self.assertIn("机器学习", md)
        self.assertIn("$0.0012", md)

    def test_multiple_records_ordering(self):
        # 连续 3 次工作，验证顺序
        for i in range(3):
            self.recorder.begin(f"task_{i}")
            self.recorder.record_local(tokens_in=i * 100)
            self.recorder.record_cloud(cost_usd=0.001)
            self.recorder.finish()
        records = self.recorder.get_recent(10)
        self.assertEqual(len(records), 3)
        # 验证 FIFO 顺序
        for i, r in enumerate(records):
            self.assertEqual(r.work_type, f"task_{i}")
            self.assertEqual(r.local["tokens_in"], i * 100)


if __name__ == "__main__":
    unittest.main(verbosity=2)
