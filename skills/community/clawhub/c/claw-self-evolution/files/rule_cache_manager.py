#!/usr/bin/env python3
"""
Rule cache manager - optimize token consumption by caching core rules
Only reload when files change, avoid re-reading the same content every time
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Optional, Tuple

WORKING_ROOT = Path("/app/working")
CACHE_FILE = WORKING_ROOT / ".rule_cache.json"

CORE_FILES = [
    ("MEMORY.md", WORKING_ROOT / "MEMORY.md"),
    ("user_profile.md", WORKING_ROOT / "memory" / "user_profile.md"),
]

class RuleCache:
    def __init__(self):
        self.cache: Dict = {}
        self._load_cache()
    
    def _load_cache(self):
        """Load cache from disk"""
        if CACHE_FILE.exists():
            try:
                with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                    self.cache = json.load(f)
            except Exception:
                self.cache = {}
        else:
            self.cache = {}
    
    def _save_cache(self):
        """Save cache to disk"""
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, indent=2)
    
    @staticmethod
    def _get_file_hash(file_path: Path) -> Optional[str]:
        """Calculate file content hash"""
        if not file_path.exists():
            return None
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                return hashlib.sha256(content).hexdigest()
        except Exception:
            return None
    
    @staticmethod
    def _read_file_content(file_path: Path) -> Optional[str]:
        """Read file content"""
        if not file_path.exists():
            return None
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return None
    
    def check_if_reload_needed(self) -> Tuple[bool, str]:
        """
        Check if any core file has changed, needs reload
        Returns: (reload_needed, message)
        """
        changed = []
        for name, path in CORE_FILES:
            current_hash = self._get_file_hash(path)
            cached = self.cache.get(name, {})
            
            if current_hash != cached.get('hash'):
                changed.append(name)
        
        if changed:
            return True, f"Core files changed: {', '.join(changed)}"
        return False, "All core files unchanged, cache valid"
    
    def update_cache(self):
        """Update cache with current file content"""
        for name, path in CORE_FILES:
            content = self._read_file_content(path)
            file_hash = self._get_file_hash(path)
            if content is not None:
                self.cache[name] = {
                    'hash': file_hash,
                    'content': content,
                    'last_updated': str(Path(__file__).stat().st_mtime)
                }
        self._save_cache()
    
    def get_cached_content(self, name: str) -> Optional[str]:
        """Get cached content"""
        entry = self.cache.get(name)
        if entry:
            return entry.get('content')
        return None
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        stats = {
            'total_cached': len(self.cache),
            'files': list(self.cache.keys()),
        }
        return stats
    
    def invalidate(self):
        """Invalidate all cache, force reload next time"""
        self.cache = {}
        self._save_cache()

def main():
    """CLI interface"""
    import sys
    cache = RuleCache()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'check':
            need_reload, msg = cache.check_if_reload_needed()
            print(msg)
            if need_reload:
                print("→ Reload required")
            else:
                print("→ Using cached content")
        elif cmd == 'update':
            cache.update_cache()
            print("✅ Cache updated")
        elif cmd == 'invalidate':
            cache.invalidate()
            print("✅ Cache invalidated, force reload next time")
        elif cmd == 'stats':
            stats = cache.get_stats()
            print(f"Cached files: {stats['total_cached']}")
            print(f"Files: {stats['files']}")
        else:
            print(f"Unknown command: {cmd}")
            print(f"Commands: check, update, invalidate, stats")
    else:
        need_reload, msg = cache.check_if_reload_needed()
        print(msg)
        if need_reload:
            cache.update_cache()
            print("✅ Cache updated")

if __name__ == "__main__":
    main()
