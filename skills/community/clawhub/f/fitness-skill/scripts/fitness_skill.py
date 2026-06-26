#!/usr/bin/env python3
"""
Fitness Skill — core module for OpenClaw.

Manages fitness plans, workout logging (with live-session support),
and Feishu-integrated reminders.
Calls external APIs (feishu_api, workspace_io, scheduler) that are provided
by the OpenClaw runtime; this module does NOT re-implement them.
"""

import json
import os
import re
from datetime import datetime, date, timedelta
from typing import Any, Optional, List


# ---------------------------------------------------------------------------
# Data paths
# ---------------------------------------------------------------------------

_DATA_DIR = os.path.join(
    os.path.expanduser("~"), ".openclaw", "workspace", "fitness-skill"
)
PLAN_PATH = os.path.join(_DATA_DIR, "plan.json")
LOG_PATH = os.path.join(_DATA_DIR, "log.json")
SESSION_PATH = os.path.join(_DATA_DIR, "active_session.json")
EXPORT_DIR = os.path.join(_DATA_DIR, "exports")


def _ensure_data_dir():
    os.makedirs(_DATA_DIR, exist_ok=True)


def _ensure_export_dir():
    os.makedirs(EXPORT_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Low-level I/O helpers
# ---------------------------------------------------------------------------

def _read_json(path: str) -> Optional[dict]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def _write_json(path: str, data: dict):
    _ensure_data_dir()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _parse_date(s: str) -> Optional[date]:
    try:
        return date.fromisoformat(s)
    except (ValueError, TypeError):
        return None


def _parse_utc(s: str) -> datetime:
    """Parse an ISO timestamp (with trailing Z) into a timezone-aware datetime."""
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


# ---------------------------------------------------------------------------
# NLP helpers
# ---------------------------------------------------------------------------

_TYPE_MAP = {
    "tennis": "tennis", "网球": "tennis",
    "gym": "gym", "健身": "gym", "力量": "gym",
    "run": "cardio", "跑步": "cardio", "cardio": "cardio",
    "swim": "swim", "游泳": "swim",
    "yoga": "yoga", "瑜伽": "yoga",
    "bench": "gym", "squat": "gym", "deadlift": "gym",
}

_FEELING_MAP = {
    "exhausted": "exhausted", "累": "exhausted", "疲": "exhausted",
    "great": "great", "好": "great", "棒": "great",
    "sore": "sore", "酸": "sore",
    "easy": "easy", "轻松": "easy",
    "tired": "tired",
}

_FATIGUE_WORDS = {"exhausted", "tired", "sore", "累", "疲", "酸"}


def _detect_type(text: str) -> str:
    lower = text.lower()
    for kw, sport in _TYPE_MAP.items():
        if kw in lower:
            return sport
    return "other"


def _detect_feeling(text: str) -> str:
    lower = text.lower()
    for kw, feel in _FEELING_MAP.items():
        if kw in lower:
            return feel
    return ""


def _extract_duration(text: str) -> int:
    lower = text.lower()
    for pat in [r"(\d+(?:\.\d+)?)\s*(?:hours?|小时|hrs?)",
                r"(\d+)\s*(?:minutes?|分钟|mins?)"]:
        m = re.search(pat, lower)
        if m:
            val = float(m.group(1))
            if "hour" in pat or "小时" in pat:
                val *= 60
            return int(val)
    return 0


def _extract_exercises(text: str) -> list:
    exercises = []
    for m in re.finditer(
        r"([\w\s]+?)\s+(\d+)\s*kg\s*[x×]\s*(\d+)\s*[x×]\s*(\d+)",
        text.lower()
    ):
        exercises.append({
            "name": m.group(1).strip().title(),
            "weight_kg": int(m.group(2)),
            "reps": int(m.group(3)),
            "sets": int(m.group(4)),
        })
    return exercises


def _recovery_advice(feeling: str, duration_min: int) -> str:
    if feeling in ("exhausted", "sore", "tired"):
        return (
            "Take it easy next session. Focus on hydration, protein intake, "
            "and 7-8 hours of sleep. Light stretching recommended."
        )
    if duration_min > 120:
        return "Long session detected. Ensure adequate rest before next workout."
    return ""


def parse_workout_text(text: str) -> dict:
    """Extract structured data from natural language workout feedback."""
    exercises = _extract_exercises(text)
    feeling = _detect_feeling(text)
    duration = _extract_duration(text)
    sport = _detect_type(text)
    return {
        "date": date.today().isoformat(),
        "type": sport,
        "duration_min": duration,
        "exercises": exercises,
        "feeling": feeling,
        "notes": text,
        "recovery_advice": _recovery_advice(feeling, duration),
    }


# ---------------------------------------------------------------------------
# FitnessSkill class
# ---------------------------------------------------------------------------

class FitnessSkill:
    """Orchestrates plan creation, workout logging, and scheduling."""

    def __init__(self, feishu_doc_id: str = ""):
        self.feishu_doc_id = feishu_doc_id or os.getenv("FEISHU_FITNESS_DOC_ID", "")
        self.plan: Optional[dict] = _read_json(PLAN_PATH)
        self.log: dict = _read_json(LOG_PATH) or {"version": "1.0", "entries": []}

    # =====================================================================
    # Plan management
    # =====================================================================

    def has_plan(self) -> bool:
        return self.plan is not None and len(self.plan.get("weekly_schedule", [])) > 0

    def create_plan(self, profile: dict) -> dict:
        freq = max(1, min(int(profile.get("frequency", 3)), 7))
        prefs = profile.get("sport_pref", ["gym"])
        level = profile.get("level", "beginner")
        days = ["Monday", "Tuesday", "Wednesday", "Thursday",
                "Friday", "Saturday", "Sunday"]
        schedule = [
            self._generate_day(prefs[i % len(prefs)], level, days[i % 7])
            for i in range(freq)
        ]
        now = datetime.utcnow().isoformat(timespec="seconds") + "Z"
        self.plan = {
            "version": "1.0",
            "user_profile": {
                "goals": profile.get("goals", []),
                "sport_pref": prefs,
                "frequency": freq,
                "level": level,
                "constraints": profile.get("constraints", ""),
                "reminder_time": profile.get("reminder_time", "08:00"),
            },
            "weekly_schedule": schedule,
            "created_at": now,
            "updated_at": now,
        }
        self._save_plan()
        return self.plan

    def update_plan(self, changes: dict) -> dict:
        if not self.plan:
            raise ValueError("No plan exists. Run create_plan first.")
        prof = self.plan["user_profile"]
        for k in ("goals", "sport_pref", "frequency", "level",
                   "constraints", "reminder_time"):
            if k in changes:
                prof[k] = changes[k]
        if any(k in changes for k in ("frequency", "sport_pref", "level")):
            days = ["Monday", "Tuesday", "Wednesday", "Thursday",
                    "Friday", "Saturday", "Sunday"]
            self.plan["weekly_schedule"] = [
                self._generate_day(prof["sport_pref"][i % len(prof["sport_pref"])],
                                   prof["level"], days[i % 7])
                for i in range(prof["frequency"])
            ]
        self.plan["updated_at"] = datetime.utcnow().isoformat(timespec="seconds") + "Z"
        self._save_plan()
        return self.plan

    def plan_to_markdown(self) -> str:
        if not self.plan:
            return "_No fitness plan found. Run `fitness-plan init` to create one._"
        prof = self.plan["user_profile"]
        lines = [
            "# Fitness Plan", "",
            f"**Goals:** {', '.join(prof.get('goals', []))}",
            f"**Preference:** {', '.join(prof.get('sport_pref', []))}",
            f"**Frequency:** {prof.get('frequency', '?')}x / week",
            f"**Level:** {prof.get('level', '?')}",
            f"**Reminder:** {prof.get('reminder_time', 'N/A')}", "",
        ]
        for dp in self.plan.get("weekly_schedule", []):
            lines.append(f"## {dp['day']} — {dp['type'].title()}")
            lines.append(f"Duration: ~{dp.get('duration_min', '?')} min\n")
            for ex in dp.get("exercises", []):
                detail = ""
                if ex.get("sets"):
                    detail += f"{ex['sets']}x{ex.get('reps', '?')}"
                if ex.get("weight_kg"):
                    detail += f" @ {ex['weight_kg']}kg"
                if ex.get("duration_min"):
                    detail += f" {ex['duration_min']} min"
                lines.append(f"- {ex['name']}  {detail}")
            lines.append("")
        return "\n".join(lines)

    # =====================================================================
    # Session management (live workout tracking)
    # =====================================================================

    SESSION_HARD_TIMEOUT_MIN = 240   # 4 hours
    SESSION_IDLE_WARN_MIN = 30       # 30 min since last message → Claw should ask

    def session_start(self, sport_type: str = "") -> dict:
        """Begin a new live workout session.
        If a stale session exists, auto-closes it first."""
        stale = self._check_and_close_stale_session()
        if not stale and self._has_active_session():
            raise ValueError(
                "A session is already active. End it first with `fitness-log end`."
            )
        session = {
            "started_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "date": date.today().isoformat(),
            "type": sport_type or "other",
            "exercises": [],
            "messages": [],
            "feeling": "",
        }
        _write_json(SESSION_PATH, session)
        return session

    def session_append(self, raw_text: str) -> dict:
        """Add an exercise/note to the active session.
        Auto-closes stale sessions before appending."""
        stale = self._check_and_close_stale_session()
        if stale:
            raise ValueError(
                f"Previous session was stale and auto-closed "
                f"({stale['duration_min']} min, {len(stale['exercises'])} exercises). "
                f"Start a new session with `fitness-log start`."
            )

        session = self._load_active_session()
        if not session:
            raise ValueError("No active session. Start one with `fitness-log start`.")

        parsed = parse_workout_text(raw_text)

        if parsed["exercises"]:
            session["exercises"].extend(parsed["exercises"])
        if parsed["feeling"]:
            session["feeling"] = parsed["feeling"]
        if parsed["type"] != "other" and session["type"] == "other":
            session["type"] = parsed["type"]

        session["messages"].append({
            "time": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "text": raw_text,
        })
        _write_json(SESSION_PATH, session)
        return {
            "added_exercises": parsed["exercises"],
            "feeling": parsed["feeling"],
            "total_exercises": len(session["exercises"]),
            "session_type": session["type"],
        }

    def session_end(self, final_text: str = "") -> dict:
        """Finalize the active session and commit to log."""
        session = self._load_active_session()
        if not session:
            raise ValueError("No active session to end.")
        return self._commit_session(session, final_text)

    def session_status(self) -> Optional[dict]:
        """Return the active session info, or None."""
        session = self._load_active_session()
        if not session:
            return None
        started = _parse_utc(session["started_at"])
        now = datetime.utcnow().replace(tzinfo=started.tzinfo)
        elapsed = int((now - started).total_seconds() / 60)

        last_msg_time = None
        idle_min = 0
        if session.get("messages"):
            last_msg_time = _parse_utc(session["messages"][-1]["time"])
            idle_min = int((now - last_msg_time).total_seconds() / 60)
        else:
            idle_min = elapsed

        is_stale = (elapsed >= self.SESSION_HARD_TIMEOUT_MIN or
                    session.get("date") != date.today().isoformat())

        return {
            "active": True,
            "type": session["type"],
            "elapsed_min": elapsed,
            "idle_min": idle_min,
            "exercises_logged": len(session["exercises"]),
            "messages": len(session.get("messages", [])),
            "feeling": session.get("feeling", ""),
            "stale": is_stale,
            "should_ask": idle_min >= self.SESSION_IDLE_WARN_MIN and not is_stale,
        }

    def _commit_session(self, session: dict, final_text: str = "") -> dict:
        """Internal: finalize a session dict into a log entry."""
        if final_text:
            parsed = parse_workout_text(final_text)
            if parsed["exercises"]:
                session["exercises"].extend(parsed["exercises"])
            if parsed["feeling"]:
                session["feeling"] = parsed["feeling"]
            if parsed["duration_min"]:
                session["duration_min_override"] = parsed["duration_min"]

        started = _parse_utc(session["started_at"])

        # For stale sessions, use last message time instead of now
        if session.get("messages"):
            last_msg = _parse_utc(session["messages"][-1]["time"])
        else:
            last_msg = started
        ended = min(datetime.utcnow().replace(tzinfo=started.tzinfo), last_msg)

        auto_duration = max(0, int((ended - started).total_seconds() / 60))
        duration = session.get("duration_min_override", auto_duration)

        all_notes = " | ".join(m["text"] for m in session.get("messages", []))
        if final_text:
            all_notes += f" | {final_text}"

        entry = {
            "date": session["date"],
            "type": session["type"],
            "duration_min": duration,
            "exercises": session["exercises"],
            "feeling": session.get("feeling", ""),
            "notes": all_notes,
            "recovery_advice": _recovery_advice(
                session.get("feeling", ""), duration
            ),
            "session_meta": {
                "started_at": session["started_at"],
                "ended_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
                "message_count": len(session.get("messages", [])),
                "auto_closed": False,
            },
        }
        self.log["entries"].append(entry)
        self._save_log()
        self._clear_active_session()
        return entry

    def _check_and_close_stale_session(self) -> Optional[dict]:
        """If an active session is stale (>4h or different day), auto-close it.
        Returns the committed entry if closed, None otherwise."""
        session = self._load_active_session()
        if not session:
            return None

        started = _parse_utc(session["started_at"])
        now = datetime.utcnow().replace(tzinfo=started.tzinfo)
        elapsed = int((now - started).total_seconds() / 60)
        different_day = session.get("date") != date.today().isoformat()

        if elapsed < self.SESSION_HARD_TIMEOUT_MIN and not different_day:
            return None

        entry = self._commit_session(session)
        entry["session_meta"]["auto_closed"] = True
        self._save_log()
        return entry

    def _has_active_session(self) -> bool:
        return os.path.exists(SESSION_PATH) and _read_json(SESSION_PATH) is not None

    def _load_active_session(self) -> Optional[dict]:
        return _read_json(SESSION_PATH)

    def _clear_active_session(self):
        try:
            os.remove(SESSION_PATH)
        except FileNotFoundError:
            pass

    # =====================================================================
    # Workout logging (one-shot, unchanged)
    # =====================================================================

    def log_workout(self, raw_text: str) -> dict:
        entry = parse_workout_text(raw_text)
        self.log["entries"].append(entry)
        self._save_log()
        return entry

    # =====================================================================
    # Querying & statistics
    # =====================================================================

    def get_recent_entries(self, n: int = 7) -> list:
        return self.log["entries"][-n:]

    def get_entries_by_days(self, days: int = 30) -> list:
        """Return entries from the last N days."""
        cutoff = date.today() - timedelta(days=days)
        return [
            e for e in self.log["entries"]
            if _parse_date(e.get("date", "")) and _parse_date(e["date"]) >= cutoff
        ]

    def weekly_summary(self) -> dict:
        return self._period_summary(7)

    def monthly_summary(self) -> dict:
        return self._period_summary(30)

    def _period_summary(self, days: int) -> dict:
        entries = self.get_entries_by_days(days)
        total_min = sum(e.get("duration_min", 0) for e in entries)
        types: dict = {}
        for e in entries:
            t = e.get("type", "other")
            types[t] = types.get(t, 0) + 1

        needs_recovery = any(
            any(w in e.get("feeling", "").lower() for w in _FATIGUE_WORDS)
            for e in entries[-2:]
        )
        advice = ""
        if needs_recovery:
            advice = ("Recent sessions show signs of fatigue. "
                      "Consider a lighter session or active recovery.")

        label = "week" if days <= 7 else f"{days} days"
        return {
            "period": label,
            "sessions": len(entries),
            "total_minutes": total_min,
            "avg_minutes_per_session": round(total_min / len(entries)) if entries else 0,
            "type_breakdown": types,
            "recovery_advice": advice,
        }

    # =====================================================================
    # Export
    # =====================================================================

    def export_log_markdown(self, days: int = 30, max_entries: int = 50) -> str:
        """Render recent log entries as a Markdown report."""
        entries = self.get_entries_by_days(days)
        if not entries:
            return "_No workout entries in the selected period._"

        if len(entries) > max_entries:
            entries = entries[-max_entries:]

        summary = self._period_summary(days)
        lines = [
            f"# Fitness Log — Last {days} Days",
            f"_Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}_\n",
            f"**Sessions:** {summary['sessions']}  |  "
            f"**Total:** {summary['total_minutes']} min  |  "
            f"**Avg:** {summary['avg_minutes_per_session']} min/session\n",
        ]
        if summary["type_breakdown"]:
            bd = ", ".join(f"{k}: {v}" for k, v in summary["type_breakdown"].items())
            lines.append(f"**Breakdown:** {bd}\n")
        if summary["recovery_advice"]:
            lines.append(f"> {summary['recovery_advice']}\n")

        lines.append("---\n")

        current_date = ""
        for e in entries:
            if e["date"] != current_date:
                current_date = e["date"]
                lines.append(f"## {current_date}\n")
            ex_str = ""
            if e.get("exercises"):
                parts = []
                for x in e["exercises"]:
                    p = x["name"]
                    if x.get("weight_kg"):
                        p += f" {x['weight_kg']}kg"
                    if x.get("sets") and x.get("reps"):
                        p += f" {x['sets']}x{x['reps']}"
                    parts.append(p)
                ex_str = " — " + ", ".join(parts)
            feel = f"  [{e['feeling']}]" if e.get("feeling") else ""
            dur = f"{e.get('duration_min', 0)} min" if e.get("duration_min") else ""
            lines.append(f"- **{e.get('type', 'other').title()}** {dur}{ex_str}{feel}")
            if e.get("recovery_advice"):
                lines.append(f"  > {e['recovery_advice']}")
            lines.append("")

        return "\n".join(lines)

    def export_to_file(self, days: int = 30, max_entries: int = 50) -> str:
        """Write the Markdown report to a file and return the path."""
        _ensure_export_dir()
        md = self.export_log_markdown(days, max_entries)
        fname = f"fitness-log-{date.today().isoformat()}.md"
        path = os.path.join(EXPORT_DIR, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(md)
        return path

    # =====================================================================
    # Feishu sync
    # =====================================================================

    def sync_plan_to_feishu(self, feishu_api: Any = None):
        if not self.feishu_doc_id or feishu_api is None:
            return
        try:
            feishu_api.write_doc(self.feishu_doc_id, self.plan_to_markdown())
        except Exception as exc:
            print(f"[fitness-skill] Feishu plan sync failed: {exc}")

    def sync_log_to_feishu(self, feishu_api: Any = None,
                           days: int = 30, max_entries: int = 50):
        """Write the log Markdown report to the Feishu doc."""
        if not self.feishu_doc_id or feishu_api is None:
            return
        md = self.export_log_markdown(days, max_entries)
        try:
            feishu_api.write_doc(self.feishu_doc_id, md)
        except Exception as exc:
            print(f"[fitness-skill] Feishu log sync failed: {exc}")

    # backward compat alias
    sync_to_feishu = sync_plan_to_feishu

    # =====================================================================
    # Scheduling
    # =====================================================================

    def setup_reminder(self, scheduler: Any = None, feishu_api: Any = None):
        if scheduler is None or feishu_api is None or not self.plan:
            return None
        reminder_time = self.plan["user_profile"].get("reminder_time", "08:00")
        h, m = reminder_time.split(":")
        cron_expr = f"{m} {h} * * *"
        today_name = datetime.utcnow().strftime("%A")

        def _reminder_callback():
            sched = self.plan.get("weekly_schedule", [])
            today_plan = next((d for d in sched if d["day"] == today_name), None)
            if today_plan:
                exercises = ", ".join(e["name"] for e in today_plan.get("exercises", []))
                msg = (f"Today's workout: {today_plan['type'].title()} "
                       f"({today_plan.get('duration_min', '?')} min)\n{exercises}")
            else:
                msg = "Rest day — stretch or take a walk!"
            try:
                feishu_api.send_message(msg)
            except Exception as exc:
                print(f"[fitness-skill] Reminder send failed: {exc}")

        return scheduler.add_cron_job(cron_expr, _reminder_callback)

    # =====================================================================
    # Internals
    # =====================================================================

    def _save_plan(self):
        _write_json(PLAN_PATH, self.plan)

    def _save_log(self):
        _write_json(LOG_PATH, self.log)

    @staticmethod
    def _generate_day(sport: str, level: str, day: str) -> dict:
        templates = {
            "gym": {
                "beginner": [
                    {"name": "Bench Press", "sets": 3, "reps": 10, "weight_kg": 0},
                    {"name": "Squat", "sets": 3, "reps": 10, "weight_kg": 0},
                    {"name": "Lat Pulldown", "sets": 3, "reps": 10, "weight_kg": 0},
                    {"name": "Plank", "sets": 3, "reps": 1, "duration_min": 1},
                ],
                "intermediate": [
                    {"name": "Bench Press", "sets": 4, "reps": 8, "weight_kg": 0},
                    {"name": "Squat", "sets": 4, "reps": 8, "weight_kg": 0},
                    {"name": "Deadlift", "sets": 3, "reps": 6, "weight_kg": 0},
                    {"name": "Overhead Press", "sets": 3, "reps": 8, "weight_kg": 0},
                    {"name": "Barbell Row", "sets": 3, "reps": 8, "weight_kg": 0},
                ],
                "advanced": [
                    {"name": "Bench Press", "sets": 5, "reps": 5, "weight_kg": 0},
                    {"name": "Squat", "sets": 5, "reps": 5, "weight_kg": 0},
                    {"name": "Deadlift", "sets": 5, "reps": 3, "weight_kg": 0},
                    {"name": "Weighted Pull-ups", "sets": 4, "reps": 6, "weight_kg": 0},
                    {"name": "Overhead Press", "sets": 4, "reps": 6, "weight_kg": 0},
                    {"name": "Barbell Row", "sets": 4, "reps": 6, "weight_kg": 0},
                ],
            },
            "tennis": {
                "beginner": [
                    {"name": "Rally practice", "duration_min": 30},
                    {"name": "Serve practice", "duration_min": 15},
                    {"name": "Footwork drills", "duration_min": 15},
                ],
                "intermediate": [
                    {"name": "Match play", "duration_min": 45},
                    {"name": "Serve & return drill", "duration_min": 20},
                    {"name": "Net volley practice", "duration_min": 15},
                    {"name": "Conditioning sprints", "duration_min": 10},
                ],
                "advanced": [
                    {"name": "Match play", "duration_min": 60},
                    {"name": "Tactical serve placement", "duration_min": 20},
                    {"name": "Approach shot drills", "duration_min": 15},
                    {"name": "Agility & footwork", "duration_min": 15},
                ],
            },
            "cardio": {
                "beginner": [
                    {"name": "Brisk Walk", "duration_min": 30},
                    {"name": "Stretching", "duration_min": 10},
                ],
                "intermediate": [
                    {"name": "Running", "duration_min": 30},
                    {"name": "Jump Rope", "duration_min": 10},
                    {"name": "Stretching", "duration_min": 10},
                ],
                "advanced": [
                    {"name": "Interval Running", "duration_min": 40},
                    {"name": "Burpees", "sets": 4, "reps": 15},
                    {"name": "Box Jumps", "sets": 4, "reps": 12},
                ],
            },
        }
        sport_lower = sport.lower() if sport.lower() in templates else "gym"
        exercises = templates[sport_lower].get(level, templates[sport_lower]["beginner"])
        total_min = sum(e.get("duration_min", 0) for e in exercises)
        if total_min == 0:
            total_min = len(exercises) * 10
        return {
            "day": day, "type": sport_lower,
            "exercises": [dict(e) for e in exercises],
            "duration_min": total_min,
        }
