from pathlib import Path


def test_project_files_exist() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (root / "pyproject.toml").exists()
    assert (root / "SKILL.md").exists()
    assert (root / "INSTALL.md").exists()
    assert (root / "canvas_claw" / "__init__.py").exists()
