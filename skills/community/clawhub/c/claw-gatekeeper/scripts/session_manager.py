#!/usr/bin/env python3
"""
Claw-Gatekeeper Session Manager
Manages session-level permissions and state for risk-based auto-approval

Features:
- Session-level auto-approval for MEDIUM/HIGH risks after user confirmation
- Per-operation-type session permissions
- Session timeout handling
- Persistent session state across OpenClaw interactions
"""

import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Set, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum


class SessionPermission(Enum):
    """Types of session permissions"""
    ONCE = "once"           # Single approval
    SESSION = "session"     # Valid for entire session
    ALWAYS = "always"       # Whitelist (persistent)
    NEVER = "never"         # Blacklist (persistent)


@dataclass
class SessionApproval:
    """Session-level approval entry"""
    operation_type: str
    risk_level: str
    operation_pattern: str
    approved_at: str
    expires_at: Optional[str] = None
    approval_type: str = "session"  # session, once, always


class SessionManager:
    """Manages session-level approvals and state"""
    
    # Session timeout (default: 30 minutes of inactivity)
    DEFAULT_SESSION_TIMEOUT = 1800  # seconds
    
    # Risk levels that support session-level auto-approval
    SESSION_APPROVAL_RISKS = ["MEDIUM", "HIGH"]
    
    # CRITICAL always requires per-confirmation
    ALWAYS_CONFIRM_RISKS = ["CRITICAL"]
    
    def __init__(self, session_dir: Optional[str] = None, 
                 timeout: int = DEFAULT_SESSION_TIMEOUT):
        self.session_dir = Path(session_dir) if session_dir else \
                          Path.home() / ".claw-gatekeeper" / "sessions"
        self.session_dir.mkdir(parents=True, exist_ok=True)
        
        self.timeout = timeout
        self.session_file = self.session_dir / "current_session.json"
        self.audit_log_file = self.session_dir / "Operate_Audit.log"
        
        # In-memory session state
        self._session_approvals: Dict[str, SessionApproval] = {}
        self._session_start_time: Optional[str] = None
        self._last_activity: Optional[str] = None
        
        # Load or initialize session
        self._load_session()
    
    def _load_session(self):
        """Load existing session or create new one"""
        if self.session_file.exists():
            try:
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Check if session is still valid
                last_activity = data.get('last_activity')
                if last_activity:
                    last_time = datetime.fromisoformat(last_activity)
                    if datetime.now() - last_time < timedelta(seconds=self.timeout):
                        # Session still valid, restore it
                        self._session_start_time = data.get('session_start')
                        self._last_activity = last_activity
                        
                        # Restore approvals
                        for key, approval_data in data.get('approvals', {}).items():
                            self._session_approvals[key] = SessionApproval(**approval_data)
                        
                        return
            except Exception as e:
                print(f"Warning: Could not load session: {e}", file=os.sys.stderr)
        
        # Create new session
        self._init_new_session()
    
    def _init_new_session(self):
        """Initialize a new session"""
        self._session_start_time = datetime.now().isoformat()
        self._last_activity = self._session_start_time
        self._session_approvals = {}
        self._save_session()
    
    def _save_session(self):
        """Save current session state to file"""
        data = {
            "session_start": self._session_start_time,
            "last_activity": self._last_activity,
            "approvals": {
                key: asdict(approval) 
                for key, approval in self._session_approvals.items()
            }
        }
        
        try:
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save session: {e}", file=os.sys.stderr)
    
    def _update_activity(self):
        """Update last activity timestamp"""
        self._last_activity = datetime.now().isoformat()
        self._save_session()
    
    def _get_approval_key(self, operation_type: str, risk_level: str, 
                          operation_detail: str) -> str:
        """Generate unique key for an operation pattern"""
        # Normalize operation detail for pattern matching
        # Extract key identifying features
        if operation_type == "file":
            # For files, use directory path as pattern
            path_parts = operation_detail.split()
            if path_parts:
                path = path_parts[-1] if len(path_parts) > 1 else operation_detail
                path = os.path.expanduser(path)
                return f"{operation_type}:{risk_level}:{os.path.dirname(path)}"
        
        elif operation_type == "shell":
            # For shell, use first command as pattern
            cmd_parts = operation_detail.split()
            if cmd_parts:
                return f"{operation_type}:{risk_level}:{cmd_parts[0]}"
        
        elif operation_type == "network":
            # For network, use domain as pattern
            if "//" in operation_detail:
                domain = operation_detail.split("//")[-1].split("/")[0]
                return f"{operation_type}:{risk_level}:{domain}"
        
        elif operation_type == "skill":
            # For skills, use skill name
            if " " in operation_detail:
                skill_name = operation_detail.split()[0]
                return f"{operation_type}:{risk_level}:{skill_name}"
        
        # Default: use full detail (hashed for brevity)
        import hashlib
        detail_hash = hashlib.md5(operation_detail.encode()).hexdigest()[:8]
        return f"{operation_type}:{risk_level}:{detail_hash}"
    
    def check_session_permission(self, operation_type: str, risk_level: str,
                                  operation_detail: str) -> Tuple[bool, str]:
        """
        Check if operation is allowed by current session permissions
        
        Returns:
            (is_allowed, reason)
        """
        self._update_activity()
        
        # LOW risk: always allow
        if risk_level == "LOW":
            return True, "LOW risk - auto-allowed"
        
        # CRITICAL risk: always require confirmation
        if risk_level in self.ALWAYS_CONFIRM_RISKS:
            return False, "CRITICAL risk - always requires confirmation"
        
        # MEDIUM/HIGH: check session approval
        if risk_level in self.SESSION_APPROVAL_RISKS:
            key = self._get_approval_key(operation_type, risk_level, operation_detail)
            
            if key in self._session_approvals:
                approval = self._session_approvals[key]
                
                # Check if expired
                if approval.expires_at:
                    expires = datetime.fromisoformat(approval.expires_at)
                    if datetime.now() > expires:
                        del self._session_approvals[key]
                        self._save_session()
                        return False, f"{risk_level} risk - session approval expired"
                
                return True, f"{risk_level} risk - approved for this session"
        
        return False, f"{risk_level} risk - requires confirmation"
    
    def grant_session_approval(self, operation_type: str, risk_level: str,
                               operation_detail: str, 
                               approval_type: str = "session") -> bool:
        """
        Grant session-level approval for an operation pattern
        
        Args:
            operation_type: Type of operation (file, shell, network, skill)
            risk_level: Risk level (MEDIUM, HIGH)
            operation_detail: Operation details
            approval_type: "session" for session-level, "once" for single use
        """
        if risk_level not in self.SESSION_APPROVAL_RISKS:
            return False
        
        key = self._get_approval_key(operation_type, risk_level, operation_detail)
        
        now = datetime.now()
        
        if approval_type == "session":
            # Session-level approval - expires when session expires
            expires = None
        elif approval_type == "once":
            # Single use - technically not stored in session
            return True
        else:
            return False
        
        approval = SessionApproval(
            operation_type=operation_type,
            risk_level=risk_level,
            operation_pattern=operation_detail[:100],
            approved_at=now.isoformat(),
            expires_at=expires.isoformat() if expires else None,
            approval_type=approval_type
        )
        
        self._session_approvals[key] = approval
        self._update_activity()
        
        return True
    
    def revoke_session_approval(self, operation_type: str = None, 
                                risk_level: str = None) -> int:
        """
        Revoke session approvals
        
        Args:
            operation_type: If specified, only revoke for this type
            risk_level: If specified, only revoke for this level
            
        Returns:
            Number of approvals revoked
        """
        to_remove = []
        
        for key, approval in self._session_approvals.items():
            match = True
            if operation_type and approval.operation_type != operation_type:
                match = False
            if risk_level and approval.risk_level != risk_level:
                match = False
            
            if match:
                to_remove.append(key)
        
        for key in to_remove:
            del self._session_approvals[key]
        
        self._update_activity()
        
        return len(to_remove)
    
    def clear_session(self):
        """Clear all session state and start fresh"""
        self._init_new_session()
    
    def get_session_info(self) -> Dict[str, Any]:
        """Get current session information"""
        return {
            "session_start": self._session_start_time,
            "last_activity": self._last_activity,
            "active_approvals": len(self._session_approvals),
            "approvals": [
                {
                    "type": a.operation_type,
                    "risk": a.risk_level,
                    "pattern": a.operation_pattern,
                    "approved_at": a.approved_at
                }
                for a in self._session_approvals.values()
            ]
        }
    
    def write_audit_log(self, entry: Dict[str, Any]):
        """
        Write entry to Operate_Audit.log with timestamp and emoji
        Format: [TIMESTAMP] [EMOJI LEVEL] [TYPE] DECISION: Details
        """
        # Risk level to emoji mapping
        RISK_EMOJIS = {
            "CRITICAL": "🔴",
            "HIGH": "🟠",
            "MEDIUM": "🟡",
            "LOW": "🟢",
            "UNKNOWN": "⚪"
        }
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        risk_level = entry.get('risk_level', 'UNKNOWN')
        operation_type = entry.get('operation_type', 'UNKNOWN')
        operation_detail = entry.get('operation_detail', '')
        decision = entry.get('decision', 'UNKNOWN')
        
        # Only log MEDIUM and above
        if risk_level == "LOW":
            return
        
        # Get emoji for risk level
        emoji = RISK_EMOJIS.get(risk_level, "⚪")
        
        # Format with emoji: [TIMESTAMP] [EMOJI LEVEL] [TYPE] DECISION: Details
        log_line = f"[{timestamp}] [{emoji} {risk_level}] [{operation_type}] {decision}: {operation_detail}\n"
        
        try:
            with open(self.audit_log_file, 'a', encoding='utf-8') as f:
                f.write(log_line)
        except Exception as e:
            print(f"Warning: Could not write to audit log: {e}", file=os.sys.stderr)
    
    def read_audit_log(self, lines: int = 100) -> list:
        """Read recent entries from Operate_Audit.log"""
        if not self.audit_log_file.exists():
            return []
        
        try:
            with open(self.audit_log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                return all_lines[-lines:]
        except Exception as e:
            print(f"Warning: Could not read audit log: {e}", file=os.sys.stderr)
            return []


def main():
    """Command-line interface for session management"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Claw-Guardian Session Manager")
    parser.add_argument("command", choices=[
        "info", "clear", "list", "revoke", "check"
    ])
    parser.add_argument("--type", help="Operation type filter")
    parser.add_argument("--risk", help="Risk level filter")
    parser.add_argument("--lines", type=int, default=50, help="Lines to show")
    
    args = parser.parse_args()
    
    manager = SessionManager()
    
    if args.command == "info":
        info = manager.get_session_info()
        print(json.dumps(info, indent=2))
    
    elif args.command == "clear":
        manager.clear_session()
        print("Session cleared. New session started.")
    
    elif args.command == "list":
        info = manager.get_session_info()
        print(f"Session started: {info['session_start']}")
        print(f"Last activity: {info['last_activity']}")
        print(f"Active approvals: {info['active_approvals']}")
        print()
        for approval in info['approvals']:
            print(f"  [{approval['risk']}] {approval['type']}: {approval['pattern']}")
    
    elif args.command == "revoke":
        count = manager.revoke_session_approval(args.type, args.risk)
        print(f"Revoked {count} session approval(s)")
    
    elif args.command == "check":
        lines = manager.read_audit_log(args.lines)
        for line in lines:
            print(line, end='')
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
