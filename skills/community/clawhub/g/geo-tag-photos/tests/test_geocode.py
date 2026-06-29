"""Tests for the Nominatim geocoder + cache + rate limit."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.geocoder import (
    USER_AGENT,
    Geocoder,
    GeocodeError,
    MIN_REQUEST_INTERVAL,
    _canonical_key,
)


class FakeClock:
    def __init__(self):
        self.t = 1000.0
        self.sleeps: list[float] = []

    def sleep(self, sec: float) -> None:
        self.sleeps.append(sec)
        self.t += sec

    def monotonic(self) -> float:
        return self.t


def _new_geocoder(tmp_path, clock=None):
    clock = clock or FakeClock()
    g = Geocoder(
        tmp_path / "cache.json",
        sleep_fn=clock.sleep,
        monotonic_fn=clock.monotonic,
    )
    return g, clock


def test_canonical_key_lowercases_and_collapses_whitespace():
    assert _canonical_key("Eiffel  Tower", "PARIS", " France ") == "eiffel tower|paris|france"


def test_geocode_cache_miss_writes_cache(tmp_path, mock_nominatim):
    mock_nominatim.responses = {
        "Eiffel Tower, Paris, France": [{"lat": "48.8584", "lon": "2.2945"}]
    }
    g, _ = _new_geocoder(tmp_path)
    result = g.geocode("Eiffel Tower", "Paris", "France")
    assert result == (48.8584, 2.2945)
    g.save_cache()
    saved = json.loads((tmp_path / "cache.json").read_text())
    assert saved["eiffel tower|paris|france"] == [48.8584, 2.2945]


def test_geocode_cache_hit_skips_network(tmp_path, mock_nominatim):
    cache_path = tmp_path / "cache.json"
    cache_path.write_text(json.dumps({"eiffel tower|paris|france": [48.8584, 2.2945]}))
    g, _ = _new_geocoder(tmp_path)
    result = g.geocode("Eiffel Tower", "Paris", "France")
    assert result == (48.8584, 2.2945)
    assert mock_nominatim.calls == []


def test_geocode_returns_none_when_no_result(tmp_path, mock_nominatim):
    mock_nominatim.responses = {"Nowhere, Nowhere, Nowhere": []}
    g, _ = _new_geocoder(tmp_path)
    assert g.geocode("Nowhere", "Nowhere", "Nowhere") is None


def test_geocode_caches_negative_results(tmp_path, mock_nominatim):
    mock_nominatim.responses = {"Nowhere, Nowhere, Nowhere": []}
    g, _ = _new_geocoder(tmp_path)
    g.geocode("Nowhere", "Nowhere", "Nowhere")
    assert g.geocode("Nowhere", "Nowhere", "Nowhere") is None
    assert len(mock_nominatim.calls) == 1


def test_geocode_rate_limits_between_misses(tmp_path, mock_nominatim):
    mock_nominatim.responses = {
        "A, A, A": [{"lat": "1", "lon": "2"}],
        "B, B, B": [{"lat": "3", "lon": "4"}],
        "C, C, C": [{"lat": "5", "lon": "6"}],
    }
    g, clock = _new_geocoder(tmp_path)
    g.geocode("A", "A", "A")
    g.geocode("B", "B", "B")
    g.geocode("C", "C", "C")
    # First call: no prior request, may sleep 0; later calls must each sleep >= MIN_REQUEST_INTERVAL.
    assert sum(clock.sleeps) >= 2 * MIN_REQUEST_INTERVAL


def test_geocode_user_agent_is_set(tmp_path, mock_nominatim):
    mock_nominatim.responses = {"X, X, X": [{"lat": "0", "lon": "0"}]}
    g, _ = _new_geocoder(tmp_path)
    g.geocode("X", "X", "X")
    assert mock_nominatim.calls[0]["headers"]["User-Agent"] == USER_AGENT


def test_geocode_retries_on_5xx_then_raises(tmp_path, mock_nominatim):
    mock_nominatim.responses = {"X, X, X": {"__status__": 503, "text": "down"}}
    g, _ = _new_geocoder(tmp_path)
    with pytest.raises(GeocodeError):
        g.geocode("X", "X", "X")
    assert len(mock_nominatim.calls) == 3  # exactly 3 attempts
