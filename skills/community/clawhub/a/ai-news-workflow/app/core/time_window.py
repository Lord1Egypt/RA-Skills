from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


DEFAULT_TZ = "Asia/Shanghai"


@dataclass
class TimeWindow:
    start_time: datetime
    end_time: datetime

    def contains(self, dt: datetime) -> bool:
        dt = normalize_to_timezone(
            dt,
            self.start_time.tzinfo.key if hasattr(self.start_time.tzinfo, "key") else DEFAULT_TZ,
        )
        return self.start_time <= dt < self.end_time

    def to_text(self) -> str:
        return f"{self.start_time.strftime('%Y-%m-%d %H:%M:%S')} ~ {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}"


def normalize_to_timezone(dt: datetime | None, timezone_str: str = DEFAULT_TZ) -> datetime | None:
    if dt is None:
        return None

    tz = ZoneInfo(timezone_str)

    if dt.tzinfo is None:
        return dt.replace(tzinfo=tz)

    return dt.astimezone(tz)

def build_time_window(
    mode: str = "previous_day",
    timezone_str: str = DEFAULT_TZ,
    start_hour: int = 0,
    end_hour: int = 0,
    lookback_days: int = 3,
    now: datetime | None = None,
) -> TimeWindow:
    """
    支持两种模式：
    1) previous_day：前一天 start_hour:00:00（含）到当天 end_hour:00:00（不含）
       - 允许 start_hour != end_hour（例如 23->23）
       - end_time 以“今天 end_hour:00:00”为锚点
    2) rolling_days：当前时间往前 lookback_days 天（含 now）
    """
    tz = ZoneInfo(timezone_str)

    # 统一 now 为带时区的时间
    if now is None:
        now = datetime.now(tz)
    else:
        now = normalize_to_timezone(now, timezone_str)

    mode = (mode or "previous_day").strip().lower()

    if mode in {"rolling_days", "rolling", "lookback"}:
        end_time = now
        start_time = now - timedelta(days=int(lookback_days))
        return TimeWindow(start_time=start_time, end_time=end_time)

    # previous_day：以“今天 end_hour:00:00”为锚点
    # 如果当前时间早于今天 end_hour:00:00，则锚点仍是今天 end_hour
    # 如果当前时间晚于今天 end_hour:00:00，锚点仍是今天 end_hour（符合你“统计口径到当天 end_hour”）
    anchor_end = now.replace(hour=int(end_hour), minute=0, second=0, microsecond=0)

    # start_time 是“锚点往前一天”，再设置 start_hour
    start_time = (anchor_end - timedelta(days=1)).replace(hour=int(start_hour), minute=0, second=0, microsecond=0)
    end_time = anchor_end

    # 防御：如果 start_time >= end_time（极少见但可能来自非法参数），则兜底为前一天0点到今天0点
    if start_time >= end_time:
        end_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start_time = (end_time - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

    return TimeWindow(start_time=start_time, end_time=end_time)

def get_event_date(dt: datetime | None, timezone_str: str = DEFAULT_TZ) -> str:
    if dt is None:
        return ""
    dt = normalize_to_timezone(dt, timezone_str)
    return dt.strftime("%Y-%m-%d")

def normalize_to_shanghai(dt: datetime | None) -> datetime | None:
    """
    向后兼容旧代码。
    等价于 normalize_to_timezone(dt, "Asia/Shanghai")
    """
    return normalize_to_timezone(dt, "Asia/Shanghai")