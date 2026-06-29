"""Tests for EXIF read/write."""
from __future__ import annotations

from pathlib import Path

import pytest

from scripts.exif_io import EXIFError, is_jpg, read_gps, read_user_comment, write_location


def test_is_jpg_accepts_jpg_and_jpeg(tmp_path):
    assert is_jpg(tmp_path / "a.jpg")
    assert is_jpg(tmp_path / "b.JPG")
    assert is_jpg(tmp_path / "c.jpeg")
    assert is_jpg(tmp_path / "d.JPEG")


def test_is_jpg_rejects_other_formats(tmp_path):
    assert not is_jpg(tmp_path / "a.png")
    assert not is_jpg(tmp_path / "b.heic")
    assert not is_jpg(tmp_path / "c.tiff")
    assert not is_jpg(tmp_path / "d.txt")


def test_read_gps_returns_none_for_no_gps(make_jpg, tmp_path):
    p = make_jpg(tmp_path, gps=None)
    assert read_gps(p) is None


def test_read_gps_returns_coordinates_when_present(make_jpg, tmp_path):
    p = make_jpg(tmp_path, gps=(48.8584, 2.2945))
    result = read_gps(p)
    assert result is not None
    lat, lon = result
    assert abs(lat - 48.8584) < 1e-3
    assert abs(lon - 2.2945) < 1e-3


def test_read_gps_handles_southern_western_hemispheres(make_jpg, tmp_path):
    p = make_jpg(tmp_path, gps=(-22.9519, -43.2105))  # Christ the Redeemer
    lat, lon = read_gps(p)
    assert abs(lat + 22.9519) < 1e-3
    assert abs(lon + 43.2105) < 1e-3


def test_write_location_roundtrip(make_jpg, tmp_path):
    p = make_jpg(tmp_path, gps=None)
    write_location(p, lat=40.6892, lon=-74.0445,
                   description="New York, USA",
                   user_comment="confidence=high; landmark=Statue of Liberty")
    lat, lon = read_gps(p)
    assert abs(lat - 40.6892) < 1e-3
    assert abs(lon + 74.0445) < 1e-3
    assert read_user_comment(p) == "confidence=high; landmark=Statue of Liberty"


def test_write_location_preserves_chinese_in_user_comment(make_jpg, tmp_path):
    p = make_jpg(tmp_path, gps=None)
    write_location(p, lat=39.9, lon=116.4,
                   description="Beijing, China",
                   user_comment="confidence=high; landmark=长城")
    assert read_user_comment(p) == "confidence=high; landmark=长城"


def test_write_location_rejects_non_jpg(tmp_path):
    p = tmp_path / "not.png"
    p.write_bytes(b"\x89PNG\r\n\x1a\n")
    with pytest.raises(EXIFError, match="JPG"):
        write_location(p, lat=0, lon=0, description="x", user_comment="y")
