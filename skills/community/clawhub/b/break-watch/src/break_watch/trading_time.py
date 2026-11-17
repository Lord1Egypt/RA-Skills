from __future__ import annotations

from datetime import datetime, time


MORNING_START = time(9, 30)
MORNING_END = time(11, 30)
AFTERNOON_START = time(13, 0)
AFTERNOON_END = time(15, 0)
TOTAL_TRADING_MINUTES = 240


def is_trading_time(moment: datetime) -> bool:
    current = moment.time()
    return MORNING_START <= current <= MORNING_END or AFTERNOON_START <= current <= AFTERNOON_END


def trading_progress(moment: datetime) -> float:
    current = moment.time()
    if current < MORNING_START:
        return 0.0
    if MORNING_START <= current <= MORNING_END:
        minutes = _minutes_between(MORNING_START, current)
        return _clamp_progress(minutes / TOTAL_TRADING_MINUTES)
    if current < AFTERNOON_START:
        return 120 / TOTAL_TRADING_MINUTES
    if AFTERNOON_START <= current <= AFTERNOON_END:
        minutes = 120 + _minutes_between(AFTERNOON_START, current)
        return _clamp_progress(minutes / TOTAL_TRADING_MINUTES)
    return 1.0


def _minutes_between(start: time, end: time) -> float:
    start_minutes = start.hour * 60 + start.minute + start.second / 60
    end_minutes = end.hour * 60 + end.minute + end.second / 60
    return max(0.0, end_minutes - start_minutes)


def _clamp_progress(value: float) -> float:
    return max(0.0, min(1.0, value))

