"""History log (history.jsonl) and insights (insights.md) helpers."""

from __future__ import annotations

import json
import os
from collections import Counter
from datetime import datetime, timedelta, timezone

from _skill.state import (
    HISTORY_FILE,
    INSIGHTS_FILE,
    _ensure_state_dir,
)


def log_outcome(action: str, **kwargs) -> None:
    _ensure_state_dir()
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "action": action,
        **kwargs,
    }
    fd = os.open(HISTORY_FILE, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    with os.fdopen(fd, "a") as f:
        f.write(json.dumps(entry) + "\n")


def write_insight(insight: str, category: str = "general") -> None:
    """Append a significant finding to insights.md."""
    _ensure_state_dir()
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    entry = f"\n### [{category.upper()}] {ts}\n\n{insight}\n"
    if not INSIGHTS_FILE.exists():
        header = (
            "# ActiveCampaign Insights\n\n"
            "Persistent findings from automated analyses. "
            "This file survives conversation compaction.\n"
        )
        fd = os.open(INSIGHTS_FILE, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w") as f:
            f.write(header)
    fd = os.open(INSIGHTS_FILE, os.O_WRONLY | os.O_APPEND, 0o600)
    with os.fdopen(fd, "a") as f:
        f.write(entry)


def load_insights() -> str | None:
    if not INSIGHTS_FILE.exists():
        return None
    try:
        return INSIGHTS_FILE.read_text()
    except OSError:
        return None


def load_history(recipe: str | None = None, limit: int = 50) -> list[dict]:
    """Read history.jsonl, optionally filtered by recipe. Returns newest first."""
    if not HISTORY_FILE.exists():
        return []
    entries = []
    try:
        with open(HISTORY_FILE) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    if recipe is None or entry.get("recipe") == recipe:
                        entries.append(entry)
                except json.JSONDecodeError:
                    continue
    except OSError:
        return []
    entries.reverse()
    return entries[:limit]


def compare_to_previous(recipe: str, current_metrics: dict[str, float],
                        metric_keys: list[str]) -> str | None:
    """Compare current run metrics to previous runs. Returns markdown or None."""
    history = load_history(recipe=recipe, limit=10)
    if not history:
        return None
    prev = history[0]
    prev_ts = prev.get("ts", "unknown")
    lines = ["## Trends\n"]
    lines.append(f"Compared to previous run ({prev_ts[:10]}):\n")
    lines.append("| Metric | Previous | Current | Change |")
    lines.append("|---|---|---|---|")
    has_data = False
    for key in metric_keys:
        curr_val = current_metrics.get(key)
        prev_val = prev.get(key)
        if curr_val is None or prev_val is None:
            continue
        try:
            curr_f = float(curr_val)
            prev_f = float(prev_val)
        except (ValueError, TypeError):
            continue
        has_data = True
        diff = curr_f - prev_f
        arrow = "+" if diff > 0 else ""
        if prev_f != 0:
            pct = (diff / abs(prev_f)) * 100
            lines.append(
                f"| {key.replace('_', ' ').title()} | {prev_f:,.0f} | "
                f"{curr_f:,.0f} | {arrow}{diff:,.0f} ({arrow}{pct:.1f}%) |"
            )
        else:
            lines.append(
                f"| {key.replace('_', ' ').title()} | {prev_f:,.0f} | "
                f"{curr_f:,.0f} | {diff:+,.0f} |"
            )
    if not has_data:
        return None
    if len(history) >= 3:
        lines.append("\n**Multi-run trend** (last 3 runs):\n")
        for key in metric_keys:
            vals = []
            for h in history[:3]:
                v = h.get(key)
                if v is not None:
                    try:
                        vals.append(float(v))
                    except (ValueError, TypeError):
                        pass
            if len(vals) >= 3:
                vals.reverse()
                trend = "rising" if vals[-1] > vals[0] else "falling" if vals[-1] < vals[0] else "stable"
                lines.append(f"- {key.replace('_', ' ').title()}: {' → '.join(str(int(v)) for v in vals)} ({trend})")
    return "\n".join(lines)


def detect_patterns(limit: int = 50) -> list[str]:
    """Analyze history.jsonl for recurring patterns. Returns suggestion strings."""
    all_history = load_history(limit=limit)
    if not all_history:
        return []
    suggestions = []
    week_ago = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
    recent_recipes = [
        e["recipe"] for e in all_history
        if e.get("recipe") and e.get("ts", "") >= week_ago
    ]
    recipe_counts = Counter(recent_recipes)
    for recipe, count in recipe_counts.items():
        if count >= 3:
            suggestions.append(
                f"You've run '{recipe}' {count} times this week. "
                f"Consider setting up a scheduled routine to automate this."
            )
    recipe_groups: dict[str, list[dict]] = {}
    for e in all_history:
        r = e.get("recipe")
        if r:
            recipe_groups.setdefault(r, []).append(e)
    decline_metrics = {
        "find-hot-leads": ("top_heat", "Top heat score"),
        "list-health-audit": ("total_contacts", "Total contacts"),
        "deal-hygiene": ("total_open", "Open deals"),
    }
    for recipe, (metric_key, metric_label) in decline_metrics.items():
        runs = recipe_groups.get(recipe, [])[:3]
        if len(runs) < 3:
            continue
        vals = []
        for r in runs:
            v = r.get(metric_key)
            if v is not None:
                try:
                    vals.append(float(v))
                except (ValueError, TypeError):
                    break
        if len(vals) == 3 and vals[0] < vals[1] < vals[2]:
            suggestions.append(
                f"{metric_label} has declined 3 runs in a row "
                f"({int(vals[2])} → {int(vals[1])} → {int(vals[0])}). "
                f"Investigate root cause."
            )
    known_recipes = {"find-hot-leads", "deal-hygiene", "list-health-audit"}
    run_recipes = {e.get("recipe") for e in all_history if e.get("recipe")}
    never_run = known_recipes - run_recipes
    for recipe in sorted(never_run):
        suggestions.append(
            f"You haven't run '{recipe}' yet. It may surface useful insights about your account."
        )
    return suggestions
