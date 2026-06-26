#!/usr/bin/env python3
"""
Memory Archiver - Tiered Memory System
Archives old QMD memory files to SQLite (Tier 0 → Tier 1)
"""

import os
import sys
import re
import sqlite3
import argparse
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

# Config
MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
ARCHIVE_DIR = Path.home() / ".openclaw" / "workspace" / "memory" / "archive"
DB_PATH = Path.home() / ".openclaw" / "memory_archive.db"
DEFAULT_DAYS = 14
OLLAMA_MODEL = "qwen2.5-coder:14b"  # or use kimi-coding if preferred

class MemoryArchiver:
    """Archives old memory files to SQLite"""
    
    def __init__(self, db_path: str = None, dry_run: bool = False):
        self.db_path = db_path or str(DB_PATH)
        self.dry_run = dry_run
        self._init_db()
        
    def _init_db(self):
        """Initialize archive database"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS archived_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_file TEXT NOT NULL,
                session_date DATE NOT NULL,
                summary TEXT NOT NULL,
                key_facts TEXT,  -- JSON array
                topics TEXT,  -- JSON array
                message_count INTEGER,
                archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_date ON archived_sessions(session_date)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_topics ON archived_sessions(topics)
        ''')
        
        conn.commit()
        conn.close()
        print(f"📁 Archive DB: {self.db_path}")
    
    def get_old_files(self, days: int = DEFAULT_DAYS) -> List[Path]:
        """Get memory files older than N days"""
        cutoff = datetime.now() - timedelta(days=days)
        old_files = []
        
        if not MEMORY_DIR.exists():
            print(f"⚠️  Memory directory not found: {MEMORY_DIR}")
            return []
        
        for file_path in MEMORY_DIR.glob("*.md"):
            # Skip archive folder contents and non-date files
            if "archive" in str(file_path):
                continue
                
            # Extract date from filename (YYYY-MM-DD.md)
            match = re.match(r'(\d{4}-\d{2}-\d{2})\.md', file_path.name)
            if not match:
                continue
                
            file_date = datetime.strptime(match.group(1), '%Y-%m-%d')
            
            if file_date < cutoff:
                old_files.append(file_path)
        
        # Sort by date (oldest first)
        old_files.sort()
        return old_files
    
    def read_file(self, file_path: Path) -> str:
        """Read file content"""
        try:
            return file_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"⚠️  Error reading {file_path}: {e}")
            return ""
    
    def summarize_with_ollama(self, content: str) -> Dict:
        """Use Ollama to summarize content"""
        
        # Truncate if too long (rough token estimate)
        max_chars = 8000
        if len(content) > max_chars:
            content = content[:max_chars] + "\n... [truncated]"
        
        prompt = f"""You are a memory summarizer. Read this daily log and extract:
1. A concise summary (2-3 sentences)
2. Key facts learned (max 5 bullet points)
3. Main topics discussed (max 3 tags)

Format your response as:
SUMMARY: <summary text>
FACTS:
- <fact 1>
- <fact 2>
...
TOPICS: <tag1>, <tag2>, <tag3>

---
LOG CONTENT:
{content}
---
"""
        
        try:
            result = subprocess.run(
                ["ollama", "run", OLLAMA_MODEL, prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            output = result.stdout.strip()
            return self._parse_summary(output)
            
        except subprocess.TimeoutExpired:
            print(f"⏱️  Ollama timeout, using fallback")
            return self._fallback_summary(content)
        except Exception as e:
            print(f"⚠️  Ollama error: {e}, using fallback")
            return self._fallback_summary(content)
    
    def _parse_summary(self, output: str) -> Dict:
        """Parse Ollama output"""
        summary = ""
        facts = []
        topics = []
        
        lines = output.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('SUMMARY:'):
                summary = line.replace('SUMMARY:', '').strip()
                current_section = 'summary'
            elif line.startswith('FACTS:'):
                current_section = 'facts'
            elif line.startswith('TOPICS:'):
                topics_text = line.replace('TOPICS:', '').strip()
                topics = [t.strip() for t in topics_text.split(',') if t.strip()]
                current_section = None
            elif line.startswith('- ') and current_section == 'facts':
                facts.append(line[2:].strip())
        
        return {
            'summary': summary or "Session archived",
            'facts': facts[:5],
            'topics': topics[:3]
        }
    
    def _fallback_summary(self, content: str) -> Dict:
        """Simple fallback if LLM fails"""
        lines = content.split('\n')
        
        # Extract first heading as summary
        summary = "Session log"
        for line in lines:
            if line.startswith('# ') or line.startswith('## '):
                summary = line.strip('# ').strip()
                break
        
        # Count lines for message count
        msg_count = len([l for l in lines if l.strip()])
        
        return {
            'summary': summary,
            'facts': [f"Log contains {msg_count} lines"],
            'topics': ["general"]
        }
    
    def archive_file(self, file_path: Path, summary_data: Dict) -> bool:
        """Store archive entry in SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Extract date from filename
        match = re.match(r'(\d{4}-\d{2}-\d{2})\.md', file_path.name)
        session_date = match.group(1) if match else datetime.now().strftime('%Y-%m-%d')
        
        try:
            import json
            cursor.execute('''
                INSERT INTO archived_sessions 
                (source_file, session_date, summary, key_facts, topics, message_count)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                str(file_path),
                session_date,
                summary_data['summary'],
                json.dumps(summary_data['facts']),
                json.dumps(summary_data['topics']),
                summary_data.get('message_count', 0)
            ))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"❌ DB error: {e}")
            return False
        finally:
            conn.close()
    
    def move_to_archive(self, file_path: Path) -> bool:
        """Move file to archive folder"""
        if self.dry_run:
            return True
            
        try:
            ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
            dest = ARCHIVE_DIR / file_path.name
            
            # Handle duplicates
            counter = 1
            while dest.exists():
                dest = ARCHIVE_DIR / f"{file_path.stem}_{counter}{file_path.suffix}"
                counter += 1
            
            file_path.rename(dest)
            return True
            
        except Exception as e:
            print(f"❌ Move error: {e}")
            return False
    
    def run(self, days: int = DEFAULT_DAYS, skip_llm: bool = False):
        """Main archive run"""
        print(f"🔍 Scanning for files older than {days} days...")
        print(f"📂 Memory dir: {MEMORY_DIR}")
        
        old_files = self.get_old_files(days)
        
        if not old_files:
            print("✅ No old files to archive")
            return
        
        print(f"📋 Found {len(old_files)} file(s) to archive")
        print()
        
        archived = 0
        failed = 0
        
        for file_path in old_files:
            print(f"📄 {file_path.name}")
            
            # Read content
            content = self.read_file(file_path)
            if not content:
                failed += 1
                continue
            
            # Summarize
            if skip_llm:
                summary_data = self._fallback_summary(content)
            else:
                summary_data = self.summarize_with_ollama(content)
                summary_data['message_count'] = len(content.split('\n'))
            
            print(f"   Summary: {summary_data['summary'][:60]}...")
            print(f"   Facts: {len(summary_data['facts'])}")
            print(f"   Topics: {', '.join(summary_data['topics'])}")
            
            # Archive to DB
            if self.dry_run:
                print(f"   [DRY RUN] Would archive")
                archived += 1
            else:
                if self.archive_file(file_path, summary_data):
                    # Move to archive folder
                    if self.move_to_archive(file_path):
                        print(f"   ✅ Archived")
                        archived += 1
                    else:
                        print(f"   ⚠️  DB ok but move failed")
                        failed += 1
                else:
                    print(f"   ❌ Archive failed")
                    failed += 1
            
            print()
        
        print(f"📊 Done: {archived} archived, {failed} failed")


def main():
    parser = argparse.ArgumentParser(description="Memory Archiver - Tier 0 → Tier 1")
    parser.add_argument('--days', type=int, default=DEFAULT_DAYS,
                       help=f'Archive files older than N days (default: {DEFAULT_DAYS})')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be archived without doing it')
    parser.add_argument('--skip-llm', action='store_true',
                       help='Skip LLM summarization (use fallback)')
    parser.add_argument('--list', action='store_true',
                       help='List archived sessions')
    parser.add_argument('--search', type=str,
                       help='Search archived summaries')
    
    args = parser.parse_args()
    
    archiver = MemoryArchiver(dry_run=args.dry_run)
    
    if args.list:
        # List archived sessions
        conn = sqlite3.connect(archiver.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT session_date, summary, topics 
            FROM archived_sessions 
            ORDER BY session_date DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        
        print(f"📚 Archived sessions ({len(rows)} total):")
        for row in rows:
            print(f"\n📅 {row[0]}")
            print(f"   {row[1][:80]}...")
            if row[2]:
                import json
                topics = json.loads(row[2])
                print(f"   🏷️  {', '.join(topics)}")
        return
    
    if args.search:
        # Search archived sessions
        import json
        conn = sqlite3.connect(archiver.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT session_date, summary, key_facts 
            FROM archived_sessions 
            WHERE summary LIKE ? OR key_facts LIKE ?
            ORDER BY session_date DESC
        ''', (f'%{args.search}%', f'%{args.search}%'))
        rows = cursor.fetchall()
        conn.close()
        
        print(f"🔍 Search results for '{args.search}' ({len(rows)} found):")
        for row in rows:
            print(f"\n📅 {row[0]}")
            print(f"   {row[1]}")
        return
    
    # Run archive
    archiver.run(days=args.days, skip_llm=args.skip_llm)


if __name__ == '__main__':
    main()
