from __future__ import annotations

import json
from typing import Any

import pytest

import google_books

ISBN = "9780306406157"
OTHER_ISBN = "9780201633610"
SENTINEL = "test-key-marker-never-leak"


class FakeResponse:
    def __init__(self, status_code: int, payload: Any = None, headers: dict | None = None):
        self.status_code = status_code
        self._payload = payload
        self.headers = headers or {}

    def json(self):
        if isinstance(self._payload, Exception):
            raise self._payload
        return self._payload


def _payload(isbn: str = ISBN, **volume_overrides: Any) -> dict:
    volume = {
        "title": "Test Book",
        "authors": ["Test Author"],
        "publisher": "Test Press",
        "publishedDate": "2024",
        "description": "Description",
        "pageCount": 200,
        "language": "en",
        "categories": ["Testing"],
        "imageLinks": {"thumbnail": "http://books.google.test/cover?zoom=1"},
        "infoLink": "https://books.google.test/info",
        "industryIdentifiers": [{"type": "ISBN_13", "identifier": isbn}],
    }
    volume.update(volume_overrides)
    return {"items": [{"id": "one", "volumeInfo": volume}]}


def test_key_uses_params_partial_fields_and_never_leaks_to_result_or_url_argument():
    captured: dict[str, Any] = {}

    def fake_get(url, **kwargs):
        captured["url"] = url
        captured.update(kwargs)
        return FakeResponse(
            200,
            _payload(title=f"Title {SENTINEL}", infoLink=f"https://example.invalid/{SENTINEL}"),
        )

    metadata, found_isbn, warning = google_books.search_google_books(
        f"isbn:{ISBN}",
        requested_isbn=ISBN,
        api_key=SENTINEL,
        request_get=fake_get,
        max_retries=0,
    )

    assert captured["url"] == google_books.GOOGLE_BOOKS_URL
    assert SENTINEL not in captured["url"]
    assert captured["params"]["key"] == SENTINEL
    assert "volumeInfo" in captured["params"]["fields"]
    assert captured["timeout"] == 12
    assert found_isbn == ISBN and warning is None
    assert SENTINEL not in json.dumps(metadata)


def test_request_exception_is_secret_safe_and_bounded_without_network_or_sleep():
    calls = 0
    sleeps: list[float] = []

    def failing_get(_url, **_kwargs):
        nonlocal calls
        calls += 1
        raise RuntimeError(f"transport included {SENTINEL}")

    result = google_books.search_google_books(
        "intitle:test",
        api_key=SENTINEL,
        request_get=failing_get,
        sleep=sleeps.append,
        delay_ms=100,
        max_retries=2,
        max_retry_after_sec=5,
    )

    assert calls == 3
    assert sleeps == [0.1, 0.2]
    assert SENTINEL not in json.dumps(result)


def test_long_retry_after_defers_instead_of_retrying_early():
    responses = [
        FakeResponse(429, {}, {"Retry-After": "99"}),
        FakeResponse(200, _payload()),
    ]
    sleeps: list[float] = []

    result = google_books.search_google_books(
        f"isbn:{ISBN}",
        requested_isbn=ISBN,
        request_get=lambda *_args, **_kwargs: responses.pop(0),
        sleep=sleeps.append,
        max_retries=1,
        max_retry_after_sec=3,
    )

    assert result[0] is None and result[2] == google_books.RATE_LIMIT_WARNING
    assert len(responses) == 1
    assert sleeps == []


@pytest.mark.parametrize("status_code", [500, 502, 503, 599])
def test_transient_5xx_retries_then_succeeds(status_code: int):
    responses = [FakeResponse(status_code, {}), FakeResponse(200, _payload())]
    sleeps: list[float] = []
    metadata, _found, warning = google_books.search_google_books(
        f"isbn:{ISBN}",
        requested_isbn=ISBN,
        request_get=lambda *_args, **_kwargs: responses.pop(0),
        sleep=sleeps.append,
        delay_ms=50,
        max_retries=1,
    )
    assert metadata is not None and warning is None
    assert sleeps == [0.05]


@pytest.mark.parametrize("status_code", [400, 403, 404])
def test_ordinary_4xx_does_not_retry(status_code: int):
    calls = 0

    def fake_get(*_args, **_kwargs):
        nonlocal calls
        calls += 1
        return FakeResponse(status_code, {"error": SENTINEL})

    result = google_books.search_google_books(
        "intitle:test",
        api_key=SENTINEL,
        request_get=fake_get,
        sleep=lambda _seconds: pytest.fail("ordinary 4xx must not sleep"),
        max_retries=4,
    )
    assert calls == 1
    assert result[0] is None
    assert result[2] == f"google books http {status_code}"
    assert SENTINEL not in json.dumps(result)


def test_isbn_search_rejects_mismatching_identifier_but_accepts_missing_identifiers():
    mismatch = google_books.parse_google_books_response(_payload(OTHER_ISBN), requested_isbn=ISBN)
    no_identifiers = google_books.parse_google_books_response(
        _payload(ISBN, industryIdentifiers=[]), requested_isbn=ISBN
    )
    assert mismatch[0] is None
    assert mismatch[2] == "google books returned a mismatching ISBN"
    assert no_identifiers[0] is not None and no_identifiers[2] is None


def test_response_normalization_is_defensive():
    metadata, found, warning = google_books.parse_google_books_response(
        _payload(ISBN, authors="not-a-list", categories=["One", "One"], pageCount="0")
    )
    assert warning is None and found == ISBN
    assert metadata is not None
    assert metadata["authors"] == []
    assert metadata["categories"] == ["One"]
    assert metadata["page_count"] is None
    assert metadata["cover_image"].startswith("https://")
    assert "zoom=2" in metadata["cover_image"]


@pytest.mark.parametrize("retry_after", ["2", "Thu, 01 Jan 1970 00:16:42 GMT"])
def test_retry_after_seconds_or_http_date_is_respected(retry_after):
    responses = [FakeResponse(429, {}, {"Retry-After": retry_after}), FakeResponse(200, _payload())]
    sleeps = []
    result = google_books.search_google_books(
        "test", request_get=lambda *a, **k: responses.pop(0), sleep=sleeps.append,
        now=lambda: 1000.0, max_retries=1, max_retry_after_sec=3,
    )
    assert result[0] and sleeps == [2.0]


@pytest.mark.parametrize("reason", ["dailyLimitExceeded", "quotaExceeded", "rateLimitExceeded", "userRateLimitExceeded"])
def test_quota_403_defers_without_retry_or_error_body_leak(reason):
    calls, deferred = [], []
    def get(*a, **k):
        calls.append(1)
        return FakeResponse(403, {"error": {"errors": [{"reason": reason, "message": SENTINEL}]}})
    result = google_books.search_google_books(
        "test", request_get=get, sleep=lambda s: pytest.fail("quota must defer"),
        on_defer=deferred.append, api_key=SENTINEL,
    )
    assert len(calls) == 1 and deferred == [0.0]
    assert result[2] == google_books.QUOTA_WARNING
    assert SENTINEL not in json.dumps(result)
