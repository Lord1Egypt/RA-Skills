"""
Audit Logger - 结构化操作审计
每一次操作都被记录，不可篡改
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

class AuditLogger:
    def __init__(self, log_dir: str = None):
        self.log_dir = log_dir or "/root/.openclaw/workspace/auto-company/projects/auto-claw/logs"
        Path(self.log_dir).mkdir(parents=True, exist_ok=True)
        self.log_file = Path(self.log_dir) / f"audit_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    
    def log(self, module: str, action: str, actor: str = "system", details: dict = None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "module": module,
            "action": action,
            "actor": actor,
            "details": details or {}
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
        return entry
    
    def query(self, module: str = None, action: str = None, limit: int = 100):
        entries = []
        if not self.log_file.exists():
            return entries
        with open(self.log_file) as f:
            for line in f:
                entry = json.loads(line)
                if module and entry.get("module") != module:
                    continue
                if action and entry.get("action") != action:
                    continue
                entries.append(entry)
        return entries[-limit:]
