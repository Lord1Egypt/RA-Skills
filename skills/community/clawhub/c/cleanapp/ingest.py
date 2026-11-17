#!/usr/bin/env python3
"""Compatibility entry point for the public single-report client.

Authenticated batches remain available through the separate CleanApp Wire API/CLI.
"""
from report import main

if __name__ == "__main__":
    raise SystemExit(main())
