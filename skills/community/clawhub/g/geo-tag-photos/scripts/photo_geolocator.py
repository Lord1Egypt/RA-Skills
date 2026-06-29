"""geo-tag-photos CLI. Subcommands: scan / geocode / report / write / cache."""
from __future__ import annotations

import argparse
import csv
import importlib.util
import shutil
import sys
from pathlib import Path

REQUIRED = [("piexif", "piexif"), ("PIL", "Pillow"), ("requests", "requests")]

WRITE_BATCH_CAP = 500


def _is_path_inside(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def _check_dependencies() -> None:
    missing = [pip for mod, pip in REQUIRED if not importlib.util.find_spec(mod)]
    if missing:
        print(
            "[geo-tag-photos] Missing dependencies: "
            + ", ".join(missing)
            + "\nInstall with: pip install -r requirements.txt",
            file=sys.stderr,
        )
        sys.exit(2)


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="photo_geolocator", description="Recover GPS for JPG photos.")
    sub = p.add_subparsers(dest="cmd", required=True)

    scan = sub.add_parser("scan", help="Read EXIF for every file in a directory")
    scan.add_argument("--dir", required=True)
    scan.add_argument("--out", required=True)

    geo = sub.add_parser("geocode", help="Resolve landmarks to coordinates")
    geo.add_argument("--input", required=True, help="ai_results.json")
    geo.add_argument("--out", required=True, help="output CSV")
    geo.add_argument("--cache", default=None, help="override default cache path")

    rep = sub.add_parser("report", help="Merge scan + geocode into reviewable CSV")
    rep.add_argument("--dir", required=True)
    rep.add_argument("--geocoded", required=True)
    rep.add_argument("--out", required=True)

    wr = sub.add_parser("write", help="Write GPS into EXIF (default dry-run)")
    wr.add_argument("--dir", required=True)
    wr.add_argument("--csv", required=True)
    wr.add_argument("--write", action="store_true",
                    help="Actually modify files (otherwise dry-run)")
    wr.add_argument("--backup-dir", default=None,
                    help="Required with --write; must be empty or non-existent")
    wr.add_argument("--include-low", action="store_true",
                    help="Also write rows with confidence=low")
    wr.add_argument("--overwrite-existing", action="store_true",
                    help="Override existing GPS in EXIF (default: keep)")

    ca = sub.add_parser("cache", help="Inspect or clear the geocode cache")
    grp = ca.add_mutually_exclusive_group(required=True)
    grp.add_argument("--show", action="store_true")
    grp.add_argument("--clear", action="store_true")
    ca.add_argument("--cache", default=None)

    return p


def _cmd_scan(args) -> int:
    from scripts.exif_io import is_jpg, read_gps  # noqa: E402

    photo_dir = Path(args.dir)
    if not photo_dir.is_dir():
        print(f"[scan] not a directory: {photo_dir}", file=sys.stderr)
        return 2

    rows: list[dict] = []
    for entry in sorted(photo_dir.iterdir()):
        if not entry.is_file():
            continue
        if not is_jpg(entry):
            rows.append({"filename": entry.name, "has_gps": "no", "lat": "", "lon": "", "note": "NOT_JPG"})
            continue
        gps = read_gps(entry)
        if gps:
            rows.append({"filename": entry.name, "has_gps": "yes", "lat": gps[0], "lon": gps[1], "note": "OK"})
        else:
            rows.append({"filename": entry.name, "has_gps": "no", "lat": "", "lon": "", "note": "NO_GPS"})

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["filename", "has_gps", "lat", "lon", "note"])
        w.writeheader()
        w.writerows(rows)
    print(f"[scan] wrote {len(rows)} rows to {out}")
    return 0


def _default_cache_path() -> Path:
    import os
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData/Local")))
        return base / "geo-tag-photos" / "cache.json"
    return Path.home() / ".cache" / "geo-tag-photos" / "cache.json"


def _cmd_geocode(args) -> int:
    import json as _json
    from scripts.geocoder import Geocoder, GeocodeError

    in_path = Path(args.input)
    if not in_path.is_file():
        print(f"[geocode] missing input file: {in_path}", file=sys.stderr)
        return 2
    entries = _json.loads(in_path.read_text(encoding="utf-8"))
    cache_path = Path(args.cache) if args.cache else _default_cache_path()
    g = Geocoder(cache_path)

    rows = []
    for e in entries:
        landmark = e.get("landmark", "").strip()
        city = e.get("city", "").strip()
        country = e.get("country", "").strip()
        row = {
            "filename": e.get("filename", ""),
            "landmark": landmark, "city": city, "country": country,
            "confidence": e.get("confidence", "low"),
            "evidence": e.get("evidence", ""),
            "lat": "", "lon": "", "geocode_status": "",
        }
        if not (landmark and city and country):
            row["geocode_status"] = "GEOCODE_FAILED"
            rows.append(row)
            continue
        try:
            result = g.geocode(landmark, city, country)
        except GeocodeError as err:
            print(f"[geocode] network error for {row['filename']}: {err}", file=sys.stderr)
            row["geocode_status"] = "NETWORK_ERROR"
            rows.append(row)
            continue
        if result is None:
            row["geocode_status"] = "GEOCODE_FAILED"
        else:
            row["lat"], row["lon"] = result
            row["geocode_status"] = "OK"
        rows.append(row)

    g.save_cache()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["filename", "landmark", "city", "country",
                                          "confidence", "evidence", "lat", "lon", "geocode_status"])
        w.writeheader()
        w.writerows(rows)
    print(f"[geocode] wrote {len(rows)} rows to {out}")
    return 0


def _cmd_report(args) -> int:
    from scripts.exif_io import is_jpg, read_gps

    photo_dir = Path(args.dir)
    if not photo_dir.is_dir():
        print(f"[report] not a directory: {photo_dir}", file=sys.stderr)
        return 2
    geo_path = Path(args.geocoded)
    if not geo_path.is_file():
        print(f"[report] missing geocoded CSV: {geo_path}", file=sys.stderr)
        return 2

    geo_by_name: dict[str, dict] = {}
    with geo_path.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            geo_by_name[r["filename"]] = r

    rows = []
    for entry in sorted(photo_dir.iterdir()):
        if not entry.is_file():
            continue
        row = {
            "filename": entry.name,
            "existing_lat": "", "existing_lon": "",
            "landmark": "", "city": "", "country": "",
            "confidence": "", "evidence": "",
            "inferred_lat": "", "inferred_lon": "",
            "action": "",
        }
        if not is_jpg(entry):
            row["action"] = "SKIP_NOT_JPG"
            rows.append(row)
            continue
        gps = read_gps(entry)
        if gps:
            row["existing_lat"], row["existing_lon"] = gps
            # Populate inferred fields too, so downstream --overwrite-existing
            # has something to write. If no AI entry exists, fields stay empty
            # and the write step will filter the row out.
            g = geo_by_name.get(entry.name)
            if g:
                row.update({
                    "landmark": g["landmark"], "city": g["city"], "country": g["country"],
                    "confidence": g["confidence"], "evidence": g.get("evidence", ""),
                    "inferred_lat": g["lat"], "inferred_lon": g["lon"],
                })
            row["action"] = "SKIP_HAS_GPS"
            rows.append(row)
            continue
        g = geo_by_name.get(entry.name)
        if not g:
            row["action"] = "SKIP_AI_UNKNOWN"
            rows.append(row)
            continue
        row.update({
            "landmark": g["landmark"], "city": g["city"], "country": g["country"],
            "confidence": g["confidence"], "evidence": g.get("evidence", ""),
            "inferred_lat": g["lat"], "inferred_lon": g["lon"],
        })
        if g.get("confidence", "").lower() == "low":
            row["action"] = "SKIP_LOW_CONFIDENCE"
        elif g.get("geocode_status") != "OK":
            row["action"] = "SKIP_NO_GEOCODE"
        else:
            row["action"] = "WRITE"
        rows.append(row)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [
            "filename", "existing_lat", "existing_lon", "landmark", "city", "country",
            "confidence", "evidence", "inferred_lat", "inferred_lon", "action",
        ])
        w.writeheader()
        w.writerows(rows)
    write_count = sum(1 for r in rows if r["action"] == "WRITE")
    print(f"[report] {len(rows)} rows; {write_count} marked WRITE -> {out}")
    return 0


def _cmd_write(args) -> int:
    from scripts.exif_io import is_jpg, read_gps, write_location

    photo_dir = Path(args.dir)
    if not photo_dir.is_dir():
        print(f"[write] not a directory: {photo_dir}", file=sys.stderr)
        return 2
    csv_path = Path(args.csv)
    if not csv_path.is_file():
        print(f"[write] missing report CSV: {csv_path}", file=sys.stderr)
        return 2

    with csv_path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    actionable: list[dict] = []
    overwrite_count = 0
    for r in rows:
        if r["action"] == "WRITE":
            actionable.append(r)
        elif r["action"] == "SKIP_LOW_CONFIDENCE" and args.include_low:
            actionable.append(r)
        elif r["action"] == "SKIP_HAS_GPS" and args.overwrite_existing:
            # Need inference data to actually write something.
            if r.get("inferred_lat") and r.get("inferred_lon"):
                actionable.append(r)
                overwrite_count += 1

    if overwrite_count:
        print(
            f"[write] WARNING: --overwrite-existing will replace existing GPS "
            f"in {overwrite_count} photo(s).",
            file=sys.stderr,
        )

    print(f"[write] {len(actionable)} rows would be written; total rows in report: {len(rows)}")

    if not args.write:
        for r in actionable:
            print(f"  DRY-RUN: {r['filename']} -> ({r['inferred_lat']}, {r['inferred_lon']})")
        print("[write] dry-run only. Pass --write --backup-dir <path> to apply.")
        return 0

    if not args.backup_dir:
        print("[write] --write requires --backup-dir <path>", file=sys.stderr)
        return 2

    backup = Path(args.backup_dir)
    if _is_path_inside(backup, photo_dir):
        print(f"[write] backup dir cannot be inside source dir", file=sys.stderr)
        return 2
    if backup.exists():
        if not backup.is_dir():
            print(f"[write] backup path exists and is not a directory: {backup}", file=sys.stderr)
            return 2
        if any(backup.iterdir()):
            print(f"[write] backup dir is not empty: {backup}", file=sys.stderr)
            return 2

    if len(actionable) > WRITE_BATCH_CAP:
        print(f"[write] {len(actionable)} > {WRITE_BATCH_CAP} cap. Split into batches.",
              file=sys.stderr)
        return 2

    if not actionable:
        return 0

    backup.mkdir(parents=True, exist_ok=True)

    failures: list[str] = []
    for r in actionable:
        src = photo_dir / r["filename"]
        if not src.is_file() or not is_jpg(src):
            failures.append(f"missing or non-JPG: {r['filename']}")
            continue
        try:
            lat = float(r["inferred_lat"])
            lon = float(r["inferred_lon"])
        except ValueError:
            failures.append(f"bad coords for {r['filename']}")
            continue
        try:
            shutil.copy2(src, backup / r["filename"])
        except Exception as e:
            failures.append(f"backup failed for {r['filename']}: {e}")
            continue
        description = f"{r['city']}, {r['country']}"
        user_comment = (
            f"confidence={r['confidence']}; landmark={r['landmark']}; source=geo-tag-photos"
        )
        try:
            write_location(src, lat=lat, lon=lon,
                           description=description, user_comment=user_comment)
        except Exception as e:
            failures.append(f"write failed for {r['filename']}: {e}")
            continue
        try:
            rb = read_gps(src)
        except Exception as e:
            failures.append(f"verify failed for {r['filename']}: {e}")
            continue
        if rb is None or abs(rb[0] - lat) > 1e-3 or abs(rb[1] - lon) > 1e-3:
            failures.append(f"verify failed for {r['filename']}")

    if failures:
        print("[write] some operations had problems:", file=sys.stderr)
        for line in failures:
            print(f"  - {line}", file=sys.stderr)
        return 1

    print(f"[write] wrote and verified {len(actionable)} photos. Backups in {backup}.")
    return 0


def _cmd_cache(args) -> int:
    cache_path = Path(args.cache) if args.cache else _default_cache_path()
    if args.show:
        if cache_path.exists():
            print(cache_path.read_text(encoding="utf-8"))
        else:
            print("{}")
        return 0
    if args.clear:
        if cache_path.exists():
            cache_path.unlink()
        print(f"[cache] cleared {cache_path}")
        return 0
    return 2


def main(argv: list[str] | None = None) -> int:
    _check_dependencies()
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.cmd == "scan":
        return _cmd_scan(args)
    if args.cmd == "geocode":
        return _cmd_geocode(args)
    if args.cmd == "report":
        return _cmd_report(args)
    if args.cmd == "write":
        return _cmd_write(args)
    if args.cmd == "cache":
        return _cmd_cache(args)
    parser.error(f"unknown command: {args.cmd}")
    return 2


if __name__ == "__main__":
    # Allow running as `python scripts/photo_geolocator.py ...` from the skill root
    # by adding the parent directory (which contains `scripts/`) to sys.path.
    _here = Path(__file__).resolve().parent
    _root = _here.parent
    if str(_root) not in sys.path:
        sys.path.insert(0, str(_root))
    raise SystemExit(main())
