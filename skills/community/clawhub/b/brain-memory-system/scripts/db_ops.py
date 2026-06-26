#!/usr/bin/env python3
"""
brain db_ops — Safe parameterized database operations
Replaces bash SQL string interpolation with Python prepared statements.
Fixes: SQL injection vulnerability (Nygma audit 2026-03-15)
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

BRAIN_DB = os.environ.get("BRAIN_DB", os.path.join(os.path.dirname(__file__), "brain.db"))
BRAIN_AGENT = os.environ.get("BRAIN_AGENT", "margot")


def get_db():
    conn = sqlite3.connect(BRAIN_DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def agent_scope():
    return (BRAIN_AGENT, 'shared')


# ============================================================
# EPISODE OPERATIONS
# ============================================================

def cmd_store(args):
    """Store an episode with parameterized INSERT."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('content')
    parser.add_argument('--title', '-t', default=None)
    parser.add_argument('--emotion', '-e', default=None)
    parser.add_argument('--intensity', '-i', default=None)
    parser.add_argument('--importance', type=int, default=5)
    parser.add_argument('--agent', default=BRAIN_AGENT)
    parser.add_argument('--source', default='manual')
    opts = parser.parse_args(args)

    title = opts.title or opts.content[:80]
    date = datetime.now().strftime("%Y-%m-%d")
    time_val = datetime.now().strftime("%H:%M")

    db = get_db()
    cursor = db.execute(
        """INSERT INTO episodes (date, time, title, content, emotion, emotion_intensity,
           importance, source, agent)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (date, time_val, title, opts.content, opts.emotion, opts.intensity,
         opts.importance, opts.source, opts.agent)
    )
    db.commit()
    ep_id = cursor.lastrowid
    db.close()
    print(f"✅ Stored episode #{ep_id}: {title}")


def cmd_recall(args):
    """Search all memory with parameterized FTS queries."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('query')
    parser.add_argument('--type', dest='search_type', default='all')
    parser.add_argument('--limit', type=int, default=10)
    opts = parser.parse_args(args)

    db = get_db()
    scope = agent_scope()

    # Sanitize FTS query — escape special chars
    safe_query = sanitize_fts(opts.query)

    if opts.search_type in ('all', 'episodic'):
        print("=== EPISODES ===")
        rows = db.execute(
            """SELECT e.date, e.time, e.title, e.importance, e.emotion, e.agent
               FROM episodes e
               JOIN episodes_fts f ON e.id = f.rowid
               WHERE episodes_fts MATCH ?
               AND e.agent IN (?, ?)
               ORDER BY e.importance DESC, e.date DESC
               LIMIT ?""",
            (safe_query, scope[0], scope[1], opts.limit)
        ).fetchall()
        for r in rows:
            print(f"  {r['date']} {r['time'] or ''} [{r['importance']}] {r['title'][:60]}  ({r['agent']})")
        if not rows:
            print("  (no matches)")
        print()

    if opts.search_type in ('all', 'fact'):
        print("=== FACTS ===")
        try:
            rows = db.execute(
                """SELECT f.entity, f.key, f.value, f.agent
                   FROM facts f
                   JOIN facts_fts ff ON f.id = ff.rowid
                   WHERE facts_fts MATCH ?
                   AND f.agent IN (?, ?)
                   LIMIT ?""",
                (safe_query, scope[0], scope[1], opts.limit)
            ).fetchall()
            for r in rows:
                print(f"  {r['entity']}.{r['key']} = {r['value'][:60]}  ({r['agent']})")
            if not rows:
                print("  (no matches)")
        except Exception:
            print("  (no facts or no matches)")
        print()

    if opts.search_type in ('all', 'proc'):
        print("=== PROCEDURES ===")
        try:
            rows = db.execute(
                """SELECT slug, title, version, agent,
                          success_count || '/' || (success_count + failure_count) as success_rate
                   FROM procedures
                   WHERE (title LIKE ? OR slug LIKE ? OR tags LIKE ?)
                   AND agent IN (?, ?)
                   LIMIT ?""",
                (f"%{opts.query}%", f"%{opts.query}%", f"%{opts.query}%",
                 scope[0], scope[1], opts.limit)
            ).fetchall()
            for r in rows:
                print(f"  {r['slug']} v{r['version']} ({r['success_rate']})  {r['title']}  ({r['agent']})")
            if not rows:
                print("  (no matches)")
        except Exception:
            print("  (no procedures or no matches)")

    db.close()


def cmd_episodes(args):
    """Show episodes for a date."""
    date = args[0] if args else datetime.now().strftime("%Y-%m-%d")
    scope = agent_scope()
    db = get_db()
    rows = db.execute(
        """SELECT time, title, importance, emotion, agent 
           FROM episodes WHERE date=? AND agent IN (?, ?)
           ORDER BY time""",
        (date, scope[0], scope[1])
    ).fetchall()
    db.close()

    if not rows:
        print(f"No episodes for {date}")
        return
    print(f"{'TIME':<6} {'IMP':>3} {'EMOTION':<12} {'AGENT':<8} TITLE")
    print("─" * 70)
    for r in rows:
        print(f"{r['time'] or '??:??':<6} {r['importance']:>3} {(r['emotion'] or '')::<12} {r['agent']:<8} {r['title'][:40]}")


def cmd_emotions(args):
    """Show emotional timeline."""
    period = int(args[0]) if args else 7
    scope = agent_scope()
    db = get_db()
    rows = db.execute(
        """SELECT date, time, title, emotion, emotion_intensity, agent
           FROM episodes 
           WHERE emotion IS NOT NULL 
           AND date >= date('now', ?)
           AND agent IN (?, ?)
           ORDER BY date DESC, time DESC""",
        (f"-{period} days", scope[0], scope[1])
    ).fetchall()
    db.close()

    if not rows:
        print(f"No emotional episodes in last {period} days")
        return
    for r in rows:
        intensity = f"/{r['emotion_intensity']}" if r['emotion_intensity'] else ""
        print(f"  {r['date']} {r['time'] or ''} [{r['emotion']}{intensity}] {r['title'][:50]}  ({r['agent']})")


def cmd_important(args):
    """Show high-importance episodes."""
    threshold = int(args[0]) if len(args) > 0 else 8
    days = int(args[1]) if len(args) > 1 else 7
    db = get_db()
    rows = db.execute(
        """SELECT date, title, importance, emotion
           FROM episodes
           WHERE importance >= ?
           AND date >= date('now', ?)
           ORDER BY importance DESC, date DESC""",
        (threshold, f"-{days} days")
    ).fetchall()
    db.close()

    if not rows:
        print(f"No episodes with importance >= {threshold} in last {days} days")
        return
    for r in rows:
        emotion = f" [{r['emotion']}]" if r['emotion'] else ""
        print(f"  {r['date']} [{r['importance']}] {r['title'][:60]}{emotion}")


def cmd_stats():
    """Overview statistics."""
    db = get_db()
    print("=== BRAIN STATS ===")

    total = db.execute("SELECT COUNT(*) FROM episodes").fetchone()[0]
    print(f"Episodes: {total}")

    row = db.execute("SELECT MIN(date) as mn, MAX(date) as mx FROM episodes").fetchone()
    print(f"Date range: {row['mn']} → {row['mx']}")

    emo = db.execute("SELECT COUNT(*) FROM episodes WHERE emotion IS NOT NULL").fetchone()[0]
    print(f"With emotions: {emo}")

    high = db.execute("SELECT COUNT(*) FROM episodes WHERE importance >= 7").fetchone()[0]
    print(f"High importance (≥7): {high}")

    cons = db.execute("SELECT COUNT(*) FROM episodes WHERE consolidated = 1").fetchone()[0]
    print(f"Consolidated: {cons}")

    facts = db.execute("SELECT COUNT(*) FROM facts").fetchone()[0]
    print(f"Facts: {facts}")

    procs = db.execute("SELECT COUNT(*) FROM procedures").fetchone()[0]
    print(f"Procedures: {procs}")

    print("\n=== EMOTION DISTRIBUTION ===")
    rows = db.execute(
        "SELECT emotion, COUNT(*) as count FROM episodes WHERE emotion IS NOT NULL GROUP BY emotion ORDER BY count DESC LIMIT 10"
    ).fetchall()
    for r in rows:
        print(f"  {r['emotion']}: {r['count']}")

    print("\n=== EPISODES PER DAY ===")
    rows = db.execute(
        """SELECT date, COUNT(*) as episodes, ROUND(AVG(importance), 1) as avg_importance
           FROM episodes GROUP BY date ORDER BY date DESC LIMIT 14"""
    ).fetchall()
    for r in rows:
        print(f"  {r['date']}: {r['episodes']} episodes (avg importance: {r['avg_importance']})")

    db.close()


def cmd_who():
    """Show all agents in the brain."""
    db = get_db()
    print("=== AGENTS IN BRAIN ===")
    
    print("\nEpisodes:")
    for r in db.execute("SELECT agent, COUNT(*) as c FROM episodes GROUP BY agent ORDER BY c DESC").fetchall():
        print(f"  {r['agent']}: {r['c']}")
    
    print("\nFacts:")
    for r in db.execute("SELECT agent, COUNT(*) as c FROM facts GROUP BY agent ORDER BY c DESC").fetchall():
        print(f"  {r['agent']}: {r['c']}")

    print("\nProcedures:")
    for r in db.execute("SELECT agent, COUNT(*) as c FROM procedures GROUP BY agent ORDER BY c DESC").fetchall():
        print(f"  {r['agent']}: {r['c']}")

    print(f"\nCurrent agent: {BRAIN_AGENT}")
    print("Scope: own + shared")
    db.close()


# ============================================================
# UTILITIES
# ============================================================

def sanitize_fts(query):
    """Sanitize a query for FTS5 MATCH — escape special characters."""
    # FTS5 special chars: AND OR NOT ( ) * " ^
    # Wrap each word in double quotes to treat as literals
    words = query.split()
    safe_words = []
    for w in words:
        # Remove any existing quotes
        w = w.replace('"', '')
        if w.upper() in ('AND', 'OR', 'NOT'):
            safe_words.append(f'"{w}"')  # Quote reserved words
        elif any(c in w for c in '()*^'):
            safe_words.append(f'"{w}"')  # Quote special chars
        else:
            safe_words.append(w)
    return ' '.join(safe_words)


# ============================================================
# DISPATCH
# ============================================================

COMMANDS = {
    'store': cmd_store,
    'recall': cmd_recall,
    'episodes': cmd_episodes,
    'emotions': cmd_emotions,
    'important': cmd_important,
    'stats': cmd_stats,
    'who': cmd_who,
}

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(f"Usage: db_ops.py <{'|'.join(COMMANDS.keys())}> [args...]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    if cmd in ('store', 'recall'):
        COMMANDS[cmd](args)
    elif cmd in ('episodes', 'emotions', 'important'):
        COMMANDS[cmd](args)
    elif cmd in ('stats', 'who'):
        COMMANDS[cmd]()


if __name__ == "__main__":
    main()
