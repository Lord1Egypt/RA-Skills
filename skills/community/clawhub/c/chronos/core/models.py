"""Data models for periodic tasks."""
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

ALLOWED_CYCLE_TYPES = (
    'once',
    'daily',
    'hourly',
    'weekly',
    'monthly_fixed',
    'monthly_range',
    'monthly_n_times',
    'monthly_dates',
)


@dataclass
class PeriodicTask:
    id: int
    name: str
    category: str = 'Inbox'
    cycle_type: str = 'once'  # once|daily|hourly|weekly|monthly_fixed|monthly_range|monthly_n_times|monthly_dates
    weekday: Optional[int] = None  # 0-6 (0=Monday, Python weekday)
    day_of_month: Optional[int] = None  # 1-31
    range_start: Optional[int] = None
    range_end: Optional[int] = None
    n_per_month: Optional[int] = None
    interval_hours: Optional[int] = None
    time_of_day: Optional[str] = '09:00'  # HH:MM; for hourly this is the anchor slot in each day
    event_time: Optional[str] = None
    timezone: str = 'Asia/Shanghai'
    is_active: bool = True
    count_current_month: int = 0
    end_date: Optional[str] = None  # YYYY-MM-DD, NULL means no end
    reminder_template: Optional[str] = None  # Custom reminder message template
    dates_list: Optional[str] = None
    task_kind: str = 'scheduled'
    source: str = 'chronos'
    legacy_entry_id: Optional[int] = None
    special_handler: Optional[str] = None
    handler_payload: Optional[str] = None
    start_date: Optional[str] = None
    delivery_target: Optional[str] = None
    delivery_mode: Optional[str] = None
    # Monitoring fields (optional, for backward compatibility)
    last_reminder_error: Optional[str] = None
    reminder_error_count: int = 0
    last_reminder_error_at: Optional[str] = None
    created_at: str = field(default_factory=lambda: date.today().isoformat())
    updated_at: str = field(default_factory=lambda: date.today().isoformat())

    @property
    def is_monthly_n_times(self) -> bool:
        return self.cycle_type == 'monthly_n_times'

    @property
    def is_hourly(self) -> bool:
        return self.cycle_type == 'hourly'


@dataclass
class PeriodicOccurrence:
    id: int
    task_id: int
    date: date
    status: str = 'pending'  # pending|reminded|completed|skipped
    reminder_job_id: Optional[str] = None
    is_auto_completed: bool = False
    completed_at: Optional[str] = None
    completion_mode: Optional[str] = None
    special_handler_result: Optional[str] = None
    scheduled_time: Optional[str] = None
    scheduled_at: Optional[str] = None
    legacy_entry_id: Optional[int] = None
