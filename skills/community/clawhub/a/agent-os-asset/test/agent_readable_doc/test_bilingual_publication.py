"""Focused bilingual publication contract for agent-readable-doc."""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys

from support import SKILL_ROOT


HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
ENGLISH = re.compile(r"[A-Za-z]{2,}")
SCANNED_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json"}


def is_bilingual_line(line: str, previous: str) -> bool:
    stripped = line.strip()
    previous = previous.strip()
    if "bilingual-compat:" in line and ENGLISH.search(line):
        return True
    if "bilingual-compat:" in previous and ENGLISH.search(previous):
        return True
    if stripped.startswith("ZH-CN:") and previous.startswith("EN:"):
        return bool(ENGLISH.search(previous))
    if " / " in line and ENGLISH.search(line):
        return True
    return False


def test_every_published_chinese_line_has_an_english_pair() -> None:
    failures: list[str] = []
    for path in sorted(SKILL_ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SCANNED_SUFFIXES:
            continue
        previous_nonblank = ""
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if HAN.search(line) and not is_bilingual_line(line, previous_nonblank):
                failures.append(f"{path.relative_to(SKILL_ROOT)}:{number}: {line.strip()}")
            if line.strip():
                previous_nonblank = line
    assert not failures, "Unpaired Chinese publication text:\n" + "\n".join(failures)


def test_skill_declares_normative_language_and_bilingual_metadata() -> None:
    skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    metadata = (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")

    assert "English is normative" in skill
    assert "ZH-CN:" in skill
    assert 'display_name: "Agent Readable Doc / Agent 可读文档"' in metadata
    assert "EN:" in metadata
    assert "ZH-CN:" in metadata


def test_cli_help_is_bilingual() -> None:
    for script_name in ("archive_sources.py", "extract_sources.py", "validate_agent_doc.py"):
        result = subprocess.run(
            [sys.executable, str(SKILL_ROOT / "scripts" / script_name), "--help"],
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr
        assert " / " in result.stdout
        assert HAN.search(result.stdout)
