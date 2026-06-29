"""EXIF read/write for JPG photos. Only touches GPS + ImageDescription + UserComment."""
from __future__ import annotations

from pathlib import Path

import piexif


class EXIFError(Exception):
    """Raised for non-JPG input or unrecoverable EXIF problems."""


_USER_COMMENT_PREFIX = b"UNICODE\x00"


def is_jpg(path: Path) -> bool:
    return path.suffix.lower() in (".jpg", ".jpeg")


def _rational_to_float(rat: tuple[int, int]) -> float:
    num, den = rat
    return num / den if den else 0.0


def _dms_to_decimal(dms: tuple, ref: bytes) -> float:
    d = _rational_to_float(dms[0])
    m = _rational_to_float(dms[1])
    s = _rational_to_float(dms[2])
    val = d + m / 60.0 + s / 3600.0
    if ref in (b"S", b"W"):
        val = -val
    return val


def _decimal_to_dms_rational(deg: float) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]]:
    abs_deg = abs(deg)
    d = int(abs_deg)
    m_full = (abs_deg - d) * 60
    m = int(m_full)
    s = (m_full - m) * 60
    return ((d, 1), (m, 1), (int(round(s * 10000)), 10000))


def read_gps(path: Path) -> tuple[float, float] | None:
    if not is_jpg(path):
        return None
    try:
        exif = piexif.load(str(path))
    except Exception:
        return None
    gps = exif.get("GPS") or {}
    lat_dms = gps.get(piexif.GPSIFD.GPSLatitude)
    lon_dms = gps.get(piexif.GPSIFD.GPSLongitude)
    lat_ref = gps.get(piexif.GPSIFD.GPSLatitudeRef)
    lon_ref = gps.get(piexif.GPSIFD.GPSLongitudeRef)
    if not (lat_dms and lon_dms and lat_ref and lon_ref):
        return None
    lat = _dms_to_decimal(lat_dms, lat_ref)
    lon = _dms_to_decimal(lon_dms, lon_ref)
    if lat == 0.0 and lon == 0.0:
        return None
    return (lat, lon)


def write_location(
    path: Path,
    *,
    lat: float,
    lon: float,
    description: str,
    user_comment: str,
) -> None:
    if not is_jpg(path):
        raise EXIFError(f"not a JPG: {path}")
    try:
        exif = piexif.load(str(path))
    except Exception as e:
        raise EXIFError(f"cannot read EXIF from {path}: {e}") from e

    gps = exif.get("GPS") or {}
    gps[piexif.GPSIFD.GPSLatitudeRef] = b"N" if lat >= 0 else b"S"
    gps[piexif.GPSIFD.GPSLatitude] = _decimal_to_dms_rational(lat)
    gps[piexif.GPSIFD.GPSLongitudeRef] = b"E" if lon >= 0 else b"W"
    gps[piexif.GPSIFD.GPSLongitude] = _decimal_to_dms_rational(lon)
    exif["GPS"] = gps

    zeroth = exif.get("0th") or {}
    zeroth[piexif.ImageIFD.ImageDescription] = description.encode("ascii", errors="replace")
    exif["0th"] = zeroth

    exif_section = exif.get("Exif") or {}
    exif_section[piexif.ExifIFD.UserComment] = (
        _USER_COMMENT_PREFIX + user_comment.encode("utf-16-le")
    )
    exif["Exif"] = exif_section

    exif_bytes = piexif.dump(exif)
    piexif.insert(exif_bytes, str(path))


def read_user_comment(path: Path) -> str | None:
    if not is_jpg(path):
        return None
    try:
        exif = piexif.load(str(path))
    except Exception:
        return None
    raw = (exif.get("Exif") or {}).get(piexif.ExifIFD.UserComment)
    if not raw:
        return None
    if raw.startswith(_USER_COMMENT_PREFIX):
        return raw[len(_USER_COMMENT_PREFIX):].decode("utf-16-le", errors="replace")
    return raw.decode("utf-8", errors="replace")
