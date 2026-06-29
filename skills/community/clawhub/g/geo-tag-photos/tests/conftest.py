"""Shared pytest fixtures for geo-tag-photos tests."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any

import piexif
import pytest
from PIL import Image


def _deg_to_dms_rational(deg: float) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]]:
    """Convert decimal degrees to ((d,1),(m,1),(s*10000,10000)) rationals."""
    abs_deg = abs(deg)
    d = int(abs_deg)
    m_full = (abs_deg - d) * 60
    m = int(m_full)
    s = (m_full - m) * 60
    return ((d, 1), (m, 1), (int(round(s * 10000)), 10000))


def _build_gps_ifd(lat: float, lon: float) -> dict:
    return {
        piexif.GPSIFD.GPSLatitudeRef: b"N" if lat >= 0 else b"S",
        piexif.GPSIFD.GPSLatitude: _deg_to_dms_rational(lat),
        piexif.GPSIFD.GPSLongitudeRef: b"E" if lon >= 0 else b"W",
        piexif.GPSIFD.GPSLongitude: _deg_to_dms_rational(lon),
    }


@pytest.fixture
def make_jpg():
    """Factory that writes a small JPG with optional embedded GPS."""

    def _make(tmp_path: Path, name: str = "test.jpg", gps: tuple[float, float] | None = None) -> Path:
        path = tmp_path / name
        img = Image.new("RGB", (100, 100), color=(255, 255, 255))

        if gps is None:
            img.save(path, "JPEG")
            return path

        lat, lon = gps
        exif_dict = {"0th": {}, "Exif": {}, "GPS": _build_gps_ifd(lat, lon), "1st": {}, "thumbnail": None}
        exif_bytes = piexif.dump(exif_dict)
        img.save(path, "JPEG", exif=exif_bytes)
        return path

    return _make


@pytest.fixture
def mock_nominatim(monkeypatch):
    """Stub requests.get used by the geocoder. Test populates `.responses`."""
    state = SimpleNamespace(responses={}, calls=[])

    def fake_get(url: str, params: dict | None = None, headers: dict | None = None, timeout: float | None = None) -> Any:
        state.calls.append({"url": url, "params": params or {}, "headers": headers or {}})
        query = (params or {}).get("q", "")
        payload = state.responses.get(query, [])
        if isinstance(payload, dict) and payload.get("__status__"):
            status = payload["__status__"]
            return SimpleNamespace(
                status_code=status,
                ok=False,
                json=lambda: [],
                text=payload.get("text", ""),
            )
        # success: payload is a list (possibly empty) of result dicts
        results = payload if isinstance(payload, list) else [payload]
        return SimpleNamespace(status_code=200, ok=True, json=lambda: results, text="")

    monkeypatch.setattr("requests.get", fake_get)
    return state
