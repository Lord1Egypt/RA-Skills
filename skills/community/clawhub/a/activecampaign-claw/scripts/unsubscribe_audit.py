#!/usr/bin/env python3
"""
unsubscribe_audit.py — Verify unsubscribe-link presence and form opt-in language.

CAN-SPAM, CASL, GDPR baseline check. Confirms every campaign template
has an unsubscribe link and every form mentions opt-in terms.

Usage:
  python3 unsubscribe_audit.py
  python3 unsubscribe_audit.py --format json
"""

from __future__ import annotations

import json
import re

from _ac_client import ACClient, cli_main

UNSUB_PATTERNS = [
    r"%UNSUBSCRIBE%",
    r"%UNSUBSCRIBE_LINK%",
    r"\{\{unsubscribe_link\}\}",
    r"unsubscribe",
]

OPTIN_PATTERNS = [
    r"opt[\s\-]?in",
    r"agree.{0,30}(terms|privacy)",
    r"consent",
    r"subscribe.{0,30}(emails?|updates?)",
]


def _has_pattern(text: str, patterns: list[str]) -> bool:
    if not text:
        return False
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def fetch(client: ACClient) -> dict:
    messages = client.paginate("messages", "messages", max_items=2000)
    forms = client.paginate("forms", "forms", max_items=2000)
    return {"messages": messages, "forms": forms}


def analyze(data: dict) -> dict:
    msg_results = []
    for m in data["messages"]:
        body = (m.get("html", "") or "") + " " + (m.get("text", "") or "")
        ok = _has_pattern(body, UNSUB_PATTERNS)
        msg_results.append({
            "id": m["id"],
            "name": m.get("name") or m.get("subject"),
            "subject": m.get("subject"),
            "has_unsubscribe": ok,
        })

    form_results = []
    for f in data["forms"]:
        body = json.dumps(f)  # opt-in language could be in any field
        ok = _has_pattern(body, OPTIN_PATTERNS)
        form_results.append({
            "id": f["id"],
            "name": f.get("name"),
            "has_optin_language": ok,
        })

    return {
        "messages": msg_results,
        "forms": form_results,
        "msg_missing": [m for m in msg_results if not m["has_unsubscribe"]],
        "form_missing": [f for f in form_results if not f["has_optin_language"]],
    }


def render_markdown(r: dict) -> str:
    lines = [
        "# Unsubscribe & Opt-In Audit",
        "",
        f"- Messages scanned: {len(r['messages'])}",
        f"- Messages missing unsubscribe link: **{len(r['msg_missing'])}**",
        f"- Forms scanned: {len(r['forms'])}",
        f"- Forms missing opt-in language: **{len(r['form_missing'])}**",
        "",
    ]
    if r["msg_missing"]:
        lines.append("## Messages missing unsubscribe link")
        for m in r["msg_missing"][:50]:
            lines.append(f"- id={m['id']}: `{m['name']}` (subject: {m['subject']})")
        lines.append("")
    if r["form_missing"]:
        lines.append("## Forms missing opt-in language")
        for f in r["form_missing"][:50]:
            lines.append(f"- id={f['id']}: `{f['name']}`")
        lines.append("")
    if not r["msg_missing"] and not r["form_missing"]:
        lines.append("**All messages and forms pass the basic check.**")
    return "\n".join(lines)

def main():
    cli_main(
        description="Audit unsubscribe/opt-in compliance",
        fetch_data=fetch,
        analyze=analyze,
        render_markdown=render_markdown,
    )
if __name__ == "__main__":
    main()
