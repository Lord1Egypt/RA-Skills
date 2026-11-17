from __future__ import annotations

from pathlib import Path

import ingest_photo


def test_extraction_failure_never_resolves_or_writes(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(
        ingest_photo,
        "extract_isbn_from_image",
        lambda _path: {"ok": False, "error": "no isbn", "warnings": []},
    )
    monkeypatch.setattr(
        ingest_photo,
        "resolve_book_metadata",
        lambda _isbn: (_ for _ in ()).throw(AssertionError("metadata must not run")),
    )
    monkeypatch.setattr(
        ingest_photo,
        "upsert_note",
        lambda **_kwargs: (_ for _ in ()).throw(AssertionError("upsert must not run")),
    )

    result = ingest_photo.ingest_book_photo("missing.jpg", str(tmp_path), "Books")
    assert result["ok"] is False and result["upsert"] is None
    assert list(tmp_path.rglob("*.md")) == []


def test_metadata_failure_never_writes(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(
        ingest_photo,
        "extract_isbn_from_image",
        lambda _path: {"ok": True, "isbn13": "9780306406157", "warnings": []},
    )
    monkeypatch.setattr(
        ingest_photo,
        "resolve_book_metadata",
        lambda _isbn: {"ok": False, "error": "not found", "warnings": []},
    )
    monkeypatch.setattr(
        ingest_photo,
        "upsert_note",
        lambda **_kwargs: (_ for _ in ()).throw(AssertionError("upsert must not run")),
    )

    result = ingest_photo.ingest_book_photo("photo.jpg", str(tmp_path), "Books")
    assert result["ok"] is False and result["upsert"] is None
    assert list(tmp_path.rglob("*.md")) == []
