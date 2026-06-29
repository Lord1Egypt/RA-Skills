"""Verify the end-to-end pipeline result.

Reports the geographic distance between each photo's written GPS and the
canonical coordinate. Pass criteria: all 8 within 5 km, backup intact.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

# Allow running from skill root or e2e/
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))

from scripts.exif_io import read_gps  # noqa: E402


THRESHOLD_KM = 5.0


def haversine_km(a: tuple[float, float], b: tuple[float, float]) -> float:
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    d_lat = lat2 - lat1
    d_lon = lon2 - lon1
    h = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(h))


def main() -> int:
    canonical = json.loads((HERE / "canonical_coords.json").read_text(encoding="utf-8"))
    landmarks = HERE / "landmarks"
    backup = HERE / "landmarks.bak"

    if not landmarks.is_dir():
        print(f"[fail] missing {landmarks}; run fetch_landmarks.py first", file=sys.stderr)
        return 2

    print(f"{'file':<22} {'expected':<22} {'got':<22} {'dist_km':>8}  status")
    fail = 0
    for name, ref in canonical.items():
        photo = landmarks / name
        if not photo.exists():
            print(f"{name:<22} {'-':<22} {'MISSING':<22} {'-':>8}  FAIL")
            fail += 1
            continue
        got = read_gps(photo)
        if got is None:
            print(f"{name:<22} ({ref['lat']:.4f}, {ref['lon']:.4f}) {'NO_GPS':<22} {'-':>8}  FAIL")
            fail += 1
            continue
        d = haversine_km((ref["lat"], ref["lon"]), got)
        ok = d <= THRESHOLD_KM
        status = "OK" if ok else "FAIL"
        print(f"{name:<22} ({ref['lat']:7.4f}, {ref['lon']:8.4f}) ({got[0]:7.4f}, {got[1]:8.4f}) {d:8.2f}  {status}")
        if not ok:
            fail += 1

    # backup integrity
    if backup.is_dir():
        backup_files = sorted(p.name for p in backup.iterdir() if p.suffix.lower() in (".jpg", ".jpeg"))
        bad_backup = [n for n in backup_files if read_gps(backup / n) is not None]
        if bad_backup:
            print(f"[fail] backup files unexpectedly have GPS: {bad_backup}")
            fail += len(bad_backup)
        if len(backup_files) != len(canonical):
            print(f"[fail] backup count {len(backup_files)} != expected {len(canonical)}")
            fail += 1
    else:
        print("[warn] no backup dir to verify (skip if you only ran dry-run)")

    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
