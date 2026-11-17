from __future__ import annotations

from typing import Any, Callable, Dict, List

import pytest

from metadata_cache import MetadataCache
from metadata_resolver import MetadataResolver, merge_missing

ISBN = "9780306406157"


class FakeResponse:
    def __init__(self, status_code: int, payload: Any = None, headers: dict | None = None):
        self.status_code = status_code
        self._payload = payload
        self.headers = headers or {}

    def json(self):
        return self._payload


class Clock:
    def __init__(self) -> None:
        self.t = 1_000_000.0

    def now(self) -> float:
        return self.t

    def sleep(self, seconds: float) -> None:
        self.t += seconds


def openlibrary_book(description: str | None = "An OL description", cover: bool = True) -> dict:
    book: Dict[str, Any] = {
        "title": "Test Book",
        "authors": [{"name": "Test Author"}],
        "publishers": [{"name": "Test Press"}],
        "publish_date": "2024",
        "number_of_pages": 200,
        "subjects": [{"name": "Testing"}],
        "url": "https://openlibrary.org/books/OL1M/Test_Book",
    }
    if description:
        book["description"] = description
    if cover:
        book["cover"] = {"large": "https://covers.openlibrary.org/b/id/1-L.jpg"}
    return {f"ISBN:{ISBN}": book}


def google_payload() -> dict:
    return {
        "items": [
            {
                "volumeInfo": {
                    "title": "Test Book (Google)",
                    "authors": ["Test Author"],
                    "description": "A Google description",
                    "imageLinks": {"thumbnail": "https://books.google.test/c?zoom=1"},
                    "industryIdentifiers": [{"type": "ISBN_13", "identifier": ISBN}],
                }
            }
        ]
    }


def router(routes: Dict[str, Callable[[], FakeResponse]], log: List[str]):
    def fake_get(url, **_kwargs):
        log.append(url)
        for prefix, make in routes.items():
            if url.startswith(prefix):
                return make()
        raise AssertionError(f"unexpected URL {url}")

    return fake_get


def make_resolver(fake_get, clock: Clock, cache: MetadataCache | None = None, **kwargs) -> MetadataResolver:
    return MetadataResolver(
        cache=cache or MetadataCache(None, now=clock.now),
        request_get=fake_get,
        sleep=clock.sleep,
        now=clock.now,
        **kwargs,
    )


def test_complete_openlibrary_result_never_calls_google():
    clock, log = Clock(), []
    fake_get = router({"https://openlibrary.org/api/books": lambda: FakeResponse(200, openlibrary_book())}, log)
    resolver = make_resolver(fake_get, clock)

    metadata, isbn, warnings = resolver.lookup(isbn13=ISBN)

    assert metadata["title"] == "Test Book" and metadata["description"] == "An OL description"
    assert isbn == ISBN and warnings == []
    assert resolver.stats.network_calls == {"openlibrary": 1, "google_books": 0}


def test_google_only_fills_missing_fields_without_overwriting():
    clock, log = Clock(), []
    fake_get = router(
        {
            "https://openlibrary.org/api/books": lambda: FakeResponse(200, openlibrary_book(description=None)),
            "https://www.googleapis.com/books/v1/volumes": lambda: FakeResponse(200, google_payload()),
        },
        log,
    )
    resolver = make_resolver(fake_get, clock)

    metadata, _isbn, _warnings = resolver.lookup(isbn13=ISBN)

    assert metadata["title"] == "Test Book"  # Open Library value kept
    assert metadata["description"] == "A Google description"  # gap filled
    assert metadata["source"] == "openlibrary"


def test_second_lookup_is_served_from_persistent_cache(tmp_path):
    clock, log = Clock(), []
    fake_get = router({"https://openlibrary.org/api/books": lambda: FakeResponse(200, openlibrary_book())}, log)
    path = tmp_path / "cache.sqlite3"

    first = make_resolver(fake_get, clock, MetadataCache(path, now=clock.now))
    first.lookup(isbn13=ISBN)
    second = make_resolver(fake_get, clock, MetadataCache(path, now=clock.now))
    metadata, _isbn, _warnings = second.lookup(isbn13=ISBN)

    assert metadata["title"] == "Test Book"
    assert len(log) == 1
    assert second.stats.cache_hits == 1 and second.stats.network_calls["openlibrary"] == 0


def test_google_429_pauses_google_for_later_rows_and_later_runs(tmp_path):
    clock, log = Clock(), []
    fake_get = router(
        {
            "https://openlibrary.org/api/books": lambda: FakeResponse(200, openlibrary_book(description=None)),
            "https://www.googleapis.com/books/v1/volumes": lambda: FakeResponse(429, {}),
        },
        log,
    )
    path = tmp_path / "cache.sqlite3"
    resolver = make_resolver(fake_get, clock, MetadataCache(path, now=clock.now), google_max_retries=1)

    _m, _i, first_warnings = resolver.lookup(isbn13=ISBN)
    _m, _i, second_warnings = resolver.lookup(isbn13="9780201633610")
    google_calls = [url for url in log if "googleapis" in url]

    assert len(google_calls) == 2  # one request plus one retry, then nothing
    assert any("paused" in w for w in first_warnings)
    assert any("cooling down" in w for w in second_warnings)

    next_run = make_resolver(fake_get, clock, MetadataCache(path, now=clock.now))
    next_run.lookup(isbn13="9780131103627")
    assert len([url for url in log if "googleapis" in url]) == 2
    assert next_run.stats.google_skipped_cooldown == 1

    clock.t += 3601
    after_cooldown = make_resolver(fake_get, clock, MetadataCache(path, now=clock.now), google_max_retries=0)
    after_cooldown.lookup(isbn13="9780131103627")
    assert len([url for url in log if "googleapis" in url]) == 3


def test_per_run_google_budget_is_enforced():
    clock, log = Clock(), []
    fake_get = router(
        {
            "https://openlibrary.org/api/books": lambda: FakeResponse(200, {}),
            "https://www.googleapis.com/books/v1/volumes": lambda: FakeResponse(200, {"items": []}),
        },
        log,
    )
    resolver = make_resolver(fake_get, clock, google_budget=2)
    for isbn in ["9780306406157", "9780201633610", "9780131103627"]:
        resolver.lookup(isbn13=isbn)

    assert resolver.stats.network_calls["google_books"] == 2
    assert resolver.stats.google_skipped_budget == 1


def test_transient_errors_are_not_cached():
    clock, log = Clock(), []
    responses = [FakeResponse(503, {}), FakeResponse(200, openlibrary_book())]
    fake_get = router({"https://openlibrary.org/api/books": lambda: responses.pop(0)}, log)
    resolver = make_resolver(fake_get, clock, providers=["openlibrary"])

    failed, _i, warnings = resolver.lookup(isbn13=ISBN)
    retried, _i, _w = resolver.lookup(isbn13=ISBN)

    assert failed is None and warnings == ["openlibrary request failed"]
    assert retried is not None and retried["title"] == "Test Book"


def test_openlibrary_requests_are_spaced():
    clock, log = Clock(), []
    fake_get = router({"https://openlibrary.org/api/books": lambda: FakeResponse(200, openlibrary_book())}, log)
    resolver = make_resolver(fake_get, clock, providers=["openlibrary"], openlibrary_delay_ms=500)
    start = clock.t
    resolver.lookup(isbn13="9780306406157")
    resolver.lookup(isbn13="9780201633610")
    assert clock.t - start == pytest.approx(0.5)


def test_base_fields_win_and_title_search_does_not_adopt_edition_isbn():
    clock, log = Clock(), []
    search = {"docs": [{"key": "/works/OL1W", "title": "CSV Title: A Novel", "author_name": ["Csv Author"], "cover_i": 7}]}
    fake_get = router(
        {
            "https://openlibrary.org/search.json": lambda: FakeResponse(200, search),
            "https://openlibrary.org/works/OL1W.json": lambda: FakeResponse(200, {"description": {"value": "Work text"}}),
        },
        log,
    )
    resolver = make_resolver(fake_get, clock, providers=["openlibrary"])
    base = {"title": "CSV Title", "authors": ["CSV Author"], "description": None, "cover_image": None}

    metadata, isbn, _w = resolver.lookup(title="CSV Title", author="CSV Author", base=base)

    assert metadata["title"] == "CSV Title" and metadata["authors"] == ["CSV Author"]
    assert metadata["description"] == "Work text"
    assert metadata["cover_image"] == "https://covers.openlibrary.org/b/id/7-L.jpg"
    assert isbn is None


def test_merge_missing_ignores_empty_values():
    assert merge_missing({"title": "A", "categories": []}, {"title": "B", "categories": ["x"], "publisher": ""}) == {
        "title": "A",
        "categories": ["x"],
    }


def test_title_search_rejects_wrong_book_and_picks_matching_doc():
    # Shapes taken from real Open Library responses (2026-10): a title plus
    # author query for "The Three-Body Problem" ranks the sequels first, and a
    # title-only query returns a physics book with the same title.
    clock, log = Clock(), []
    docs = {
        "docs": [
            {"key": "/works/OL16314245W", "title": "The Dark Forest (The Three-Body Problem Series Book 2)", "author_name": ["Liu Cixin"]},
            {"key": "/works/OL15172337W", "title": "The Three-Body Problem", "author_name": ["Mauri Valtonen", "Hannu Karttunen"]},
            {"key": "/works/OL9W", "title": "The Three-Body Problem", "author_name": ["Cixin Liu"], "cover_i": 3},
        ]
    }
    fake_get = router(
        {
            "https://openlibrary.org/search.json": lambda: FakeResponse(200, docs),
            "https://openlibrary.org/works/OL9W.json": lambda: FakeResponse(200, {"description": "Right book"}),
        },
        log,
    )
    resolver = make_resolver(fake_get, clock, providers=["openlibrary"])
    metadata, _isbn, _w = resolver.lookup(title="The Three-Body Problem", author="Liu Cixin")
    assert metadata["description"] == "Right book"
    assert "limit=5" in log[0]

    only_wrong = {"docs": docs["docs"][:2]}
    fake_get = router({"https://openlibrary.org/search.json": lambda: FakeResponse(200, only_wrong)}, [])
    resolver = make_resolver(fake_get, Clock(), providers=["openlibrary"])
    metadata, _isbn, warnings = resolver.lookup(title="The Three-Body Problem", author="Liu Cixin")
    assert not (metadata or {}).get("description")
    assert any("no close title/author match" in w for w in warnings)


def test_isbn_lookup_follows_edition_record_to_work_description():
    # Real jscmd=data responses carry the edition key but no works link.
    clock, log = Clock(), []
    book = openlibrary_book(description=None)
    book[f"ISBN:{ISBN}"]["key"] = "/books/OL1M"
    book[f"ISBN:{ISBN}"]["subjects"] = [{"name": f"S{i}"} for i in range(30)]
    fake_get = router(
        {
            "https://openlibrary.org/api/books": lambda: FakeResponse(200, book),
            "https://openlibrary.org/books/OL1M.json": lambda: FakeResponse(200, {"works": [{"key": "/works/OL7W"}]}),
            "https://openlibrary.org/works/OL7W.json": lambda: FakeResponse(200, {"description": {"value": "Work blurb"}}),
        },
        log,
    )
    resolver = make_resolver(fake_get, clock, providers=["openlibrary"])
    metadata, _isbn, _w = resolver.lookup(isbn13=ISBN)
    assert metadata["description"] == "Work blurb"
    assert len(metadata["categories"]) == 10
    assert [u.split("?")[0] for u in log] == [
        "https://openlibrary.org/api/books",
        "https://openlibrary.org/books/OL1M.json",
        "https://openlibrary.org/works/OL7W.json",
    ]


def test_google_title_search_needs_matching_title_and_drops_isbn():
    clock = Clock()
    wrong = google_payload()
    fake_get = router(
        {
            "https://openlibrary.org/search.json": lambda: FakeResponse(200, {"docs": []}),
            "https://www.googleapis.com/books/v1/volumes": lambda: FakeResponse(200, wrong),
        },
        [],
    )
    resolver = make_resolver(fake_get, clock, google_delay_ms=0)
    metadata, isbn, warnings = resolver.lookup(title="Completely Different", author="Someone")
    assert not (metadata or {}).get("description") and isbn is None
    assert any("google books found no close" in w for w in warnings)

    resolver = make_resolver(fake_get, Clock(), google_delay_ms=0)
    metadata, isbn, _w = resolver.lookup(title="Test Book", author="Test Author")
    assert metadata["description"] == "A Google description"
    assert isbn is None


def test_isbn_miss_falls_back_to_openlibrary_title_search_before_google():
    # Real case: Ensaio sobre a Cegueira (9789722110723) has no Open Library
    # ISBN record, but the title search finds the work.
    clock, log = Clock(), []
    search = {"docs": [{"key": "/works/OL27420W", "title": "Ensaio Sobre a Cegueira",
                        "author_name": ["José Saramago"], "cover_i": 10482411,
                        "publisher": ["Haenaem"]}]}
    fake_get = router(
        {
            "https://openlibrary.org/api/books": lambda: FakeResponse(200, {}),
            "https://openlibrary.org/search.json": lambda: FakeResponse(200, search),
            "https://openlibrary.org/works/OL27420W.json": lambda: FakeResponse(
                200, {"description": "Uma cegueira branca.\r\n\r\nSegundo paragrafo."}),
        },
        log,
    )
    resolver = make_resolver(fake_get, clock)
    base = {"title": "Ensaio sobre a Cegueira", "authors": ["José Saramago"], "publisher": None,
            "description": None, "cover_image": None}
    metadata, isbn, _w = resolver.lookup(isbn13="9789722110723", title="Ensaio sobre a Cegueira",
                                         author="José Saramago", base=base)
    assert isbn == "9789722110723"
    assert metadata["cover_image"] == "https://covers.openlibrary.org/b/id/10482411-L.jpg"
    assert metadata["description"] == "Uma cegueira branca.\n\nSegundo paragrafo."
    assert metadata["publisher"] is None  # work-level publishers belong to other editions
    assert not any("googleapis" in u for u in log)


@pytest.mark.parametrize("failure", ["http", "network"])
def test_google_budget_includes_retry_attempts(failure):
    clock, calls = Clock(), []

    def get(url, **kwargs):
        calls.append(url)
        if failure == "network":
            raise OSError("offline")
        return FakeResponse(503, {})

    resolver = make_resolver(get, clock, providers=["google_books"], google_budget=2, google_max_retries=5)
    resolver.lookup(isbn13=ISBN)
    _, _, warnings = resolver.lookup(isbn13="9780201633610")
    assert len(calls) == 2
    assert resolver.stats.network_calls["google_books"] == 2
    assert any("budget" in warning for warning in warnings)


def test_default_openlibrary_interval_respects_one_request_per_second():
    clock, times = Clock(), []
    def get(url, **kwargs):
        times.append(clock.now())
        return FakeResponse(200, {})
    resolver = make_resolver(get, clock, providers=["openlibrary"])
    resolver.lookup(isbn13=ISBN)
    resolver.lookup(isbn13="9780201633610")
    assert len(times) == 2
    assert times[1] - times[0] >= 1


@pytest.mark.parametrize("status,payload", [(200, {}), (200, {"items": [{"volumeInfo": {"title": "Test Book"}}]}), (429, {})])
def test_google_only_never_falls_back_when_incomplete_missing_or_limited(status, payload):
    clock, calls = Clock(), []
    def get(url, **kwargs):
        calls.append(url)
        assert "googleapis.com" in url
        return FakeResponse(status, payload)
    resolver = make_resolver(get, clock, providers=["google_books"], google_max_retries=0)
    resolver.lookup(isbn13=ISBN)
    resolver.lookup(isbn13="9780201633610")
    assert calls and resolver.stats.network_calls["openlibrary"] == 0


def test_google_first_preserves_google_fields_and_fills_from_openlibrary():
    clock, calls = Clock(), []
    payload = google_payload()
    del payload["items"][0]["volumeInfo"]["description"]
    get = router({
        "https://www.googleapis.com": lambda: FakeResponse(200, payload),
        "https://openlibrary.org": lambda: FakeResponse(200, openlibrary_book()),
    }, calls)
    resolver = make_resolver(get, clock, providers=["google_books", "openlibrary"])
    metadata, _, _ = resolver.lookup(isbn13=ISBN)
    assert "googleapis.com" in calls[0]
    assert metadata["title"] == "Test Book (Google)"
    assert metadata["source"] == "google_books"
    assert metadata["description"] == "An OL description"


def test_google_only_ignores_openlibrary_cache_and_keeps_trusted_base():
    clock = Clock()
    cache = MetadataCache(None, now=clock.now)
    cache.put(f"openlibrary:isbn:{ISBN}", {"metadata": {"title": "OL cached"}, "isbn13": ISBN}, 1)
    calls = []
    resolver = make_resolver(router({"https://www.googleapis.com": lambda: FakeResponse(200, google_payload())}, calls), clock,
                             cache, providers=["google_books"])
    metadata, _, _ = resolver.lookup(isbn13=ISBN, base={"title": "My title"})
    assert metadata["title"] == "My title" and metadata["description"] == "A Google description"
    assert len(calls) == 1 and resolver.stats.cache_hits == 0


@pytest.mark.parametrize("providers", ["google_books", "openlibrary", "google_books,openlibrary", "openlibrary,google_books"])
def test_provider_and_pacing_environment_settings(monkeypatch, providers):
    monkeypatch.setenv("BOOK_CAPTURE_METADATA_PROVIDER_ORDER", providers)
    monkeypatch.setenv("BOOK_CAPTURE_GOOGLE_MIN_INTERVAL_MS", "1200")
    resolver = MetadataResolver.from_env(cache=MetadataCache(None))
    assert resolver.providers == providers.split(",")
    assert resolver.google_min_interval_ms == 1200


def test_google_paces_every_attempt_including_retry_and_later_lookup():
    clock, times = Clock(), []
    responses = [FakeResponse(503, {}), FakeResponse(200, {}), FakeResponse(200, {})]
    def get(*a, **k):
        times.append(clock.now())
        return responses.pop(0)
    resolver = make_resolver(get, clock, providers=["google_books"], google_min_interval_ms=1200, google_delay_ms=0)
    resolver.lookup(isbn13=ISBN)
    resolver.lookup(isbn13="9780201633610")
    assert len(times) == 3 and times[0] == 1_000_000.0
    assert all(b-a >= 1.199 for a,b in zip(times,times[1:]))


@pytest.mark.parametrize("status,headers,payload", [
    (429, {"Retry-After": "7200"}, {}),
    (503, {"Retry-After": "7200"}, {}),
    (403, {}, {"error": {"errors": [{"reason": "dailyLimitExceeded"}]}}),
])
def test_deferred_google_requests_persist_without_provider_switch(tmp_path, status, headers, payload):
    clock, calls = Clock(), []
    def get(url, **kwargs):
        calls.append(url)
        return FakeResponse(status, payload, headers)
    path = tmp_path / "cache.sqlite3"
    resolver = make_resolver(get, clock, MetadataCache(path, now=clock.now), providers=["google_books"])
    resolver.lookup(isbn13=ISBN)
    assert len(calls) == 1
    clock.t += 3500 if status == 403 else 7000
    next_run = make_resolver(get, clock, MetadataCache(path, now=clock.now), providers=["google_books"])
    _, _, warnings = next_run.lookup(isbn13="9780201633610")
    assert len(calls) == 1 and any("cooling down" in w for w in warnings)
    clock.t += 3601
    next_run.lookup(isbn13="9780201633610")
    assert len(calls) == 2
