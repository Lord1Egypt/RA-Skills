from __future__ import annotations

from pathlib import Path
import re

from support import SKILL_ROOT


def test_skill_frontmatter_is_public_release() -> None:
    text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    frontmatter = text.split("---", 2)[1]

    assert "user-invocable:" not in frontmatter
    assert re.search(r"(?m)^metadata:\s*$", frontmatter)
    assert re.search(r'(?m)^\s+version:\s*["\']?0\.2\.0["\']?\s*$', frontmatter)


def test_child_skill_has_no_personal_paths() -> None:
    personal_path = re.compile(r"(?:/" + r"Users/[^/\s]+|/" + r"home/[^/\s]+|~/(?:\.|Library/|Documents/))")
    text_files = [
        path
        for path in SKILL_ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".py", ".yaml", ".yml", ".json"}
    ]

    offenders = [str(path.relative_to(SKILL_ROOT)) for path in text_files if personal_path.search(path.read_text(encoding="utf-8"))]
    assert offenders == []


def test_skill_documents_archive_as_preview_then_execute() -> None:
    skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    workflow_text = (SKILL_ROOT / "references" / "conversion-workflow.md").read_text(encoding="utf-8")

    for text in (skill_text, workflow_text):
        assert "--execute" in text
        assert "dry-run" in text.lower()


def test_test_loader_found_nested_child_skill() -> None:
    assert SKILL_ROOT.name == "agent-readable-doc"
    assert SKILL_ROOT.parent.name == "skills"
