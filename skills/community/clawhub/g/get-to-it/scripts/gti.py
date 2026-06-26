#!/usr/bin/env python3
"""
Get To It (GTI) — Core CLI & Database Module
A dynamic task management system with motivation-aware prioritization.

Usage:
    python gti.py <command> [args...]

Commands:
    init                          Initialize or migrate the database
    morning [--hours N]           Generate morning brief (Top 3)
    capture "text"                Quick capture an idea or task
    add-goal "title" [options]    Add a new goal
    add-project GOAL_ID "title"   Add a project under a goal
    add-task PROJECT_ID "title"   Add a task under a project
    start TASK_ID                 Start working on a task (records started_at)
    complete TASK_ID              Mark task as completed (auto-calculates time)
    complete TASK_ID --minutes N  Mark completed with manual time override
    skip TASK_ID [--reason "..."] Skip a task (tracks skip count)
    pause TASK_ID                 Pause a task
    resume TASK_ID                Resume a paused task
    review [--project ID]         Review progress & momentum
    mood EMOJI                    Record daily mood (fire/neutral/tired)
    status                        Overall system status (JSON)
    ideas [--all]                 List idea bank
    promote-idea IDEA_ID PRJ_ID   Promote idea to task
    memory                        List active short-term memories
    remember "content" [--type T] Store a short-term memory
    log [--days N]                Show action log (default 7 days)
    today-hours [N]               Get or set today's available hours
    time-stats [--category CAT]   Show time prediction accuracy stats
    smart-estimate CAT MINUTES    Get calibrated time estimate
    connect-calendar NAME URL     Register an ical calendar source
    sync-calendar [--id N]        Sync calendar events for today
    list-calendars                List registered calendar sources
    disconnect-calendar ID        Remove a calendar source
    free-time [--start HH:MM]     Calculate free time from calendar
    store-ltm "text" [--type T]   Store important statement in long-term memory
    recall-ltm "query" [--n N]    Semantic search in long-term memory
    list-ltm [--type T]           List all long-term memories
    clear-ltm ID                  Delete a long-term memory by ID
    agent-status                  Show all agent tasks and their state
    agent-retry TASK_ID           Retry a failed agent task
    agent-handoff TASK_ID         Hand off agent task to human
    weight-stats                  Show current scoring weights and ML training status
    learn-weights                 Train scoring weights from recommendation history (>=10 samples)
    morning --format telegram     Output morning brief as Telegram Markdown text
"""

import sqlite3
import json
import sys
import os
import argparse
from datetime import datetime, timedelta, date, time as dtime
from pathlib import Path

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    from icalendar import Calendar as iCalendar
    HAS_ICAL = True
except ImportError:
    HAS_ICAL = False

try:
    from urllib.request import urlopen, Request
    from urllib.error import URLError
    HAS_URLLIB = True
except ImportError:
    HAS_URLLIB = False

# Database lives in the user's workspace folder so it persists
DB_DIR = os.environ.get("GTI_DB_DIR", os.path.expanduser("~"))
DB_PATH = os.path.join(DB_DIR, ".get-to-it.db")

# ─────────────────────────────────────────────
# Database Setup
# ─────────────────────────────────────────────

SCHEMA = """
CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    vision TEXT,
    priority INTEGER DEFAULT 5,
    status TEXT DEFAULT 'active',
    deadline TEXT,
    created_at TEXT DEFAULT (datetime('now','localtime')),
    updated_at TEXT DEFAULT (datetime('now','localtime'))
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_id INTEGER REFERENCES goals(id),
    title TEXT NOT NULL,
    milestones TEXT DEFAULT '[]',
    progress_pct REAL DEFAULT 0,
    momentum_score REAL DEFAULT 0,
    status TEXT DEFAULT 'active',
    created_at TEXT DEFAULT (datetime('now','localtime')),
    updated_at TEXT DEFAULT (datetime('now','localtime'))
);

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER REFERENCES projects(id),
    title TEXT NOT NULL,
    description TEXT,
    assignee TEXT DEFAULT 'human',
    status TEXT DEFAULT 'pending',
    estimated_minutes INTEGER,
    skip_count INTEGER DEFAULT 0,
    skip_reasons TEXT DEFAULT '[]',
    deadline TEXT,
    completed_at TEXT,
    created_at TEXT DEFAULT (datetime('now','localtime')),
    updated_at TEXT DEFAULT (datetime('now','localtime'))
);

CREATE TABLE IF NOT EXISTS ideas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    raw_input TEXT NOT NULL,
    relevance_score REAL,
    related_goal_id INTEGER REFERENCES goals(id),
    motivation_at_capture TEXT DEFAULT 'medium',
    suggested_action TEXT DEFAULT 'idea_bank',
    status TEXT DEFAULT 'captured',
    created_at TEXT DEFAULT (datetime('now','localtime'))
);

CREATE TABLE IF NOT EXISTS daily_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT UNIQUE NOT NULL,
    available_hours REAL,
    emoji_mood TEXT,
    tasks_completed INTEGER DEFAULT 0,
    momentum_score REAL,
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now','localtime'))
);

CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    content TEXT NOT NULL,
    related_task_id INTEGER,
    created_at TEXT DEFAULT (datetime('now','localtime')),
    expires_at TEXT
);

CREATE TABLE IF NOT EXISTS action_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action_type TEXT NOT NULL,
    entity_type TEXT,
    entity_id INTEGER,
    details TEXT,
    created_at TEXT DEFAULT (datetime('now','localtime'))
);
"""


def get_db():
    """Get database connection with WAL mode for concurrency safety."""
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA foreign_keys=ON")
    return db


def migrate_db(db):
    """Run idempotent migrations for V2 schema changes."""
    alter_migrations = [
        "ALTER TABLE tasks ADD COLUMN actual_minutes INTEGER",
        "ALTER TABLE tasks ADD COLUMN started_at TEXT",
        "ALTER TABLE tasks ADD COLUMN category TEXT",
    ]
    for sql in alter_migrations:
        try:
            db.execute(sql)
        except sqlite3.OperationalError:
            pass  # Column already exists

    # V2: Time estimates learning table
    db.execute("""
        CREATE TABLE IF NOT EXISTS time_estimates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_category TEXT,
            goal_id INTEGER,
            estimated_minutes_median REAL,
            sample_count INTEGER DEFAULT 0,
            accuracy_ratio REAL DEFAULT 1.0,
            updated_at TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    # V2: Calendar config & cached events
    db.execute("""
        CREATE TABLE IF NOT EXISTS calendar_config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            source_type TEXT NOT NULL DEFAULT 'ical_url',
            source_path TEXT NOT NULL,
            enabled INTEGER DEFAULT 1,
            last_synced_at TEXT,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS calendar_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            calendar_id INTEGER REFERENCES calendar_config(id),
            summary TEXT,
            dtstart TEXT NOT NULL,
            dtend TEXT NOT NULL,
            all_day INTEGER DEFAULT 0,
            location TEXT,
            event_date TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    # V2: Long-term memory with TF-IDF vectors
    db.execute("""
        CREATE TABLE IF NOT EXISTS long_term_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            content_type TEXT DEFAULT 'context',
            vector TEXT,
            metadata TEXT,
            last_accessed TEXT,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    # V2: Agent task tracking improvements
    db.execute("""
        CREATE TABLE IF NOT EXISTS agent_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER REFERENCES tasks(id),
            event_type TEXT NOT NULL,
            details TEXT,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    # V2 P3: ML weight learning
    # Tracks what was recommended each morning and whether it was completed
    db.execute("""
        CREATE TABLE IF NOT EXISTS recommendation_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER REFERENCES tasks(id),
            brief_date TEXT NOT NULL,
            position INTEGER NOT NULL,
            priority_score REAL,
            factors TEXT,
            was_completed INTEGER DEFAULT 0,
            completed_at TEXT,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        )
    """)
    # Stores learned or manually configured scoring weights
    db.execute("""
        CREATE TABLE IF NOT EXISTS scoring_weights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            factor TEXT NOT NULL UNIQUE,
            weight REAL NOT NULL,
            sample_count INTEGER DEFAULT 0,
            last_trained TEXT,
            updated_at TEXT DEFAULT (datetime('now','localtime'))
        )
    """)
    # Seed default weights if not present
    default_weights = [
        ("deadline",   30.0),
        ("goal_priority", 20.0),
        ("momentum",   15.0),
        ("skip_penalty", 10.0),
        ("time_fit",   15.0),
        ("proximity",  10.0),
    ]
    for factor, weight in default_weights:
        db.execute(
            "INSERT OR IGNORE INTO scoring_weights (factor, weight) VALUES (?,?)",
            (factor, weight)
        )

    db.commit()


def init_db():
    """Initialize database schema + run V2 migrations."""
    db = get_db()
    db.executescript(SCHEMA)
    migrate_db(db)
    db.commit()
    db.close()
    return {"status": "ok", "db_path": DB_PATH, "message": "Database initialized (V2)"}


def log_action(db, action_type, entity_type=None, entity_id=None, details=None):
    """Record an action in the action log."""
    db.execute(
        "INSERT INTO action_log (action_type, entity_type, entity_id, details) VALUES (?,?,?,?)",
        (action_type, entity_type, entity_id, json.dumps(details) if details else None)
    )


# ─────────────────────────────────────────────
# Goals
# ─────────────────────────────────────────────

def add_goal(title, vision=None, priority=5, deadline=None):
    db = get_db()
    cur = db.execute(
        "INSERT INTO goals (title, vision, priority, deadline) VALUES (?,?,?,?)",
        (title, vision, priority, deadline)
    )
    goal_id = cur.lastrowid
    log_action(db, "goal_created", "goal", goal_id, {"title": title})
    db.commit()
    db.close()
    return {"status": "ok", "goal_id": goal_id, "title": title}


def list_goals(status="active"):
    db = get_db()
    rows = db.execute(
        "SELECT * FROM goals WHERE status=? ORDER BY priority DESC, created_at",
        (status,)
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────────
# Projects
# ─────────────────────────────────────────────

def add_project(goal_id, title, milestones=None):
    db = get_db()
    ms = json.dumps(milestones or [])
    cur = db.execute(
        "INSERT INTO projects (goal_id, title, milestones) VALUES (?,?,?)",
        (goal_id, title, ms)
    )
    pid = cur.lastrowid
    log_action(db, "project_created", "project", pid, {"title": title, "goal_id": goal_id})
    db.commit()
    db.close()
    return {"status": "ok", "project_id": pid, "title": title}


def list_projects(goal_id=None, status="active"):
    db = get_db()
    if goal_id:
        rows = db.execute(
            "SELECT p.*, g.title as goal_title FROM projects p JOIN goals g ON p.goal_id=g.id WHERE p.status=? AND p.goal_id=? ORDER BY p.created_at",
            (status, goal_id)
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT p.*, g.title as goal_title FROM projects p JOIN goals g ON p.goal_id=g.id WHERE p.status=? ORDER BY p.created_at",
            (status,)
        ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def update_project_progress(project_id):
    """Recalculate project progress based on task completion."""
    db = get_db()
    total = db.execute("SELECT COUNT(*) FROM tasks WHERE project_id=?", (project_id,)).fetchone()[0]
    done = db.execute("SELECT COUNT(*) FROM tasks WHERE project_id=? AND status='completed'", (project_id,)).fetchone()[0]
    pct = (done / total * 100) if total > 0 else 0
    db.execute("UPDATE projects SET progress_pct=?, updated_at=datetime('now','localtime') WHERE id=?", (pct, project_id))
    db.commit()
    db.close()
    return pct


# ─────────────────────────────────────────────
# Tasks
# ─────────────────────────────────────────────

def add_task(project_id, title, description=None, assignee="human", estimated_minutes=None, deadline=None):
    db = get_db()
    cur = db.execute(
        "INSERT INTO tasks (project_id, title, description, assignee, estimated_minutes, deadline) VALUES (?,?,?,?,?,?)",
        (project_id, title, description, assignee, estimated_minutes, deadline)
    )
    tid = cur.lastrowid
    log_action(db, "task_created", "task", tid, {"title": title, "project_id": project_id, "assignee": assignee})
    db.commit()
    db.close()
    return {"status": "ok", "task_id": tid, "title": title}


def complete_task(task_id, manual_minutes=None):
    db = get_db()
    task = db.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    if not task:
        db.close()
        return {"status": "error", "message": f"Task {task_id} not found"}

    now = datetime.now()
    actual = None
    time_source = None

    if manual_minutes is not None:
        # User manually specified actual time
        actual = manual_minutes
        time_source = "manual"
    elif task["started_at"]:
        # Auto-calculate from started_at
        try:
            started = datetime.fromisoformat(task["started_at"])
            actual = round((now - started).total_seconds() / 60)
            time_source = "auto"
        except (ValueError, TypeError):
            pass

    db.execute(
        "UPDATE tasks SET status='completed', completed_at=datetime('now','localtime'), actual_minutes=?, updated_at=datetime('now','localtime') WHERE id=?",
        (actual, task_id)
    )
    # Update daily task count
    today = now.strftime("%Y-%m-%d")
    db.execute(
        "INSERT INTO daily_logs (date, tasks_completed) VALUES (?, 1) ON CONFLICT(date) DO UPDATE SET tasks_completed=tasks_completed+1",
        (today,)
    )
    log_action(db, "task_completed", "task", task_id, {
        "title": task["title"],
        "actual_minutes": actual,
        "estimated_minutes": task["estimated_minutes"],
        "time_source": time_source,
    })
    db.commit()

    # Update time prediction model if we have both estimated and actual
    time_feedback = None
    if actual and task["estimated_minutes"]:
        task_category = None
        task_goal_id = None
        try:
            task_category = task["category"]
        except (IndexError, KeyError):
            pass
        try:
            task_goal_id = task["goal_id"]
        except (IndexError, KeyError):
            pass
        time_feedback = update_time_model(
            db, task_category, task["estimated_minutes"], actual,
            goal_id=task_goal_id
        )
        db.commit()

    # V2 P3: Mark this task as completed in recommendation_log (for ML training)
    now_str = now.isoformat()
    db.execute(
        """UPDATE recommendation_log
           SET was_completed=1, completed_at=?
           WHERE task_id=? AND was_completed=0""",
        (now_str, task_id)
    )
    db.commit()

    # Recalculate project progress
    pct = update_project_progress(task["project_id"])
    db.close()

    result = {"status": "ok", "task_id": task_id, "title": task["title"], "project_progress": pct}
    if actual is not None:
        result["actual_minutes"] = actual
        result["estimated_minutes"] = task["estimated_minutes"]
        result["time_source"] = time_source
    if time_feedback:
        result["time_feedback"] = time_feedback
    return result


def skip_task(task_id, reason=None):
    db = get_db()
    task = db.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    if not task:
        db.close()
        return {"status": "error", "message": f"Task {task_id} not found"}
    reasons = json.loads(task["skip_reasons"])
    if reason:
        reasons.append({"reason": reason, "at": datetime.now().isoformat()})
    new_count = task["skip_count"] + 1
    db.execute(
        "UPDATE tasks SET skip_count=?, skip_reasons=?, updated_at=datetime('now','localtime') WHERE id=?",
        (new_count, json.dumps(reasons), task_id)
    )
    # Store skip reason in memory
    if reason:
        expires = (datetime.now() + timedelta(days=14)).isoformat()
        db.execute(
            "INSERT INTO memory (type, content, related_task_id, expires_at) VALUES (?,?,?,?)",
            ("skip_reason", reason, task_id, expires)
        )
    log_action(db, "task_skipped", "task", task_id, {"title": task["title"], "reason": reason, "skip_count": new_count})
    db.commit()
    db.close()
    trigger_check = new_count >= 3
    return {"status": "ok", "task_id": task_id, "skip_count": new_count, "trigger_checkin": trigger_check}


def pause_task(task_id):
    db = get_db()
    db.execute("UPDATE tasks SET status='paused', updated_at=datetime('now','localtime') WHERE id=?", (task_id,))
    log_action(db, "task_paused", "task", task_id)
    db.commit()
    db.close()
    return {"status": "ok", "task_id": task_id, "new_status": "paused"}


def resume_task(task_id):
    db = get_db()
    db.execute("UPDATE tasks SET status='pending', updated_at=datetime('now','localtime') WHERE id=?", (task_id,))
    log_action(db, "task_resumed", "task", task_id)
    db.commit()
    db.close()
    return {"status": "ok", "task_id": task_id, "new_status": "pending"}


def start_task(task_id):
    """Record the start time for a task (V2 time tracking)."""
    db = get_db()
    task = db.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    if not task:
        db.close()
        return {"status": "error", "message": f"Task {task_id} not found"}
    if task["status"] == "completed":
        db.close()
        return {"status": "error", "message": f"Task {task_id} is already completed"}
    now_iso = datetime.now().isoformat()
    db.execute(
        "UPDATE tasks SET status='in_progress', started_at=?, updated_at=datetime('now','localtime') WHERE id=?",
        (now_iso, task_id)
    )
    log_action(db, "task_started", "task", task_id, {"title": task["title"], "started_at": now_iso})
    db.commit()
    db.close()
    return {"status": "ok", "task_id": task_id, "title": task["title"], "started_at": now_iso}


def get_actionable_tasks():
    """Get all tasks that can be worked on today (pending or in_progress, human-assigned)."""
    db = get_db()
    rows = db.execute("""
        SELECT t.*, t.category as task_category,
               p.title as project_title, p.goal_id, g.title as goal_title, g.priority as goal_priority,
               p.progress_pct, p.momentum_score
        FROM tasks t
        JOIN projects p ON t.project_id = p.id
        JOIN goals g ON p.goal_id = g.id
        WHERE t.status IN ('pending', 'in_progress')
        AND t.assignee = 'human'
        AND g.status = 'active'
        AND p.status = 'active'
        ORDER BY t.created_at
    """).fetchall()
    db.close()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────────
# Calendar Integration (V2)
# ─────────────────────────────────────────────

def connect_calendar(name, source_path, source_type="ical_url"):
    """Register a calendar source (ical URL or local .ics file path)."""
    db = get_db()
    # Check if already exists
    existing = db.execute(
        "SELECT id FROM calendar_config WHERE source_path=?", (source_path,)
    ).fetchone()
    if existing:
        db.close()
        return {"status": "ok", "calendar_id": existing["id"], "message": "Calendar already connected", "name": name}
    cur = db.execute(
        "INSERT INTO calendar_config (name, source_type, source_path) VALUES (?,?,?)",
        (name, source_type, source_path)
    )
    cal_id = cur.lastrowid
    log_action(db, "calendar_connected", "calendar", cal_id, {"name": name, "source_type": source_type})
    db.commit()
    db.close()
    return {"status": "ok", "calendar_id": cal_id, "name": name, "source_type": source_type}


def list_calendars():
    """List all registered calendar sources."""
    db = get_db()
    rows = db.execute("SELECT * FROM calendar_config ORDER BY created_at").fetchall()
    db.close()
    return [dict(r) for r in rows]


def disconnect_calendar(cal_id):
    """Remove a calendar source and its cached events."""
    db = get_db()
    db.execute("DELETE FROM calendar_events WHERE calendar_id=?", (cal_id,))
    db.execute("DELETE FROM calendar_config WHERE id=?", (cal_id,))
    db.commit()
    db.close()
    return {"status": "ok", "message": f"Calendar {cal_id} disconnected"}


def _fetch_ical_data(source_path, source_type):
    """Fetch raw ical data from URL or local file."""
    if source_type == "ical_file":
        path = os.path.expanduser(source_path)
        if not os.path.exists(path):
            return None, f"File not found: {path}"
        with open(path, "rb") as f:
            return f.read(), None
    elif source_type == "ical_url":
        if not HAS_URLLIB:
            return None, "urllib not available"
        try:
            req = Request(source_path, headers={"User-Agent": "GetToIt/2.0"})
            with urlopen(req, timeout=15) as resp:
                return resp.read(), None
        except Exception as e:
            return None, f"Failed to fetch URL: {e}"
    return None, f"Unknown source type: {source_type}"


def _parse_ical_events(ical_data, target_date=None):
    """
    Parse ical data and extract events for target_date.
    Returns list of {summary, dtstart, dtend, all_day, location}.
    """
    if not HAS_ICAL:
        return [], "icalendar library not installed (pip install icalendar)"

    if target_date is None:
        target_date = date.today()

    try:
        cal = iCalendar.from_ical(ical_data)
    except Exception as e:
        return [], f"Failed to parse ical: {e}"

    events = []
    for component in cal.walk():
        if component.name != "VEVENT":
            continue

        dtstart = component.get("dtstart")
        dtend = component.get("dtend")
        if not dtstart:
            continue

        dtstart_val = dtstart.dt
        dtend_val = dtend.dt if dtend else None

        # Handle all-day events (date objects, not datetime)
        is_all_day = isinstance(dtstart_val, date) and not isinstance(dtstart_val, datetime)

        if is_all_day:
            event_date = dtstart_val
            if event_date != target_date:
                # Check multi-day all-day events
                if dtend_val and target_date >= dtstart_val and target_date < dtend_val:
                    pass  # Target date falls within multi-day event
                else:
                    continue
            start_str = f"{target_date.isoformat()}T00:00:00"
            end_str = f"{target_date.isoformat()}T23:59:59"
        else:
            # For datetime events, handle timezone-naive comparison
            if hasattr(dtstart_val, 'date'):
                event_date = dtstart_val.date()
            else:
                continue

            # Check if event falls on target_date
            if event_date != target_date:
                # Check if multi-hour event spans into target_date
                if dtend_val and hasattr(dtend_val, 'date'):
                    if not (dtstart_val.date() <= target_date <= dtend_val.date()):
                        continue
                else:
                    continue

            start_str = dtstart_val.isoformat()
            end_str = dtend_val.isoformat() if dtend_val else start_str

        summary = str(component.get("summary", "（無標題）"))
        location = str(component.get("location", "")) if component.get("location") else None

        events.append({
            "summary": summary,
            "dtstart": start_str,
            "dtend": end_str,
            "all_day": is_all_day,
            "location": location,
            "event_date": target_date.isoformat(),
        })

    # Sort by start time
    events.sort(key=lambda e: e["dtstart"])
    return events, None


def sync_calendar(cal_id=None, target_date=None):
    """
    Sync one or all calendars: fetch ical data, parse events for target_date,
    store in calendar_events cache.
    """
    if target_date is None:
        target_date = date.today()

    db = get_db()
    if cal_id:
        calendars = db.execute("SELECT * FROM calendar_config WHERE id=? AND enabled=1", (cal_id,)).fetchall()
    else:
        calendars = db.execute("SELECT * FROM calendar_config WHERE enabled=1").fetchall()

    if not calendars:
        db.close()
        return {"status": "ok", "message": "No calendars configured", "events": [], "synced": 0}

    all_events = []
    errors = []
    date_str = target_date.isoformat()

    for cal in calendars:
        cal = dict(cal)
        # Fetch ical data
        ical_data, err = _fetch_ical_data(cal["source_path"], cal["source_type"])
        if err:
            errors.append({"calendar": cal["name"], "error": err})
            continue

        # Parse events
        events, parse_err = _parse_ical_events(ical_data, target_date)
        if parse_err:
            errors.append({"calendar": cal["name"], "error": parse_err})
            continue

        # Clear old cached events for this calendar + date
        db.execute(
            "DELETE FROM calendar_events WHERE calendar_id=? AND event_date=?",
            (cal["id"], date_str)
        )

        # Insert new events
        for ev in events:
            db.execute(
                "INSERT INTO calendar_events (calendar_id, summary, dtstart, dtend, all_day, location, event_date) VALUES (?,?,?,?,?,?,?)",
                (cal["id"], ev["summary"], ev["dtstart"], ev["dtend"], 1 if ev["all_day"] else 0, ev["location"], date_str)
            )

        # Update last_synced_at
        db.execute(
            "UPDATE calendar_config SET last_synced_at=datetime('now','localtime') WHERE id=?",
            (cal["id"],)
        )

        all_events.extend(events)

    log_action(db, "calendar_synced", details={"date": date_str, "events_count": len(all_events)})
    db.commit()
    db.close()

    return {
        "status": "ok",
        "date": date_str,
        "events": all_events,
        "synced": len(calendars) - len(errors),
        "errors": errors if errors else None,
    }


def get_today_events(target_date=None):
    """Get cached events for today (or target_date) from DB."""
    if target_date is None:
        target_date = date.today()
    date_str = target_date.isoformat()

    db = get_db()
    rows = db.execute(
        "SELECT ce.*, cc.name as calendar_name FROM calendar_events ce JOIN calendar_config cc ON ce.calendar_id=cc.id WHERE ce.event_date=? ORDER BY ce.dtstart",
        (date_str,)
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def calculate_free_time(target_date=None, work_start="09:00", work_end="18:00"):
    """
    Calculate available free time slots based on today's calendar events.
    Returns total free hours and a list of free slots.

    work_start/work_end define the working window (24h format).
    """
    if target_date is None:
        target_date = date.today()

    events = get_today_events(target_date)

    ws_h, ws_m = map(int, work_start.split(":"))
    we_h, we_m = map(int, work_end.split(":"))
    day_start = datetime.combine(target_date, dtime(ws_h, ws_m))
    day_end = datetime.combine(target_date, dtime(we_h, we_m))

    # Collect busy blocks (non-all-day events only)
    busy = []
    all_day_events = []
    timed_events = []

    for ev in events:
        if ev["all_day"]:
            all_day_events.append(ev)
            continue

        try:
            ev_start = datetime.fromisoformat(ev["dtstart"].replace("Z", "+00:00"))
            ev_end = datetime.fromisoformat(ev["dtend"].replace("Z", "+00:00"))

            # Strip timezone info for naive comparison
            if ev_start.tzinfo:
                ev_start = ev_start.replace(tzinfo=None)
            if ev_end.tzinfo:
                ev_end = ev_end.replace(tzinfo=None)

            # Clamp to work window
            block_start = max(ev_start, day_start)
            block_end = min(ev_end, day_end)
            if block_start < block_end:
                busy.append((block_start, block_end))
                timed_events.append({
                    "summary": ev["summary"],
                    "start": block_start.strftime("%H:%M"),
                    "end": block_end.strftime("%H:%M"),
                    "minutes": round((block_end - block_start).total_seconds() / 60),
                })
        except (ValueError, TypeError):
            continue

    # Merge overlapping busy blocks
    busy.sort()
    merged = []
    for start, end in busy:
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))

    # Calculate free slots
    free_slots = []
    cursor = day_start
    for bstart, bend in merged:
        if cursor < bstart:
            free_slots.append({
                "start": cursor.strftime("%H:%M"),
                "end": bstart.strftime("%H:%M"),
                "minutes": round((bstart - cursor).total_seconds() / 60),
            })
        cursor = max(cursor, bend)
    if cursor < day_end:
        free_slots.append({
            "start": cursor.strftime("%H:%M"),
            "end": day_end.strftime("%H:%M"),
            "minutes": round((day_end - cursor).total_seconds() / 60),
        })

    total_free_minutes = sum(s["minutes"] for s in free_slots)
    total_busy_minutes = sum(e["minutes"] for e in timed_events)

    return {
        "date": target_date.isoformat(),
        "work_window": f"{work_start}-{work_end}",
        "total_free_hours": round(total_free_minutes / 60, 1),
        "total_free_minutes": total_free_minutes,
        "total_busy_minutes": total_busy_minutes,
        "free_slots": free_slots,
        "timed_events": timed_events,
        "all_day_events": [{"summary": e["summary"]} for e in all_day_events],
        "event_count": len(events),
    }


# ─────────────────────────────────────────────
# Time Prediction Model (V2)
# ─────────────────────────────────────────────

def update_time_model(db, category, estimated_minutes, actual_minutes, goal_id=None):
    """
    Update the rolling accuracy model for a task category.
    Uses exponential weighted moving average (alpha=0.3) so recent data has more weight.
    Returns feedback dict for the user.
    """
    category = category or "_general"
    ratio = actual_minutes / estimated_minutes if estimated_minutes > 0 else 1.0

    row = db.execute(
        "SELECT * FROM time_estimates WHERE task_category=?", (category,)
    ).fetchone()

    alpha = 0.3  # Weight for new observation
    if row:
        old_ratio = row["accuracy_ratio"]
        old_count = row["sample_count"]
        new_ratio = round(old_ratio * (1 - alpha) + ratio * alpha, 3)
        new_count = old_count + 1
        # Rolling median approximation: use weighted average as proxy
        old_median = row["estimated_minutes_median"] or actual_minutes
        new_median = round(old_median * (1 - alpha) + actual_minutes * alpha, 1)
        db.execute(
            "UPDATE time_estimates SET accuracy_ratio=?, sample_count=?, estimated_minutes_median=?, updated_at=datetime('now','localtime') WHERE id=?",
            (new_ratio, new_count, new_median, row["id"])
        )
    else:
        new_ratio = ratio
        new_count = 1
        db.execute(
            "INSERT INTO time_estimates (task_category, goal_id, accuracy_ratio, sample_count, estimated_minutes_median) VALUES (?,?,?,?,?)",
            (category, goal_id, round(ratio, 3), 1, actual_minutes)
        )

    return {
        "category": category,
        "this_ratio": round(ratio, 2),
        "rolling_ratio": round(new_ratio, 2) if row else round(ratio, 2),
        "sample_count": new_count,
        "interpretation": _interpret_ratio(ratio),
    }


def _interpret_ratio(ratio):
    """Human-readable interpretation of actual/estimated ratio."""
    if ratio <= 0.7:
        return "faster_than_expected"
    elif ratio <= 1.3:
        return "on_target"
    elif ratio <= 2.0:
        return "slower_than_expected"
    else:
        return "significantly_over"


def smart_estimate(category, user_raw_estimate):
    """
    Adjust a user's raw time estimate based on historical accuracy.
    Returns calibrated estimate in minutes.
    """
    db = get_db()
    category = category or "_general"
    row = db.execute(
        "SELECT accuracy_ratio, sample_count FROM time_estimates WHERE task_category=?",
        (category,)
    ).fetchone()
    db.close()

    if row and row["sample_count"] >= 3:
        ratio = row["accuracy_ratio"]
        calibrated = round(user_raw_estimate * ratio)
        return {
            "raw_estimate": user_raw_estimate,
            "calibrated_estimate": calibrated,
            "ratio": ratio,
            "sample_count": row["sample_count"],
            "calibrated": True,
        }
    else:
        return {
            "raw_estimate": user_raw_estimate,
            "calibrated_estimate": user_raw_estimate,
            "ratio": 1.0,
            "sample_count": row["sample_count"] if row else 0,
            "calibrated": False,
        }


def get_time_stats(category=None):
    """Get time prediction accuracy statistics."""
    db = get_db()

    # Per-category stats from time_estimates table
    if category:
        rows = db.execute(
            "SELECT * FROM time_estimates WHERE task_category=?", (category,)
        ).fetchall()
    else:
        rows = db.execute("SELECT * FROM time_estimates ORDER BY sample_count DESC").fetchall()
    categories = [dict(r) for r in rows]

    # Overall stats from completed tasks with both estimated and actual
    completed = db.execute("""
        SELECT estimated_minutes, actual_minutes, category
        FROM tasks
        WHERE status='completed' AND actual_minutes IS NOT NULL AND estimated_minutes IS NOT NULL
        ORDER BY completed_at DESC
    """).fetchall()
    db.close()

    total_tasks = len(completed)
    if total_tasks > 0:
        ratios = [t["actual_minutes"] / t["estimated_minutes"] for t in completed if t["estimated_minutes"] > 0]
        avg_ratio = round(sum(ratios) / len(ratios), 2) if ratios else 1.0
        on_target = sum(1 for r in ratios if 0.7 <= r <= 1.3)
        accuracy_pct = round(on_target / len(ratios) * 100, 1) if ratios else 0
        total_overrun = round(sum(
            (t["actual_minutes"] - t["estimated_minutes"])
            for t in completed if t["actual_minutes"] > t["estimated_minutes"]
        ))
    else:
        avg_ratio = None
        accuracy_pct = None
        total_overrun = 0

    return {
        "total_tracked_tasks": total_tasks,
        "overall_accuracy_ratio": avg_ratio,
        "on_target_pct": accuracy_pct,
        "total_overrun_minutes": total_overrun,
        "categories": categories,
    }


# ─────────────────────────────────────────────
# Ideas
# ─────────────────────────────────────────────

def capture_idea(raw_input, relevance_score=None, related_goal_id=None, motivation="medium", suggested_action="idea_bank"):
    db = get_db()
    cur = db.execute(
        "INSERT INTO ideas (raw_input, relevance_score, related_goal_id, motivation_at_capture, suggested_action) VALUES (?,?,?,?,?)",
        (raw_input, relevance_score, related_goal_id, motivation, suggested_action)
    )
    iid = cur.lastrowid
    log_action(db, "idea_captured", "idea", iid, {"raw_input": raw_input[:100], "relevance": relevance_score})
    db.commit()
    db.close()
    return {"status": "ok", "idea_id": iid, "suggested_action": suggested_action}


def list_ideas(include_all=False):
    db = get_db()
    if include_all:
        rows = db.execute("SELECT * FROM ideas ORDER BY created_at DESC").fetchall()
    else:
        rows = db.execute("SELECT * FROM ideas WHERE status='captured' ORDER BY created_at DESC").fetchall()
    db.close()
    return [dict(r) for r in rows]


def promote_idea(idea_id, project_id, title=None):
    db = get_db()
    idea = db.execute("SELECT * FROM ideas WHERE id=?", (idea_id,)).fetchone()
    if not idea:
        db.close()
        return {"status": "error", "message": f"Idea {idea_id} not found"}
    task_title = title or idea["raw_input"][:80]
    cur = db.execute(
        "INSERT INTO tasks (project_id, title, description, assignee) VALUES (?,?,?,?)",
        (project_id, task_title, f"Promoted from idea #{idea_id}: {idea['raw_input']}", "human")
    )
    tid = cur.lastrowid
    db.execute("UPDATE ideas SET status='promoted' WHERE id=?", (idea_id,))
    log_action(db, "idea_promoted", "idea", idea_id, {"task_id": tid, "project_id": project_id})
    db.commit()
    db.close()
    return {"status": "ok", "task_id": tid, "from_idea": idea_id}


# ─────────────────────────────────────────────
# Daily Logs & Mood
# ─────────────────────────────────────────────

def record_mood(emoji):
    """Record daily mood: fire, neutral, tired."""
    mood_map = {"fire": "fire", "🔥": "fire", "neutral": "neutral", "😐": "neutral", "tired": "tired", "😴": "tired"}
    mood = mood_map.get(emoji, emoji)
    today = datetime.now().strftime("%Y-%m-%d")
    db = get_db()
    db.execute(
        "INSERT INTO daily_logs (date, emoji_mood) VALUES (?, ?) ON CONFLICT(date) DO UPDATE SET emoji_mood=?",
        (today, mood, mood)
    )
    log_action(db, "mood_recorded", details={"mood": mood, "date": today})
    db.commit()
    db.close()
    return {"status": "ok", "date": today, "mood": mood}


def set_today_hours(hours):
    today = datetime.now().strftime("%Y-%m-%d")
    db = get_db()
    db.execute(
        "INSERT INTO daily_logs (date, available_hours) VALUES (?, ?) ON CONFLICT(date) DO UPDATE SET available_hours=?",
        (today, hours, hours)
    )
    db.commit()
    db.close()
    return {"status": "ok", "date": today, "available_hours": hours}


def get_today_hours():
    today = datetime.now().strftime("%Y-%m-%d")
    db = get_db()
    row = db.execute("SELECT available_hours FROM daily_logs WHERE date=?", (today,)).fetchone()
    db.close()
    return row["available_hours"] if row and row["available_hours"] else None


# ─────────────────────────────────────────────
# Memory (Short-term, 14-day rolling)
# ─────────────────────────────────────────────

def remember(content, mem_type="context", related_task_id=None):
    expires = (datetime.now() + timedelta(days=14)).isoformat()
    db = get_db()
    cur = db.execute(
        "INSERT INTO memory (type, content, related_task_id, expires_at) VALUES (?,?,?,?)",
        (mem_type, content, related_task_id, expires)
    )
    db.commit()
    db.close()
    return {"status": "ok", "memory_id": cur.lastrowid}


def list_memory():
    """List active (non-expired) memories."""
    now = datetime.now().isoformat()
    db = get_db()
    rows = db.execute(
        "SELECT * FROM memory WHERE expires_at > ? ORDER BY created_at DESC",
        (now,)
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def cleanup_expired_memory():
    now = datetime.now().isoformat()
    db = get_db()
    db.execute("DELETE FROM memory WHERE expires_at <= ?", (now,))
    db.commit()
    db.close()


# ─────────────────────────────────────────────
# Momentum Calculation
# ─────────────────────────────────────────────

def calculate_momentum(days=7):
    """
    Calculate momentum score over the last N days.
    Dual signal: completed sub-tasks (objective) + emoji mood (subjective).
    Score: 0-100.
    """
    db = get_db()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    logs = db.execute(
        "SELECT * FROM daily_logs WHERE date >= ? AND date <= ? ORDER BY date",
        (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    ).fetchall()

    mood_scores = {"fire": 2, "neutral": 1, "tired": 0}
    total_mood = 0
    total_tasks = 0
    active_days = 0
    streak = 0
    max_streak = 0
    daily_data = []

    for log in logs:
        l = dict(log)
        mood = mood_scores.get(l.get("emoji_mood"), 1)
        tasks = l.get("tasks_completed", 0)
        total_mood += mood
        total_tasks += tasks
        is_active = tasks > 0 or l.get("emoji_mood") == "fire"
        if is_active:
            active_days += 1
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 0
        daily_data.append({
            "date": l["date"],
            "mood": l.get("emoji_mood", "?"),
            "tasks_completed": tasks,
            "is_active": is_active
        })

    # Normalize to 0-100
    days_counted = max(len(logs), 1)
    mood_score = (total_mood / (days_counted * 2)) * 40        # 0-40 from mood
    task_score = min(total_tasks / days_counted * 10, 40)       # 0-40 from tasks (cap at ~4/day)
    streak_score = min(max_streak / days * 20, 20)              # 0-20 from streak

    momentum = round(mood_score + task_score + streak_score, 1)

    # Trend detection
    if len(daily_data) >= 4:
        first_half = daily_data[:len(daily_data)//2]
        second_half = daily_data[len(daily_data)//2:]
        first_active = sum(1 for d in first_half if d["is_active"])
        second_active = sum(1 for d in second_half if d["is_active"])
        if second_active > first_active:
            trend = "accelerating"
        elif second_active < first_active:
            trend = "decelerating"
        else:
            trend = "steady"
    else:
        trend = "insufficient_data"

    db.close()
    return {
        "momentum_score": momentum,
        "trend": trend,
        "active_days": active_days,
        "total_days": days_counted,
        "current_streak": streak,
        "max_streak": max_streak,
        "total_tasks_completed": total_tasks,
        "daily_data": daily_data
    }


# ─────────────────────────────────────────────
# ML Weight Learning (Priority 3)
# ─────────────────────────────────────────────

def load_scoring_weights():
    """Load scoring weights from DB. Returns dict with factor -> weight mapping.
    _source is 'learned' if any weights have been trained, else 'default'.
    """
    db = get_db()
    rows = db.execute("SELECT factor, weight, sample_count FROM scoring_weights").fetchall()
    db.close()
    w = {}
    trained = False
    for r in rows:
        w[r["factor"]] = r["weight"]
        if r["sample_count"] > 0:
            trained = True
    # Fill defaults for any missing factors
    defaults = {"deadline": 30.0, "goal_priority": 20.0, "momentum": 15.0,
                "skip_penalty": 10.0, "time_fit": 15.0, "proximity": 10.0}
    for k, v in defaults.items():
        if k not in w:
            w[k] = v
    w["_source"] = "learned" if trained else "default"
    return w


def learn_weights():
    """
    Train scoring weights using logistic regression on recommendation_log data.
    Requires >= 10 completed recommendations to be meaningful.

    Returns a dict with training results or an error if insufficient data.
    """
    db = get_db()

    # Pull all logged recommendations with their completion outcome
    rows = db.execute("""
        SELECT rl.task_id, rl.position, rl.priority_score, rl.factors,
               rl.was_completed, t.actual_minutes, t.estimated_minutes
        FROM recommendation_log rl
        LEFT JOIN tasks t ON t.id = rl.task_id
        WHERE rl.brief_date >= date('now', '-90 days', 'localtime')
        ORDER BY rl.created_at
    """).fetchall()

    if len(rows) < 10:
        db.close()
        return {
            "status": "insufficient_data",
            "sample_count": len(rows),
            "message": f"Need ≥10 logged recommendations, have {len(rows)}. Keep using the morning brief to gather data."
        }

    factor_names = ["deadline", "goal_priority", "momentum", "skip_penalty", "time_fit", "proximity"]

    # Build feature matrix X and label vector y
    X_rows = []
    y = []
    for r in rows:
        try:
            factors = json.loads(r["factors"]) if r["factors"] else {}
        except (json.JSONDecodeError, TypeError):
            factors = {}
        # Feature vector: per-factor contribution normalized to [0,1]
        feat = []
        for f in factor_names:
            val = factors.get(f, 0.0)
            # Normalise by the default max weight for the factor so all features are ~[0,1]
            max_vals = {"deadline": 30.0, "goal_priority": 20.0, "momentum": 15.0,
                        "skip_penalty": 10.0, "time_fit": 15.0, "proximity": 10.0}
            feat.append(val / max_vals.get(f, 10.0))
        X_rows.append(feat)
        y.append(1 if r["was_completed"] else 0)

    if not HAS_NUMPY:
        db.close()
        return {"status": "error", "message": "numpy not available — install numpy to enable ML weight learning"}

    X = np.array(X_rows, dtype=float)
    y = np.array(y, dtype=float)

    # Simple logistic regression via gradient descent (no sklearn needed)
    n_samples, n_features = X.shape
    theta = np.zeros(n_features)
    lr = 0.1
    for _ in range(500):
        z = X.dot(theta)
        h = 1.0 / (1.0 + np.exp(-np.clip(z, -20, 20)))
        grad = X.T.dot(h - y) / n_samples
        theta -= lr * grad

    # Convert learned coefficients → weights (scale to [0, 30] range)
    theta_abs = np.abs(theta)
    total = theta_abs.sum()
    if total > 0:
        # Proportional rescaling: preserve total weight budget of ~100
        total_budget = 100.0
        new_weights = (theta_abs / total) * total_budget
    else:
        # No signal — keep defaults
        new_weights = np.array([30.0, 20.0, 15.0, 10.0, 15.0, 10.0])

    # Update DB
    now_str = datetime.now().isoformat()
    for fname, nw in zip(factor_names, new_weights):
        db.execute(
            """UPDATE scoring_weights
               SET weight=?, sample_count=sample_count+?, last_trained=?, updated_at=?
               WHERE factor=?""",
            (round(float(nw), 2), len(rows), now_str, now_str, fname)
        )
    db.commit()
    db.close()

    result_weights = {f: round(float(w), 2) for f, w in zip(factor_names, new_weights)}
    return {
        "status": "ok",
        "sample_count": len(rows),
        "completion_rate": round(float(y.mean()), 3),
        "weights_learned": result_weights,
        "message": f"Weights updated from {len(rows)} samples (completion rate: {y.mean():.1%})"
    }


def weight_stats():
    """Return current scoring weights and training metadata."""
    db = get_db()
    rows = db.execute(
        "SELECT factor, weight, sample_count, last_trained FROM scoring_weights ORDER BY weight DESC"
    ).fetchall()
    log_count = db.execute("SELECT COUNT(*) as c FROM recommendation_log").fetchone()["c"]
    completed_count = db.execute(
        "SELECT COUNT(*) as c FROM recommendation_log WHERE was_completed=1"
    ).fetchone()["c"]
    db.close()

    weights = [dict(r) for r in rows]
    trained = any(r["sample_count"] > 0 for r in weights)
    return {
        "status": "ok",
        "source": "learned" if trained else "default",
        "weights": weights,
        "total_recommendations_logged": log_count,
        "total_completed": completed_count,
        "completion_rate": round(completed_count / log_count, 3) if log_count > 0 else 0,
        "ready_to_train": log_count >= 10,
    }


# ─────────────────────────────────────────────
# Morning Brief (Priority Engine)
# ─────────────────────────────────────────────

def morning_brief(available_hours=None, output_format="json"):
    """
    Generate the morning brief: Top 3 tasks with reasoning.
    Considers: deadline, goal priority, momentum, skip count, available time, task size.
    If calendar is connected, auto-syncs and calculates free time.
    Returns structured data for the persona layer to format.
    """
    # V2: Calendar integration — auto-sync and calculate free time
    calendar_info = None
    calendars = list_calendars()
    if calendars:
        sync_result = sync_calendar()  # Sync all enabled calendars
        free_time = calculate_free_time()
        calendar_info = {
            "free_time": free_time,
            "sync_result": sync_result,
        }
        # Use calendar-derived hours if user didn't manually specify
        if available_hours is None and free_time["total_free_hours"] > 0:
            available_hours = free_time["total_free_hours"]

    if available_hours:
        set_today_hours(available_hours)

    hours = available_hours or get_today_hours()
    tasks = get_actionable_tasks()
    momentum = calculate_momentum()
    memories = list_memory()
    cleanup_expired_memory()

    # V2: Recall relevant long-term memories using today's task titles as query
    long_term_context = []
    if tasks:
        query_text = " ".join(t["title"] for t in tasks[:5])
        recalled = recall_relevant(query_text, n=3)
        long_term_context = [
            {"id": r["id"], "content": r["content"], "type": r.get("content_type", "context")}
            for r in recalled
        ]

    # V2: Check for agent tasks needing attention
    agent_attention = []
    try:
        agent_st = get_agent_status()
        agent_attention = agent_st.get("needs_attention", [])
    except Exception:
        pass

    # V2 P3: Load dynamic scoring weights from DB
    w = load_scoring_weights()

    # Build context for each task
    scored_tasks = []
    now = datetime.now()

    for t in tasks:
        score = 0
        reasons = []
        factors = {}  # Track per-factor contributions for ML logging

        # 1. Deadline pressure
        deadline_contrib = 0
        if t["deadline"]:
            try:
                dl = datetime.fromisoformat(t["deadline"])
                days_left = (dl - now).days
                if days_left <= 0:
                    deadline_contrib = w["deadline"]
                    reasons.append("deadline_overdue")
                elif days_left <= 2:
                    deadline_contrib = w["deadline"] * 0.83
                    reasons.append("deadline_imminent")
                elif days_left <= 7:
                    deadline_contrib = w["deadline"] * 0.5
                    reasons.append("deadline_this_week")
            except:
                pass
        score += deadline_contrib
        factors["deadline"] = round(deadline_contrib, 2)

        # 2. Goal priority
        goal_p = t.get("goal_priority", 5)
        goal_contrib = (goal_p / 10) * w["goal_priority"]
        score += goal_contrib
        factors["goal_priority"] = round(goal_contrib, 2)
        if goal_p >= 8:
            reasons.append("high_priority_goal")

        # 3. Project momentum
        proj_momentum = t.get("momentum_score", 0)
        if proj_momentum > 50:
            mom_contrib = w["momentum"]
            reasons.append("high_momentum_project")
        elif proj_momentum > 20:
            mom_contrib = w["momentum"] * 0.53
        else:
            mom_contrib = 0
        score += mom_contrib
        factors["momentum"] = round(mom_contrib, 2)

        # 4. Skip count penalty
        if t["skip_count"] >= 3:
            skip_contrib = -w["skip_penalty"]
            reasons.append("frequently_skipped_needs_checkin")
        elif t["skip_count"] >= 1:
            skip_contrib = -w["skip_penalty"] * 0.3
        else:
            skip_contrib = 0
        score += skip_contrib
        factors["skip_penalty"] = round(skip_contrib, 2)

        # V2: Get calibrated time estimate
        calibrated_est = None
        if t["estimated_minutes"]:
            cal = smart_estimate(t.get("task_category") or t.get("category"), t["estimated_minutes"])
            if cal["calibrated"]:
                calibrated_est = cal["calibrated_estimate"]

        effective_minutes = calibrated_est or t.get("estimated_minutes")

        # 5. Time fit (using calibrated time + dynamic weight)
        time_contrib = 0
        if hours and effective_minutes:
            available_min = hours * 60
            if effective_minutes <= available_min * 0.4:
                time_contrib = w["time_fit"]
                reasons.append("fits_available_time")
            elif effective_minutes <= available_min * 0.8:
                time_contrib = w["time_fit"] * 0.53
            else:
                time_contrib = -w["time_fit"] * 0.33
                reasons.append("too_large_for_today")
        score += time_contrib
        factors["time_fit"] = round(time_contrib, 2)

        # 6. Progress proximity
        pct = t.get("progress_pct", 0)
        if pct >= 70:
            prox_contrib = w["proximity"]
            reasons.append("project_almost_done")
        elif pct >= 40:
            prox_contrib = w["proximity"] * 0.5
        else:
            prox_contrib = 0
        score += prox_contrib
        factors["proximity"] = round(prox_contrib, 2)

        # Check memory for skip reasons related to this task
        task_memories = [m for m in memories if m.get("related_task_id") == t["id"]]
        if task_memories:
            reasons.append("has_memory_context")

        scored_tasks.append({
            **t,
            "priority_score": score,
            "reasons": reasons,
            "task_memories": [m["content"] for m in task_memories],
            "calibrated_minutes": calibrated_est,
            "factors": factors,
        })

    # Sort by score, take top 3
    scored_tasks.sort(key=lambda x: x["priority_score"], reverse=True)
    top3 = scored_tasks[:3]

    # Calculate total estimated time (prefer calibrated)
    total_min = sum(t.get("calibrated_minutes") or t.get("estimated_minutes") or 30 for t in top3)

    # Check for stagnation (trigger persona pressure)
    days_since_last_complete = None
    db = get_db()
    last = db.execute(
        "SELECT created_at FROM action_log WHERE action_type='task_completed' ORDER BY created_at DESC LIMIT 1"
    ).fetchone()

    # V2 P3: Log recommendations for ML training (upsert by date + task_id)
    today_str = now.strftime("%Y-%m-%d")
    for pos, task in enumerate(top3, 1):
        existing = db.execute(
            "SELECT id FROM recommendation_log WHERE task_id=? AND brief_date=?",
            (task["id"], today_str)
        ).fetchone()
        if not existing:
            db.execute(
                "INSERT INTO recommendation_log (task_id, brief_date, position, priority_score, factors) VALUES (?,?,?,?,?)",
                (task["id"], today_str, pos, task["priority_score"], json.dumps(task.get("factors", {})))
            )
    db.commit()

    db.close()
    if last:
        try:
            last_dt = datetime.fromisoformat(last["created_at"])
            days_since_last_complete = (now - last_dt).days
        except:
            pass

    # Determine persona mode
    if days_since_last_complete is None:
        persona_mode = "welcome"
    elif days_since_last_complete == 0:
        persona_mode = "normal"
    elif days_since_last_complete <= 2:
        persona_mode = "gentle_nudge"
    else:
        persona_mode = "firm_push"

    return {
        "date": today_str,
        "day_of_week": now.strftime("%A"),
        "available_hours": hours,
        "top3": top3,
        "total_estimated_minutes": total_min,
        "momentum": momentum,
        "persona_mode": persona_mode,
        "days_since_last_complete": days_since_last_complete,
        "total_actionable_tasks": len(scored_tasks),
        "active_goals": len(set(t.get("goal_title") for t in scored_tasks)),
        "calendar": calendar_info,
        "long_term_context": long_term_context,
        "agent_attention": [
            {"id": t["id"], "title": t["title"], "status": t["status"], "age_minutes": t.get("age_minutes")}
            for t in agent_attention
        ],
        "weights_source": w.get("_source", "default"),
    }


def _format_morning_telegram(brief):
    """Format morning brief as Telegram Markdown (v2-compatible) text."""
    lines = []
    date_str = brief.get("date", "今天")
    dow = brief.get("day_of_week", "")
    hours = brief.get("available_hours")
    cal = brief.get("calendar")

    # Header
    lines.append(f"🌅 *早安！{date_str} ({dow})*")
    if hours:
        lines.append(f"⏰ 今天可用時間：*{hours:.1f} 小時*")
    if cal and cal.get("free_time"):
        events = cal["free_time"].get("events_count", 0)
        if events:
            lines.append(f"📅 今天有 {events} 個行程")
    lines.append("")

    # Agent attention
    for a in brief.get("agent_attention", []):
        lines.append(f"⚠️ *Agent 任務需注意：* #{a['id']} {a['title']} (狀態: {a['status']})")
    if brief.get("agent_attention"):
        lines.append("")

    # Top 3
    lines.append("*📋 今日 Top 3*")
    top3 = brief.get("top3", [])
    indicators = {"deadline_overdue": "📌", "deadline_imminent": "📌", "high_priority_goal": "⚡",
                  "has_momentum": "🔄", "agent": "🤖", "has_memory_context": "💭"}
    for i, task in enumerate(top3, 1):
        reasons = task.get("reasons", [])
        emoji = ""
        for r in reasons:
            e = indicators.get(r)
            if e:
                emoji = e
                break
        title = task.get("title", "?")
        mins = task.get("calibrated_minutes") or task.get("estimated_minutes")
        time_str = f" \\(~{mins}分鐘\\)" if mins else ""
        lines.append(f"{i}\\. {emoji} *{title}*{time_str}")
        # Add memory note if any
        mems = task.get("task_memories", [])
        if mems:
            lines.append(f"   💭 _{mems[0]}_")
    lines.append("")

    # Long-term context
    ltm = brief.get("long_term_context", [])
    if ltm:
        lines.append(f"🧠 _{ltm[0]['content']}_")
        lines.append("")

    # Total estimate
    total_min = brief.get("total_estimated_minutes", 0)
    if total_min:
        h, m = divmod(total_min, 60)
        time_label = f"{h}小時{m}分" if h else f"{m}分鐘"
        lines.append(f"⏱ Top 3 預估合計：{time_label}")
    lines.append("")
    lines.append("從哪一件開始？回覆任務編號即可 🚀")

    return "\n".join(lines)


# ─────────────────────────────────────────────
# Review / Status
# ─────────────────────────────────────────────

def review(project_id=None):
    """Get progress review data."""
    db = get_db()
    if project_id:
        project = db.execute("SELECT p.*, g.title as goal_title FROM projects p JOIN goals g ON p.goal_id=g.id WHERE p.id=?", (project_id,)).fetchone()
        if not project:
            db.close()
            return {"status": "error", "message": f"Project {project_id} not found"}
        tasks = db.execute("SELECT * FROM tasks WHERE project_id=? ORDER BY created_at", (project_id,)).fetchall()
        milestones = json.loads(project["milestones"]) if project["milestones"] else []
        db.close()
        return {
            "project": dict(project),
            "tasks": [dict(t) for t in tasks],
            "milestones": milestones,
            "momentum": calculate_momentum()
        }
    else:
        goals = db.execute("SELECT * FROM goals WHERE status='active' ORDER BY priority DESC").fetchall()
        result = []
        for g in goals:
            projects = db.execute("SELECT * FROM projects WHERE goal_id=? AND status='active'", (g["id"],)).fetchall()
            goal_data = dict(g)
            goal_data["projects"] = []
            for p in projects:
                pdata = dict(p)
                total = db.execute("SELECT COUNT(*) FROM tasks WHERE project_id=?", (p["id"],)).fetchone()[0]
                done = db.execute("SELECT COUNT(*) FROM tasks WHERE project_id=? AND status='completed'", (p["id"],)).fetchone()[0]
                pending = db.execute("SELECT COUNT(*) FROM tasks WHERE project_id=? AND status='pending'", (p["id"],)).fetchone()[0]
                pdata["task_count"] = {"total": total, "completed": done, "pending": pending}
                goal_data["projects"].append(pdata)
            result.append(goal_data)
        db.close()
        return {
            "goals": result,
            "momentum": calculate_momentum()
        }


def overall_status():
    """Quick system status."""
    db = get_db()
    goals = db.execute("SELECT COUNT(*) FROM goals WHERE status='active'").fetchone()[0]
    projects = db.execute("SELECT COUNT(*) FROM projects WHERE status='active'").fetchone()[0]
    pending = db.execute("SELECT COUNT(*) FROM tasks WHERE status='pending'").fetchone()[0]
    in_progress = db.execute("SELECT COUNT(*) FROM tasks WHERE status='in_progress'").fetchone()[0]
    completed_total = db.execute("SELECT COUNT(*) FROM tasks WHERE status='completed'").fetchone()[0]
    ideas_count = db.execute("SELECT COUNT(*) FROM ideas WHERE status='captured'").fetchone()[0]
    db.close()
    return {
        "active_goals": goals,
        "active_projects": projects,
        "tasks_pending": pending,
        "tasks_in_progress": in_progress,
        "tasks_completed_total": completed_total,
        "ideas_in_bank": ideas_count,
        "momentum": calculate_momentum()
    }


# ─────────────────────────────────────────────
# Long-Term Memory (V2) — TF-IDF Vector Engine
# ─────────────────────────────────────────────
#
# Architecture: character n-gram TF-IDF stored as JSON arrays in SQLite.
# No model downloads required. Works for Chinese + English.
# At personal scale (<1000 memories) cosine similarity is fast enough (numpy).

def _tokenize(text):
    """
    Tokenize text into character bigrams + trigrams + words.
    Works naturally for Chinese (no spaces) and English.
    """
    import re
    tokens = []
    # Character n-grams (bigrams + trigrams) — handles Chinese
    for n in (2, 3):
        tokens.extend(text[i:i+n] for i in range(len(text) - n + 1))
    # Word-level tokens for English/pinyin
    words = re.findall(r'[a-zA-Z0-9\u4e00-\u9fff]+', text.lower())
    tokens.extend(words)
    return tokens


def _build_vocab_and_vectors(texts):
    """Build a shared vocabulary and TF-IDF vectors for a list of texts."""
    if not HAS_NUMPY:
        return None, None

    # Build token frequency per document
    token_counts = []
    for text in texts:
        tokens = _tokenize(text)
        freq = {}
        for t in tokens:
            freq[t] = freq.get(t, 0) + 1
        token_counts.append(freq)

    # Build global vocabulary (top 2000 by document frequency)
    df = {}
    for freq in token_counts:
        for t in freq:
            df[t] = df.get(t, 0) + 1

    vocab = sorted(df, key=lambda t: -df[t])[:2000]
    vocab_idx = {t: i for i, t in enumerate(vocab)}
    n_docs = max(len(texts), 1)
    idf = np.array([
        1.0 + np.log(n_docs / (df.get(t, 0) + 1))
        for t in vocab
    ], dtype=np.float32)

    # Compute TF-IDF vectors
    vectors = []
    for freq in token_counts:
        total = max(sum(freq.values()), 1)
        tf = np.zeros(len(vocab), dtype=np.float32)
        for t, c in freq.items():
            if t in vocab_idx:
                tf[vocab_idx[t]] = c / total
        vec = tf * idf
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        vectors.append(vec)

    return vocab, vectors


def _text_to_vector(text, vocab_idx, idf):
    """Project a single text onto an existing vocabulary."""
    if not HAS_NUMPY:
        return None
    tokens = _tokenize(text)
    freq = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    total = max(sum(freq.values()), 1)
    tf = np.zeros(len(vocab_idx), dtype=np.float32)
    for t, c in freq.items():
        if t in vocab_idx:
            tf[vocab_idx[t]] = c / total
    vec = tf * idf
    norm = np.linalg.norm(vec)
    return (vec / norm).tolist() if norm > 0 else vec.tolist()


def store_long_term(content, content_type="context", metadata=None):
    """
    Store an important statement in long-term memory.
    Computes a TF-IDF vector from all existing memories + this new one.
    content_type: 'preference' | 'constraint' | 'insight' | 'context'
    """
    db = get_db()
    meta_str = json.dumps(metadata) if metadata else None

    # Get all existing memories to rebuild shared vocabulary
    existing = db.execute("SELECT id, content, vector FROM long_term_memory").fetchall()
    all_texts = [r["content"] for r in existing] + [content]

    # Rebuild TF-IDF vectors for all (incremental rebuild on insert)
    vocab, vectors = _build_vocab_and_vectors(all_texts)

    if vocab is not None:
        # Update existing memory vectors
        for i, row in enumerate(existing):
            vec_str = json.dumps(vectors[i].tolist())
            db.execute("UPDATE long_term_memory SET vector=? WHERE id=?", (vec_str, row["id"]))
        new_vec_str = json.dumps(vectors[-1].tolist())
    else:
        new_vec_str = None

    cur = db.execute(
        "INSERT INTO long_term_memory (content, content_type, vector, metadata) VALUES (?,?,?,?)",
        (content, content_type, new_vec_str, meta_str)
    )
    ltm_id = cur.lastrowid
    log_action(db, "ltm_stored", "long_term_memory", ltm_id, {"type": content_type, "preview": content[:80]})
    db.commit()
    db.close()
    return {"status": "ok", "ltm_id": ltm_id, "content_type": content_type}


def recall_relevant(query, n=3, content_type=None):
    """
    Semantic search: find top-N long-term memories relevant to a query.
    Falls back to keyword overlap if numpy unavailable.
    """
    db = get_db()
    if content_type:
        rows = db.execute(
            "SELECT * FROM long_term_memory WHERE content_type=? ORDER BY created_at DESC",
            (content_type,)
        ).fetchall()
    else:
        rows = db.execute("SELECT * FROM long_term_memory ORDER BY created_at DESC").fetchall()

    if not rows:
        db.close()
        return []

    if HAS_NUMPY and rows[0]["vector"]:
        # Load stored vectors
        stored_vecs = []
        valid_rows = []
        for r in rows:
            if r["vector"]:
                try:
                    stored_vecs.append(np.array(json.loads(r["vector"]), dtype=np.float32))
                    valid_rows.append(r)
                except (json.JSONDecodeError, ValueError):
                    pass

        if stored_vecs:
            # Project query onto existing vocabulary
            all_texts = [r["content"] for r in valid_rows]
            vocab, all_vecs = _build_vocab_and_vectors(all_texts + [query])
            query_vec = np.array(all_vecs[-1], dtype=np.float32)
            doc_vecs = np.array([v.tolist() for v in all_vecs[:-1]], dtype=np.float32)

            # Cosine similarities (already normalized)
            scores = doc_vecs @ query_vec
            top_idx = np.argsort(scores)[::-1][:n]

            results = []
            for i in top_idx:
                if scores[i] > 0.05:  # Minimum relevance threshold
                    r = dict(valid_rows[i])
                    r.pop("vector", None)  # Strip vector from output
                    r["similarity"] = round(float(scores[i]), 4)
                    # Update last_accessed
                    db.execute("UPDATE long_term_memory SET last_accessed=datetime('now','localtime') WHERE id=?", (r["id"],))
                    results.append(r)
            db.commit()
            db.close()
            return results

    # Fallback: keyword overlap scoring
    query_tokens = set(_tokenize(query))
    scored = []
    for r in rows:
        doc_tokens = set(_tokenize(r["content"]))
        overlap = len(query_tokens & doc_tokens)
        if overlap > 0:
            scored.append((overlap, dict(r)))
    scored.sort(key=lambda x: -x[0])
    db.close()
    results = []
    for _, r in scored[:n]:
        r.pop("vector", None)
        results.append(r)
    return results


def list_long_term_memory(content_type=None):
    """List all long-term memories, optionally filtered by type."""
    db = get_db()
    if content_type:
        rows = db.execute(
            "SELECT id, content, content_type, created_at, last_accessed FROM long_term_memory WHERE content_type=? ORDER BY created_at DESC",
            (content_type,)
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT id, content, content_type, created_at, last_accessed FROM long_term_memory ORDER BY created_at DESC"
        ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def delete_long_term_memory(ltm_id):
    """Delete a specific long-term memory by ID."""
    db = get_db()
    db.execute("DELETE FROM long_term_memory WHERE id=?", (ltm_id,))
    db.commit()
    db.close()
    return {"status": "ok", "deleted_id": ltm_id}


# ─────────────────────────────────────────────
# Agent Task Management (V2)
# ─────────────────────────────────────────────

AGENT_TIMEOUT_MINUTES = 30


def get_agent_status():
    """
    List all agent tasks with their current state and age.
    Automatically marks timed-out tasks (>AGENT_TIMEOUT_MINUTES in agent_processing).
    """
    db = get_db()
    agent_tasks = db.execute("""
        SELECT t.*, p.title as project_title, g.title as goal_title
        FROM tasks t
        JOIN projects p ON t.project_id = p.id
        JOIN goals g ON p.goal_id = g.id
        WHERE t.assignee = 'agent'
        ORDER BY t.updated_at DESC
    """).fetchall()

    now = datetime.now()
    results = []
    timed_out = []

    for task in agent_tasks:
        t = dict(task)
        age_minutes = None
        is_stale = False

        if t["updated_at"]:
            try:
                updated = datetime.fromisoformat(t["updated_at"])
                age_minutes = round((now - updated).total_seconds() / 60)
                if t["status"] == "agent_processing" and age_minutes > AGENT_TIMEOUT_MINUTES:
                    is_stale = True
                    timed_out.append(t["id"])
            except (ValueError, TypeError):
                pass

        t["age_minutes"] = age_minutes
        t["is_timed_out"] = is_stale
        results.append(t)

    # Auto-mark timed-out tasks as agent_failed and update in-memory status too
    for tid in timed_out:
        db.execute(
            "UPDATE tasks SET status='agent_failed', updated_at=datetime('now','localtime') WHERE id=?",
            (tid,)
        )
        db.execute(
            "INSERT INTO agent_events (task_id, event_type, details) VALUES (?, 'timeout', ?)",
            (tid, json.dumps({"timeout_minutes": AGENT_TIMEOUT_MINUTES}))
        )
        log_action(db, "agent_timeout", "task", tid, {"timeout_minutes": AGENT_TIMEOUT_MINUTES})
        # Also update in-memory result
        for t in results:
            if t["id"] == tid:
                t["status"] = "agent_failed"
                t["is_timed_out"] = True

    if timed_out:
        db.commit()

    db.close()

    processing = [t for t in results if t["status"] == "agent_processing"]
    failed = [t for t in results if t["status"] == "agent_failed"]
    completed = [t for t in results if t["status"] == "completed"]
    pending = [t for t in results if t["status"] in ("pending", "in_progress")]

    return {
        "agent_tasks": results,
        "summary": {
            "processing": len(processing),
            "failed": len(failed),
            "completed": len(completed),
            "pending_for_agent": len(pending),
            "just_timed_out": timed_out,
        },
        "needs_attention": failed,
    }


def agent_retry(task_id):
    """Reset a failed/timed-out agent task back to pending for retry."""
    db = get_db()
    task = db.execute("SELECT * FROM tasks WHERE id=? AND assignee='agent'", (task_id,)).fetchone()
    if not task:
        db.close()
        return {"status": "error", "message": f"Agent task {task_id} not found"}
    if task["status"] not in ("agent_failed",):
        db.close()
        return {"status": "error", "message": f"Task {task_id} is {task['status']}, not failed — nothing to retry"}

    db.execute(
        "UPDATE tasks SET status='pending', started_at=NULL, updated_at=datetime('now','localtime') WHERE id=?",
        (task_id,)
    )
    db.execute(
        "INSERT INTO agent_events (task_id, event_type, details) VALUES (?, 'retry', ?)",
        (task_id, json.dumps({"previous_status": task["status"]}))
    )
    log_action(db, "agent_retry", "task", task_id, {"title": task["title"]})
    db.commit()
    db.close()
    return {"status": "ok", "task_id": task_id, "new_status": "pending", "message": f"Task '{task['title']}' queued for retry"}


def agent_handoff(task_id):
    """Reassign a failed agent task to human."""
    db = get_db()
    task = db.execute("SELECT * FROM tasks WHERE id=? AND assignee='agent'", (task_id,)).fetchone()
    if not task:
        db.close()
        return {"status": "error", "message": f"Agent task {task_id} not found"}

    db.execute(
        "UPDATE tasks SET assignee='human', status='pending', updated_at=datetime('now','localtime') WHERE id=?",
        (task_id,)
    )
    db.execute(
        "INSERT INTO agent_events (task_id, event_type, details) VALUES (?, 'handoff_to_human', ?)",
        (task_id, json.dumps({"previous_status": task["status"]}))
    )
    log_action(db, "agent_handoff", "task", task_id, {"title": task["title"]})
    db.commit()
    db.close()
    return {"status": "ok", "task_id": task_id, "new_assignee": "human", "message": f"Task '{task['title']}' handed off to you"}


# ─────────────────────────────────────────────
# Action Log
# ─────────────────────────────────────────────

def get_action_log(days=7):
    db = get_db()
    since = (datetime.now() - timedelta(days=days)).isoformat()
    rows = db.execute(
        "SELECT * FROM action_log WHERE created_at >= ? ORDER BY created_at DESC",
        (since,)
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────────
# CLI Entry Point
# ─────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "No command provided. Use: init, morning, capture, add-goal, add-project, add-task, start, complete, skip, pause, resume, review, mood, status, ideas, promote-idea, memory, remember, log, today-hours, time-stats, smart-estimate, connect-calendar, sync-calendar, list-calendars, disconnect-calendar, free-time"}))
        sys.exit(1)

    cmd = sys.argv[1]

    # Ensure DB exists
    if cmd != "init" and not os.path.exists(DB_PATH):
        init_db()

    try:
        if cmd == "init":
            result = init_db()

        elif cmd == "morning":
            hours = None
            if "--hours" in sys.argv:
                idx = sys.argv.index("--hours")
                hours = float(sys.argv[idx + 1])
            fmt = "json"
            if "--format" in sys.argv:
                idx = sys.argv.index("--format")
                fmt = sys.argv[idx + 1]
            brief_data = morning_brief(hours)
            if fmt == "telegram":
                # Output Telegram markdown text directly (not JSON)
                print(_format_morning_telegram(brief_data))
                sys.exit(0)
            result = brief_data

        elif cmd == "capture":
            if len(sys.argv) < 3:
                result = {"status": "error", "message": "Usage: capture 'text'"}
            else:
                text = sys.argv[2]
                relevance = float(sys.argv[3]) if len(sys.argv) > 3 else None
                goal_id = int(sys.argv[4]) if len(sys.argv) > 4 else None
                motivation = sys.argv[5] if len(sys.argv) > 5 else "medium"
                action = sys.argv[6] if len(sys.argv) > 6 else "idea_bank"
                result = capture_idea(text, relevance, goal_id, motivation, action)

        elif cmd == "add-goal":
            if len(sys.argv) < 3:
                result = {"status": "error", "message": "Usage: add-goal 'title' [--vision 'x'] [--priority N] [--deadline 'YYYY-MM-DD']"}
            else:
                title = sys.argv[2]
                vision = None; priority = 5; deadline = None
                args = sys.argv[3:]
                i = 0
                while i < len(args):
                    if args[i] == "--vision" and i+1 < len(args):
                        vision = args[i+1]; i += 2
                    elif args[i] == "--priority" and i+1 < len(args):
                        priority = int(args[i+1]); i += 2
                    elif args[i] == "--deadline" and i+1 < len(args):
                        deadline = args[i+1]; i += 2
                    else:
                        i += 1
                result = add_goal(title, vision, priority, deadline)

        elif cmd == "add-project":
            if len(sys.argv) < 4:
                result = {"status": "error", "message": "Usage: add-project GOAL_ID 'title'"}
            else:
                result = add_project(int(sys.argv[2]), sys.argv[3])

        elif cmd == "add-task":
            if len(sys.argv) < 4:
                result = {"status": "error", "message": "Usage: add-task PROJECT_ID 'title' [--assignee human|agent] [--minutes N] [--deadline 'YYYY-MM-DD']"}
            else:
                pid = int(sys.argv[2])
                title = sys.argv[3]
                assignee = "human"; minutes = None; deadline = None; desc = None
                args = sys.argv[4:]
                i = 0
                while i < len(args):
                    if args[i] == "--assignee" and i+1 < len(args):
                        assignee = args[i+1]; i += 2
                    elif args[i] == "--minutes" and i+1 < len(args):
                        minutes = int(args[i+1]); i += 2
                    elif args[i] == "--deadline" and i+1 < len(args):
                        deadline = args[i+1]; i += 2
                    elif args[i] == "--desc" and i+1 < len(args):
                        desc = args[i+1]; i += 2
                    else:
                        i += 1
                # V2: also parse --category
                category = None
                if "--category" in sys.argv:
                    idx = sys.argv.index("--category")
                    category = sys.argv[idx + 1]
                result = add_task(pid, title, desc, assignee, minutes, deadline)
                # Set category on the task if provided
                if category and result.get("task_id"):
                    db = get_db()
                    db.execute("UPDATE tasks SET category=? WHERE id=?", (category, result["task_id"]))
                    db.commit()
                    db.close()
                    result["category"] = category

        elif cmd == "start":
            if len(sys.argv) < 3:
                result = {"status": "error", "message": "Usage: start TASK_ID"}
            else:
                result = start_task(int(sys.argv[2]))

        elif cmd == "complete":
            manual_min = None
            if "--minutes" in sys.argv:
                idx = sys.argv.index("--minutes")
                manual_min = int(sys.argv[idx + 1])
            result = complete_task(int(sys.argv[2]), manual_minutes=manual_min)

        elif cmd == "skip":
            reason = None
            if "--reason" in sys.argv:
                idx = sys.argv.index("--reason")
                reason = sys.argv[idx + 1]
            result = skip_task(int(sys.argv[2]), reason)

        elif cmd == "pause":
            result = pause_task(int(sys.argv[2]))

        elif cmd == "resume":
            result = resume_task(int(sys.argv[2]))

        elif cmd == "review":
            pid = None
            if "--project" in sys.argv:
                idx = sys.argv.index("--project")
                pid = int(sys.argv[idx + 1])
            result = review(pid)

        elif cmd == "mood":
            result = record_mood(sys.argv[2])

        elif cmd == "status":
            result = overall_status()

        elif cmd == "ideas":
            show_all = "--all" in sys.argv
            result = list_ideas(show_all)

        elif cmd == "promote-idea":
            title = sys.argv[4] if len(sys.argv) > 4 else None
            result = promote_idea(int(sys.argv[2]), int(sys.argv[3]), title)

        elif cmd == "memory":
            result = list_memory()

        elif cmd == "remember":
            mtype = "context"
            tid = None
            if "--type" in sys.argv:
                idx = sys.argv.index("--type")
                mtype = sys.argv[idx + 1]
            if "--task" in sys.argv:
                idx = sys.argv.index("--task")
                tid = int(sys.argv[idx + 1])
            result = remember(sys.argv[2], mtype, tid)

        elif cmd == "log":
            days = 7
            if "--days" in sys.argv:
                idx = sys.argv.index("--days")
                days = int(sys.argv[idx + 1])
            result = get_action_log(days)

        elif cmd == "today-hours":
            if len(sys.argv) > 2:
                result = set_today_hours(float(sys.argv[2]))
            else:
                h = get_today_hours()
                result = {"available_hours": h}

        elif cmd == "list-goals":
            result = list_goals()

        elif cmd == "list-projects":
            gid = None
            if "--goal" in sys.argv:
                idx = sys.argv.index("--goal")
                gid = int(sys.argv[idx + 1])
            result = list_projects(gid)

        elif cmd == "time-stats":
            cat = None
            if "--category" in sys.argv:
                idx = sys.argv.index("--category")
                cat = sys.argv[idx + 1]
            result = get_time_stats(cat)

        elif cmd == "smart-estimate":
            if len(sys.argv) < 4:
                result = {"status": "error", "message": "Usage: smart-estimate CATEGORY MINUTES"}
            else:
                result = smart_estimate(sys.argv[2], int(sys.argv[3]))

        elif cmd == "connect-calendar":
            if len(sys.argv) < 4:
                result = {"status": "error", "message": "Usage: connect-calendar NAME 'URL_or_PATH' [--type ical_url|ical_file]"}
            else:
                cal_name = sys.argv[2]
                cal_source = sys.argv[3]
                cal_type = "ical_url"
                if "--type" in sys.argv:
                    idx = sys.argv.index("--type")
                    cal_type = sys.argv[idx + 1]
                result = connect_calendar(cal_name, cal_source, cal_type)

        elif cmd == "sync-calendar":
            cid = None
            if "--id" in sys.argv:
                idx = sys.argv.index("--id")
                cid = int(sys.argv[idx + 1])
            result = sync_calendar(cal_id=cid)

        elif cmd == "list-calendars":
            result = list_calendars()

        elif cmd == "disconnect-calendar":
            if len(sys.argv) < 3:
                result = {"status": "error", "message": "Usage: disconnect-calendar CALENDAR_ID"}
            else:
                result = disconnect_calendar(int(sys.argv[2]))

        elif cmd == "free-time":
            ws = "09:00"
            we = "18:00"
            if "--start" in sys.argv:
                idx = sys.argv.index("--start")
                ws = sys.argv[idx + 1]
            if "--end" in sys.argv:
                idx = sys.argv.index("--end")
                we = sys.argv[idx + 1]
            result = calculate_free_time(work_start=ws, work_end=we)

        elif cmd == "store-ltm":
            if len(sys.argv) < 3:
                result = {"status": "error", "message": "Usage: store-ltm 'content' [--type preference|constraint|insight|context]"}
            else:
                content = sys.argv[2]
                ltm_type = "context"
                if "--type" in sys.argv:
                    idx = sys.argv.index("--type")
                    ltm_type = sys.argv[idx + 1]
                result = store_long_term(content, content_type=ltm_type)

        elif cmd == "recall-ltm":
            if len(sys.argv) < 3:
                result = {"status": "error", "message": "Usage: recall-ltm 'query' [--n N] [--type T]"}
            else:
                query = sys.argv[2]
                n = 3
                if "--n" in sys.argv:
                    idx = sys.argv.index("--n")
                    n = int(sys.argv[idx + 1])
                ltm_type = None
                if "--type" in sys.argv:
                    idx = sys.argv.index("--type")
                    ltm_type = sys.argv[idx + 1]
                result = recall_relevant(query, n=n, content_type=ltm_type)

        elif cmd == "list-ltm":
            ltm_type = None
            if "--type" in sys.argv:
                idx = sys.argv.index("--type")
                ltm_type = sys.argv[idx + 1]
            result = list_long_term_memory(content_type=ltm_type)

        elif cmd == "clear-ltm":
            if len(sys.argv) < 3:
                result = {"status": "error", "message": "Usage: clear-ltm LTM_ID"}
            else:
                result = delete_long_term_memory(int(sys.argv[2]))

        elif cmd == "weight-stats":
            result = weight_stats()

        elif cmd == "learn-weights":
            result = learn_weights()

        elif cmd == "agent-status":
            result = get_agent_status()

        elif cmd == "agent-retry":
            if len(sys.argv) < 3:
                result = {"status": "error", "message": "Usage: agent-retry TASK_ID"}
            else:
                result = agent_retry(int(sys.argv[2]))

        elif cmd == "agent-handoff":
            if len(sys.argv) < 3:
                result = {"status": "error", "message": "Usage: agent-handoff TASK_ID"}
            else:
                result = agent_handoff(int(sys.argv[2]))

        else:
            result = {"status": "error", "message": f"Unknown command: {cmd}"}

        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))

    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
