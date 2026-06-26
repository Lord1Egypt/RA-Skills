#!/usr/bin/env python3
# Author: SQ
"""
Initialize the Garmin SQLite database
与 garmin_db_reader.py 保持完全一致的 schema
与 sync_all.py INSERT 语句完全对齐
"""
import sqlite3, os
from pathlib import Path

DB_PATH = Path.home() / ".clawdbot" / "garmin" / "data.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS daily_metrics (
    date TEXT PRIMARY KEY,
    steps INTEGER,
    distance_km REAL,
    calories INTEGER,
    active_seconds INTEGER,
    floors INTEGER,
    resting_heart_rate INTEGER,
    min_heart_rate INTEGER,
    max_heart_rate INTEGER,
    body_battery_current INTEGER,
    body_battery_highest INTEGER,
    body_battery_lowest INTEGER,
    body_battery_charged INTEGER,
    body_battery_drained INTEGER,
    avg_stress INTEGER,
    max_stress INTEGER,
    hrv_value INTEGER,
    breathing_rate REAL,
    vo2_max REAL,
    fitness_age INTEGER,
    last_sync_time TEXT,
    moderate_intensity_minutes INTEGER,
    vigorous_intensity_minutes INTEGER,
    stress_average INTEGER,
    calories_active REAL,
    calories_bmr REAL,
    floors_descended REAL,
    intensity_minutes INTEGER
)""")

c.execute("""CREATE TABLE IF NOT EXISTS sleep_data (
    date TEXT PRIMARY KEY,
    total_sleep_hours REAL,
    deep_sleep_hours REAL,
    light_sleep_hours REAL,
    rem_sleep_hours REAL,
    awake_time_minutes INTEGER,
    sleep_score INTEGER,
    sleep_quality TEXT,
    avg_heart_rate INTEGER,
    avg_spo2 INTEGER,
    last_sync_time TEXT,
    duration_minutes INTEGER,
    nap_count INTEGER,
    nap_total_minutes INTEGER,
    nap_details TEXT,
    sleep_source TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS workouts (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    type TEXT,
    name TEXT,
    distance_km REAL,
    duration_seconds INTEGER,
    calories INTEGER,
    avg_heart_rate INTEGER,
    max_heart_rate INTEGER,
    last_sync_time TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS garmin_status (
    id INTEGER PRIMARY KEY,
    last_sync_time TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS sync_log (
    sync_time TEXT,
    source TEXT,
    records INTEGER,
    status TEXT
)""")

conn.commit()
conn.close()
print(f"✅ Database initialized at {DB_PATH}")
print("   Tables: daily_metrics, sleep_data, workouts, garmin_status")
