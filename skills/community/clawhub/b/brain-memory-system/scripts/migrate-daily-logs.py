#!/usr/bin/env python3
"""
Migrate markdown daily logs into Brain episodic memory.
Parses ## HH:MM — Title [feeling: word/intensity] format.
"""
import re
import sqlite3
import sys
import os
from pathlib import Path
from datetime import datetime

MEMORY_DIR = os.environ.get("MEMORY_DIR", "memory")
BRAIN_DB = os.environ.get("BRAIN_DB", "tools/brain/brain.db")

# Pattern: ## HH:MM — Title [feeling: word/intensity]
ENTRY_PATTERN = re.compile(
    r'^##\s+'
    r'(?P<time>\d{1,2}:\d{2}(?:\s*[AP]M)?)'
    r'\s*[-—–]\s*'
    r'(?P<title>.+?)'
    r'(?:\s*\[feeling:\s*(?P<emotion>[^/\]]+?)(?:/(?P<intensity>[^\]]+))?\])?'
    r'\s*$',
    re.IGNORECASE
)

# Also match entries without time: ## Title [feeling: ...]
ENTRY_NO_TIME = re.compile(
    r'^##\s+'
    r'(?P<title>[^[\n]+?)'
    r'(?:\s*\[feeling:\s*(?P<emotion>[^/\]]+?)(?:/(?P<intensity>[^\]]+))?\])?'
    r'\s*$',
    re.IGNORECASE
)

# Date from filename: YYYY-MM-DD.md
DATE_PATTERN = re.compile(r'(\d{4}-\d{2}-\d{2})\.md$')


def parse_daily_log(filepath: Path) -> list[dict]:
    """Parse a daily log markdown file into episode entries."""
    date_match = DATE_PATTERN.search(filepath.name)
    if not date_match:
        return []
    
    date = date_match.group(1)
    entries = []
    current_entry = None
    content_lines = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        # Skip the H1 title line
        if line.startswith('# ') and not line.startswith('## '):
            continue
        
        # Try matching entry header with time
        match = ENTRY_PATTERN.match(line.strip())
        if not match:
            # Try without time (some entries don't have timestamps)
            match = ENTRY_NO_TIME.match(line.strip())
            if match and not line.strip().startswith('## Steps') and not line.strip().startswith('## Failure'):
                # Only treat as entry if it looks like a real entry header
                title = match.group('title').strip()
                if len(title) < 3 or title.lower() in ('steps', 'failure log', 'version history', 'format', 'active handoffs', 'archive', 'quick reference for bud'):
                    content_lines.append(line)
                    continue
        
        if match:
            # Save previous entry
            if current_entry:
                current_entry['content'] = ''.join(content_lines).strip()
                if current_entry['content']:  # Only add if has content
                    entries.append(current_entry)
            
            # Start new entry
            time_val = match.group('time') if 'time' in match.groupdict() and match.group('time') else None
            current_entry = {
                'date': date,
                'time': normalize_time(time_val) if time_val else None,
                'title': match.group('title').strip().rstrip('🔒🔧🛡️⚡🎉✅❌🔴🟡🟢💓🏠📋🔊💡🎤📝🗓️📊🦴🎩❓🌿🤖💻📱🔑').strip(),
                'emotion': match.group('emotion').strip() if match.group('emotion') else None,
                'emotion_intensity': match.group('intensity').strip() if 'intensity' in match.groupdict() and match.group('intensity') else None,
            }
            content_lines = []
        else:
            content_lines.append(line)
    
    # Don't forget last entry
    if current_entry:
        current_entry['content'] = ''.join(content_lines).strip()
        if current_entry['content']:
            entries.append(current_entry)
    
    return entries


def normalize_time(time_str: str) -> str:
    """Normalize time to HH:MM 24h format."""
    if not time_str:
        return None
    time_str = time_str.strip()
    
    # Already 24h format
    if re.match(r'^\d{1,2}:\d{2}$', time_str):
        parts = time_str.split(':')
        return f"{int(parts[0]):02d}:{parts[1]}"
    
    # 12h format with AM/PM
    match = re.match(r'(\d{1,2}):(\d{2})\s*(AM|PM)', time_str, re.IGNORECASE)
    if match:
        h, m, period = int(match.group(1)), match.group(2), match.group(3).upper()
        if period == 'PM' and h != 12:
            h += 12
        elif period == 'AM' and h == 12:
            h = 0
        return f"{h:02d}:{m}"
    
    return time_str


def estimate_importance(entry: dict) -> int:
    """Estimate importance 1-10 based on content signals."""
    content = (entry.get('content', '') + ' ' + entry.get('title', '')).lower()
    score = 5  # baseline
    
    # High importance signals
    if any(w in content for w in ['puddin', 'darian', 'fix', 'deploy', 'broke', 'critical', 'security']):
        score += 2
    if any(w in content for w in ['lesson', 'root cause', 'learned', 'mistake']):
        score += 2
    if entry.get('emotion_intensity') == 'high':
        score += 2
    if entry.get('emotion_intensity') == 'medium':
        score += 1
    
    # Low importance signals
    if any(w in content for w in ['heartbeat_ok', 'nothing new', 'routine', 'no action needed']):
        score -= 2
    if 'cron' in content and 'fix' not in content:
        score -= 1
    
    return max(1, min(10, score))


def migrate(dry_run=False):
    """Run the migration."""
    memory_path = Path(MEMORY_DIR)
    log_files = sorted(memory_path.glob('2026-*.md'))
    
    if not log_files:
        print(f"No daily log files found in {memory_path}/")
        return
    
    print(f"Found {len(log_files)} daily log files")
    
    total_entries = 0
    all_entries = []
    
    for log_file in log_files:
        entries = parse_daily_log(log_file)
        if entries:
            print(f"  {log_file.name}: {len(entries)} entries")
            all_entries.extend(entries)
            total_entries += len(entries)
    
    print(f"\nTotal: {total_entries} episodes parsed")
    
    if dry_run:
        print("\n--- DRY RUN (not writing to DB) ---")
        for e in all_entries[:10]:
            print(f"  [{e['date']} {e.get('time', '??:??')}] {e['title'][:60]}"
                  f" | emotion={e.get('emotion', 'none')}/{e.get('emotion_intensity', 'none')}"
                  f" | importance={estimate_importance(e)}")
        if len(all_entries) > 10:
            print(f"  ... and {len(all_entries) - 10} more")
        return
    
    # Initialize DB
    db_path = Path(BRAIN_DB)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(db_path))
    
    # Apply schema
    schema_path = db_path.parent / 'schema.sql'
    if schema_path.exists():
        conn.executescript(schema_path.read_text())
        print(f"Schema applied from {schema_path}")
    
    # Insert episodes
    inserted = 0
    skipped = 0
    for entry in all_entries:
        # Check for duplicates
        existing = conn.execute(
            "SELECT id FROM episodes WHERE date=? AND title=?",
            (entry['date'], entry['title'])
        ).fetchone()
        
        if existing:
            skipped += 1
            continue
        
        importance = estimate_importance(entry)
        
        conn.execute(
            """INSERT INTO episodes 
               (date, time, title, content, emotion, emotion_intensity, 
                importance, source, agent)
               VALUES (?, ?, ?, ?, ?, ?, ?, 'migration', 'margot')""",
            (entry['date'], entry.get('time'), entry['title'], entry['content'],
             entry.get('emotion'), entry.get('emotion_intensity'), importance)
        )
        inserted += 1
    
    conn.commit()
    
    # Verify
    count = conn.execute("SELECT COUNT(*) FROM episodes").fetchone()[0]
    print(f"\nMigration complete!")
    print(f"  Inserted: {inserted}")
    print(f"  Skipped (duplicates): {skipped}")
    print(f"  Total episodes in DB: {count}")
    
    # Test FTS
    test = conn.execute(
        "SELECT date, title FROM episodes_fts WHERE episodes_fts MATCH ? LIMIT 3",
        ('LightRAG',)
    ).fetchall()
    if test:
        print(f"\nFTS test ('LightRAG'): {len(test)} results")
        for row in test:
            print(f"  {row[0]}: {row[1][:60]}")
    
    conn.close()


if __name__ == '__main__':
    dry_run = '--dry-run' in sys.argv
    migrate(dry_run=dry_run)
