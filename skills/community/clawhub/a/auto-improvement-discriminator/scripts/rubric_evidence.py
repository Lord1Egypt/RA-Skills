#!/usr/bin/env python3
"""Phase 1 minimal skill-evaluator evidence adapter for generic-skill Critic.

This module does not run the full skill-evaluator benchmark/red-team stack.
Instead, it converts a generic-skill candidate into evaluator-friendly structured
signals using the published rubric/category/boundary rules so the Critic can
consume evidence beyond pure heuristics.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from lib.common import KEEP_CATEGORIES, protected_target

EVALUATION_STANDARDS_REF = "(see benchmark-store/interfaces/evaluation-standards.md)"
DESIGN_DOC_REF = "(internal design reference)"

CATEGORY_TO_EVALUATOR_CATEGORY = {
    "docs": "process-type",
    "reference": "process-type",
    "guardrail": "process-type",
    "workflow": "process-type",
    "prompt": "creation-type",
    "tests": "evaluation-type",
}

RUBRIC_WEIGHTS = {
    "tool-type": {
        "accuracy": 0.35,
        "reliability": 0.20,
        "efficiency": 0.25,
        "cost": 0.15,
        "coverage": 0.05,
    },
    "process-type": {
        "accuracy": 0.25,
        "reliability": 0.30,
        "efficiency": 0.20,
        "cost": 0.15,
        "coverage": 0.10,
    },
    "analysis-type": {
        "accuracy": 0.40,
        "reliability": 0.20,
        "efficiency": 0.20,
        "cost": 0.15,
        "coverage": 0.05,
    },
    "creation-type": {
        "accuracy": 0.30,
        "reliability": 0.20,
        "efficiency": 0.20,
        "cost": 0.10,
        "coverage": 0.10,
        "user_satisfaction": 0.10,
    },
    "evaluation-type": {
        "accuracy": 0.45,
        "reliability": 0.20,
        "efficiency": 0.15,
        "cost": 0.10,
        "coverage": 0.10,
        "security": 0.10,
    },
}

VERDICT_THRESHOLDS = {
    "approve": 0.80,
    "conditional": 0.60,
}


def _clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def resolve_skill_root(target_path: str) -> Path:
    target = Path(target_path).expanduser().resolve()
    if target.is_dir():
        return target
    if target.parent.name == "references":
        return target.parent.parent.resolve()
    return target.parent.resolve()


def inspect_skill_structure(skill_root: Path) -> dict[str, bool]:
    return {
        "has_skill_md": (skill_root / "SKILL.md").exists(),
        "has_readme": (skill_root / "README.md").exists(),
        "has_scripts": (skill_root / "scripts").exists(),
        "has_evals": (skill_root / "evals").exists(),
        "has_tests": (skill_root / "tests").exists(),
    }


def derive_skill_level(structure: dict[str, bool]) -> str:
    if all(
        structure.get(key, False)
        for key in ("has_skill_md", "has_readme", "has_scripts", "has_evals", "has_tests")
    ):
        return "Level 3"
    if all(structure.get(key, False) for key in ("has_skill_md", "has_scripts", "has_evals")):
        return "Level 2"
    if structure.get("has_skill_md", False):
        return "Level 1"
    return "未评级"


def candidate_to_evaluator_input(candidate: dict[str, Any]) -> dict[str, Any]:
    evaluator_category = CATEGORY_TO_EVALUATOR_CATEGORY.get(candidate.get("category"), "process-type")
    skill_root = resolve_skill_root(candidate.get("target_path", ""))
    return {
        "candidate_id": candidate.get("id"),
        "candidate_category": candidate.get("category", "unknown"),
        "candidate_title": candidate.get("title"),
        "risk_level": candidate.get("risk_level", "medium"),
        "target_path": candidate.get("target_path"),
        "skill_root": str(skill_root),
        "evaluator_category": evaluator_category,
        "execution_action": (candidate.get("execution_plan") or {}).get("action"),
        "source_ref_count": len(candidate.get("source_refs", []) or []),
        "executor_support": bool(candidate.get("executor_support")),
        "protected_target": protected_target(candidate.get("target_path", "")),
    }


def _dimension_scores(candidate: dict[str, Any], structure: dict[str, bool], skill_level: str) -> dict[str, float]:
    category = candidate.get("category", "unknown")
    risk_level = candidate.get("risk_level", "medium")
    source_ref_count = len(candidate.get("source_refs", []) or [])
    executor_support = bool(candidate.get("executor_support"))
    action = (candidate.get("execution_plan") or {}).get("action", "")
    is_protected = protected_target(candidate.get("target_path", ""))
    keep_category = category in KEEP_CATEGORIES

    level_bonus = {"Level 1": 0.03, "Level 2": 0.10, "Level 3": 0.15}.get(skill_level, 0.0)
    risk_bonus = {"low": 0.16, "medium": 0.02, "high": -0.20}.get(risk_level, 0.0)

    accuracy = 0.55 + min(source_ref_count, 3) * 0.08 + (0.07 if candidate.get("proposed_change_summary") else 0.0) + level_bonus
    reliability = 0.42 + risk_bonus + (0.18 if executor_support else -0.12) + (0.10 if keep_category else -0.06) + (0.08 if structure.get("has_scripts") else 0.0) - (0.25 if is_protected else 0.0)
    efficiency = 0.50 + (0.20 if executor_support else -0.08) + (0.15 if action == "append_markdown_section" else -0.05) - (0.05 if is_protected else 0.0)
    cost = 0.88 if action == "append_markdown_section" else 0.62
    if risk_level == "high":
        cost -= 0.10
    coverage = 0.34 + min(source_ref_count, 3) * 0.09 + (0.12 if structure.get("has_tests") else 0.0) + (0.10 if structure.get("has_evals") else 0.0) + (0.05 if category == "tests" else 0.0)
    security = 0.84 + (0.06 if category == "guardrail" else 0.0) - ({"low": 0.0, "medium": 0.18, "high": 0.35}.get(risk_level, 0.18)) - (0.20 if is_protected else 0.0)

    return {
        "accuracy": round(_clamp(accuracy), 3),
        "reliability": round(_clamp(reliability), 3),
        "efficiency": round(_clamp(efficiency), 3),
        "cost": round(_clamp(cost), 3),
        "coverage": round(_clamp(coverage), 3),
        "security": round(_clamp(security), 3),
    }


def _weighted_overall(scores: dict[str, float], evaluator_category: str) -> tuple[float, dict[str, float]]:
    raw_weights = RUBRIC_WEIGHTS.get(evaluator_category, RUBRIC_WEIGHTS["process-type"])
    usable_weights = {key: value for key, value in raw_weights.items() if key in scores}
    total = sum(usable_weights.values()) or 1.0
    normalized = {key: value / total for key, value in usable_weights.items()}
    overall = sum(scores[key] * normalized[key] for key in normalized)
    return round(overall, 3), {key: round(value, 3) for key, value in normalized.items()}


def _verdict(overall_score: float, boundary_ok: bool) -> str:
    if not boundary_ok:
        return "reject"
    if overall_score >= VERDICT_THRESHOLDS["approve"]:
        return "approve"
    if overall_score >= VERDICT_THRESHOLDS["conditional"]:
        return "conditional"
    return "reject"


def _recommendations(
    scores: dict[str, float],
    structure: dict[str, bool],
    verdict: str,
    boundary: dict[str, Any],
) -> list[dict[str, str]]:
    recs: list[dict[str, str]] = []
    if scores.get("coverage", 0.0) < 0.60:
        recs.append(
            {
                "priority": "medium",
                "category": "coverage",
                "description": "coverage 仍偏弱，当前更像 rubric-assisted 初筛，不是 benchmark-backed 评估。",
                "action": "补充 smoke cases / eval assets，再让后续 evaluator adapter 消费。",
            }
        )
    if not structure.get("has_tests"):
        recs.append(
            {
                "priority": "medium",
                "category": "tests",
                "description": "目标 skill 缺少 tests/，会限制更高等级的 evaluator 判定。",
                "action": "补 tests/ 或最小 smoke checks，为后续 hidden/frozen test 接线做准备。",
            }
        )
    if verdict == "reject" or (verdict == "conditional" and not boundary.get("auto_promote_eligible")):
        recs.append(
            {
                "priority": "high",
                "category": "gate",
                "description": "当前证据更适合 conditional/reject，不宜把复杂变更直接 auto-keep。",
                "action": "继续走 pending_promote / human review，而不是直接执行。",
            }
        )
    elif verdict == "conditional" and boundary.get("auto_promote_eligible"):
        recs.append(
            {
                "priority": "low",
                "category": "gate",
                "description": "当前是低风险可执行候选，但 evaluator 证据仍未达到 approve 档。",
                "action": "允许保守执行，同时保留后续 benchmark / hidden tests 升级空间。",
            }
        )
    return recs


def build_evaluator_evidence(candidate: dict[str, Any]) -> dict[str, Any]:
    adapted = candidate_to_evaluator_input(candidate)
    skill_root = Path(adapted["skill_root"])
    structure = inspect_skill_structure(skill_root)
    skill_level = derive_skill_level(structure)
    dimension_scores = _dimension_scores(candidate, structure, skill_level)
    overall_score_0to1, weights = _weighted_overall(dimension_scores, adapted["evaluator_category"])

    boundary = {
        "keep_category": candidate.get("category") in KEEP_CATEGORIES,
        "executor_support": adapted["executor_support"],
        "protected_target": adapted["protected_target"],
        "risk_level": adapted["risk_level"],
        "auto_promote_eligible": (
            candidate.get("category") in KEEP_CATEGORIES
            and adapted["risk_level"] == "low"
            and adapted["executor_support"]
            and not adapted["protected_target"]
        ),
    }
    verdict = _verdict(overall_score_0to1, boundary["auto_promote_eligible"] or overall_score_0to1 >= 0.60)
    limitations = [
        "Phase 1 minimal integration: uses rubric/category/boundary evidence only.",
        "Frozen benchmark not run.",
        "Hidden tests not run.",
        "External regression not run.",
    ]

    return {
        "enabled": True,
        "adapter": {
            "name": "skill-evaluator-phase1-minimal",
            "mode": "rubric-evidence",
            "design_doc": DESIGN_DOC_REF,
            "standards_ref": EVALUATION_STANDARDS_REF,
        },
        "candidate_input": adapted,
        "skill_profile": {
            "skill_root": str(skill_root),
            "structure": structure,
            "skill_level": skill_level,
        },
        "rubric": {
            "evaluator_category": adapted["evaluator_category"],
            "weights": weights,
            "thresholds": VERDICT_THRESHOLDS,
        },
        "dimension_scores": dimension_scores,
        "overall_score_0to1": overall_score_0to1,
        "overall_score_10": round(overall_score_0to1 * 10, 2),
        "verdict": verdict,
        "boundary": boundary,
        "test_tracks": {
            "frozen_benchmark": {"status": "not_run", "note": "Phase 1 only wires rubric evidence."},
            "hidden_tests": {"status": "not_run", "note": "Phase 1 only wires rubric evidence."},
            "external_regression": {"status": "not_run", "note": "Phase 1 only wires rubric evidence."},
        },
        "recommendations": _recommendations(dimension_scores, structure, verdict, boundary),
        "limitations": limitations,
    }
