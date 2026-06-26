"""Tests for context-usage.sh script."""

import json
import os
import subprocess
import tempfile
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"


def run_context_usage(transcript_content):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        f.write(transcript_content)
        f.flush()
        result = subprocess.run(
            ["bash", str(SCRIPTS_DIR / "context-usage.sh"), f.name],
            capture_output=True, text=True, timeout=10,
        )
        os.unlink(f.name)
        return result.stdout.strip()


class TestContextUsage:
    def test_extracts_tokens_from_realistic_format(self):
        """Real Claude Code transcripts have usage nested in a large JSON object."""
        # Simulate a realistic final JSONL line with nested usage
        line = json.dumps({
            "type": "assistant",
            "message": {"role": "assistant", "content": "Done."},
            "usage": {
                "input_tokens": 150000,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 120000,
                "output_tokens": 500,
            }
        })
        output = run_context_usage(line + "\n")
        assert "Input tokens: 150000" in output

    def test_filters_streaming_placeholder(self):
        """Streaming entries have input_tokens=1, should be filtered."""
        line = json.dumps({"type": "stream", "usage": {"input_tokens": 1, "output_tokens": 0}})
        output = run_context_usage(line + "\n")
        assert output == ""

    def test_empty_file_no_output(self):
        output = run_context_usage("")
        assert output == ""

    def test_no_usage_field(self):
        line = json.dumps({"type": "message", "content": "hello"})
        output = run_context_usage(line + "\n")
        assert output == ""

    def test_uses_last_line(self):
        """Should read the last line, not intermediate lines."""
        lines = []
        for i in range(50):
            lines.append(json.dumps({"type": "stream", "usage": {"input_tokens": 1, "output_tokens": 0}}))
        # Last line has the real count
        lines.append(json.dumps({"usage": {"input_tokens": 200000, "output_tokens": 1000}}))
        output = run_context_usage("\n".join(lines) + "\n")
        assert "Input tokens: 200000" in output
