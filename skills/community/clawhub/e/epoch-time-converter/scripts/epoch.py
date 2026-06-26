#!/usr/bin/env python3
"""Convert between Unix epoch timestamps and human-readable datetimes.

Usage:
    epoch.py to-date <value> [--unit s|ms] [--tz <IANA>]
    epoch.py to-epoch <iso-or-space-string> --tz <IANA> [--unit s|ms]
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def _parse_tz(name: str) -> ZoneInfo:
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError as exc:
        raise SystemExit(f"unknown timezone: {name!r}") from exc


def cmd_to_date(args: argparse.Namespace) -> int:
    raw = args.value
    if args.unit == "ms":
        seconds = raw / 1000.0
    else:
        seconds = float(raw)
    tz = _parse_tz(args.tz)
    dt = datetime.fromtimestamp(seconds, tz=timezone.utc).astimezone(tz)
    offset = dt.strftime("%z")
    offset_fmt = f"{offset[:3]}:{offset[3:]}" if offset else ""
    print(f"{dt.strftime('%Y-%m-%d %H:%M:%S')} {offset_fmt} ({args.tz})")
    return 0


def cmd_to_epoch(args: argparse.Namespace) -> int:
    text = args.value.strip().replace("T", " ")
    # Accept "YYYY-MM-DD HH:MM[:SS[.ffffff]]"
    fmts = [
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
    ]
    parsed: datetime | None = None
    for fmt in fmts:
        try:
            parsed = datetime.strptime(text, fmt)
            break
        except ValueError:
            continue
    if parsed is None:
        raise SystemExit(f"could not parse datetime: {args.value!r}")
    tz = _parse_tz(args.tz)
    aware = parsed.replace(tzinfo=tz)
    epoch = aware.timestamp()
    if args.unit == "ms":
        print(f"{int(round(epoch * 1000))} (ms, from {args.value!r} in {args.tz})")
    else:
        print(f"{int(round(epoch))} (s, from {args.value!r} in {args.tz})")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="epoch", description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("to-date", help="epoch -> human datetime")
    p1.add_argument("value", type=int)
    p1.add_argument("--unit", choices=["s", "ms"], default="s")
    p1.add_argument("--tz", default="UTC")
    p1.set_defaults(func=cmd_to_date)

    p2 = sub.add_parser("to-epoch", help="human datetime -> epoch")
    p2.add_argument("value")
    p2.add_argument("--tz", required=True)
    p2.add_argument("--unit", choices=["s", "ms"], default="s")
    p2.set_defaults(func=cmd_to_epoch)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
