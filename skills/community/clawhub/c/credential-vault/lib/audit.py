"""Audit logging for credential access."""
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any


DEFAULT_AUDIT_LOG = Path.home() / ".openclaw" / "vault" / "audit.log"


class AuditLogger:
    """Logs credential access events."""
    
    def __init__(self, log_file: Optional[Path] = None):
        self.log_file = log_file or DEFAULT_AUDIT_LOG
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log(self, action: str, key_name: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Log a credential access event.
        
        Args:
            action: Action performed (get, add, remove, etc.)
            key_name: Name of the credential (NOT the value!)
            details: Optional additional details
        
        Note:
            NEVER log the actual credential value!
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "key_name": key_name,
            "details": details or {}
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def read(self, last: int = 100) -> List[Dict[str, Any]]:
        """Read recent audit log entries.
        
        Args:
            last: Number of recent entries to return
        
        Returns:
            List of log entries
        """
        if not self.log_file.exists():
            return []
        
        entries = []
        with open(self.log_file, 'r') as f:
            for line in f:
                try:
                    entries.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue  # Skip malformed lines
        
        return entries[-last:]
