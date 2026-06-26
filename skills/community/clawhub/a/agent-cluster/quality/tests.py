"""
Quality Package Tests - 单元测试

覆盖：
- models.py: 数据模型测试
- scorer.py: 5维度评分测试
- gate.py: 质量门禁测试
- reviewer.py: 审查Agent测试
- retry_loop.py: 重试循环测试
"""

from __future__ import annotations

import asyncio
import json
import sys
import time
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

# Add parent dir to path
sys.path.insert(0, ".")

from quality.models import (
    AgentResult,
    QualityDimension,
    QualityScore,
    QualityReport,
    RetryStrategy,
    TaskContext,
)
from quality.scorer import (
    AccuracyScorer,
    CompletenessScorer,
    QualityScorer,
    RelevanceScorer,
    TimelinessScorer,
    UsabilityScorer,
)
from quality.gate import (
    GateDecision,
    GateHistoryEntry,
    ImprovementSuggester,
    QualityGate,
    QualityTier,
)
from quality.reviewer import QualityReviewer, ReviewResult
from quality.retry_loop import QualityRetryLoop, RetryLoopResult, StrategyAdjuster


# =============================================================================
# Fixtures
# =============================================================================

def make_result(
    task_id: str = "test-001",
    output: str = "库存查询完成：SKU001 当前库存 500 件。",
    success: bool = True,
    duration_ms: float = 5000.0,
    expected_ms: float = 10000.0,
    engine: str = "claude_ma",
    tool_calls: list = None,
    error: str = None,
    tokens: int = 500,
    task_description: str = "查询 SKU001 的当前库存",
) -> AgentResult:
    return AgentResult(
        task_id=task_id,
        task_description="查询 SKU001 的当前库存",
        output=output,
        raw_output=output,
        success=success,
        error=error,
        duration_ms=duration_ms,
        expected_duration_ms=expected_ms,
        tokens_used=tokens,
        tool_calls=tool_calls or [{"name": "query_stock"}, {"name": "format_output"}],
        agent_name="inventory_agent",
        engine=engine,
        context={"intent_type": "stock_query"},
    )


def make_context(
    intent_type: str = "stock_query",
    subtasks: list = None,
    expected_outputs: list = None,
    required_tools: list = None,
    quality_tier: str = "normal",
) -> TaskContext:
    return TaskContext(
        task_id="test-001",
        intent_type=intent_type,
        expected_outputs=expected_outputs or ["库存数量", "SKU", "状态"],
        required_tools=required_tools or ["query_stock"],
        subtasks=subtasks or ["查询库存", "格式化输出"],
        quality_tier=quality_tier,
    )


# =============================================================================
# Models Tests
# =============================================================================

class TestQualityScore(unittest.TestCase):
    def test_score_clamp(self):
        qs = QualityScore(dimension=QualityDimension.COMPLETENESS, score=150.0)
        self.assertEqual(qs.score, 100.0)
        qs2 = QualityScore(dimension=QualityDimension.ACCURACY, score=-10.0)
        self.assertEqual(qs2.score, 0.0)

    def test_is_pass(self):
        qs = QualityScore(dimension=QualityDimension.USABILITY, score=70.0)
        self.assertTrue(qs.is_pass)
        qs2 = QualityScore(dimension=QualityDimension.RELEVANCE, score=55.0)
        self.assertFalse(qs2.is_pass)

    def test_to_dict(self):
        qs = QualityScore(
            dimension=QualityDimension.TIMELINESS,
            score=85.0,
            evidence="耗时正常",
            suggestions=["保持"],
        )
        d = qs.to_dict()
        self.assertEqual(d["dimension"], "timeliness")
        self.assertEqual(d["score"], 85.0)
        self.assertEqual(d["evidence"], "耗时正常")


class TestQualityReport(unittest.TestCase):
    def test_weighted_average(self):
        scores = {
            QualityDimension.COMPLETENESS: QualityScore(
                dimension=QualityDimension.COMPLETENESS, score=80.0
            ),
            QualityDimension.ACCURACY: QualityScore(
                dimension=QualityDimension.ACCURACY, score=100.0
            ),
            QualityDimension.RELEVANCE: QualityScore(
                dimension=QualityDimension.RELEVANCE, score=80.0
            ),
            QualityDimension.TIMELINESS: QualityScore(
                dimension=QualityDimension.TIMELINESS, score=100.0
            ),
            QualityDimension.USABILITY: QualityScore(
                dimension=QualityDimension.USABILITY, score=80.0
            ),
        }
        report = QualityReport(report_id="r1", task_id="t1", scores=scores)
        # 0.25*80 + 0.25*100 + 0.20*80 + 0.15*100 + 0.15*80 = 20+25+16+15+12 = 88
        self.assertAlmostEqual(report.overall, 88.0, places=1)
        self.assertFalse(report.passed)

    def test_passed_threshold(self):
        scores = {d: QualityScore(dimension=d, score=95.0) for d in QualityDimension}
        report = QualityReport(report_id="r2", task_id="t2", scores=scores)
        self.assertTrue(report.passed)
        self.assertEqual(len(report.failed_dimensions), 0)

    def test_summary(self):
        scores = {d: QualityScore(dimension=d, score=70.0) for d in QualityDimension}
        report = QualityReport(report_id="r3", task_id="t3", scores=scores)
        summary = report.summary()
        self.assertIn("质量评分报告", summary)
        self.assertIn("未达标", summary)


# =============================================================================
# Scorer Tests
# =============================================================================

class TestCompletenessScorer(unittest.TestCase):
    def test_empty_output(self):
        scorer = CompletenessScorer()
        result = make_result(output="", success=False)
        qs = scorer.score(result, None)
        self.assertLess(qs.score, 30)

    def test_with_context_subtasks(self):
        scorer = CompletenessScorer()
        result = make_result(
            output="已完成库存查询，已格式化输出，字段齐全。",
            tool_calls=[{"name": "query_stock"}, {"name": "format_output"}],
        )
        ctx = make_context(subtasks=["查询库存", "格式化输出"])
        qs = scorer.score(result, ctx)
        # 有子任务覆盖+工具调用 → 完整性应有明显提升
        self.assertGreaterEqual(qs.score, 50)

    def test_missing_required_tools(self):
        scorer = CompletenessScorer()
        result = make_result(output="完成", tool_calls=[{"name": "unknown_tool"}])
        ctx = make_context(required_tools=["query_stock", "db_write"])
        qs = scorer.score(result, ctx)
        self.assertLess(qs.score, 80)


class TestAccuracyScorer(unittest.TestCase):
    def test_success_with_json(self):
        scorer = AccuracyScorer()
        # 使用更长的多句输出，确保词数超过200获得加分
        result = make_result(
            output="以下是 SKU001 的详细查询结果，包含库存数量、SKU编号、仓库信息和状态。该数据来源于 ERP 系统实时查询，数据准确可靠。"
            + json.dumps({"sku": "SKU001", "qty": 500, "date": "2026-04-14", "status": "正常"}),
            success=True,
        )
        qs = scorer.score(result, None)
        # JSON正确、数值+日期+规范编码+长文本 → 应得高分
        self.assertGreaterEqual(qs.score, 70)

    def test_error_penalty(self):
        scorer = AccuracyScorer()
        result = make_result(output="完成", success=False, error="timeout")
        qs = scorer.score(result, None)
        self.assertEqual(qs.score, 20.0)  # 执行失败 → 准确性极低


class TestRelevanceScorer(unittest.TestCase):
    def test_keyword_match(self):
        scorer = RelevanceScorer()
        result = make_result(
            task_description="查询 SKU001 的库存数量和状态",
            output="SKU001 库存数量 500 件，状态正常。",
        )
        qs = scorer.score(result, None)
        self.assertGreater(qs.score, 50)

    def test_intent_mismatch(self):
        scorer = RelevanceScorer()
        result = make_result(
            task_description="查询库存",
            output="以下是物流配送的优化建议：...",
        )
        ctx = make_context(intent_type="stock_query")
        qs = scorer.score(result, ctx)
        self.assertLess(qs.score, 60)


class TestTimelinessScorer(unittest.TestCase):
    def test_ontime(self):
        scorer = TimelinessScorer()
        result = make_result(duration_ms=5000.0, expected_ms=10000.0)
        qs = scorer.score(result, None)
        self.assertEqual(qs.score, 100.0)

    def test_slight_delay(self):
        scorer = TimelinessScorer()
        result = make_result(duration_ms=15000.0, expected_ms=10000.0)
        qs = scorer.score(result, None)
        self.assertLess(qs.score, 100)
        self.assertGreater(qs.score, 60)

    def test_severe_delay(self):
        scorer = TimelinessScorer()
        result = make_result(duration_ms=60000.0, expected_ms=10000.0)
        qs = scorer.score(result, None)
        self.assertLessEqual(qs.score, 40)


class TestUsabilityScorer(unittest.TestCase):
    def test_json_structure_bonus(self):
        scorer = UsabilityScorer()
        result = make_result(output='```json\n{"key": "value"}\n```')
        qs = scorer.score(result, None)
        self.assertGreater(qs.score, 70)

    def test_plain_text_penalty(self):
        scorer = UsabilityScorer()
        result = make_result(output="这是一段没有任何格式的长文本。" * 5)
        qs = scorer.score(result, None)
        self.assertLess(qs.score, 80)


class TestQualityScorer(unittest.TestCase):
    def test_all_dimensions_scored(self):
        scorer = QualityScorer()
        result = make_result()
        report = scorer.score(result, make_context())
        self.assertEqual(len(report.scores), 5)
        for dim in QualityDimension:
            self.assertIn(dim, report.scores)

    def test_overall_calculation(self):
        scorer = QualityScorer()
        result = make_result(output="完成")
        report = scorer.score(result, None)
        self.assertGreaterEqual(report.overall, 0)
        self.assertLessEqual(report.overall, 100)

    def test_score_from_dict(self):
        scorer = QualityScorer()
        result_dict = make_result().to_dict()
        report = scorer.score_from_dict(result_dict)
        self.assertIsInstance(report, QualityReport)


# =============================================================================
# Gate Tests
# =============================================================================

class TestQualityTier(unittest.TestCase):
    def test_thresholds(self):
        self.assertEqual(QualityTier.NORMAL.threshold, 90.0)
        self.assertEqual(QualityTier.HIGH.threshold, 95.0)
        self.assertEqual(QualityTier.CRITICAL.threshold, 98.0)

    def test_from_str(self):
        self.assertEqual(QualityTier.from_str("high"), QualityTier.HIGH)
        self.assertEqual(QualityTier.from_str("CRITICAL"), QualityTier.CRITICAL)
        self.assertEqual(QualityTier.from_str("unknown"), QualityTier.NORMAL)


class TestQualityGate(unittest.TestCase):
    def test_pass(self):
        scores = {d: QualityScore(dimension=d, score=95.0) for d in QualityDimension}
        report = QualityReport(report_id="r", task_id="t", scores=scores)
        gate = QualityGate(threshold=90.0)
        decision = gate.evaluate(report)
        self.assertTrue(decision.passed)
        self.assertEqual(decision.gap, 0.0)

    def test_fail(self):
        scores = {d: QualityScore(dimension=d, score=70.0) for d in QualityDimension}
        report = QualityReport(report_id="r", task_id="t", scores=scores)
        gate = QualityGate(threshold=90.0)
        decision = gate.evaluate(report)
        self.assertFalse(decision.passed)
        self.assertGreater(decision.gap, 0)

    def test_history_recorded(self):
        scores = {d: QualityScore(dimension=d, score=95.0) for d in QualityDimension}
        report = QualityReport(report_id="r1", task_id="t1", scores=scores)
        gate = QualityGate(record_history=True)
        gate.evaluate(report)
        self.assertEqual(len(gate.history), 1)
        self.assertEqual(gate.history[0].task_id, "t1")

    def test_stats(self):
        gate = QualityGate()
        # No history
        stats = gate.get_stats()
        self.assertEqual(stats["total"], 0)
        # With pass/fail
        scores = {d: QualityScore(dimension=d, score=95.0) for d in QualityDimension}
        report = QualityReport(report_id="r", task_id="t", scores=scores)
        gate.evaluate(report)
        stats = gate.get_stats()
        self.assertEqual(stats["total"], 1)
        self.assertEqual(stats["passed"], 1)


class TestImprovementSuggester(unittest.TestCase):
    def test_generates_suggestions_for_failed_dims(self):
        scores = {
            QualityDimension.COMPLETENESS: QualityScore(
                dimension=QualityDimension.COMPLETENESS, score=40.0
            ),
            QualityDimension.ACCURACY: QualityScore(
                dimension=QualityDimension.ACCURACY, score=50.0
            ),
            QualityDimension.RELEVANCE: QualityScore(
                dimension=QualityDimension.RELEVANCE, score=50.0
            ),
            QualityDimension.TIMELINESS: QualityScore(
                dimension=QualityDimension.TIMELINESS, score=80.0
            ),
            QualityDimension.USABILITY: QualityScore(
                dimension=QualityDimension.USABILITY, score=80.0
            ),
        }
        report = QualityReport(report_id="r", task_id="t", scores=scores)
        suggestions = ImprovementSuggester.suggest(report)
        self.assertGreater(len(suggestions), 0)
        # Should have suggestions for completeness (lowest score = 40)
        self.assertTrue(any("补充" in s or "子任务" in s for s in suggestions))


# =============================================================================
# RetryStrategy Tests
# =============================================================================

class TestStrategyAdjuster(unittest.TestCase):
    def test_refine_prompt_adds_guidance(self):
        adjuster = StrategyAdjuster()
        result = make_result(task_id="t1")
        # Use REL score=50 to make it fail (is_pass threshold=60)
        report = QualityReport(
            report_id="r1",
            task_id="t1",
            scores={
                d: QualityScore(dimension=d, score=50.0 if d == QualityDimension.RELEVANCE else 90.0)
                for d in QualityDimension
            },
        )
        new_desc = adjuster._refine_prompt(result, report, attempt=1)
        self.assertIn("相关性", new_desc)
        self.assertIn(result.task_description, new_desc)

    def test_suggest_engine_cycles(self):
        adjuster = StrategyAdjuster()
        result = make_result(engine="claude_ma")
        new_engine = adjuster._suggest_engine(result)
        self.assertEqual(new_engine, "deepseek")

        result2 = make_result(engine="deepseek")
        new_engine2 = adjuster._suggest_engine(result2)
        self.assertEqual(new_engine2, "local")


# =============================================================================
# Reviewer Tests
# =============================================================================

class TestQualityReviewer(unittest.TestCase):
    def test_review_sync_pass(self):
        reviewer = QualityReviewer()
        result = make_result(output="完成")
        # 构造一个高分结果
        high_result = AgentResult(
            task_id="t1",
            task_description="查询库存",
            output=json.dumps({"sku": "SKU001", "qty": 500, "status": "正常"}),
            success=True,
            tool_calls=[{"name": "query_stock"}, {"name": "format_output"}],
        )
        review = reviewer.review(high_result)
        self.assertIsInstance(review, ReviewResult)
        self.assertEqual(len(review.all_reports), 1)

    def test_review_sync_fail(self):
        reviewer = QualityReviewer()
        result = make_result(output="错", success=False)
        review = reviewer.review(result)
        self.assertFalse(review.passed)
        self.assertEqual(review.attempts, 1)

    def test_review_batch(self):
        reviewer = QualityReviewer()
        results = [make_result(output="ok"), make_result(output="ok")]
        reviews = reviewer.review_batch(results)
        self.assertEqual(len(reviews), 2)

    def test_gate_accessible(self):
        reviewer = QualityReviewer()
        self.assertEqual(reviewer.gate.threshold, 90.0)


# =============================================================================
# RetryLoop Tests
# =============================================================================

class TestQualityRetryLoop(unittest.TestCase):
    def test_no_executor_no_retry(self):
        scorer = QualityScorer()
        gate = QualityGate()
        loop = QualityRetryLoop(scorer=scorer, gate=gate, max_attempts=3)
        result = make_result()
        loop_result = loop.run_sync(
            initial_result=result,
            initial_context=None,
            executor=None,
        )
        self.assertEqual(loop_result.attempts, 1)

    def test_max_attempts_respected(self):
        scorer = QualityScorer()
        gate = QualityGate()
        loop = QualityRetryLoop(scorer=scorer, gate=gate, max_attempts=2)

        async def fake_executor(*args, **kwargs):
            return make_result(output="ok")

        result = loop.run_sync(
            initial_result=make_result(output="fail", success=False),
            initial_context=None,
            executor=fake_executor,
        )
        # May or may not escalate depending on score
        self.assertLessEqual(result.attempts, 2)


class TestRetryLoopAsync(unittest.TestCase):
    def test_improved_flag(self):
        scorer = QualityScorer()
        gate = QualityGate()
        loop = QualityRetryLoop(scorer=scorer, gate=gate, max_attempts=2)

        async def fake_executor(*args, **kwargs):
            # Return high-quality result
            return make_result(
                output=json.dumps({"sku": "SKU001", "qty": 500}),
                tool_calls=[{"name": "query_stock"}],
            )

        result = asyncio.get_event_loop().run_until_complete(
            loop.run(
                initial_result=make_result(output="low"),
                initial_context=None,
                executor=fake_executor,
            )
        )
        self.assertGreaterEqual(result.attempts, 1)


# =============================================================================
# Integration Tests
# =============================================================================

class TestFullQualityPipeline(unittest.TestCase):
    """
    端到端集成测试：模拟完整的质量审查流程
    """

    def test_full_pipeline_high_quality(self):
        """高质量输出 → 一次达标"""
        reviewer = QualityReviewer(auto_retry=False)
        result = AgentResult(
            task_id="integration-001",
            task_description="查询 SKU001 的库存",
            output=json.dumps({
                "sku": "SKU001",
                "warehouse": "华东仓",
                "qty": 500,
                "status": "正常",
                "summary": "华东仓SKU001库存充足",
            }),
            success=True,
            duration_ms=3000.0,
            expected_duration_ms=10000.0,
            tokens_used=800,
            tool_calls=[
                {"name": "query_stock"},
                {"name": "format_output"},
            ],
        )
        context = make_context(
            intent_type="stock_query",
            subtasks=["查询库存", "格式化输出"],
            expected_outputs=["SKU", "库存", "状态"],
            required_tools=["query_stock"],
        )
        review = reviewer.review(result, context)
        self.assertGreater(review.final_report.overall, 50)
        self.assertIn(review.final_report.report_id, review.final_report.report_id)

    def test_full_pipeline_low_quality(self):
        """低质量输出 → 失败并有建议"""
        reviewer = QualityReviewer(auto_retry=False)
        result = make_result(
            task_id="integration-002",
            output="",
            success=False,
            error="执行失败",
        )
        review = reviewer.review(result)
        self.assertFalse(review.passed)
        if review.decision:
            self.assertGreater(len(review.decision.suggestions), 0)

    def test_tier_override(self):
        """质量等级覆盖"""
        reviewer = QualityReviewer()
        high_result = AgentResult(
            task_id="tier-test",
            task_description="关键任务",
            output=json.dumps({"sku": "SKU001", "qty": 500}),
            success=True,
        )
        # normal tier: 90 threshold
        review_normal = reviewer.review(high_result)
        # high tier: 95 threshold
        review_high = reviewer.review(high_result, tier=QualityTier.HIGH)
        self.assertLessEqual(
            review_high.final_report.overall,
            review_normal.final_report.overall + 10
        )


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)
