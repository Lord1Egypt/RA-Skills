"""Tests for the `geocode` CLI subcommand."""
from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts.photo_geolocator import main


def _read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_geocode_writes_coordinates(tmp_path, mock_nominatim):
    mock_nominatim.responses = {
        "Eiffel Tower, Paris, France": [{"lat": "48.8584", "lon": "2.2945"}]
    }
    ai = tmp_path / "ai.json"
    ai.write_text(json.dumps([{
        "filename": "p1.jpg", "landmark": "Eiffel Tower",
        "city": "Paris", "country": "France",
        "confidence": "high", "evidence": "Eiffel tower visible",
    }]), encoding="utf-8")
    out = tmp_path / "geo.csv"
    code = main(["geocode", "--input", str(ai), "--out", str(out),
                 "--cache", str(tmp_path / "cache.json")])
    assert code == 0
    rows = _read_csv(out)
    assert rows[0]["filename"] == "p1.jpg"
    assert abs(float(rows[0]["lat"]) - 48.8584) < 1e-3
    assert rows[0]["geocode_status"] == "OK"


def test_geocode_marks_not_found(tmp_path, mock_nominatim):
    mock_nominatim.responses = {"Atlantis, Atlantis, Atlantis": []}
    ai = tmp_path / "ai.json"
    ai.write_text(json.dumps([{
        "filename": "p2.jpg", "landmark": "Atlantis",
        "city": "Atlantis", "country": "Atlantis",
        "confidence": "low", "evidence": "??",
    }]), encoding="utf-8")
    out = tmp_path / "geo.csv"
    main(["geocode", "--input", str(ai), "--out", str(out),
          "--cache", str(tmp_path / "cache.json")])
    rows = _read_csv(out)
    assert rows[0]["geocode_status"] == "GEOCODE_FAILED"
    assert rows[0]["lat"] == ""


def test_geocode_continues_after_network_error(tmp_path, mock_nominatim, monkeypatch):
    # First entry: server error all the way; second entry: success.
    mock_nominatim.responses = {
        "Bad, Bad, Bad": {"__status__": 503},
        "Eiffel Tower, Paris, France": [{"lat": "48.8584", "lon": "2.2945"}],
    }
    # Speed up: stub time.sleep inside the geocoder
    monkeypatch.setattr("time.sleep", lambda s: None)

    ai = tmp_path / "ai.json"
    ai.write_text(json.dumps([
        {"filename": "p1.jpg", "landmark": "Bad", "city": "Bad", "country": "Bad", "confidence": "high"},
        {"filename": "p2.jpg", "landmark": "Eiffel Tower", "city": "Paris", "country": "France", "confidence": "high"},
    ]), encoding="utf-8")
    out = tmp_path / "geo.csv"
    main(["geocode", "--input", str(ai), "--out", str(out),
          "--cache", str(tmp_path / "cache.json")])
    rows = _read_csv(out)
    assert rows[0]["geocode_status"] == "NETWORK_ERROR"
    assert rows[1]["geocode_status"] == "OK"
