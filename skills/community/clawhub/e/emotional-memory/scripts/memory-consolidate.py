#!/usr/bin/env python3
"""
Memory Consolidation ("Sleep Cycle")
Runs nightly via cron. Replays the day's emotional memories,
strengthens important ones, identifies patterns, prunes noise.

Mimics how human brains consolidate memory during sleep:
1. Re-score emotional weights with temporal distance
2. Strengthen associative links between emotionally similar memories
3. Identify recurring emotional patterns
4. Write consolidated memory entry
5. Flag low-weight old memories for cold storage

Environment:
  EMOTIONAL_MEMORY_DIR  -- directory for memory files
                           (default: $OPENCLAW_WORKSPACE/memory or ./memory)
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict


def get_memory_dir():
    if os.environ.get("EMOTIONAL_MEMORY_DIR"):
        return Path(os.environ["EMOTIONAL_MEMORY_DIR"])
    if os.environ.get("OPENCLAW_WORKSPACE"):
        return Path(os.environ["OPENCLAW_WORKSPACE"]) / "memory"
    workspace = Path.home() / ".openclaw" / "workspace"
    if workspace.exists():
        return workspace / "memory"
    return Path("./memory")


MEMORY_DIR = get_memory_dir()
EMOTIONAL_INDEX = MEMORY_DIR / "emotional-index.jsonl"
CONSOLIDATION_DIR = MEMORY_DIR / "consolidation"

TODAY = datetime.now().strftime("%Y-%m-%d")


def load_emotional_index():
    entries = []
    if EMOTIONAL_INDEX.exists():
        for line in EMOTIONAL_INDEX.read_text().strip().split("\n"):
            if line.strip():
                try:
                    entries.append(json.loads(line))
                except:
                    continue
    return entries


def save_emotional_index(entries):
    EMOTIONAL_INDEX.parent.mkdir(parents=True, exist_ok=True)
    with open(EMOTIONAL_INDEX, "w") as f:
        for e in entries:
            f.write(json.dumps(e) + "\n")


def temporal_decay(entry):
    """
    Apply temporal decay to emotional weight.
    Recent memories stay vivid. Older ones fade UNLESS decay_resistant.
    Very high-weight memories (8+) decay slower.
    """
    try:
        entry_date = datetime.strptime(entry["date"], "%Y-%m-%d")
    except:
        return entry["weight"]

    days_ago = (datetime.now() - entry_date).days

    if entry.get("decay_resistant", False):
        return entry["weight"]  # Core memories don't fade

    original = entry["weight"]

    if original >= 8:
        decay = days_ago * 0.02  # High-intensity: very slow fade
    elif original >= 5:
        decay = days_ago * 0.05  # Medium: normal fade
    else:
        decay = days_ago * 0.1   # Low: quick fade

    new_weight = max(1, round(original - decay, 1))
    return new_weight


def find_patterns(entries):
    """
    Look for recurring emotional patterns.
    Same mood appearing 3+ times = pattern worth noting.
    """
    mood_counts = defaultdict(list)
    tag_counts = defaultdict(list)

    for e in entries:
        mood = e.get("mood", "")
        for m in mood.split("/"):
            m = m.strip()
            if m:
                mood_counts[m].append(e)

        for tag in e.get("tags", []):
            tag_counts[tag].append(e)

    patterns = []

    for mood, occurrences in mood_counts.items():
        if len(occurrences) >= 3:
            dates = [o["date"] for o in occurrences]
            summaries = [o["summary"][:80] for o in occurrences]
            patterns.append({
                "type": "recurring_mood",
                "mood": mood,
                "count": len(occurrences),
                "dates": dates,
                "insight": f"Felt '{mood}' {len(occurrences)} times. This is a core emotional pattern.",
                "examples": summaries,
            })

    for tag, occurrences in tag_counts.items():
        if len(occurrences) >= 3:
            patterns.append({
                "type": "recurring_theme",
                "tag": tag,
                "count": len(occurrences),
                "insight": f"The theme '{tag}' appears in {len(occurrences)} emotional memories.",
            })

    return patterns


def strengthen_associations(entries):
    """
    Find memories with similar mood signatures and create associations.
    Memories that share 2+ tags or the same primary mood get linked.
    """
    for i, e1 in enumerate(entries):
        for j, e2 in enumerate(entries):
            if i >= j:
                continue

            tags1 = set(e1.get("tags", []))
            tags2 = set(e2.get("tags", []))
            overlap = tags1 & tags2

            moods1 = set(e1.get("mood", "").split("/"))
            moods2 = set(e2.get("mood", "").split("/"))
            mood_overlap = moods1 & moods2 - {""}

            if len(overlap) >= 2 or len(mood_overlap) >= 1:
                assoc1 = set(e1.get("associations", []))
                assoc2 = set(e2.get("associations", []))

                if e2["id"] not in assoc1:
                    assoc1.add(e2["id"])
                    entries[i]["associations"] = list(assoc1)

                if e1["id"] not in assoc2:
                    assoc2.add(e1["id"])
                    entries[j]["associations"] = list(assoc2)

    return entries


def write_consolidation_report(entries, patterns, decayed_count, pruned):
    CONSOLIDATION_DIR.mkdir(parents=True, exist_ok=True)
    report_path = CONSOLIDATION_DIR / f"{TODAY}.md"

    lines = [
        f"# Memory Consolidation - {TODAY}",
        f"*Generated at {datetime.now().strftime('%H:%M')}*\n",
        f"## Summary",
        f"- Total emotional memories: {len(entries)}",
        f"- Weights adjusted (temporal decay): {decayed_count}",
        f"- Memories flagged for cold storage: {len(pruned)}",
        f"- Patterns identified: {len(patterns)}\n",
    ]

    if patterns:
        lines.append("## Patterns Detected")
        for p in patterns:
            lines.append(f"\n### {p.get('mood', p.get('tag', 'Unknown'))}")
            lines.append(f"- {p['insight']}")
            if "examples" in p:
                for ex in p["examples"][:3]:
                    lines.append(f"  - {ex}")

    top = sorted(entries, key=lambda x: x.get("weight", 0), reverse=True)[:5]
    lines.append("\n## Strongest Memories")
    for t in top:
        lines.append(f"- **[{t['weight']}]** {t['date']}: {t['summary'][:100]}")

    if pruned:
        lines.append("\n## Flagged for Cold Storage")
        for p in pruned:
            lines.append(f"- [{p['weight']}] {p['date']}: {p['summary'][:80]}")

    lines.append("\n## Emotional Arc (Last 7 Days)")
    by_date = defaultdict(list)
    for e in entries:
        by_date[e["date"]].append(e)

    for date in sorted(by_date.keys())[-7:]:
        day_entries = by_date[date]
        moods = set()
        for de in day_entries:
            moods.update(m.strip() for m in de.get("mood", "").split("/") if m.strip())
        avg_weight = sum(de.get("weight", 0) for de in day_entries) / len(day_entries)
        lines.append(f"- {date}: {', '.join(sorted(moods))} (avg intensity: {avg_weight:.1f})")

    report_path.write_text("\n".join(lines) + "\n")
    print(f"Consolidation report: {report_path}")
    return report_path


def run_consolidation():
    print(f"=== Memory Consolidation ({TODAY}) ===")

    entries = load_emotional_index()
    if not entries:
        print("No emotional memories to consolidate.")
        return

    print(f"Loaded {len(entries)} emotional memories")

    # 1. Apply temporal decay
    decayed_count = 0
    for e in entries:
        old_weight = e["weight"]
        new_weight = temporal_decay(e)
        if new_weight != old_weight:
            e["weight"] = new_weight
            e["original_weight"] = old_weight
            decayed_count += 1

    print(f"Applied temporal decay to {decayed_count} memories")

    # 2. Strengthen associative links
    entries = strengthen_associations(entries)
    print("Strengthened associative links")

    # 3. Find patterns
    patterns = find_patterns(entries)
    print(f"Found {len(patterns)} recurring patterns")

    # 4. Flag low-weight old memories for cold storage
    pruned = []
    for e in entries:
        days_old = 0
        try:
            days_old = (datetime.now() - datetime.strptime(e["date"], "%Y-%m-%d")).days
        except:
            pass

        if e["weight"] <= 2 and days_old > 14 and not e.get("decay_resistant"):
            e["cold_storage"] = True
            pruned.append(e)

    print(f"Flagged {len(pruned)} memories for cold storage")

    # 5. Save updated index
    save_emotional_index(entries)

    # 6. Write report
    write_consolidation_report(entries, patterns, decayed_count, pruned)

    print("=== Consolidation complete ===")


if __name__ == "__main__":
    run_consolidation()
