#!/usr/bin/env python3
import argparse
import os
import sys
import uuid
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_jobs, save_jobs, load_stats, save_stats
from lib.schedule import compute_next_run

VALID_TYPES = ["daily", "weekly", "monthly", "interval"]

def parse_csv(value):
    if not value:
        return []
    return [v.strip() for v in value.split(",") if v.strip()]

def main():
    parser = argparse.ArgumentParser(description="Add a recurring cron job")
    parser.add_argument("--title", required=True)
    parser.add_argument("--schedule_type", choices=VALID_TYPES, required=True)
    parser.add_argument("--time_of_day", help="HH:MM for daily/weekly/monthly")
    parser.add_argument("--days_of_week", help="Comma-separated: mon,tue,fri")
    parser.add_argument("--day_of_month", type=int, help="1-31")
    parser.add_argument("--interval", type=int, help="Minutes for interval schedules")
    parser.add_argument("--timezone", default="Asia/Tokyo")
    parser.add_argument("--start_date")
    parser.add_argument("--end_date")
    parser.add_argument("--tags")
    parser.add_argument("--notes", default="")

    args = parser.parse_args()

    if args.schedule_type in ["daily", "weekly", "monthly"] and not args.time_of_day:
        parser.error("--time_of_day is required for daily/weekly/monthly")

    if args.schedule_type == "weekly" and not args.days_of_week:
        parser.error("--days_of_week is required for weekly")

    if args.schedule_type == "monthly" and not args.day_of_month:
        parser.error("--day_of_month is required for monthly")

    if args.schedule_type == "interval" and not args.interval:
        parser.error("--interval is required for interval")

    job_id = f"JOB-{str(uuid.uuid4())[:4].upper()}"
    now = datetime.now().isoformat()

    next_run = compute_next_run(
        schedule_type=args.schedule_type,
        time_of_day=args.time_of_day,
        days_of_week=parse_csv(args.days_of_week),
        day_of_month=args.day_of_month,
        interval=args.interval
    )

    job = {
        "id": job_id,
        "title": args.title,
        "status": "active",
        "schedule_type": args.schedule_type,
        "interval": args.interval,
        "time_of_day": args.time_of_day,
        "days_of_week": parse_csv(args.days_of_week),
        "day_of_month": args.day_of_month,
        "timezone": args.timezone,
        "start_date": args.start_date,
        "end_date": args.end_date,
        "last_run_at": None,
        "next_run_at": next_run.isoformat() if next_run else None,
        "missed_runs": 0,
        "notes": args.notes,
        "tags": parse_csv(args.tags),
        "created_at": now,
        "updated_at": now
    }

    data = load_jobs()
    data["jobs"][job_id] = job
    save_jobs(data)

    stats = load_stats()
    stats["total_jobs_created"] += 1
    save_stats(stats)

    print(f"✓ Job added: {job_id}")
    print(f"  Title: {args.title}")
    print(f"  Next run: {job['next_run_at']}")

if __name__ == "__main__":
    main()
