"""Tests for SKILL.md — validate YAML frontmatter structure."""

import pathlib

SKILL_MD = pathlib.Path(__file__).parent.parent / "SKILL.md"


def _parse_frontmatter(text: str) -> dict:
    """Hand-parse YAML frontmatter delimited by '---' lines."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = i
            break
    if end is None:
        return {}
    fm: dict = {}
    i = 1
    while i < end:
        line = lines[i]
        if ":" in line and not line.startswith(" ") and not line.startswith("\t"):
            key, _, rest = line.partition(":")
            rest = rest.strip()
            if rest == ">":
                # Multi-line folded scalar — collect indented continuation lines
                parts = []
                i += 1
                while i < end and (lines[i].startswith(" ") or lines[i].startswith("\t")):
                    parts.append(lines[i].strip())
                    i += 1
                fm[key.strip()] = " ".join(parts)
                continue
            else:
                fm[key.strip()] = rest.strip('"').strip("'")
        i += 1
    return fm


def test_skill_md_exists():
    assert SKILL_MD.exists(), "SKILL.md not found at repo root"


def test_frontmatter_present():
    content = SKILL_MD.read_text()
    assert content.startswith("---"), "SKILL.md must start with YAML frontmatter (---)"


def test_required_field_name():
    content = SKILL_MD.read_text()
    fm = _parse_frontmatter(content)
    assert "name" in fm, "frontmatter missing 'name' field"
    assert fm["name"].strip(), "'name' field must be non-empty"


def test_required_field_description():
    content = SKILL_MD.read_text()
    fm = _parse_frontmatter(content)
    assert "description" in fm, "frontmatter missing 'description' field"
    assert fm["description"].strip(), "'description' field must be non-empty"


def test_name_value():
    content = SKILL_MD.read_text()
    fm = _parse_frontmatter(content)
    assert (
        fm.get("name") == "friday-budgeting-pro"
    ), f"Expected name 'friday-budgeting-pro', got '{fm.get('name')}'"
