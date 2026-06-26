"""
Driftwatch — Truncation Danger Zone Simulation

Maps exactly which lines and sections fall in the truncation danger zone
for each bootstrap file. Shows operators what their agent can't see.

OpenClaw truncation: keeps first 14,000 chars (head) + last 4,000 chars (tail).
Everything between is cut. These numbers are fixed (70% and 20% of the 20K limit).

Danger zone only exists when file > 18,000 chars (head + tail = 18K).
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from references.constants import (
    BOOTSTRAP_MAX_CHARS_PER_FILE,
    BOOTSTRAP_FILE_ORDER,
    TRUNCATION_HEAD_RATIO,
    TRUNCATION_TAIL_RATIO,
)

# Fixed char positions based on the limit, not the file
HEAD_CHARS = int(BOOTSTRAP_MAX_CHARS_PER_FILE * TRUNCATION_HEAD_RATIO)  # 14,000
TAIL_CHARS = int(BOOTSTRAP_MAX_CHARS_PER_FILE * TRUNCATION_TAIL_RATIO)  # 4,000
SAFE_THRESHOLD = HEAD_CHARS + TAIL_CHARS  # 18,000 — below this, no danger zone

# Only simulate for files at 60%+ of limit
SIMULATION_MIN_PERCENT = 60


def _char_to_line(content, char_pos):
    """Convert a character position to a 1-based line number."""
    return content[:char_pos].count("\n") + 1


def _parse_headings(content):
    """Parse markdown headings with their char positions and content ranges."""
    headings = []
    lines = content.split("\n")
    char_offset = 0

    for i, line in enumerate(lines):
        match = re.match(r"^(#{2,3})\s+(.+)$", line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            headings.append({
                "heading": f"{'#' * level} {text}",
                "heading_level": level,
                "line": i + 1,  # 1-based
                "start_char": char_offset,
            })
        char_offset += len(line) + 1  # +1 for newline

    # Calculate content range for each heading (extends to next heading or EOF)
    for i, h in enumerate(headings):
        if i + 1 < len(headings):
            h["end_char"] = headings[i + 1]["start_char"]
        else:
            h["end_char"] = len(content)

    return headings


def _sections_in_zone(headings, zone_start, zone_end):
    """Find headings whose content overlaps with the danger zone."""
    sections = []
    for h in headings:
        # Check for overlap between [h.start_char, h.end_char) and [zone_start, zone_end)
        overlap_start = max(h["start_char"], zone_start)
        overlap_end = min(h["end_char"], zone_end)
        if overlap_start < overlap_end:
            sections.append({
                "heading": h["heading"],
                "heading_level": h["heading_level"],
                "line": h["line"],
                "chars_in_zone": overlap_end - overlap_start,
            })
    return sections


def analyze_simulation(workspace_path):
    """
    Analyze truncation danger zones for all bootstrap files.

    Returns a dict with simulation results per file.
    """
    files = []

    for filename in BOOTSTRAP_FILE_ORDER:
        fpath = os.path.join(workspace_path, filename)
        if not os.path.isfile(fpath):
            continue

        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
        except (OSError, UnicodeDecodeError):
            continue

        total_chars = len(content)
        percent_of_limit = round(total_chars / BOOTSTRAP_MAX_CHARS_PER_FILE * 100, 1)

        # Skip files under 60% — no simulation needed
        if percent_of_limit < SIMULATION_MIN_PERCENT:
            files.append({
                "file": filename,
                "total_chars": total_chars,
                "percent_of_limit": percent_of_limit,
                "simulation_needed": False,
                "status": "safe",
                "note": "Well under limit — no truncation risk",
            })
            continue

        # File is 60-90% — approaching but no danger zone yet
        if total_chars <= SAFE_THRESHOLD:
            files.append({
                "file": filename,
                "total_chars": total_chars,
                "percent_of_limit": percent_of_limit,
                "simulation_needed": False,
                "status": "approaching",
                "note": (
                    f"At {percent_of_limit}% of limit. No danger zone yet — "
                    f"file fits within head ({HEAD_CHARS:,}) + tail ({TAIL_CHARS:,}) zones."
                ),
            })
            continue

        # File is >18K — danger zone exists
        zone_start = HEAD_CHARS
        zone_end = total_chars - TAIL_CHARS
        zone_chars = zone_end - zone_start

        # Determine status
        if total_chars > BOOTSTRAP_MAX_CHARS_PER_FILE:
            status = "truncated_now"
            chars_key = "chars_truncated"
        else:
            status = "at_risk"
            chars_key = "chars_at_risk"

        # Map lines
        start_line = _char_to_line(content, zone_start)
        end_line = _char_to_line(content, zone_end)

        # Find sections in the danger zone
        headings = _parse_headings(content)
        sections = _sections_in_zone(headings, zone_start, zone_end)

        section_key = "sections_truncated" if status == "truncated_now" else "sections_at_risk"

        # Build recommendation
        if status == "truncated_now":
            pct_truncated = round(zone_chars / total_chars * 100)
            recommendation = (
                f"{zone_chars:,} chars ({pct_truncated}% of file) are ACTIVELY being truncated. "
                f"Your agent cannot see lines {start_line}-{end_line}."
            )
        else:
            recommendation = (
                f"Content between lines {start_line}-{end_line} would be cut first "
                f"if this file exceeds {BOOTSTRAP_MAX_CHARS_PER_FILE:,} chars"
            )

        danger_zone = {
            "start_char": zone_start,
            "end_char": zone_end,
            chars_key: zone_chars,
            "start_line": start_line,
            "end_line": end_line,
            section_key: sections,
        }

        files.append({
            "file": filename,
            "total_chars": total_chars,
            "percent_of_limit": percent_of_limit,
            "simulation_needed": True,
            "status": status,
            "danger_zone": danger_zone,
            "recommendation": recommendation,
        })

    return {"files": files}
