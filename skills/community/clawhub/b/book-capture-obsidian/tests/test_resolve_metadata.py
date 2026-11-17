from __future__ import annotations

import resolve_metadata

ISBN = "9780306406157"


class FakeResolver:
    def __init__(self, result):
        self.result = result
        self.calls = []

    def lookup(self, **kwargs):
        self.calls.append(kwargs)
        return self.result


def test_resolved_metadata_is_wrapped_in_the_stable_envelope():
    metadata = {"title": "Fallback Book", "authors": ["Fallback Author"], "source": "openlibrary"}
    resolver = FakeResolver((metadata, ISBN, ["google_books skipped: per-run request budget reached"]))

    result = resolve_metadata.resolve_book_metadata(ISBN, resolver=resolver)

    assert result["ok"] is True
    assert result["metadata"] == metadata
    assert result["warnings"] == ["google_books skipped: per-run request budget reached"]
    assert resolver.calls == [{"isbn13": ISBN, "title": "", "author": ""}]


def test_all_provider_failures_return_backward_compatible_envelope():
    resolver = FakeResolver((None, None, ["google failed", "open failed"]))

    result = resolve_metadata.resolve_book_metadata(ISBN, resolver=resolver)

    assert result == {
        "stage": "resolve_metadata",
        "ok": False,
        "error": "metadata not found in configured providers",
        "isbn13": ISBN,
        "metadata": None,
        "warnings": ["google failed", "open failed"],
    }


def test_title_lookup_works_without_isbn_and_invalid_isbn_is_rejected():
    resolver = FakeResolver(({"title": "Dune"}, "9780441013593", []))
    by_title = resolve_metadata.resolve_book_metadata(None, title="Dune", author="Frank Herbert", resolver=resolver)
    invalid = resolve_metadata.resolve_book_metadata("123", resolver=resolver)

    assert by_title["ok"] is True and by_title["isbn13"] == "9780441013593"
    assert resolver.calls[0] == {"isbn13": None, "title": "Dune", "author": "Frank Herbert"}
    assert invalid["ok"] is False and len(resolver.calls) == 1
