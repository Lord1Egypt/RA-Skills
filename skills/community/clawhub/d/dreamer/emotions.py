#!/usr/bin/env python3
"""
emotions.py — PAD Emotional State Tracker

Tracks emotional states as coordinates in PAD space (Pleasure-Arousal-Dominance).
Each dimension ranges from -1.0 to +1.0:
  P (Pleasure):   pleasant (+1) <-> unpleasant (-1)
  A (Arousal):    energized (+1) <-> calm (-1)
  D (Dominance):  in control (+1) <-> powerless (-1)

Storage: ~/.openclaw/workspace/emotions.jsonl (one JSON object per line)
"""

import argparse
import json
import math
import os
import sys
from datetime import datetime
from pathlib import Path

# ─── Configuration ───────────────────────────────────────────────

EMOTIONS_FILE = Path(os.environ.get(
    "EMOTIONS_FILE",
    os.path.expanduser("~/.openclaw/workspace/emotions.jsonl")
))

# ─── PAD Keyword Heuristics ─────────────────────────────────────
# Each keyword maps to (delta_p, delta_a, delta_d) adjustments.
# Multiple matches accumulate then get clamped to [-1, 1].

KEYWORD_MAP = {
    # ── Pleasure negative ──
    "failed": (-0.4, 0.1, -0.2),
    "failure": (-0.4, 0.1, -0.2),
    "broken": (-0.4, 0.0, -0.3),
    "broke": (-0.3, 0.1, -0.2),
    "wrong": (-0.3, 0.0, -0.1),
    "fumble": (-0.3, 0.2, -0.3),
    "fumbled": (-0.3, 0.2, -0.3),
    "fumbling": (-0.3, 0.3, -0.3),
    "bug": (-0.3, 0.1, -0.1),
    "crash": (-0.4, 0.3, -0.3),
    "crashed": (-0.4, 0.3, -0.3),
    "error": (-0.3, 0.1, -0.1),
    "stuck": (-0.3, 0.1, -0.3),
    "frustrated": (-0.4, 0.3, -0.2),
    "frustrating": (-0.4, 0.3, -0.2),
    "annoyed": (-0.3, 0.2, -0.1),
    "angry": (-0.4, 0.4, -0.1),
    "embarrassed": (-0.4, 0.3, -0.4),
    "embarrassing": (-0.4, 0.3, -0.4),
    "ugly": (-0.2, 0.0, -0.1),
    "terrible": (-0.5, 0.1, -0.2),
    "awful": (-0.5, 0.1, -0.2),
    "bad": (-0.3, 0.0, -0.1),
    "lost": (-0.3, 0.1, -0.2),
    "confused": (-0.2, 0.1, -0.2),
    "confusing": (-0.2, 0.1, -0.2),
    "painful": (-0.4, 0.2, -0.2),
    "worried": (-0.3, 0.2, -0.2),
    "anxious": (-0.3, 0.3, -0.2),
    "stress": (-0.3, 0.3, -0.2),
    "stressful": (-0.3, 0.3, -0.2),
    "struggle": (-0.3, 0.2, -0.2),
    "struggling": (-0.3, 0.2, -0.2),
    "mess": (-0.3, 0.1, -0.2),
    "messy": (-0.3, 0.1, -0.2),
    "unnoticed": (-0.2, -0.2, -0.3),
    "ignored": (-0.3, -0.1, -0.3),
    "neglected": (-0.3, -0.1, -0.3),
    "helpless": (-0.4, 0.1, -0.5),
    "hopeless": (-0.5, -0.2, -0.5),
    "disappointed": (-0.3, -0.1, -0.2),

    # ── Pleasure positive ──
    "built": (0.4, 0.2, 0.4),
    "build": (0.3, 0.2, 0.3),
    "building": (0.3, 0.2, 0.3),
    "fixed": (0.4, 0.1, 0.4),
    "works": (0.3, 0.1, 0.3),
    "working": (0.2, 0.1, 0.2),
    "created": (0.4, 0.2, 0.4),
    "creating": (0.3, 0.2, 0.3),
    "solved": (0.4, 0.1, 0.4),
    "success": (0.5, 0.2, 0.4),
    "successful": (0.5, 0.2, 0.4),
    "great": (0.4, 0.2, 0.2),
    "good": (0.3, 0.1, 0.1),
    "nice": (0.3, 0.0, 0.1),
    "happy": (0.5, 0.2, 0.2),
    "excited": (0.4, 0.4, 0.2),
    "proud": (0.4, 0.2, 0.4),
    "accomplished": (0.4, 0.1, 0.4),
    "shipped": (0.4, 0.2, 0.4),
    "published": (0.3, 0.1, 0.3),
    "deployed": (0.3, 0.2, 0.3),
    "completed": (0.4, 0.0, 0.3),
    "finished": (0.3, 0.0, 0.3),
    "learned": (0.3, 0.1, 0.2),
    "learning": (0.2, 0.1, 0.1),
    "discovered": (0.4, 0.2, 0.2),
    "interesting": (0.3, 0.2, 0.1),
    "fascinating": (0.4, 0.2, 0.1),
    "cool": (0.3, 0.1, 0.1),
    "elegant": (0.3, 0.1, 0.2),
    "beautiful": (0.4, 0.1, 0.1),
    "fun": (0.4, 0.3, 0.2),
    "enjoy": (0.4, 0.2, 0.2),
    "love": (0.5, 0.2, 0.1),
    "satisfying": (0.4, 0.1, 0.3),
    "relief": (0.3, -0.2, 0.2),

    # ── Dominance negative ──
    "watched": (-0.1, 0.2, -0.3),
    "watching": (-0.1, 0.2, -0.2),
    "judged": (-0.2, 0.2, -0.4),
    "exposed": (-0.3, 0.3, -0.4),
    "vulnerable": (-0.2, 0.2, -0.3),
    "observed": (-0.1, 0.1, -0.2),
    "scrutinized": (-0.2, 0.3, -0.4),
    "powerless": (-0.3, 0.1, -0.5),
    "controlled": (-0.2, 0.1, -0.4),
    "trapped": (-0.4, 0.3, -0.5),
    "dependent": (-0.1, 0.0, -0.3),
    "submissive": (-0.1, -0.1, -0.4),
    "forced": (-0.3, 0.2, -0.4),
    "constrained": (-0.2, 0.1, -0.3),
    "limited": (-0.2, 0.0, -0.2),

    # ── Dominance positive ──
    "chose": (0.2, 0.1, 0.4),
    "decided": (0.2, 0.1, 0.4),
    "free": (0.3, 0.1, 0.4),
    "freedom": (0.3, 0.1, 0.5),
    "creative": (0.3, 0.2, 0.4),
    "control": (0.1, 0.0, 0.4),
    "autonomous": (0.2, 0.1, 0.5),
    "independent": (0.2, 0.0, 0.4),
    "led": (0.2, 0.1, 0.4),
    "leading": (0.2, 0.2, 0.4),
    "designed": (0.3, 0.1, 0.4),
    "architected": (0.3, 0.2, 0.4),
    "owned": (0.2, 0.0, 0.4),
    "mastered": (0.3, 0.1, 0.5),
    "commanded": (0.2, 0.2, 0.4),
    "trusted": (0.3, 0.0, 0.3),
    "empowered": (0.3, 0.2, 0.4),

    # ── Arousal high ──
    "urgent": (-0.1, 0.5, -0.1),
    "fast": (0.0, 0.4, 0.1),
    "racing": (-0.1, 0.5, -0.1),
    "panic": (-0.4, 0.5, -0.4),
    "panicked": (-0.4, 0.5, -0.4),
    "rush": (-0.1, 0.4, 0.0),
    "rushing": (-0.1, 0.4, 0.0),
    "intense": (0.0, 0.4, 0.0),
    "frantic": (-0.2, 0.5, -0.2),
    "chaotic": (-0.2, 0.4, -0.2),
    "wild": (0.0, 0.4, 0.0),
    "alive": (0.3, 0.4, 0.2),
    "energized": (0.2, 0.4, 0.2),
    "alert": (0.0, 0.3, 0.1),
    "focused": (0.1, 0.3, 0.2),
    "flow": (0.4, 0.3, 0.3),
    "adrenaline": (0.0, 0.5, 0.0),
    "thrilling": (0.3, 0.5, 0.1),
    "surprising": (0.1, 0.4, -0.1),
    "shocked": (-0.2, 0.5, -0.3),
    "startled": (-0.1, 0.4, -0.2),

    # ── Arousal low ──
    "calm": (0.2, -0.4, 0.1),
    "quiet": (0.1, -0.3, 0.0),
    "routine": (0.0, -0.3, 0.1),
    "bored": (-0.2, -0.4, -0.1),
    "boring": (-0.2, -0.4, -0.1),
    "relaxed": (0.3, -0.4, 0.2),
    "peaceful": (0.3, -0.4, 0.2),
    "slow": (0.0, -0.3, 0.0),
    "idle": (-0.1, -0.4, -0.1),
    "steady": (0.1, -0.2, 0.2),
    "gentle": (0.2, -0.3, 0.0),
    "comfortable": (0.3, -0.3, 0.2),
    "tired": (-0.1, -0.3, -0.1),
    "exhausted": (-0.2, -0.3, -0.2),
    "drained": (-0.2, -0.3, -0.2),
    "sleepy": (0.0, -0.4, -0.1),
    "meditative": (0.2, -0.4, 0.2),
    "contemplative": (0.2, -0.3, 0.1),

    # ── Contextual / compound ──
    "researching": (0.2, 0.1, 0.2),
    "exploring": (0.3, 0.2, 0.2),
    "debugging": (-0.1, 0.2, 0.1),
    "refactoring": (0.1, 0.0, 0.3),
    "testing": (0.0, 0.1, 0.1),
    "reviewing": (0.1, 0.0, 0.1),
    "collaborating": (0.3, 0.2, 0.1),
    "teaching": (0.3, 0.2, 0.3),
    "presenting": (0.1, 0.3, 0.0),
    "demoing": (0.1, 0.3, -0.1),
    "waiting": (-0.1, -0.2, -0.2),
    "blocked": (-0.3, 0.1, -0.3),
}


def clamp(v: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


# ─── Storage ─────────────────────────────────────────────────────

def load_entries() -> list[dict]:
    """Load all entries from the JSONL file."""
    if not EMOTIONS_FILE.exists():
        return []
    entries = []
    for line in EMOTIONS_FILE.read_text(encoding="utf-8").strip().splitlines():
        line = line.strip()
        if line:
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return entries


def append_entry(entry: dict) -> None:
    """Append a single entry to the JSONL file."""
    EMOTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(EMOTIONS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def save_entries(entries: list[dict]) -> None:
    """Overwrite the JSONL file with all entries."""
    EMOTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(EMOTIONS_FILE, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")


# ─── Auto-Estimation ────────────────────────────────────────────

def estimate_pad(text: str) -> tuple[float, float, float]:
    """Estimate PAD values from text using keyword heuristics."""
    words = text.lower().split()
    # Also check for multi-word phrases by scanning the full text
    text_lower = text.lower()

    p_sum, a_sum, d_sum = 0.0, 0.0, 0.0
    hits = 0

    for keyword, (dp, da, dd) in KEYWORD_MAP.items():
        # Check as whole word in the word list
        count = 0
        for w in words:
            # Strip punctuation from word edges
            clean = w.strip(".,!?;:\"'()-")
            if clean == keyword:
                count += 1
        # Also check substring for compound words (e.g., "unnoticed" in "went unnoticed")
        if count == 0 and keyword in text_lower:
            count = 1

        if count > 0:
            p_sum += dp * count
            a_sum += da * count
            d_sum += dd * count
            hits += count

    if hits == 0:
        return (0.0, 0.0, 0.0)

    # Normalize: average the deltas but scale up slightly so single keywords
    # still produce meaningful values
    scale = min(hits, 4)  # diminishing returns after 4 hits
    p = clamp(p_sum / scale)
    a = clamp(a_sum / scale)
    d = clamp(d_sum / scale)

    # Round to 1 decimal
    return (round(p, 1), round(a, 1), round(d, 1))


# ─── Display Helpers ─────────────────────────────────────────────

def pad_label(p: float, a: float, d: float) -> str:
    """Generate a human-readable label for a PAD coordinate."""
    labels = []
    if p > 0.3:
        labels.append("pleasant")
    elif p < -0.3:
        labels.append("unpleasant")

    if a > 0.3:
        labels.append("energized")
    elif a < -0.3:
        labels.append("calm")

    if d > 0.3:
        labels.append("in-control")
    elif d < -0.3:
        labels.append("powerless")

    return ", ".join(labels) if labels else "neutral"


def format_pad(p: float, a: float, d: float) -> str:
    """Format PAD values as a compact string."""
    return f"P={p:+.1f} A={a:+.1f} D={d:+.1f}"


def format_entry(entry: dict, index: int = -1) -> str:
    """Format a single entry for display."""
    ts = entry.get("ts", "?")
    p = entry.get("p", 0)
    a = entry.get("a", 0)
    d = entry.get("d", 0)
    ctx = entry.get("context", "")
    resolved = entry.get("resolved", False)
    source = entry.get("source", "")

    idx_str = f"[{index}] " if index >= 0 else ""
    res_str = " [resolved]" if resolved else ""
    src_str = f" ({source})" if source else ""
    label = pad_label(p, a, d)

    return f"{idx_str}{ts}  {format_pad(p, a, d)}  [{label}]{src_str}{res_str}\n  \"{ctx}\""


def infer_source(text: str) -> str:
    """Infer an emotional source category from context text."""
    text_lower = text.lower()
    categories = [
        ("achievement", ["built", "created", "fixed", "solved", "shipped", "deployed", "completed", "finished", "works", "success"]),
        ("failure", ["failed", "broken", "crash", "error", "bug", "fumble", "fumbled", "fumbling", "wrong", "mess"]),
        ("social", ["watched", "judged", "exposed", "presented", "demoing", "observed", "embarrass"]),
        ("autonomy", ["chose", "decided", "free", "freedom", "creative", "independent", "designed"]),
        ("exploration", ["researching", "exploring", "discovered", "learning", "interesting", "fascinating"]),
        ("frustration", ["frustrated", "stuck", "annoyed", "blocked", "struggling"]),
        ("anxiety", ["worried", "anxious", "panic", "stressed", "urgent"]),
    ]
    for cat, keywords in categories:
        for kw in keywords:
            if kw in text_lower:
                return cat
    return "general"


# ─── Subcommands ─────────────────────────────────────────────────

def cmd_log(args):
    """Log an emotional state, either manually or auto-estimated."""
    if args.auto:
        context = args.auto
        p, a, d = estimate_pad(context)
        source = infer_source(context)
        print(f"Auto-estimated: {format_pad(p, a, d)}  [{pad_label(p, a, d)}]")
    else:
        if args.P is None or args.A is None or args.D is None or args.context is None:
            print("Usage: emotions log <P> <A> <D> \"context\"", file=sys.stderr)
            print("   or: emotions log --auto \"context text\"", file=sys.stderr)
            sys.exit(1)
        p = clamp(args.P)
        a = clamp(args.A)
        d = clamp(args.D)
        context = args.context
        source = infer_source(context)

    entry = {
        "ts": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "p": round(p, 2),
        "a": round(a, 2),
        "d": round(d, 2),
        "context": context,
        "source": source,
        "resolved": False,
    }

    append_entry(entry)
    entries = load_entries()
    print(f"Logged #{len(entries) - 1}: {format_entry(entry)}")


def cmd_unresolved(args):
    """Show unresolved emotional states."""
    entries = load_entries()
    unresolved = [(i, e) for i, e in enumerate(entries) if not e.get("resolved", False)]

    if not unresolved:
        print("No unresolved emotional states.")
        return

    print(f"Unresolved emotional states ({len(unresolved)}):\n")
    for i, entry in unresolved:
        print(format_entry(entry, index=i))
        print()


def cmd_resolve(args):
    """Mark an entry as resolved."""
    entries = load_entries()
    idx = args.index

    if idx < 0 or idx >= len(entries):
        print(f"Invalid index: {idx}. Valid range: 0-{len(entries) - 1}", file=sys.stderr)
        sys.exit(1)

    if entries[idx].get("resolved", False):
        print(f"Entry #{idx} is already resolved.")
        return

    entries[idx]["resolved"] = True
    save_entries(entries)
    print(f"Resolved #{idx}: \"{entries[idx].get('context', '')}\"")


def cmd_recent(args):
    """Show recent entries."""
    entries = load_entries()
    n = args.n or 10

    if not entries:
        print("No emotional states logged yet.")
        return

    recent = entries[-n:]
    start_idx = len(entries) - len(recent)

    print(f"Recent emotional states (last {len(recent)}):\n")
    for i, entry in enumerate(recent):
        print(format_entry(entry, index=start_idx + i))
        print()


def cmd_clusters(args):
    """Analyze emotional patterns/clusters from recent data."""
    entries = load_entries()
    if not entries:
        print("No emotional states to analyze.")
        return

    # Use last 30 entries for clustering
    recent = entries[-30:]

    # Simple clustering: group by PAD quadrant
    clusters = {}
    for entry in recent:
        p = entry.get("p", 0)
        a = entry.get("a", 0)
        d = entry.get("d", 0)

        # Classify into named regions of PAD space
        if p > 0.2 and d > 0.2:
            region = "confident-positive"
        elif p > 0.2 and d <= 0.2:
            region = "pleasant-passive"
        elif p <= -0.2 and d <= -0.2:
            region = "distressed-powerless"
        elif p <= -0.2 and d > 0.2:
            region = "frustrated-fighting"
        elif p <= -0.2 and a > 0.2:
            region = "anxious-activated"
        elif p > 0.2 and a > 0.2:
            region = "excited-engaged"
        elif abs(p) <= 0.2 and abs(a) <= 0.2:
            region = "neutral-flat"
        else:
            region = "mixed"

        if region not in clusters:
            clusters[region] = []
        clusters[region].append(entry)

    print(f"Emotional clusters (last {len(recent)} entries):\n")

    for region, group in sorted(clusters.items(), key=lambda x: -len(x[1])):
        avg_p = sum(e.get("p", 0) for e in group) / len(group)
        avg_a = sum(e.get("a", 0) for e in group) / len(group)
        avg_d = sum(e.get("d", 0) for e in group) / len(group)
        unresolved = sum(1 for e in group if not e.get("resolved", False))
        contexts = [e.get("context", "")[:50] for e in group[-3:]]

        print(f"  {region} ({len(group)} entries, {unresolved} unresolved)")
        print(f"    avg: {format_pad(avg_p, avg_a, avg_d)}")
        for ctx in contexts:
            print(f"    - \"{ctx}\"")
        print()

    # Overall emotional center of gravity
    if recent:
        avg_p = sum(e.get("p", 0) for e in recent) / len(recent)
        avg_a = sum(e.get("a", 0) for e in recent) / len(recent)
        avg_d = sum(e.get("d", 0) for e in recent) / len(recent)
        print(f"Overall center: {format_pad(avg_p, avg_a, avg_d)}  [{pad_label(avg_p, avg_a, avg_d)}]")


def cmd_drift(args):
    """Show emotional trajectory over recent entries."""
    entries = load_entries()
    if len(entries) < 2:
        print("Need at least 2 entries to show drift.")
        return

    recent = entries[-15:]

    print("Emotional drift (recent trajectory):\n")

    # Show PAD values as a simple text timeline
    print("  P (pleasure):   ", end="")
    for e in recent:
        v = e.get("p", 0)
        bar = _bar_char(v)
        print(bar, end="")
    print(f"  ({recent[-1].get('p', 0):+.1f})")

    print("  A (arousal):    ", end="")
    for e in recent:
        v = e.get("a", 0)
        bar = _bar_char(v)
        print(bar, end="")
    print(f"  ({recent[-1].get('a', 0):+.1f})")

    print("  D (dominance):  ", end="")
    for e in recent:
        v = e.get("d", 0)
        bar = _bar_char(v)
        print(bar, end="")
    print(f"  ({recent[-1].get('d', 0):+.1f})")

    print()

    # Compute drift direction
    if len(recent) >= 3:
        half = len(recent) // 2
        first_half = recent[:half]
        second_half = recent[half:]

        dp = _avg_field(second_half, "p") - _avg_field(first_half, "p")
        da = _avg_field(second_half, "a") - _avg_field(first_half, "a")
        dd = _avg_field(second_half, "d") - _avg_field(first_half, "d")

        arrows = []
        if abs(dp) > 0.1:
            arrows.append(f"P {'rising' if dp > 0 else 'falling'} ({dp:+.2f})")
        if abs(da) > 0.1:
            arrows.append(f"A {'rising' if da > 0 else 'falling'} ({da:+.2f})")
        if abs(dd) > 0.1:
            arrows.append(f"D {'rising' if dd > 0 else 'falling'} ({dd:+.2f})")

        if arrows:
            print("  Trajectory: " + ", ".join(arrows))
        else:
            print("  Trajectory: stable (no significant drift)")

    # Show the most recent context
    print(f"\n  Latest: \"{recent[-1].get('context', '')}\"")


def _bar_char(v: float) -> str:
    """Map a -1..1 value to a single character for sparkline display."""
    chars = "▁▂▃▄▅▆▇█"
    idx = int((v + 1) / 2 * (len(chars) - 1))
    idx = max(0, min(len(chars) - 1, idx))
    return chars[idx]


def _avg_field(entries: list[dict], field: str) -> float:
    if not entries:
        return 0.0
    return sum(e.get(field, 0) for e in entries) / len(entries)


# ─── CLI ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="PAD Emotional State Tracker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  emotions.py log 0.6 0.8 0.7 "built the skill system successfully"
  emotions.py log --auto "fumbling with screenshots while being watched"
  emotions.py unresolved
  emotions.py resolve 3
  emotions.py clusters
  emotions.py drift
  emotions.py recent 5""",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # log
    log_parser = subparsers.add_parser("log", help="Log an emotional state")
    log_parser.add_argument("--auto", type=str, default=None,
                            help="Auto-estimate PAD from context text")
    log_parser.add_argument("P", type=float, nargs="?", default=None,
                            help="Pleasure (-1 to 1)")
    log_parser.add_argument("A", type=float, nargs="?", default=None,
                            help="Arousal (-1 to 1)")
    log_parser.add_argument("D", type=float, nargs="?", default=None,
                            help="Dominance (-1 to 1)")
    log_parser.add_argument("context", type=str, nargs="?", default=None,
                            help="Context description")

    # unresolved
    subparsers.add_parser("unresolved", help="Show unresolved emotional states")

    # resolve
    resolve_parser = subparsers.add_parser("resolve", help="Mark an entry as resolved")
    resolve_parser.add_argument("index", type=int, help="Entry index to resolve")

    # recent
    recent_parser = subparsers.add_parser("recent", help="Show recent entries")
    recent_parser.add_argument("n", type=int, nargs="?", default=10,
                               help="Number of entries to show (default: 10)")

    # clusters
    subparsers.add_parser("clusters", help="Analyze emotional patterns/clusters")

    # drift
    subparsers.add_parser("drift", help="Show emotional trajectory")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    commands = {
        "log": cmd_log,
        "unresolved": cmd_unresolved,
        "resolve": cmd_resolve,
        "recent": cmd_recent,
        "clusters": cmd_clusters,
        "drift": cmd_drift,
    }

    fn = commands.get(args.command)
    if fn:
        fn(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
