"""Intelligence degradation evaluator.

Scores model responses against check functions, compares to baselines,
and raises alerts when degradation exceeds thresholds.
"""

from dataclasses import dataclass, field
from typing import Optional
import time

from .benchmarks.questions import ALL_QUESTIONS


@dataclass
class QuestionResult:
    """Single question evaluation result."""
    question_id: str
    category: str
    passed: bool
    weight: float
    response_length: int
    latency_ms: float = 0.0
    response_preview: str = ""


@dataclass
class CategoryScore:
    """Score for one category (math/reasoning/code)."""
    category: str
    total: int
    passed: int
    weighted_score: float  # 0.0 - 1.0
    total_weight: float
    status: str = "ok"  # ok, warn, critical
    delta_vs_baseline: Optional[float] = None
    results: list = field(default_factory=list)


@dataclass
class BenchmarkReport:
    """Full benchmark report."""
    model: str
    timestamp: float
    overall_score: float  # 0.0 - 1.0
    categories: list  # list of CategoryScore
    total_questions: int
    total_passed: int
    total_latency_ms: float
    degradation_detected: bool = False
    alerts: list = field(default_factory=list)


class IntelEvaluator:
    """Evaluate model intelligence using benchmark questions."""

    # Thresholds for degradation detection
    DEGRADE_WARN = 0.05    # 5% drop → warning
    DEGRADE_CRITICAL = 0.10  # 10% drop → critical alert

    def __init__(self):
        self.baselines = {}  # {category: weighted_score} from baseline run

    def set_baseline(self, baseline_scores: dict):
        """Set baseline scores for later comparison.
        
        baseline_scores: {category: weighted_score} or {"overall": score}
        """
        self.baselines = baseline_scores

    def evaluate_response(self, question: dict, response_text: str,
                          latency_ms: float = 0.0) -> QuestionResult:
        """Evaluate a single response against its check function."""
        check_fn = question.get("check")
        raw_prompt = question.get("prompt", question.get("question", ""))
        if check_fn is None:
            # No check function → auto-evaluate by examining response
            # Use response length + content richness as heuristic
            text = response_text.strip()
            if len(text) < 20:
                passed = False
            elif len(text) > 5000:
                # Suspiciously long = likely hallucination/rambling
                passed = len([w for w in text.split() if len(w) > 2]) / max(len(text.split()), 1) > 0.4
            else:
                passed = True
        else:
            try:
                passed = check_fn(response_text)
            except Exception:
                passed = False

        return QuestionResult(
            question_id=question.get("id", question.get("question_id", "unknown")),
            category=question.get("category", "unknown"),
            passed=passed,
            weight=question.get("weight", 1.0),
            response_length=len(response_text),
            latency_ms=latency_ms,
            response_preview=response_text[:200] + "..." if len(response_text) > 200 else response_text,
        )

    def compute_scores(self, results: list[QuestionResult]) -> BenchmarkReport:
        """Compute category and overall scores from individual results."""
        categories = {}
        for r in results:
            if r.category not in categories:
                categories[r.category] = {"total": 0, "passed": 0, "weighted": 0.0, "total_weight": 0.0, "results": []}
            cat = categories[r.category]
            cat["total"] += 1
            if r.passed:
                cat["passed"] += 1
                cat["weighted"] += r.weight
            cat["total_weight"] += r.weight
            cat["results"].append(r)

        total_passed = sum(1 for r in results if r.passed)
        total_weighted = sum(r.weight for r in results if r.passed)
        total_weight_all = sum(r.weight for r in results)
        overall_score = total_weighted / total_weight_all if total_weight_all > 0 else 0.0

        category_scores = []
        for cat_name, cat_data in categories.items():
            score = cat_data["weighted"] / cat_data["total_weight"] if cat_data["total_weight"] > 0 else 0.0
            delta = None
            status = "ok"

            if self.baselines and cat_name in self.baselines:
                baseline = self.baselines[cat_name]
                delta = score - baseline
                if delta <= -self.DEGRADE_CRITICAL:
                    status = "critical"
                elif delta <= -self.DEGRADE_WARN:
                    status = "warn"

            category_scores.append(CategoryScore(
                category=cat_name,
                total=cat_data["total"],
                passed=cat_data["passed"],
                weighted_score=score,
                total_weight=cat_data["total_weight"],
                status=status,
                delta_vs_baseline=delta,
                results=cat_data["results"],
            ))

        # Degradation alerts
        alerts = []
        for cs in category_scores:
            if cs.status == "critical":
                alerts.append(f"🚨 {cs.category}: 大幅下降 {abs(cs.delta_vs_baseline)*100:.1f}% (current={cs.weighted_score:.2%}, baseline={self.baselines.get(cs.category, 0):.2%})")
            elif cs.status == "warn":
                alerts.append(f"⚠️  {cs.category}: 轻微下降 {abs(cs.delta_vs_baseline)*100:.1f}%")

        overall_delta = None
        if self.baselines and "overall" in self.baselines:
            overall_delta = overall_score - self.baselines["overall"]
            if overall_delta <= -self.DEGRADE_CRITICAL:
                alerts.insert(0, f"🚨 OVERALL: 整体降智 {abs(overall_delta)*100:.1f}%")
                degradation_detected = True
            elif overall_delta <= -self.DEGRADE_WARN:
                alerts.insert(0, f"⚠️  OVERALL: 疑似下降 {abs(overall_delta)*100:.1f}%")
                degradation_detected = True
            else:
                degradation_detected = False
        else:
            degradation_detected = any(cs.status in ("warn", "critical") for cs in category_scores)

        total_latency = sum(r.latency_ms for r in results)

        return BenchmarkReport(
            model="unknown",
            timestamp=time.time(),
            overall_score=overall_score,
            categories=category_scores,
            total_questions=len(results),
            total_passed=total_passed,
            total_latency_ms=total_latency,
            degradation_detected=degradation_detected,
            alerts=alerts,
        )

    def build_baseline_from_report(self, report: BenchmarkReport) -> dict:
        """Extract baseline scores from a report (for subsequent comparisons)."""
        baseline = {"overall": report.overall_score}
        for cs in report.categories:
            baseline[cs.category] = cs.weighted_score
        return baseline
