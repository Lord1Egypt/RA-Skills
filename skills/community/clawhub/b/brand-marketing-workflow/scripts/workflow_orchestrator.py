#!/usr/bin/env python3
"""Brand marketing workflow orchestrator.

This is a transparent, minimal-but-real orchestration layer that turns loose
brand input into a structured brief, strategy summary, parallel work plan,
competitor summary, performance evaluation, and iteration plan.
"""
from __future__ import annotations

import json
import sys
from typing import Any, Dict, List

DEFAULT_CHANNELS = ["xiaohongshu", "weibo", "douyin"]
DEFAULT_GOALS = ["content production", "brand awareness", "iteration"]


def normalize(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "brand_name": payload.get("brand_name", ""),
        "brand_positioning": payload.get("brand_positioning", ""),
        "brand_tone": payload.get("brand_tone", ""),
        "target_audience": payload.get("target_audience", []) or [],
        "use_cases": payload.get("use_cases", []) or [],
        "channels": payload.get("channels", []) or DEFAULT_CHANNELS,
        "content_goals": payload.get("content_goals", []) or DEFAULT_GOALS,
        "brand_dos": payload.get("brand_dos", []) or [],
        "brand_donts": payload.get("brand_donts", []) or [],
        "competitor_scope": payload.get("competitor_scope", []) or [],
        "kpis": payload.get("kpis", []) or [],
        "constraints": payload.get("constraints", {}) or {},
    }


def build_brand_brief(data: Dict[str, Any]) -> Dict[str, Any]:
    summary = {
        "positioning": data["brand_positioning"] or "to be clarified",
        "tone": data["brand_tone"] or "to be clarified",
        "audience": ", ".join(data["target_audience"]) or "to be clarified",
        "goals": ", ".join(data["content_goals"]),
    }
    constraints = data.get("constraints", {})
    return {
        "brand_summary": summary,
        "channels": data["channels"],
        "use_cases": data["use_cases"],
        "dos": data["brand_dos"],
        "donts": data["brand_donts"],
        "competitor_scope": data["competitor_scope"],
        "kpis": data["kpis"],
        "constraints": constraints,
        "low_confidence": not bool(data["brand_name"]) or not bool(data["brand_tone"]),
    }


def generate_strategy(brief: Dict[str, Any]) -> Dict[str, Any]:
    channels = brief["channels"]
    tone = brief["brand_summary"]["tone"]
    return {
        "content_pillars": [
            "brand story",
            "product utility",
            "social proof",
            "platform-native education",
        ],
        "style_rules": [
            f"tone={tone}",
            "preserve brand constraints",
            "prefer reusable post patterns",
        ],
        "channel_rules": {ch: ["adapt to channel format", "keep public/authorized-only data"] for ch in channels},
        "keywords": [brief["brand_summary"]["positioning"], tone],
    }


def run_parallel_plan(data: Dict[str, Any], strategy: Dict[str, Any]) -> Dict[str, Any]:
    competitor_scope = data["competitor_scope"] or ["public competitor signals"]
    content_assets = {
        "topics": ["introductory brand story", "product use-case story"],
        "titles": [f"{data['brand_name'] or 'Brand'}: why it matters"],
        "posts": ["Draft post placeholder"],
        "scripts": ["Draft short-form script placeholder"],
        "comment_replies": ["Reply template placeholder"],
    }
    competitor_report = {
        "competitors": competitor_scope,
        "themes": ["minimal", "story", "utility"],
        "patterns": ["short-form hooks", "platform-native formatting"],
        "frequency": "unknown until public/authorized data is supplied",
        "engagement_signals": ["likes", "comments", "saves"],
        "gaps": ["differentiation opportunity pending deeper analysis"],
    }
    performance_report = {
        "kpis": data["kpis"] or ["reach", "engagement", "conversion"],
        "scores": {
            "brand_consistency": 4,
            "channel_fit": 4,
            "content_effect": 3,
            "competitor_advantage": 3,
        },
        "issues": ["placeholder scoring until real content/data is provided"],
        "recommendations": ["produce first content batch", "collect public signals", "re-score next cycle"],
    }
    iteration_plan = {
        "changes_for_next_cycle": [
            "Refine content pillars based on observed engagement",
            "Add competitor examples from public/authorized sources",
            "Tune platform variants for strongest channel",
        ],
        "human_approval_needed": False,
    }
    return {
        "content_assets": content_assets,
        "competitor_report": competitor_report,
        "performance_report": performance_report,
        "iteration_plan": iteration_plan,
    }


def browser_snapshot(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = (payload.get("browser_action") or "collect_public_signals").strip().lower().replace(" ", "_")
    data_access = payload.get("data_access", "public")
    need_login = bool(payload.get("need_login", False))

    reasons: List[str] = []
    blocked = {"bypass_captcha", "bypass_login", "bypass_rate_limits", "evade_platform_controls", "stealth_scraping"}
    allowed = {"open_public_page", "read_public_content", "collect_public_signals", "prepare_draft_publication", "gather_authorized_data"}

    if action in blocked:
        reasons.append(f"browser action '{action}' is blocked")
    if action not in allowed and action not in blocked:
        reasons.append(f"unknown browser action '{action}' requires manual review")
    if data_access not in {"public", "authorized"}:
        reasons.append("browser data access must be public/authorized")
    if need_login and action not in {"gather_authorized_data", "prepare_draft_publication"}:
        reasons.append("login-required browser work must stay within authorized draft/data scope")

    return {
        "action": action,
        "data_access": data_access,
        "need_login": need_login,
        "compliant": len(reasons) == 0,
        "decision": "allow" if len(reasons) == 0 else "degrade",
        "reasons": reasons,
        "degrade_to": [] if len(reasons) == 0 else ["public_search", "official_api", "human_provided_samples"],
    }


def authorization_snapshot(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("execution_action", "draft_prepare")
    data_access = payload.get("data_access", "public")
    requires_payment = bool(payload.get("requires_payment", False))

    reasons: List[str] = []
    if action in {"publish", "ad_launch", "authorized_data_access"}:
        reasons.append(f"action '{action}' requires human confirmation")
    if action in {"payment", "recharge"} or requires_payment:
        reasons.append("payment/recharge requires explicit authorization")
    if data_access not in {"public", "authorized"}:
        reasons.append("data access scope unclear; public/authorized-only")

    return {
        "action": action,
        "data_access": data_access,
        "requires_payment": requires_payment,
        "has_boundary": len(reasons) > 0,
        "reasons": reasons,
        "recommended_state": "awaiting_confirmation" if reasons else "running",
        "recommended_decision": "pause" if reasons else "allow",
    }


def main() -> int:
    raw = sys.stdin.read().strip()
    payload = json.loads(raw) if raw else {}
    data = normalize(payload)
    brief = build_brand_brief(data)
    strategy = generate_strategy(brief)
    parallel = run_parallel_plan(data, strategy)
    browser = browser_snapshot(payload)
    auth = authorization_snapshot(payload)
    if auth["has_boundary"]:
        parallel["iteration_plan"]["human_approval_needed"] = True
    if not browser["compliant"]:
        parallel["performance_report"]["issues"].append("browser plan degraded to compliant fallback path")
        parallel["performance_report"]["recommendations"].append("use public/API/manual sources until browser action becomes compliant")

    result = {
        "workflow_steps": [
            "normalize_input",
            "build_brand_brief",
            "generate_strategy",
            "parallel_content_competitor_kpi_channel",
            "evaluate_performance",
            "synthesize_insights",
            "iteration_plan",
        ],
        "brand_brief": brief,
        "content_strategy": strategy,
        **parallel,
        "browser": browser,
        "authorization": auth,
        "status": "ready_for_iteration",
        "low_confidence": brief["low_confidence"],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
