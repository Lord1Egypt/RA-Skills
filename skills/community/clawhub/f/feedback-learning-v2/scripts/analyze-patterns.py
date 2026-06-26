#!/usr/bin/env python3
"""
analyze-patterns.py v2 — Nightly batch analysis of events.jsonl
NEW in v2:
  - Tracks BOTH positive AND negative patterns
  - Structured gene promotion (condition → action → context)
  - Behavioral Delta Test (promotes only if rule changes future decisions)
  - Stagnation detection (gene exists but pattern keeps recurring → stale)
  - Gene expiry (90 days inactivity)
  - Configurable via $FEEDBACK_LEARNING_DIR

Run via cron: 30 3 * * * python3 ~/.openclaw/shared/learning/analyze-patterns.py
"""
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from difflib import SequenceMatcher

DIR = os.environ.get("FEEDBACK_LEARNING_DIR",
                     os.path.expanduser("~/.openclaw/shared/learning"))
EVENTS_FILE = os.path.join(DIR, "events.jsonl")
PATTERNS_FILE = os.path.join(DIR, "patterns.json")
GENES_FILE = os.path.join(DIR, "genes.json")

PROMOTION_THRESHOLD = 3
PROMOTION_WINDOW_DAYS = 30
SIMILARITY_THRESHOLD = 0.60
GENE_EXPIRY_DAYS = 90  # inactivity → auto-expire


def load_events(since_days=30):
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
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() >= SIMILARITY_THRESHOLD


def group_events(events, include_positive=False):
    """Group similar events by signal/hint text."""
    groups = []
    for ev in events:
        ev_type = ev.get("type", "")
        if ev_type == "positive" and not include_positive:
            continue  # separate call for positive

        signal = ev.get("signal", "")
        hint = ev.get("hint", "")
        key_text = hint if hint else signal
        if not key_text:
            continue

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
                "signal_text": signal,
                "events": [ev],
                "count": 1,
                "agents": {ev.get("agent", "unknown")},
                "type": ev_type,
                "source": ev.get("source", "unknown"),
            })

    return groups


def behavioral_delta_test(key_text, genes_data):
    """
    Check if promoting this pattern would actually change future behavior.
    Returns True if no existing active gene already covers this pattern.
    """
    existing_rules = genes_data.get("rules", [])
    for rule in existing_rules:
        if not rule.get("active", True):
            continue
        if similar(key_text, rule.get("origin", "")):
            return False  # already covered — no delta
    return True


def make_structured_rule(group):
    """
    Create a structured gene from a pattern group.
    Tries to extract condition/action from hint text; falls back to template.
    """
    hint = group["key_text"]
    signal = group["signal_text"]
    ev_type = group["type"]

    # Try to parse "condition → action" patterns in hint
    if "→" in hint or "->" in hint:
        parts = hint.replace("->", "→").split("→", 1)
        condition = parts[0].strip()
        action = parts[1].strip()
    elif ev_type == "positive":
        condition = f"When doing: {signal}"
        action = f"Continue doing: {hint}"
    else:
        condition = f"When: {signal}"
        action = f"Instead: {hint}"

    return {
        "condition": condition[:200],
        "action": action[:200],
        "context": f"Observed {group['count']}x across agents: {sorted(group['agents'])}",
    }


def update_patterns(neg_groups, pos_groups):
    """Update patterns.json with negative and positive patterns."""
    patterns_data = load_json(PATTERNS_FILE) or {
        "version": "2.1", "patterns": {"negative": [], "positive": []}
    }

    def groups_to_list(groups):
        result = []
        for g in groups:
            result.append({
                "key": g["key_text"][:100],
                "count": g["count"],
                "type": g["type"],
                "source": g["source"],
                "agents": sorted(g["agents"]),
                "first_seen": g["events"][0].get("ts", ""),
                "last_seen": g["events"][-1].get("ts", ""),
            })
        return sorted(result, key=lambda x: -x["count"])

    if "patterns" not in patterns_data or not isinstance(patterns_data["patterns"], dict):
        patterns_data["patterns"] = {"negative": [], "positive": []}

    patterns_data["patterns"]["negative"] = groups_to_list(neg_groups)
    patterns_data["patterns"]["positive"] = groups_to_list(pos_groups)
    patterns_data["updated"] = datetime.now(timezone.utc).isoformat()
    save_json(PATTERNS_FILE, patterns_data)
    return patterns_data["patterns"]


def promote_rules(neg_groups, genes_data):
    """Promote negative patterns that hit threshold and pass delta test."""
    promoted = []
    stagnated = []

    for g in neg_groups:
        if g["count"] < PROMOTION_THRESHOLD:
            continue

        # Check if already promoted
        existing = next(
            (r for r in genes_data.get("rules", [])
             if similar(g["key_text"], r.get("origin", "")) and r.get("active")),
            None
        )

        if existing:
            # Gene exists but pattern still recurring → STAGNATION
            existing["occurrences"] = existing.get("occurrences", 0) + g["count"]
            existing["last_seen"] = g["events"][-1].get("ts", "")
            if existing.get("status") == "active":
                existing["status"] = "stale"
                stagnated.append(existing)
        else:
            # Behavioral delta test
            if not behavioral_delta_test(g["key_text"], genes_data):
                continue

            structured = make_structured_rule(g)
            rule = {
                "id": f"gene_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{len(promoted)}",
                "status": "active",
                "origin": g["key_text"][:100],
                "type": g["type"],
                "agents": sorted(g["agents"]),
                "occurrences": g["count"],
                "condition": structured["condition"],
                "action": structured["action"],
                "context": structured["context"],
                "promoted_at": datetime.now(timezone.utc).isoformat(),
                "last_seen": g["events"][-1].get("ts", ""),
                "expires": None,
                "active": True,
            }
            genes_data.setdefault("rules", []).append(rule)
            promoted.append(rule)

    return promoted, stagnated


def expire_inactive_genes(genes_data):
    """Mark genes with no recent events as expired."""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=GENE_EXPIRY_DAYS)).isoformat()
    expired = []
    for rule in genes_data.get("rules", []):
        if not rule.get("active"):
            continue
        last_seen = rule.get("last_seen", rule.get("promoted_at", ""))
        if last_seen and last_seen < cutoff:
            rule["active"] = False
            rule["status"] = "expired"
            rule["expires"] = datetime.now(timezone.utc).isoformat()
            expired.append(rule)
    return expired


def main():
    print(f"[{datetime.now().isoformat()}] analyze-patterns v2 running...")

    events = load_events(since_days=PROMOTION_WINDOW_DAYS)
    print(f"  Events (last {PROMOTION_WINDOW_DAYS}d): {len(events)}")

    if not events:
        print("  No events. Done.")
        return

    by_type = defaultdict(int)
    for ev in events:
        by_type[ev.get("type", "?")] += 1
    print(f"  By type: {dict(by_type)}")

    # Group negative + positive separately
    neg_events = [e for e in events if e.get("type") in ("error", "correction", "requery")]
    pos_events = [e for e in events if e.get("type") == "positive"]

    neg_groups = group_events(neg_events)
    pos_groups = group_events(pos_events, include_positive=True)

    print(f"  Negative patterns: {len(neg_groups)} | Positive patterns: {len(pos_groups)}")

    # Update patterns.json
    update_patterns(neg_groups, pos_groups)

    # Load genes and run promotion
    genes_data = load_json(GENES_FILE) or {"version": "2.1", "rules": []}

    # Expire inactive genes
    expired = expire_inactive_genes(genes_data)
    if expired:
        print(f"  ♻️  Expired {len(expired)} stale gene(s)")

    # Promote new rules
    promoted, stagnated = promote_rules(neg_groups, genes_data)

    if promoted:
        print(f"  🎯 PROMOTED {len(promoted)} new rule(s):")
        for r in promoted:
            print(f"     [{r['id']}] {r['condition'][:60]} → {r['action'][:60]}")
    else:
        approaching = [g for g in neg_groups if g["count"] == PROMOTION_THRESHOLD - 1]
        if approaching:
            print(f"  ⏳ {len(approaching)} pattern(s) approaching threshold")

    if stagnated:
        print(f"  ⚠️  STAGNATION: {len(stagnated)} gene(s) marked stale (rule exists but pattern persists!)")
        for r in stagnated:
            print(f"     [{r['id']}] {r['condition'][:60]}")

    if promoted or stagnated or expired:
        genes_data["updated"] = datetime.now(timezone.utc).isoformat()
        save_json(GENES_FILE, genes_data)

    print("  Done.")


if __name__ == "__main__":
    main()
