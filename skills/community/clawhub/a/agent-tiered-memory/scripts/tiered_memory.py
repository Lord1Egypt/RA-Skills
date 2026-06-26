"""
Tiered Memory - Unified interface for QMD + SQLite memory
"""

import os
import sys
import json
import sqlite3
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta

# Config
MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
ARCHIVE_DB = Path.home() / ".openclaw" / "memory_archive.db"


class TieredMemory:
    """
    Unified interface for tiered memory system.
    
    Tier 0: QMD semantic search (recent 7-14 days)
    Tier 1: SQLite archive (older sessions)
    """
    
    def __init__(self, 
                 memory_dir: str = None, 
                 archive_db: str = None,
                 qmd_enabled: bool = True):
        self.memory_dir = Path(memory_dir) if memory_dir else MEMORY_DIR
        self.archive_db = archive_db or str(ARCHIVE_DB)
        self.qmd_enabled = qmd_enabled
    
    def search(self, query: str, days_back: int = 14, limit: int = 10) -> Dict[str, List]:
        """
        Search across both memory tiers.
        
        Args:
            query: Search query
            days_back: How many days to check in Tier 0
            limit: Max results per tier
            
        Returns:
            Dict with 'tier0' and 'tier1' results
        """
        results = {
            'tier0': [],  # QMD results
            'tier1': []   # Archive results
        }
        
        # Tier 0: Recent files (file system scan)
        results['tier0'] = self._search_recent_files(query, days_back, limit)
        
        # Tier 1: Archive (SQLite)
        results['tier1'] = self._search_archive(query, limit)
        
        return results
    
    def _search_recent_files(self, query: str, days_back: int, limit: int) -> List[Dict]:
        """Search recent memory files (Tier 0)"""
        cutoff = datetime.now() - timedelta(days=days_back)
        matches = []
        
        if not self.memory_dir.exists():
            return matches
        
        for file_path in self.memory_dir.glob("*.md"):
            # Skip archive folder
            if "archive" in str(file_path):
                continue
            
            # Check date
            try:
                import re
                match = re.match(r'(\d{4}-\d{2}-\d{2})\.md', file_path.name)
                if match:
                    file_date = datetime.strptime(match.group(1), '%Y-%m-%d')
                    if file_date < cutoff:
                        continue  # Too old, skip (will be in archive)
            except:
                pass
            
            # Read and search
            try:
                content = file_path.read_text(encoding='utf-8')
                # Simple keyword search (QMD does semantic, we do keyword)
                if query.lower() in content.lower():
                    # Find context around match
                    idx = content.lower().find(query.lower())
                    start = max(0, idx - 100)
                    end = min(len(content), idx + 200)
                    context = content[start:end].replace('\n', ' ')
                    
                    matches.append({
                        'source': str(file_path),
                        'date': file_path.stem,
                        'context': context,
                        'tier': 0
                    })
                    
                    if len(matches) >= limit:
                        break
                        
            except Exception as e:
                continue
        
        return matches
    
    def _search_archive(self, query: str, limit: int) -> List[Dict]:
        """Search SQLite archive (Tier 1)"""
        matches = []
        
        if not Path(self.archive_db).exists():
            return matches
        
        try:
            conn = sqlite3.connect(self.archive_db)
            cursor = conn.cursor()
            
            # Search summaries and key_facts
            cursor.execute('''
                SELECT session_date, summary, key_facts, topics
                FROM archived_sessions
                WHERE summary LIKE ? OR key_facts LIKE ?
                ORDER BY session_date DESC
                LIMIT ?
            ''', (f'%{query}%', f'%{query}%', limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            for row in rows:
                matches.append({
                    'date': row[0],
                    'summary': row[1],
                    'key_facts': json.loads(row[2]) if row[2] else [],
                    'topics': json.loads(row[3]) if row[3] else [],
                    'tier': 1
                })
                
        except Exception as e:
            print(f"Archive search error: {e}")
        
        return matches
    
    def get_recent_sessions(self, days: int = 7) -> List[Dict]:
        """Get list of recent memory sessions"""
        sessions = []
        cutoff = datetime.now() - timedelta(days=days)
        
        if not self.memory_dir.exists():
            return sessions
        
        for file_path in self.memory_dir.glob("*.md"):
            if "archive" in str(file_path):
                continue
            
            try:
                import re
                match = re.match(r'(\d{4}-\d{2}-\d{2})\.md', file_path.name)
                if match:
                    file_date = datetime.strptime(match.group(1), '%Y-%m-%d')
                    if file_date >= cutoff:
                        sessions.append({
                            'date': match.group(1),
                            'path': str(file_path),
                            'tier': 0
                        })
            except:
                pass
        
        return sorted(sessions, key=lambda x: x['date'], reverse=True)
    
    def get_archived_sessions(self, limit: int = 100) -> List[Dict]:
        """Get list of archived sessions"""
        sessions = []
        
        if not Path(self.archive_db).exists():
            return sessions
        
        try:
            conn = sqlite3.connect(self.archive_db)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT session_date, summary, topics
                FROM archived_sessions
                ORDER BY session_date DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            for row in rows:
                sessions.append({
                    'date': row[0],
                    'summary': row[1][:100] + "..." if len(row[1]) > 100 else row[1],
                    'topics': json.loads(row[2]) if row[2] else [],
                    'tier': 1
                })
                
        except Exception as e:
            print(f"Error reading archive: {e}")
        
        return sessions
    
    def get_session(self, date_str: str) -> Optional[Dict]:
        """
        Get a specific session by date.
        
        Args:
            date_str: Date in YYYY-MM-DD format
            
        Returns:
            Session data or None
        """
        # Try Tier 0 first (file system)
        file_path = self.memory_dir / f"{date_str}.md"
        if file_path.exists():
            try:
                content = file_path.read_text(encoding='utf-8')
                return {
                    'date': date_str,
                    'content': content,
                    'tier': 0,
                    'source': str(file_path)
                }
            except Exception as e:
                pass
        
        # Try Tier 1 (archive)
        try:
            conn = sqlite3.connect(self.archive_db)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT summary, key_facts, topics
                FROM archived_sessions
                WHERE session_date = ?
            ''', (date_str,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    'date': date_str,
                    'summary': row[0],
                    'key_facts': json.loads(row[1]) if row[1] else [],
                    'topics': json.loads(row[2]) if row[2] else [],
                    'tier': 1
                }
                
        except Exception as e:
            pass
        
        return None
    
    def stats(self) -> Dict:
        """Get memory system statistics"""
        stats = {
            'tier0_count': 0,
            'tier1_count': 0,
            'total_size_mb': 0
        }
        
        # Tier 0 stats
        if self.memory_dir.exists():
            for file_path in self.memory_dir.glob("*.md"):
                if "archive" not in str(file_path):
                    stats['tier0_count'] += 1
                    stats['total_size_mb'] += file_path.stat().st_size / (1024 * 1024)
        
        # Tier 1 stats
        if Path(self.archive_db).exists():
            try:
                conn = sqlite3.connect(self.archive_db)
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM archived_sessions')
                stats['tier1_count'] = cursor.fetchone()[0]
                conn.close()
                
                stats['total_size_mb'] += Path(self.archive_db).stat().st_size / (1024 * 1024)
            except:
                pass
        
        stats['total_size_mb'] = round(stats['total_size_mb'], 2)
        return stats


# CLI for testing
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description="Tiered Memory")
    parser.add_argument('action', choices=['search', 'stats', 'recent', 'archived'])
    parser.add_argument('--query', '-q', help='Search query')
    parser.add_argument('--days', '-d', type=int, default=14, help='Days back')
    parser.add_argument('--limit', '-l', type=int, default=10, help='Result limit')
    
    args = parser.parse_args()
    
    mem = TieredMemory()
    
    if args.action == 'stats':
        s = mem.stats()
        print(f"Tier 0 (Recent): {s['tier0_count']} sessions")
        print(f"Tier 1 (Archive): {s['tier1_count']} sessions")
        print(f"Total size: {s['total_size_mb']} MB")
    
    elif args.action == 'search':
        if not args.query:
            print("Error: --query required")
            sys.exit(1)
        
        results = mem.search(args.query, args.days, args.limit)
        
        print(f"\n🔍 Search: '{args.query}'")
        print(f"\n📂 Tier 0 (Recent):")
        for r in results['tier0']:
            print(f"  [{r['date']}] {r['context'][:80]}...")
        
        print(f"\n📦 Tier 1 (Archive):")
        for r in results['tier1']:
            print(f"  [{r['date']}] {r['summary'][:80]}...")
    
    elif args.action == 'recent':
        sessions = mem.get_recent_sessions(args.days)
        print(f"Recent sessions (last {args.days} days):")
        for s in sessions:
            print(f"  {s['date']} - {s['path']}")
    
    elif args.action == 'archived':
        sessions = mem.get_archived_sessions(args.limit)
        print(f"Archived sessions:")
        for s in sessions:
            topics = ', '.join(s['topics']) if s['topics'] else 'none'
            print(f"  [{s['date']}] {s['summary'][:60]}... (tags: {topics})")
