#!/usr/bin/env python3
"""Convert between Unix epoch timestamps and human-readable datetimes.

Usage:
  epoch.py now [--tz TZ]
  epoch.py to-human <EPOCH> [--tz TZ]
  epoch.py to-epoch "<YYYY-MM-DD HH:MM:SS>" [--tz TZ]

Notes:
  - <EPOCH> may be in seconds, milliseconds, microseconds, or nanoseconds;
    the unit is auto-detected by magnitude.
  - --tz accepts an IANA name (e.g. Asia/Shanghai). Defaults to UTC.
"""
import argparse
import sys
from datetime import datetime, timezone

try:
    from zoneinfo import ZoneInfo
except ImportError:  # Python < 3.9
    ZoneInfo = None


def resolve_tz(name):
    if not name or name.upper() == "UTC":
        return timezone.utc
    if ZoneInfo is None:
        raise SystemExit("zoneinfo unavailable; use --tz UTC")
    try:
        return ZoneInfo(name)
    except Exception:
        raise SystemExit(f"unknown timezone: {name}")


def detect_seconds(value):
    """Auto-detect unit from magnitude and return float seconds."""
    n = abs(value)
    if n >= 1e17:      # nanoseconds
        return value / 1e9
    if n >= 1e14:      # microseconds
        return value / 1e6
    if n >= 1e11:      # milliseconds
        return value / 1e3
    return float(value)  # seconds


def cmd_now(tz):
    dt = datetime.now(tz)
    epoch = dt.timestamp()
    print(f"epoch_seconds: {int(epoch)}")
    print(f"epoch_millis:  {int(epoch * 1000)}")
    print(f"datetime:      {dt.isoformat()}")


def cmd_to_human(epoch_raw, tz):
    secs = detect_seconds(float(epoch_raw))
    dt = datetime.fromtimestamp(secs, tz)
    print(dt.isoformat())


def cmd_to_epoch(text, tz):
    parsed = None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            parsed = datetime.strptime(text, fmt)
            break
        except ValueError:
            continue
    if parsed is None:
        raise SystemExit(f"could not parse datetime: {text!r}")
    parsed = parsed.replace(tzinfo=tz)
    print(int(parsed.timestamp()))


def main(argv=None):
    p = argparse.ArgumentParser(description="Epoch <-> human datetime converter")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_now = sub.add_parser("now", help="show current time")
    p_now.add_argument("--tz", default="UTC")

    p_h = sub.add_parser("to-human", help="epoch -> ISO datetime")
    p_h.add_argument("epoch")
    p_h.add_argument("--tz", default="UTC")

    p_e = sub.add_parser("to-epoch", help="datetime -> epoch seconds")
    p_e.add_argument("datetime")
    p_e.add_argument("--tz", default="UTC")

    args = p.parse_args(argv)
    tz = resolve_tz(args.tz)

    if args.cmd == "now":
        cmd_now(tz)
    elif args.cmd == "to-human":
        cmd_to_human(args.epoch, tz)
    elif args.cmd == "to-epoch":
        cmd_to_epoch(args.datetime, tz)


if __name__ == "__main__":
    main()
