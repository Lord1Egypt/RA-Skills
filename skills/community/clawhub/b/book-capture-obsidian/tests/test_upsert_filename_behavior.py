from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "upsert_obsidian_note.py"


def _load_upsert_module():
    spec = importlib.util.spec_from_file_location("upsert_obsidian_note_under_test", str(MODULE_PATH))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_candidate_filename_sanitizes_colon_and_unicode_punctuation():
    module = _load_upsert_module()

    metadata = {
        "title": "Core： “Alpha” — Beta ★",
        "authors": ['A/B "C"'],
        "publisher": "Pub｜House",
        "published_date": "2024-01-01",
    }

    assert module._candidate_filename(metadata) == "Core Alpha Beta - A B C (Pub House, 2024).md"


def test_sample_title_sanitizer_behavior_is_stable_and_readable():
    module = _load_upsert_module()

    metadata = {
        "title": "The Fundamental Wisdom of the Middle Way: Nāgārjuna's Mūlamadhyamakakārikā",
        "authors": ["Jay L. Garfield"],
        "publisher": "Oxford University Press",
        "published_date": "1995",
    }

    assert module._candidate_filename(metadata) == (
        "The Fundamental Wisdom of the Middle Way Nāgārjuna s Mūlamadhyamakakārikā"
        " - Jay L Garfield (Oxford University Press, 1995).md"
    )


def test_matched_existing_note_moves_to_canonical_name_with_collision_suffix(tmp_path):
    module = _load_upsert_module()

    vault = tmp_path / "Vault"
    shelf_dir = vault / "Books" / "reading"
    shelf_dir.mkdir(parents=True, exist_ok=True)

    existing_note = shelf_dir / "Legacy Imported Name.md"
    existing_note.write_text(
        """---
title: "Legacy Imported Name"
isbn_13: "9780306406157"
goodreads_book_id: "12345"
---

Legacy content.
""",
        encoding="utf-8",
    )

    payload = {
        "isbn13": "9780306406157",
        "goodreads_book_id": "12345",
        "shelf": "reading",
        "metadata": {
            "title": "A：Title — With “Noise” ★",
            "authors": ["Ana/María"],
            "publisher": "Pub:House",
            "published_date": "2021",
            "source": "manual",
        },
    }

    canonical_name = module._candidate_filename(payload["metadata"])
    canonical_path = shelf_dir / canonical_name

    canonical_collision_content = "# Canonical collision\n"
    canonical_path.write_text(canonical_collision_content, encoding="utf-8")

    result = module.upsert_note(
        payload=payload,
        vault_path=str(vault),
        notes_dir="Books",
        target_note=None,
    )

    expected_path = canonical_path.with_name(f"{canonical_path.stem} (2){canonical_path.suffix}").resolve()

    assert result["ok"] is True
    assert Path(result["note_path"]) == expected_path
    assert result["moved"] is True
    assert result["previous_note_path"] == str(existing_note.resolve())
    assert expected_path.parent == shelf_dir.resolve()
    assert str(expected_path).startswith(str(vault.resolve()))

    assert not existing_note.exists()
    assert canonical_path.exists()
    assert canonical_path.read_text(encoding="utf-8") == canonical_collision_content
    assert expected_path.exists()

    moved_note_content = expected_path.read_text(encoding="utf-8")
    assert "# A：Title — With “Noise” ★" in moved_note_content
