"""Tests for the `write` CLI subcommand: dry-run, safety, write+verify."""
from __future__ import annotations

import csv
from pathlib import Path

from scripts.exif_io import read_gps
from scripts.photo_geolocator import main


def _make_report(path: Path, rows: list[dict]) -> None:
    fields = ["filename", "existing_lat", "existing_lon", "landmark", "city", "country",
              "confidence", "evidence", "inferred_lat", "inferred_lon", "action"]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def _row(filename, lat, lon, action="WRITE", confidence="high", landmark="X", city="Y", country="Z"):
    return {
        "filename": filename, "existing_lat": "", "existing_lon": "",
        "landmark": landmark, "city": city, "country": country,
        "confidence": confidence, "evidence": "",
        "inferred_lat": str(lat), "inferred_lon": str(lon),
        "action": action,
    }


def test_write_default_is_dry_run(make_jpg, tmp_path):
    photos = tmp_path / "p"; photos.mkdir()
    p = make_jpg(photos, name="a.jpg", gps=None)
    rep = tmp_path / "rep.csv"
    _make_report(rep, [_row("a.jpg", 48.8584, 2.2945)])
    mtime = p.stat().st_mtime
    code = main(["write", "--dir", str(photos), "--csv", str(rep)])
    assert code == 0
    assert p.stat().st_mtime == mtime
    assert read_gps(p) is None


def test_write_requires_backup_dir(make_jpg, tmp_path):
    photos = tmp_path / "p"; photos.mkdir()
    make_jpg(photos, name="a.jpg", gps=None)
    rep = tmp_path / "rep.csv"
    _make_report(rep, [_row("a.jpg", 1.0, 2.0)])
    code = main(["write", "--dir", str(photos), "--csv", str(rep), "--write"])
    assert code == 2


def test_write_rejects_non_empty_backup_dir(make_jpg, tmp_path):
    photos = tmp_path / "p"; photos.mkdir()
    make_jpg(photos, name="a.jpg", gps=None)
    rep = tmp_path / "rep.csv"
    _make_report(rep, [_row("a.jpg", 1.0, 2.0)])
    backup = tmp_path / "bak"; backup.mkdir()
    (backup / "junk.txt").write_text("x")
    code = main(["write", "--dir", str(photos), "--csv", str(rep),
                 "--write", "--backup-dir", str(backup)])
    assert code == 2


def test_write_rejects_backup_path_that_is_a_file(make_jpg, tmp_path):
    photos = tmp_path / "p"; photos.mkdir()
    make_jpg(photos, name="a.jpg", gps=None)
    rep = tmp_path / "rep.csv"
    _make_report(rep, [_row("a.jpg", 1.0, 2.0)])
    backup_file = tmp_path / "bak"
    backup_file.write_text("not a dir")  # regular file, not a directory
    code = main(["write", "--dir", str(photos), "--csv", str(rep),
                 "--write", "--backup-dir", str(backup_file)])
    assert code == 2


def test_write_rejects_backup_inside_source(make_jpg, tmp_path):
    photos = tmp_path / "p"; photos.mkdir()
    make_jpg(photos, name="a.jpg", gps=None)
    rep = tmp_path / "rep.csv"
    _make_report(rep, [_row("a.jpg", 1.0, 2.0)])
    code = main(["write", "--dir", str(photos), "--csv", str(rep),
                 "--write", "--backup-dir", str(photos / "inside")])
    assert code == 2


def test_write_rejects_over_500_writes(make_jpg, tmp_path):
    photos = tmp_path / "p"; photos.mkdir()
    rows = []
    for i in range(501):
        name = f"f{i}.jpg"
        make_jpg(photos, name=name, gps=None)
        rows.append(_row(name, 1.0, 2.0))
    rep = tmp_path / "rep.csv"
    _make_report(rep, rows)
    code = main(["write", "--dir", str(photos), "--csv", str(rep),
                 "--write", "--backup-dir", str(tmp_path / "bak")])
    assert code == 2


def test_write_performs_backup_and_writes(make_jpg, tmp_path):
    photos = tmp_path / "p"; photos.mkdir()
    p = make_jpg(photos, name="a.jpg", gps=None)
    rep = tmp_path / "rep.csv"
    _make_report(rep, [_row("a.jpg", 48.8584, 2.2945)])
    backup = tmp_path / "bak"
    code = main(["write", "--dir", str(photos), "--csv", str(rep),
                 "--write", "--backup-dir", str(backup)])
    assert code == 0
    # original is now tagged
    lat, lon = read_gps(p)
    assert abs(lat - 48.8584) < 1e-3
    # backup copy exists and is untagged (matches the input we made earlier)
    assert (backup / "a.jpg").is_file()
    assert read_gps(backup / "a.jpg") is None


def test_write_skips_non_write_actions(make_jpg, tmp_path):
    photos = tmp_path / "p"; photos.mkdir()
    p = make_jpg(photos, name="a.jpg", gps=None)
    rep = tmp_path / "rep.csv"
    _make_report(rep, [_row("a.jpg", 1.0, 2.0, action="SKIP_LOW_CONFIDENCE", confidence="low")])
    backup = tmp_path / "bak"
    code = main(["write", "--dir", str(photos), "--csv", str(rep),
                 "--write", "--backup-dir", str(backup)])
    assert code == 0
    assert read_gps(p) is None
    # No backup created when there's nothing to write
    assert not backup.exists() or not any(backup.iterdir())


def test_write_overwrite_existing_replaces_gps(make_jpg, tmp_path):
    """End-to-end: photo has GPS, AI has inference, --overwrite-existing replaces it."""
    photos = tmp_path / "p"; photos.mkdir()
    p = make_jpg(photos, name="a.jpg", gps=(10.0, 20.0))  # existing GPS
    rep = tmp_path / "rep.csv"
    # Build a SKIP_HAS_GPS row with FULL inferred data (matches what fixed _cmd_report produces)
    fields = ["filename", "existing_lat", "existing_lon", "landmark", "city", "country",
              "confidence", "evidence", "inferred_lat", "inferred_lon", "action"]
    row = {
        "filename": "a.jpg",
        "existing_lat": "10.0", "existing_lon": "20.0",
        "landmark": "Eiffel Tower", "city": "Paris", "country": "France",
        "confidence": "high", "evidence": "tower visible",
        "inferred_lat": "48.8584", "inferred_lon": "2.2945",
        "action": "SKIP_HAS_GPS",
    }
    import csv
    with rep.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerow(row)
    backup = tmp_path / "bak"
    code = main(["write", "--dir", str(photos), "--csv", str(rep),
                 "--write", "--backup-dir", str(backup), "--overwrite-existing"])
    assert code == 0
    from scripts.exif_io import read_gps
    new = read_gps(p)
    assert new is not None
    assert abs(new[0] - 48.8584) < 1e-3
    assert abs(new[1] - 2.2945) < 1e-3
    # Backup retains the original GPS
    bak_gps = read_gps(backup / "a.jpg")
    assert bak_gps is not None
    assert abs(bak_gps[0] - 10.0) < 1e-3


def test_write_overwrite_existing_skips_when_no_inference(make_jpg, tmp_path):
    """SKIP_HAS_GPS without inference data should not be written even with --overwrite-existing."""
    photos = tmp_path / "p"; photos.mkdir()
    p = make_jpg(photos, name="a.jpg", gps=(10.0, 20.0))
    rep = tmp_path / "rep.csv"
    fields = ["filename", "existing_lat", "existing_lon", "landmark", "city", "country",
              "confidence", "evidence", "inferred_lat", "inferred_lon", "action"]
    row = {
        "filename": "a.jpg",
        "existing_lat": "10.0", "existing_lon": "20.0",
        "landmark": "", "city": "", "country": "",
        "confidence": "", "evidence": "",
        "inferred_lat": "", "inferred_lon": "",
        "action": "SKIP_HAS_GPS",
    }
    import csv
    with rep.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerow(row)
    backup = tmp_path / "bak"
    code = main(["write", "--dir", str(photos), "--csv", str(rep),
                 "--write", "--backup-dir", str(backup), "--overwrite-existing"])
    assert code == 0
    from scripts.exif_io import read_gps
    # Original GPS preserved (no inference to apply)
    gps = read_gps(p)
    assert abs(gps[0] - 10.0) < 1e-3
