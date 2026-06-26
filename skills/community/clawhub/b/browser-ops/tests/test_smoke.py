"""Smoke test for browser-ops skill."""

def test_skill_directory_exists():
    from pathlib import Path
    import os
    skill_dir = Path(os.path.expanduser("~/.claude/skills/browser-ops"))
    assert skill_dir.exists()

def test_skill_md_exists():
    from pathlib import Path
    import os
    skill_md = Path(os.path.expanduser("~/.claude/skills/browser-ops/SKILL.md"))
    assert skill_md.exists()
