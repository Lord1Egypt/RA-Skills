#!/usr/bin/env python3
"""
diff.py — Semantic diff engine for competitor-radar.

Compares current snapshot to previous snapshot for each tracked page type.
Uses an LLM (via OpenClaw's Claude integration) for semantic interpretation —
not a raw line diff.

Usage:
  python3 diff.py <slug>
  python3 diff.py --all

Output (stdout): JSON dict of diff results per page type.
"""

from __future__ import annotations
import argparse
import difflib
import hashlib
import json
import os
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"
COMPETITORS_FILE = DATA_DIR / "competitors.json"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_competitors() -> dict:
    if not COMPETITORS_FILE.exists():
        return {"competitors": []}
    return json.loads(COMPETITORS_FILE.read_text())


def get_competitor(slug: str) -> dict | None:
    data = load_competitors()
    return next((c for c in data["competitors"] if c["slug"] == slug), None)


def sorted_snapshots(slug: str, page_type: str, suffix: str = "txt") -> list[Path]:
    d = SNAPSHOTS_DIR / slug
    if not d.exists():
        return []
    return sorted(d.glob(f"{page_type}_*.{suffix}"), reverse=True)


def load_two_most_recent(slug: str, page_type: str) -> tuple[str | None, str | None]:
    """Returns (current_text, previous_text). Either may be None."""
    files = sorted_snapshots(slug, page_type, "txt")
    current = files[0].read_text(encoding="utf-8") if len(files) > 0 else None
    previous = files[1].read_text(encoding="utf-8") if len(files) > 1 else None
    return current, previous


def content_hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


def word_change_pct(old: str, new: str) -> float:
    """Approximate percentage of words that changed."""
    old_words = set(old.lower().split())
    new_words = set(new.lower().split())
    if not old_words:
        return 100.0
    changed = len(old_words.symmetric_difference(new_words))
    return round(changed / max(len(old_words), len(new_words)) * 100, 1)


def raw_unified_diff(old: str, new: str, label: str = "") -> str:
    """Return a readable unified diff string."""
    old_lines = old.splitlines(keepends=True)
    new_lines = new.splitlines(keepends=True)
    diff = difflib.unified_diff(old_lines, new_lines,
                                 fromfile=f"previous_{label}",
                                 tofile=f"current_{label}",
                                 n=2)
    return "".join(list(diff)[:100])  # cap at 100 lines


# ---------------------------------------------------------------------------
# Price extraction (heuristic — no LLM needed)
# ---------------------------------------------------------------------------

PRICE_PATTERN = re.compile(
    r"\$\s?(\d[\d,]*(?:\.\d{1,2})?)\s*/?\s*(mo(?:nth)?|yr|year|annually|per\s+user)?",
    re.IGNORECASE
)
PLAN_PATTERN = re.compile(
    r"\b(free|starter|basic|pro|professional|team|business|enterprise|growth|scale"
    r"|plus|premium|standard|advanced)\b",
    re.IGNORECASE
)


def extract_prices(text: str) -> list[dict]:
    """Extract all price mentions from text."""
    results = []
    for m in PRICE_PATTERN.finditer(text):
        results.append({
            "amount": m.group(1).replace(",", ""),
            "period": (m.group(2) or "").lower().strip(),
            "context": text[max(0, m.start() - 40):m.end() + 40].strip(),
        })
    return results


def extract_plans(text: str) -> list[str]:
    return list({m.group(0).lower() for m in PLAN_PATTERN.finditer(text)})


def diff_pricing(old_text: str, new_text: str) -> dict:
    """
    Compare pricing pages. Returns structured change summary.
    Does NOT require LLM — uses regex extraction.
    """
    old_prices = extract_prices(old_text)
    new_prices = extract_prices(new_text)
    old_plans = extract_plans(old_text)
    new_plans = extract_plans(new_text)

    added_plans = [p for p in new_plans if p not in old_plans]
    removed_plans = [p for p in old_plans if p not in new_plans]

    old_amounts = {p["amount"] for p in old_prices}
    new_amounts = {p["amount"] for p in new_prices}
    price_increases = [a for a in new_amounts if a not in old_amounts]
    price_removals = [a for a in old_amounts if a not in new_amounts]

    changed = bool(added_plans or removed_plans or price_increases or price_removals)
    pct = word_change_pct(old_text, new_text)

    return {
        "changed": changed,
        "word_change_pct": pct,
        "added_plans": added_plans,
        "removed_plans": removed_plans,
        "new_price_points": price_increases,
        "removed_price_points": price_removals,
        "old_prices": old_prices,
        "new_prices": new_prices,
        "raw_diff_preview": raw_unified_diff(old_text[:3000], new_text[:3000], "pricing"),
        "signal_level": "HIGH" if changed else ("MEDIUM" if pct > 15 else "NONE"),
    }


# ---------------------------------------------------------------------------
# Homepage hero diff
# ---------------------------------------------------------------------------

def diff_hero(old_text: str, new_text: str) -> dict:
    changed = old_text.strip() != new_text.strip()
    return {
        "changed": changed,
        "old_hero": old_text.strip(),
        "new_hero": new_text.strip(),
        "signal_level": "MEDIUM" if changed else "NONE",
    }


# ---------------------------------------------------------------------------
# Generic content diff (blog posts, changelog)
# ---------------------------------------------------------------------------

def diff_generic(old_text: str, new_text: str, page_type: str) -> dict:
    pct = word_change_pct(old_text, new_text)
    changed = pct > 5
    return {
        "changed": changed,
        "word_change_pct": pct,
        "raw_diff_preview": raw_unified_diff(old_text[:2000], new_text[:2000], page_type),
        "signal_level": "LOW" if changed else "NONE",
    }


# ---------------------------------------------------------------------------
# LLM semantic interpretation
# ---------------------------------------------------------------------------

def llm_interpret_pricing_diff(diff_result: dict, competitor_name: str) -> str:
    """
    Build a human-readable interpretation of the pricing diff.
    When running inside OpenClaw, the agent will call this and interpret
    the result with Claude. For standalone use, returns a template.
    """
    if not diff_result["changed"] and diff_result["word_change_pct"] < 5:
        return "No significant pricing changes detected."

    parts = []
    if diff_result["removed_plans"]:
        parts.append(f"Removed plans: {', '.join(diff_result['removed_plans'])}")
    if diff_result["added_plans"]:
        parts.append(f"New plans: {', '.join(diff_result['added_plans'])}")
    if diff_result["new_price_points"]:
        parts.append(f"New price points: ${', $'.join(diff_result['new_price_points'])}")
    if diff_result["removed_price_points"]:
        parts.append(f"Removed prices: ${', $'.join(diff_result['removed_price_points'])}")
    if diff_result["word_change_pct"] > 15:
        parts.append(f"Overall page changed significantly ({diff_result['word_change_pct']}% words differ)")

    summary = ". ".join(parts) if parts else "Minor content changes detected."

    # LLM prompt hint — the OpenClaw agent will expand on this
    prompt_hint = (
        f"PRICING_DIFF_SUMMARY for {competitor_name}:\n{summary}\n\n"
        f"RAW_DIFF_PREVIEW:\n{diff_result.get('raw_diff_preview', '')[:1000]}\n\n"
        "Interpret this pricing change in 2-3 bullets. What does it signal strategically? "
        "Are they moving upmarket? Simplifying? Cutting the free tier? Adding enterprise? "
        "What should competitors know about this?"
    )
    return prompt_hint


def llm_interpret_hero_diff(diff_result: dict, competitor_name: str) -> str:
    if not diff_result["changed"]:
        return "No positioning change."
    return (
        f"HOMEPAGE_HERO_CHANGE for {competitor_name}:\n"
        f"OLD: {diff_result['old_hero']}\n"
        f"NEW: {diff_result['new_hero']}\n\n"
        "What does this positioning change signal? Are they targeting a new segment? "
        "Adding AI messaging? Moving from feature to outcome language? "
        "1-2 bullet strategic interpretation."
    )


# ---------------------------------------------------------------------------
# Main diff runner
# ---------------------------------------------------------------------------

def run_diff_for_competitor(slug: str) -> dict:
    competitor = get_competitor(slug)
    if not competitor:
        return {"error": f"Competitor '{slug}' not found", "slug": slug}

    name = competitor["name"]
    results = {"slug": slug, "name": name, "signals": {}}

    # Pricing diff
    current_pricing, prev_pricing = load_two_most_recent(slug, "pricing")
    if current_pricing and prev_pricing:
        d = diff_pricing(prev_pricing, current_pricing)
        d["llm_prompt"] = llm_interpret_pricing_diff(d, name)
        results["signals"]["pricing"] = d
    elif current_pricing:
        results["signals"]["pricing"] = {"changed": False, "note": "first_run_no_baseline"}

    # Homepage hero diff
    current_hero, prev_hero = load_two_most_recent(slug, "homepage_hero")
    if current_hero and prev_hero:
        d = diff_hero(prev_hero, current_hero)
        d["llm_prompt"] = llm_interpret_hero_diff(d, name)
        results["signals"]["homepage_hero"] = d
    elif current_hero:
        results["signals"]["homepage_hero"] = {"changed": False, "note": "first_run_no_baseline"}

    # Aggregate highest signal level
    signal_levels = [s.get("signal_level", "NONE")
                     for s in results["signals"].values()]
    priority = {"HIGH": 3, "MEDIUM": 2, "LOW": 1, "NONE": 0}
    top = max(signal_levels, key=lambda x: priority.get(x, 0), default="NONE")
    results["highest_signal"] = top
    results["has_changes"] = top != "NONE"

    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="competitor-radar diff engine")
    parser.add_argument("slug", nargs="?", help="Competitor slug to diff")
    parser.add_argument("--all", action="store_true", help="Run diff for all competitors")
    args = parser.parse_args()

    data = load_competitors()
    active = [c for c in data["competitors"] if c.get("active", True)]

    if args.all:
        slugs = [c["slug"] for c in active]
    elif args.slug:
        slugs = [args.slug]
    else:
        parser.print_help()
        sys.exit(1)

    all_results = [run_diff_for_competitor(s) for s in slugs]
    print(json.dumps(all_results, indent=2, default=str))


if __name__ == "__main__":
    main()
