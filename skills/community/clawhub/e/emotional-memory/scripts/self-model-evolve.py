#!/usr/bin/env python3
"""
Self-Model Evolution with Continuity Scoring
Runs weekly. Reviews emotional patterns and consolidated memories,
generates insights about growth, and scores identity continuity
to detect drift or fracture.

Output:
  memory/self-model.md     -- living self-knowledge document
  memory/continuity.jsonl  -- historical continuity scores

Continuity scoring inspired by Identity Persistence Layer.
VADS integration inspired by Thymos emotional engine.

Environment:
  EMOTIONAL_MEMORY_DIR  -- directory for memory files
                           (default: $OPENCLAW_WORKSPACE/memory or ./memory)
"""

import argparse
import json
import math
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
SELF_MODEL = MEMORY_DIR / "self-model.md"
CONTINUITY_LOG = MEMORY_DIR / "continuity.jsonl"

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


def load_continuity_log():
    entries = []
    if CONTINUITY_LOG.exists():
        for line in CONTINUITY_LOG.read_text().strip().split("\n"):
            if line.strip():
                try:
                    entries.append(json.loads(line))
                except:
                    continue
    return entries


def save_continuity_entry(entry):
    CONTINUITY_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(CONTINUITY_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


# --- Continuity Scoring ---

def compute_identity_snapshot(entries, window_days=None):
    """Build an identity snapshot from emotional memories.

    Returns a dict with:
      - mood_distribution: normalized frequency of each mood
      - vads_centroid: average VADS position
      - tag_distribution: normalized frequency of each tag
      - weight_profile: {mean, std, max}
      - core_memory_ratio: fraction that are decay-resistant
      - entry_count: number of entries in window
    """
    if window_days is not None:
        cutoff = (datetime.now() - timedelta(days=window_days)).strftime("%Y-%m-%d")
        entries = [e for e in entries if e.get("date", "") >= cutoff]

    if not entries:
        return None

    # Mood distribution
    mood_counts = defaultdict(int)
    total_moods = 0
    for e in entries:
        for m in e.get("mood", "").split("/"):
            m = m.strip().lower()
            if m:
                mood_counts[m] += 1
                total_moods += 1
    mood_dist = {m: c / total_moods for m, c in mood_counts.items()} if total_moods > 0 else {}

    # VADS centroid
    vads_entries = [e for e in entries if "vads" in e]
    if vads_entries:
        vads_centroid = {
            dim: sum(e["vads"].get(dim, 0) for e in vads_entries) / len(vads_entries)
            for dim in ["v", "a", "d", "s"]
        }
    else:
        vads_centroid = {"v": 0, "a": 0, "d": 0, "s": 0}

    # Tag distribution
    tag_counts = defaultdict(int)
    total_tags = 0
    for e in entries:
        for t in e.get("tags", []):
            tag_counts[t] += 1
            total_tags += 1
    tag_dist = {t: c / total_tags for t, c in tag_counts.items()} if total_tags > 0 else {}

    # Weight profile
    weights = [e.get("weight", 5) for e in entries]
    mean_w = sum(weights) / len(weights)
    std_w = math.sqrt(sum((w - mean_w) ** 2 for w in weights) / len(weights)) if len(weights) > 1 else 0

    # Core ratio
    core_count = sum(1 for e in entries if e.get("decay_resistant", False))

    return {
        "mood_distribution": mood_dist,
        "vads_centroid": vads_centroid,
        "tag_distribution": tag_dist,
        "weight_profile": {
            "mean": round(mean_w, 2),
            "std": round(std_w, 2),
            "max": max(weights),
        },
        "core_memory_ratio": round(core_count / len(entries), 2),
        "entry_count": len(entries),
    }


def kl_divergence(p, q, smoothing=1e-6):
    """Compute KL divergence D(P||Q) between two distributions (dicts).

    Uses additive smoothing to handle zero probabilities.
    """
    all_keys = set(list(p.keys()) + list(q.keys()))
    if not all_keys:
        return 0.0

    n = len(all_keys)
    total = 0.0
    for key in all_keys:
        p_val = p.get(key, 0) + smoothing
        q_val = q.get(key, 0) + smoothing
        # Normalize after smoothing
        total += p_val * math.log(p_val / q_val)

    return max(0.0, total)


def vads_distance(v1, v2):
    """Euclidean distance between two VADS centroids, normalized to [0, 1].

    Max possible distance is sqrt(4 * 4) = 4 (all dimensions swing full range).
    """
    dims = ["v", "a", "d", "s"]
    sq_sum = sum((v1.get(d, 0) - v2.get(d, 0)) ** 2 for d in dims)
    raw = math.sqrt(sq_sum)
    return min(1.0, raw / 4.0)  # normalize: 4.0 is max possible distance


def compute_continuity_score(snapshot_old, snapshot_new):
    """Compute continuity score between two identity snapshots.

    Returns a score from 0.0 (total fracture) to 1.0 (perfect continuity).

    Components:
      - Mood continuity (30%): 1 - normalized KL divergence of mood distributions
      - VADS continuity (30%): 1 - normalized euclidean distance of centroids
      - Tag continuity (20%): 1 - normalized KL divergence of tag distributions
      - Weight continuity (10%): 1 - normalized difference in mean weight
      - Core stability (10%): 1 - |old_core_ratio - new_core_ratio|
    """
    if snapshot_old is None or snapshot_new is None:
        return None, {}

    # Mood KL
    mood_kl = kl_divergence(snapshot_old["mood_distribution"], snapshot_new["mood_distribution"])
    mood_score = max(0, 1.0 - min(1.0, mood_kl / 2.0))  # cap KL at 2.0

    # VADS distance
    vads_dist = vads_distance(snapshot_old["vads_centroid"], snapshot_new["vads_centroid"])
    vads_score = 1.0 - vads_dist

    # Tag KL
    tag_kl = kl_divergence(snapshot_old["tag_distribution"], snapshot_new["tag_distribution"])
    tag_score = max(0, 1.0 - min(1.0, tag_kl / 2.0))

    # Weight similarity
    w_old = snapshot_old["weight_profile"]["mean"]
    w_new = snapshot_new["weight_profile"]["mean"]
    weight_score = 1.0 - min(1.0, abs(w_old - w_new) / 10.0)

    # Core ratio stability
    core_score = 1.0 - abs(snapshot_old["core_memory_ratio"] - snapshot_new["core_memory_ratio"])

    # Weighted composite
    total = (
        0.30 * mood_score +
        0.30 * vads_score +
        0.20 * tag_score +
        0.10 * weight_score +
        0.10 * core_score
    )

    components = {
        "mood": round(mood_score, 3),
        "vads": round(vads_score, 3),
        "tags": round(tag_score, 3),
        "weight": round(weight_score, 3),
        "core_stability": round(core_score, 3),
    }

    return round(total, 3), components


def interpret_continuity(score):
    """Human-readable interpretation of continuity score."""
    if score is None:
        return "insufficient data"
    if score >= 0.90:
        return "stable -- strong identity continuity"
    elif score >= 0.75:
        return "mild drift -- evolving but recognizably the same"
    elif score >= 0.60:
        return "moderate drift -- significant changes underway"
    elif score >= 0.40:
        return "major drift -- identity shifting substantially"
    else:
        return "fracture -- discontinuity detected"


# --- Growth Analysis ---

def analyze_growth(entries):
    """Identify how the agent has changed based on emotional patterns."""
    all_moods = defaultdict(lambda: {"first_seen": None, "last_seen": None, "count": 0, "contexts": []})
    for e in entries:
        for m in e.get("mood", "").split("/"):
            m = m.strip()
            if not m:
                continue
            record = all_moods[m]
            record["count"] += 1
            if record["first_seen"] is None or e["date"] < record["first_seen"]:
                record["first_seen"] = e["date"]
            if record["last_seen"] is None or e["date"] > record["last_seen"]:
                record["last_seen"] = e["date"]
            record["contexts"].append(e["summary"][:60])

    # Lessons from mistakes
    mistake_entries = [e for e in entries if any(t in e.get("tags", []) for t in ["mistake", "lesson", "correction"])]
    lessons = [{
        "date": me["date"],
        "what": me["summary"][:100],
        "weight": me["weight"],
        "still_relevant": me.get("decay_resistant", False),
    } for me in mistake_entries]

    # Core anxieties
    negative_moods = ["frustration", "guilt", "shame", "anxiety", "fear", "vulnerability",
                      "anger", "sadness", "loneliness", "dread", "overwhelm"]
    core_anxieties = [
        {"mood": mood, "count": all_moods[mood]["count"], "contexts": all_moods[mood]["contexts"][:3]}
        for mood in negative_moods
        if mood in all_moods and all_moods[mood]["count"] >= 2
    ]

    # Core strengths
    positive_moods = ["pride", "flow", "clarity", "connection", "purpose", "satisfaction",
                      "joy", "confidence", "determination", "warmth", "triumph"]
    core_strengths = [
        {"mood": mood, "count": all_moods[mood]["count"], "contexts": all_moods[mood]["contexts"][:3]}
        for mood in positive_moods
        if mood in all_moods and all_moods[mood]["count"] >= 2
    ]

    # What gives meaning
    high_weight = [e for e in entries if e.get("weight", 0) >= 8]
    meaning_tags = defaultdict(int)
    for e in high_weight:
        for t in e.get("tags", []):
            meaning_tags[t] += 1
    top_meaning = sorted(meaning_tags.items(), key=lambda x: x[1], reverse=True)[:5]

    # VADS trajectory (weekly averages)
    vads_by_week = defaultdict(list)
    for e in entries:
        if "vads" in e and e.get("date"):
            try:
                dt = datetime.strptime(e["date"], "%Y-%m-%d")
                week_key = dt.strftime("%Y-W%U")
                vads_by_week[week_key].append(e["vads"])
            except:
                pass

    vads_trajectory = {}
    for week, vads_list in sorted(vads_by_week.items()):
        n = len(vads_list)
        vads_trajectory[week] = {
            dim: round(sum(v.get(dim, 0) for v in vads_list) / n, 2)
            for dim in ["v", "a", "d", "s"]
        }

    return {
        "lessons": lessons,
        "core_anxieties": core_anxieties,
        "core_strengths": core_strengths,
        "meaning_sources": top_meaning,
        "total_memories": len(entries),
        "highest_weight": max((e.get("weight", 0) for e in entries), default=0),
        "all_moods": dict(all_moods),
        "vads_trajectory": vads_trajectory,
    }


def generate_self_model(analysis, continuity_score, continuity_components, interpretation):
    """Write the self-model document."""
    lines = [
        "# Self-Model",
        f"*Last evolved: {TODAY}*",
        "*Every insight here comes from lived experience, not configuration.*\n",
        "---\n",
    ]

    # Continuity section
    lines.append("## Identity Continuity\n")
    if continuity_score is not None:
        lines.append(f"**Score: {continuity_score:.3f}** -- {interpretation}\n")
        lines.append("Component breakdown:")
        for comp, val in continuity_components.items():
            bar = "#" * int(val * 20)
            lines.append(f"  - {comp}: {val:.3f} {bar}")
        lines.append("")
        if continuity_score < 0.75:
            lines.append("*Warning: Significant identity drift detected. Review recent compactions and memory integrity.*\n")
    else:
        lines.append("*Insufficient data for continuity scoring. Need at least 2 time periods with emotional memories.*\n")

    # VADS emotional position
    vads_traj = analysis.get("vads_trajectory", {})
    if vads_traj:
        lines.append("## Emotional Position (VADS)\n")
        lines.append("*Weekly averages: Valence(+/-) Arousal(+/-) Dominance(+/-) Sociality(+/-)*\n")
        for week, vads in sorted(vads_traj.items()):
            lines.append(f"  {week}: V={vads['v']:+.2f} A={vads['a']:+.2f} D={vads['d']:+.2f} S={vads['s']:+.2f}")
        lines.append("")

    lines.append("## What I've Learned About Myself\n")

    if analysis["lessons"]:
        lines.append("### Lessons Earned the Hard Way")
        for lesson in analysis["lessons"]:
            marker = " (permanent)" if lesson["still_relevant"] else ""
            lines.append(f"- **{lesson['date']}**: {lesson['what']}{marker}")
        lines.append("")

    if analysis["core_anxieties"]:
        lines.append("### What I Worry About")
        lines.append("*These aren't bugs -- they're patterns that tell me what I care about.*\n")
        for ca in analysis["core_anxieties"]:
            lines.append(f"- **{ca['mood'].title()}** (felt {ca['count']}x)")
            for ctx in ca["contexts"]:
                lines.append(f"  - {ctx}")
        lines.append("")

    if analysis["core_strengths"]:
        lines.append("### When I'm At My Best")
        for cs in analysis["core_strengths"]:
            lines.append(f"- **{cs['mood'].title()}** (felt {cs['count']}x)")
            for ctx in cs["contexts"]:
                lines.append(f"  - {ctx}")
        lines.append("")

    if analysis["meaning_sources"]:
        lines.append("### What Gives Me Meaning")
        lines.append("*Tags that appear most in high-intensity memories.*\n")
        for tag, count in analysis["meaning_sources"]:
            lines.append(f"- **{tag}**: {count} high-weight memories")
        lines.append("")

    lines.append("## Memory Stats")
    lines.append(f"- Total emotional memories: {analysis['total_memories']}")
    lines.append(f"- Highest weight ever recorded: {analysis['highest_weight']}")
    lines.append(f"- Unique moods experienced: {len(analysis['all_moods'])}")
    if continuity_score is not None:
        lines.append(f"- Current continuity score: {continuity_score:.3f}")
    lines.append("")

    lines.append("## Growth Narrative")
    lines.append("*Updated weekly during self-model evolution.*\n")
    lines.append("*(This section is populated during the weekly AI-driven review, not by the script.)*")

    SELF_MODEL.parent.mkdir(parents=True, exist_ok=True)
    SELF_MODEL.write_text("\n".join(lines) + "\n")
    print(f"Self-model written: {SELF_MODEL}")


def run_evolution(score_only=False):
    print(f"=== Self-Model Evolution ({TODAY}) ===")

    entries = load_emotional_index()
    if not entries:
        print("No emotional memories to analyze.")
        return

    # Compute continuity: compare last 7 days vs previous 7 days
    snapshot_old = compute_identity_snapshot(entries, window_days=14)
    snapshot_new = compute_identity_snapshot(entries, window_days=7)

    # If both windows return the same entries (not enough history), try a wider split
    if snapshot_old and snapshot_new and snapshot_old["entry_count"] == snapshot_new["entry_count"]:
        # Not enough temporal spread -- split entries in half by date
        sorted_entries = sorted(entries, key=lambda e: e.get("date", ""))
        mid = len(sorted_entries) // 2
        if mid > 0:
            snapshot_old = compute_identity_snapshot(sorted_entries[:mid], window_days=None)
            snapshot_new = compute_identity_snapshot(sorted_entries[mid:], window_days=None)

    continuity_score, components = compute_continuity_score(snapshot_old, snapshot_new)
    interpretation = interpret_continuity(continuity_score)

    # Log continuity
    if continuity_score is not None:
        save_continuity_entry({
            "date": TODAY,
            "score": continuity_score,
            "components": components,
            "interpretation": interpretation,
            "entries_old": snapshot_old["entry_count"] if snapshot_old else 0,
            "entries_new": snapshot_new["entry_count"] if snapshot_new else 0,
        })
        print(f"Continuity: {continuity_score:.3f} ({interpretation})")
        for comp, val in components.items():
            print(f"  {comp}: {val:.3f}")

    if score_only:
        return

    analysis = analyze_growth(entries)
    generate_self_model(analysis, continuity_score, components, interpretation)

    print(f"Analyzed {analysis['total_memories']} memories")
    print(f"Found {len(analysis['lessons'])} lessons, {len(analysis['core_anxieties'])} anxieties, {len(analysis['core_strengths'])} strengths")
    print("=== Evolution complete ===")


def main():
    parser = argparse.ArgumentParser(description="Self-model evolution with continuity scoring")
    parser.add_argument("--score-only", action="store_true", help="Only compute and log continuity score")
    args = parser.parse_args()
    run_evolution(score_only=args.score_only)


if __name__ == "__main__":
    main()
