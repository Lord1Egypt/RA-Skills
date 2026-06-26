#!/usr/bin/env python3
"""
brain facts — Structured fact storage wrapper
Queries the legacy facts.db for backward compatibility.
Future: migrate to brain.db facts table with full schema.
"""

import json
import os
import sqlite3
import sys

FACTS_DB = os.environ.get("BRAIN_FACTS_DB", os.path.join(os.path.dirname(__file__), "..", "facts.db"))


def get_conn():
    if not os.path.exists(FACTS_DB):
        print(f"❌ Facts database not found: {FACTS_DB}", file=sys.stderr)
        sys.exit(1)
    return sqlite3.connect(FACTS_DB)


def cmd_get(entity, key):
    """Get a specific fact value."""
    conn = get_conn()
    cursor = conn.cursor()
    
    # Try exact match first
    cursor.execute(
        "SELECT value, category, confidence, permanent FROM facts WHERE entity = ? AND key = ?",
        (entity, key)
    )
    row = cursor.fetchone()
    
    if row:
        value, category, confidence, permanent = row
        # Track access for decay scoring
        try:
            cursor.execute(
                "UPDATE facts SET access_count = access_count + 1, last_accessed = datetime('now') WHERE entity = ? AND key = ?",
                (entity, key)
            )
            conn.commit()
        except Exception as e:
            print(f"(access tracking failed: {e})", file=sys.stderr)
        conn.close()
        print(value)
        return
    
    # Try case-insensitive fallback
    cursor.execute(
        "SELECT value FROM facts WHERE LOWER(entity) = LOWER(?) AND LOWER(key) = LOWER(?)",
        (entity, key)
    )
    row = cursor.fetchone()
    conn.close()
    
    if row:
        print(row[0])
    else:
        print(f"(not found: {entity}.{key})", file=sys.stderr)
        sys.exit(1)


def cmd_set(entity, key, value, category="general", permanent=False, confidence=1.0):
    """Set a fact (upsert)."""
    conn = get_conn()
    cursor = conn.cursor()
    
    perm = 1 if permanent else 0
    
    cursor.execute(
        """INSERT INTO facts (entity, key, value, category, confidence, permanent, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
           ON CONFLICT(entity, key) DO UPDATE SET
           value=excluded.value,
           category=excluded.category,
           confidence=excluded.confidence,
           permanent=excluded.permanent,
           updated_at=datetime('now')""",
        (entity, key, value, category, confidence, perm)
    )
    conn.commit()
    conn.close()
    print(f"✅ Set: {entity}.{key} = {value}")


def cmd_search(query, limit=10, json_out=False):
    """Full-text search across facts."""
    conn = get_conn()
    cursor = conn.cursor()
    
    cursor.execute(
        """SELECT f.entity, f.key, f.value, f.category, f.confidence
           FROM facts f
           JOIN facts_fts fts ON f.id = fts.rowid
           WHERE facts_fts MATCH ?
           ORDER BY f.access_count DESC, f.confidence DESC
           LIMIT ?""",
        (query, limit)
    )
    rows = cursor.fetchall()
    
    # Track access for found facts
    for row in rows:
        try:
            cursor.execute(
                "UPDATE facts SET access_count = access_count + 1, last_accessed = datetime('now') WHERE entity = ? AND key = ?",
                (row[0], row[1])
            )
        except Exception as e:
            pass  # Batch tracking — log would be too noisy
    conn.commit()
    conn.close()
    
    if json_out:
        results = [{"entity": r[0], "key": r[1], "value": r[2], "category": r[3], "confidence": r[4]} for r in rows]
        print(json.dumps(results, indent=2))
    else:
        if not rows:
            print("No matches found")
            return
        
        print(f"{'ENTITY':<20} {'KEY':<20} {'VALUE':<30} {'CAT':<10}")
        print("─" * 80)
        for r in rows:
            entity = r[0][:18]
            key = r[1][:18]
            value = r[2][:28]
            cat = r[3][:8]
            print(f"{entity:<20} {key:<20} {value:<30} {cat:<10}")


def cmd_list(entity=None, category=None, limit=50):
    """List facts, optionally filtered by entity or category."""
    conn = get_conn()
    cursor = conn.cursor()
    
    query = "SELECT entity, key, value, category FROM facts WHERE 1=1"
    params = []
    
    if entity:
        query += " AND entity = ?"
        params.append(entity)
    if category:
        query += " AND category = ?"
        params.append(category)
    
    query += " ORDER BY updated_at DESC LIMIT ?"
    params.append(limit)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        print("No facts found")
        return
    
    print(f"{'ENTITY':<20} {'KEY':<20} {'VALUE':<30} {'CAT':<10}")
    print("─" * 80)
    for r in rows:
        entity = r[0][:18]
        key = r[1][:18]
        value = r[2][:28]
        cat = r[3][:8]
        print(f"{entity:<20} {key:<20} {value:<30} {cat:<10}")


def cmd_delete(entity, key):
    """Delete a specific fact."""
    conn = get_conn()
    cursor = conn.cursor()
    
    cursor.execute(
        "DELETE FROM facts WHERE entity = ? AND key = ?",
        (entity, key)
    )
    conn.commit()
    
    if cursor.rowcount > 0:
        print(f"🗑️ Deleted: {entity}.{key}")
    else:
        print(f"❌ Not found: {entity}.{key}")
    
    conn.close()


def cmd_stats():
    """Show facts database statistics."""
    conn = get_conn()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM facts")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT entity) FROM facts")
    entities = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT category) FROM facts")
    categories = cursor.fetchone()[0]
    
    cursor.execute("SELECT category, COUNT(*) FROM facts GROUP BY category ORDER BY COUNT(*) DESC LIMIT 5")
    top_cats = cursor.fetchall()
    
    cursor.execute("SELECT entity, COUNT(*) FROM facts GROUP BY entity ORDER BY COUNT(*) DESC LIMIT 5")
    top_entities = cursor.fetchall()
    
    conn.close()
    
    print("=== FACTS DATABASE STATS ===")
    print(f"Total facts: {total}")
    print(f"Unique entities: {entities}")
    print(f"Categories: {categories}")
    print()
    print("Top categories:")
    for cat, count in top_cats:
        print(f"  {cat}: {count}")
    print()
    print("Top entities:")
    for ent, count in top_entities:
        print(f"  {ent}: {count}")


def main():
    if len(sys.argv) < 2:
        print("Usage: brain facts <command> [args]")
        print("Commands: get, set, search, list, delete, stats")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "get":
        if len(sys.argv) < 4:
            print("Usage: brain facts get <entity> <key>")
            sys.exit(1)
        cmd_get(sys.argv[2], sys.argv[3])
    
    elif cmd == "set":
        if len(sys.argv) < 5:
            print('Usage: brain facts set <entity> <key> <value> [--category <cat>] [--permanent] [--confidence <0.0-1.0>]')
            sys.exit(1)
        
        entity = sys.argv[2]
        key = sys.argv[3]
        value = sys.argv[4]
        category = "general"
        permanent = False
        confidence = 1.0
        
        i = 5
        while i < len(sys.argv):
            if sys.argv[i] == "--category":
                category = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--permanent":
                permanent = True
                i += 1
            elif sys.argv[i] == "--confidence":
                confidence = float(sys.argv[i + 1])
                i += 2
            else:
                i += 1
        
        cmd_set(entity, key, value, category, permanent, confidence)
    
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("Usage: brain facts search <query> [--limit N] [--json]")
            sys.exit(1)
        
        query = sys.argv[2]
        limit = 10
        json_out = False
        
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--limit":
                limit = int(sys.argv[i + 1])
                i += 2
            elif sys.argv[i] == "--json":
                json_out = True
                i += 1
            else:
                i += 1
        
        cmd_search(query, limit, json_out)
    
    elif cmd == "list":
        entity = None
        category = None
        limit = 50
        
        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--entity":
                entity = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--category":
                category = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--limit":
                limit = int(sys.argv[i + 1])
                i += 2
            else:
                i += 1
        
        cmd_list(entity, category, limit)
    
    elif cmd == "delete":
        if len(sys.argv) < 4:
            print("Usage: brain facts delete <entity> <key>")
            sys.exit(1)
        cmd_delete(sys.argv[2], sys.argv[3])
    
    elif cmd == "stats":
        cmd_stats()
    
    else:
        print(f"Unknown command: {cmd}")
        print("Commands: get, set, search, list, delete, stats")
        sys.exit(1)


if __name__ == "__main__":
    main()
