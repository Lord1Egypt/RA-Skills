from __future__ import annotations

from pathlib import Path

from upsert_obsidian_note import upsert_note


def _payload(title: str = "The Testing Book") -> dict:
    return {
        "isbn13": "9780306406157",
        "shelf": "sci-com",
        "tags": ["book", "testing"],
        "metadata": {
            "title": title,
            "authors": ["Test Author"],
            "publisher": "Test Press",
            "published_date": "2024-03-01",
            "description": "A useful test description.",
            "page_count": 321,
            "language": "en",
            "categories": ["Software Testing"],
            "cover_image": "https://example.invalid/cover.jpg",
            "source": "unit_test",
            "source_url": "https://example.invalid/book",
        },
    }


def test_upsert_is_idempotent_and_writes_rich_note_only_in_tmp_path(tmp_path: Path):
    note_path = tmp_path / "Books" / "explicit.md"
    first = upsert_note(
        payload=_payload(),
        vault_path=str(tmp_path),
        notes_dir="Books",
        target_note=str(note_path),
    )
    first_content = note_path.read_text(encoding="utf-8")
    second = upsert_note(
        payload=_payload(),
        vault_path=str(tmp_path),
        notes_dir="Books",
        target_note=str(note_path),
    )

    assert first["ok"] is True and first["created"] is True
    assert second["ok"] is True and second["updated"] is False
    assert note_path.read_text(encoding="utf-8") == first_content
    assert "isbn_13: \"9780306406157\"" in first_content
    assert "## Summary" in first_content
    assert '  - "software-testing"' in first_content


def test_upsert_preserves_user_notes_when_managed_metadata_changes(tmp_path: Path):
    note_path = tmp_path / "Books" / "explicit.md"
    upsert_note(_payload(), str(tmp_path), "Books", str(note_path))
    content = note_path.read_text(encoding="utf-8")
    note_path.write_text(content + "\nMy handwritten observation.\n", encoding="utf-8")

    updated = upsert_note(_payload("The Testing Book, Revised"), str(tmp_path), "Books", str(note_path))
    new_content = note_path.read_text(encoding="utf-8")

    assert updated["ok"] is True
    assert updated["preserved_user_content"] is True
    assert "My handwritten observation." in new_content
    assert "The Testing Book, Revised" in new_content


def test_upsert_rejects_explicit_target_outside_vault(tmp_path: Path):
    vault = tmp_path / "vault"
    outside = tmp_path / "outside.md"
    result = upsert_note(_payload(), str(vault), "Books", str(outside))
    assert result["ok"] is False
    assert not outside.exists()


def test_note_language_pt_uses_portuguese_headings(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("BOOK_CAPTURE_NOTE_LANGUAGE", "pt")
    payload = _payload()
    payload["metadata"]["description"] = None
    note_path = tmp_path / "Books" / "pt.md"
    upsert_note(payload=payload, vault_path=str(tmp_path), notes_dir="Books", target_note=str(note_path))
    content = note_path.read_text(encoding="utf-8")
    assert "## Sinopse" in content
    assert "Obra de Test Author, publicada por Test Press (2024)." in content


def test_upsert_refuses_to_write_without_an_existing_vault(tmp_path: Path, monkeypatch):
    monkeypatch.delenv("BOOK_CAPTURE_VAULT_PATH", raising=False)
    monkeypatch.chdir(tmp_path)
    missing = upsert_note(payload=_payload(), vault_path="", notes_dir="Books")
    not_a_dir = upsert_note(payload=_payload(), vault_path=str(tmp_path / "nope"), notes_dir="Books")
    assert missing["ok"] is False and not_a_dir["ok"] is False
    assert "vault" in missing["error"]
    assert list(tmp_path.rglob("*.md")) == []


def test_related_links_only_scan_configured_folders(tmp_path: Path, monkeypatch):
    learnings = tmp_path / "Notes" / "testing ideas.md"
    learnings.parent.mkdir(parents=True)
    learnings.write_text("# Testing ideas\n", encoding="utf-8")

    monkeypatch.delenv("BOOK_CAPTURE_RELATED_DIRS", raising=False)
    first = upsert_note(payload=_payload(), vault_path=str(tmp_path), notes_dir="Books")
    assert first["related_links"] == []

    monkeypatch.setenv("BOOK_CAPTURE_RELATED_DIRS", "Notes")
    second = upsert_note(payload=_payload(), vault_path=str(tmp_path), notes_dir="Books")
    assert second["related_links"] == ["[[Notes/testing ideas]]"]


def test_crlf_description_does_not_rewrite_note_on_every_run(tmp_path: Path):
    payload = _payload()
    payload["metadata"]["description"] = "First paragraph.\r\n\r\nSecond paragraph."
    note_path = tmp_path / "Books" / "crlf.md"
    first = upsert_note(payload=payload, vault_path=str(tmp_path), notes_dir="Books", target_note=str(note_path))
    mtime = note_path.stat().st_mtime_ns
    second = upsert_note(payload=payload, vault_path=str(tmp_path), notes_dir="Books", target_note=str(note_path))

    assert first["created"] is True
    assert second["updated"] is False
    assert note_path.stat().st_mtime_ns == mtime
    assert b"\r" not in note_path.read_bytes()


def test_external_text_cannot_inject_dataview_code(tmp_path: Path):
    payload = _payload("Sneaky `$= dv.el('b', 'x')` Title")
    payload["metadata"]["description"] = (
        "Intro.\n```dataviewjs\ndv.paragraph('pwned')\n```\n"
        "~~~dataviewjs\ndv.paragraph('pwned')\n~~~\n"
        "Inline `$= app.vault.getFiles().length` and `= this.file.name`."
    )
    note_path = tmp_path / "Books" / "explicit.md"
    upsert_note(payload, str(tmp_path), "Books", str(note_path))
    body = note_path.read_text(encoding="utf-8").split("\n---\n", 1)[1]

    assert "```" not in body.replace("\\`", "")
    assert "~~~" not in body.replace("\\~", "")
    assert "`$=" not in body.replace("\\`", "")
    assert "# Sneaky \\`$= dv.el('b', 'x')\\` Title" in body
    second = upsert_note(payload, str(tmp_path), "Books", str(note_path))
    assert second["updated"] is False


def test_existing_backslashes_do_not_undo_the_escaping(tmp_path: Path):
    payload = _payload("Plain Title")
    payload["metadata"]["description"] = "Trick \\`$= app.vault.getFiles().length\\` and \\\\`= this.file.name\\\\`."
    note_path = tmp_path / "Books" / "explicit.md"
    upsert_note(payload, str(tmp_path), "Books", str(note_path))
    summary = note_path.read_text(encoding="utf-8").split("## Summary\n", 1)[1].split("\n", 1)[0]

    # Every backtick must be preceded by an odd number of backslashes.
    for i, ch in enumerate(summary):
        if ch == "`":
            run = len(summary[:i]) - len(summary[:i].rstrip("\\"))
            assert run % 2 == 1, summary
