#!/usr/bin/env python3
"""BilimClass API — расписание, домашка, оценки"""

import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

try:
    import requests
except ImportError:
    print("Установи: pip install requests", file=sys.stderr)
    sys.exit(1)


def load_config():
    candidates = [
        Path.home() / ".openclaw" / ".env.json",
        Path("/mnt/c/Users/User/.openclaw/.env.json"),
        Path(os.environ.get("OPENCLAW_STATE_DIR", "")) / ".env.json" if os.environ.get("OPENCLAW_STATE_DIR") else None,
    ]
    for p in candidates:
        if p and p.exists():
            with open(p) as f:
                data = json.load(f)
            bc = data.get("bilimclass", {})
            if bc:
                return bc
    raise FileNotFoundError("bilimclass config not found in .env.json")


bc = load_config()

TOKEN = bc["token"]
JOURNAL_TOKEN = bc.get("journalToken", "")
SCHOOL_ID = bc["schoolId"]
EDU_YEAR = bc["eduYear"]
USER_ID = bc["userId"]
STUDENT_UUID = bc["studentSchoolUuid"]
STUDENT_GROUPS = bc.get("studentGroups", [])

API_BASE = "https://api.bilimclass.kz/api/v4/os/clientoffice"
JOURNAL_BASE = "https://journal-service.bilimclass.kz/diary"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "X-School-Id": SCHOOL_ID,
    "X-Localization": "ru",
    "Referer": "https://www.bilimclass.kz/2025/schedule",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0",
    "Accept": "application/json, text/plain, */*",
}

JOURNAL_HEADERS = {
    "Authorization": f"Bearer {JOURNAL_TOKEN}",
    "X-Localization": "ru",
    "X-School-Id": SCHOOL_ID,
    "external": "1",
    "Referer": "https://www.bilimclass.kz/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0",
    "Accept": "application/json",
}

SUBJECT_NAMES = {}  # populated from schedule


def get_schedule(date_str: str = None):
    if not date_str:
        date_str = datetime.now().strftime("%d.%m.%Y")
    params = {
        "schoolId": SCHOOL_ID, "eduYear": EDU_YEAR,
        "studentSchoolUuid": STUDENT_UUID, "date": date_str,
    }
    r = requests.get(f"{API_BASE}/schedule", params=params, headers=HEADERS, timeout=15)
    if r.status_code == 200:
        return r.json().get("data", {})
    return {"error": r.status_code, "body": r.text[:300]}


def get_week(date_str: str = None):
    if date_str:
        d = datetime.strptime(date_str, "%d.%m.%Y")
    else:
        d = datetime.now()
    monday = d - timedelta(days=d.weekday())
    sunday = monday + timedelta(days=6)
    all_days = []
    current = monday
    while current <= sunday:
        ds = current.strftime("%d.%m.%Y")
        data = get_schedule(ds)
        if "error" not in data:
            all_days.extend(data.get("days", []))
        current += timedelta(days=1)
    return {"days": all_days}


def get_diary(date_str: str = None):
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%dT00:00:00.000Z")
    elif len(date_str) == 10:
        date_str = f"{date_str}T00:00:00.000Z"
    results = []
    for group in STUDENT_GROUPS:
        params = {
            "schoolId": SCHOOL_ID, "eduYear": EDU_YEAR,
            "userId": USER_ID, "studentGroupUuid": group["uuid"], "date": date_str,
        }
        r = requests.get(JOURNAL_BASE, params=params, headers=JOURNAL_HEADERS, timeout=15)
        if r.status_code == 200:
            data = r.json()
            diary_data = data if isinstance(data, dict) else {}
            has_content = False
            for entry in diary_data.get("data", {}).values() if isinstance(diary_data, dict) else []:
                for mt in ["formattedScore", "sor", "soch"]:
                    if entry.get(mt, {}).get("mark") is not None:
                        has_content = True
            if has_content or diary_data.get("data"):
                results.append({"group": group["name"], "data": diary_data})
    return results


def get_grades(date_from: str, date_to: str):
    """Fetch all grades between dates (YYYY-MM-DD). Returns list of grade dicts."""
    if len(date_from) == 10:
        date_from = f"{date_from}T00:00:00.000Z"
    if len(date_to) == 10:
        date_to = f"{date_to}T00:00:00.000Z"
    start = datetime.strptime(date_from[:10], "%Y-%m-%d")
    end = datetime.strptime(date_to[:10], "%Y-%m-%d")
    all_grades = []
    current = start
    while current <= end:
        ds = current.strftime("%Y-%m-%dT00:00:00.000Z")
        for group in STUDENT_GROUPS:
            params = {
                "schoolId": SCHOOL_ID, "eduYear": EDU_YEAR,
                "userId": USER_ID, "studentGroupUuid": group["uuid"], "date": ds,
            }
            try:
                r = requests.get(JOURNAL_BASE, params=params, headers=JOURNAL_HEADERS, timeout=10)
                if r.status_code == 200:
                    diary_data = r.json().get("data", {})
                    if isinstance(diary_data, dict):
                        for entry in diary_data.values():
                            for mt in ["formattedScore", "sor", "soch"]:
                                mo = entry.get(mt)
                                if mo and mo.get("mark") is not None:
                                    all_grades.append({
                                        "subjectId": mo.get("subjectId"),
                                        "mark": mo["mark"],
                                        "max": mo.get("markMax", 10),
                                        "type": mt,
                                        "date": mo.get("date", ""),
                                    })
            except:
                pass
        current += timedelta(days=1)
    return all_grades


def aggregate_grades(grades):
    by_subj = defaultdict(list)
    for g in grades:
        by_subj[g["subjectId"]].append(g)
    return by_subj


def _load_subject_names():
    global SUBJECT_NAMES
    if SUBJECT_NAMES:
        return
    d = datetime.now()
    monday = d - timedelta(days=d.weekday())
    for i in range(7):
        ds = (monday + timedelta(days=i)).strftime("%d.%m.%Y")
        data = get_schedule(ds)
        if "error" not in data:
            for day in data.get("days", []):
                for lesson in day.get("schedule", []):
                    sid = lesson.get("subject", {}).get("subjectId")
                    label = lesson.get("subject", {}).get("label", "?")
                    if sid:
                        SUBJECT_NAMES[sid] = label


def format_grades_report(grades):
    """Return formatted string with per-subject grade summary."""
    by_subj = aggregate_grades(grades)
    _load_subject_names()
    lines = []
    for subj_id in sorted(by_subj.keys()):
        gs = by_subj[subj_id]
        name = SUBJECT_NAMES.get(subj_id, f"Предмет #{subj_id}")
        marks = [g["mark"] for g in gs]
        maxes = [g["max"] for g in gs]
        avg_m = sum(marks) / len(marks)
        avg_mx = sum(maxes) / len(maxes)
        pct = (avg_m / avg_mx * 100) if avg_mx > 0 else 0
        mn, mx = min(marks), max(marks)
        if pct >= 80:
            icon = "🟢"
        elif pct >= 58:
            icon = "🟡"
        else:
            icon = "🔴"
        lines.append(f"{icon} {name}: {avg_m:.1f}/{avg_mx:.1f} ({pct:.0f}%) — {len(marks)} оц. (мин.{mn}/макс.{mx})")
        lines.append(f"   Оценки: {marks}")
    return "\n".join(lines)


def format_day(day, include_time=True):
    lines = [f"\n📅 {day.get('date_label', '')}"]
    for lesson in day.get("schedule", []):
        subj = lesson.get("subject", {}).get("label", "???")
        time = lesson.get("time", {}).get("label", "")
        teacher = lesson.get("teacher", "")
        hw = lesson.get("homework", {}).get("body", "")
        time_str = f"🕐 {time} | " if time and include_time else ""
        lines.append(f"  {time_str}{subj}")
        if teacher:
            lines.append(f"     👨‍🏫 {teacher}")
        if hw and hw not in ["", "не предусмотренно", "не предусмотрено", "Не предусмотрено", None]:
            lines.append(f"     📝 {hw[:150]}")
    return "\n".join(lines)


USAGE = """BilimClass CLI
  schedule [DD.MM.YYYY]  — расписание на дату
  week [DD.MM.YYYY]      — расписание на неделю
  diary [YYYY-MM-DD]     — домашка на дату
  grades [от] [до]       — оценки (YYYY-MM-DD)
  quarter-report         — сводка по оценкам за последнюю четверть
  today                  — расписание на сегодня
  tomorrow               — расписание на завтра
  --raw                  — сырой JSON"""


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--raw"]
    raw = "--raw" in sys.argv
    cmd = args[0] if args else "help"

    if cmd == "schedule":
        data = get_schedule(args[1] if len(args) > 1 else None)
        if raw:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        elif "error" in data:
            print(f"❌ Ошибка: {data['error']} — {data['body'][:200]}")
        else:
            for day in data.get("days", []):
                print(format_day(day))

    elif cmd == "week":
        data = get_week(args[1] if len(args) > 1 else None)
        if raw:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        elif not data.get("days"):
            print("📭 Нет данных за эту неделю")
        else:
            for day in data["days"]:
                print(format_day(day))

    elif cmd == "diary":
        data = get_diary(args[1] if len(args) > 1 else None)
        if raw:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        elif not data:
            print("📭 Нет домашки на эту дату")
        else:
            for entry in data:
                print(f"\n📝 {entry['group']}")
                print(json.dumps(entry.get("data", {}), indent=2, ensure_ascii=False)[:500])

    elif cmd in ("grades", "quarter-report"):
        if cmd == "quarter-report":
            df = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")
            dt = datetime.now().strftime("%Y-%m-%d")
        elif len(args) >= 3:
            df, dt = args[1], args[2]
        elif len(args) == 2:
            df = args[1]
            dt = datetime.now().strftime("%Y-%m-%d")
        else:
            df = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            dt = datetime.now().strftime("%Y-%m-%d")
        grades = get_grades(df, dt)
        if raw:
            print(json.dumps(aggregate_grades(grades), indent=2, default=str, ensure_ascii=False))
        else:
            total = len(grades)
            print(f"📊 Оценки за {df} — {dt}: {total} оц.")
            if grades:
                print(format_grades_report(grades))
            else:
                print("📭 Нет оценок за этот период")

    elif cmd == "today":
        ds = datetime.now().strftime("%d.%m.%Y")
        data = get_schedule(ds)
        if raw:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        elif "error" in data:
            print(f"❌ Ошибка: {data['error']}")
        else:
            if not data.get("days"):
                print(f"📭 Нет уроков на {ds}")
            else:
                for day in data["days"]:
                    print(format_day(day))

    elif cmd == "tomorrow":
        ds = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
        data = get_schedule(ds)
        if raw:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        elif "error" in data:
            print(f"❌ Ошибка: {data['error']}")
        else:
            for day in data.get("days", []):
                print(format_day(day))

    elif cmd == "help":
        print(USAGE)

    else:
        print(f"Неизвестная команда: {cmd}")
