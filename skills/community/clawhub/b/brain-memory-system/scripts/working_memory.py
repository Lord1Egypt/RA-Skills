#!/usr/bin/env python3
"""
brain wm — Working Memory (Prefrontal Cortex)

Syncs SESSION-STATE.md ↔ working_memory table with TTL/expiry.
Capacity-limited (~7 slots, like human working memory).

Usage:
  brain wm show                     Show current working memory slots
  brain wm add "content" --type goal|context|task|note [--ttl 4h] [--priority 5]
  brain wm clear [--expired]        Clear all or just expired slots
  brain wm load                     Load from SESSION-STATE.md into working memory
  brain wm dump                     Dump working memory back to SESSION-STATE.md
  brain wm sync                     Bidirectional sync (load + merge + dump)
"""

import json
import os
import re
import sqlite3
import sys
from datetime import datetime, timedelta, timezone

BRAIN_DB = os.environ.get("BRAIN_DB", os.path.join(os.path.dirname(__file__), "brain.db"))
BRAIN_AGENT = os.environ.get("BRAIN_AGENT", "margot")
SESSION_STATE = os.environ.get("SESSION_STATE", os.path.join(os.path.dirname(__file__), "..", "..", "SESSION-STATE.md"))
MAX_SLOTS = 12  # Capacity limit (slightly above Miller's 7±2)

# TTL parsing
TTL_PATTERN = re.compile(r'^(\d+)(m|h|d)$')
TTL_MULTIPLIERS = {'m': 60, 'h': 3600, 'd': 86400}


def parse_ttl(ttl_str):
    """Parse TTL string like '4h', '30m', '2d' into seconds."""
    if not ttl_str:
        return 4 * 3600  # Default: 4 hours
    m = TTL_PATTERN.match(ttl_str)
    if not m:
        return int(ttl_str)  # Assume raw seconds
    return int(m.group(1)) * TTL_MULTIPLIERS[m.group(2)]


def get_db():
    conn = sqlite3.connect(BRAIN_DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def cmd_show(json_out=False):
    """Show current working memory slots."""
    db = get_db()
    
    # Expire old slots first
    db.execute(
        "DELETE FROM working_memory WHERE expires_at IS NOT NULL AND expires_at < datetime('now') AND agent = ?",
        (BRAIN_AGENT,)
    )
    db.commit()
    
    rows = db.execute(
        """SELECT id, slot_type, content, priority, expires_at, created_at
           FROM working_memory WHERE agent = ?
           ORDER BY priority DESC, created_at DESC""",
        (BRAIN_AGENT,)
    ).fetchall()
    db.close()
    
    if json_out:
        print(json.dumps([dict(r) for r in rows], indent=2))
        return
    
    if not rows:
        print("Working memory is empty")
        return
    
    print(f"🧠 WORKING MEMORY ({len(rows)}/{MAX_SLOTS} slots) — {BRAIN_AGENT}")
    print(f"{'ID':>4} {'TYPE':<8} {'PRI':>3} {'EXPIRES':<20} CONTENT")
    print("─" * 80)
    for r in rows:
        exp = r["expires_at"][:16] if r["expires_at"] else "never"
        content = r["content"][:50].replace("\n", " ")
        print(f"{r['id']:>4} {r['slot_type']:<8} {r['priority']:>3} {exp:<20} {content}")


def cmd_add(content, slot_type="note", priority=5, ttl_str="4h"):
    """Add a slot to working memory."""
    db = get_db()
    
    # Expire old slots
    db.execute(
        "DELETE FROM working_memory WHERE expires_at IS NOT NULL AND expires_at < datetime('now') AND agent = ?",
        (BRAIN_AGENT,)
    )
    
    # Check capacity
    current = db.execute(
        "SELECT COUNT(*) as c FROM working_memory WHERE agent = ?", (BRAIN_AGENT,)
    ).fetchone()["c"]
    
    if current >= MAX_SLOTS:
        # Evict lowest priority, oldest slot — but show what's being evicted
        evicted = db.execute(
            """SELECT id, slot_type, content, priority FROM working_memory WHERE agent = ?
               ORDER BY priority ASC, created_at ASC LIMIT 1""",
            (BRAIN_AGENT,)
        ).fetchone()
        if evicted:
            db.execute("DELETE FROM working_memory WHERE id = ?", (evicted["id"],))
            print(f"⚠️ Evicted [{evicted['slot_type']}/pri:{evicted['priority']}]: {evicted['content'][:60]}")
    
    ttl_seconds = parse_ttl(ttl_str)
    expires_at = (datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds)).strftime("%Y-%m-%d %H:%M:%S")
    
    db.execute(
        """INSERT INTO working_memory (agent, slot_type, content, priority, expires_at)
           VALUES (?, ?, ?, ?, ?)""",
        (BRAIN_AGENT, slot_type, content, priority, expires_at)
    )
    db.commit()
    
    slot_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    db.close()
    
    ttl_human = f"{ttl_seconds // 3600}h" if ttl_seconds >= 3600 else f"{ttl_seconds // 60}m"
    print(f"✅ Slot #{slot_id}: [{slot_type}] {content[:60]} (TTL: {ttl_human}, priority: {priority})")


def cmd_clear(expired_only=False):
    """Clear working memory slots."""
    db = get_db()
    
    if expired_only:
        result = db.execute(
            "DELETE FROM working_memory WHERE expires_at IS NOT NULL AND expires_at < datetime('now') AND agent = ?",
            (BRAIN_AGENT,)
        )
        print(f"🗑️ Cleared {result.rowcount} expired slots")
    else:
        result = db.execute("DELETE FROM working_memory WHERE agent = ?", (BRAIN_AGENT,))
        print(f"🗑️ Cleared all {result.rowcount} working memory slots")
    
    db.commit()
    db.close()


def cmd_load():
    """Parse SESSION-STATE.md and load into working memory."""
    if not os.path.exists(SESSION_STATE):
        print(f"❌ SESSION-STATE.md not found at {SESSION_STATE}")
        return
    
    with open(SESSION_STATE) as f:
        content = f.read()
    
    db = get_db()
    loaded = 0
    
    # Parse sections
    sections = {
        "Active Context": "context",
        "Open Agenda": "task",
        "Hot State": "context",
        "Key Lessons": "note",
    }
    
    current_section = None
    for line in content.split("\n"):
        line = line.strip()
        
        # Detect section headers
        for header, slot_type in sections.items():
            if header in line and line.startswith("#"):
                current_section = (header, slot_type)
                break
        
        # Parse bullet items under sections (flexible: -, *, •, 1., 2), - [ ], etc.)
        if current_section and re.match(r'^[\-\*\•]\s+|^\d+[\.\)]\s+|^- \[[ x]\]\s+', line):
            item = re.sub(r'^[\-\*\•\d\.\)\[\] x]+\s*', '', line).strip()
            if not item or len(item) < 5:
                continue
            
            # Strip markdown bold
            item = item.replace("**", "")
            
            header, slot_type = current_section
            priority = 7 if slot_type == "context" else 5 if slot_type == "task" else 3
            
            # Check for duplicates
            existing = db.execute(
                "SELECT id FROM working_memory WHERE agent = ? AND content = ?",
                (BRAIN_AGENT, item)
            ).fetchone()
            
            if not existing:
                # 8h TTL for loaded state (will be refreshed on next sync)
                expires = (datetime.now(timezone.utc) + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
                db.execute(
                    "INSERT INTO working_memory (agent, slot_type, content, priority, expires_at) VALUES (?, ?, ?, ?, ?)",
                    (BRAIN_AGENT, slot_type, item, priority, expires)
                )
                loaded += 1
    
    db.commit()
    
    # Enforce capacity — evict lowest priority if over limit
    total = db.execute("SELECT COUNT(*) as c FROM working_memory WHERE agent = ?", (BRAIN_AGENT,)).fetchone()["c"]
    evicted = 0
    while total > MAX_SLOTS:
        db.execute(
            """DELETE FROM working_memory WHERE id = (
                SELECT id FROM working_memory WHERE agent = ?
                ORDER BY priority ASC, created_at ASC LIMIT 1
            )""", (BRAIN_AGENT,)
        )
        total -= 1
        evicted += 1
    if evicted:
        db.commit()
    
    db.close()
    print(f"✅ Loaded {loaded} items from SESSION-STATE.md into working memory" + 
          (f" ({evicted} evicted to fit {MAX_SLOTS}-slot cap)" if evicted else ""))


def cmd_dump():
    """Write working memory back to SESSION-STATE.md."""
    db = get_db()
    
    # Expire first
    db.execute(
        "DELETE FROM working_memory WHERE expires_at IS NOT NULL AND expires_at < datetime('now') AND agent = ?",
        (BRAIN_AGENT,)
    )
    db.commit()
    
    rows = db.execute(
        """SELECT slot_type, content, priority FROM working_memory 
           WHERE agent = ? ORDER BY priority DESC, created_at DESC""",
        (BRAIN_AGENT,)
    ).fetchall()
    db.close()
    
    if not rows:
        print("Working memory is empty — nothing to dump")
        return
    
    # Group by type
    grouped = {}
    for r in rows:
        t = r["slot_type"]
        if t not in grouped:
            grouped[t] = []
        grouped[t].append(r["content"])
    
    # Build SESSION-STATE.md
    now = datetime.now().strftime("%Y-%m-%d %I:%M %p EDT")
    lines = [
        "# SESSION-STATE.md",
        f"> Last updated: {now}",
        "",
    ]
    
    type_headers = {
        "context": "## Active Context",
        "goal": "## Goals",
        "task": "## Open Agenda",
        "note": "## Key Lessons (Recent)",
    }
    
    for slot_type, header in type_headers.items():
        items = grouped.get(slot_type, [])
        if items:
            lines.append(header)
            for i, item in enumerate(items, 1):
                if slot_type == "task":
                    lines.append(f"{i}. {item}")
                else:
                    lines.append(f"- {item}")
            lines.append("")
    
    output = "\n".join(lines)
    
    with open(SESSION_STATE, "w") as f:
        f.write(output)
    
    print(f"✅ Dumped {len(rows)} working memory slots to SESSION-STATE.md")


def cmd_sync():
    """Bidirectional sync: load from SESSION-STATE, merge, dump back."""
    print("🔄 Syncing working memory ↔ SESSION-STATE.md...")
    cmd_load()
    cmd_dump()


def main():
    if len(sys.argv) < 2:
        print("Usage: brain wm <show|add|clear|load|dump|sync> [args]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "show":
        json_out = "--json" in sys.argv
        cmd_show(json_out=json_out)
    
    elif cmd == "add":
        if len(sys.argv) < 3:
            print('Usage: brain wm add "content" [--type goal|context|task|note] [--ttl 4h] [--priority 5]')
            sys.exit(1)
        
        content = sys.argv[2]
        slot_type = "note"
        priority = 5
        ttl = "4h"
        
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--type":
                slot_type = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--priority":
                priority = int(sys.argv[i + 1])
                i += 2
            elif sys.argv[i] == "--ttl":
                ttl = sys.argv[i + 1]
                i += 2
            else:
                i += 1
        
        cmd_add(content, slot_type, priority, ttl)
    
    elif cmd == "clear":
        expired_only = "--expired" in sys.argv
        cmd_clear(expired_only)
    
    elif cmd == "load":
        cmd_load()
    
    elif cmd == "dump":
        cmd_dump()
    
    elif cmd == "sync":
        cmd_sync()
    
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
