"""Scheduling logic: date matching, occurrence generation, quota management."""
import calendar
from datetime import datetime, timedelta, date
from typing import List, Optional, Tuple
from zoneinfo import ZoneInfo
from functools import lru_cache

from .models import PeriodicTask

SHANGHAI_TZ = ZoneInfo('Asia/Shanghai')


def to_shanghai_date(dt: Optional[datetime] = None) -> date:
    """Convert datetime to Shanghai date (today if None)."""
    if dt is None:
        return datetime.now(SHANGHAI_TZ).date()
    if isinstance(dt, date) and not isinstance(dt, datetime):
        return dt
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=SHANGHAI_TZ)
    else:
        dt = dt.astimezone(SHANGHAI_TZ)
    return dt.date()


def is_same_month(d1: date, d2: date) -> bool:
    return d1.year == d2.year and d1.month == d2.month


@lru_cache(maxsize=128)
def get_weekdays_in_month(year: int, month: int, weekday: int) -> List[date]:
    """Return all dates in month matching weekday (0=Monday)."""
    first_day = date(year, month, 1)
    if month == 12:
        last_day = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(year, month + 1, 1) - timedelta(days=1)

    dates = []
    current = first_day
    while current <= last_day:
        if current.weekday() == weekday:
            dates.append(current)
        current += timedelta(days=1)
    return dates


class TaskScheduler:
    """Encapsulates all scheduling logic for periodic tasks."""

    def __init__(self, task: PeriodicTask, as_of: Optional[date] = None):
        self.task = task
        self.as_of = to_shanghai_date(as_of)
        self.end_date = None
        if task.end_date:
            try:
                self.end_date = date.fromisoformat(task.end_date)
            except ValueError:
                self.end_date = None
        self.start_date = None
        if task.start_date:
            try:
                self.start_date = date.fromisoformat(task.start_date)
            except ValueError:
                self.start_date = None

    def should_remind_today(self) -> bool:
        """Check if today matches the cycle and quota allows."""
        today = self.as_of

        if self.start_date and today < self.start_date:
            return False
        if self.end_date and today > self.end_date:
            return False

        if self.task.cycle_type == 'once':
            return self.start_date == today

        if self.task.cycle_type == 'daily':
            return True

        if self.task.cycle_type == 'hourly':
            return self._get_hourly_schedule_for_day(today) != []

        if self.task.cycle_type == 'weekly':
            if self.task.weekday is None:
                return False
            return today.weekday() == self.task.weekday

        if self.task.cycle_type == 'monthly_fixed':
            if self.task.day_of_month is None:
                return False
            return today.day == self.task.day_of_month

        if self.task.cycle_type == 'monthly_range':
            return self._in_monthly_range(today)

        if self.task.cycle_type == 'monthly_n_times':
            if self.task.weekday is not None and today.weekday() != self.task.weekday:
                return False
            if self.task.count_current_month >= (self.task.n_per_month or 0):
                return False
            return True

        if self.task.cycle_type == 'monthly_dates':
            return today in self._get_monthly_dates(today.year, today.month)

        return False

    def _parse_time_of_day(self) -> tuple[int, int] | None:
        raw = (self.task.time_of_day or '').strip()
        if not raw:
            return None
        try:
            hour_str, minute_str = raw.split(':', 1)
            hour = int(hour_str)
            minute = int(minute_str)
        except ValueError:
            return None
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            return None
        return hour, minute

    def _normalized_interval_hours(self) -> int | None:
        value = self.task.interval_hours
        if value is None:
            value = 1
        try:
            value = int(value)
        except (TypeError, ValueError):
            return None
        if value <= 0 or value > 24:
            return None
        return value

    def _get_hourly_schedule_for_day(self, target_day: date) -> List[str]:
        interval = self._normalized_interval_hours()
        anchor = self._parse_time_of_day()
        if interval is None or anchor is None:
            return []

        start_hour, start_minute = anchor
        slots: List[str] = []
        seen: set[str] = set()
        for hour in range(start_hour, 24, interval):
            label = f"{hour:02d}:{start_minute:02d}"
            if label not in seen:
                slots.append(label)
                seen.add(label)
        if interval != 24:
            for hour in range(start_hour - interval, -1, -interval):
                label = f"{hour:02d}:{start_minute:02d}"
                if label not in seen:
                    slots.append(label)
                    seen.add(label)
        slots.sort()
        return slots

    def get_hourly_schedule_for_day(self, target_day: date) -> List[str]:
        return self._get_hourly_schedule_for_day(target_day)

    def _get_monthly_dates(self, year: int, month: int) -> List[date]:
        if not self.task.dates_list:
            return []
        days: List[int] = []
        for chunk in str(self.task.dates_list).split(','):
            chunk = chunk.strip()
            if not chunk:
                continue
            try:
                day = int(chunk)
            except ValueError:
                continue
            if 1 <= day <= 31:
                days.append(day)
        unique_days = sorted(set(days))
        results: List[date] = []
        for day in unique_days:
            try:
                results.append(date(year, month, day))
            except ValueError:
                continue
        return results

    def _in_monthly_range(self, today: date) -> bool:
        """Check if today falls within the configured range (may cross month)."""
        start = self.task.range_start
        end = self.task.range_end
        if start is None or end is None:
            return False

        if start <= end:
            return start <= today.day <= end

        year = today.year
        month = today.month

        try:
            interval1_start = date(year, month, start)
            if month == 12:
                interval1_end = date(year + 1, 1, end)
            else:
                interval1_end = date(year, month + 1, end)
            if interval1_start <= today <= interval1_end:
                return True
        except ValueError:
            pass

        try:
            if month == 1:
                interval2_start = date(year - 1, 12, start)
            else:
                interval2_start = date(year, month - 1, start)
            interval2_end = date(year, month, end)
            if interval2_start <= today <= interval2_end:
                return True
        except ValueError:
            pass

        return False

    def get_occurrences_for_month(self, year: int, month: int) -> List[date]:
        """Generate all occurrence dates for the given month, respecting start/end date."""
        cycle_type = self.task.cycle_type
        dates: List[date] = []

        if cycle_type == 'once':
            if self.start_date and self.start_date.year == year and self.start_date.month == month:
                dates = [self.start_date]
            else:
                dates = []

        elif cycle_type == 'daily':
            days_in_month = calendar.monthrange(year, month)[1]
            dates = [date(year, month, d) for d in range(1, days_in_month + 1)]

        elif cycle_type == 'hourly':
            days_in_month = calendar.monthrange(year, month)[1]
            dates = [date(year, month, d) for d in range(1, days_in_month + 1)]

        elif cycle_type == 'weekly':
            if self.task.weekday is None:
                return []
            dates = get_weekdays_in_month(year, month, self.task.weekday)

        elif cycle_type == 'monthly_fixed':
            day = self.task.day_of_month
            if day is None:
                return []
            try:
                dates = [date(year, month, day)]
            except ValueError:
                dates = []

        elif cycle_type == 'monthly_range':
            start = self.task.range_start
            end = self.task.range_end
            if start is None or end is None:
                return []

            days_in_month = calendar.monthrange(year, month)[1]
            dates = [
                current
                for current in (date(year, month, day) for day in range(1, days_in_month + 1))
                if self._in_monthly_range(current)
            ]

        elif cycle_type == 'monthly_n_times':
            if self.task.weekday is None:
                days_in_month = calendar.monthrange(year, month)[1]
                dates = [date(year, month, d) for d in range(1, days_in_month + 1)]
            else:
                dates = get_weekdays_in_month(year, month, self.task.weekday)

        elif cycle_type == 'monthly_dates':
            dates = self._get_monthly_dates(year, month)

        else:
            return []

        if self.start_date:
            dates = [d for d in dates if d >= self.start_date]
        if self.end_date:
            dates = [d for d in dates if d <= self.end_date]

        return dates

    def get_pending_dates_in_month(self, year: int, month: int, existing_occurrences: List[Tuple[date, str]]) -> List[date]:
        """Return dates in month that should be pending (not already completed/skipped)."""
        all_dates = self.get_occurrences_for_month(year, month)
        if not all_dates:
            return []

        done_dates = {d for d, s in existing_occurrences if s in ('completed', 'skipped')}
        pending_dates = [d for d in all_dates if d not in done_dates]

        if self.task.cycle_type == 'monthly_n_times':
            count_current = self.task.count_current_month
            n = self.task.n_per_month or 0
            allowed = max(0, n - count_current)
            if allowed == 0:
                return []
            pending_dates.sort()
            return pending_dates[:allowed]

        return pending_dates
