#!/usr/bin/env python3
"""The unified `photos-cleaner` entry point (ROADMAP T1.6)."""

import json
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest
from test_new_scripts import create_full_test_db

ROOT = Path(__file__).resolve().parent.parent
DISPATCHER = ROOT / "photos_cleaner.py"
COMMANDS = sorted(p.stem for p in (ROOT / "scripts").glob("[a-z]*.py"))

sys.path.insert(0, str(ROOT))
import photos_cleaner  # noqa: E402


def cli(*args: str, module: bool = False) -> subprocess.CompletedProcess:
    entry = ["-m", "photos_cleaner"] if module else [str(DISPATCHER)]
    return subprocess.run([sys.executable, *entry, *args], capture_output=True, text=True, cwd=ROOT, timeout=60)


@pytest.fixture(scope="module")
def db(tmp_path_factory) -> str:
    path = tmp_path_factory.mktemp("lib") / "Photos.sqlite"
    target = sqlite3.connect(path)
    create_full_test_db().backup(target)
    target.close()
    return str(path)


def test_help_lists_every_command():
    result = cli("--help")
    assert result.returncode == 0
    listed = re.findall(r"^  ([a-z-]+)\s", result.stdout, re.M)
    assert listed == [c.replace("_", "-") for c in COMMANDS]
    for mutating in ("cleanup-executor", "smart-export"):
        assert re.search(rf"^  {mutating}\s+\(mutating\)", result.stdout, re.M)


def test_no_arguments_is_a_usage_error_with_the_list():
    result = cli()
    assert result.returncode == 2
    assert "commands:" in result.stdout


def test_summaries_match_skill_md():
    rows = dict(re.findall(r"^\| `([a-z_]+)`(?: ⚠️)? \| (.+?) \| [🔴🟠🟡] \|", (ROOT / "SKILL.md").read_text(), re.M))
    assert set(photos_cleaner.SUMMARIES) == set(COMMANDS) == set(rows)
    assert {name: text.replace("'", '"') for name, text in photos_cleaner.SUMMARIES.items()} == {
        name: text.replace("'", '"') for name, text in rows.items()
    }


@pytest.mark.parametrize("command", ["library-analysis", "library_analysis", "library_analysis.py"])
def test_dispatch_matches_running_the_script(db, command):
    via_cli = cli(command, "--db-path", db)
    direct = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "library_analysis.py"), "--db-path", db],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert via_cli.returncode == direct.returncode == 0
    # Identical apart from when it ran; `command` is the same name either way.
    assert {**json.loads(via_cli.stdout), "generated_at": None} == {**json.loads(direct.stdout), "generated_at": None}


def test_module_form(db):
    result = cli("storage-analyzer", "--db-path", db, module=True)
    assert result.returncode == 0
    assert '"by_source"' in result.stdout


def test_exit_codes_pass_through(tmp_path):
    assert cli("library-analysis", "--db-path", str(tmp_path / "missing.sqlite")).returncode == 3
    assert cli("library-analysis", "--no-such-flag").returncode == 2


def test_unknown_command_suggests():
    result = cli("junk-findr")
    assert result.returncode == 2
    assert "Did you mean: junk-finder?" in result.stderr


def test_command_help_uses_the_cli_name():
    result = cli("scene-search", "--help")
    assert result.returncode == 0
    assert result.stdout.startswith("usage: photos-cleaner scene-search")


def test_commands_dir_requires_our_scripts(tmp_path, monkeypatch):
    """An unrelated scripts/ beside an installed copy must not be mistaken for ours."""
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "unrelated.py").write_text("")
    monkeypatch.setattr(photos_cleaner, "__file__", str(tmp_path / "photos_cleaner.py"))
    monkeypatch.setattr(photos_cleaner.importlib.util, "find_spec", lambda name: None)
    with pytest.raises(SystemExit, match="can't find its commands"):
        photos_cleaner.commands_dir()


def test_dispatcher_defers_annotations_for_old_pythons():
    """On 3.9, `list[str] | None` in a signature raises at def time, before _bootstrap can explain.

    CI has no 3.9; this pins the guard. (Verified by hand on 3.9.25: TypeError without it,
    the upgrade message with it.)
    """
    import ast

    tree = ast.parse(DISPATCHER.read_text(encoding="utf-8"))
    imports = [node for node in tree.body if isinstance(node, ast.ImportFrom) and node.module == "__future__"]
    assert any(alias.name == "annotations" for node in imports for alias in node.names)
