#!/usr/bin/env python3
"""
Agent Scorecard — Main Evaluation Engine
=========================================
Define quality dimensions, run automated pattern-based checks,
support manual scoring with guided rubrics, and produce aggregate scores.

Usage:
    from scorecard import Scorecard
    sc = Scorecard(config)
    result = sc.evaluate(text, manual_scores={"accuracy": 4})
    print(result.summary())

Or from CLI:
    python3 scorecard.py --config scorecard_config.json --input response.txt
    python3 scorecard.py --config scorecard_config.json --input response.txt --manual
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


# ── Helpers ────────────────────────────────────────────────────────────────

def _load_config(path: str) -> Any:
    """Load configuration from a JSON file."""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Config not found: {path}")
    if not path.endswith(".json"):
        raise ValueError(f"Config must be a .json file: {path}")
    if os.path.getsize(path) > 1_000_000:
        raise ValueError(f"Config file too large (>1MB): {path}")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)



def _get(cfg: Any, name: str, default: Any = None) -> Any:
    if isinstance(cfg, dict):
        return cfg.get(name, default)
    return getattr(cfg, name, default)


# ── Automated Checks ──────────────────────────────────────────────────────

class AutoChecker:
    """Run pattern-based automated checks on text."""

    def __init__(self, checks_cfg: dict):
        self._cfg = checks_cfg

    # -- individual checks (each returns score 1-5 and detail string) ------

    def response_length(self, text: str) -> Tuple[int, str]:
        c = self._cfg.get("response_length", {})
        length = len(text)
        score = 5
        detail = f"length={length}"
        if length < c.get("min_chars", 100):
            score = max(1, score - c.get("penalty_short", 2))
            detail += " [too short]"
        elif length > c.get("max_chars", 15000):
            score = max(1, score - c.get("penalty_long", 1))
            detail += " [too long]"
        elif length < c.get("ideal_min", 300):
            score = max(1, score - 1)
            detail += " [below ideal]"
        elif length > c.get("ideal_max", 8000):
            score = max(1, score - 1)
            detail += " [above ideal]"
        return score, detail

    def format_structure(self, text: str) -> Tuple[int, str]:
        c = self._cfg.get("format_structure", {})
        score = 5
        issues: list[str] = []
        pen = c.get("missing_penalty", 1)
        if c.get("expect_headers") and not re.search(r"^#{1,6}\s", text, re.M):
            score = max(1, score - pen)
            issues.append("no headers")
        if c.get("expect_lists") and not re.search(r"^[\s]*[-*\d]\s", text, re.M):
            score = max(1, score - pen)
            issues.append("no lists")
        if c.get("expect_code_blocks") and "```" not in text:
            score = max(1, score - pen)
            issues.append("no code blocks")
        for pat in c.get("custom_patterns", []):
            try:
                if not re.search(pat, text, re.M):
                    score = max(1, score - pen)
                    issues.append(f"missing pattern: {pat}")
            except re.error:
                issues.append(f"bad regex: {pat}")
        detail = "; ".join(issues) if issues else "ok"
        return score, detail

    def code_blocks(self, text: str) -> Tuple[int, str]:
        c = self._cfg.get("code_blocks", {})
        blocks = re.findall(r"```(\w*)\n(.*?)```", text, re.S)
        score = 5
        issues: list[str] = []
        if not blocks:
            return 5, "no code blocks present"
        for lang, body in blocks:
            if c.get("require_language_tag", True) and not lang:
                score = max(1, score - 1)
                issues.append("code block missing language tag")
            max_lines = c.get("max_block_lines", 200)
            lines = body.count("\n") + 1
            if lines > max_lines:
                score = max(1, score - 1)
                issues.append(f"code block {lines} lines (max {max_lines})")
        detail = "; ".join(issues) if issues else f"{len(blocks)} blocks ok"
        return score, detail

    def _word_density_check(self, text: str, check_name: str) -> Tuple[int, str]:
        c = self._cfg.get(check_name, {})
        words = [w.lower() for w in c.get("words", c.get("markers", []))]
        text_lower = text.lower()
        hits: list[str] = []
        for w in words:
            count = text_lower.count(w)
            if count:
                hits.append(f"{w}×{count}")
        total_hits = sum(text_lower.count(w) for w in words)
        score = 5
        threshold = c.get("threshold_per_1000_chars")
        if threshold is not None:
            density = (total_hits / max(len(text), 1)) * 1000
            if density > threshold:
                score = max(1, score - c.get("penalty", 1))
        else:
            pen_per = c.get("penalty_per_hit", 1)
            max_pen = c.get("max_penalty", 3)
            penalty = min(total_hits * pen_per, max_pen)
            score = max(1, score - penalty)
        detail = ", ".join(hits) if hits else "none found"
        return score, detail

    def sycophancy(self, text: str) -> Tuple[int, str]:
        return self._word_density_check(text, "sycophancy")

    def filler_words(self, text: str) -> Tuple[int, str]:
        return self._word_density_check(text, "filler_words")

    def hedge_words(self, text: str) -> Tuple[int, str]:
        return self._word_density_check(text, "hedge_words")

    def required_sections(self, text: str) -> Tuple[int, str]:
        c = self._cfg.get("required_sections", {})
        sections = c.get("sections", [])
        if not sections:
            return 5, "no required sections configured"
        case = c.get("case_sensitive", False)
        check_text = text if case else text.lower()
        missing: list[str] = []
        for s in sections:
            target = s if case else s.lower()
            if target not in check_text:
                missing.append(s)
        pen = c.get("penalty_per_missing", 1)
        score = max(1, 5 - len(missing) * pen)
        detail = f"missing: {missing}" if missing else "all present"
        return score, detail

    def style_consistency(self, text: str) -> Tuple[int, str]:
        c = self._cfg.get("style_consistency", {})
        sentences = re.split(r"[.!?]+", text)
        sentences = [s.strip() for s in sentences if s.strip()]
        if len(sentences) < 3:
            return 5, "too few sentences to measure"
        lengths = [len(s.split()) for s in sentences]
        mean = sum(lengths) / len(lengths)
        variance = sum((l - mean) ** 2 for l in lengths) / len(lengths)
        std_dev = math.sqrt(variance)
        max_std = c.get("max_sentence_length_std_dev", 30)
        score = 5
        if std_dev > max_std:
            score = max(1, score - c.get("penalty", 1))
        detail = f"std_dev={std_dev:.1f} (max {max_std})"
        return score, detail

    def run(self, check_name: str, text: str) -> Tuple[int, str]:
        fn = getattr(self, check_name, None)
        if fn is None:
            return 5, f"unknown check: {check_name}"
        try:
            return fn(text)
        except Exception as exc:
            return 3, f"check error: {exc}"


# ── Results ───────────────────────────────────────────────────────────────

@dataclass
class DimensionResult:
    name: str
    label: str
    score: float
    weight: float
    threshold: int
    passed: bool
    auto_details: Dict[str, Tuple[int, str]] = field(default_factory=dict)
    source: str = "auto"  # "auto", "manual", "blended"
    rubric_text: str = ""


@dataclass
class EvalResult:
    dimensions: List[DimensionResult]
    overall_score: float
    overall_passed: bool
    aggregate_method: str
    agent: str = ""
    task_type: str = ""
    timestamp: str = ""
    text_length: int = 0

    def summary(self, precision: int = 2) -> str:
        lines = [
            f"Overall: {round(self.overall_score, precision)}/5 "
            f"({'PASS' if self.overall_passed else 'FAIL'})",
            f"Method: {self.aggregate_method}  |  Agent: {self.agent}  |  Task: {self.task_type}",
            "",
        ]
        for d in self.dimensions:
            status = "✓" if d.passed else "✗"
            lines.append(
                f"  {status} {d.label}: {round(d.score, precision)}/5 "
                f"(threshold {d.threshold}, weight {d.weight}) [{d.source}]"
            )
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "overall_score": self.overall_score,
            "overall_passed": self.overall_passed,
            "aggregate_method": self.aggregate_method,
            "agent": self.agent,
            "task_type": self.task_type,
            "timestamp": self.timestamp,
            "text_length": self.text_length,
            "dimensions": [
                {
                    "name": d.name,
                    "label": d.label,
                    "score": d.score,
                    "weight": d.weight,
                    "threshold": d.threshold,
                    "passed": d.passed,
                    "source": d.source,
                    "auto_details": {
                        k: {"score": v[0], "detail": v[1]}
                        for k, v in d.auto_details.items()
                    },
                }
                for d in self.dimensions
            ],
        }


# ── Scorecard Engine ──────────────────────────────────────────────────────

class Scorecard:
    """Main evaluation engine."""

    def __init__(self, config: Any):
        self.dimensions: list[dict] = _get(config, "DIMENSIONS", [])
        checks_cfg = _get(config, "AUTO_CHECKS", {})
        self.checker = AutoChecker(checks_cfg)
        self.aggregate_method: str = _get(config, "AGGREGATE_METHOD", "weighted_average")
        self.overall_threshold: float = _get(config, "OVERALL_PASS_THRESHOLD", 3.0)
        self.precision: int = _get(config, "SCORE_PRECISION", 2)
        self.default_agent: str = _get(config, "DEFAULT_AGENT", "default")
        self.default_task: str = _get(config, "DEFAULT_TASK_TYPE", "general")

    def evaluate(
        self,
        text: str,
        manual_scores: Optional[Dict[str, float]] = None,
        agent: Optional[str] = None,
        task_type: Optional[str] = None,
    ) -> EvalResult:
        """
        Evaluate text against all configured dimensions.

        Args:
            text: The agent output to evaluate.
            manual_scores: Optional dict of {dimension_name: score} for manual scoring.
            agent: Agent identifier (for tracking).
            task_type: Task category (for tracking).

        Returns:
            EvalResult with per-dimension and aggregate scores.
        """
        import datetime

        manual_scores = manual_scores or {}
        results: list[DimensionResult] = []

        for dim in self.dimensions:
            name = dim["name"]
            auto_checks = dim.get("auto_checks", [])
            threshold = dim.get("threshold", 3)
            weight = dim.get("weight", 1.0)
            label = dim.get("label", name)
            rubric = dim.get("rubric", {})

            # Run automated checks
            auto_details: Dict[str, Tuple[int, str]] = {}
            auto_scores: list[int] = []
            for check_name in auto_checks:
                s, d = self.checker.run(check_name, text)
                auto_details[check_name] = (s, d)
                auto_scores.append(s)

            auto_avg = sum(auto_scores) / len(auto_scores) if auto_scores else None

            # Determine final score
            if name in manual_scores:
                manual_s = max(1, min(5, manual_scores[name]))
                if auto_avg is not None:
                    score = (manual_s + auto_avg) / 2
                    source = "blended"
                else:
                    score = manual_s
                    source = "manual"
            elif auto_avg is not None:
                score = auto_avg
                source = "auto"
            else:
                score = 3.0  # neutral default when no data
                source = "auto"

            rubric_text = rubric.get(round(score), rubric.get(int(score), ""))

            results.append(DimensionResult(
                name=name,
                label=label,
                score=round(score, self.precision),
                weight=weight,
                threshold=threshold,
                passed=score >= threshold,
                auto_details=auto_details,
                source=source,
                rubric_text=rubric_text,
            ))

        overall = self._aggregate(results)
        return EvalResult(
            dimensions=results,
            overall_score=round(overall, self.precision),
            overall_passed=overall >= self.overall_threshold,
            aggregate_method=self.aggregate_method,
            agent=agent or self.default_agent,
            task_type=task_type or self.default_task,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            text_length=len(text),
        )

    def _aggregate(self, results: list[DimensionResult]) -> float:
        if not results:
            return 0.0
        if self.aggregate_method == "minimum":
            return min(r.score for r in results)
        if self.aggregate_method == "geometric_mean":
            product = 1.0
            for r in results:
                product *= max(r.score, 0.01)
            return product ** (1.0 / len(results))
        # weighted_average (default)
        total_weight = sum(r.weight for r in results)
        if total_weight == 0:
            return 0.0
        return sum(r.score * r.weight for r in results) / total_weight

    def interactive_manual(self, text: str) -> Dict[str, float]:
        """Guide a human through manual scoring with rubric display."""
        print("\n" + "=" * 60)
        print("MANUAL EVALUATION MODE")
        print("=" * 60)
        print(f"\nText to evaluate ({len(text)} chars):")
        print("-" * 40)
        preview = text[:500] + ("..." if len(text) > 500 else "")
        print(preview)
        print("-" * 40)

        scores: Dict[str, float] = {}
        for dim in self.dimensions:
            name = dim["name"]
            label = dim.get("label", name)
            rubric = dim.get("rubric", {})
            print(f"\n--- {label} ---")
            for level in sorted(rubric.keys()):
                print(f"  {level}: {rubric[level]}")
            while True:
                try:
                    raw = input(f"  Score for {label} (1-5, or 's' to skip): ").strip()
                    if raw.lower() == "s":
                        break
                    val = float(raw)
                    if 1 <= val <= 5:
                        scores[name] = val
                        break
                    print("  Must be 1-5.")
                except (ValueError, EOFError):
                    print("  Enter a number 1-5 or 's'.")
        return scores


# ── CLI ───────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Agent Scorecard — evaluate AI agent output quality"
    )
    parser.add_argument("--config", required=True, help="Path to config .json file")
    parser.add_argument("--input", required=True, help="Path to text file to evaluate")
    parser.add_argument("--manual", action="store_true", help="Enable interactive manual scoring")
    parser.add_argument("--agent", default=None, help="Agent identifier")
    parser.add_argument("--task", default=None, help="Task type")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of summary")
    parser.add_argument("--save", default=None, help="Append result to history file (JSONL)")
    args = parser.parse_args()

    try:
        cfg = _load_config(args.config)
    except Exception as exc:
        print(f"Error loading config: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as exc:
        print(f"Error reading input: {exc}", file=sys.stderr)
        sys.exit(1)

    sc = Scorecard(cfg)

    manual_scores: Optional[Dict[str, float]] = None
    if args.manual:
        manual_scores = sc.interactive_manual(text)

    result = sc.evaluate(text, manual_scores=manual_scores, agent=args.agent, task_type=args.task)

    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(result.summary(sc.precision))

    if args.save:
        try:
            with open(args.save, "a", encoding="utf-8") as f:
                f.write(json.dumps(result.to_dict()) + "\n")
            print(f"\nSaved to {args.save}")
        except Exception as exc:
            print(f"Error saving: {exc}", file=sys.stderr)

    sys.exit(0 if result.overall_passed else 1)


if __name__ == "__main__":
    main()
