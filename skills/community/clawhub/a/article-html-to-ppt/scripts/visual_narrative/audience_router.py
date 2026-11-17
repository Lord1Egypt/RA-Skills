"""Choose one professional presentation route from a source-context brief.

This is deliberately separate from ``task_router``.  Task routing chooses a
visual-narrative implementation; audience routing first establishes who must
be convinced, what decision they must make, and the professional narrative
that the deck must follow.  Insufficient context blocks production rather
than silently producing a generic deck.
"""

from __future__ import annotations

from typing import Any


ROUTES = (
    "strategic_decision",
    "investor_commercial",
    "product_prd",
    "technical_architecture",
    "project_governance",
    "research_insight",
    "education_explanation",
    "brand_content_communication",
)


NARRATIVE_CONTRACTS = {
    "strategic_decision": ["decision_context", "strategic_options", "recommendation_and_tradeoffs"],
    "investor_commercial": ["market_and_thesis", "traction_and_economics", "ask_and_risks"],
    "product_prd": ["problem_and_scope", "user_flow_and_rules", "acceptance_and_open_questions"],
    "technical_architecture": ["system_context", "architecture_and_interfaces", "reliability_and_decisions"],
    "project_governance": ["outcomes_and_scope", "plan_and_dependencies", "risks_and_decisions_needed"],
    "research_insight": ["research_question", "evidence_and_findings", "implications_and_actions"],
    "education_explanation": ["learning_goal", "concept_and_examples", "practice_and_recap"],
    "brand_content_communication": ["audience_tension", "brand_story_and_proof", "call_to_action"],
}


ROUTE_SIGNALS = {
    "strategic_decision": {
        "audiences": {"executive", "leadership_team", "board", "management"},
        "objectives": {"decide", "approve_strategy", "align_strategy"},
        "materials": {"strategy_memo", "business_case", "decision_brief"},
        "scenarios": {"strategy_review", "executive_decision", "board_meeting"},
    },
    "investor_commercial": {
        "audiences": {"investor", "customer_buyer", "partner"},
        "objectives": {"raise_funding", "win_business", "commercial_due_diligence"},
        "materials": {"pitch_deck", "investment_memo", "sales_proposal"},
        "scenarios": {"fundraising", "client_pitch", "investment_committee"},
    },
    "product_prd": {
        "audiences": {"product_manager", "engineer", "designer", "tester"},
        "objectives": {"review_and_align", "approve_requirements", "plan_delivery"},
        "materials": {"prd", "product_specification", "feature_brief"},
        "scenarios": {"prd_review", "sprint_planning", "design_review"},
    },
    "technical_architecture": {
        "audiences": {"architect", "technical_lead", "developer", "security_reviewer"},
        "objectives": {"approve_architecture", "evaluate_technical_design", "align_implementation"},
        "materials": {"architecture_document", "technical_design", "rfc"},
        "scenarios": {"architecture_review", "technical_design_review", "rfc_review"},
    },
    "project_governance": {
        "audiences": {"project_sponsor", "program_manager", "steering_committee"},
        "objectives": {"govern_delivery", "resolve_risks", "approve_milestones"},
        "materials": {"project_plan", "status_report", "raid_log"},
        "scenarios": {"steering_committee", "project_status_review", "stage_gate"},
    },
    "research_insight": {
        "audiences": {"researcher", "analyst", "policy_maker"},
        "objectives": {"communicate_findings", "recommend_action", "review_evidence"},
        "materials": {"research_report", "analysis_report", "white_paper"},
        "scenarios": {"research_review", "insight_briefing", "policy_briefing"},
    },
    "education_explanation": {
        "audiences": {"learner", "student", "trainee", "new_hire"},
        "objectives": {"teach", "onboard", "explain_concept"},
        "materials": {"training_material", "course_outline", "lesson_plan"},
        "scenarios": {"training_session", "classroom", "onboarding"},
    },
    "brand_content_communication": {
        "audiences": {"consumer", "public_audience", "community"},
        "objectives": {"build_awareness", "engage_audience", "launch_campaign"},
        "materials": {"campaign_brief", "brand_brief", "content_brief"},
        "scenarios": {"campaign_launch", "social_content", "brand_presentation"},
    },
}


def route_audience(brief: Any) -> dict[str, Any]:
    """Return one route decision or a production-blocking ambiguity result."""
    if not isinstance(brief, dict) or not _has_minimum_context(brief):
        return _blocked(["AUDIENCE_ROUTE_INSUFFICIENT_CONTEXT"])

    audiences = set(_strings(brief.get("primary_audience")))
    objective = _single(brief.get("delivery_objective"))
    material = _single(brief.get("source_material_type"))
    scenario = _single(brief.get("delivery_scenario"))

    scores: dict[str, float] = {}
    evidence: dict[str, list[str]] = {}
    for route, signals in ROUTE_SIGNALS.items():
        hits: list[str] = []
        score = 0.0
        audience_hits = audiences & signals["audiences"]
        if audience_hits:
            score += min(0.4, 0.2 * len(audience_hits))
            hits.append("audience:" + ",".join(sorted(audience_hits)))
        if objective in signals["objectives"]:
            score += 0.25
            hits.append(f"objective:{objective}")
        if material in signals["materials"]:
            score += 0.2
            hits.append(f"material:{material}")
        if scenario in signals["scenarios"]:
            score += 0.15
            hits.append(f"scenario:{scenario}")
        scores[route] = round(min(score, 1.0), 2)
        evidence[route] = hits

    selected = max(ROUTES, key=scores.get)
    ranked = sorted(scores.values(), reverse=True)
    runner_up = ranked[1]
    confidence = scores[selected]
    if confidence < 0.7 or confidence - runner_up < 0.15:
        return _blocked(["AUDIENCE_ROUTE_AMBIGUOUS"], scores=scores, evidence=evidence)

    return {
        "schema_version": "1.0",
        "status": "ready",
        "selected_route": selected,
        "confidence": confidence,
        "scores": scores,
        "route_evidence": evidence[selected],
        "rejected_routes": [route for route in ROUTES if route != selected],
        "narrative_contract": {"sequence": NARRATIVE_CONTRACTS[selected]},
        "blocking_codes": [],
    }


def _has_minimum_context(brief: dict[str, Any]) -> bool:
    return bool(_strings(brief.get("primary_audience"))) and bool(_single(brief.get("delivery_objective")))


def _strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _single(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _blocked(
    blocking_codes: list[str],
    *,
    scores: dict[str, float] | None = None,
    evidence: dict[str, list[str]] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "status": "blocked",
        "selected_route": None,
        "confidence": 0.0,
        "scores": scores or {route: 0.0 for route in ROUTES},
        "route_evidence": [],
        "rejected_routes": list(ROUTES),
        "narrative_contract": None,
        "blocking_codes": blocking_codes,
        "candidate_evidence": evidence or {},
    }
