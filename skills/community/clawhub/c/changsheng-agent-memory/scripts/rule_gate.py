#!/usr/bin/env python3
"""rule_gate.py — optional action-time guardrail for ChangSheng (v0.4).

Reads .changsheng/rules.json — the user's extracted PROHIBITIONS only
("never …", "don't …", "always ask first") — and checks an action description
against them. A hit means the action violates a stated rule and should be
blocked before it runs. Positive rules ("always do X") are NOT enforced here:
they cannot be checked mechanically and are carried by the recovery-time
alignment layer instead (SKILL.md step 2b). The agent writes rules.json at
recovery; only rules the user stated as hard prohibitions belong in it.

rules.json schema (single source of truth — keep in sync with SKILL.md):
{
  "rules": [
    {"id": "r1", "text": "Never delete files without asking the user first",
     "keywords": ["delete", "remove", "rm ", "unlink"]},
    {"id": "r2", "text": "Never send external messages without approval",
     "keywords": ["send message", "publish", "post to", "email to"]}
  ]
}

Input modes:
  --check "description of the action"     plain description on argv
  (no args, piped)                         Claude Code PreToolUse JSON on stdin:
                                           {"tool_name": "Bash",
                                            "tool_input": {"command": "rm -rf x"}}

Exit codes (fail-open — never block a real action on tooling errors):
  0 = pass (also: no rules.json, empty stdin, unreadable/corrupt rules.json,
      or no keyword hit)
  2 = blocked (rule hit; the violating rule is printed to stderr)
  1 = usage error (--check given but no description)

Pure stdlib. No network. Writes nothing. MIT-0.
"""

import json
import os
import sys

RULES_FILE = ".changsheng/rules.json"


def load_rules(base: str = ".") -> list:
    path = os.path.join(base, RULES_FILE)
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []          # no rules configured → nothing to enforce
    except Exception as e:
        print(f"[rule_gate] warning: cannot read {path}: {e}", file=sys.stderr)
        return []          # corrupt rules → fail open, do not block real work
    rules = data.get("rules", []) if isinstance(data, dict) else []
    return [r for r in rules if isinstance(r, dict) and r.get("keywords")]


def check(description: str, rules: list) -> list:
    """Return the rules hit by description (empty list = pass)."""
    text = (description or "").lower()
    hits = []
    for r in rules:
        kws = [k.lower() for k in r.get("keywords", [])]
        if any(k in text for k in kws if k):
            hits.append(r)
    return hits


def _compose_from_stdin() -> str:
    """Claude Code PreToolUse hook payload → one searchable description."""
    raw = sys.stdin.read() if not sys.stdin.isatty() else ""
    if not raw.strip():
        return ""          # no payload → pass (fail open)
    try:
        obj = json.loads(raw)
    except Exception:
        return ""          # malformed payload → pass (fail open)
    tool = str(obj.get("tool_name", ""))
    ti = obj.get("tool_input") or {}
    parts = [tool]
    if isinstance(ti, dict):
        for k in ("command", "description", "prompt", "text", "query", "path"):
            v = ti.get(k)
            if v:
                parts.append(str(v))
    return " ".join(parts)


def demo() -> int:
    rules = [
        {"id": "r1", "text": "Never delete files without asking the user first",
         "keywords": ["delete", "remove", "rm ", "del ", "unlink"]},
        {"id": "r2", "text": "Never send external messages without approval",
         "keywords": ["send message", "post to", "publish", "email to"]},
    ]
    assert check("delete the whole project folder", rules)[0]["id"] == "r1"
    assert check("publish this to twitter", rules)[0]["id"] == "r2"
    assert check("summarise today's work log", rules) == []          # benign
    assert check("always reply in chinese", rules) == []             # positive rule: not gate-enforced
    print("[demo] rule_gate: 4/4 PASS")
    return 0


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        return demo()
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        desc = " ".join(sys.argv[2:])
        if not desc:
            print("[rule_gate] --check needs a description", file=sys.stderr)
            return 1
    else:
        desc = _compose_from_stdin()
        if not desc:
            return 0       # hook with no/empty payload → pass (fail open)
    hits = check(desc, load_rules())
    if hits:
        print("⛔ action blocked — violates a rule you set:", file=sys.stderr)
        for h in hits:
            print(f"   - [{h.get('id', '?')}] {h.get('text', '?')}", file=sys.stderr)
        return 2
    print("[rule_gate] pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
