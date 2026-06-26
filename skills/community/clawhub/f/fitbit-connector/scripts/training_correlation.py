#!/usr/bin/env python3
"""Training ↔ health correlation (local-first, SQLite-based).

This module ingests structured calendar events (Google Calendar JSON export shape),
extracts training session metadata, and builds local join/correlation views against
`daily_health_summary` in `health_unified.sqlite3`.
"""

import argparse
import hashlib
import json
import re
import sqlite3
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


HEALTH_DB_PATH = Path(__file__).resolve().parent.parent / "assets" / "health_unified.sqlite3"
DEFAULT_CALENDAR_JSON = Path(__file__).resolve().parent.parent / "cache" / "calendar" / "training-calendar-full.json"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _print(payload: Dict[str, Any]) -> None:
    print(json.dumps(payload, separators=(",", ":"), ensure_ascii=False))


def _connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS training_sessions (
            session_id TEXT PRIMARY KEY,
            source_event_id TEXT,
            source_calendar TEXT,
            source_path TEXT,
            source_updated_at TEXT,
            session_date TEXT NOT NULL,
            start_at TEXT,
            end_at TEXT,
            title TEXT NOT NULL,
            description TEXT,
            training_block TEXT,
            exercise_tags_json TEXT,
            primary_lifts_json TEXT,
            set_count_est INTEGER,
            rep_count_est INTEGER,
            max_load_kg REAL,
            volume_load_est REAL,
            notes_hash TEXT,
            ingested_at TEXT NOT NULL
        )
        """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_training_sessions_date ON training_sessions(session_date)")

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS training_daily_summary (
            date TEXT PRIMARY KEY,
            sessions_count INTEGER NOT NULL,
            titles_json TEXT,
            exercise_tags_json TEXT,
            primary_lifts_json TEXT,
            set_count_est INTEGER,
            rep_count_est INTEGER,
            max_load_kg REAL,
            volume_load_est REAL,
            training_block TEXT,
            ingested_at TEXT NOT NULL
        )
        """
    )

    conn.execute(
        """
        CREATE VIEW IF NOT EXISTS v_health_daily_best AS
        WITH ranked AS (
          SELECT *,
                 CASE WHEN source='fitbit' THEN 2 WHEN source='apple_health' THEN 1 ELSE 0 END AS pri,
                 ROW_NUMBER() OVER (
                   PARTITION BY date
                   ORDER BY CASE WHEN source='fitbit' THEN 2 WHEN source='apple_health' THEN 1 ELSE 0 END DESC,
                            ingested_at DESC
                 ) AS rn
          FROM daily_health_summary
        )
        SELECT
          date,
          source,
          steps,
          active_zone_minutes,
          calories_out,
          resting_hr,
          hrv_rmssd,
          sleep_minutes,
          sleep_efficiency,
          sleep_score,
          data_quality,
          ingested_at
        FROM ranked
        WHERE rn = 1
        """
    )

    conn.execute(
        """
        CREATE VIEW IF NOT EXISTS v_health_daily_fitbit AS
        SELECT
          date,
          source,
          steps,
          active_zone_minutes,
          calories_out,
          resting_hr,
          hrv_rmssd,
          sleep_minutes,
          sleep_efficiency,
          sleep_score,
          data_quality,
          ingested_at
        FROM daily_health_summary
        WHERE source = 'fitbit'
        """
    )

    conn.execute(
        """
        CREATE VIEW IF NOT EXISTS v_health_daily_apple AS
        SELECT
          date,
          source,
          steps,
          active_zone_minutes,
          calories_out,
          resting_hr,
          hrv_rmssd,
          sleep_minutes,
          sleep_efficiency,
          sleep_score,
          data_quality,
          ingested_at
        FROM daily_health_summary
        WHERE source = 'apple_health'
        """
    )

    conn.execute(
        """
        CREATE VIEW IF NOT EXISTS v_training_health_daily AS
        SELECT
          h.date,
          h.source AS health_source,
          h.steps,
          h.active_zone_minutes,
          h.calories_out,
          h.resting_hr,
          h.hrv_rmssd,
          h.sleep_minutes,
          h.sleep_efficiency,
          h.sleep_score,
          h.data_quality,
          COALESCE(t.sessions_count, 0) AS training_sessions,
          t.titles_json AS training_titles_json,
          t.exercise_tags_json,
          t.primary_lifts_json,
          t.set_count_est,
          t.rep_count_est,
          t.max_load_kg,
          t.volume_load_est,
          t.training_block
        FROM v_health_daily_best h
        LEFT JOIN training_daily_summary t ON t.date = h.date
        """
    )

    conn.execute(
        """
        CREATE VIEW IF NOT EXISTS v_training_health_daily_fitbit AS
        SELECT
          h.date,
          h.source AS health_source,
          h.steps,
          h.active_zone_minutes,
          h.calories_out,
          h.resting_hr,
          h.hrv_rmssd,
          h.sleep_minutes,
          h.sleep_efficiency,
          h.sleep_score,
          h.data_quality,
          COALESCE(t.sessions_count, 0) AS training_sessions,
          t.titles_json AS training_titles_json,
          t.exercise_tags_json,
          t.primary_lifts_json,
          t.set_count_est,
          t.rep_count_est,
          t.max_load_kg,
          t.volume_load_est,
          t.training_block
        FROM v_health_daily_fitbit h
        LEFT JOIN training_daily_summary t ON t.date = h.date
        """
    )

    conn.execute(
        """
        CREATE VIEW IF NOT EXISTS v_training_health_daily_apple AS
        SELECT
          h.date,
          h.source AS health_source,
          h.steps,
          h.active_zone_minutes,
          h.calories_out,
          h.resting_hr,
          h.hrv_rmssd,
          h.sleep_minutes,
          h.sleep_efficiency,
          h.sleep_score,
          h.data_quality,
          COALESCE(t.sessions_count, 0) AS training_sessions,
          t.titles_json AS training_titles_json,
          t.exercise_tags_json,
          t.primary_lifts_json,
          t.set_count_est,
          t.rep_count_est,
          t.max_load_kg,
          t.volume_load_est,
          t.training_block
        FROM v_health_daily_apple h
        LEFT JOIN training_daily_summary t ON t.date = h.date
        """
    )

    conn.commit()
    return conn


TITLE_PREFIX_RE = re.compile(r"^\s*(training|workout\s*log)\s*[—-]\s*", re.IGNORECASE)
TOKEN_SPLIT_RE = re.compile(r"\s*\+\s*|\s*,\s*|\s*\/\s*|\s*\|\s*")
LOAD_RE = re.compile(r"(?P<kg>\d+(?:[\.,]\d+)?)\s*(?:kg)?\s*[x×]\s*(?P<reps>\d{1,2})\b", re.IGNORECASE)
SETS_RE = re.compile(r"(?P<sets>\d{1,2})\s*[x×]\s*(?P<reps>\d{1,2})\s*@\s*(?P<kg>\d+(?:[\.,]\d+)?)\s*(?:kg)?", re.IGNORECASE)
KG_SETS_REPS_RE = re.compile(r"(?P<kg>\d+(?:[\.,]\d+)?)\s*(?:kg)?\s*,?\s*(?P<sets>\d{1,2})\s*[x×]\s*(?P<reps>\d{1,2})\b", re.IGNORECASE)

EXERCISE_KEYWORDS = {
    "squat": [r"\bsquats?\b"],
    "bench": [r"\bbench(?:\s+press)?\b"],
    "press": [r"\bohp\b", r"\boverhead\s+press\b", r"\bstrict\s+press\b", r"\bmilitary\s+press\b", r"(^|\n|[:\-\s])press([^a-z]|$)"],
    "deadlift": [r"\bdeadlifts?\b", r"\bdl\b"],
    "row": [r"\brows?\b", r"\bcable[-\s]*rows?\b", r"\bbarbell\s+rows?\b"],
    "chin": [r"\bchins?\b", r"\bcable[-\s]*chins?\b", r"\bpull[-\s]*ups?\b", r"\bchin[-\s]*ups?\b"],
}

PRIMARY_LIFTS = {"squat", "bench", "press", "deadlift"}
KG_REP_LIST_RE = re.compile(r"(?P<kg>\d+(?:[\.,]\d+)?)\s*kg\b(?P<tail>.*?)(?=(?:\d+(?:[\.,]\d+)?\s*kg\b)|$)", re.IGNORECASE)


@dataclass
class ParsedSession:
    session_id: str
    source_event_id: str
    source_calendar: Optional[str]
    source_path: str
    source_updated_at: Optional[str]
    session_date: str
    start_at: Optional[str]
    end_at: Optional[str]
    title: str
    description: Optional[str]
    training_block: Optional[str]
    exercise_tags: List[str]
    primary_lifts: List[str]
    set_count_est: Optional[int]
    rep_count_est: Optional[int]
    max_load_kg: Optional[float]
    volume_load_est: Optional[float]
    notes_hash: str


def _normalize_kg(x: str) -> float:
    return float(x.replace(",", "."))


def _event_datetime_field(ev: Dict[str, Any], key: str) -> Tuple[Optional[str], Optional[str]]:
    obj = ev.get(key) or {}
    if not isinstance(obj, dict):
        return None, None
    dt = obj.get("dateTime")
    d = obj.get("date")
    return dt, d


def _extract_session_date(ev: Dict[str, Any]) -> Optional[str]:
    start_dt, start_d = _event_datetime_field(ev, "start")
    if start_dt and len(start_dt) >= 10:
        return start_dt[:10]
    if start_d:
        return start_d
    return None


def _clean_title(summary: str) -> str:
    return TITLE_PREFIX_RE.sub("", (summary or "").strip())


def _infer_training_block(summary: str) -> Optional[str]:
    s = summary.lower()
    if "stress" in s:
        return "stress"
    if "volume" in s:
        return "volume"
    if "intensity" in s:
        return "intensity"
    if "recovery" in s or "light" in s:
        return "recovery"
    return None


def _extract_exercise_tags(summary: str, description: str) -> List[str]:
    text = f"{summary}\n{description or ''}".lower()
    out: List[str] = []
    for tag, aliases in EXERCISE_KEYWORDS.items():
        if any(re.search(pattern, text, re.IGNORECASE | re.MULTILINE) for pattern in aliases):
            out.append(tag)
    if "press" in out:
        has_true_press = bool(
            re.search(r"\b(overhead|strict|military)\s+press\b|\bohp\b", text, re.IGNORECASE | re.MULTILINE)
            or re.search(r"(^|\n)\s*press\b|(?:\+|/|,)\s*press\b|\bpress\s*(?:\+|/|,|$)", text, re.IGNORECASE | re.MULTILINE)
        )
        if re.search(r"\bbench\s+press\b", text, re.IGNORECASE) and not has_true_press:
            out = [t for t in out if t != "press"]
    if out:
        return sorted(set(out))

    # fallback: split the title body and keep non-empty tokens
    body = _clean_title(summary)
    tokens = [t.strip() for t in TOKEN_SPLIT_RE.split(body) if t.strip()]
    normalized = []
    for t in tokens:
        tt = re.sub(r"\(.*?\)", "", t).strip().lower()
        if tt:
            normalized.append(tt)
    return sorted(set(normalized))[:12]


def _extract_load_features(summary: str, description: str) -> Tuple[Optional[int], Optional[int], Optional[float], Optional[float]]:
    desc = description or ''
    if 'LOG' in desc:
        desc = desc.split('LOG', 1)[1]
    text = f"{summary}\n{desc}"

    set_count = 0
    rep_count = 0
    max_kg: Optional[float] = None
    volume: float = 0.0

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        line_sets = 0
        line_reps = 0
        line_volume = 0.0
        line_max: Optional[float] = None

        matched_structured = False
        for regex in (SETS_RE, KG_SETS_REPS_RE):
            for m in regex.finditer(line):
                sets = int(m.group("sets"))
                reps = int(m.group("reps"))
                kg = _normalize_kg(m.group("kg"))
                if sets >= 1:
                    matched_structured = True
                    line_sets += sets
                    line_reps += sets * reps
                    line_volume += sets * kg * reps
                    line_max = kg if line_max is None else max(line_max, kg)

        for m in LOAD_RE.finditer(line):
            kg = _normalize_kg(m.group("kg"))
            reps = int(m.group("reps"))
            line_sets += 1
            line_reps += reps
            line_volume += kg * reps
            line_max = kg if line_max is None else max(line_max, kg)

        if line_sets:
            set_count += line_sets
            rep_count += line_reps
            volume += line_volume
            if line_max is not None:
                max_kg = line_max if max_kg is None else max(max_kg, line_max)
            continue

        for m in KG_REP_LIST_RE.finditer(line):
            kg = _normalize_kg(m.group("kg"))
            reps = [int(x) for x in re.findall(r"\b(\d{1,2})\b", m.group("tail"))]
            reps = [r for r in reps if 1 <= r <= 30]
            if not reps:
                continue
            line_sets += len(reps)
            line_reps += sum(reps)
            line_volume += kg * sum(reps)
            line_max = kg if line_max is None else max(line_max, kg)

        if line_sets:
            set_count += line_sets
            rep_count += line_reps
            volume += line_volume
            if line_max is not None:
                max_kg = line_max if max_kg is None else max(max_kg, line_max)

    if set_count == 0:
        return None, None, None, None

    return set_count, rep_count if rep_count > 0 else None, max_kg, volume if volume > 0 else None


def _iter_events(payload: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    if isinstance(payload.get("events"), list):
        for ev in payload["events"]:
            if isinstance(ev, dict):
                yield ev
        return
    if isinstance(payload.get("items"), list):
        for ev in payload["items"]:
            if isinstance(ev, dict):
                yield ev
        return
    if isinstance(payload, list):
        for ev in payload:
            if isinstance(ev, dict):
                yield ev


def _is_training_event(summary: str, description: str, title_prefixes: Sequence[str]) -> bool:
    s = (summary or "").strip().lower()
    d = (description or "").lower()

    if any(s.startswith(p.lower()) for p in title_prefixes):
        return True
    if s.startswith("workout log"):
        return True

    # fallback keyword gate
    keywords = ["squat", "bench", "deadlift", "press", "chins", "row"]
    return any(k in s for k in keywords) and ("training" in s or "workout" in s or any(k in d for k in keywords))


def _canonical_session_id(source_calendar: Optional[str], event_id: str, session_date: str, title: str) -> str:
    if event_id:
        raw = f"{source_calendar or ''}|{event_id}".encode("utf-8", "ignore")
    else:
        raw = f"{source_calendar or ''}|{session_date}|{title}".encode("utf-8", "ignore")
    return hashlib.sha1(raw).hexdigest()


def reset_training_tables(conn: sqlite3.Connection, start: Optional[str] = None, end: Optional[str] = None) -> Dict[str, Any]:
    where = []
    params: List[Any] = []
    if start:
        where.append("session_date >= ?")
        params.append(start)
    if end:
        where.append("session_date <= ?")
        params.append(end)
    where_sql = f"WHERE {' AND '.join(where)}" if where else ""

    conn.execute(f"DELETE FROM training_sessions {where_sql}", params)
    if where:
        conn.execute("DELETE FROM training_daily_summary WHERE date BETWEEN COALESCE(?, date) AND COALESCE(?, date)", (start, end))
    else:
        conn.execute("DELETE FROM training_daily_summary")
    conn.commit()
    return {"ok": True, "operation": "reset-training", "start": start, "end": end}


def import_calendar_events(
    conn: sqlite3.Connection,
    json_path: Path,
    title_prefixes: Sequence[str],
    calendar_filter: Optional[str],
    start: Optional[str],
    end: Optional[str],
) -> Dict[str, Any]:
    payload = json.loads(json_path.read_text())

    if start:
        d_start = date.fromisoformat(start)
    else:
        d_start = None
    if end:
        d_end = date.fromisoformat(end)
    else:
        d_end = None

    scanned = 0
    selected = 0
    upserts = 0

    for ev in _iter_events(payload):
        scanned += 1
        summary = (ev.get("summary") or "").strip()
        description = (ev.get("description") or "").strip()
        if not summary:
            continue

        if not _is_training_event(summary, description, title_prefixes):
            continue

        session_date = _extract_session_date(ev)
        if not session_date:
            continue

        d = date.fromisoformat(session_date)
        if d_start and d < d_start:
            continue
        if d_end and d > d_end:
            continue

        source_calendar = ((ev.get("organizer") or {}).get("displayName") if isinstance(ev.get("organizer"), dict) else None)
        if calendar_filter and source_calendar and calendar_filter.lower() not in source_calendar.lower():
            continue

        start_dt, start_d = _event_datetime_field(ev, "start")
        end_dt, _ = _event_datetime_field(ev, "end")
        start_at = start_dt or start_d

        tags = _extract_exercise_tags(summary, description)
        primary_lifts = sorted([t for t in tags if t in PRIMARY_LIFTS])
        set_count, rep_count, max_kg, volume = _extract_load_features(summary, description)
        training_block = _infer_training_block(summary)
        source_event_id = str(ev.get("id") or ev.get("iCalUID") or "")
        session_id = _canonical_session_id(source_calendar, source_event_id, session_date, summary)
        notes_hash = hashlib.sha1((description or "").encode("utf-8", "ignore")).hexdigest()

        selected += 1
        conn.execute(
            """
            INSERT INTO training_sessions(
                session_id, source_event_id, source_calendar, source_path, source_updated_at,
                session_date, start_at, end_at, title, description, training_block,
                exercise_tags_json, primary_lifts_json,
                set_count_est, rep_count_est, max_load_kg, volume_load_est,
                notes_hash, ingested_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(session_id) DO UPDATE SET
                source_updated_at=excluded.source_updated_at,
                source_calendar=excluded.source_calendar,
                session_date=excluded.session_date,
                start_at=excluded.start_at,
                end_at=excluded.end_at,
                title=excluded.title,
                description=excluded.description,
                training_block=excluded.training_block,
                exercise_tags_json=excluded.exercise_tags_json,
                primary_lifts_json=excluded.primary_lifts_json,
                set_count_est=excluded.set_count_est,
                rep_count_est=excluded.rep_count_est,
                max_load_kg=excluded.max_load_kg,
                volume_load_est=excluded.volume_load_est,
                notes_hash=excluded.notes_hash,
                ingested_at=excluded.ingested_at
            """,
            (
                session_id,
                source_event_id,
                source_calendar,
                str(json_path),
                ev.get("updated"),
                session_date,
                start_at,
                end_dt,
                summary,
                description or None,
                training_block,
                json.dumps(tags, ensure_ascii=False),
                json.dumps(primary_lifts, ensure_ascii=False),
                set_count,
                rep_count,
                max_kg,
                volume,
                notes_hash,
                utc_now_iso(),
            ),
        )
        upserts += 1

    conn.commit()
    return {
        "ok": True,
        "operation": "import-calendar-events",
        "json_path": str(json_path),
        "scanned": scanned,
        "selected_training": selected,
        "upserts": upserts,
        "start": start,
        "end": end,
    }


def rebuild_training_daily_summary(conn: sqlite3.Connection, start: Optional[str], end: Optional[str]) -> Dict[str, Any]:
    where = []
    params: List[Any] = []
    if start:
        where.append("session_date >= ?")
        params.append(start)
    if end:
        where.append("session_date <= ?")
        params.append(end)
    where_sql = f"WHERE {' AND '.join(where)}" if where else ""

    if where:
        conn.execute(f"DELETE FROM training_daily_summary WHERE date IN (SELECT DISTINCT session_date FROM training_sessions {where_sql})", params)
    else:
        conn.execute("DELETE FROM training_daily_summary")

    rows = conn.execute(
        f"""
        SELECT
          session_date,
          COUNT(*) AS sessions_count,
          GROUP_CONCAT(title, ' || ') AS titles_concat,
          SUM(COALESCE(set_count_est,0)) AS set_count_est,
          SUM(COALESCE(rep_count_est,0)) AS rep_count_est,
          MAX(max_load_kg) AS max_load_kg,
          SUM(COALESCE(volume_load_est,0)) AS volume_load_est,
          GROUP_CONCAT(COALESCE(training_block,''), ',') AS blocks_concat
        FROM training_sessions
        {where_sql}
        GROUP BY session_date
        ORDER BY session_date
        """,
        params,
    ).fetchall()

    upserts = 0
    for r in rows:
        d = r[0]
        titles = [t.strip() for t in (r[2] or "").split("||") if t.strip()]
        sess_rows = conn.execute(
            "SELECT exercise_tags_json, primary_lifts_json FROM training_sessions WHERE session_date=? ORDER BY start_at",
            (d,),
        ).fetchall()
        tags = set()
        lifts = set()
        for tr in sess_rows:
            try:
                tags.update(json.loads(tr[0] or "[]"))
            except Exception:
                pass
            try:
                lifts.update(json.loads(tr[1] or "[]"))
            except Exception:
                pass

        block_candidates = [b.strip() for b in (r[7] or "").split(",") if b.strip()]
        training_block = block_candidates[0] if block_candidates else None

        conn.execute(
            """
            INSERT INTO training_daily_summary(
                date, sessions_count, titles_json, exercise_tags_json, primary_lifts_json,
                set_count_est, rep_count_est, max_load_kg, volume_load_est, training_block, ingested_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(date) DO UPDATE SET
                sessions_count=excluded.sessions_count,
                titles_json=excluded.titles_json,
                exercise_tags_json=excluded.exercise_tags_json,
                primary_lifts_json=excluded.primary_lifts_json,
                set_count_est=excluded.set_count_est,
                rep_count_est=excluded.rep_count_est,
                max_load_kg=excluded.max_load_kg,
                volume_load_est=excluded.volume_load_est,
                training_block=excluded.training_block,
                ingested_at=excluded.ingested_at
            """,
            (
                d,
                int(r[1] or 0),
                json.dumps(titles[:8], ensure_ascii=False),
                json.dumps(sorted(tags), ensure_ascii=False),
                json.dumps(sorted(lifts), ensure_ascii=False),
                int(r[3] or 0),
                int(r[4] or 0),
                r[5],
                float(r[6] or 0) if r[6] is not None else None,
                training_block,
                utc_now_iso(),
            ),
        )
        upserts += 1

    conn.commit()
    return {
        "ok": True,
        "operation": "rebuild-training-daily-summary",
        "rows": upserts,
        "start": start,
        "end": end,
    }


def _training_health_view(source: str) -> str:
    mapping = {
        "best": "v_training_health_daily",
        "fitbit": "v_training_health_daily_fitbit",
        "apple_health": "v_training_health_daily_apple",
    }
    if source not in mapping:
        raise ValueError(f"unsupported health source: {source}")
    return mapping[source]


def status(conn: sqlite3.Connection, source: str = "fitbit") -> Dict[str, Any]:
    view = _training_health_view(source)
    sessions = conn.execute("SELECT COUNT(*) FROM training_sessions").fetchone()[0]
    days = conn.execute("SELECT COUNT(*) FROM training_daily_summary").fetchone()[0]
    rng = conn.execute("SELECT MIN(session_date), MAX(session_date) FROM training_sessions").fetchone()
    cov = conn.execute(
        f"""
        SELECT COUNT(*)
        FROM {view}
        WHERE training_sessions > 0
          AND (sleep_minutes IS NOT NULL OR hrv_rmssd IS NOT NULL OR resting_hr IS NOT NULL)
        """
    ).fetchone()[0]
    return {
        "ok": True,
        "operation": "status",
        "db": str(HEALTH_DB_PATH),
        "health_source": source,
        "training_sessions": sessions,
        "training_days": days,
        "training_range": {"start": rng[0], "end": rng[1]},
        "days_with_training_and_health": cov,
    }


def _window_dates(days: int) -> Tuple[str, str]:
    d1 = date.today()
    d0 = d1 - timedelta(days=max(days - 1, 0))
    return d0.isoformat(), d1.isoformat()


def health_window(conn: sqlite3.Connection, days: int, source: str = "fitbit") -> Dict[str, Any]:
    view = _training_health_view(source)
    start, end = _window_dates(days)
    rows = conn.execute(
        f"""
        SELECT
          date, health_source, sleep_minutes, hrv_rmssd, resting_hr,
          steps, calories_out, active_zone_minutes,
          training_sessions, training_titles_json, exercise_tags_json, primary_lifts_json,
          set_count_est, rep_count_est, max_load_kg, volume_load_est, training_block,
          data_quality
        FROM {view}
        WHERE date BETWEEN ? AND ?
        ORDER BY date DESC
        """,
        (start, end),
    ).fetchall()

    out_rows = []
    for r in rows:
        out_rows.append(
            {
                "date": r[0],
                "health_source": r[1],
                "sleep_minutes": r[2],
                "hrv_rmssd": r[3],
                "resting_hr": r[4],
                "steps": r[5],
                "calories_out": r[6],
                "active_zone_minutes": r[7],
                "training_sessions": r[8],
                "training_titles": json.loads(r[9]) if r[9] else [],
                "exercise_tags": json.loads(r[10]) if r[10] else [],
                "primary_lifts": json.loads(r[11]) if r[11] else [],
                "set_count_est": r[12],
                "rep_count_est": r[13],
                "max_load_kg": r[14],
                "volume_load_est": r[15],
                "training_block": r[16],
                "data_quality": r[17],
            }
        )

    return {
        "ok": True,
        "operation": "health-window",
        "health_source": source,
        "days": days,
        "start": start,
        "end": end,
        "rows": out_rows,
    }


def correlation_summary(conn: sqlite3.Connection, days: int, source: str = "fitbit") -> Dict[str, Any]:
    view = _training_health_view(source)
    start, end = _window_dates(days)

    rows = conn.execute(
        f"""
        WITH base AS (
          SELECT date, training_sessions, hrv_rmssd, resting_hr, sleep_minutes
          FROM {view}
          WHERE date BETWEEN ? AND ?
        ),
        next_day AS (
          SELECT
            b.date AS train_date,
            CASE WHEN b.training_sessions > 0 THEN 1 ELSE 0 END AS trained,
            n.hrv_rmssd AS next_hrv,
            n.resting_hr AS next_rhr,
            n.sleep_minutes AS next_sleep
          FROM base b
          LEFT JOIN {view} n
            ON n.date = date(b.date, '+1 day')
        )
        SELECT
          trained,
          COUNT(*) AS n_days,
          AVG(next_hrv) AS avg_next_hrv,
          AVG(next_rhr) AS avg_next_resting_hr,
          AVG(next_sleep) AS avg_next_sleep_minutes
        FROM next_day
        GROUP BY trained
        ORDER BY trained DESC
        """,
        (start, end),
    ).fetchall()

    by_group = {
        "trained_days": None,
        "non_trained_days": None,
    }
    for trained, n_days, avg_hrv, avg_rhr, avg_sleep in rows:
        key = "trained_days" if trained == 1 else "non_trained_days"
        by_group[key] = {
            "n_days": int(n_days or 0),
            "avg_next_day_hrv_rmssd": round(avg_hrv, 2) if avg_hrv is not None else None,
            "avg_next_day_resting_hr": round(avg_rhr, 2) if avg_rhr is not None else None,
            "avg_next_day_sleep_minutes": round(avg_sleep, 2) if avg_sleep is not None else None,
        }

    return {
        "ok": True,
        "operation": "correlation-summary",
        "health_source": source,
        "days": days,
        "start": start,
        "end": end,
        "next_day_metrics_by_training": by_group,
        "note": "Context signal only; not autoprescription logic.",
    }


def sync_calendar(
    conn: sqlite3.Connection,
    json_path: Path,
    title_prefixes: Sequence[str],
    calendar_filter: Optional[str],
    start: Optional[str],
    end: Optional[str],
    reset: bool = False,
) -> Dict[str, Any]:
    reset_result = None
    if reset:
        reset_result = reset_training_tables(conn, start, end)
    import_result = import_calendar_events(conn, json_path, title_prefixes, calendar_filter, start, end)
    rebuild_result = rebuild_training_daily_summary(conn, start, end)
    return {
        "ok": True,
        "operation": "sync-calendar",
        "reset": reset_result,
        "import": import_result,
        "daily_summary": rebuild_result,
        "status": status(conn),
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--db", default=str(HEALTH_DB_PATH))
    sub = p.add_subparsers(dest="cmd", required=True)

    st = sub.add_parser("status")
    st.add_argument("--source", choices=["fitbit", "apple_health", "best"], default="fitbit")

    sc = sub.add_parser("sync-calendar")
    sc.add_argument("--json", default=str(DEFAULT_CALENDAR_JSON))
    sc.add_argument("--title-prefix", action="append", default=["Training —", "Training -", "Workout Log —"])  # repeatable
    sc.add_argument("--calendar-filter")
    sc.add_argument("--start")
    sc.add_argument("--end")
    sc.add_argument("--reset", action="store_true", help="Delete existing training-layer rows before import")

    sub.add_parser("reset-training")

    rds = sub.add_parser("rebuild-daily")
    rds.add_argument("--start")
    rds.add_argument("--end")

    hw = sub.add_parser("health-window")
    hw.add_argument("--days", type=int, default=28)
    hw.add_argument("--source", choices=["fitbit", "apple_health", "best"], default="fitbit")

    cs = sub.add_parser("correlation-summary")
    cs.add_argument("--days", type=int, default=90)
    cs.add_argument("--source", choices=["fitbit", "apple_health", "best"], default="fitbit")

    args = p.parse_args()
    conn = _connect(Path(args.db))

    if args.cmd == "status":
        result = status(conn, args.source)
    elif args.cmd == "sync-calendar":
        result = sync_calendar(
            conn,
            Path(args.json),
            args.title_prefix,
            args.calendar_filter,
            args.start,
            args.end,
            args.reset,
        )
    elif args.cmd == "reset-training":
        result = reset_training_tables(conn)
    elif args.cmd == "rebuild-daily":
        result = rebuild_training_daily_summary(conn, args.start, args.end)
    elif args.cmd == "health-window":
        result = health_window(conn, args.days, args.source)
    elif args.cmd == "correlation-summary":
        result = correlation_summary(conn, args.days, args.source)
    else:
        result = {"ok": False, "error": "unknown command"}

    _print(result)


if __name__ == "__main__":
    main()
