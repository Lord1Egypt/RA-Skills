#!/usr/bin/env python3
"""
Cache Manager: Content-addressable cache for task results.
- Cache task results by hash of (task_type + params)
- Check cache before delegating  
- Store results in TOON format
- Auto-expire after configurable TTL
"""
import hashlib
import json
import os
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

CACHE_DIR = Path('/a0/usr/projects/frugal_orchestrator/cache')
DEFAULT_TTL_DAYS = 7

class CacheManager:
    """Content-addressable cache with TOON format storage"""
    
    def __init__(self, ttl_days: int = DEFAULT_TTL_DAYS):
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(days=ttl_days)
        self.stats = {'hits': 0, 'misses': 0, 'expired': 0}
    
    def _hash_task(self, task_type: str, params: Dict[str, Any]) -> str:
        """Generate content hash from task type + params"""
        content = f"{task_type}:{json.dumps(params, sort_keys=True, default=str)}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def _to_toon(self, data: Dict[str, Any], task_hash: str, task_type: str) -> str:
        """Convert data to TOON format"""
        lines = [
            f"# Task Cache Entry",
            f"task_hash: {task_hash}",
            f"task_type: {task_type}",
            f"created: {datetime.now().isoformat()}",
            f"expires: {(datetime.now() + self.ttl).isoformat()}",
            f"ttl_days: {self.ttl.days}",
            ""
        ]
        
        # Convert result data
        for key, value in data.items():
            if isinstance(value, str):
                if '\n' in value:
                    lines.append(f"{key}:")
                    for line in value.split('\n'):
                        lines.append(f"  {line}")
                else:
                    lines.append(f"{key}: {value}")
            elif isinstance(value, (list, dict)):
                lines.append(f"{key}: {json.dumps(value)}")
            else:
                lines.append(f"{key}: {value}")
        
        return '\n'.join(lines)
    
    def _from_toon(self, content: str) -> Dict[str, Any]:
        """Parse TOON format to dictionary"""
        result = {}
        lines = content.split('\n')
        current_key = None
        multiline_value = []
        
        for line in lines:
            line = line.rstrip()
            if not line or line.startswith('#'):
                if current_key and multiline_value:
                    result[current_key] = '\n'.join(multiline_value)
                    multiline_value = []
                current_key = None
                continue
            
            match = re.match(r'^([\w_]+):\s*(.*)$', line)
            if match:
                if current_key and multiline_value:
                    result[current_key] = '\n'.join(multiline_value)
                    multiline_value = []
                
                key, value = match.group(1), match.group(2)
                
                if not value:
                    current_key = key
                    multiline_value = []
                elif value.startswith('[') or value.startswith('{'):
                    try:
                        result[key] = json.loads(value)
                    except:
                        result[key] = value
                else:
                    result[key] = value
                current_key = None
            elif current_key is not None and line.startswith('  '):
                multiline_value.append(line[2:])
            else:
                if current_key and multiline_value:
                    result[current_key] = '\n'.join(multiline_value)
                    multiline_value = []
                current_key = None
        
        if current_key and multiline_value:
            result[current_key] = '\n'.join(multiline_value)
        
        return result
    
    def get(self, task_type: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get cached result if valid"""
        task_hash = self._hash_task(task_type, params)
        cache_file = CACHE_DIR / f"{task_hash}.toon"
        
        if not cache_file.exists():
            self.stats['misses'] += 1
            return None
        
        try:
            content = cache_file.read_text()
            data = self._from_toon(content)
            
            expires = data.get('expires', '')
            if expires:
                try:
                    expires_dt = datetime.fromisoformat(expires)
                    if datetime.now() > expires_dt:
                        cache_file.unlink()
                        self.stats['expired'] += 1
                        self.stats['misses'] += 1
                        return None
                except:
                    pass
            
            self.stats['hits'] += 1
            return data.get('result', data)
        
        except Exception:
            self.stats['misses'] += 1
            return None
    
    def set(self, task_type: str, params: Dict[str, Any], result: Dict[str, Any]) -> str:
        """Cache result with TOON format"""
        task_hash = self._hash_task(task_type, params)
        cache_file = CACHE_DIR / f"{task_hash}.toon"
        
        data = {'result': result}
        toon_content = self._to_toon(data, task_hash, task_type)
        cache_file.write_text(toon_content)
        
        return task_hash
    
    def exists(self, task_type: str, params: Dict[str, Any]) -> bool:
        """Check if cached entry exists without reading"""
        task_hash = self._hash_task(task_type, params)
        cache_file = CACHE_DIR / f"{task_hash}.toon"
        if not cache_file.exists():
            return False
        
        try:
            content = cache_file.read_text()
            data = self._from_toon(content)
            expires = data.get('expires', '')
            if expires:
                try:
                    expires_dt = datetime.fromisoformat(expires)
                    if datetime.now() > expires_dt:
                        cache_file.unlink()
                        return False
                except:
                    pass
        except:
            pass
        
        return True
    
    def invalidate(self, task_type: str = None) -> int:
        """Invalidate cache entries"""
        count = 0
        for f in CACHE_DIR.glob("*.toon"):
            if task_type is None or task_type in f.read_text():
                f.unlink()
                count += 1
        return count
    
    def stats_summary(self) -> Dict[str, Any]:
        """Get cache statistics"""
        files = list(CACHE_DIR.glob("*.toon"))
        total_size = sum(f.stat().st_size for f in files)
        total_ops = self.stats['hits'] + self.stats['misses']
        
        return {
            'hits': self.stats['hits'],
            'misses': self.stats['misses'],
            'expired': self.stats['expired'],
            'total_files': len(files),
            'total_size_bytes': total_size,
            'hit_rate': round(self.stats['hits'] / total_ops * 100, 2) if total_ops > 0 else 0
        }
    
    def list_entries(self) -> list:
        """List all cache entries"""
        entries = []
        for f in CACHE_DIR.glob("*.toon"):
            try:
                data = self._from_toon(f.read_text())
                entries.append({
                    'hash': data.get('task_hash'),
                    'type': data.get('task_type'),
                    'created': data.get('created'),
                    'expires': data.get('expires'),
                    'file': str(f.name)
                })
            except:
                pass
        return entries


def main():
    import sys
    cache = TaskCache()
    
    if len(sys.argv) < 2:
        print(json.dumps(cache.stats_summary(), indent=2))
        return
    
    cmd = sys.argv[1]
    
    if cmd == 'get':
        if len(sys.argv) < 4:
            print(json.dumps({'error': 'Usage: cache_manager.py get <task_type> <params_json>'}))
            return
        task_type = sys.argv[2]
        params = json.loads(sys.argv[3])
        result = cache.get(task_type, params)
        print(json.dumps({'hit': result is not None, 'result': result}, indent=2, default=str))
    
    elif cmd == 'set':
        if len(sys.argv) < 5:
            print(json.dumps({'error': 'Usage: cache_manager.py set <task_type> <params_json> <result_json>'}))
            return
        task_type = sys.argv[2]
        params = json.loads(sys.argv[3])
        result = json.loads(' '.join(sys.argv[4:]))
        task_hash = cache.set(task_type, params, result)
        print(json.dumps({'cached': True, 'hash': task_hash}))
    
    elif cmd == 'exists':
        task_type = sys.argv[2]
        params = json.loads(sys.argv[3])
        exists = cache.exists(task_type, params)
        print(json.dumps({'exists': exists}))
    
    elif cmd == 'invalidate':
        task_type = sys.argv[2] if len(sys.argv) > 2 else None
        count = cache.invalidate(task_type)
        print(json.dumps({'invalidated': count}))
    
    elif cmd == 'list':
        entries = cache.list_entries()
        print(json.dumps({'entries': entries}, indent=2, default=str))
    
    elif cmd == 'stats':
        print(json.dumps(cache.stats_summary(), indent=2))
    
    else:
        print(json.dumps({'error': f'Unknown command: {cmd}', 'available': ['get', 'set', 'exists', 'invalidate', 'list', 'stats']}))


if __name__ == '__main__':
    main()
