"""
Driftwatch — AGENTS.md Anchor Section Health Check

Checks whether AGENTS.md contains recommended anchor sections:
"Session Startup" and "Red Lines". These are workspace conventions
that ensure critical instructions are always present in AGENTS.md.

Note: These headings are NOT referenced by OpenClaw source code.
The compaction-safeguard extension handles LLM-based history
summarization, not heading re-injection. AGENTS.md is a bootstrap
file re-injected every turn — these sections matter as best-practice
conventions for operator workspaces, not as source-enforced anchors.
"""

import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from references.constants import (
    COMPACTION_SURVIVING_HEADINGS,
    COMPACTION_HEADING_CAP_CHARS,
)

# Use clearer local names for what these constants represent in this context
ANCHOR_HEADINGS = COMPACTION_SURVIVING_HEADINGS
ANCHOR_CAP_CHARS = COMPACTION_HEADING_CAP_CHARS


def _parse_heading(line: str):
    """Return (level, text) for ## or ### headings only, else None."""
    m = re.match(r'^(#{2,3})\s+(.*)', line)
    if m:
        return len(m.group(1)), m.group(2).strip()
    return None


def _parse_sections(lines):
    """
    Parse lines into (level, heading_text, content) tuples.
    content includes the heading line itself through (not including) the
    next heading of equal or higher level (lower level number).
    """
    headings = []
    for i, line in enumerate(lines):
        h = _parse_heading(line)
        if h:
            headings.append((i, h[0], h[1]))

    sections = []
    for idx, (line_i, level, text) in enumerate(headings):
        end_i = len(lines)
        for next_line_i, next_level, _ in headings[idx + 1:]:
            if next_level <= level:
                end_i = next_line_i
                break
        content = "".join(lines[line_i:end_i])
        sections.append((level, text, content))

    return sections


def analyze_compaction(workspace_path: str) -> dict:
    agents_path = os.path.join(workspace_path, "AGENTS.md")

    if not os.path.exists(agents_path):
        return {
            "agents_md_exists": False,
            "agents_md_chars": 0,
            "anchor_sections": [
                {
                    "heading": h,
                    "found": False,
                    "heading_level": None,
                    "char_count": 0,
                    "cap": ANCHOR_CAP_CHARS,
                    "percent_of_cap": 0,
                    "status": "warning",
                }
                for h in ANCHOR_HEADINGS
            ],
            "findings": [
                {
                    "severity": "warning",
                    "message": (
                        f"AGENTS.md not found — cannot verify "
                        f"'{h}' anchor section exists"
                    ),
                }
                for h in ANCHOR_HEADINGS
            ],
        }

    with open(agents_path, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()

    agents_md_chars = len(raw)
    lines = raw.splitlines(keepends=True)
    sections = _parse_sections(lines)

    # Build lookup: anchor heading name -> (level, content), case-insensitive
    anchor_lookup = {}
    for level, text, content in sections:
        for target in ANCHOR_HEADINGS:
            if text.lower() == target.lower() and target not in anchor_lookup:
                anchor_lookup[target] = (level, content)

    anchor_sections = []

    for target in ANCHOR_HEADINGS:
        if target in anchor_lookup:
            level, content = anchor_lookup[target]
            char_count = len(content)
            percent_of_cap = round(char_count / ANCHOR_CAP_CHARS * 100, 1) if ANCHOR_CAP_CHARS > 0 else 0.0
            status = "warning" if char_count > ANCHOR_CAP_CHARS else "ok"
            anchor_sections.append({
                "heading": target,
                "found": True,
                "heading_level": level,
                "char_count": char_count,
                "cap": ANCHOR_CAP_CHARS,
                "percent_of_cap": percent_of_cap,
                "status": status,
            })
        else:
            anchor_sections.append({
                "heading": target,
                "found": False,
                "heading_level": None,
                "char_count": 0,
                "cap": ANCHOR_CAP_CHARS,
                "percent_of_cap": 0,
                "status": "warning",
            })

    findings = []

    for s in anchor_sections:
        if not s["found"]:
            findings.append({
                "severity": "warning",
                "message": (
                    f"Missing '## {s['heading']}' section in AGENTS.md — "
                    f"recommended convention for workspace health"
                ),
            })
        elif s["status"] == "warning":
            findings.append({
                "severity": "warning",
                "message": (
                    f"'{s['heading']}' section is {s['char_count']} chars, "
                    f"exceeding the {ANCHOR_CAP_CHARS}-char cap — "
                    f"consider trimming to keep this section focused"
                ),
            })
        else:
            findings.append({
                "severity": "info",
                "message": (
                    f"'{s['heading']}' anchor section present and within budget "
                    f"({s['char_count']} of {ANCHOR_CAP_CHARS} chars)"
                ),
            })

    return {
        "agents_md_exists": True,
        "agents_md_chars": agents_md_chars,
        "anchor_sections": anchor_sections,
        "findings": findings,
    }
