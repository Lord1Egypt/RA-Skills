"""Main periodic task manager using the new core modules."""
import sys
import argparse
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_DIR))

import subprocess
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo
from typing import Optional

from core.db import DB, db_commit, clear_task_cache, get_periodic_tasks, get_periodic_task
from core.scheduler import TaskScheduler, to_shanghai_date
from core.learning import LearningContext
from core.models import PeriodicTask, ALLOWED_CYCLE_TYPES
from core.config import get_chat_id
from core.openclaw_cron import build_cron_add_command, build_cron_remove_command

CYCLE_TYPES = list(ALLOWED_CYCLE_TYPES)
SHANGHAI_TZ = ZoneInfo('Asia/Shanghai')


def parse_time_of_day(value: str) -> str:
    import re
    match = re.fullmatch(r'(\d{1,2}):(\d{2})', value.strip())
    if not match:
        raise argparse.ArgumentTypeError("time must be HH:MM")
    hour = int(match.group(1))
    minute = int(match.group(2))
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        raise argparse.ArgumentTypeError("time must be HH:MM (00:00-23:59)")
    return f"{hour:02d}:{minute:02d}"


def validate_add_params(args: argparse.Namespace) -> None:
    if args.weekday is not None and (args.weekday < 0 or args.weekday > 6):
        raise ValueError("weekday must be 0-6 (Mon=0)")
    if args.day_of_month is not None and (args.day_of_month < 1 or args.day_of_month > 31):
        raise ValueError("day must be 1-31")
    if args.range_start is not None and (args.range_start < 1 or args.range_start > 31):
        raise ValueError("range-start must be 1-31")
    if args.range_end is not None and (args.range_end < 1 or args.range_end > 31):
        raise ValueError("range-end must be 1-31")
    if args.n_per_month is not None and args.n_per_month <= 0:
        raise ValueError("n-per-month must be > 0")
    if args.interval_hours is not None and (args.interval_hours <= 0 or args.interval_hours > 24):
        raise ValueError("interval-hours must be 1-24")
    if args.end_date:
        try:
            date.fromisoformat(args.end_date)
        except ValueError as exc:
            raise ValueError("end-date must be YYYY-MM-DD") from exc
    if args.start_date:
        try:
            date.fromisoformat(args.start_date)
        except ValueError as exc:
            raise ValueError("start-date must be YYYY-MM-DD") from exc
    if args.dates_list:
        cleaned = [chunk.strip() for chunk in args.dates_list.split(',') if chunk.strip()]
        if not cleaned:
            raise ValueError("monthly_dates tasks require --dates-list")
        parsed_days = []
        for chunk in cleaned:
            try:
                day = int(chunk)
            except ValueError as exc:
                raise ValueError("dates-list must contain comma-separated day numbers") from exc
            if day < 1 or day > 31:
                raise ValueError("dates-list day must be 1-31")
            parsed_days.append(day)
        args.dates_list = ','.join(str(day) for day in sorted(set(parsed_days)))

    if args.cycle_type == 'once' and not args.start_date:
        raise ValueError("scheduled once tasks require --start-date YYYY-MM-DD")
    if args.cycle_type == 'hourly' and args.interval_hours is None:
        args.interval_hours = 1
    if args.cycle_type == 'weekly' and args.weekday is None:
        raise ValueError("weekly tasks require --weekday")
    if args.cycle_type == 'monthly_fixed' and args.day_of_month is None:
        raise ValueError("monthly_fixed tasks require --day")
    if args.cycle_type == 'monthly_range' and (args.range_start is None or args.range_end is None):
        raise ValueError("monthly_range tasks require --range-start and --range-end")
    if args.cycle_type == 'monthly_n_times' and args.n_per_month is None:
        raise ValueError("monthly_n_times tasks require --n-per-month")
    if args.cycle_type == 'monthly_dates' and not args.dates_list:
        raise ValueError("monthly_dates tasks require --dates-list")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Chronos periodic task manager")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--add", action="store_true", help="Add a periodic task")
    group.add_argument("--complete-activity", type=int, help="Complete activity by task id")
    group.add_argument("--ensure-today", action="store_true", help="Ensure today's occurrences")

    parser.add_argument("--name")
    parser.add_argument("--category", default="Inbox")
    parser.add_argument("--cycle-type", default="once", choices=CYCLE_TYPES)
    parser.add_argument("--time", dest="time_of_day", type=parse_time_of_day, default="09:00")
    parser.add_argument("--weekday", type=int)
    parser.add_argument("--day", dest="day_of_month", type=int)
    parser.add_argument("--range-start", type=int)
    parser.add_argument("--range-end", type=int)
    parser.add_argument("--n-per-month", type=int)
    parser.add_argument("--interval-hours", type=int)
    parser.add_argument("--dates-list")
    parser.add_argument("--start-date")
    parser.add_argument("--end-date")
    parser.add_argument("--reminder-template")
    parser.add_argument("--task-kind", default="scheduled")
    parser.add_argument("--source", default="chronos")
    parser.add_argument("--legacy-entry-id", type=int)
    parser.add_argument("--special-handler")
    parser.add_argument("--handler-payload")
    parser.add_argument("--delivery-target")
    parser.add_argument("--delivery-mode")

    return parser


class PeriodicTaskManager:
    """Manages periodic tasks: scheduling, completion, cleanup."""

    def __init__(self):
        self.db = DB()

    def add_activity(self, **params) -> int:
        """Add a new periodic task."""
        with LearningContext("add_activity", f"Add task: {params.get('name')} ({params.get('cycle_type')})", confidence="H"):
            cur = self.db.execute(
                """
                INSERT INTO periodic_tasks
                (name, category, cycle_type, weekday, day_of_month, range_start, range_end, n_per_month,
                 interval_hours, time_of_day, event_time, timezone, is_active, count_current_month, end_date, reminder_template,
                 dates_list, task_kind, source, legacy_entry_id, special_handler, handler_payload, start_date,
                 delivery_target, delivery_mode, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Asia/Shanghai', 1, 0, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """,
                (
                    params.get('name'),
                    params.get('category', 'Inbox'),
                    params.get('cycle_type', 'once'),
                    params.get('weekday'),
                    params.get('day_of_month'),
                    params.get('range_start'),
                    params.get('range_end'),
                    params.get('n_per_month'),
                    params.get('interval_hours'),
                    params.get('time_of_day', '09:00'),
                    params.get('time_of_day', '09:00'),
                    params.get('end_date'),
                    params.get('reminder_template'),
                    params.get('dates_list'),
                    params.get('task_kind', 'scheduled'),
                    params.get('source', 'chronos'),
                    params.get('legacy_entry_id'),
                    params.get('special_handler'),
                    params.get('handler_payload'),
                    params.get('start_date'),
                    params.get('delivery_target'),
                    params.get('delivery_mode'),
                ),
            )
            db_commit()
            clear_task_cache()
            activity_id = cur.lastrowid
            return activity_id

    def reset_monthly_counters(self, today: date):
        if today.day == 1:
            with LearningContext("reset_monthly_counters", f"Reset monthly counters for {today.strftime('%Y-%m')}", confidence="H"):
                self.db.execute(
                    """
                    UPDATE periodic_tasks
                    SET count_current_month = 0
                    WHERE cycle_type = 'monthly_n_times' AND is_active = 1
                    """
                )
                db_commit()
                clear_task_cache()

    def create_occurrence_if_missing(self, task_id: int, occ_date: date, scheduled_time: str | None = None) -> int:
        task = get_periodic_task(task_id)
        scheduled_time = scheduled_time or (task.get('time_of_day') if task else None)
        scheduled_at = None
        if scheduled_time:
            scheduled_at = f"{occ_date.isoformat()}T{scheduled_time}:00"
        self.db.execute(
            """
            INSERT OR IGNORE INTO periodic_occurrences (task_id, date, status, scheduled_time, scheduled_at)
            VALUES (?, ?, 'pending', ?, ?)
            """,
            (task_id, occ_date.isoformat(), scheduled_time, scheduled_at),
        )
        db_commit()
        cur = self.db.execute(
            "SELECT id FROM periodic_occurrences WHERE task_id = ? AND date = ? AND COALESCE(scheduled_time, '') = COALESCE(?, '')",
            (task_id, occ_date.isoformat(), scheduled_time),
        )
        row = cur.fetchone()
        if row:
            return row[0]
        cur = self.db.execute("SELECT id FROM periodic_occurrences WHERE task_id = ? AND date = ?", (task_id, occ_date.isoformat()))
        row = cur.fetchone()
        return row[0] if row else None

    def schedule_reminder_cron(self, task_id: int, occ_date: date, time_of_day: str) -> Optional[str]:
        cur = self.db.execute(
            "SELECT name, reminder_template FROM periodic_tasks WHERE id = ?",
            (task_id,),
        )
        row = cur.fetchone()
        if not row:
            return None
        task_name, reminder_template = row[0], row[1]

        try:
            chat_id = get_chat_id()
        except ValueError as exc:
            print(f"Chronos chat_id not configured: {exc}")
            return None

        hour, minute = map(int, time_of_day.split(':'))
        reminder_minute = minute - 5
        reminder_hour = hour
        reminder_date = occ_date

        if reminder_minute < 0:
            reminder_minute += 60
            reminder_hour -= 1
            if reminder_hour < 0:
                reminder_hour += 24
                reminder_date = occ_date - timedelta(days=1)

        dt_shanghai = datetime(reminder_date.year, reminder_date.month, reminder_date.day, reminder_hour, reminder_minute, tzinfo=SHANGHAI_TZ)
        utc_dt = dt_shanghai.astimezone(ZoneInfo('UTC'))

        now_utc = datetime.now(ZoneInfo('UTC'))
        if utc_dt <= now_utc:
            message_text = self._format_reminder_message(task_name, occ_date, time_of_day, reminder_template, immediate=True)
            immediate_job_name = f"reminder_immediate_{task_id}_{occ_date.strftime('%Y%m%d')}_{time_of_day.replace(':', '')}"
            try:
                subprocess.run(
                    build_cron_add_command(
                        job_name=immediate_job_name,
                        at_iso=now_utc.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        message=message_text,
                        chat_id=chat_id,
                    ),
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
            except (OSError, subprocess.SubprocessError) as e:
                print(f"Failed to send immediate reminder: {e}")
            return None

        iso_time = utc_dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        try:
            task_row = get_periodic_task(task_id) or {}
        except Exception:
            task_row = {}
        cycle_type = task_row.get('cycle_type')
        interval_hours = task_row.get('interval_hours')
        if cycle_type == 'hourly' and interval_hours not in (None, 24):
            job_name = f"task_reminder_{task_id}_{occ_date.strftime('%Y%m%d')}_{time_of_day.replace(':', '')}"
        else:
            job_name = f"task_reminder_{task_id}_{occ_date.strftime('%Y%m%d')}"
        message_text = self._format_reminder_message(task_name, occ_date, time_of_day, reminder_template, immediate=False)

        cmd = build_cron_add_command(job_name=job_name, at_iso=iso_time, message=message_text, chat_id=chat_id)
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        except (OSError, subprocess.SubprocessError) as e:
            print(f"Failed to schedule cron: {e}")
            return None
        if result.returncode == 0:
            return job_name
        print(f"Failed to schedule cron: {result.stderr}")
        return None

    def generate_reminders_for_today(self) -> int:
        today = to_shanghai_date()
        self.reset_monthly_counters(today)

        scheduled = 0
        tasks = get_periodic_tasks(active_only=True)

        for task_dict in tasks:
            task = PeriodicTask(**task_dict)
            scheduler = TaskScheduler(task, today)

            if not scheduler.should_remind_today():
                continue

            schedule_times = scheduler.get_hourly_schedule_for_day(today) if task.cycle_type == 'hourly' else [task.time_of_day]
            for schedule_time in schedule_times:
                if not schedule_time:
                    continue
                occ_id = self.create_occurrence_if_missing(task.id, today, scheduled_time=schedule_time)
                if not occ_id:
                    continue

                cur = self.db.execute("SELECT status, reminder_job_id FROM periodic_occurrences WHERE id = ?", (occ_id,))
                status, job_name = cur.fetchone()
                if status not in ('pending', 'reminded'):
                    continue
                if task.cycle_type == 'once' and task.start_date and task.start_date != today.isoformat():
                    continue
                if getattr(task, 'task_kind', 'scheduled') == 'system':
                    continue
                if not job_name:
                    job_name = self.schedule_reminder_cron(task.id, today, schedule_time)
                    if job_name:
                        self.db.execute("UPDATE periodic_occurrences SET reminder_job_id = ? WHERE id = ?", (job_name, occ_id))
                        db_commit()
                        scheduled += 1

        return scheduled

    def cleanup_old_jobs(self, before_date: date) -> int:
        cur = self.db.execute(
            """
            SELECT o.id, o.reminder_job_id
            FROM periodic_occurrences o
            WHERE o.date <= ? AND o.reminder_job_id IS NOT NULL
            """,
            (before_date.isoformat(),),
        )
        jobs = cur.fetchall()

        cleaned = 0
        for occ_id, job_name in jobs:
            try:
                result = subprocess.run(build_cron_remove_command(job_name), capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    self.db.execute("UPDATE periodic_occurrences SET reminder_job_id = NULL WHERE id = ?", (occ_id,))
                    cleaned += 1
            except subprocess.TimeoutExpired:
                print(f"Timeout removing cron job {job_name}")
            except Exception as e:
                print(f"Error removing cron job {job_name}: {e}")

        db_commit()
        return cleaned

    def complete_occurrence(self, occurrence_id: int) -> bool:
        with LearningContext("complete_occurrence", f"Complete occurrence {occurrence_id}", confidence="H"):
            cur = self.db.execute(
                """
                UPDATE periodic_occurrences
                SET status = 'completed', completed_at = CURRENT_TIMESTAMP,
                    completion_mode = COALESCE(completion_mode, 'manual')
                WHERE id = ? AND status != 'completed'
                """,
                (occurrence_id,),
            )
            affected = cur.rowcount
            if affected > 0:
                db_commit()
                cur = self.db.execute("SELECT task_id FROM periodic_occurrences WHERE id = ?", (occurrence_id,))
                row = cur.fetchone()
                if row:
                    task_id = row[0]
                    cur = self.db.execute("SELECT cycle_type, n_per_month, count_current_month FROM periodic_tasks WHERE id = ?", (task_id,))
                    cycle_type_row = cur.fetchone()
                    if cycle_type_row and cycle_type_row[0] == 'monthly_n_times':
                        self.db.execute("UPDATE periodic_tasks SET count_current_month = count_current_month + 1 WHERE id = ?", (task_id,))
                        n_per_month = cycle_type_row[1]
                        current_count = (cycle_type_row[2] or 0)
                        if n_per_month is not None and current_count + 1 >= n_per_month:
                            self.db.execute(
                                """
                                UPDATE periodic_occurrences
                                SET status = 'completed', is_auto_completed = 1,
                                    completion_mode = COALESCE(completion_mode, 'auto_quota')
                                WHERE task_id = ? AND status IN ('pending', 'reminded')
                                  AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now', 'localtime')
                                """,
                                (task_id,),
                            )
                        db_commit()
            return affected > 0

    def complete_activity_cycle(self, task_id: int, as_of: Optional[date] = None) -> int:
        with LearningContext("complete_activity_cycle", f"Complete all pending for task {task_id} up to today", confidence="H"):
            today = to_shanghai_date(as_of)
            task_dict = get_periodic_task(task_id)
            if not task_dict:
                return 0
            task = PeriodicTask(**task_dict)
            affected = 0

            cur = self.db.execute(
                """
                SELECT id FROM periodic_occurrences
                WHERE task_id = ? AND status = 'pending'
                  AND date <= ?
                  AND strftime('%Y-%m', date) = ?
                """,
                (task_id, today.isoformat(), today.strftime('%Y-%m')),
            )
            pending_ids = [row[0] for row in cur.fetchall()]

            for occ_id in pending_ids:
                self.complete_occurrence(occ_id)
                affected += 1

            if task.cycle_type == 'monthly_n_times':
                updated_task = PeriodicTask(**(get_periodic_task(task_id) or {}))
                if updated_task.count_current_month >= (updated_task.n_per_month or 0):
                    cur = self.db.execute(
                        """
                        UPDATE periodic_occurrences
                        SET status = 'completed', is_auto_completed = 1,
                            completion_mode = COALESCE(completion_mode, 'auto_quota')
                        WHERE task_id = ? AND status = 'pending'
                          AND strftime('%Y-%m', date) = ?
                        """,
                        (task_id, today.strftime('%Y-%m')),
                    )
                    affected += cur.rowcount
                    db_commit()

            cur = self.db.execute(
                """
                SELECT reminder_job_id FROM periodic_occurrences
                WHERE task_id = ? AND reminder_job_id IS NOT NULL
                """,
                (task_id,),
            )
            job_names = [row[0] for row in cur.fetchall()]
            for job_name in job_names:
                try:
                    subprocess.run(build_cron_remove_command(job_name), capture_output=True, text=True, timeout=10)
                except Exception:
                    pass

            return affected

    def _format_reminder_message(self, task_name: str, occ_date: date, time_of_day: str, reminder_template: Optional[str], immediate: bool) -> str:
        if not reminder_template:
            if immediate:
                return f"⏰ 周期任务提醒（补发）：{task_name} 已到时间（{occ_date} {time_of_day}）"
            return f"⏰ 周期任务提醒（提前5分钟）：{task_name} 即将开始"

        template_vars = {
            "task_name": task_name,
            "name": task_name,
            "date": occ_date.isoformat(),
            "time": time_of_day,
            "when": "immediate" if immediate else "scheduled",
        }
        try:
            return reminder_template.format_map(template_vars)
        except KeyError:
            return reminder_template

    def ensure_today_occurrences(self) -> int:
        today = to_shanghai_date()
        self.reset_monthly_counters(today)

        count = 0
        tasks = get_periodic_tasks(active_only=True)

        for task_dict in tasks:
            task = PeriodicTask(**task_dict)
            scheduler = TaskScheduler(task, today)

            if not scheduler.should_remind_today():
                continue

            schedule_times = scheduler.get_hourly_schedule_for_day(today) if task.cycle_type == 'hourly' else [task.time_of_day]
            for schedule_time in schedule_times:
                occ_id = self.create_occurrence_if_missing(task.id, today, scheduled_time=schedule_time)
                if occ_id:
                    count += 1

        return count

    def _build_today_todo_snapshot(self, today: date) -> str:
        active_periodic_rows = self.db.execute(
            """
            SELECT o.id, o.date, o.status, t.name, t.cycle_type, o.scheduled_time
            FROM periodic_occurrences o
            JOIN periodic_tasks t ON o.task_id = t.id
            WHERE o.date = ? AND o.status IN ('pending', 'reminded')
            ORDER BY COALESCE(o.scheduled_time, t.time_of_day), t.name, o.id
            """,
            (today.isoformat(),),
        ).fetchall()
        skipped_periodic_rows = self.db.execute(
            """
            SELECT o.id, o.date, o.status, t.name, t.cycle_type, o.scheduled_time
            FROM periodic_occurrences o
            JOIN periodic_tasks t ON o.task_id = t.id
            WHERE o.date = ? AND o.status = 'skipped'
            ORDER BY COALESCE(o.scheduled_time, t.time_of_day), t.name, o.id
            """,
            (today.isoformat(),),
        ).fetchall()

        active_simple_rows = self.db.execute(
            """
            SELECT e.id, e.text, e.status, COALESCE(g.name, 'Inbox') AS group_name
            FROM entries e
            LEFT JOIN groups g ON e.group_id = g.id
            WHERE e.status IN ('pending', 'in_progress')
              AND NOT EXISTS (
                  SELECT 1 FROM periodic_tasks t
                  WHERE t.legacy_entry_id = e.id
              )
            ORDER BY e.id
            """
        ).fetchall()
        skipped_simple_rows = self.db.execute(
            """
            SELECT e.id, e.text, e.status, COALESCE(g.name, 'Inbox') AS group_name
            FROM entries e
            LEFT JOIN groups g ON e.group_id = g.id
            WHERE e.status = 'skipped'
              AND NOT EXISTS (
                  SELECT 1 FROM periodic_tasks t
                  WHERE t.legacy_entry_id = e.id
              )
            ORDER BY e.id
            """
        ).fetchall()

        lines = [f"📋 今日待办总览（{today.isoformat()}）"]
        if active_periodic_rows:
            lines.append("")
            lines.append("【今日周期任务】")
            for row in active_periodic_rows:
                status = row['status']
                if status == 'reminded':
                    status = '已提醒'
                schedule_suffix = f" @ {row['scheduled_time']}" if row['scheduled_time'] else ''
                lines.append(f"- FIN-{row['id']} | {row['name']} ({row['cycle_type']}){schedule_suffix} | {status}")
        else:
            lines.append("")
            lines.append("【今日周期任务】")
            lines.append("- 无")

        if active_simple_rows:
            lines.append("")
            lines.append("【其他待办】")
            for row in active_simple_rows:
                status = row['status']
                if status == 'in_progress':
                    status = '进行中'
                lines.append(f"- ID{row['id']} | {row['group_name']} | {row['text']} | {status}")
        else:
            lines.append("")
            lines.append("【其他待办】")
            lines.append("- 无")

        skipped_total = len(skipped_periodic_rows) + len(skipped_simple_rows)
        if skipped_total:
            lines.append("")
            lines.append(f"【已跳过】共 {skipped_total} 项（默认不混入活跃待办）")
            for row in skipped_periodic_rows:
                schedule_suffix = f" @ {row['scheduled_time']}" if row['scheduled_time'] else ''
                lines.append(f"- FIN-{row['id']} | {row['name']} ({row['cycle_type']}){schedule_suffix} | 已跳过")
            for row in skipped_simple_rows:
                lines.append(f"- ID{row['id']} | {row['group_name']} | {row['text']} | 已跳过")

        return "\n".join(lines)

    def _send_today_todo_snapshot(self, today: date) -> bool:
        try:
            chat_id = get_chat_id()
        except ValueError as exc:
            print(f"Chronos chat_id not configured for todo snapshot: {exc}")
            return False

        now_utc = datetime.now(ZoneInfo('UTC')).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        message_text = self._build_today_todo_snapshot(today)
        job_name = f"todo_snapshot_{today.strftime('%Y%m%d')}"
        try:
            result = subprocess.run(
                build_cron_add_command(job_name=job_name, at_iso=now_utc, message=message_text, chat_id=chat_id),
                capture_output=True,
                text=True,
                timeout=10,
            )
        except (OSError, subprocess.SubprocessError) as e:
            print(f"Failed to send todo snapshot: {e}")
            return False

        if result.returncode != 0:
            print(f"Failed to send todo snapshot: {result.stderr}")
            return False
        return True

    def run_daily(self) -> int:
        with LearningContext("periodic_manager_daily_run", "Generate today's reminders, clean old cron jobs, and push today's todo snapshot", confidence="H"):
            today = to_shanghai_date()
            scheduled = self.generate_reminders_for_today()
            cleaned = self.cleanup_old_jobs(today - timedelta(days=1))
            snapshot_sent = 1 if self._send_today_todo_snapshot(today) else 0
            return scheduled + cleaned + snapshot_sent


def main():
    manager = PeriodicTaskManager()
    try:
        parser = build_parser()
        args = parser.parse_args()

        if args.add:
            if not args.name:
                print("Missing required --name for --add")
                sys.exit(2)
            try:
                validate_add_params(args)
            except ValueError as exc:
                print(f"参数错误：{exc}")
                sys.exit(2)

            params = {
                'name': args.name,
                'category': args.category,
                'cycle_type': args.cycle_type,
                'time_of_day': args.time_of_day,
                'task_kind': args.task_kind,
                'source': args.source,
            }
            if args.weekday is not None:
                params['weekday'] = args.weekday
            if args.day_of_month is not None:
                params['day_of_month'] = args.day_of_month
            if args.range_start is not None:
                params['range_start'] = args.range_start
            if args.range_end is not None:
                params['range_end'] = args.range_end
            if args.n_per_month is not None:
                params['n_per_month'] = args.n_per_month
            if args.interval_hours is not None:
                params['interval_hours'] = args.interval_hours
            if args.dates_list is not None:
                params['dates_list'] = args.dates_list
            if args.start_date is not None:
                params['start_date'] = args.start_date
            if args.end_date is not None:
                params['end_date'] = args.end_date
            if args.reminder_template is not None:
                params['reminder_template'] = args.reminder_template
            if args.legacy_entry_id is not None:
                params['legacy_entry_id'] = args.legacy_entry_id
            if args.special_handler is not None:
                params['special_handler'] = args.special_handler
            if args.handler_payload is not None:
                params['handler_payload'] = args.handler_payload
            if args.delivery_target is not None:
                params['delivery_target'] = args.delivery_target
            if args.delivery_mode is not None:
                params['delivery_mode'] = args.delivery_mode

            activity_id = manager.add_activity(**params)
            print(f"✅ Added task {activity_id}: {params.get('name')}")

        elif args.complete_activity is not None:
            affected = manager.complete_activity_cycle(args.complete_activity)
            print(f"Completed {affected} occurrences for task {args.complete_activity}")

        elif args.ensure_today:
            count = manager.ensure_today_occurrences()
            print(f"Ensured {count} occurrences for today")

        else:
            result = manager.run_daily()
            print(f"Periodic task manager: processed {result} items")
    finally:
        manager.db.close()


if __name__ == "__main__":
    main()
