"""Tests for post-edit-check.sh PostToolUse hook."""

import json
import os
import subprocess
import tempfile
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"


def run_post_edit(tool_name, file_path="", tool_input=None):
    if tool_input is None:
        tool_input = {"file_path": file_path}
    inp = json.dumps({
        "tool_name": tool_name,
        "tool_input": tool_input,
        "hook_event_name": "PostToolUse",
    })
    result = subprocess.run(
        ["bash", str(SCRIPTS_DIR / "post-edit-check.sh")],
        capture_output=True, text=True, input=inp, timeout=10,
    )
    return result.stdout.strip(), result.returncode


class TestPostEditCheck:
    def test_ignores_non_edit_tools(self):
        """Should exit silently for non-Write/Edit tools."""
        stdout, rc = run_post_edit("Bash", "/tmp/test.py")
        assert rc == 0
        assert stdout == ""

    def test_ignores_read_tool(self):
        stdout, rc = run_post_edit("Read", "/tmp/test.py")
        assert rc == 0
        assert stdout == ""

    def test_handles_missing_file(self):
        """Should exit silently when file doesn't exist."""
        stdout, rc = run_post_edit("Write", "/tmp/nonexistent_file_12345.py")
        assert rc == 0
        assert stdout == ""

    def test_handles_empty_file_path(self):
        stdout, rc = run_post_edit("Write", "")
        assert rc == 0
        assert stdout == ""

    def test_runs_on_write_tool(self):
        """Should trigger for Write tool on a real file (even if no linter found)."""
        with tempfile.NamedTemporaryFile(suffix=".xyz", delete=False, mode='w') as f:
            f.write("test content")
            f.flush()
            stdout, rc = run_post_edit("Write", f.name)
            os.unlink(f.name)
        assert rc == 0
        # Unknown extension — no linter runs, no output
        assert stdout == ""

    def test_runs_on_edit_tool(self):
        """Should trigger for Edit tool."""
        with tempfile.NamedTemporaryFile(suffix=".xyz", delete=False, mode='w') as f:
            f.write("test")
            f.flush()
            stdout, rc = run_post_edit("Edit", f.name, {
                "file_path": f.name,
                "old_string": "a",
                "new_string": "b",
            })
            os.unlink(f.name)
        assert rc == 0

    def test_shell_script_with_shellcheck(self):
        """If shellcheck is installed, should detect issues in .sh files."""
        with tempfile.NamedTemporaryFile(suffix=".sh", delete=False, mode='w') as f:
            f.write("#!/bin/bash\necho $UNQUOTED_VAR\n")
            f.flush()
            stdout, rc = run_post_edit("Write", f.name)
            os.unlink(f.name)
        assert rc == 0
        # If shellcheck is installed, should find issues
        import shutil
        if shutil.which("shellcheck"):
            assert "shellcheck" in stdout.lower() or "hookSpecificOutput" in stdout
