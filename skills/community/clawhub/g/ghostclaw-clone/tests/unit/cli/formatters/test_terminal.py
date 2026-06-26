import pytest
from ghostclaw.cli.formatters import TerminalFormatter
from typing import Dict, Any
import re

@pytest.fixture
def mock_report() -> Dict[str, Any]:
    return {
        "vibe_score": 85,
        "stack": "Python",
        "files_analyzed": 10,
        "total_lines": 500,
        "issues": ["Issue 1"],
        "architectural_ghosts": ["Ghost 1"],
        "red_flags": ["Flag 1"],
        "errors": ["Error 1"],
        "ai_synthesis": "Overall looks fine.",
        "coupling_metrics": {"avg_ccn": 2.5, "avg_nd": 1.5}
    }

def _strip_ansi(s: str) -> str:
    """Remove ANSI escape codes from a string."""
    return re.sub(r'\x1b\[[0-9;]*m', '', s)

def test_terminal_formatter(mock_report):
    formatter = TerminalFormatter()
    result = formatter.format(mock_report)

    stripped = _strip_ansi(result)
    assert "🟢 Vibe Score: 85/100" in stripped
    assert "Stack: Python" in stripped
    assert "Files: 10, Lines: 500" in stripped
    assert "Metrics: Avg CCN: 2.5, Avg Nesting: 1.5" in stripped
    assert "Issue 1" in stripped
    assert "Ghost 1" in stripped
    assert "Flag 1" in stripped
    assert "Error 1" in stripped
    assert "Overall looks fine." in stripped
    assert "💡 Tip: Run with '--patch' to generate refactor suggestions" in stripped

def test_terminal_print(mock_report, capsys):
    formatter = TerminalFormatter()
    formatter.print_to_terminal(mock_report)

    captured = capsys.readouterr()
    stripped = _strip_ansi(captured.out)
    assert "🟢 Vibe Score: 85/100" in stripped
    assert "Stack: Python" in stripped
