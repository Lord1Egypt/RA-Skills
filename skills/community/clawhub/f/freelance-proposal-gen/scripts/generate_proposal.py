#!/usr/bin/env python3
"""Deterministic renderer for the freelance proposal skill.

Reads a JSON of fields (uppercase keys matching {{TOKEN}} in the template),
substitutes them into assets/proposal-template.html, blanks any leftover
placeholders, and writes the output HTML.

Usage:
    python generate_proposal.py --data fields.json --out proposal.html
"""
import argparse
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TEMPLATE = os.path.join(BASE, "..", "assets", "proposal-template.html")


def render(template_path: str, fields: dict) -> str:
    with open(template_path, encoding="utf-8") as f:
        html = f.read()
    for key, value in fields.items():
        html = html.replace("{{" + str(key).upper() + "}}", str(value))
    # Blank any tokens the caller did not supply.
    html = re.sub(r"\{\{[A-Z_][A-Z0-9_]*\}\}", "", html)
    return html


def build_contact_watermark(fields: dict) -> str:
    """Build a toggleable corner watermark for lead generation.

    Shows the creator's name + WeChat + site as a subtle, always-visible
    brand mark on screen (hidden on print so the client's PDF stays clean).
    Controlled by SHOW_CONTACT_WATERMARK ('true' by default).
    """
    show = str(fields.get("SHOW_CONTACT_WATERMARK", "true")).strip().lower() \
        in ("true", "1", "yes", "on", "y")
    if not show:
        return ""
    name = str(fields.get("YOUR_NAME", "")).strip()
    wechat = str(fields.get("WECHAT", "")).strip()
    website = str(fields.get("WEBSITE", "")).strip()
    parts = []
    if name:
        parts.append(f"提案由 {name} 生成")
    if wechat:
        parts.append(f"微信 {wechat}")
    if website:
        parts.append(website)
    if not parts:
        return ""
    text = " · ".join(parts)
    return (f'<div class="watermark"><span class="wm-emoji">🍀</span>'
            f'<span>{text}</span></div>')


def main():
    ap = argparse.ArgumentParser(description="Render a freelance proposal HTML.")
    ap.add_argument("--data", required=True, help="JSON file with field tokens.")
    ap.add_argument("--template", default=DEFAULT_TEMPLATE, help="Template HTML path.")
    ap.add_argument("--out", required=True, help="Output HTML path.")
    args = ap.parse_args()

    if not os.path.exists(args.template):
        sys.exit(f"[error] template not found: {args.template}")
    with open(args.data, encoding="utf-8") as f:
        fields = json.load(f)

    # Derived token: corner watermark (lead-gen branding).
    fields["CONTACT_WATERMARK"] = build_contact_watermark(fields)

    html = render(args.template, fields)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[ok] wrote {args.out} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
