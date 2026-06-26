"""
交易日历模块
"""

from datetime import datetime, date, timedelta

from utils.helpers import parse_date


def is_trade_day(dt=None):
    if dt is None:
        dt = date.today()
    elif isinstance(dt, str):
        dt = parse_date(dt)
        if dt is None:
            return False
    if isinstance(dt, datetime):
        dt = dt.date()
    return dt.weekday() < 5


def prev_trade_day(dt=None):
    if dt is None:
        dt = date.today()
    elif isinstance(dt, str):
        dt = parse_date(dt)
        if dt is None:
            dt = date.today()
    if isinstance(dt, datetime):
        dt = dt.date()
    check_date = dt - timedelta(days=1)
    while check_date.weekday() >= 5:
        check_date -= timedelta(days=1)
    return check_date


def next_trade_day(dt=None):
    if dt is None:
        dt = date.today()
    elif isinstance(dt, str):
        dt = parse_date(dt)
        if dt is None:
            dt = date.today()
    if isinstance(dt, datetime):
        dt = dt.date()
    check_date = dt + timedelta(days=1)
    while check_date.weekday() >= 5:
        check_date += timedelta(days=1)
    return check_date


def get_effective_date(dt=None, mode='morning'):
    if dt is None:
        dt = date.today()
    elif isinstance(dt, str):
        dt = parse_date(dt)
        if dt is None:
            dt = date.today()
    if isinstance(dt, datetime):
        dt = dt.date()
    if mode == 'morning':
        if not is_trade_day(dt):
            return prev_trade_day(dt)
        return dt
    else:
        if not is_trade_day(dt):
            return prev_trade_day(dt)
        return dt
