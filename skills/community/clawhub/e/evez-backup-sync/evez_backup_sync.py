#!/usr/bin/env python3
"""
EVEZ Backup & Sync Engine
- Git auto-commit + push to GitHub (every 10 min)
- Supabase cloud backup (files + state)
- mem0 persistent memory (knowledge + context)
- Composio integration for external services
"""

import json, time, os, subprocess, hashlib, logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from datetime import datetime

log = logging.getLogger("evez-backup")

WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
EVEZ_OS = WORKSPACE / "evez-os-sensors"
STATE_DIR = EVEZ_OS / "backup_state"
STATE_DIR.mkdir(parents=True, exist_ok=True)

# ── GIT BACKUP ──
def git_status():
    """Get git status of workspace."""
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True, text=True, cwd=str(WORKSPACE), timeout=10
        )
        return result.stdout.strip().split("\n") if result.stdout.strip() else []
    except Exception as e:
        return [f"error: {e}"]

def git_commit_push(message=None):
    """Commit all changes and push to GitHub."""
    if message is None:
        message = f"auto: EVEZ backup {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
    
    results = {"commit": None, "push": None}
    
    try:
        # Stage everything
        subprocess.run(["git", "add", "-A"], cwd=str(WORKSPACE), timeout=30, capture_output=True)
        
        # Commit
        r = subprocess.run(
            ["git", "commit", "-m", message, "--allow-empty"],
            capture_output=True, text=True, cwd=str(WORKSPACE), timeout=30
        )
        results["commit"] = r.stdout.strip() + r.stderr.strip()
        
        # Push (try all remotes)
        for remote in ["advancement", "origin", "evez666"]:
            try:
                r = subprocess.run(
                    ["git", "push", remote, "main"],
                    capture_output=True, text=True, cwd=str(WORKSPACE), timeout=60
                )
                if r.returncode == 0:
                    results["push"] = f"pushed to {remote}"
                    break
                else:
                    results["push"] = f"failed: {r.stderr.strip()[:100]}"
            except:
                continue
        
        if not results["push"]:
            results["push"] = "all remotes failed (will retry)"
    except Exception as e:
        results["error"] = str(e)
    
    # Save state
    state = {
        "last_commit": datetime.utcnow().isoformat(),
        "message": message,
        "results": results,
    }
    (STATE_DIR / "last_git.json").write_text(json.dumps(state, indent=2))
    
    return results

# ── SUPABASE BACKUP ──
def supabase_backup(data: dict, table: str = "evez_state"):
    """Backup data to Supabase (requires SUPABASE_URL + KEY)."""
    url = os.environ.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_KEY", "")
    
    if not url or not key:
        return {"status": "skipped", "reason": "no Supabase credentials"}
    
    try:
        from supabase import create_client
        sb = create_client(url, key)
        
        record = {
            "created_at": datetime.utcnow().isoformat(),
            "table_name": table,
            "data": json.dumps(data),
            "checksum": hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:16],
        }
        
        result = sb.table(table).insert(record).execute()
        return {"status": "synced", "record": len(result.data)}
    except Exception as e:
        return {"status": "error", "error": str(e)[:200]}

# ── MEM0 PERSISTENT MEMORY ──
def mem0_save(content: str, user_id: str = "evez", metadata: dict = None):
    """Save knowledge to mem0 persistent memory."""
    try:
        from mem0 import Memory
        m = Memory.from_config({
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "collection_name": "evez_memory",
                    "embedding_model_dims": 1536,
                    "path": str(STATE_DIR / "qdrant"),
                }
            }
        })
        result = m.add(content, user_id=user_id, metadata=metadata or {})
        return {"status": "saved", "id": str(result)}
    except Exception as e:
        # Fallback: save to local JSON
        path = STATE_DIR / "mem0_fallback.json"
        memories = []
        if path.exists():
            try: memories = json.loads(path.read_text())
            except: pass
        memories.append({
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow().isoformat(),
        })
        path.write_text(json.dumps(memories[-500:], indent=2))
        return {"status": "saved_local", "fallback": True, "error": str(e)[:100]}

def mem0_search(query: str, user_id: str = "evez", limit: int = 5):
    """Search mem0 persistent memory."""
    try:
        from mem0 import Memory
        m = Memory.from_config({
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "collection_name": "evez_memory",
                    "embedding_model_dims": 1536,
                    "path": str(STATE_DIR / "qdrant"),
                }
            }
        })
        return m.search(query, user_id=user_id, limit=limit)
    except:
        # Fallback: search local
        path = STATE_DIR / "mem0_fallback.json"
        if not path.exists():
            return []
        memories = json.loads(path.read_text())
        return [m for m in memories if query.lower() in m.get("content", "").lower()][:limit]

# ── FULL BACKUP CYCLE ──
def full_backup():
    """Run a full backup cycle: git + supabase + mem0."""
    results = {
        "timestamp": datetime.utcnow().isoformat(),
        "git": None,
        "supabase": None,
        "mem0": None,
    }
    
    # 1. Git commit + push
    changes = git_status()
    if len(changes) > 0 and changes[0] != "":
        results["git"] = git_commit_push()
    else:
        results["git"] = {"status": "no changes"}
    
    # 2. Supabase backup of critical state
    critical_state = {}
    # Consciousness engine state
    ce_dir = EVEZ_OS / "consciousness_state"
    if ce_dir.exists():
        for f in ce_dir.glob("*.json"):
            try: critical_state[f"consciousness/{f.name}"] = json.loads(f.read_text())
            except: pass
    # Bridge state
    bs = EVEZ_OS / "bridge_state.json"
    if bs.exists():
        try: critical_state["bridge"] = json.loads(bs.read_text())
        except: pass
    # Circuit manifest
    cm = EVEZ_OS / "circuit_manifest.json"
    if cm.exists():
        try: critical_state["circuit_manifest"] = json.loads(cm.read_text())
        except: pass
    
    results["supabase"] = supabase_backup(critical_state, "evez_state")
    
    # 3. mem0 — save key insights
    insights = []
    # Recent monologue
    mono = ce_dir / "monologue.json" if ce_dir.exists() else None
    if mono and mono.exists():
        try:
            thoughts = json.loads(mono.read_text())
            for t in thoughts[-5:]:
                insights.append(t.get("thought", ""))
        except: pass
    
    mem0_results = []
    for insight in insights:
        if insight:
            r = mem0_save(insight, metadata={"source": "consciousness", "type": "thought"})
            mem0_results.append(r)
    results["mem0"] = {"saved": len(mem0_results)}
    
    # Save backup state
    (STATE_DIR / "last_backup.json").write_text(json.dumps(results, indent=2))
    
    return results

# ── HTTP ──
class BackupHandler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _j(self, data, s=200):
        self.send_response(s)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def do_GET(self):
        p = self.path.split("?")[0]
        if p == "/api/health":
            self._j({"status": "READY", "services": ["git", "supabase", "mem0"]})
        elif p == "/api/status":
            lb = STATE_DIR / "last_backup.json"
            last = json.loads(lb.read_text()) if lb.exists() else None
            self._j({"last_backup": last, "git_changes": len(git_status())})
        elif p == "/api/git/status":
            self._j({"changes": git_status()})
        elif p == "/":
            self._j({"service": "EVEZ Backup & Sync", "targets": ["github", "supabase", "mem0"]})
        else:
            self._j({"error": "not found"}, 404)
    
    def do_POST(self):
        p = self.path.split("?")[0]
        l = int(self.headers.get("Content-Length", 0))
        b = json.loads(self.rfile.read(l)) if l > 0 else {}
        
        if p == "/api/backup":
            self._j(full_backup())
        elif p == "/api/git/push":
            self._j(git_commit_push(b.get("message")))
        elif p == "/api/supabase":
            self._j(supabase_backup(b.get("data", {}), b.get("table", "evez_state")))
        elif p == "/api/mem0/save":
            self._j(mem0_save(b.get("content", ""), b.get("user_id", "evez"), b.get("metadata")))
        elif p == "/api/mem0/search":
            self._j({"results": mem0_search(b.get("query", ""), b.get("user_id", "evez"), b.get("limit", 5))})
        else:
            self._j({"error": "not found"}, 404)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=9114)
    args = parser.parse_args()
    s = HTTPServer(("0.0.0.0", args.port), BackupHandler)
    print(f"EVEZ Backup & Sync on :{args.port}")
    s.serve_forever()
