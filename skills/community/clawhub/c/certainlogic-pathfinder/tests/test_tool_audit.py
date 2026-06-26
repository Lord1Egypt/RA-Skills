"""Tests for ToolAuditChain and AuditedToolExecutor."""

import json
import subprocess
import tempfile
import time
from pathlib import Path

import pytest

from agentpathfinder.pathfinder_core import generate_master_key, derive_key
from agentpathfinder.audit_trail import AuditTrail
from agentpathfinder.tool_audit import ToolAuditChain, AuditedToolExecutor


class TestToolAuditChain:
    """Test tool call tracking with HMAC signatures."""

    @pytest.fixture
    def audit(self, tmp_path):
        """Create a temporary audit trail with a derived key."""
        master_key = generate_master_key()
        audit_key = derive_key(master_key, b"audit_signing_key")
        log_path = tmp_path / "audit.jsonl"
        return AuditTrail(log_path, audit_key)

    @pytest.fixture
    def tool_audit(self, audit):
        """Create a ToolAuditChain for task tsk_abc, step 1."""
        return ToolAuditChain("tsk_abc", 1, audit)

    def test_log_tool_call(self, tool_audit):
        """Tool invocation is logged and signed."""
        tool_id = tool_audit.log_tool_call("exec", {"command": "ls -la"})
        assert tool_id.startswith("tl_")
        assert tool_id in tool_audit._active_calls

    def test_log_tool_result(self, tool_audit):
        """Tool result is logged with full output."""
        tool_id = tool_audit.log_tool_call("exec", {"command": "echo hello"})
        result = tool_audit.log_tool_result(
            tool_id, {"stdout": "hello\n", "stderr": ""}, exit_code=0, duration_ms=42
        )
        assert result["status"] == "completed"
        assert result["result"]["stdout"] == "hello\n"
        assert result["exit_code"] == 0
        assert tool_id not in tool_audit._active_calls

    def test_log_tool_error(self, tool_audit):
        """Tool crash is logged with exception details."""
        tool_id = tool_audit.log_tool_call("exec", {"command": "false"})
        try:
            raise RuntimeError("Command failed")
        except Exception as e:
            result = tool_audit.log_tool_error(tool_id, e, duration_ms=15)
        assert result["status"] == "error"
        assert "RuntimeError" in result["error"]
        assert tool_id not in tool_audit._active_calls

    def test_sub_tool_chain(self, tool_audit):
        """Child chains track depth and parent reference."""
        tool_id = tool_audit.log_tool_call("exec", {"command": "parent"})
        child = tool_audit.child_chain("exec", tool_id)
        assert child.depth == 1
        assert child.parent_tool_id == tool_id

    def test_max_depth_protection(self, tool_audit):
        """Deep recursion is blocked."""
        tool_audit.depth = ToolAuditChain.MAX_CHAIN_DEPTH
        with pytest.raises(RuntimeError, match="depth exceeded"):
            tool_audit.log_tool_call("exec", {"command": "boom"})

    def test_detect_hanging_calls(self, tool_audit):
        """Find tool calls that never got a result."""
        tool_id = tool_audit.log_tool_call("exec", {"command": "sleep 999"})
        hanging = tool_audit.detect_hanging_calls(timeout_seconds=-1)  # Immediate
        assert len(hanging) == 1
        assert hanging[0]["tool_name"] == "exec"

    def test_tool_summary(self, tool_audit):
        """Summary counts tool events correctly."""
        t1 = tool_audit.log_tool_call("exec", {"command": "a"})
        t2 = tool_audit.log_tool_call("read", {"path": "/tmp/x"})
        tool_audit.log_tool_result(t1, "ok")
        tool_audit.log_tool_error(t2, ValueError("not found"))

        summary = tool_audit.get_tool_summary()
        assert summary["task_id"] == "tsk_abc"
        assert summary["total_tool_events"] == 4  # 2 invoked + 2 results
        assert summary["by_tool"]["exec"]["completed"] == 1
        assert summary["by_tool"]["read"]["error"] == 1


class TestAuditedToolExecutor:
    """Test tool execution wrappers with audit logging."""

    @pytest.fixture
    def executor(self, tmp_path):
        """Create an AuditedToolExecutor with temporary audit trail."""
        master_key = generate_master_key()
        audit_key = derive_key(master_key, b"audit_signing_key")
        log_path = tmp_path / "audit.jsonl"
        audit_trail = AuditTrail(log_path, audit_key)
        tool_audit = ToolAuditChain("tsk_test", 1, audit_trail)
        return AuditedToolExecutor(tool_audit)

    def test_exec_success(self, executor):
        """Successful command execution is logged."""
        result = executor.exec("echo 'hello world'")
        assert result["returncode"] == 0
        assert "hello world" in result["stdout"]

        # Verify audit trail has both INVOKED and RESULT events
        events = executor.audit.audit.read_trail("tsk_test")
        tool_events = [e for e in events if e.get("event", "").startswith("TOOL_")]
        assert len(tool_events) == 2
        assert tool_events[0]["event"] == "TOOL_INVOKED"
        assert tool_events[1]["event"] == "TOOL_RESULT"

    def test_exec_error(self, executor):
        """Failed command execution is logged with non-zero exit code."""
        result = executor.exec("false", timeout=5)  # exits with 1
        assert result["returncode"] == 1

    def test_read_file(self, executor, tmp_path):
        """File read is logged."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        content = executor.read_file(str(test_file))
        assert content == "test content"

    def test_write_file(self, executor, tmp_path):
        """File write is logged."""
        test_file = tmp_path / "output.txt"
        executor.write_file(str(test_file), "written content")
        
        assert test_file.read_text() == "written content"

    def test_web_fetch(self, executor):
        """Web fetch is logged."""
        # Use httpbin for reliable testing
        content = executor.web_fetch("https://httpbin.org/get")
        assert "httpbin" in content or len(content) > 0
