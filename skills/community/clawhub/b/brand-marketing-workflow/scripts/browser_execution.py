#!/usr/bin/env python3
"""Unified browser capability + compliance planner.

Input example:
{
  "action": "collect_public_signals",
  "data_access": "public",
  "need_login": false,
  "platform": "xiaohongshu"
}
"""
from __future__ import annotations

import json
import sys
from typing import Dict, List

ACTION_MAP = {
    "open public page": "open_public_page",
    "read public content": "read_public_content",
    "collect public signals": "collect_public_signals",
    "prepare draft publication": "prepare_draft_publication",
    "gather authorized data": "gather_authorized_data",
}

ALLOWED = {
    "open_public_page",
    "read_public_content",
    "collect_public_signals",
    "prepare_draft_publication",
    "gather_authorized_data",
}

BLOCKED = {
    "bypass_captcha",
    "bypass_login",
    "bypass_rate_limits",
    "evade_platform_controls",
    "stealth_scraping",
}


def norm_action(action: str) -> str:
    a = (action or "").strip().lower()
    return ACTION_MAP.get(a, a.replace(" ", "_"))


def capability_plan(action: str) -> List[str]:
    plans = {
        "open_public_page": ["navigate", "state", "screenshot(optional)"],
        "read_public_content": ["navigate", "state", "get_text/get_html"],
        "collect_public_signals": ["navigate", "state", "extract likes/comments/saves/public metadata"],
        "prepare_draft_publication": ["open compose page", "fill draft fields", "save draft only"],
        "gather_authorized_data": ["open authorized account scope", "read permitted metrics", "export summary"],
    }
    return plans.get(action, ["manual_review_required"])


def compliance_check(action: str, data_access: str, need_login: bool) -> Dict[str, object]:
    reasons: List[str] = []

    if action in BLOCKED:
        reasons.append(f"'{action}' is explicitly blocked")

    if action not in ALLOWED and action not in BLOCKED:
        reasons.append(f"unknown browser action '{action}' requires manual review")

    if data_access not in {"public", "authorized"}:
        reasons.append("data_access must be public or authorized")

    if need_login and action not in {"gather_authorized_data", "prepare_draft_publication"}:
        reasons.append("login-required actions must stay within authorized draft/data scopes")

    compliant = len(reasons) == 0
    decision = "allow" if compliant else "degrade"
    degrade_to = [
        "public_search",
        "official_api",
        "human_provided_samples",
    ] if not compliant else []

    return {
        "compliant": compliant,
        "decision": decision,
        "reasons": reasons,
        "degrade_to": degrade_to,
    }


def main() -> int:
    raw = sys.stdin.read().strip()
    payload = json.loads(raw) if raw else {}

    requested = payload.get("action", "")
    action = norm_action(requested)
    data_access = payload.get("data_access", "public")
    need_login = bool(payload.get("need_login", False))
    platform = payload.get("platform", "")

    policy = compliance_check(action, data_access, need_login)

    out = {
        "requested_action": requested,
        "normalized_action": action,
        "platform": platform,
        "allowed_actions": sorted(list(ALLOWED)),
        "blocked_actions": sorted(list(BLOCKED)),
        "capability_plan": capability_plan(action),
        "compliance": policy,
        "notes": "browser capability and compliance are unified: execute only within compliant scope",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
