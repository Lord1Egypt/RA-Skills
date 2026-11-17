#!/usr/bin/env python3
"""search_chictr.py - China ChiCTR search (delegates to the unified Coze endpoint).

ChiCTR is the WHO primary registry for China covering academic / investigator-
initiated trials (distinct from CDE, which covers drug trials). It has NO public
API and blocks automated access. It is served by the SAME unified Coze workflow
(source="chictr"), extended alongside WHO ICTRP / CDE / ISRCTN / DRKS. This thin
wrapper forwards to search_ictrp.py --source chictr, sharing the ICTRP Bearer
token and the unified endpoint — no separate endpoint or token to provision.

The unified endpoint must be configured to serve source="chictr" before real
records are returned. No network I/O unless --run (safe preview).

WAF auto-fallback (2026-09-07): When the direct ChiCTR source is judged
unavailable -- i.e. returns 0 records + no error AND the control-word probe also
returns 0 (the signature of the Aliyun WAF `acw_sc__v2` block / backend node
outage) -- this wrapper automatically switches to the WHO ICTRP line with the SAME
keyword and keeps ONLY ChiCTR-origin records (registry field = ChiCTR, or a
ChiCTR registration-number pattern on Main ID / 登记号 / raw). The recovered
records are written back into the CHICTR envelope with `fallback_used=who_ictrp`.
Because WHO only indexes English, the Chinese keyword is auto-localized to
English (curated term_map first, online fallback for long-tail terms) before the
WHO call -- see `_localize_who_payload` in search_ictrp.py. Disable the WHO
fallback via `--no-fallback-who`, or disable the keyword localization via
`--no-kw-localize`. This mirrors the behavior documented in
search_ictrp.py `run()` / `_fallback_who_for_chictr`.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import search_ictrp  # noqa: E402


if __name__ == "__main__":
    sys.argv = [sys.argv[0], "--source", "chictr"] + sys.argv[1:]
    search_ictrp.main()
