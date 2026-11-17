#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
time_series.py / 时间序列异常检测（FAERS 报告数随时间的突变）

Answers: "has the reporting rate of this (drug, event) pair suddenly jumped?"
Useful for catching Weber-effect / new safety-signal upticks that a single
pooled disproportionality estimate would smooth over.

Pipeline:
  1. fetch_monthly_series() — ONE openFDA `receivedate` count facet for the
     drug&event pair, returning monthly {ym:YYYYMM, count}. (Reuses fetch_faers
     .count_field; no per-quarter loop, so rate-limit friendly.)
  2. to_quarterly() — aggregate months into quarters.
  3. detect_anomaly() — pure-stdlib CUSUM + rolling Z-score (window 4) +
     changepoint (Welch t-test split). No network.

All math is pure local; only fetch_monthly_series touches the network.
/ 纯本地统计；仅取数联网。
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_faers


def fetch_monthly_series(drug, event, field="patient.drug.medicinalproduct",
                         api_key=None, date_from=None, date_to=None, timeout=60,
                         fetch_mod=None, ev_field=None, date_field=None):
    """Return ordered list of {ym: 'YYYYMM', count: int} for the (drug, event)
    pair via a single openFDA receivedate count facet. Returns [] on failure.

    *fetch_mod* lets callers inject the (possibly shimmed) ``fetch_faers``
    module — e.g. in MAUDE device mode the global is rebound to
    ``DeviceEventShim``, whose ``count_field`` targets device/event.json. When
    omitted, the locally imported module is used (FAERS default, unchanged).
    *ev_field* selects the adverse-event dimension (reaction MedDRA PT for
    FAERS, event_type for MAUDE device events); *date_field* selects the date
    dimension (receivedate for FAERS, date_received for MAUDE).
    """
    mod = fetch_mod if fetch_mod is not None else fetch_faers
    if ev_field is None:
        ev_field = "patient.reaction.reactionmeddrapt"
    if date_field is None:
        date_field = "receivedate"
    clause = mod._date_clause(date_from, date_to, date_field=date_field)
    search = '%s:"%s" AND %s:"%s"%s' % (field, drug, ev_field, event, clause)
    try:
        rows = mod.count_field(search, date_field, api_key=api_key,
                               limit=1000, timeout=timeout)
    except Exception as e:  # noqa: BLE001
        print("[WARN] trend monthly fetch failed: %s" % e)
        return []
    out = []
    for r in rows:
        ym = r.get("term") or r.get("time")
        if not ym:
            continue
        out.append({"ym": str(ym), "count": int(r.get("count") or 0)})
    out.sort(key=lambda x: x["ym"])
    return out


def to_quarterly(monthly):
    """Aggregate monthly {ym,count} into quarterly {q:'YYYYQn', count}, sorted."""
    agg = {}
    for m in monthly:
        ym = m["ym"]
        if len(ym) < 6:
            continue
        y, mo = ym[:4], ym[4:6]
        try:
            q = (int(mo) - 1) // 3 + 1
        except ValueError:
            continue
        key = "%sQ%d" % (y, q)
        agg[key] = agg.get(key, 0) + m["count"]
    return [{"q": k, "count": agg[k]} for k in sorted(agg)]


def detect_anomaly(series):
    """Detect temporal anomalies in an ordered count series (oldest -> newest).

    Methods (all pure stdlib):
      - CUSUM: cumulative sum of (x - mean - k), k = 0.5*sd; flags if the running
        max exceeds 5*k (sustained upward shift).
      - Rolling Z (window 4): standardized deviation of the latest point vs the
        trailing window; flags if |z| > 3 (a single sharp spike).
      - Changepoint: brute-force split maximizing Welch t between the two halves;
        reports the split index, the pre/post mean lift, and whether |t| > 3.5.

    Returns a dict (no network). `anomaly_flag` is True if ANY method flags.
    """
    n = len(series)
    if n < 6:
        return {"n": n, "mean": None, "sd": None, "cusum_flag": False,
                "cusum_max": None, "rolling_z": None, "rolling_z_flag": False,
                "rolling_z_at": None, "changepoint_idx": None,
                "changepoint_lift": None, "anomaly_flag": False,
                "note": "insufficient points (<6) for stable detection"}
    vals = [float(x) for x in series]
    mean = sum(vals) / n
    sd = math.sqrt(sum((v - mean) ** 2 for v in vals) / n)
    k = 0.5 * sd if sd > 0 else 0.5

    # --- CUSUM ---
    cusum = 0.0
    cusum_max = 0.0
    for v in vals:
        cusum = max(0.0, cusum + (v - mean - k))
        cusum_max = max(cusum_max, cusum)
    cusum_flag = (k > 0) and (cusum_max > 5 * k)

    # --- Rolling Z (window 4) ---
    win = 4
    rz_max = None
    rz_at = None
    for i in range(win, n):
        w = vals[i - win:i]
        wm = sum(w) / len(w)
        wsd = math.sqrt(sum((x - wm) ** 2 for x in w) / len(w)) if len(w) > 1 else 0.0
        if wsd > 0:
            z = (vals[i] - wm) / wsd
            if rz_max is None or abs(z) > abs(rz_max):
                rz_max = z
                rz_at = i
    rz_flag = (rz_max is not None) and (abs(rz_max) > 3.0)

    # --- Changepoint (Welch t over all splits) ---
    best_stat = -1.0
    best_idx = None
    pre_mean = post_mean = None
    for i in range(2, n - 2):
        a = vals[:i]
        b = vals[i:]
        ma = sum(a) / len(a)
        mb = sum(b) / len(b)
        va = sum((x - ma) ** 2 for x in a) / len(a)
        vb = sum((x - mb) ** 2 for x in b) / len(b)
        se = math.sqrt(va / len(a) + vb / len(b))
        if se > 0:
            t = abs(mb - ma) / se
            if t > best_stat:
                best_stat = t
                best_idx = i
                pre_mean, post_mean = ma, mb
    lift = None
    if pre_mean is not None and pre_mean > 0:
        lift = post_mean / pre_mean - 1.0
    changepoint_flag = best_stat > 3.5

    anomaly_flag = bool(cusum_flag or rz_flag or changepoint_flag)
    return {
        "n": n, "mean": round(mean, 2), "sd": round(sd, 2),
        "cusum_flag": cusum_flag, "cusum_max": round(cusum_max, 2),
        "rolling_z": (round(rz_max, 2) if rz_max is not None else None),
        "rolling_z_flag": rz_flag, "rolling_z_at": rz_at,
        "changepoint_idx": best_idx,
        "changepoint_lift": (round(lift, 3) if lift is not None else None),
        "changepoint_t": (round(best_stat, 2) if best_stat >= 0 else None),
        "anomaly_flag": anomaly_flag,
    }


if __name__ == "__main__":
    # quick self-test (no network)
    import json
    demo = [5, 6, 5, 7, 6, 5, 8, 7, 6, 40, 42, 38, 45, 41, 39]
    print(json.dumps(detect_anomaly(demo), indent=2))
