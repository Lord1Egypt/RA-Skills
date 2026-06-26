"""
tests/test_skill_md_sync.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Regression tests for scripts/check_skill_md_sync.py.

1. Running against the real repo exits 0 (code + docs in sync).
2. Synthetic: adding a fake @mcp.tool that's absent from SKILL.md → exits 1.
3. Synthetic: adding a fake tool entry to SKILL.md absent from code → exits 1.
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SCRIPT = REPO_ROOT / "scripts" / "check_skill_md_sync.py"


def _run(cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
        cwd=cwd,
    )


# ---------------------------------------------------------------------------
# 1. Real repo must be in sync
# ---------------------------------------------------------------------------


def test_real_repo_is_in_sync():
    """scripts/check_skill_md_sync.py exits 0 on the current repo."""
    result = _run(REPO_ROOT)
    assert result.returncode == 0, (
        "SKILL.md is out of sync with server/main.py!\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )
    assert "OK" in result.stdout


# ---------------------------------------------------------------------------
# Helper: build a minimal fake repo tree in tmp_path
# ---------------------------------------------------------------------------


def _make_fake_repo(tmp_path: Path, extra_code_tool: str = "", extra_doc_tool: str = "") -> Path:
    """
    Create a stripped-down repo with:
      - server/main.py  — one real @mcp.tool (real_tool) + optional extra
      - SKILL.md        — documents real_tool + optional extra
    Returns tmp_path.
    """
    server_dir = tmp_path / "server"
    server_dir.mkdir(parents=True)

    extra_code_block = ""
    if extra_code_tool:
        extra_code_block = f"\n@mcp.tool\ndef {extra_code_tool}() -> dict:\n    return {{}}\n"

    # Build main.py without textwrap.dedent so embedded extra_code_block
    # (which has no leading indent) does not confuse the common-prefix calc.
    main_py_lines = [
        "class _MCP:",
        "    @staticmethod",
        "    def tool(fn=None):",
        "        if fn is None:",
        "            return lambda f: f",
        "        return fn",
        "",
        "mcp = _MCP()",
        "",
        "@mcp.tool",
        "def real_tool() -> dict:",
        "    return {}",
    ]
    main_py_content = "\n".join(main_py_lines) + "\n" + extra_code_block
    (server_dir / "main.py").write_text(main_py_content, encoding="utf-8")

    extra_doc_line = ""
    if extra_doc_tool:
        extra_doc_line = f"- `{extra_doc_tool}` — a phantom tool\n"

    skill_md_content = (
        "---\n"
        "name: test-skill\n"
        "description: test\n"
        "---\n"
        "## Available MCP Tools\n"
        "- `real_tool` — does the real thing\n" + extra_doc_line
    )
    (tmp_path / "SKILL.md").write_text(skill_md_content, encoding="utf-8")

    # Copy the script into scripts/
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "check_skill_md_sync.py").write_text(
        SCRIPT.read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    return tmp_path


# ---------------------------------------------------------------------------
# 2. Fake @mcp.tool not in SKILL.md → exits 1
# ---------------------------------------------------------------------------


def test_missing_from_skill_md_fails(tmp_path):
    """A tool in code but absent from SKILL.md must be flagged (exit 1)."""
    repo = _make_fake_repo(tmp_path, extra_code_tool="undocumented_tool")
    result = _run(repo)
    assert result.returncode == 1, "Expected exit 1 when code has undocumented tool"
    assert "undocumented_tool" in result.stdout


# ---------------------------------------------------------------------------
# 3. Fake SKILL.md entry not in code → exits 1
# ---------------------------------------------------------------------------


def test_missing_from_code_fails(tmp_path):
    """A tool documented in SKILL.md but absent from code must be flagged (exit 1)."""
    repo = _make_fake_repo(tmp_path, extra_doc_tool="phantom_tool")
    result = _run(repo)
    assert result.returncode == 1, "Expected exit 1 when SKILL.md documents a ghost tool"
    assert "phantom_tool" in result.stdout


# ---------------------------------------------------------------------------
# 4. Synthetic in-sync repo exits 0
# ---------------------------------------------------------------------------


def test_synthetic_in_sync_passes(tmp_path):
    """A minimal synthetic repo with code and docs in sync exits 0."""
    repo = _make_fake_repo(tmp_path)
    result = _run(repo)
    assert (
        result.returncode == 0
    ), f"Expected exit 0 for in-sync repo.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    assert "OK" in result.stdout
