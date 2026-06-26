#!/usr/bin/env python3
import argparse
import hashlib
import json
import sqlite3
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def file_sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS daily_health_summary (
            date TEXT NOT NULL,
            source TEXT NOT NULL,
            steps INTEGER,
            active_zone_minutes INTEGER,
            calories_out INTEGER,
            distance_km REAL,
            floors INTEGER,
            resting_hr INTEGER,
            hrv_rmssd REAL,
            sleep_minutes INTEGER,
            sleep_efficiency INTEGER,
            sleep_score INTEGER,
            data_quality TEXT,
            source_payload_hash TEXT,
            ingested_at TEXT NOT NULL,
            PRIMARY KEY (date, source)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS ingest_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            started_at TEXT NOT NULL,
            finished_at TEXT,
            status TEXT NOT NULL,
            details_json TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS apple_health_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            metric TEXT NOT NULL,
            value REAL,
            unit TEXT,
            start_at TEXT,
            end_at TEXT,
            source_name TEXT,
            device TEXT,
            raw_json TEXT,
            imported_at TEXT NOT NULL
        )
        """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_apple_metric_start ON apple_health_records(metric, start_at)")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS apple_import_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL,
            file_sha256 TEXT NOT NULL UNIQUE,
            imported_at TEXT NOT NULL,
            records INTEGER NOT NULL DEFAULT 0,
            notes TEXT
        )
        """
    )
    return conn


def _insert_run(conn: sqlite3.Connection, source: str, details: Dict) -> int:
    conn.execute(
        "INSERT INTO ingest_runs(source, started_at, status, details_json) VALUES (?,?,?,?)",
        (source, utc_now_iso(), "running", json.dumps(details)),
    )
    return conn.execute("SELECT last_insert_rowid()").fetchone()[0]


def _finish_run(conn: sqlite3.Connection, run_id: int, status: str, details: Dict) -> None:
    conn.execute(
        "UPDATE ingest_runs SET finished_at=?, status=?, details_json=? WHERE id=?",
        (utc_now_iso(), status, json.dumps(details), run_id),
    )


def run_init(conn: sqlite3.Connection) -> Dict:
    conn.commit()
    return {"ok": True, "operation": "init"}


def import_fitbit_cache(conn: sqlite3.Connection, fitbit_db_path: Path, start: Optional[str], end: Optional[str]) -> Dict:
    run_id = _insert_run(conn, "fitbit", {"fitbit_db": str(fitbit_db_path), "start": start, "end": end})

    src = sqlite3.connect(str(fitbit_db_path))
    src.row_factory = sqlite3.Row

    where = []
    params = []
    if start:
        where.append("date >= ?")
        params.append(start)
    if end:
        where.append("date <= ?")
        params.append(end)
    where_sql = ("WHERE " + " AND ".join(where)) if where else ""

    q = f"""
    SELECT date, steps, active_zone_minutes, calories_out, distance_km, floors,
           resting_hr, hrv_rmssd, sleep_minutes, sleep_efficiency, sleep_score, data_quality
    FROM daily_metrics
    {where_sql}
    ORDER BY date ASC
    """
    rows = src.execute(q, params).fetchall()

    upserts = 0
    for r in rows:
        conn.execute(
            """
            INSERT INTO daily_health_summary(
                date, source, steps, active_zone_minutes, calories_out, distance_km, floors,
                resting_hr, hrv_rmssd, sleep_minutes, sleep_efficiency, sleep_score,
                data_quality, source_payload_hash, ingested_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(date, source) DO UPDATE SET
                steps=excluded.steps,
                active_zone_minutes=excluded.active_zone_minutes,
                calories_out=excluded.calories_out,
                distance_km=excluded.distance_km,
                floors=excluded.floors,
                resting_hr=excluded.resting_hr,
                hrv_rmssd=excluded.hrv_rmssd,
                sleep_minutes=excluded.sleep_minutes,
                sleep_efficiency=excluded.sleep_efficiency,
                sleep_score=excluded.sleep_score,
                data_quality=excluded.data_quality,
                ingested_at=excluded.ingested_at
            """,
            (
                r["date"],
                "fitbit",
                r["steps"],
                r["active_zone_minutes"],
                r["calories_out"],
                r["distance_km"],
                r["floors"],
                r["resting_hr"],
                r["hrv_rmssd"],
                r["sleep_minutes"],
                r["sleep_efficiency"],
                r["sleep_score"],
                r["data_quality"],
                None,
                utc_now_iso(),
            ),
        )
        upserts += 1

    _finish_run(
        conn,
        run_id,
        "ok",
        {"rows": upserts, "start": start, "end": end, "fitbit_db": str(fitbit_db_path)},
    )
    conn.commit()
    src.close()
    return {"ok": True, "operation": "import-fitbit-cache", "rows": upserts, "start": start, "end": end}


def import_apple_export(conn: sqlite3.Connection, export_xml: Path, limit: int, force: bool = False) -> Dict:
    xml_hash = file_sha256(export_xml)
    existing = conn.execute(
        "SELECT id, imported_at, records FROM apple_import_files WHERE file_sha256=?",
        (xml_hash,),
    ).fetchone()
    if existing and not force:
        return {
            "ok": True,
            "operation": "import-apple-export",
            "skipped": True,
            "reason": "same_file_already_imported",
            "file_sha256": xml_hash,
            "first_imported_at": existing[1],
            "first_records": existing[2],
        }

    run_id = _insert_run(conn, "apple_health", {"export_xml": str(export_xml), "limit": limit, "force": force, "file_sha256": xml_hash})

    metric_map = {
        "HKQuantityTypeIdentifierStepCount": "steps",
        "HKQuantityTypeIdentifierHeartRate": "heart_rate",
        "HKQuantityTypeIdentifierRestingHeartRate": "resting_hr",
        "HKQuantityTypeIdentifierHeartRateVariabilitySDNN": "hrv_sdnn",
        "HKCategoryTypeIdentifierSleepAnalysis": "sleep",
    }

    count = 0
    for event, elem in ET.iterparse(str(export_xml), events=("end",)):
        if elem.tag != "Record":
            continue
        hk_type = elem.attrib.get("type", "")
        metric = metric_map.get(hk_type)
        if not metric:
            elem.clear()
            continue
        raw = {
            "type": hk_type,
            "unit": elem.attrib.get("unit"),
            "value": elem.attrib.get("value"),
            "sourceName": elem.attrib.get("sourceName"),
            "device": elem.attrib.get("device"),
            "startDate": elem.attrib.get("startDate"),
            "endDate": elem.attrib.get("endDate"),
        }
        value = None
        try:
            value = float(raw["value"]) if raw["value"] is not None else None
        except Exception:
            value = None

        conn.execute(
            """
            INSERT INTO apple_health_records(metric, value, unit, start_at, end_at, source_name, device, raw_json, imported_at)
            VALUES (?,?,?,?,?,?,?,?,?)
            """,
            (
                metric,
                value,
                raw.get("unit"),
                raw.get("startDate"),
                raw.get("endDate"),
                raw.get("sourceName"),
                raw.get("device"),
                json.dumps(raw),
                utc_now_iso(),
            ),
        )
        count += 1
        elem.clear()
        if limit and count >= limit:
            break

    conn.execute(
        """
        INSERT INTO apple_import_files(file_path, file_sha256, imported_at, records, notes)
        VALUES (?,?,?,?,?)
        ON CONFLICT(file_sha256) DO UPDATE SET
            imported_at=excluded.imported_at,
            records=excluded.records,
            notes=excluded.notes
        """,
        (str(export_xml), xml_hash, utc_now_iso(), count, "forced_reimport" if existing and force else "initial_import"),
    )

    _finish_run(conn, run_id, "ok", {"records": count, "limit": limit, "export_xml": str(export_xml), "file_sha256": xml_hash})
    conn.commit()
    return {"ok": True, "operation": "import-apple-export", "records": count, "limit": limit, "file_sha256": xml_hash}


def aggregate_apple_daily(conn: sqlite3.Connection, start: Optional[str], end: Optional[str]) -> Dict:
    run_id = _insert_run(conn, "apple_health_aggregate", {"start": start, "end": end})

    where = ["start_at IS NOT NULL"]
    params = []
    if start:
        where.append("substr(start_at,1,10) >= ?")
        params.append(start)
    if end:
        where.append("substr(start_at,1,10) <= ?")
        params.append(end)
    where_sql = " AND ".join(where)

    q = f"""
    SELECT
      substr(start_at,1,10) AS d,
      CAST(SUM(CASE WHEN metric='steps' THEN COALESCE(value,0) ELSE 0 END) AS INTEGER) AS steps,
      CAST(ROUND(AVG(CASE WHEN metric='resting_hr' AND value > 0 THEN value END)) AS INTEGER) AS resting_hr,
      AVG(CASE WHEN metric='hrv_sdnn' AND value > 0 THEN value END) AS hrv_rmssd,
      CAST(SUM(CASE WHEN metric='sleep' AND end_at IS NOT NULL
              THEN (julianday(end_at) - julianday(start_at))*1440 ELSE 0 END) AS INTEGER) AS sleep_minutes,
      COUNT(*) AS n
    FROM apple_health_records
    WHERE {where_sql}
    GROUP BY d
    ORDER BY d ASC
    """

    rows = conn.execute(q, params).fetchall()
    upserts = 0
    for d, steps, resting_hr, hrv_rmssd, sleep_minutes, _n in rows:
        present = sum(
            1
            for x in (
                steps if steps and steps > 0 else None,
                resting_hr,
                hrv_rmssd,
                sleep_minutes if sleep_minutes and sleep_minutes > 0 else None,
            )
            if x is not None
        )
        quality = "complete" if present >= 3 else ("partial" if present >= 1 else "degraded")

        conn.execute(
            """
            INSERT INTO daily_health_summary(
                date, source, steps, active_zone_minutes, calories_out, distance_km, floors,
                resting_hr, hrv_rmssd, sleep_minutes, sleep_efficiency, sleep_score,
                data_quality, source_payload_hash, ingested_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(date, source) DO UPDATE SET
                steps=excluded.steps,
                resting_hr=excluded.resting_hr,
                hrv_rmssd=excluded.hrv_rmssd,
                sleep_minutes=excluded.sleep_minutes,
                data_quality=excluded.data_quality,
                ingested_at=excluded.ingested_at
            """,
            (
                d,
                "apple_health",
                int(steps or 0),
                None,
                None,
                None,
                None,
                resting_hr,
                hrv_rmssd,
                int(sleep_minutes or 0),
                None,
                None,
                quality,
                None,
                utc_now_iso(),
            ),
        )
        upserts += 1

    _finish_run(conn, run_id, "ok", {"rows": upserts, "start": start, "end": end})
    conn.commit()
    return {"ok": True, "operation": "aggregate-apple-daily", "rows": upserts, "start": start, "end": end}


def stats(conn: sqlite3.Connection) -> Dict:
    out = {}
    out["daily_health_summary"] = conn.execute("SELECT COUNT(*) FROM daily_health_summary").fetchone()[0]
    out["apple_health_records"] = conn.execute("SELECT COUNT(*) FROM apple_health_records").fetchone()[0]
    out["ingest_runs"] = conn.execute("SELECT COUNT(*) FROM ingest_runs").fetchone()[0]
    out["sources"] = [
        {"source": r[0], "count": r[1]}
        for r in conn.execute("SELECT source, COUNT(*) FROM daily_health_summary GROUP BY source ORDER BY source").fetchall()
    ]
    return {"ok": True, "operation": "stats", "stats": out}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(PROJECT_ROOT / "assets" / "health_unified.sqlite3"))
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init")

    fc = sub.add_parser("import-fitbit-cache")
    fc.add_argument("--fitbit-db", default=str(PROJECT_ROOT / "assets" / "fitbit_metrics.sqlite3"))
    fc.add_argument("--start")
    fc.add_argument("--end")

    ah = sub.add_parser("import-apple-export")
    ah.add_argument("--xml", required=True)
    ah.add_argument("--limit", type=int, default=0)
    ah.add_argument("--force", action="store_true", help="Allow re-import even if same export file hash was already imported")

    ad = sub.add_parser("aggregate-apple-daily")
    ad.add_argument("--start")
    ad.add_argument("--end")

    sub.add_parser("stats")

    args = ap.parse_args()
    conn = connect(Path(args.db))

    if args.cmd == "init":
        result = run_init(conn)
    elif args.cmd == "import-fitbit-cache":
        result = import_fitbit_cache(conn, Path(args.fitbit_db), args.start, args.end)
    elif args.cmd == "import-apple-export":
        result = import_apple_export(conn, Path(args.xml), args.limit, force=args.force)
    elif args.cmd == "aggregate-apple-daily":
        result = aggregate_apple_daily(conn, args.start, args.end)
    elif args.cmd == "stats":
        result = stats(conn)
    else:
        result = {"ok": False, "error": "unknown command"}

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    main()
