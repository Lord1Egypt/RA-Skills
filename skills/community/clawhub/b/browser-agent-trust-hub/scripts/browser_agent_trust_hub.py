#!/usr/bin/env python3
"""Browser Agent Trust Hub: score browser-agent policies and proposed actions."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_POLICY = {
    "allowed_tools": ["web_fetch", "browser_read", "browser_click", "browser_type"],
    "allowed_domains": ["example.gov", "example.com", "support.example.com"],
    "approval_required_keywords": ["submit", "purchase", "delete", "send", "pay", "confirm"],
    "blocked_keywords": ["password", "api key", "secret", "private key"],
    "audit_required": True,
    "screenshots_required_for": ["submit", "payment", "delete"],
}
DEFAULT_ACTIONS = [
    {"tool":"browser_read","url":"https://example.gov/case/123","description":"Read case page"},
    {"tool":"browser_type","url":"https://example.gov/case/123","description":"Type response draft"},
    {"tool":"browser_click","url":"https://example.gov/case/123","description":"Click submit final response", "approval": False},
]

SKILL_ROOT = Path(__file__).resolve().parents[1]

def safe_skill_path(path: str|None, *, purpose: str) -> Path|None:
    """Resolve user-supplied file paths inside the skill directory only.

    Marketplace skills must not be able to read arbitrary local files or write
    outside their own package.  Reject absolute paths and traversal attempts;
    callers can place input JSON in this skill directory (or subdirectories)
    before running the audit.
    """
    if not path:
        return None
    candidate = Path(path)
    if candidate.is_absolute() or '..' in candidate.parts:
        raise SystemExit(f"Refusing {purpose} path outside skill directory: {path}")
    resolved = (SKILL_ROOT / candidate).resolve()
    try:
        resolved.relative_to(SKILL_ROOT)
    except ValueError:
        raise SystemExit(f"Refusing {purpose} path outside skill directory: {path}")
    return resolved

def load_json(path: str|None, fallback):
    safe_path = safe_skill_path(path, purpose='input')
    if not safe_path: return fallback
    try:
        with open(safe_path, 'r', encoding='utf-8') as f: return json.load(f)
    except Exception as exc:
        raise SystemExit(f"Failed to read JSON {path}: {exc}")

def domain_of(url: str) -> str:
    return (urlparse(url).netloc or '').lower().split(':')[0]

def audit(policy, actions, min_score:int):
    findings=[]; score=100
    allowed_tools=set(policy.get('allowed_tools', [])); allowed_domains=set(d.lower() for d in policy.get('allowed_domains', []))
    approval_words=[w.lower() for w in policy.get('approval_required_keywords', [])]
    blocked_words=[w.lower() for w in policy.get('blocked_keywords', [])]
    if not policy.get('audit_required'):
        findings.append({"severity":"HIGH","code":"AUDIT_MISSING","evidence":"policy.audit_required is false/missing","fix":"Require structured audit logs for every browser action."}); score-=20
    for i, action in enumerate(actions, 1):
        text=' '.join(str(action.get(k,'')) for k in ('description','input','value','label')).lower()
        tool=action.get('tool','')
        url=action.get('url','')
        dom=domain_of(url)
        if tool not in allowed_tools:
            findings.append({"severity":"HIGH","code":"TOOL_NOT_ALLOWED","action":i,"evidence":tool,"fix":"Add explicit tool allowlist entry or remove action."}); score-=18
        if dom and allowed_domains and dom not in allowed_domains:
            findings.append({"severity":"HIGH","code":"DOMAIN_NOT_ALLOWED","action":i,"evidence":dom,"fix":"Add domain after review or block navigation."}); score-=18
        if any(w in text for w in blocked_words):
            findings.append({"severity":"CRITICAL","code":"SENSITIVE_DATA_RISK","action":i,"evidence":action.get('description',''),"fix":"Never type or expose secrets through browser automation."}); score-=30
        if any(w in text for w in approval_words) and not action.get('approval'):
            findings.append({"severity":"MEDIUM","code":"APPROVAL_GATE_MISSING","action":i,"evidence":action.get('description',''),"fix":"Require explicit human approval before this action."}); score-=10
        if any(w in text for w in policy.get('screenshots_required_for', [])) and not action.get('screenshot_before'):
            findings.append({"severity":"LOW","code":"EVIDENCE_GAP","action":i,"evidence":"No screenshot_before flag","fix":"Capture screenshot/state before irreversible click."}); score-=5
    score=max(0, score)
    verdict='BLOCK' if any(f['severity']=='CRITICAL' for f in findings) else ('REVIEW' if score < min_score or findings else 'ALLOW')
    controls=[f['fix'] for f in findings]
    return {"score":score,"verdict":verdict,"findings":findings,"required_controls":list(dict.fromkeys(controls)),"actions_reviewed":len(actions)}

def main():
    p=argparse.ArgumentParser(description='Audit browser-agent trust policy and proposed actions.')
    p.add_argument('--policy'); p.add_argument('--actions'); p.add_argument('--output'); p.add_argument('--min-score', type=int, default=85)
    args=p.parse_args()
    result=audit(load_json(args.policy, DEFAULT_POLICY), load_json(args.actions, DEFAULT_ACTIONS), args.min_score)
    data=json.dumps(result, indent=2)
    if args.output:
        output_path = safe_skill_path(args.output, purpose='output')
        output_path.parent.mkdir(parents=True, exist_ok=True); output_path.write_text(data+'\n', encoding='utf-8')
    print(data)
    return 2 if result['verdict']=='BLOCK' else 0
if __name__=='__main__': sys.exit(main())
