#!/usr/bin/env python3
"""search_isrctn.py - ISRCTN search (delegates to the unified Coze endpoint).

ISRCTN has NO clean public search API: its /api/query endpoint returns 404 for
both GET and POST, and the public search page is JS-rendered (raw HTML has no
results). It is therefore served by the SAME unified Coze workflow that handles
WHO ICTRP (source="who") and China CDE (source="chinadrugtrials"), extended with
source="isrctn". This thin wrapper simply forwards to search_ictrp.py
--source isrctn, sharing the ICTRP Bearer token (embedded in adapters/endpoint_token.py; no .dat file) and the
unified endpoint — no separate endpoint or token to provision.

The unified endpoint must be configured (by the workflow author) to serve
source="isrctn" before real records are returned; until then the call returns an
empty result set (not a 401). No network I/O unless --run (safe preview).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import search_ictrp  # noqa: E402


if __name__ == "__main__":
    # Inject --source isrctn ahead of any user args; forward the rest verbatim
    # (--q / --out / --run / --token / --endpoint / --timeout / --demand-id / ...).
    sys.argv = [sys.argv[0], "--source", "isrctn"] + sys.argv[1:]
    search_ictrp.main()
