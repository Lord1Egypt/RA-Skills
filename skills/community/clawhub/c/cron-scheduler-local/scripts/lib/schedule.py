#!/usr/bin/env python3
from datetime import datetime, timedelta

WEEKDAY_MAP = {
    "mon": 0,
    "tue": 1,
    "wed": 2,
    "thu": 3,
    "fri": 4,
    "sat": 5,
    "sun": 6,
}

def parse_time_of_day(value):
    return datetime.strptime(value, "%H:%M").time()

def next_daily_run(time_of_day, now=None):
    now = now or datetime.now()
    t = parse_time_of_day(time_of_day)
    candidate = now.replace(hour=t.hour, minute=t.minute, second=0, microsecond=0)
    if candidate <= now:
        candidate += timedelta(days=1)
    return candidate

def next_weekly_run(days_of_week, time_of_day, now=None):
    now = now or datetime.now()
    t = parse_time_of_day(time_of_day)
    target_days = sorted(WEEKDAY_MAP[d.lower()] for d in days_of_week)
    for offset in range(0, 8):
        candidate_day = now + timedelta(days=offset)
        if candidate_day.weekday() in target_days:
            candidate = candidate_day.replace(hour=t.hour, minute=t.minute, second=0, microsecond=0)
            if candidate > now:
                return candidate
    return None

def next_monthly_run(day_of_month, time_of_day, now=None):
    now = now or datetime.now()
    t = parse_time_of_day(time_of_day)

    year = now.year
    month = now.month

    for _ in range(0, 2):
        try:
            candidate = datetime(year, month, day_of_month, t.hour, t.minute)
            if candidate > now:
                return candidate
        except ValueError:
            pass

        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
    return None

def next_interval_run(interval_minutes, now=None):
    now = now or datetime.now()
    return now + timedelta(minutes=interval_minutes)

def compute_next_run(schedule_type, time_of_day=None, days_of_week=None, day_of_month=None, interval=None):
    if schedule_type == "daily":
        return next_daily_run(time_of_day)
    if schedule_type == "weekly":
        return next_weekly_run(days_of_week or [], time_of_day)
    if schedule_type == "monthly":
        return next_monthly_run(day_of_month, time_of_day)
    if schedule_type == "interval":
        return next_interval_run(interval)
    raise ValueError(f"Unsupported schedule_type: {schedule_type}")
