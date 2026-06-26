#!/usr/bin/env python3
"""
BirdWeather PUC — data access and logging tool.

Usage:
  python3 birdweather.py summary    --token TOKEN
  python3 birdweather.py detections --token TOKEN [--limit N]
  python3 birdweather.py species    --token TOKEN [--period day|week|month]
  python3 birdweather.py sensors    --token TOKEN
  python3 birdweather.py log        --token TOKEN --db PATH
  python3 birdweather.py new-species --token TOKEN --db PATH
"""

import argparse
import json
import sqlite3
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from typing import Any


BASE_URL = "https://app.birdweather.com/api/v1/stations"
TIMEOUT = 10


def fetch(token: str, path: str, params: dict[str, str] | None = None) -> dict[str, Any]:
    """Fetch JSON from BirdWeather API. Raises RuntimeError on failure."""
    url = f"{BASE_URL}/{token}/{path}"
    if params:
        query = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{url}?{query}"
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code} fetching {path}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error fetching {path}: {exc.reason}") from exc


def cmd_summary(token: str) -> dict[str, Any]:
    """Today's detection count, species count, top 10 birds, station status."""
    stats_data = fetch(token, "stats", {"period": "day"})
    species_data = fetch(token, "species", {"period": "day", "limit": "10"})
    weather_data = fetch(token, "weather")

    station = weather_data.get("station", {})
    puc = weather_data.get("weather", {}).get("puc") or {}

    top_species = []
    for s in species_data.get("species", []):
        top_species.append({
            "commonName": s.get("commonName", ""),
            "scientificName": s.get("scientificName", ""),
            "detections": (s.get("detections") or {}).get("total", 0),
            "color": s.get("color", ""),
            "thumbnailUrl": s.get("thumbnailUrl", ""),
        })

    sensors = _parse_sensors(puc)

    return {
        "stationName": station.get("name", ""),
        "live": station.get("live", False),
        "detectionsToday": stats_data.get("detections", 0),
        "speciesToday": stats_data.get("species", 0),
        "topSpecies": top_species,
        "sensors": sensors,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def cmd_detections(token: str, limit: int = 10) -> list[dict[str, Any]]:
    """Recent detections with species info, confidence, and audio URL."""
    data = fetch(token, "detections", {"limit": str(limit)})
    results = []
    for d in data.get("detections", []):
        sp = d.get("species") or {}
        results.append({
            "id": d.get("id"),
            "timestamp": d.get("timestamp", ""),
            "confidence": round(d.get("confidence", 0), 4),
            "certainty": d.get("certainty", ""),
            "commonName": sp.get("commonName", ""),
            "scientificName": sp.get("scientificName", ""),
            "color": sp.get("color", ""),
            "thumbnailUrl": sp.get("thumbnailUrl", ""),
            "soundscapeUrl": (d.get("soundscape") or {}).get("url", ""),
        })
    return results


def cmd_species(token: str, period: str = "week") -> list[dict[str, Any]]:
    """Species list for a given period, sorted by detection count."""
    data = fetch(token, "species", {"period": period, "limit": "50"})
    results = []
    for s in data.get("species", []):
        results.append({
            "id": s.get("id"),
            "commonName": s.get("commonName", ""),
            "scientificName": s.get("scientificName", ""),
            "detections": (s.get("detections") or {}).get("total", 0),
            "color": s.get("color", ""),
            "thumbnailUrl": s.get("thumbnailUrl", ""),
            "latestDetectionAt": s.get("latestDetectionAt", ""),
        })
    return sorted(results, key=lambda x: x["detections"], reverse=True)


def cmd_sensors(token: str) -> dict[str, Any]:
    """Current environmental sensor readings from the PUC."""
    data = fetch(token, "weather")
    puc = (data.get("weather") or {}).get("puc") or {}
    sensors = _parse_sensors(puc)
    if not sensors:
        return {"error": "No sensor data available"}
    return sensors


def cmd_log(token: str, db_path: str) -> dict[str, Any]:
    """Log current sensor snapshot and update species catalog in SQLite."""
    weather_data = fetch(token, "weather")
    puc = (weather_data.get("weather") or {}).get("puc") or {}
    sensors = _parse_sensors(puc)

    species_data = fetch(token, "species", {"period": "month", "limit": "100"})

    db = _open_db(db_path)
    try:
        sensor_id = None
        if sensors:
            now = datetime.now(timezone.utc).isoformat()
            cur = db.execute(
                """INSERT INTO birdweather_sensor_history
                   (recorded_at, temp_f, humidity, pressure, aqi, eco2, sound_db, voc)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    now,
                    sensors.get("tempF"),
                    sensors.get("humidity"),
                    sensors.get("pressure"),
                    sensors.get("aqi"),
                    sensors.get("eco2"),
                    sensors.get("soundDb"),
                    sensors.get("voc"),
                ),
            )
            sensor_id = cur.lastrowid

        updated = 0
        inserted = 0
        for s in species_data.get("species", []):
            sp_id = s.get("id")
            if not sp_id:
                continue
            count = (s.get("detections") or {}).get("total", 0)
            existing = db.execute(
                "SELECT species_id FROM birdweather_species WHERE species_id = ?", (sp_id,)
            ).fetchone()
            if existing:
                db.execute(
                    "UPDATE birdweather_species SET detection_count = ? WHERE species_id = ?",
                    (count, sp_id),
                )
                updated += 1
            else:
                db.execute(
                    """INSERT INTO birdweather_species
                       (species_id, common_name, scientific_name, color, thumbnail_url,
                        first_detected_at, detection_count)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        sp_id,
                        s.get("commonName", ""),
                        s.get("scientificName", ""),
                        s.get("color", ""),
                        s.get("thumbnailUrl", ""),
                        s.get("latestDetectionAt", ""),
                        count,
                    ),
                )
                inserted += 1

        db.commit()
        return {
            "sensorRowId": sensor_id,
            "speciesInserted": inserted,
            "speciesUpdated": updated,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    finally:
        db.close()


def cmd_new_species(token: str, db_path: str) -> list[dict[str, Any]]:
    """Return species detected today that are not in the local DB catalog."""
    live = fetch(token, "species", {"period": "day", "limit": "100"})
    live_ids = {s.get("id") for s in live.get("species", []) if s.get("id")}

    db = _open_db(db_path)
    try:
        known_ids = {
            row[0]
            for row in db.execute("SELECT species_id FROM birdweather_species").fetchall()
        }
    finally:
        db.close()

    new_ids = live_ids - known_ids
    new_species = []
    for s in live.get("species", []):
        if s.get("id") in new_ids:
            new_species.append({
                "id": s.get("id"),
                "commonName": s.get("commonName", ""),
                "scientificName": s.get("scientificName", ""),
                "detections": (s.get("detections") or {}).get("total", 0),
                "color": s.get("color", ""),
                "thumbnailUrl": s.get("thumbnailUrl", ""),
                "latestDetectionAt": s.get("latestDetectionAt", ""),
            })
    return new_species


def _parse_sensors(puc: dict[str, Any]) -> dict[str, Any] | None:
    """Convert raw PUC sensor dict to clean named fields."""
    if not puc:
        return None
    temp_c = puc.get("temperature")
    temp_f = round((temp_c * 9 / 5) + 32, 1) if temp_c is not None else None
    return {
        "tempF": temp_f,
        "tempC": round(temp_c, 1) if temp_c is not None else None,
        "humidity": round(puc["humidity"], 1) if puc.get("humidity") is not None else None,
        "pressure": round(puc["barometricPressure"], 1) if puc.get("barometricPressure") is not None else None,
        "aqi": round(puc["aqi"], 1) if puc.get("aqi") is not None else None,
        "eco2": round(puc["eco2"]) if puc.get("eco2") is not None else None,
        "soundDb": round(puc["soundPressureLevel"], 1) if puc.get("soundPressureLevel") is not None else None,
        "voc": puc.get("voc"),
    }


def _open_db(path: str) -> sqlite3.Connection:
    """Open SQLite DB and create tables if needed."""
    db = sqlite3.connect(path)
    db.execute("""
        CREATE TABLE IF NOT EXISTS birdweather_species (
            species_id    INTEGER PRIMARY KEY,
            common_name   TEXT,
            scientific_name TEXT,
            color         TEXT,
            thumbnail_url TEXT,
            first_detected_at TEXT,
            detection_count INTEGER DEFAULT 0
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS birdweather_sensor_history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            recorded_at TEXT,
            temp_f      REAL,
            humidity    REAL,
            pressure    REAL,
            aqi         REAL,
            eco2        REAL,
            sound_db    REAL,
            voc         REAL
        )
    """)
    db.commit()
    return db


def main() -> None:
    parser = argparse.ArgumentParser(description="BirdWeather PUC data tool")
    parser.add_argument("command", choices=["summary", "detections", "species", "sensors", "log", "new-species"])
    parser.add_argument("--token", required=True, help="BirdWeather station token")
    parser.add_argument("--limit", type=int, default=10, help="Number of detections to fetch")
    parser.add_argument("--period", default="week", choices=["day", "week", "month"], help="Time period for species")
    parser.add_argument("--db", help="Path to SQLite database file")
    args = parser.parse_args()

    try:
        if args.command == "summary":
            result = cmd_summary(args.token)
        elif args.command == "detections":
            result = cmd_detections(args.token, args.limit)
        elif args.command == "species":
            result = cmd_species(args.token, args.period)
        elif args.command == "sensors":
            result = cmd_sensors(args.token)
        elif args.command == "log":
            if not args.db:
                print(json.dumps({"error": "--db required for log command"}))
                sys.exit(1)
            result = cmd_log(args.token, args.db)
        elif args.command == "new-species":
            if not args.db:
                print(json.dumps({"error": "--db required for new-species command"}))
                sys.exit(1)
            result = cmd_new_species(args.token, args.db)
        else:
            print(json.dumps({"error": f"Unknown command: {args.command}"}))
            sys.exit(1)

        print(json.dumps(result, indent=2))

    except RuntimeError as exc:
        print(json.dumps({"error": str(exc)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
