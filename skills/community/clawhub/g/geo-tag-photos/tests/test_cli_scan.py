"""Tests for the `scan` CLI subcommand."""
from __future__ import annotations

import csv
from pathlib import Path

from scripts.photo_geolocator import main


def _read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_scan_marks_no_gps_jpg(make_jpg, tmp_path):
    photos = tmp_path / "photos"
    photos.mkdir()
    make_jpg(photos, name="a.jpg", gps=None)
    out = tmp_path / "out.csv"
    code = main(["scan", "--dir", str(photos), "--out", str(out)])
    assert code == 0
    rows = _read_csv(out)
    assert len(rows) == 1
    assert rows[0]["filename"] == "a.jpg"
    assert rows[0]["has_gps"] == "no"
    assert rows[0]["note"] == "NO_GPS"


def test_scan_reports_existing_gps(make_jpg, tmp_path):
    photos = tmp_path / "photos"
    photos.mkdir()
    make_jpg(photos, name="b.jpg", gps=(48.8584, 2.2945))
    out = tmp_path / "out.csv"
    main(["scan", "--dir", str(photos), "--out", str(out)])
    row = _read_csv(out)[0]
    assert row["has_gps"] == "yes"
    assert abs(float(row["lat"]) - 48.8584) < 1e-3
    assert abs(float(row["lon"]) - 2.2945) < 1e-3
    assert row["note"] == "OK"


def test_scan_flags_non_jpg(tmp_path):
    photos = tmp_path / "photos"
    photos.mkdir()
    (photos / "weird.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    out = tmp_path / "out.csv"
    main(["scan", "--dir", str(photos), "--out", str(out)])
    row = _read_csv(out)[0]
    assert row["filename"] == "weird.png"
    assert row["note"] == "NOT_JPG"


def test_scan_returns_2_for_missing_dir(tmp_path):
    out = tmp_path / "out.csv"
    code = main(["scan", "--dir", str(tmp_path / "nope"), "--out", str(out)])
    assert code == 2
