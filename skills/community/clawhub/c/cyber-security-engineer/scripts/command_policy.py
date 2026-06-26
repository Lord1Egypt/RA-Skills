#!/usr/bin/env python3
import json
import re
import shlex
import sys
from pathlib import Path
from typing import Dict, List, Optional


POLICY_PATH = Path.home() / ".openclaw" / "security" / "command-policy.json"


def _load_policy() -> Dict[str, object]:
    if not POLICY_PATH.exists():
        return {}
    try:
        raw = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        return raw if isinstance(raw, dict) else {}
    except Exception:
        return {}


def _compile_patterns(items: object) -> List[re.Pattern]:
    if not isinstance(items, list):
        return []
    out: List[re.Pattern] = []
    for s in items:
        if not isinstance(s, str) or not s.strip():
            continue
        try:
            out.append(re.compile(s))
        except re.error as e:
            sys.stderr.write(f"command_policy: skipping invalid regex pattern '{s}': {e}\n")
            continue
    return out


def _match_any(patterns: List[re.Pattern], text: str) -> Optional[str]:
    for p in patterns:
        if p.search(text):
            return p.pattern
    return None


def _load_exact_rules(items: object) -> List[List[str]]:
    if not isinstance(items, list):
        return []
    out: List[List[str]] = []
    for entry in items:
        if isinstance(entry, list) and all(isinstance(s, str) and s for s in entry):
            out.append(entry)
    return out


def _match_exact(rules: List[List[str]], argv: List[str]) -> bool:
    return any(rule == argv for rule in rules)


def evaluate_command(argv: List[str]) -> Dict[str, object]:
    """
    Evaluate the command argv against an optional allow/deny policy.

    Policy format (~/.openclaw/security/command-policy.json):
      {
        "allow": ["^/usr/bin/apt\\b", "^/usr/bin/brew\\b"],
        "deny":  ["\\brm\\s+-rf\\b"],
        "allow_exact": [["/usr/bin/systemctl","restart","nginx"]],
        "deny_exact":  [["/usr/bin/rm","-rf","/"]]
      }

    Behavior:
    - If policy file is missing: allow.
    - If deny_exact or deny regex matches: block.
    - If allow_exact is non-empty: require exact match.
    - Else if allow regex list is non-empty: require allow match.
    """
    cmd_str = shlex.join(argv) if argv else ""
    pol = _load_policy()
    allow = _compile_patterns(pol.get("allow"))
    deny = _compile_patterns(pol.get("deny"))
    allow_exact = _load_exact_rules(pol.get("allow_exact"))
    deny_exact = _load_exact_rules(pol.get("deny_exact"))

    if deny_exact and _match_exact(deny_exact, argv):
        return {"allowed": False, "reason": "deny_exact_match", "pattern": "exact"}

    deny_match = _match_any(deny, cmd_str)
    if deny_match:
        return {"allowed": False, "reason": "deny_match", "pattern": deny_match}

    if allow_exact:
        if not _match_exact(allow_exact, argv):
            return {"allowed": False, "reason": "not_in_allow_exact", "pattern": None}
        return {"allowed": True, "reason": "allow_exact_match", "pattern": "exact"}

    if allow:
        allow_match = _match_any(allow, cmd_str)
        if not allow_match:
            return {"allowed": False, "reason": "not_in_allowlist", "pattern": None}
        return {"allowed": True, "reason": "allow_match", "pattern": allow_match}

    return {"allowed": True, "reason": "no_policy_or_allow_empty", "pattern": None}
