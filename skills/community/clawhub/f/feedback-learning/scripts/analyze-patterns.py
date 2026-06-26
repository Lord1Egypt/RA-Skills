#!/usr/bin/env python3
"""
analyze-patterns.py — Nightly batch analysis of events.jsonl
Groups similar events, tracks frequency, updates patterns.json
Promotes rules that hit threshold (3 in 30 days) → genes.json

Run via cron daily at 3:30 AM.
"""
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from difflib import SequenceMatcher

LEARNING_DIR = os.path.expanduser("~/.openclaw/shared/learning")
EVENTS_FILE = os.path.join(LEARNING_DIR, "events.jsonl")
PATTERNS_FILE = os.path.join(LEARNING_DIR, "patterns.json")
GENES_FILE = os.path.join(LEARNING_DIR, "genes.json")

PROMOTION_THRESHOLD = 3  # occurrences
PROMOTION_WINDOW_DAYS = 30
SIMILARITY_THRESHOLD = 0.6  # for grouping similar events


def load_events(since_days=30):
    """Load events from the last N days."""
    events = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=since_days)
    
    if not os.path.exists(EVENTS_FILE) or os.path.getsize(EVENTS_FILE) == 0:
        return events
    
    with open(EVENTS_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
                ts = datetime.fromisoformat(ev["ts"].replace("Z", "+00:00"))
                if ts >= cutoff:
                    events.append(ev)
            except (json.JSONDecodeError, KeyError):
                continue
    return events


def load_json(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def similar(a, b):
    """Check if two strings are similar enough to group."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() >= SIMILARITY_THRESHOLD


def group_events(events):
    """Group similar events by signal text."""
    groups = []
    
    for ev in events:
        if ev.get("type") == "positive":
            continue  # skip positive feedback for pattern analysis
        
        signal = ev.get("signal", "")
        hint = ev.get("hint", "")
        key_text = hint if hint else signal
        
        if not key_text:
            continue
        
        # Try to find existing group
        matched = False
        for group in groups:
            if similar(key_text, group["key_text"]):
                group["events"].append(ev)
                group["count"] += 1
                group["agents"].add(ev.get("agent", "unknown"))
                matched = True
                break
        
        if not matched:
            groups.append({
                "key_text": key_text,
                "events": [ev],
                "count": 1,
                "agents": {ev.get("agent", "unknown")},
                "type": ev.get("type", "error"),
                "source": ev.get("source", "unknown"),
            })
    
    return groups


def update_patterns(groups):
    """Update patterns.json with current group data."""
    patterns_data = load_json(PATTERNS_FILE) or {"version": "2.0", "patterns": []}
    
    new_patterns = []
    for group in groups:
        new_patterns.append({
            "key": group["key_text"][:100],
            "count": group["count"],
            "type": group["type"],
            "source": group["source"],
            "agents": sorted(group["agents"]),
            "first_seen": group["events"][0].get("ts", ""),
            "last_seen": group["events"][-1].get("ts", ""),
            "promoted": False,
        })
    
    patterns_data["patterns"] = sorted(new_patterns, key=lambda x: -x["count"])
    patterns_data["updated"] = datetime.now(timezone.utc).isoformat()
    save_json(PATTERNS_FILE, patterns_data)
    
    return new_patterns


def promote_rules(patterns):
    """Promote patterns that hit threshold to genes.json."""
    genes_data = load_json(GENES_FILE) or {"version": "2.0", "rules": []}
    existing_keys = {r.get("origin", "") for r in genes_data.get("rules", [])}
    
    promoted = []
    for p in patterns:
        if p["count"] >= PROMOTION_THRESHOLD and p["key"] not in existing_keys:
            rule = {
                "id": f"gene_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{len(promoted)}",
                "origin": p["key"],
                "type": p["type"],
                "agents": p["agents"],
                "occurrences": p["count"],
                "promoted_at": datetime.now(timezone.utc).isoformat(),
                "rule": f"AVOID: {p['key']}",  # Will be refined by LLM in cron
                "expires": None,
                "active": True,
            }
            genes_data["rules"].append(rule)
            promoted.append(rule)
    
    if promoted:
        genes_data["updated"] = datetime.now(timezone.utc).isoformat()
        save_json(GENES_FILE, genes_data)
    
    return promoted


def main():
    print(f"[{datetime.now().isoformat()}] Analyzing learning events...")
    
    events = load_events(since_days=PROMOTION_WINDOW_DAYS)
    print(f"  Events in last {PROMOTION_WINDOW_DAYS} days: {len(events)}")
    
    if not events:
        print("  No events to analyze. Done.")
        return
    
    # Count by type
    by_type = defaultdict(int)
    for ev in events:
        by_type[ev.get("type", "unknown")] += 1
    print(f"  By type: {dict(by_type)}")
    
    # Group similar events
    groups = group_events(events)
    print(f"  Unique patterns: {len(groups)}")
    
    # Update patterns.json
    patterns = update_patterns(groups)
    
    # Check for promotions
    promoted = promote_rules(patterns)
    if promoted:
        print(f"  🎯 PROMOTED {len(promoted)} rules to genes.json!")
        for r in promoted:
            print(f"    - {r['origin'][:60]} ({r['occurrences']}x)")
    else:
        ready = [p for p in patterns if p["count"] >= PROMOTION_THRESHOLD - 1]
        if ready:
            print(f"  ⏳ {len(ready)} patterns approaching threshold")
    
    print("  Done.")


if __name__ == "__main__":
    main()
