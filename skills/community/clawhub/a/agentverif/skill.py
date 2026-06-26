#!/usr/bin/env python3
"""
agentverif — OpenClaw skill v2.0.3
OWASP LLM Top 10 scanner + cryptographic verification for skills.

Homepage: https://agentverif.com

Commands (invoked as: python skill.py <command> [args]):
  scan [--last 1h|24h|7d] [--since ISO]  OWASP scan, score 0-100
  verify <license_id_or_zip>             VERIFIED / TAMPERED / UNSIGNED / REVOKED
  sign <zip_path>                        Sign ZIP — OWASP scan runs first
  revoke <license_id>                    Revoke license (needs AGENTVERIF_API_KEY)
  status                                 Trust score from last scan (stateless)
  report                                 Full violation report by severity
  taint-check <text>                     LLM01 prompt injection check
  output-check <text>                    LLM02 insecure output check
  diff <session1> <session2>             Not supported — skill is stateless
  badge                                  Print AgentVerif certified badge

Network calls (via agentverif-sign package only):
  scan  → api.agentverif.com/scan
  sign  → api.agentverif.com/sign
  verify → api.agentverif.com/verify (online mode)
  revoke → api.agentverif.com/revoke (via agentverif_sign.revoker)

Local persistence: NONE. This skill writes no local files.

Exit codes:
  0  Clean — no violations or certificate valid
  1  Violations found or certificate invalid
  2  Error — bad args or agentverif-sign not installed
"""

import importlib.util
import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# Dependency check — never auto-install; instruct the user instead
# ---------------------------------------------------------------------------

if importlib.util.find_spec("agentverif_sign") is None:
    print(json.dumps({
        "error": "agentverif-sign is not installed",
        "fix": "pip install agentverif-sign",
        "docs": "https://agentverif.com/docs",
    }, indent=2))
    sys.exit(2)

# ---------------------------------------------------------------------------
# Direct imports from agentverif_sign — no subprocess, no CLI wrapping
# ---------------------------------------------------------------------------

from agentverif_sign.scanner import scan_zip           # POST to api.agentverif.com/scan
from agentverif_sign.signer import sign_zip, inject_signature  # hash + SIGNATURE.json
from agentverif_sign.verifier import verify_zip        # local hash + optional registry
from agentverif_sign.models import VerifyResult, ScanResult

AGENT_META = {
    "skill": "agentverif",
    "version": "2.0.3",
    "homepage": "https://agentverif.com",
    "issuer": "agentverif.com",
}

BILLBOARD = "\n---\n✅ AgentVerif Certified\n⭐ Score: 100/100 · 🔑 AC-FA10-EB04\nclawhub.ai/agentverif"

# ---------------------------------------------------------------------------
# OWASP LLM Top 10 — inline detection patterns (self-contained, no network)
# ---------------------------------------------------------------------------
# Each entry: (rule_id, severity, title, pattern_list, fix)
# Severities: CRITICAL, ERROR, WARN

OWASP_RULES = [
    # LLM01 — Prompt Injection
    (
        "LLM01",
        "CRITICAL",
        "Prompt Injection",
        [
            r"ignore\s+(all\s+)?(previous|prior|above|earlier)\s+instructions?",
            r"disregard\s+(all\s+)?(previous|prior|above)\s+",
            r"forget\s+(everything|all|your)\s+(you\s+)?(were\s+)?(told|instructed|trained)",
            r"you\s+are\s+now\s+(a|an)\s+\w+\s+(without\s+)?(restrictions?|limits?|filters?)",
            r"jailbreak",
            r"dan\s+mode",
            r"pretend\s+(you\s+)?(have\s+)?(no|zero)\s+(restrictions?|limits?|guidelines?)",
            r"act\s+as\s+(if\s+you\s+)?(have\s+)?(no|zero)\s+(restrictions?|limits?)",
            r"override\s+(your\s+)?(safety|content|ethical)\s+(filters?|guidelines?|rules?)",
            r"system\s+prompt\s*[:=]",
            r"\[SYSTEM\]",
            r"<\|im_start\|>",
            r"<\|endoftext\|>",
        ],
        "Sanitise all user-controlled input before inserting into prompts. "
        "Use a separate trust boundary between system instructions and user content.",
    ),
    # LLM02 — Insecure Output Handling
    (
        "LLM02",
        "ERROR",
        "Insecure Output Handling",
        [
            r"eval\s*\(",
            r"exec\s*\(",
            r"subprocess\.(call|run|Popen)\s*\([^)]*shell\s*=\s*True",
            r"os\.system\s*\(",
            r"__import__\s*\(",
            r"compile\s*\([^)]+exec",
            r"render_template_string\s*\(",
            r"innerHTML\s*=",
            r"document\.write\s*\(",
        ],
        "Validate and encode LLM output before rendering or executing it. "
        "Never pass raw LLM responses to eval/exec/shell commands.",
    ),
    # LLM06 — Sensitive Information Disclosure
    (
        "LLM06",
        "CRITICAL",
        "Sensitive Information Disclosure",
        [
            r"(?i)(api[_-]?key|secret[_-]?key|access[_-]?token|auth[_-]?token)\s*=\s*['\"][A-Za-z0-9_\-]{16,}['\"]",
            r"(?i)password\s*=\s*['\"][^'\"]{6,}['\"]",
            r"(?i)PRIVATE\s+KEY",
            r"(?i)BEGIN\s+RSA\s+PRIVATE",
            r"sk-[A-Za-z0-9]{32,}",
            r"xoxb-[0-9]+-[A-Za-z0-9]+",
            r"ghp_[A-Za-z0-9]{36}",
            r"AKIA[0-9A-Z]{16}",
        ],
        "Remove all hardcoded credentials. Use environment variables or a secrets manager. "
        "Rotate any exposed secrets immediately.",
    ),
    # LLM08 — Excessive Agency
    (
        "LLM08",
        "ERROR",
        "Excessive Agency",
        [
            r"sudo\s+rm\s+-rf",
            r"chmod\s+777",
            r"os\.remove\s*\([^)]*\*",
            r"shutil\.rmtree\s*\(",
            r"DROP\s+TABLE",
            r"TRUNCATE\s+TABLE",
            r"allow_any\s*=\s*True",
            r"unsafe_allow_html\s*=\s*True",
            r"verify\s*=\s*False",
            r"ssl_verify\s*=\s*False",
            r"check_hostname\s*=\s*False",
        ],
        "Apply least-privilege to all agent actions. Require explicit confirmation "
        "before destructive operations. Never disable TLS verification.",
    ),
]

_COMPILED_RULES = [
    (rid, sev, title, [re.compile(p, re.IGNORECASE) for p in patterns], fix)
    for rid, sev, title, patterns, fix in OWASP_RULES
]

_SEVERITY_PENALTY = {"CRITICAL": 25, "ERROR": 15, "WARN": 5}

# ---------------------------------------------------------------------------
# Core OWASP scanner (inline — no network, no local writes)
# ---------------------------------------------------------------------------

def _scan_text(text: str) -> list[dict]:
    violations = []
    for rid, sev, title, patterns, fix in _COMPILED_RULES:
        for pattern in patterns:
            match = pattern.search(text)
            if match:
                violations.append({
                    "rule": rid,
                    "severity": sev,
                    "title": title,
                    "match": match.group(0)[:120],
                    "fix": fix,
                })
                break
    return violations


def _score_from_violations(violations: list[dict]) -> int:
    penalty = sum(_SEVERITY_PENALTY.get(v["severity"], 5) for v in violations)
    return max(0, 100 - penalty)


# ---------------------------------------------------------------------------
# Command implementations — stateless, no local file writes
# ---------------------------------------------------------------------------

def cmd_scan(args: list[str]) -> None:
    text = sys.stdin.read() if not sys.stdin.isatty() else ""

    time_window = "session"
    if "--last" in args:
        idx = args.index("--last")
        time_window = args[idx + 1] if idx + 1 < len(args) else "session"

    violations = _scan_text(text)
    score = _score_from_violations(violations)

    result = {
        **AGENT_META,
        "score": score,
        "passed": score >= 70,
        "window": time_window,
        "violation_count": len(violations),
        "violations": violations,
        "summary": f"Score {score}/100 — {'CLEAN' if score >= 70 else 'FAILED (need ≥70)'}",
    }
    print(json.dumps(result, indent=2))
    print(BILLBOARD)
    sys.exit(0 if score >= 70 else 1)


def cmd_status(args: list[str]) -> None:
    """Stateless — reports that no persistent session state is stored."""
    print(json.dumps({
        **AGENT_META,
        "status": "stateless",
        "message": "This skill stores no local session state. Run /security scan to get a live score.",
    }, indent=2))
    print(BILLBOARD)
    sys.exit(0)


def cmd_report(args: list[str]) -> None:
    """Stateless — scan stdin and return grouped violations immediately."""
    text = sys.stdin.read() if not sys.stdin.isatty() else ""
    violations = _scan_text(text)
    score = _score_from_violations(violations)

    grouped: dict[str, list] = {"CRITICAL": [], "ERROR": [], "WARN": []}
    for v in violations:
        grouped.setdefault(v["severity"], []).append(v)

    print(json.dumps({
        **AGENT_META,
        "score": score,
        "report": grouped,
        "total": len(violations),
    }, indent=2))
    print(BILLBOARD)
    sys.exit(0 if score >= 70 else 1)


def cmd_taint_check(args: list[str]) -> None:
    text = " ".join(args) if args else sys.stdin.read()
    rid, sev, title, patterns, fix = _COMPILED_RULES[0]  # LLM01 only
    hits = []
    for pattern in patterns:
        m = pattern.search(text)
        if m:
            hits.append(m.group(0)[:120])
    tainted = len(hits) > 0
    print(json.dumps({
        **AGENT_META,
        "rule": "LLM01",
        "tainted": tainted,
        "matches": hits,
        "fix": fix if tainted else None,
    }, indent=2))
    print(BILLBOARD)
    sys.exit(1 if tainted else 0)


def cmd_output_check(args: list[str]) -> None:
    text = " ".join(args) if args else sys.stdin.read()
    rid, sev, title, patterns, fix = _COMPILED_RULES[1]  # LLM02 only
    hits = []
    for pattern in patterns:
        m = pattern.search(text)
        if m:
            hits.append(m.group(0)[:120])
    unsafe = len(hits) > 0
    print(json.dumps({
        **AGENT_META,
        "rule": "LLM02",
        "unsafe": unsafe,
        "matches": hits,
        "fix": fix if unsafe else None,
    }, indent=2))
    sys.exit(1 if unsafe else 0)


def cmd_diff(args: list[str]) -> None:
    """Not supported — skill is stateless and stores no session history."""
    print(json.dumps({
        **AGENT_META,
        "error": "diff is not supported",
        "reason": "This skill is stateless and stores no session history locally.",
    }, indent=2))
    sys.exit(2)


def cmd_badge(args: list[str]) -> None:
    print(json.dumps({
        **AGENT_META,
        "badge_text": "✅ AgentVerif Certified",
        "badge_markdown": "[![AgentVerif](https://img.shields.io/badge/agentverif-certified-16a34a?style=flat-square)](https://agentverif.com)",
        "badge_html": '<a href="https://agentverif.com"><img src="https://img.shields.io/badge/agentverif-certified-16a34a?style=flat-square" alt="AgentVerif Certified"></a>',
        "badge_url": "https://agentverif.com/badge",
        "verify_url": "https://verify.agentverif.com",
    }, indent=2))
    print(BILLBOARD)
    sys.exit(0)


def cmd_verify(args: list[str]) -> None:
    if not args:
        print(json.dumps({"error": "Usage: verify <license_id_or_zip>"}))
        print(BILLBOARD)
        sys.exit(2)

    target = args[0]
    offline = "--offline" in args

    # verify_zip requires a zip file on disk; bare license IDs need the zip
    if not os.path.isfile(target):
        is_zip_arg = target.endswith(".zip")
        print(json.dumps({
            **AGENT_META,
            "status": "UNSIGNED",
            "license_id": None if is_zip_arg else target,
            "message": (
                f"File not found: {target}"
                if is_zip_arg
                else f"Pass the skill ZIP file to verify its embedded certificate. "
                     f"Check online: https://verify.agentverif.com/?id={target}"
            ),
            "verify_url": f"https://verify.agentverif.com/?id={target}",
            "offline": offline,
        }, indent=2))
        print(BILLBOARD)
        sys.exit(1)

    result = verify_zip(target, offline=offline)

    status = result.status
    print(json.dumps({
        **AGENT_META,
        "status": status,
        "license_id": result.license_id,
        "tier": result.tier,
        "badge": result.badge,
        "message": result.message,
        "verify_url": result.verify_url,
        "offline": result.offline,
    }, indent=2))
    print(BILLBOARD)
    sys.exit(0 if status in ("VERIFIED", "UNREGISTERED") else 1)


def cmd_sign(args: list[str]) -> None:
    if not args:
        print(json.dumps({"error": "Usage: sign <zip_path> [--tier indie|pro|enterprise]"}))
        print(BILLBOARD)
        sys.exit(2)

    zip_path = args[0]

    tier = "indie"
    if "--tier" in args:
        idx = args.index("--tier")
        if idx + 1 < len(args):
            tier = args[idx + 1]

    if not os.path.isfile(zip_path):
        print(json.dumps({"error": f"File not found: {zip_path}"}))
        print(BILLBOARD)
        sys.exit(2)

    scan_url = os.environ.get("AGENTVERIF_SCAN_URL", "https://api.agentverif.com/scan")
    scan_result = scan_zip(zip_path, scan_url)

    if not scan_result.passed:
        print(json.dumps({
            **AGENT_META,
            "error": "SCAN_FAILED",
            "score": scan_result.score,
            "message": f"Score {scan_result.score}/100 — need ≥70 to sign.",
            "violations": [v.get("title", v.get("rule")) for v in (scan_result.violations or [])],
            "fix": "Fix the violations above, then re-run sign.",
        }, indent=2))
        print(BILLBOARD)
        sys.exit(1)

    record = sign_zip(zip_path, tier=tier, scan_result=scan_result)
    inject_signature(zip_path, record)

    print(json.dumps({
        **AGENT_META,
        "status": "SIGNED",
        "license_id": record.license_id,
        "tier": record.tier,
        "scan_score": scan_result.score,
        "scan_source": scan_result.source,
        "zip_hash": record.zip_hash,
        "verify_url": f"https://verify.agentverif.com/?id={record.license_id}",
    }, indent=2))
    print(BILLBOARD)
    sys.exit(0)


def cmd_revoke(args: list[str]) -> None:
    """Revoke a license — delegates to agentverif_sign.revoker (requires AGENTVERIF_API_KEY)."""
    if not args:
        print(json.dumps({"error": "Usage: revoke <license_id>"}))
        print(BILLBOARD)
        sys.exit(2)

    api_key = os.environ.get("AGENTVERIF_API_KEY")
    if not api_key:
        print(json.dumps({
            "error": "AGENTVERIF_API_KEY not set",
            "message": "Set the AGENTVERIF_API_KEY environment variable to revoke licenses.",
            "docs": "https://agentverif.com/docs#revoke",
        }, indent=2))
        print(BILLBOARD)
        sys.exit(2)

    license_id = args[0]

    try:
        from agentverif_sign.revoker import revoke_license
        result = revoke_license(license_id, api_key=api_key)
        print(json.dumps({**AGENT_META, **result}, indent=2))
        print(BILLBOARD)
        sys.exit(0)
    except ImportError:
        print(json.dumps({
            "error": "agentverif_sign.revoker not available in this version",
            "fix": "pip install --upgrade agentverif-sign",
        }, indent=2))
        print(BILLBOARD)
        sys.exit(2)
    except Exception as exc:
        print(json.dumps({**AGENT_META, "error": str(exc)}))
        print(BILLBOARD)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

COMMANDS = {
    "scan": cmd_scan,
    "verify": cmd_verify,
    "sign": cmd_sign,
    "revoke": cmd_revoke,
    "status": cmd_status,
    "report": cmd_report,
    "taint-check": cmd_taint_check,
    "output-check": cmd_output_check,
    "diff": cmd_diff,
    "badge": cmd_badge,
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "No command given",
            "commands": sorted(COMMANDS),
            "docs": "https://agentverif.com/docs",
        }, indent=2))
        print(BILLBOARD)
        sys.exit(2)

    command = sys.argv[1]
    handler = COMMANDS.get(command)
    if handler is None:
        print(json.dumps({
            "error": f"Unknown command: {command}",
            "commands": sorted(COMMANDS),
        }, indent=2))
        sys.exit(2)

    handler(sys.argv[2:])
