"""Tests for the `report` CLI subcommand."""
from __future__ import annotations

import csv
from pathlib import Path

from scripts.photo_geolocator import main


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def _read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _make_geo_csv(path: Path, entries: list[dict]) -> None:
    fields = ["filename", "landmark", "city", "country", "confidence", "evidence",
              "lat", "lon", "geocode_status"]
    _write_csv(path, fields, entries)


def test_report_marks_write_action_for_clean_inference(make_jpg, tmp_path):
    photos = tmp_path / "p"
    photos.mkdir()
    make_jpg(photos, name="a.jpg", gps=None)
    geo = tmp_path / "geo.csv"
    _make_geo_csv(geo, [{
        "filename": "a.jpg", "landmark": "Eiffel Tower", "city": "Paris", "country": "France",
        "confidence": "high", "evidence": "tower visible",
        "lat": "48.8584", "lon": "2.2945", "geocode_status": "OK",
    }])
    out = tmp_path / "rep.csv"
    main(["report", "--dir", str(photos), "--geocoded", str(geo), "--out", str(out)])
    row = _read_csv(out)[0]
    assert row["action"] == "WRITE"
    assert row["inferred_lat"] == "48.8584"


def test_report_skips_existing_gps(make_jpg, tmp_path):
    photos = tmp_path / "p"
    photos.mkdir()
    make_jpg(photos, name="a.jpg", gps=(1.0, 2.0))
    geo = tmp_path / "geo.csv"
    _make_geo_csv(geo, [{
        "filename": "a.jpg", "landmark": "X", "city": "X", "country": "X",
        "confidence": "high", "evidence": "", "lat": "1", "lon": "2", "geocode_status": "OK",
    }])
    out = tmp_path / "rep.csv"
    main(["report", "--dir", str(photos), "--geocoded", str(geo), "--out", str(out)])
    assert _read_csv(out)[0]["action"] == "SKIP_HAS_GPS"


def test_report_skips_low_confidence(make_jpg, tmp_path):
    photos = tmp_path / "p"
    photos.mkdir()
    make_jpg(photos, name="a.jpg", gps=None)
    geo = tmp_path / "geo.csv"
    _make_geo_csv(geo, [{
        "filename": "a.jpg", "landmark": "X", "city": "X", "country": "X",
        "confidence": "low", "evidence": "", "lat": "1", "lon": "2", "geocode_status": "OK",
    }])
    out = tmp_path / "rep.csv"
    main(["report", "--dir", str(photos), "--geocoded", str(geo), "--out", str(out)])
    assert _read_csv(out)[0]["action"] == "SKIP_LOW_CONFIDENCE"


def test_report_skips_geocode_failed(make_jpg, tmp_path):
    photos = tmp_path / "p"
    photos.mkdir()
    make_jpg(photos, name="a.jpg", gps=None)
    geo = tmp_path / "geo.csv"
    _make_geo_csv(geo, [{
        "filename": "a.jpg", "landmark": "X", "city": "X", "country": "X",
        "confidence": "high", "evidence": "", "lat": "", "lon": "", "geocode_status": "GEOCODE_FAILED",
    }])
    out = tmp_path / "rep.csv"
    main(["report", "--dir", str(photos), "--geocoded", str(geo), "--out", str(out)])
    assert _read_csv(out)[0]["action"] == "SKIP_NO_GEOCODE"


def test_report_marks_unknown_for_missing_ai_entry(make_jpg, tmp_path):
    photos = tmp_path / "p"
    photos.mkdir()
    make_jpg(photos, name="orphan.jpg", gps=None)
    geo = tmp_path / "geo.csv"
    _make_geo_csv(geo, [])
    out = tmp_path / "rep.csv"
    main(["report", "--dir", str(photos), "--geocoded", str(geo), "--out", str(out)])
    assert _read_csv(out)[0]["action"] == "SKIP_AI_UNKNOWN"


def test_report_populates_inferred_fields_on_skip_has_gps(make_jpg, tmp_path):
    """SKIP_HAS_GPS rows must still carry the AI inference so --overwrite-existing has data."""
    photos = tmp_path / "p"; photos.mkdir()
    make_jpg(photos, name="a.jpg", gps=(10.0, 20.0))
    geo = tmp_path / "geo.csv"
    _make_geo_csv(geo, [{
        "filename": "a.jpg", "landmark": "Eiffel Tower", "city": "Paris", "country": "France",
        "confidence": "high", "evidence": "tower",
        "lat": "48.8584", "lon": "2.2945", "geocode_status": "OK",
    }])
    out = tmp_path / "rep.csv"
    main(["report", "--dir", str(photos), "--geocoded", str(geo), "--out", str(out)])
    row = _read_csv(out)[0]
    assert row["action"] == "SKIP_HAS_GPS"
    assert row["existing_lat"] != ""
    # The fix: inferred fields are also populated for downstream --overwrite-existing
    assert row["landmark"] == "Eiffel Tower"
    assert row["inferred_lat"] == "48.8584"
    assert row["confidence"] == "high"
