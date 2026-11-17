from __future__ import annotations

from pathlib import Path

import migrate_goodreads_csv

HEADER = "Book Id,Title,Author,ISBN,ISBN13,Publisher,Year Published,Exclusive Shelf,Bookshelves\n"


def _csv(tmp_path: Path, rows: int) -> Path:
    path = tmp_path / "goodreads.csv"
    lines = [HEADER]
    for i in range(rows):
        lines.append(f'{i},Book {i},Author {i},,,Press,2020,to-read,\n')
    path.write_text("".join(lines), encoding="utf-8")
    return path


class CountingResolver:
    def __init__(self):
        self.calls = 0

        class Stats:
            def as_dict(self_inner):
                return {"calls": self.calls}

        self.stats = Stats()

    def lookup(self, **kwargs):
        self.calls += 1
        base = dict(kwargs["base"])
        base["description"] = "Filled"
        return base, None, ["google_books skipped: cooling down after a rate limit"]


def test_dry_run_never_calls_metadata_providers(tmp_path: Path):
    resolver = CountingResolver()
    result = migrate_goodreads_csv.migrate_csv(
        str(_csv(tmp_path, 3)), str(tmp_path), "Books", dry_run=True, enrich=True, resolver=resolver
    )
    assert result["ok"] is True and result["stats"]["unchanged"] == 3
    assert resolver.calls == 0
    assert result["enrichment"]["enabled"] is False


def test_live_run_enriches_keeps_csv_source_and_summarises_warnings(tmp_path: Path):
    resolver = CountingResolver()
    result = migrate_goodreads_csv.migrate_csv(
        str(_csv(tmp_path, 3)), str(tmp_path), "Books", dry_run=False, enrich=True, limit=2, resolver=resolver
    )
    notes = sorted((tmp_path / "Books").glob("*.md"))

    assert result["stats"]["created"] == 2 and resolver.calls == 2
    assert result["enrichment"]["warnings"] == {"google_books skipped: cooling down after a rate limit": 2}
    content = notes[0].read_text(encoding="utf-8")
    assert "Filled" in content and 'source: "goodreads_csv"' in content


def test_rows_without_isbn_are_kept_and_rerun_is_idempotent(tmp_path: Path):
    csv_path = _csv(tmp_path, 2)
    first = migrate_goodreads_csv.migrate_csv(str(csv_path), str(tmp_path), "Books", dry_run=False, enrich=False)
    second = migrate_goodreads_csv.migrate_csv(str(csv_path), str(tmp_path), "Books", dry_run=False, enrich=False)

    assert first["stats"]["created"] == 2 and first["stats"]["skipped"] == 0
    assert second["stats"]["created"] == 0 and second["stats"]["unchanged"] == 2
    assert len(list((tmp_path / "Books").glob("*.md"))) == 2
    assert 'goodreads_book_id: "0"' in (tmp_path / "Books").joinpath(
        sorted(p.name for p in (tmp_path / "Books").glob("*.md"))[0]
    ).read_text(encoding="utf-8")


def test_shelf_grouping_stays_inside_the_vault_and_never_deletes(tmp_path: Path):
    vault = tmp_path / "vault"
    vault.mkdir()
    csv_path = tmp_path / "evil.csv"
    csv_path.write_text(
        HEADER + '1,Same,Author,,,P,2020,../../escape,\n' + '2,Same,Author,,,P,2020,read,\n',
        encoding="utf-8",
    )

    result = migrate_goodreads_csv.migrate_csv(
        str(csv_path), str(vault), "Books", dry_run=False, group_by_shelf=True, enrich=False
    )

    outside = [p for p in tmp_path.rglob("*.md") if vault not in p.parents]
    assert outside == []
    assert len(list(vault.rglob("*.md"))) == 2
    assert (vault / "Books" / "escape").is_dir()
    assert result["stats"]["created"] == 2
