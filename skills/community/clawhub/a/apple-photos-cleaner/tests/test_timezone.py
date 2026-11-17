#!/usr/bin/env python3
"""
Regression tests for local-time date math (ROADMAP T0.1).

Photos stores ZDATECREATED in UTC and the capture offset in
ZADDITIONALASSETATTRIBUTES.ZTIMEZONEOFFSET. Every hour/day/year bucket must use
the local wall-clock time the photo was taken at, not UTC.

The fixture assets are chosen so the old UTC-only math gives a different answer
for every assertion:

  CHICAGO - 2025-12-31 23:30 local, UTC-6  (UTC: 2026-01-01 05:30)
  TOKYO   - 2026-01-01 00:30 local, UTC+9  (UTC: 2025-12-31 15:30)
  NO_TZ   - NULL offset, UTC 2025-06-15 03:00 → 2025-06-14 23:00 in New York (EDT)
"""

import sqlite3
import time
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

from _common import (
    coredata_to_local,
    datetime_to_coredata,
    has_timezone_offset,
    local_datetime_sql,
    tz_offset_sql,
)

CHICAGO_OFFSET = -6 * 3600
TOKYO_OFFSET = 9 * 3600

CHICAGO_UTC = datetime(2026, 1, 1, 5, 30)
TOKYO_UTC = datetime(2025, 12, 31, 15, 30)
NO_TZ_UTC = datetime(2025, 6, 15, 3, 0)


@pytest.fixture
def new_york_tz(monkeypatch):
    """Pin the system zone so the NULL-offset fallback is deterministic."""
    monkeypatch.setenv("TZ", "America/New_York")
    time.tzset()
    yield
    monkeypatch.undo()
    time.tzset()


@pytest.fixture
def tz_db(new_york_tz):
    """full_db's schema with ZTIMEZONEOFFSET added and only the three fixture assets."""
    from test_new_scripts import create_full_test_db

    conn = create_full_test_db()
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE ZADDITIONALASSETATTRIBUTES ADD COLUMN ZTIMEZONEOFFSET INTEGER")
    cursor.execute("DELETE FROM ZASSET")
    cursor.execute("DELETE FROM ZADDITIONALASSETATTRIBUTES")
    for pk, name, utc, offset in [
        (1, "CHICAGO.heic", CHICAGO_UTC, CHICAGO_OFFSET),
        (2, "TOKYO.heic", TOKYO_UTC, TOKYO_OFFSET),
        (3, "NO_TZ.heic", NO_TZ_UTC, None),
    ]:
        cursor.execute(
            """
            INSERT INTO ZASSET (Z_PK, ZFILENAME, ZDATECREATED, ZWIDTH, ZHEIGHT, ZKIND, ZUUID)
            VALUES (?, ?, ?, 4032, 3024, 0, ?)
        """,
            (pk, name, datetime_to_coredata(utc), f"CCCCCCCC-0000-0000-0000-00000000000{pk}"),
        )
        cursor.execute(
            "INSERT INTO ZADDITIONALASSETATTRIBUTES (ZASSET, ZORIGINALFILESIZE, ZTIMEZONEOFFSET) VALUES (?, 1000, ?)",
            (pk, offset),
        )
    conn.commit()
    yield conn
    conn.close()


def run_with(module: str, conn: sqlite3.Connection, fn, **kwargs):
    with patch(f"{module}.PhotosDB") as mock_db:
        mock_db.return_value.__enter__ = MagicMock(return_value=conn)
        mock_db.return_value.__exit__ = MagicMock(return_value=False)
        return fn(db_path="test", **kwargs)


class TestHelpers:
    def test_offset_wins(self):
        assert coredata_to_local(datetime_to_coredata(CHICAGO_UTC), CHICAGO_OFFSET) == datetime(2025, 12, 31, 23, 30)
        assert coredata_to_local(datetime_to_coredata(TOKYO_UTC), TOKYO_OFFSET) == datetime(2026, 1, 1, 0, 30)

    def test_null_offset_uses_system_zone(self, new_york_tz):
        assert coredata_to_local(datetime_to_coredata(NO_TZ_UTC), None) == datetime(2025, 6, 14, 23, 0)

    def test_null_timestamp(self):
        assert coredata_to_local(None, 3600) is None

    def test_sql_matches_python(self, tz_db):
        cursor = tz_db.cursor()
        assert has_timezone_offset(cursor)
        cursor.execute(f"""
            SELECT a.ZDATECREATED, {tz_offset_sql(True)} AS tz_offset, {local_datetime_sql(True)} AS local_dt
            FROM ZASSET a LEFT JOIN ZADDITIONALASSETATTRIBUTES aa ON a.Z_PK = aa.ZASSET
        """)
        for row in cursor.fetchall():
            expected = coredata_to_local(row["ZDATECREATED"], row["tz_offset"])
            assert datetime.fromisoformat(row["local_dt"]) == expected

    def test_schema_without_column(self, basic_db, new_york_tz):
        cursor = basic_db.cursor()
        assert not has_timezone_offset(cursor)
        assert tz_offset_sql(False) == "NULL"
        cursor.execute(f"SELECT {local_datetime_sql(False)} AS d FROM ZASSET a WHERE a.Z_PK = 1")
        assert cursor.fetchone()["d"] is not None


class TestScripts:
    def test_library_analysis_years_and_range(self, tz_db):
        from library_analysis import analyze_library

        result = run_with("library_analysis", tz_db, analyze_library)
        assert result["by_year"] == {"2025": 2, "2026": 1}  # CHICAGO + NO_TZ | TOKYO
        assert result["summary"]["min_date"] == "2025-06-14T23:00:00"  # NO_TZ in New York, not UTC 03:00
        assert result["summary"]["max_date"] == "2026-01-01T00:30:00"  # TOKYO, not CHICAGO's UTC 05:30
        assert set(result["storage_by_year"]) == {"2025", "2026"}

    def test_photo_habits_hours(self, tz_db):
        from photo_habits import analyze_habits

        result = run_with("photo_habits", tz_db, analyze_habits)
        counts = {h["hour"]: h["count"] for h in result["by_hour"]}
        assert counts[23] == 2  # CHICAGO 23:30 + NO_TZ 23:00
        assert counts[0] == 1  # TOKYO 00:30
        assert sum(counts.values()) == 3

    def test_photo_habits_year_filter(self, tz_db):
        from photo_habits import analyze_habits

        result = run_with("photo_habits", tz_db, analyze_habits, year="2025")
        counts = {h["hour"]: h["count"] for h in result["by_hour"] if h["count"]}
        assert counts == {23: 2}  # CHICAGO + NO_TZ; UTC math would pick TOKYO 15:30 + NO_TZ 03:00

    def test_on_this_day_new_years_eve(self, tz_db):
        from on_this_day import on_this_day

        target = datetime.now().replace(year=datetime.now().year + 1, month=12, day=31)
        result = run_with("on_this_day", tz_db, on_this_day, target_date=target.date().isoformat())
        names = [p["filename"] for y in result["years"] for p in y["photos"]]
        assert names == ["CHICAGO.heic"]

    def test_on_this_day_null_offset_fallback(self, tz_db):
        from on_this_day import on_this_day

        result = run_with("on_this_day", tz_db, on_this_day, target_date="2030-06-14")
        names = [p["filename"] for y in result["years"] for p in y["photos"]]
        assert names == ["NO_TZ.heic"]

    def test_timeline_recap_local_day(self, tz_db):
        from timeline_recap import generate_timeline

        result = run_with("timeline_recap", tz_db, generate_timeline, start_date="2025-12-31", end_date="2025-12-31")
        assert result["summary"]["total_photos"] == 1
        [day] = result["timeline"]
        assert day["date"] == "2025-12-31"
        assert [e["time"] for e in day["events"]] == ["23:30"]  # CHICAGO, in local time

    def test_photo_habits_period_uses_local_extremes(self, tz_db):
        """UTC row order ends on CHICAGO (05:30 UTC Jan 1), but TOKYO is the latest local time."""
        from photo_habits import analyze_habits

        summary = run_with("photo_habits", tz_db, analyze_habits)["summary"]
        assert (summary["first_date"], summary["last_date"]) == ("2025-06-14T23:00:00", "2026-01-01T00:30:00")

    def test_timeline_recap_clusters_in_local_order(self, tz_db):
        """In UTC order TOKYO (local Jan 1 00:30) precedes CHICAGO (local Dec 31 23:30)."""
        from timeline_recap import generate_timeline

        result = run_with("timeline_recap", tz_db, generate_timeline, start_date="2025-12-31", end_date="2026-01-01")
        [day] = result["timeline"]
        [event] = day["events"]
        assert day["date"] == "2025-12-31"
        assert (event["time"], event["duration_minutes"]) == ("23:30", 60)

    def test_smart_export_end_date_inclusive_and_local(self, tz_db):
        from smart_export import generate_export_plan

        result = run_with("smart_export", tz_db, generate_export_plan, start_date="2025-12-31", end_date="2025-12-31")
        assert list(result["folders"]) == ["2025/12-December"]
        [item] = result["folders"]["2025/12-December"]["items"]
        assert (item["filename"], item["created"]) == ("CHICAGO.heic", "2025-12-31T23:30:00")

    def test_window_crosses_year(self, tz_db):
        """A ±1 day window around Jan 1 catches both New Year's photos."""
        from on_this_day import on_this_day

        target = (datetime.now() + timedelta(days=400)).replace(month=1, day=1)
        result = run_with("on_this_day", tz_db, on_this_day, target_date=target.date().isoformat(), window_days=1)
        names = sorted(p["filename"] for y in result["years"] for p in y["photos"])
        # TOKYO is local 2026-01-01 and excluded only if 2026 is the current year
        expected = ["CHICAGO.heic"] if datetime.now().year == 2026 else ["CHICAGO.heic", "TOKYO.heic"]
        assert names == expected


class TestDstBoundaries:
    """The NULL-offset fallback must apply the zone's rules at capture time, not today's offset.

    America/New_York, 2025: clocks jump 02:00 → 03:00 EDT on Mar 9 (07:00 UTC) and fall
    back 02:00 → 01:00 EST on Nov 2 (06:00 UTC).
    """

    CASES = (
        (datetime(2025, 3, 9, 6, 59), datetime(2025, 3, 9, 1, 59)),  # last minute of EST
        (datetime(2025, 3, 9, 7, 1), datetime(2025, 3, 9, 3, 1)),  # first minute of EDT; 02:xx never happens
        (datetime(2025, 11, 2, 5, 30), datetime(2025, 11, 2, 1, 30)),  # 01:30 EDT
        (datetime(2025, 11, 2, 6, 30), datetime(2025, 11, 2, 1, 30)),  # 01:30 again, now EST
    )

    @pytest.mark.parametrize(("utc", "local"), CASES)
    def test_python_fallback(self, new_york_tz, utc, local):
        assert coredata_to_local(datetime_to_coredata(utc), None) == local

    @pytest.mark.parametrize(("utc", "local"), CASES)
    def test_sql_fallback_matches(self, new_york_tz, utc, local):
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE ZASSET (ZDATECREATED REAL)")
        conn.execute("INSERT INTO ZASSET VALUES (?)", (datetime_to_coredata(utc),))
        (value,) = conn.execute(f"SELECT {local_datetime_sql(False)} FROM ZASSET a").fetchone()
        assert datetime.fromisoformat(value) == local

    @pytest.mark.parametrize(
        ("utc", "offset", "local"),
        [
            (datetime(2025, 7, 1, 16, 0), -4 * 3600, datetime(2025, 7, 1, 12, 0)),  # recorded EDT
            (datetime(2025, 1, 1, 17, 0), -5 * 3600, datetime(2025, 1, 1, 12, 0)),  # recorded EST
        ],
    )
    def test_recorded_offset_ignores_system_dst(self, new_york_tz, utc, offset, local):
        assert coredata_to_local(datetime_to_coredata(utc), offset) == local
