#!/usr/bin/env python3
"""
trust_scorer.py - Dynamic Trust Scoring

Maintains trust scores for tools/models based on recent failures.
Scores persist in insight.db and guide automated decisions:
- X.com links → always use grok42 (highest trust)
- General web → use tavily as first fallback (high trust)
- web_fetch → low trust, used only as last resort

Runs during heartbeat to keep scores up to date.
"""

import re
from pathlib import Path
import sqlite3
from datetime import datetime

WORKSPACE = Path("/home/node/.openclaw/workspace")
REGRESSIONS_MD = WORKSPACE / "REGRESSIONS.md"
DB_PATH = "/home/node/.openclaw/database/insight.db"

# Category → tool adjustment (same logic as friction_detector)
CATEGORY_ADJUSTMENTS = {
    "network_block": {"web_fetch": -5, "tavily": +2},
    "third_party_service": {"web_fetch": -5, "grok42": +2},
    "silent_wait": {},  # no specific tool
    "model_selection": {"grok42": +1},  # if model switch caused issue, boost target model score
    "tool_error": {"web_fetch": -2}  # generic tool failure penalizes web_fetch
}

# Initial scores if table empty
DEFAULT_SCORES = {
    "tavily": 85,
    "grok42": 95,
    "web_fetch": 40
}

def ensure_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trust_scores (
            tool TEXT PRIMARY KEY,
            score INTEGER NOT NULL DEFAULT 50,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

def init_default_scores(conn):
    cursor = conn.cursor()
    for tool, score in DEFAULT_SCORES.items():
        cursor.execute("""
            INSERT OR IGNORE INTO trust_scores (tool, score) VALUES (?, ?)
        """, (tool, score))
    conn.commit()

def load_scores(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT tool, score FROM trust_scores")
    rows = cursor.fetchall()
    return {tool: score for tool, score in rows}

def save_score(conn, tool, score):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO trust_scores (tool, score, last_updated) VALUES (?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(tool) DO UPDATE SET score=excluded.score, last_updated=CURRENT_TIMESTAMP
    """, (tool, score))
    conn.commit()

def categorize_friction(description):
    """Simple categorization based on description keywords (generic English)."""
    desc_low = description.lower()
    patterns = {
        "network_block": [r"403", r"blocked", r"cloudflare", r"access.*denied", r"network.*fail", r"timeout", r"unreachable"],
        "third_party_service": [r"x\.com", r"twitter", r"twitter\.com", r"third.*party", r"external.*site", r"api.*fail"],
        "silent_wait": [r"silent", r"unresponsive", r"hang", r"stuck", r"no.*response", r"long.*wait"],
        "model_selection": [r"model", r"switch.*model", r"invalid.*model", r"model.*timeout"],
        "tool_error": [r"tool.*fail", r"exec.*error", r"read.*error", r"command.*failed"]
    }
    for category, pats in patterns.items():
        for pat in pats:
            if re.search(pat, desc_low, re.IGNORECASE):
                return category
    return "other"

def parse_entries():
    """Parse REGRESSIONS.md to extract date and failure description."""
    if not REGRESSIONS_MD.exists():
        return []
    text = REGRESSIONS_MD.read_text(encoding="utf-8")
    # Look for: ### YYYY-MM-DD ... then "Failure:" line then "**Rules**:"
    pattern = r'###\s+(\d{4}-\d{2}-\d{2})\s+[^\n]*?\n.*?\nFailure:\s*(.+?)\n\*\*Rules\*\*:'
    matches = re.findall(pattern, text, re.DOTALL)
    entries = []
    for date_str, description in matches:
        desc_line = description.split('\n')[0].strip()
        entries.append({"date": date_str, "description": desc_line})
    return entries

def clamp(score, min_val=0, max_val=100):
    return max(min_val, min(max_val, score))

def update_trust_scores():
    """Main entry: analyze recent failures and adjust trust scores."""
    entries = parse_entries()
    if not entries:
        print("\n📊 Trust Scores: No failure records found to adjust scores.\n")
        return

    # Connect to DB
    conn = sqlite3.connect(DB_PATH)
    ensure_table(conn)
    init_default_scores(conn)
    scores = load_scores(conn)

    # Apply adjustments based on entries (simple: each entry adjusts once)
    for entry in entries:
        cat = categorize_friction(entry["description"])
        adj = CATEGORY_ADJUSTMENTS.get(cat, {})
        for tool, delta in adj.items():
            current = scores.get(tool, DEFAULT_SCORES.get(tool, 50))
            new_score = clamp(current + delta)
            scores[tool] = new_score
            save_score(conn, tool, new_score)

    conn.close()

    # Print report
    print("\n📊 Trust Scores Updated:\n")
    print("{:<12} {:>6}".format("Tool", "Score"))
    print("-" * 20)
    for tool, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        print("{:<12} {:>6}".format(tool, score))
    print()

if __name__ == "__main__":
    update_trust_scores()
