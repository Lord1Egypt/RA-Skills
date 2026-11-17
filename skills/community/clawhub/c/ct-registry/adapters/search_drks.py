#!/usr/bin/env python3
"""search_drks.py - DRKS (German Clinical Trials Register) search (delegates).

DRKS search is JS/redirect-based: the search form has no static action and a
plain GET/POST returns no result rows, so there is no clean HTTP search API. It
is served by the SAME unified Coze workflow (source="drks"), extended alongside
WHO ICTRP / CDE / ISRCTN / ChiCTR. This thin wrapper forwards to
search_ictrp.py --source drks, sharing the ICTRP Bearer token and the unified
endpoint — no separate endpoint or token to provision.

The unified endpoint must be configured to serve source="drks" before real
records are returned. No network I/O unless --run (safe preview).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import search_ictrp  # noqa: E402


if __name__ == "__main__":
    sys.argv = [sys.argv[0], "--source", "drks"] + sys.argv[1:]
    search_ictrp.main()
