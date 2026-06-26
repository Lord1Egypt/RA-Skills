#!/usr/bin/env python3
"""Compatibility wrapper for the old streaming helper name.

The self-contained implementation runs one due turn at a time. Durable
progress comes from sshsign leases plus OpenClaw cron/scan, not from a
long-lived upstream negotiation process.
"""
from __future__ import annotations

from _turn_once import main


if __name__ == "__main__":
    raise SystemExit(main())
