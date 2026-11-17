from __future__ import annotations

from pathlib import Path

import generate_dashboard


def _note(path: Path, shelf: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f'---\ntitle: "x"\nshelf: "{shelf}"\ntags:\n  - "book"\n---\n# x\n', encoding="utf-8")


def test_dashboard_counts_by_shelf_and_uses_configured_folder(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # the default template must not depend on the working directory
    _note(tmp_path / "Library" / "a.md", "currently-reading")
    _note(tmp_path / "Library" / "b.md", "to-read")
    _note(tmp_path / "Library" / "read" / "c.md", "read")
    _note(tmp_path / "Library" / "d.md", "inbox")

    result = generate_dashboard.generate_dashboard(
        vault_path=str(tmp_path),
        notes_dir="Library",
        dashboard_file="Library/Library Dashboard.md",
        template_file=str(generate_dashboard.DEFAULT_TEMPLATE),
    )
    rendered = (tmp_path / "Library" / "Library Dashboard.md").read_text(encoding="utf-8")

    assert result["ok"] is True
    assert result["counts"] == {
        "total_books": 4,
        "to_read_count": 1,
        "reading_count": 1,
        "finished_count": 1,
        "inbox_count": 1,
    }
    assert 'FROM "Library"' in rendered and "5. Library" not in rendered
    assert '"currently-reading", "reading"' in rendered
    assert "| currently-reading | 1 |" in rendered

    again = generate_dashboard.generate_dashboard(
        vault_path=str(tmp_path),
        notes_dir="Library",
        dashboard_file="Library/Library Dashboard.md",
        template_file=str(generate_dashboard.DEFAULT_TEMPLATE),
    )
    assert again["updated"] is False and again["counts"]["total_books"] == 4


def test_cli_requires_vault(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.delenv("BOOK_CAPTURE_VAULT_PATH", raising=False)
    assert generate_dashboard.main(["--vault-path", str(tmp_path / "missing")]) == 1
    assert "vault" in capsys.readouterr().out


def test_dashboard_path_cannot_escape_the_vault(tmp_path: Path):
    vault = tmp_path / "vault"
    _note(vault / "Books" / "a.md", "read")
    result = generate_dashboard.generate_dashboard(
        vault_path=str(vault),
        notes_dir="Books",
        dashboard_file="../outside.md",
        template_file=str(generate_dashboard.DEFAULT_TEMPLATE),
    )
    assert result["ok"] is False and "escapes" in result["error"]
    assert not (tmp_path / "outside.md").exists()


def test_shelf_names_cannot_inject_dataview_code(tmp_path: Path):
    _note(tmp_path / "Library" / "a.md", "`$= app.vault.getFiles().length`")
    _note(tmp_path / "Library" / "b.md", "a|b ~~~dataviewjs")

    generate_dashboard.generate_dashboard(
        vault_path=str(tmp_path),
        notes_dir="Library",
        dashboard_file="Library/Library Dashboard.md",
        template_file=str(generate_dashboard.DEFAULT_TEMPLATE),
    )
    rendered = (tmp_path / "Library" / "Library Dashboard.md").read_text(encoding="utf-8")
    table = rendered.split("## By shelf", 1)[1].split("## Recently added", 1)[0]

    assert "| \\`$= app.vault.getfiles().length\\` | 1 |" in table
    assert "| a\\|b \\~\\~\\~dataviewjs | 1 |" in table
