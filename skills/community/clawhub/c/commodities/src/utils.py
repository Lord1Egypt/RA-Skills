from datetime import datetime


def format_number(num, decimals=2):
    if num is None:
        return "N/A"

    try:
        return f"{float(num):,.{decimals}f}"
    except (TypeError, ValueError):
        return "N/A"


def format_range(label: str, range_data: dict) -> str:
    high = range_data.get("high")
    low = range_data.get("low")
    high_str = f"${format_number(high)}" if high is not None else "N/A"
    low_str = f"${format_number(low)}" if low is not None else "N/A"
    return f"{label} Low:  {low_str}\n{label} High: {high_str}"


def format_volume_summary(volume, avg_volume) -> str:
    if volume is None or avg_volume is None or avg_volume <= 0:
        return "Vol: N/A"

    volume_percent = (volume / avg_volume) * 100
    return (
        f"Vol: {format_number(volume / 1_000_000, 1)}M "
        f"Avg: {format_number(avg_volume / 1_000_000, 1)}M "
        f"| {format_number(volume_percent, 0)}% of avg"
    )


def format_event_date(event_date) -> str:
    if isinstance(event_date, str) and event_date.startswith("Est."):
        return event_date
    if isinstance(event_date, (int, float)):
        return datetime.utcfromtimestamp(event_date).strftime("%Y-%m-%d %H:%M:%S GMT")
    if isinstance(event_date, datetime):
        return event_date.strftime("%Y-%m-%d %H:%M:%S GMT")

    try:
        value = str(event_date)
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S GMT")
    except Exception:
        return str(event_date)
