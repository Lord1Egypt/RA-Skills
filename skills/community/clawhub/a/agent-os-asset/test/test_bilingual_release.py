"""Bilingual publication contract for shipped Agent Skill content."""

from __future__ import annotations

from pathlib import Path
import re
import subprocess


REPO_ROOT = Path(__file__).resolve().parents[1]
HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
ENGLISH = re.compile(r"[A-Za-z]{2,}")
SCANNED_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json"}
ROOT_MARKDOWN_FILES = ("SKILL.md", "README.md", "AGENTS.md")


def _published_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    paths = []
    for value in result.stdout.splitlines():
        path = REPO_ROOT / value
        if not path.is_file() or path.suffix not in SCANNED_SUFFIXES:
            continue
        if value.startswith("test/") or value.startswith(".github/"):
            continue
        paths.append(path)
    return paths


def _is_bilingual_line(line: str, previous: str) -> bool:
    stripped = line.strip()
    previous = previous.strip()
    if "bilingual-compat:" in line and ENGLISH.search(line):
        return True
    if "bilingual-compat:" in previous and ENGLISH.search(previous):
        return True
    if stripped.startswith("ZH-CN:") and previous.startswith("EN:"):
        return bool(ENGLISH.search(previous))
    if " / " in line and ENGLISH.search(line):
        english = ENGLISH.search(line)
        chinese = HAN.search(line)
        separator = line.find(" / ")
        return bool(english and chinese and english.start() < separator < chinese.start())
    return False


def test_all_published_chinese_has_an_english_pair() -> None:
    failures: list[str] = []
    for path in _published_files():
        previous_nonblank = ""
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if HAN.search(line) and not _is_bilingual_line(line, previous_nonblank):
                failures.append(f"{path.relative_to(REPO_ROOT)}:{number}: {line.strip()}")
            if line.strip():
                previous_nonblank = line
    assert not failures, "Unpaired Chinese publication text:\n" + "\n".join(failures)


def test_root_skill_declares_bilingual_policy() -> None:
    text = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert "English is normative" in text
    assert "ZH-CN" in text


def test_root_markdown_declares_english_normative_bilingual_content() -> None:
    for name in ROOT_MARKDOWN_FILES:
        text = (REPO_ROOT / name).read_text(encoding="utf-8")
        assert "English is normative" in text, name
        assert "ZH-CN:" in text or " / " in text, name


def test_root_python_user_facing_labels_are_bilingual() -> None:
    workbench = (REPO_ROOT / "scripts" / "review_workbench.py").read_text(
        encoding="utf-8"
    )
    for label in (
        "Filters / 筛选",
        "Status / 状态",
        "Suggestion / 建议",
        "Select all / 全选",
        "Download decisions.json / 下载 decisions.json",
        "Open / 打开",
        "Copy / 复制",
    ):
        assert label in workbench

    auto_sync = (REPO_ROOT / "scripts" / "auto_sync.py").read_text(
        encoding="utf-8"
    )
    assert "Sync failed / 同步失败" in auto_sync
    assert "Added / 新增" in auto_sync

    code_adapter = (REPO_ROOT / "scripts" / "code_repo_adapter.py").read_text(
        encoding="utf-8"
    )
    assert "## Summary / 摘要" in code_adapter
    assert "No. / 编号" in code_adapter

    mixed_adapter = (REPO_ROOT / "scripts" / "mixed_folder_adapter.py").read_text(
        encoding="utf-8"
    )
    assert "## Summary / 摘要" in mixed_adapter
    assert "Data bundle / 数据 bundle" in mixed_adapter
