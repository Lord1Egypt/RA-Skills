"""AgentPathfinder v2 — Tool Chain Audit Extension

Cryptographically signs every tool call and result as part of the audit trail.
Designed for company brain deployments where every agent action must be auditable.

Features:
- Tool invocation logging with full args/results (not hashed)
- Sub-tool chain tracking with depth limits
- Crash recovery for stuck tool calls
- Integration hooks for exec/browser/file operations
"""

import json
import time
import uuid
from pathlib import Path
from typing import Dict, Any, Optional, List

from .audit_trail import AuditTrail
from .pathfinder_core import hmac_sign


class ToolAuditChain:
    """Tracks tool invocations within a task's audit trail.
    
    Each tool call and result is HMAC-signed by the task's audit key.
    Sub-tool chains are tracked via parent references up to max_depth.
    """

    # Maximum depth for sub-tool chaining
    MAX_CHAIN_DEPTH = 50
    
    # Tool categories for filtering/reporting
    CATEGORIES = {
        "exec": "system_command",
        "system": "system_command",
        "browser": "web_automation",
        "web_fetch": "web_automation",
        "read": "filesystem",
        "write": "filesystem",
        "edit": "filesystem",
        "exec": "filesystem",  # file operations via exec
        "message": "communication",
        "cron": "scheduling",
        "gateway": "infrastructure",
        "nodes": "device_control",
        "canvas": "visualization",
        "subagents": "orchestration",
        "sessions_send": "orchestration",
    }

    def __init__(self, task_id: str, step_number: int, audit_trail: AuditTrail,
                 parent_tool_id: Optional[str] = None, depth: int = 0):
        self.task_id = task_id
        self.step_number = step_number
        self.audit = audit_trail
        self.parent_tool_id = parent_tool_id
        self.depth = depth
        self._active_calls: Dict[str, Dict[str, Any]] = {}  # tool_id -> call info

    # ------------------------------------------------------------------
    # Core tool call logging
    # ------------------------------------------------------------------
    def log_tool_call(self, tool_name: str, args: Dict[str, Any],
                      tool_id: Optional[str] = None) -> str:
        """Log a tool invocation with full arguments.
        
        Returns the tool_id for correlating with the result.
        """
        if self.depth >= self.MAX_CHAIN_DEPTH:
            raise RuntimeError(
                f"Tool chain depth exceeded {self.MAX_CHAIN_DEPTH} — "
                "possible infinite recursion"
            )

        tool_id = tool_id or f"tl_{uuid.uuid4().hex[:12]}"
        
        # Categorize for filtering
        category = self.CATEGORIES.get(tool_name, "uncategorized")

        call_record = {
            "tool_id": tool_id,
            "tool_name": tool_name,
            "category": category,
            "step_number": self.step_number,
            "depth": self.depth,
            "parent_tool_id": self.parent_tool_id,
            "args": args,  # Full args, not hashed (company brain use case)
            "status": "invoked",
            "timestamp_invoked": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }

        self._active_calls[tool_id] = call_record

        self.audit.log(
            "TOOL_INVOKED",
            self.task_id,
            step_number=self.step_number,
            tool_id=tool_id,
            tool_name=tool_name,
            category=category,
            depth=self.depth,
            parent_tool_id=self.parent_tool_id,
            args=args,
        )

        return tool_id

    def log_tool_result(self, tool_id: str, result: Any,
                        exit_code: int = 0, duration_ms: Optional[int] = None,
                        error: Optional[str] = None) -> Dict[str, Any]:
        """Log a tool result with full output.
        
        If tool crashed (error set), logs error details instead of result.
        """
        if tool_id not in self._active_calls:
            raise ValueError(f"Tool {tool_id} was not logged as invoked")

        call_record = self._active_calls[tool_id]
        call_record["status"] = "error" if error else "completed"
        call_record["timestamp_completed"] = time.strftime(
            "%Y-%m-%dT%H:%M:%SZ", time.gmtime()
        )
        call_record["exit_code"] = exit_code
        call_record["duration_ms"] = duration_ms

        if error:
            call_record["error"] = error
            call_record["result"] = None
        else:
            call_record["result"] = result  # Full result, not hashed

        self.audit.log(
            "TOOL_RESULT",
            self.task_id,
            step_number=self.step_number,
            tool_id=tool_id,
            tool_name=call_record["tool_name"],
            status=call_record["status"],
            exit_code=exit_code,
            duration_ms=duration_ms,
            result=None if error else result,
            error=error,
        )

        del self._active_calls[tool_id]
        return call_record

    def log_tool_error(self, tool_id: str, exception: BaseException,
                       duration_ms: Optional[int] = None) -> Dict[str, Any]:
        """Convenience: log a tool crash."""
        return self.log_tool_result(
            tool_id=tool_id,
            result=None,
            exit_code=-1,
            duration_ms=duration_ms,
            error=f"{type(exception).__name__}: {str(exception)[:500]}"
        )

    # ------------------------------------------------------------------
    # Sub-tool chaining
    # ------------------------------------------------------------------
    def child_chain(self, tool_name: str, tool_id: str) -> "ToolAuditChain":
        """Create a child chain for a sub-tool invocation.
        
        Example: exec calls browser internally → child chain.
        """
        return ToolAuditChain(
            task_id=self.task_id,
            step_number=self.step_number,
            audit_trail=self.audit,
            parent_tool_id=tool_id,
            depth=self.depth + 1,
        )

    # ------------------------------------------------------------------
    # Status & recovery
    # ------------------------------------------------------------------
    def get_active_calls(self) -> List[Dict[str, Any]]:
        """Return tools currently in 'invoked' state (not yet completed).
        Useful for crash recovery — find calls that never got a result."""
        return list(self._active_calls.values())

    def detect_hanging_calls(self, timeout_seconds: int = 300) -> List[Dict[str, Any]]:
        """Find tool calls that have been 'invoked' longer than timeout."""
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).timestamp()
        hanging = []
        for call in self._active_calls.values():
            # Parse ISO timestamp with Z suffix
            ts = call["timestamp_invoked"].replace("Z", "+00:00")
            invoked_epoch = datetime.fromisoformat(ts).timestamp()
            if now - invoked_epoch > timeout_seconds:
                hanging.append(call)
        return hanging

    def force_complete(self, tool_id: str, reason: str = "timeout") -> None:
        """Force-complete a hanging tool call (admin recovery)."""
        if tool_id in self._active_calls:
            self.log_tool_result(
                tool_id=tool_id,
                result=None,
                exit_code=-2,
                error=f"Force-completed after {reason}"
            )

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------
    def get_tool_summary(self) -> Dict[str, Any]:
        """Summary of all tool activity in this chain."""
        events = self.audit.read_trail(self.task_id)
        tool_events = [e for e in events if e.get("event", "").startswith("TOOL_")]
        
        by_name = {}
        for e in tool_events:
            name = e.get("tool_name", "unknown")
            by_name.setdefault(name, {"invoked": 0, "completed": 0, "error": 0})
            if e["event"] == "TOOL_INVOKED":
                by_name[name]["invoked"] += 1
            elif e["event"] == "TOOL_RESULT":
                status = e.get("status", "completed")
                by_name[name]["error"] += 1 if status == "error" else 0
                by_name[name]["completed"] += 1 if status == "completed" else 0

        return {
            "task_id": self.task_id,
            "step_number": self.step_number,
            "total_tool_events": len(tool_events),
            "by_tool": by_name,
            "active_calls": len(self._active_calls),
            "depth": self.depth,
        }


# ------------------------------------------------------------------
# Integration helpers (wrap OpenClaw tools)
# ------------------------------------------------------------------

class AuditedToolExecutor:
    """Wrapper that adds audit logging around actual tool executions.
    
    Usage:
        audit = TaskEngine(...).get_tool_audit(task_id, step_number)
        executor = AuditedToolExecutor(audit)
        result = executor.exec("curl -s http://api/health")
    """

    def __init__(self, tool_audit: ToolAuditChain):
        self.audit = tool_audit

    def exec(self, command: str, timeout: Optional[int] = None) -> Dict[str, Any]:
        """Execute shell command with full audit logging."""
        tool_id = self.audit.log_tool_call("exec", {
            "command": command,
            "timeout": timeout,
        })
        
        start = time.time()
        try:
            import subprocess
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True,
                timeout=timeout
            )
            duration_ms = int((time.time() - start) * 1000)
            
            self.audit.log_tool_result(
                tool_id=tool_id,
                result={
                    "stdout": result.stdout[:10000],  # Truncate very large output
                    "stderr": result.stderr[:5000],
                    "returncode": result.returncode,
                },
                exit_code=result.returncode,
                duration_ms=duration_ms,
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except Exception as e:
            duration_ms = int((time.time() - start) * 1000)
            self.audit.log_tool_error(tool_id, e, duration_ms)
            raise

    def web_fetch(self, url: str, max_chars: int = 5000) -> str:
        """Fetch URL with audit logging."""
        tool_id = self.audit.log_tool_call("web_fetch", {
            "url": url,
            "max_chars": max_chars,
        })
        
        start = time.time()
        try:
            import urllib.request
            with urllib.request.urlopen(url, timeout=30) as response:
                content = response.read().decode("utf-8", errors="ignore")[:max_chars]
            
            duration_ms = int((time.time() - start) * 1000)
            self.audit.log_tool_result(
                tool_id=tool_id,
                result={"content_length": len(content), "status": response.status},
                exit_code=0,
                duration_ms=duration_ms,
            )
            return content
        except Exception as e:
            duration_ms = int((time.time() - start) * 1000)
            self.audit.log_tool_error(tool_id, e, duration_ms)
            raise

    def read_file(self, path: str) -> str:
        """Read file with audit logging."""
        tool_id = self.audit.log_tool_call("read_file", {"path": path})
        
        start = time.time()
        try:
            content = Path(path).read_text(encoding="utf-8", errors="ignore")
            duration_ms = int((time.time() - start) * 1000)
            
            self.audit.log_tool_result(
                tool_id=tool_id,
                result={"content_length": len(content), "path": path},
                exit_code=0,
                duration_ms=duration_ms,
            )
            return content
        except Exception as e:
            duration_ms = int((time.time() - start) * 1000)
            self.audit.log_tool_error(tool_id, e, duration_ms)
            raise

    def write_file(self, path: str, content: str) -> None:
        """Write file with audit logging."""
        tool_id = self.audit.log_tool_call("write_file", {
            "path": path,
            "content_length": len(content),
        })
        
        start = time.time()
        try:
            Path(path).write_text(content, encoding="utf-8")
            duration_ms = int((time.time() - start) * 1000)
            
            self.audit.log_tool_result(
                tool_id=tool_id,
                result={"bytes_written": len(content), "path": path},
                exit_code=0,
                duration_ms=duration_ms,
            )
        except Exception as e:
            duration_ms = int((time.time() - start) * 1000)
            self.audit.log_tool_error(tool_id, e, duration_ms)
            raise
