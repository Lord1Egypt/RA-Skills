#!/usr/bin/env python3
"""
Brain Consolidation Pipeline — "Sleep Replay"

Mimics hippocampal consolidation during sleep:
1. Score unconsolidated episodes by importance, emotion, novelty, rehearsal
2. High-scoring episodes get facts extracted and stored in semantic memory
3. Mark episodes as consolidated
4. Log all consolidation actions
5. Optionally forget (archive) low-value old episodes

Designed to run as a nightly cron or on-demand via `brain consolidate`.
"""
import sqlite3
import json
import os
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path

BRAIN_DB = os.environ.get("BRAIN_DB", str(Path(__file__).parent / "brain.db"))
DRY_RUN = "--dry-run" in sys.argv
VERBOSE = "--verbose" in sys.argv or "-v" in sys.argv
AGENT = os.environ.get("BRAIN_AGENT", "margot")

# Consolidation thresholds
CONSOLIDATION_SCORE_THRESHOLD = 4.0  # Minimum score to consolidate (importance ~7+ or 5+ with emotion)
FORGET_AGE_DAYS = 90                  # Archive episodes older than this (Nygma: 30 was too aggressive)
FORGET_IMPORTANCE_MAX = 3             # Only forget low-importance episodes
MAX_CONSOLIDATE_PER_RUN = 50          # Don't process too many at once


def score_episode(ep: dict) -> float:
    """
    Score an episode for consolidation priority.
    Mimics amygdala (emotion) + hippocampal (novelty/rehearsal) weighting.
    """
    importance = ep.get("importance", 5) or 5
    novelty = ep.get("novelty", 5) or 5
    rehearsal = ep.get("rehearsal_count", 0) or 0
    
    # Emotional weight
    emotion_score = 0
    intensity = ep.get("emotion_intensity", "")
    if intensity == "high":
        emotion_score = 3
    elif intensity == "medium":
        emotion_score = 2
    elif intensity == "low":
        emotion_score = 1
    elif ep.get("emotion"):  # Has emotion but no intensity
        emotion_score = 1.5
    
    # Weighted score — target range 0-10, threshold 5.0
    # importance=7 + no emotion should be ~5.5 (consolidatable)
    # importance=4 + no emotion should be ~3.5 (skip)
    score = (
        importance * 0.6 +          # Importance (1-10, biggest factor) → 0.6-6.0
        emotion_score * 0.8 +       # Amygdala: emotional weight (0-3) → 0-2.4
        min(rehearsal, 5) * 0.2 +   # Rehearsal (capped at 5) → 0-1.0
        (novelty / 10) * 0.6        # Novelty (1-10) → 0.06-0.6
    )
    
    return round(score, 2)


def extract_facts_from_episode(ep: dict) -> list[dict]:
    """
    Extract factual knowledge from an episode's content.
    Returns list of {entity, key, value} dicts.
    
    This is a rule-based extractor. For production, could use LLM.
    """
    facts = []
    content = ep.get("content", "")
    title = ep.get("title", "")
    
    # Pattern: "Root cause: ..." or "Root cause was ..."
    root_cause = re.search(r'[Rr]oot cause[:\s]+(.+?)(?:\.|$)', content)
    if root_cause:
        facts.append({
            "entity": _extract_entity(title),
            "key": "root_cause",
            "value": root_cause.group(1).strip()[:500]
        })
    
    # Pattern: "Lesson: ..." or "Key lesson: ..."
    lesson = re.search(r'[Ll]esson[:\s]+(.+?)(?:\.|$)', content)
    if lesson:
        facts.append({
            "entity": _extract_entity(title),
            "key": "lesson_learned",
            "value": lesson.group(1).strip()[:500]
        })
    
    # Pattern: "Fix: ..." or "Fixed by ..."
    fix = re.search(r'[Ff]ix(?:ed)?(?:\s+by)?[:\s]+(.+?)(?:\.|$)', content)
    if fix:
        facts.append({
            "entity": _extract_entity(title),
            "key": "fix_applied",
            "value": fix.group(1).strip()[:500]
        })
    
    # Pattern: URLs/IPs
    urls = re.findall(r'https?://\S+', content)
    for url in urls[:3]:  # Cap at 3
        facts.append({
            "entity": _extract_entity(title),
            "key": "related_url",
            "value": url
        })
    
    # Pattern: "Version X.Y.Z" or "vX.Y.Z"
    version = re.search(r'(?:version|v)(\d+\.\d+(?:\.\d+)?)', content, re.I)
    if version:
        facts.append({
            "entity": _extract_entity(title),
            "key": "version",
            "value": version.group(1)
        })
    
    return facts


def _extract_entity(title: str) -> str:
    """Extract a reasonable entity name from episode title."""
    # Remove common prefixes
    title = re.sub(r'^(Nightly Build|Security Audit|Heartbeat|Fleet Alert)[:\s-]*', '', title)
    # Take first meaningful word(s)
    words = title.split()[:3]
    return "_".join(w.strip(":-—()[]") for w in words if w.strip(":-—()[]"))[:50] or "general"


def consolidate(conn: sqlite3.Connection):
    """Main consolidation pipeline."""
    now = datetime.now(tz=None).isoformat()
    
    # 1. Get unconsolidated episodes
    episodes = conn.execute("""
        SELECT id, date, time, title, content, emotion, emotion_intensity,
               importance, novelty, rehearsal_count, agent
        FROM episodes
        WHERE consolidated = 0
        AND agent = ?
        ORDER BY importance DESC, date DESC
        LIMIT ?
    """, (AGENT, MAX_CONSOLIDATE_PER_RUN)).fetchall()
    
    columns = ["id", "date", "time", "title", "content", "emotion", 
               "emotion_intensity", "importance", "novelty", "rehearsal_count", "agent"]
    
    consolidated = 0
    facts_created = 0
    skipped = 0
    archived = 0
    
    print(f"=== CONSOLIDATION RUN ({AGENT}) ===")
    print(f"Unconsolidated episodes: {len(episodes)}")
    print(f"Threshold: {CONSOLIDATION_SCORE_THRESHOLD}")
    print(f"Mode: {'DRY RUN' if DRY_RUN else 'LIVE'}")
    print()
    
    for row in episodes:
        ep = dict(zip(columns, row))
        score = score_episode(ep)
        
        if score < CONSOLIDATION_SCORE_THRESHOLD:
            if VERBOSE:
                print(f"  SKIP [{score:.1f}] {ep['date']} {ep['title'][:50]}")
            skipped += 1
            continue
        
        print(f"  CONSOLIDATE [{score:.1f}] {ep['date']} {ep['title'][:50]}")
        
        # Extract facts
        facts = extract_facts_from_episode(ep)
        for fact in facts:
            if VERBOSE:
                print(f"    → fact: {fact['entity']}.{fact['key']} = {fact['value'][:60]}")
            
            if not DRY_RUN:
                # Upsert — update if exists, insert if new
                existing = conn.execute(
                    "SELECT id, updated_at FROM facts WHERE entity=? AND key=? AND agent=?",
                    (fact["entity"], fact["key"], AGENT)
                ).fetchone()
                
                if existing:
                    # Optimistic locking: only update if fact hasn't been modified
                    # since we read it (prevents overwriting user edits during consolidation)
                    result = conn.execute("""
                        UPDATE facts SET value=?, times_confirmed=times_confirmed+1,
                               last_confirmed=?, updated_at=?
                        WHERE id=? AND updated_at=?
                    """, (fact["value"], now, now, existing["id"], existing["updated_at"]))
                    if result.rowcount == 0:
                        if VERBOSE:
                            print(f"    ⚠️ Conflict: {fact['entity']}.{fact['key']} was modified concurrently — skipping")
                        continue
                else:
                    conn.execute("""
                        INSERT INTO facts (entity, key, value, source_episode_id, agent, created_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (fact["entity"], fact["key"], fact["value"], ep["id"], AGENT, now))
                facts_created += 1
        
        # Mark as consolidated
        if not DRY_RUN:
            conn.execute("""
                UPDATE episodes SET consolidated=1, consolidated_at=? WHERE id=?
            """, (now, ep["id"]))
            
            # Log the consolidation
            conn.execute("""
                INSERT INTO consolidation_log (source_type, source_id, action, destination, reason, agent, occurred_at)
                VALUES ('episode', ?, 'consolidated', 'facts', ?, ?, ?)
            """, (ep["id"], f"score={score:.1f}, {len(facts)} facts extracted", AGENT, now))
        
        consolidated += 1
    
    # 2. Forgetting — archive old low-value episodes
    cutoff = (datetime.now(tz=None) - timedelta(days=FORGET_AGE_DAYS)).strftime("%Y-%m-%d")
    forgettable = conn.execute("""
        SELECT id, date, title, importance FROM episodes
        WHERE date < ? AND importance <= ? AND consolidated = 1 AND agent = ?
    """, (cutoff, FORGET_IMPORTANCE_MAX, AGENT)).fetchall()
    
    if forgettable:
        print(f"\n  FORGETTING: {len(forgettable)} old low-value episodes (>{FORGET_AGE_DAYS} days, importance ≤{FORGET_IMPORTANCE_MAX})")
        for fid, fdate, ftitle, fimp in forgettable:
            if VERBOSE:
                print(f"    → archive: {fdate} {ftitle[:50]} (imp: {fimp})")
            if not DRY_RUN:
                conn.execute("""
                    INSERT INTO consolidation_log (source_type, source_id, action, reason, agent, occurred_at)
                    VALUES ('episode', ?, 'archived', 'low importance + old', ?, ?)
                """, (fid, AGENT, now))
                # Don't delete — just mark. Could add an 'archived' column later.
            archived += 1
    
    if not DRY_RUN:
        conn.commit()
    
    # Summary
    print(f"\n=== CONSOLIDATION SUMMARY ===")
    print(f"  Consolidated: {consolidated}")
    print(f"  Facts created/updated: {facts_created}")
    print(f"  Skipped (below threshold): {skipped}")
    print(f"  Archived (forgotten): {archived}")
    
    # Remaining
    remaining = conn.execute(
        "SELECT COUNT(*) FROM episodes WHERE consolidated=0 AND agent=?", (AGENT,)
    ).fetchone()[0]
    print(f"  Remaining unconsolidated: {remaining}")


def main():
    conn = sqlite3.connect(BRAIN_DB)
    try:
        consolidate(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
