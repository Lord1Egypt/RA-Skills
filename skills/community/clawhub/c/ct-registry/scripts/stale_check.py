#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
stale_check.py / 陈旧试验检测 (stale-trial detection) — upgrade D (2026-09-29)

长期未更新 / 已终止的试验会被误判为「活跃竞品」，污染竞品格局与评分。本模块
基于每条记录的**最后更新日期**与**归一化后的 overallStatus**做纯本地启发式判定，
给活跃态试验打上 stale 标记，并估计「最后活跃时间」(last_active)。

零联网、零第三方依赖（仅 stdlib）。判定规则（默认，均可通过参数调整）：

  活跃态集合（需监控陈旧）：RECRUITING / ACTIVE_NOT_RECRUITING / ENROLLING_BY_INVITATION
                            / NOT_YET_RECRUITING / ONGOING（canon_status 归一后）
  终态集合（不算活跃竞品）：COMPLETED / TERMINATED / WITHDRAWN / SUSPENDED / UNKNOWN

  对「活跃态」记录：
    * 若能取到 last_update_posted（或 last_known_status / results_first_posted /
      start_date 作降级），距 as_of 超过 stale_days（默认 365）→ stale=True，
      reason="no update for N days while status=<X>"。
    * 若完全没有可用日期 → stale=None（未知），reason="no last-update date"，
      绝不臆断为活跃（保守：交人工核对，不静默放行）。
  对「终态」记录：stale=False 但 active_competitor=False（不进入活跃竞品计数）。

输出：每条记录附 `stale` / `stale_reason` / `last_active` / `active_competitor`；
聚合 summary 附 counts（active_competitors / stale_active / terminated /
unknown_date）。ct_registry / report 的竞品格局据此过滤 stale 与终态。
"""
import argparse
import json
import re
import sys
from datetime import date, datetime

# Canonical status buckets (after normalize.canon_status folding)
_ACTIVE_STATUSES = {
    "RECRUITING", "ACTIVE_NOT_RECRUITING", "ENROLLING_BY_INVITATION",
    "NOT_YET_RECRUITING", "ONGOING",
}
_TERMINAL_STATUSES = {
    "COMPLETED", "TERMINATED", "WITHDRAWN", "SUSPENDED", "UNKNOWN",
}

# Field preference order for "last activity" date (earliest = most authoritative)
_LAST_DATE_FIELDS = (
    "last_update_posted", "status_last_known", "results_first_posted",
    "primary_completion_date", "start_date",
)


def _parse_date(v):
    """Parse CT.gov-style '2024-03' / '2024-03-15' / '2024' into a date.

    Partial dates resolve to the FIRST day of the missing component (start of
    month / year) — deliberately conservative, so a stale estimate never hides
    behind a rounded-up late date.
    """
    if not v:
        return None
    s = str(v).strip()
    m = re.match(r"^(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?", s)
    if not m:
        return None
    y = int(m.group(1))
    mo = int(m.group(2)) if m.group(2) else 1
    d = int(m.group(3)) if m.group(3) else 1
    try:
        return date(y, mo, d)
    except ValueError:
        return None


def record_last_date(rec):
    """Return (date, field_used) for the most recent authoritative date on a
    record, following _LAST_DATE_FIELDS preference. None if nothing parses."""
    for f in _LAST_DATE_FIELDS:
        dt = _parse_date(rec.get(f))
        if dt is not None:
            return dt, f
    return None, None


def classify_stale(rec, as_of=None, stale_days=365):
    """Tag one normalized record. Returns the same dict, with keys added:
      stale              : True / False / None (None = cannot determine)
      stale_reason       : human-readable explanation
      last_active        : ISO date string of the estimated last activity
      active_competitor  : True only if status is active AND not stale
    """
    if as_of is None:
        as_of = date.today()
    status = (rec.get("status") or "").strip().upper()
    ld, field = record_last_date(rec)
    out = dict(rec)
    out["last_active"] = ld.isoformat() if ld else None

    if status in _TERMINAL_STATUSES:
        out["stale"] = False
        out["active_competitor"] = False
        out["stale_reason"] = "terminal status %s (not an active competitor)" % status
        return out

    if status in _ACTIVE_STATUSES or status == "":
        if ld is None:
            out["stale"] = None
            out["active_competitor"] = None  # unknown — surface for human check
            out["stale_reason"] = "no usable last-update date; requires manual check"
            return out
        age_days = (as_of - ld).days
        if age_days > stale_days:
            out["stale"] = True
            out["active_competitor"] = False
            out["stale_reason"] = ("no update for %d days (>%d) while status=%s "
                                   "(last from %s)" % (age_days, stale_days,
                                                       status or "ACTIVE", field))
        else:
            out["stale"] = False
            out["active_competitor"] = True
            out["stale_reason"] = "updated %d days ago, status=%s" % (age_days, status)
        return out

    # unrecognized status verbatim (e.g. EU "Authorised") — conservative unknown
    out["stale"] = None
    out["active_competitor"] = None
    out["stale_reason"] = "unrecognized status %r; requires manual check" % status
    return out


def summarize(records):
    """Aggregate stale-detection counts over tagged records."""
    counts = {"total": len(records), "active_competitors": 0,
              "stale_active": 0, "terminal": 0, "unknown": 0}
    for r in records:
        st = r.get("status", "")
        if r.get("active_competitor") is True:
            counts["active_competitors"] += 1
        elif r.get("stale") is True:
            counts["stale_active"] += 1
        elif st in _TERMINAL_STATUSES:
            counts["terminal"] += 1
        else:
            counts["unknown"] += 1
    return counts


def apply(records, as_of=None, stale_days=365):
    """Tag every record; returns (tagged_records, summary)."""
    tagged = [classify_stale(r, as_of=as_of, stale_days=stale_days) for r in records]
    return tagged, summarize(tagged)


def main():
    ap = argparse.ArgumentParser(description="Stale-trial detection (pure local).")
    ap.add_argument("--in", dest="infile", required=True,
                    help="normalized.json path")
    ap.add_argument("--out", help="write tagged records here")
    ap.add_argument("--as-of", help="YYYY-MM-DD reference date (default today)")
    ap.add_argument("--stale-days", type=int, default=365,
                    help="days without update before an active trial is stale")
    args = ap.parse_args()
    as_of = datetime.strptime(args.as_of, "%Y-%m-%d").date() if args.as_of else date.today()
    with open(args.infile, encoding="utf-8") as f:
        records = json.load(f)
    tagged, summary = apply(records, as_of=as_of, stale_days=args.stale_days)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(tagged, f, ensure_ascii=False, indent=2)
        print("[OK] wrote", args.out)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    n_stale = sum(1 for r in tagged if r.get("stale") is True)
    for r in tagged:
        if r.get("stale") is True:
            print("STALE: %s [%s] %s" % (r.get("registry_id"), r.get("status"),
                                         r.get("stale_reason")), file=sys.stderr)
    if n_stale:
        print("[WARN] %d stale active trials excluded from active-competitor count"
              % n_stale, file=sys.stderr)


if __name__ == "__main__":
    main()
