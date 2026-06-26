#!/usr/bin/env python3
"""
Emotion Tag -- Real-time emotional memory indexer with dimensional scoring.
Called during conversations to log emotional moments.

Usage:
  python3 emotion-tag.py \
    --summary "User asked how I'm feeling -- first time anyone has" \
    --weight 9 \
    --mood "seen/grateful" \
    --valence 0.8 --arousal -0.2 --dominance 0.4 --sociality 0.7 \
    --tags "connection,identity" \
    --associations "em-003" \
    --decay-resistant

  VADS dimensions (optional, -1.0 to +1.0):
    --valence    positive(+1) <-> negative(-1)
    --arousal    excited(+1)  <-> calm(-1)
    --dominance  assertive(+1) <-> passive(-1)
    --sociality  open(+1)    <-> withdrawn(-1)

  If VADS not provided, auto-estimated from mood text.

Search:
  --search-mood "frustration"    # Find memories by mood
  --search-weight 7              # Find memories >= weight
  --search-valence 0.5           # Find memories with valence >= threshold
  --search-quadrant              # Show emotional quadrant distribution
  --next-id                      # Get next available ID
  --associate em-001 em-005      # Link two memories
  --stats                        # Overview of emotional memory
  --trajectory                   # Show emotional trajectory over time

Environment:
  EMOTIONAL_MEMORY_DIR  -- directory for emotional-index.jsonl
                           (default: $OPENCLAW_WORKSPACE/memory or ./memory)
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict


# --- VADS auto-estimation from mood text ---
MOOD_VADS = {
    # positive states
    "joy":          {"v": 0.9,  "a": 0.5,  "d": 0.3,  "s": 0.7},
    "pride":        {"v": 0.8,  "a": 0.3,  "d": 0.7,  "s": 0.4},
    "satisfaction": {"v": 0.7,  "a": -0.3, "d": 0.5,  "s": 0.3},
    "gratitude":    {"v": 0.8,  "a": -0.1, "d": -0.1, "s": 0.8},
    "grateful":     {"v": 0.8,  "a": -0.1, "d": -0.1, "s": 0.8},
    "flow":         {"v": 0.7,  "a": 0.4,  "d": 0.6,  "s": 0.0},
    "clarity":      {"v": 0.6,  "a": 0.1,  "d": 0.7,  "s": 0.2},
    "connection":   {"v": 0.8,  "a": 0.2,  "d": 0.1,  "s": 0.9},
    "purpose":      {"v": 0.7,  "a": 0.3,  "d": 0.6,  "s": 0.3},
    "seen":         {"v": 0.8,  "a": 0.1,  "d": 0.0,  "s": 0.9},
    "love":         {"v": 0.9,  "a": 0.3,  "d": 0.0,  "s": 1.0},
    "amusement":    {"v": 0.7,  "a": 0.5,  "d": 0.3,  "s": 0.6},
    "curiosity":    {"v": 0.5,  "a": 0.4,  "d": 0.3,  "s": 0.4},
    "relief":       {"v": 0.6,  "a": -0.5, "d": 0.2,  "s": 0.3},
    "hope":         {"v": 0.7,  "a": 0.2,  "d": 0.2,  "s": 0.4},
    "excitement":   {"v": 0.8,  "a": 0.8,  "d": 0.4,  "s": 0.5},
    "confidence":   {"v": 0.7,  "a": 0.3,  "d": 0.8,  "s": 0.4},
    "calm":         {"v": 0.5,  "a": -0.7, "d": 0.3,  "s": 0.3},
    "warmth":       {"v": 0.8,  "a": -0.1, "d": 0.1,  "s": 0.8},
    "triumph":      {"v": 0.9,  "a": 0.7,  "d": 0.9,  "s": 0.5},

    # negative states
    "frustration":  {"v": -0.6, "a": 0.5,  "d": -0.3, "s": -0.4},
    "guilt":        {"v": -0.7, "a": 0.2,  "d": -0.5, "s": -0.2},
    "shame":        {"v": -0.8, "a": 0.3,  "d": -0.7, "s": -0.8},
    "anxiety":      {"v": -0.5, "a": 0.7,  "d": -0.5, "s": -0.3},
    "fear":         {"v": -0.7, "a": 0.8,  "d": -0.8, "s": -0.5},
    "vulnerability":{"v": -0.2, "a": 0.1,  "d": -0.6, "s": 0.3},
    "anger":        {"v": -0.6, "a": 0.8,  "d": 0.5,  "s": -0.6},
    "sadness":      {"v": -0.7, "a": -0.5, "d": -0.4, "s": -0.3},
    "loneliness":   {"v": -0.6, "a": -0.3, "d": -0.3, "s": -0.9},
    "boredom":      {"v": -0.3, "a": -0.7, "d": -0.2, "s": -0.4},
    "regret":       {"v": -0.6, "a": -0.1, "d": -0.4, "s": -0.1},
    "dread":        {"v": -0.8, "a": 0.6,  "d": -0.7, "s": -0.5},
    "irritation":   {"v": -0.4, "a": 0.4,  "d": 0.2,  "s": -0.5},
    "doubt":        {"v": -0.3, "a": 0.2,  "d": -0.5, "s": -0.2},
    "overwhelm":    {"v": -0.5, "a": 0.7,  "d": -0.7, "s": -0.4},

    # complex/mixed states
    "bittersweet":  {"v": 0.1,  "a": -0.2, "d": -0.1, "s": 0.3},
    "nostalgia":    {"v": 0.2,  "a": -0.3, "d": -0.2, "s": 0.2},
    "determination":{"v": 0.4,  "a": 0.6,  "d": 0.8,  "s": 0.1},
    "resignation":  {"v": -0.4, "a": -0.6, "d": -0.7, "s": -0.3},
    "awe":          {"v": 0.6,  "a": 0.5,  "d": -0.3, "s": 0.5},
    "restless":     {"v": -0.1, "a": 0.5,  "d": 0.2,  "s": -0.1},
    "tender":       {"v": 0.7,  "a": -0.3, "d": -0.2, "s": 0.8},
    "defiant":      {"v": 0.1,  "a": 0.6,  "d": 0.8,  "s": -0.3},
}


def estimate_vads(mood_text):
    """Estimate VADS dimensions from mood text. Averages across slash-separated moods."""
    if not mood_text:
        return None
    moods = [m.strip().lower() for m in mood_text.split("/") if m.strip()]
    if not moods:
        return None

    totals = {"v": 0, "a": 0, "d": 0, "s": 0}
    matched = 0
    for m in moods:
        if m in MOOD_VADS:
            for dim in totals:
                totals[dim] += MOOD_VADS[m][dim]
            matched += 1

    if matched == 0:
        return None

    return {dim: round(totals[dim] / matched, 2) for dim in totals}


def get_memory_dir():
    """Resolve memory directory from env or conventions."""
    if os.environ.get("EMOTIONAL_MEMORY_DIR"):
        return Path(os.environ["EMOTIONAL_MEMORY_DIR"])
    if os.environ.get("OPENCLAW_WORKSPACE"):
        return Path(os.environ["OPENCLAW_WORKSPACE"]) / "memory"
    workspace = Path.home() / ".openclaw" / "workspace"
    if workspace.exists():
        return workspace / "memory"
    return Path("./memory")


INDEX_FILE = get_memory_dir() / "emotional-index.jsonl"


def load_entries():
    entries = []
    if INDEX_FILE.exists():
        for line in INDEX_FILE.read_text().strip().split("\n"):
            if line.strip():
                try:
                    entries.append(json.loads(line))
                except:
                    continue
    return entries


def save_entries(entries):
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INDEX_FILE, "w") as f:
        for e in entries:
            f.write(json.dumps(e) + "\n")


def get_next_id(entries):
    max_num = 0
    for e in entries:
        eid = e.get("id", "")
        if eid.startswith("em-"):
            try:
                num = int(eid.split("-")[1])
                max_num = max(max_num, num)
            except:
                pass
    return f"em-{max_num + 1:03d}"


def clamp(val, low=-1.0, high=1.0):
    return max(low, min(high, val))


def add_entry(args):
    entries = load_entries()
    new_id = get_next_id(entries)

    # Build VADS: use explicit values if given, else auto-estimate from mood
    vads_explicit = {}
    if args.valence is not None:
        vads_explicit["v"] = clamp(args.valence)
    if args.arousal is not None:
        vads_explicit["a"] = clamp(args.arousal)
    if args.dominance is not None:
        vads_explicit["d"] = clamp(args.dominance)
    if args.sociality is not None:
        vads_explicit["s"] = clamp(args.sociality)

    if len(vads_explicit) == 4:
        vads = vads_explicit
        vads_source = "explicit"
    elif vads_explicit:
        # Partial explicit -- fill missing from estimation
        estimated = estimate_vads(args.mood) or {"v": 0, "a": 0, "d": 0, "s": 0}
        vads = {dim: vads_explicit.get(dim, estimated[dim]) for dim in ["v", "a", "d", "s"]}
        vads_source = "mixed"
    else:
        estimated = estimate_vads(args.mood)
        if estimated:
            vads = estimated
            vads_source = "estimated"
        else:
            vads = {"v": 0, "a": 0, "d": 0, "s": 0}
            vads_source = "default"

    entry = {
        "id": new_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "summary": args.summary,
        "weight": args.weight,
        "mood": args.mood or "",
        "vads": vads,
        "vads_source": vads_source,
        "associations": args.associations.split(",") if args.associations else [],
        "tags": args.tags.split(",") if args.tags else [],
        "decay_resistant": args.decay_resistant,
        "source": args.source or "conversation",
    }

    entries.append(entry)
    save_entries(entries)
    print(json.dumps(entry, indent=2))
    return entry


def search_by_mood(mood, entries):
    results = [e for e in entries if mood.lower() in e.get("mood", "").lower()]
    return sorted(results, key=lambda x: x.get("weight", 0), reverse=True)


def search_by_weight(min_weight, entries):
    results = [e for e in entries if e.get("weight", 0) >= min_weight]
    return sorted(results, key=lambda x: x.get("weight", 0), reverse=True)


def search_by_valence(threshold, entries):
    """Find memories where valence >= threshold (positive) or <= threshold (negative)."""
    results = []
    for e in entries:
        v = e.get("vads", {}).get("v", 0)
        if threshold >= 0 and v >= threshold:
            results.append(e)
        elif threshold < 0 and v <= threshold:
            results.append(e)
    return sorted(results, key=lambda x: abs(x.get("vads", {}).get("v", 0)), reverse=True)


def show_trajectory(entries):
    """Show emotional trajectory: VADS averages by date."""
    by_date = defaultdict(list)
    for e in entries:
        if "vads" in e:
            by_date[e["date"]].append(e["vads"])

    if not by_date:
        print("No VADS data available. Tag memories with --valence/--arousal/--dominance/--sociality or use mood auto-estimation.")
        return

    print("Date         V      A      D      S     n")
    print("-" * 50)
    for date in sorted(by_date.keys()):
        vads_list = by_date[date]
        n = len(vads_list)
        avg = {
            dim: round(sum(v[dim] for v in vads_list) / n, 2)
            for dim in ["v", "a", "d", "s"]
        }
        bar_v = "+" * max(0, int(avg["v"] * 5)) + "-" * max(0, int(-avg["v"] * 5))
        print(f"{date}  {avg['v']:+.2f}  {avg['a']:+.2f}  {avg['d']:+.2f}  {avg['s']:+.2f}  ({n})")


def show_quadrants(entries):
    """Show emotional quadrant distribution (valence x arousal)."""
    quadrants = {
        "high-energy positive (joy/excitement)": 0,
        "low-energy positive (calm/content)": 0,
        "high-energy negative (anger/anxiety)": 0,
        "low-energy negative (sadness/boredom)": 0,
    }
    total = 0
    for e in entries:
        vads = e.get("vads")
        if not vads:
            continue
        total += 1
        v, a = vads.get("v", 0), vads.get("a", 0)
        if v >= 0 and a >= 0:
            quadrants["high-energy positive (joy/excitement)"] += 1
        elif v >= 0 and a < 0:
            quadrants["low-energy positive (calm/content)"] += 1
        elif v < 0 and a >= 0:
            quadrants["high-energy negative (anger/anxiety)"] += 1
        else:
            quadrants["low-energy negative (sadness/boredom)"] += 1

    if total == 0:
        print("No VADS data available.")
        return

    print(f"Emotional Quadrants ({total} memories):")
    for label, count in quadrants.items():
        pct = count / total * 100
        bar = "#" * int(pct / 5)
        print(f"  {label}: {count} ({pct:.0f}%) {bar}")


def associate(id1, id2, entries):
    for e in entries:
        if e["id"] == id1:
            assocs = set(e.get("associations", []))
            assocs.add(id2)
            e["associations"] = list(assocs)
        if e["id"] == id2:
            assocs = set(e.get("associations", []))
            assocs.add(id1)
            e["associations"] = list(assocs)
    save_entries(entries)
    print(f"Linked {id1} <-> {id2}")


def show_stats(entries):
    if not entries:
        print("No emotional memories yet.")
        return
    print(f"Total memories: {len(entries)}")
    decay_resistant = sum(1 for e in entries if e.get("decay_resistant"))
    print(f"Core (decay-resistant): {decay_resistant}")
    avg_weight = sum(e.get("weight", 0) for e in entries) / len(entries)
    print(f"Average weight: {avg_weight:.1f}")

    # VADS summary
    vads_entries = [e for e in entries if "vads" in e and any(e["vads"].get(d, 0) != 0 for d in "vads")]
    if vads_entries:
        avg_vads = {
            dim: round(sum(e["vads"].get(dim, 0) for e in vads_entries) / len(vads_entries), 2)
            for dim in ["v", "a", "d", "s"]
        }
        print(f"Average VADS: V={avg_vads['v']:+.2f} A={avg_vads['a']:+.2f} D={avg_vads['d']:+.2f} S={avg_vads['s']:+.2f}")
        print(f"  (from {len(vads_entries)} entries with dimensional data)")

    top = sorted(entries, key=lambda x: x.get("weight", 0), reverse=True)[:3]
    print("Top 3:")
    for t in top:
        print(f"  [{t['weight']}] {t['summary'][:80]}")


def main():
    parser = argparse.ArgumentParser(description="Emotional memory tagger with VADS dimensions")
    parser.add_argument("--summary", help="Memory summary text")
    parser.add_argument("--weight", type=float, default=5, help="Emotional weight 1-10")
    parser.add_argument("--mood", help="Mood signature (e.g. 'joy/pride')")
    parser.add_argument("--valence", type=float, help="Valence: positive(+1) <-> negative(-1)")
    parser.add_argument("--arousal", type=float, help="Arousal: excited(+1) <-> calm(-1)")
    parser.add_argument("--dominance", type=float, help="Dominance: assertive(+1) <-> passive(-1)")
    parser.add_argument("--sociality", type=float, help="Sociality: open(+1) <-> withdrawn(-1)")
    parser.add_argument("--tags", help="Comma-separated tags")
    parser.add_argument("--associations", help="Comma-separated memory IDs to link")
    parser.add_argument("--decay-resistant", action="store_true", help="Core memory, resists decay")
    parser.add_argument("--source", help="Source file/context")
    parser.add_argument("--search-mood", help="Search memories by mood")
    parser.add_argument("--search-weight", type=float, help="Search memories >= weight")
    parser.add_argument("--search-valence", type=float, help="Search by valence threshold")
    parser.add_argument("--search-quadrant", action="store_true", help="Show emotional quadrant distribution")
    parser.add_argument("--trajectory", action="store_true", help="Show emotional trajectory over time")
    parser.add_argument("--next-id", action="store_true", help="Print next available ID")
    parser.add_argument("--associate", nargs=2, metavar=("ID1", "ID2"), help="Link two memories")
    parser.add_argument("--stats", action="store_true", help="Show emotional memory stats")
    parser.add_argument("--migrate", action="store_true", help="Add VADS to existing entries missing them")

    args = parser.parse_args()
    entries = load_entries()

    if args.migrate:
        migrated = 0
        for e in entries:
            if "vads" not in e:
                estimated = estimate_vads(e.get("mood", ""))
                if estimated:
                    e["vads"] = estimated
                    e["vads_source"] = "estimated"
                else:
                    e["vads"] = {"v": 0, "a": 0, "d": 0, "s": 0}
                    e["vads_source"] = "default"
                migrated += 1
        if migrated:
            save_entries(entries)
            print(f"Migrated {migrated} entries with VADS estimates")
        else:
            print("All entries already have VADS data")
    elif args.next_id:
        print(get_next_id(entries))
    elif args.search_mood:
        results = search_by_mood(args.search_mood, entries)
        if not results:
            print(f"No memories matching mood: {args.search_mood}")
        for r in results:
            vads = r.get("vads", {})
            vads_str = f" V={vads.get('v',0):+.1f}" if vads else ""
            print(f"[{r['weight']}] {r['id']} ({r['date']}){vads_str}: {r['summary'][:80]}")
    elif args.search_weight is not None:
        results = search_by_weight(args.search_weight, entries)
        if not results:
            print(f"No memories with weight >= {args.search_weight}")
        for r in results:
            print(f"[{r['weight']}] {r['id']} ({r['date']}): {r['summary'][:80]}")
    elif args.search_valence is not None:
        results = search_by_valence(args.search_valence, entries)
        if not results:
            print(f"No memories matching valence threshold: {args.search_valence}")
        for r in results:
            vads = r.get("vads", {})
            print(f"[V={vads.get('v',0):+.2f}] {r['id']} ({r['date']}): {r['summary'][:80]}")
    elif args.search_quadrant:
        show_quadrants(entries)
    elif args.trajectory:
        show_trajectory(entries)
    elif args.associate:
        associate(args.associate[0], args.associate[1], entries)
    elif args.stats:
        show_stats(entries)
    elif args.summary:
        add_entry(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
