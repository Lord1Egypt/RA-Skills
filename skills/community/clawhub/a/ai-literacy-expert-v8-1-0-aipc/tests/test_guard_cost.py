"""
test_guard_cost.py - 规则层 + 成本监控单元测试（6 项）

覆盖：
  11. G001 知识点数量校验
  12. G007 学习目标动词校验（含英文术语）
  13. G008 成本熔断拒绝
  14. CostMonitor record_cost 累计
  15. CostMonitor alert_level 阈值
  16. CostMonitor 状态持久化
"""
import sys
import os
import json
import tempfile
import unittest
from pathlib import Path

_scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
sys.path.insert(0, _scripts_dir)

from lesson_plan_guard import validate_lesson_plan, RuleConfig
from cost_monitor import CostMonitor


class TestGuardG001(unittest.TestCase):
    """测试 G001 知识点数量校验。"""

    def test_insufficient_knowledge_points(self):
        """知识点不足应触发 G001。"""
        plan = {
            "knowledge_points": ["AI"],
            "clips": [{"knowledge_point": "AI", "difficulty": 1, "duration_sec": 120}],
            "pedagogy_method": "讲授式",
            "learning_objectives": ["了解AI基础"],
            "assessment": {"questions": [
                {"question": "Q1", "answer": "A1"},
                {"question": "Q2", "answer": "A2"},
                {"question": "Q3", "answer": "A3"},
            ]},
        }
        passed, errors = validate_lesson_plan(plan, None, None)
        self.assertFalse(passed)
        codes = [e["code"] for e in errors]
        self.assertIn("G001", codes)

    def test_sufficient_knowledge_points(self):
        """知识点充足应通过 G001。"""
        plan = {
            "knowledge_points": ["AI", "机器学习", "深度学习"],
            "clips": [{"knowledge_point": "AI", "difficulty": 1, "duration_sec": 120}],
            "pedagogy_method": "讲授式",
            "learning_objectives": ["了解AI基础"],
            "assessment": {"questions": [
                {"question": "Q1", "answer": "A1"},
                {"question": "Q2", "answer": "A2"},
                {"question": "Q3", "answer": "A3"},
            ]},
        }
        passed, errors = validate_lesson_plan(plan, None, None)
        codes = [e["code"] for e in errors]
        self.assertNotIn("G001", codes)


class TestGuardG007(unittest.TestCase):
    """测试 G007 学习目标动词校验。"""

    def test_english_term_after_verb_passes(self):
        """动词后跟英文术语应通过（如"理解 CNN 原理"）。"""
        plan = {
            "knowledge_points": ["AI", "ML", "DL"],
            "clips": [{"knowledge_point": "AI", "difficulty": 1, "duration_sec": 120}],
            "pedagogy_method": "讲授式",
            "learning_objectives": ["理解CNN原理", "掌握Python编程"],
            "assessment": {"questions": [
                {"question": "Q1", "answer": "A1"},
                {"question": "Q2", "answer": "A2"},
                {"question": "Q3", "answer": "A3"},
            ]},
        }
        passed, errors = validate_lesson_plan(plan, None, None)
        codes = [e["code"] for e in errors]
        self.assertNotIn("G007", codes,
                         "动词后跟英文术语不应触发 G007")

    def test_invalid_verb_fails(self):
        """不以合法动词开头应触发 G007。"""
        plan = {
            "knowledge_points": ["AI", "ML", "DL"],
            "clips": [{"knowledge_point": "AI", "difficulty": 1, "duration_sec": 120}],
            "pedagogy_method": "讲授式",
            "learning_objectives": ["学习AI基础"],  # "学习" 不在白名单
            "assessment": {"questions": [
                {"question": "Q1", "answer": "A1"},
                {"question": "Q2", "answer": "A2"},
                {"question": "Q3", "answer": "A3"},
            ]},
        }
        passed, errors = validate_lesson_plan(plan, None, None)
        codes = [e["code"] for e in errors]
        self.assertIn("G007", codes)


class TestGuardG008(unittest.TestCase):
    """测试 G008 成本熔断拒绝。"""

    def test_circuit_breaker_rejects_plan(self):
        """成本熔断触发时应直接拒绝。"""
        class MockCostMonitor:
            def is_circuit_breaker_triggered(self):
                return True
            cumulative_cost_usd = 100.0
            monthly_budget_usd = 10.0

        plan = {"knowledge_points": ["AI", "ML", "DL"]}
        passed, errors = validate_lesson_plan(plan, None, MockCostMonitor())
        self.assertFalse(passed)
        codes = [e["code"] for e in errors]
        self.assertIn("G008", codes)


class TestCostMonitorRecordCost(unittest.TestCase):
    """测试 CostMonitor record_cost 累计。"""

    def test_record_cost_accumulates(self):
        """多次 record_cost 应累计成本。"""
        with tempfile.TemporaryDirectory() as tmpdir:
            monitor = CostMonitor(monthly_budget_usd=10.0, storage_dir=Path(tmpdir))
            monitor.record_cost(1.5, "req-1")
            monitor.record_cost(2.0, "req-2")
            self.assertAlmostEqual(monitor.cumulative_cost_usd, 3.5, places=2)


class TestCostMonitorAlertLevel(unittest.TestCase):
    """测试 CostMonitor alert_level 阈值。"""

    def test_alert_levels(self):
        """不同累计成本应触发不同告警级别。"""
        with tempfile.TemporaryDirectory() as tmpdir:
            monitor = CostMonitor(monthly_budget_usd=10.0, storage_dir=Path(tmpdir))
            # 0% → none
            self.assertEqual(monitor.get_alert_level(), "none")
            # 50% → warning_50
            monitor.record_cost(5.0, "req-1")
            self.assertEqual(monitor.get_alert_level(), "warning_50")
            # 80% → warning_80
            monitor.record_cost(3.0, "req-2")  # total=8.0 → 80%
            self.assertEqual(monitor.get_alert_level(), "warning_80")
            # 100% → critical_100
            monitor.record_cost(2.0, "req-3")  # total=10.0 → 100%
            self.assertEqual(monitor.get_alert_level(), "critical_100")


class TestCostMonitorPersistence(unittest.TestCase):
    """测试 CostMonitor 状态持久化。"""

    def test_state_persists_across_instances(self):
        """新实例应加载之前的累计成本。"""
        with tempfile.TemporaryDirectory() as tmpdir:
            monitor1 = CostMonitor(monthly_budget_usd=10.0, storage_dir=Path(tmpdir))
            monitor1.record_cost(3.0, "req-1")

            monitor2 = CostMonitor(storage_dir=Path(tmpdir))
            self.assertAlmostEqual(monitor2.cumulative_cost_usd, 3.0, places=2)


if __name__ == "__main__":
    unittest.main()
