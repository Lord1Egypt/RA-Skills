#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fetch_reports.py / FAERS 个案翻页下载

Downloads individual FAERS adverse-event reports via the openFDA public REST API
by paginating `limit/skip`. Hard cap HARD_CAP=10000 to avoid over-consuming the
free (keyless) quota. No confidential data input; reads only public data.

Outputs (all per-page checkpointed where applicable):
  - raw JSON array of full reports                 (--out,  e.g. faers_reports_raw.json)  [written once at end]
  - per-page JSONL checkpoint (resume-safe)         (<out>.jsonl, append each page)
  - flattened CSV of key fields, one row per report (--out-csv, e.g. faers_reports.csv)   [appended each page]
  - Excel workbook (.xlsx) via xlsxwriter           (--out-xlsx, e.g. faers_reports.xlsx)  [written once at end]

Reuses BASE / _q / _date_clause / _get_json from fetch_faers.py (retry + backoff).

Resilience: after EACH page is fetched it is written to disk immediately (CSV appended;
JSONL checkpoint appended; progress printed). If the run is interrupted, the partial CSV /
JSONL already on disk is preserved — no page already saved is lost. The final consolidated
JSON array + XLSX workbook are written once at completion.

Note: downloaded reports are the FIRST N in API return order (NOT a random sample),
so local tallies carry a selection bias. The fast (`--fast`) mode instead uses openFDA
`count` facet queries over the FULL matched population (no bias, seconds) — but age is
NOT count-able via the API, so the age block is omitted there. Country IS facetable
(`primarysourcecountry.exact`) and is included in both modes.

Parallel: `--parallel N` splits [0, n_target) into N contiguous windows downloaded
by N threads concurrently (overlaps the ~50-60s per-page server latency). Wall-clock
time roughly divides by N for large-result drugs. Per-worker CSV/JSONL checkpoints are
merged into the final files at completion; the consolidated JSON + XLSX are written once.
"""
import argparse
import csv
import json
import os
import sys
import time
import threading

try:
    import requests
except ImportError:
    requests = None

try:
    import xlsxwriter
except ImportError:
    xlsxwriter = None

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_faers import BASE, _q, _date_clause, _get_json, count_field  # reuse retry + date + count
from export_xlsx import export_workbook, prepare_dists_from_facets  # xlsx + fast aggregator

HARD_CAP = 10000  # never exceed: free-quota protection
# openFDA per-request `limit` max is 1000, but 100 keeps a single page safely
# under the 120s timeout even for large-result drugs (e.g. 100+ MB pages).
PAGE = 100

# Fast/count mode: openFDA `count` facet fields per dists key.
# Verified field paths: country/indication need `.exact`; age is NOT count-able
# (404) so it is intentionally omitted → fast mode renders 8 of the 9 blocks.
FAST_FACETS = [
    ("serious",     "serious"),
    ("sex",         "patient.patientsex"),
    ("report_type", "reporttype"),
    ("country",     "primarysourcecountry.exact"),
    ("year",        "receivedate"),
    ("reaction",    "patient.reaction.reactionmeddrapt.exact"),
    ("indication",  "patient.drug.drugindication.exact"),
    ("drug_role",   "patient.drug.drugcharacterization"),
]


def _extract(report):
    """Flatten one FAERS report into a small dict of case-level fields."""
    out = {}
    out["safetyreportid"] = report.get("safetyreportid")
    out["safetyreportversion"] = report.get("safetyreportversion")
    out["receivedate"] = report.get("receivedate")
    out["serious"] = report.get("serious")
    out["reporttype"] = report.get("reporttype")
    out["primarysourcecountry"] = report.get("primarysourcecountry")
    out["occurcountry"] = report.get("occurcountry")
    out["reportercountry"] = report.get("reportercountry")
    patient = report.get("patient") or {}
    out["patientsex"] = patient.get("patientsex")
    out["patientage"] = patient.get("patientage")
    out["patientageunit"] = patient.get("patientageunit")
    reactions = patient.get("reaction") or []
    out["reaction_pts"] = "; ".join(
        [r.get("reactionmeddrapt", "") for r in reactions if r.get("reactionmeddrapt")]
    )
    drugs = patient.get("drug") or []
    names, chars, inds = [], [], []
    for d in drugs:
        nm = d.get("medicinalproduct")
        if nm:
            names.append(nm)
        ch = d.get("drugcharacterization")
        if ch is not None:
            chars.append(str(ch))
        ind = d.get("drugindication")
        if ind:
            inds.append(ind)
    # `drug` (medicinalproduct names) is the SAME semantic as the interactive
    # template's 合并用药 column; xlsx_sheets._norm_case prefers it over the
    # characterization/indication fallbacks → the two Excel templates converge.
    out["drug"] = "; ".join(names)
    out["drug_characterizations"] = "; ".join(chars)  # 1=怀疑药 2=合并药 3=相互作用
    out["drug_indications"] = "; ".join(inds)
    return out


def _write_csv_append(rows, path, first=False):
    """Append rows to CSV; write header only on first call. Enables per-page checkpoint."""
    if not rows:
        return
    cols = list(rows[0].keys())
    mode = "w" if first else "a"
    with open(path, mode, encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        if first:
            w.writeheader()
        for r in rows:
            w.writerow(r)


def _write_jsonl_append(reports, path):
    """Append each raw report as one JSON line. Per-page checkpoint (resume-safe)."""
    with open(path, "a", encoding="utf-8") as f:
        for r in reports:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def _download_window(search, api_key, start, end, worker_id, csv_path, jsonl_path):
    """Download reports in [start, end). Per-page checkpoint to csv_path/jsonl_path.
    Returns (reports_list, extracted_list). openFDA `skip` is absolute within the full
    result set, so windows are disjoint and ordered; concatenating worker outputs in
    window order yields a skip-ascending sequence."""
    reports, extracted = [], []
    skip = start
    page_idx = 0
    first = True
    while skip < end:
        take = min(PAGE, end - skip)
        j = _get_json(_q(search, limit=take, skip=skip, api_key=api_key),
                      api_key=api_key)
        batch = j.get("results", [])
        if not batch:
            break
        reports.extend(batch)
        new_ext = [_extract(r) for r in batch]
        extracted.extend(new_ext)
        skip += len(batch)
        page_idx += 1
        if csv_path:
            _write_csv_append(new_ext, csv_path, first=first)
            first = False
        if jsonl_path:
            _write_jsonl_append(batch, jsonl_path)
        print("[INFO][w%d] window %d/%d (got %d) page %d — checkpoint saved"
              % (worker_id, skip, end, len(reports), page_idx))
        if skip >= end:
            break
        time.sleep(0.5)  # rate-limit politeness between pages
    return reports, extracted


def _merge_csv_parts(part_paths, final_csv):
    """Concatenate part CSVs, keeping only the first header row."""
    with open(final_csv, "w", encoding="utf-8-sig", newline="") as out:
        wrote_header = False
        for p in part_paths:
            if not os.path.exists(p):
                continue
            with open(p, "r", encoding="utf-8-sig", newline="") as f:
                lines = f.read().splitlines()
            if not lines:
                continue
            if not wrote_header:
                out.write(lines[0] + "\n")
                wrote_header = True
            for ln in lines[1:]:
                out.write(ln + "\n")


def _merge_files_cat(part_paths, final_path):
    """Plain concatenation of text files (used for JSONL merge)."""
    with open(final_path, "w", encoding="utf-8") as out:
        for p in part_paths:
            if not os.path.exists(p):
                continue
            with open(p, "r", encoding="utf-8") as f:
                out.write(f.read())


# xlsx rendering moved to export_xlsx.export_workbook (README + 9 charts + Summary).


def fetch_facets(drug, date_from=None, date_to=None, api_key=None,
                 field="patient.drug.medicinalproduct"):
    """Fast mode: run openFDA `count` facet queries for the 8 dimensions.
    Returns (total_matching, {key: [{"term","count"}, ...]}). Age omitted (404)."""
    clause = _date_clause(date_from, date_to)
    search = '%s:"%s"%s' % (field, drug, clause)
    j0 = _get_json(_q(search, limit=1, api_key=api_key), api_key=api_key)
    total = int(j0.get("meta", {}).get("results", {}).get("total", 0))
    facets = {}
    for key, fld in FAST_FACETS:
        # openFDA `count` rejects limit>=1000 with 403, so cap at 100.
        # (categorical fields have ≤4 distinct values; receivedate ignores limit
        # and returns all daily buckets, which we aggregate to years.)
        lim = 12 if key in ("country", "indication") else (15 if key == "reaction" else 100)
        res = count_field(search, fld, api_key=api_key, limit=lim)
        facets[key] = res
        print("[INFO] facet %-12s -> %d buckets" % (key, len(res)))
    return total, facets


def render_summary_text(dists, total, drug, date_from=None, date_to=None):
    """Render the count-facet summary as plain text and print to stdout.

    This is the DEFAULT retrieval deliverable (context summary): fast (seconds,
    full matched population) and NON-biased. The user reads it inline; the Excel
    workbook is generated only on a later explicit request (--out-xlsx)."""
    k = dists.get("kpis", {})
    L = []
    L.append("=" * 58)
    L.append("  FAERS 安全性检索汇总 / FAERS Safety Summary")
    L.append("=" * 58)
    L.append("药物 Drug        : %s" % drug)
    if date_from or date_to:
        L.append("时间窗 Window     : %s ~ %s" % (date_from or "...", date_to or "..."))
    L.append("匹配报告总数     : %s   (分析基数 = 全量匹配)" % total)
    L.append("严重报告         : %s  (%.1f%%)" % (k.get("n_serious", 0), k.get("serious_rate", 0) * 100))
    L.append("性别             : 男 %.1f%% / 女 %.1f%%" % (k.get("male_pct", 0) * 100, k.get("female_pct", 0) * 100))
    L.append("年份跨度         : %s" % k.get("year_span", "-"))
    L.append("-" * 58)

    def _block(title, items, n=None, fmt="%-14s %8d"):
        L.append(title)
        for lbl, cnt in (items[:n] if n else items):
            L.append("   " + fmt % (lbl, cnt))

    _block("严重性 / Seriousness:", dists.get("serious", []))
    _block("性别 / Sex:", dists.get("sex", []))
    _block("报告类型 / Report type:", dists.get("report_type", []))
    _block("来源国家 Top5 / Countries:", dists.get("country", [])[:5])
    yr = dists.get("year", [])
    if yr:
        tail = [yr[-1]] if len(yr) > 3 else []
        _block("逐年趋势 / Annual (首3 + 末1):", yr[:3] + tail, fmt="%-8s %8d")
    _block("Top 反应 Top5 / Reactions:", dists.get("reaction", [])[:5], fmt="%-32s %8d")
    _block("Top 指征 Top5 / Indications:", dists.get("indication", [])[:5], fmt="%-32s %8d")
    _block("药物角色 / Drug role:", dists.get("drug_role", []))
    L.append("-" * 58)
    L.append("WARNING 以上为分布概览，未做信号检测 (PRR/ROR/IC)，非因果结论。")
    L.append("NEXT    -> 要 Excel 汇总页: 加 --out-xlsx <file.xlsx> (秒级, 复用本次缓存)")
    L.append("NEXT    -> 要个案级数据(含年龄): 加 --run --max N [--parallel K]")
    L.append("=" * 58)
    print("\n".join(L))


def save_summary_cache(path, drug, date_from, date_to, total, facets):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"drug": drug, "date_from": date_from, "date_to": date_to,
                       "total": total, "facets": facets}, f, ensure_ascii=False)
        print("[INFO] summary cache -> %s" % path)
    except Exception as e:
        print("[WARN] cache write failed: %s" % e)


def load_summary_cache(path, drug, date_from, date_to):
    try:
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
        if d.get("drug") != drug or d.get("date_from") != date_from \
                or d.get("date_to") != date_to:
            return None
        return d
    except Exception:
        return None


def fetch_reports(drug, date_from=None, date_to=None, max_records=1000,
                  field="patient.drug.medicinalproduct", api_key=None,
                  run=False, out=None, out_csv=None, out_xlsx=None,
                  lang="auto", parallel=1, present=True, cache_path=None):
    """Three-state retrieval entry point (v0.1.18).

    - PRESENT (default, no --run / no --out-xlsx): fetch openFDA count facets
      (seconds, FULL matched population, no selection bias), print a compact
      summary to stdout, and stash a JSON cache so a later `--out-xlsx` reuses
      the results WITHOUT re-hitting the network.
    - OUT_XLSX (--out-xlsx without --run): build the Summary Excel workbook from
      the facets; prefers the cache when drug+window match (no re-network).
    - RUN (--run): paginate-DOWNLOAD case-level reports (DETAIL mode). With
      --out-xlsx it also builds the 9-chart detail workbook from downloaded cases.

    NOTE: the former `--fast` flag is now a no-op alias — present/summary already
    use count facets over the full population by default.
    """
    if requests is None:
        raise RuntimeError("requests not installed: pip install requests")
    parallel = max(1, int(parallel))

    # ── No --run: PRESENT or OUT_XLSX (count facets over the FULL matched population) ──
    if not run:
        # OUT_XLSX: build the Summary workbook; prefer cache (no re-network)
        if out_xlsx is not None:
            cached = load_summary_cache(cache_path, drug, date_from, date_to) if cache_path else None
            if cached is not None:
                total = cached["total"]
                facets = cached["facets"]
                print("[INFO] cache hit -> reuse facets (no network)")
            else:
                total, facets = fetch_facets(drug, date_from, date_to, api_key, field)
                if cache_path:
                    save_summary_cache(cache_path, drug, date_from, date_to, total, facets)
            dists = prepare_dists_from_facets(facets, total)
            meta = {"drug": drug, "field": field, "date_from": date_from,
                    "date_to": date_to, "total_matching": total,
                    "hard_cap": HARD_CAP, "mode": "fast"}
            export_workbook([], out_xlsx, meta=meta, dists=dists, lang=lang)
            print("[OK] wrote", out_xlsx, "(fast / count mode, summary workbook)")
            return {"mode": "summary_xlsx", "drug": drug, "total_matching": total}

        # PRESENT (default retrieval): print summary to context + cache, no Excel
        total, facets = fetch_facets(drug, date_from, date_to, api_key, field)
        dists = prepare_dists_from_facets(facets, total)
        render_summary_text(dists, total, drug, date_from, date_to)
        if cache_path:
            save_summary_cache(cache_path, drug, date_from, date_to, total, facets)
        return {"mode": "present", "drug": drug, "total_matching": total,
                "facets": facets,
                "note": "Summary printed to console; cache saved for --out-xlsx reuse."}

    # ── RUN / DETAIL mode: paginate-download cases (unchanged core logic) ──
    cap = min(int(max_records), HARD_CAP)
    if int(max_records) > HARD_CAP:
        print("[WARN] requested %d exceeds hard cap %d; clamped to %d"
              % (max_records, HARD_CAP, HARD_CAP))

    clause = _date_clause(date_from, date_to)
    search = '%s:"%s"%s' % (field, drug, clause)

    # total available (1 lightweight call)
    j0 = _get_json(_q(search, limit=1, api_key=api_key), api_key=api_key)
    total = int(j0.get("meta", {}).get("results", {}).get("total", 0))
    n_target = min(total, cap)
    print("[INFO] total matching=%d, will download=%d (cap=%d)"
          % (total, n_target, cap))

    jsonl_path = (os.path.splitext(out)[0] + ".jsonl") if out else None

    # ── Parallel paging: split [0, n_target) into N contiguous windows ──
    # Each worker downloads its window via _download_window (which checkpoints
    # per page). For large-result drugs each `limit=100` page costs ~50-60s
    # server-side, so N threads overlap that latency and roughly divide wall
    # time by N. openFDA `skip` is absolute, so windows are disjoint & ordered.
    stem = os.path.splitext(out)[0] if out else (
        os.path.splitext(out_csv)[0] if out_csv else "faers_reports")
    if parallel <= 1:
        windows = [(0, n_target)]
        w_csv = [out_csv]
        w_jsonl = [jsonl_path]
    else:
        print("[INFO] parallel download: %d workers over [0, %d)"
              % (parallel, n_target))
        step = (n_target + parallel - 1) // parallel  # ceil division
        windows = [(i * step, min(n_target, (i + 1) * step))
                   for i in range(parallel)]
        w_csv = [(stem + (".part%d.csv" % i)) if out_csv else None
                 for i in range(parallel)]
        w_jsonl = [(stem + (".part%d.jsonl" % i)) if jsonl_path else None
                   for i in range(parallel)]

    results = [None] * len(windows)

    def _run(wi, wstart, wend, wcsv, wjsonl):
        results[wi] = _download_window(search, api_key, wstart, wend,
                                       wi, wcsv, wjsonl)

    threads = []
    for wi, (ws, we) in enumerate(windows):
        t = threading.Thread(target=_run, args=(wi, ws, we, w_csv[wi], w_jsonl[wi]),
                             daemon=True)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    # merge worker outputs in window order (each window is skip-ascending)
    reports, extracted = [], []
    for wi in range(len(windows)):
        r, e = results[wi] or ([], [])
        reports.extend(r)
        extracted.extend(e)

    # merge per-worker checkpoint files into the final CSV/JSONL (parallel>1 only)
    if parallel > 1:
        if out_csv:
            _merge_csv_parts([p for p in w_csv if p], out_csv)
        if jsonl_path:
            _merge_files_cat([p for p in w_jsonl if p], jsonl_path)
        for p in (list(w_csv) + list(w_jsonl)):  # tidy part files
            if p and os.path.exists(p):
                try:
                    os.remove(p)
                except OSError:
                    pass

    result = {
        "source": "FAERS",
        "api": "openFDA drug/event.json",
        "drug": drug,
        "field": field,
        "date_from": date_from,
        "date_to": date_to,
        "total_matching": total,
        "downloaded": len(reports),
        "hard_cap": HARD_CAP,
        "parallel": parallel,
        "note": ("First N reports in API return order (NOT a random sample). "
                 "Age / country recoverable locally from case-level data. "
                 "Parallel download splits [0, n_target) across %d worker(s)." % parallel),
        "reports": reports,
    }
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("[OK] wrote", out)
    if out_xlsx:
        meta = {"drug": drug, "field": field, "date_from": date_from,
                "date_to": date_to, "total_matching": total, "hard_cap": HARD_CAP,
                "parallel": parallel}
        export_workbook(extracted, out_xlsx, meta=meta, lang=lang)
        print("[OK] wrote", out_xlsx)
    if out_csv:
        tag = "" if parallel <= 1 else (" (merged from %d workers)" % parallel)
        print("[OK] wrote", out_csv + tag)
    return result


def main():
    ap = argparse.ArgumentParser(
        description="FAERS safety retrieval. DEFAULT (no --run / no --out-xlsx) = print a "
                    "count-facet summary to the console + cache it (seconds, full matched "
                    "population). --out-xlsx = build the Summary Excel from the facets "
                    "(reuses cache if present). --run = paginate-DOWNLOAD case reports.")
    ap.add_argument("--drug", required=True)
    ap.add_argument("--field", default="patient.drug.medicinalproduct")
    ap.add_argument("--date-from", help="filter receivedate >= YYYYMMDD")
    ap.add_argument("--date-to", help="filter receivedate <= YYYYMMDD")
    ap.add_argument("--max", type=int, default=1000,
                    help="max reports to download in DETAIL mode (--run); hard cap 10000")
    ap.add_argument("--api-key", help="openFDA API key (raises quota to 120k/day). "
                                        "Also read from env OPENFDA_API_KEY or skill-root .env (git-ignored). "
                                        "Optional: keyless anonymous quota works for low-volume use.")
    ap.add_argument("--run", action="store_true",
                    help="paginate-DOWNLOAD case reports (DETAIL mode). With --out-xlsx "
                         "builds the 9-chart detail workbook from downloaded cases.")
    ap.add_argument("--out", help="raw reports JSON path (DETAIL mode only; written at end)")
    ap.add_argument("--out-csv", help="flattened CSV path (DETAIL mode; appended each page)")
    ap.add_argument("--out-xlsx", help="Excel workbook path (.xlsx). WITHOUT --run -> fast "
                    "Summary workbook from count facets (seconds, full population, reuses "
                    "cache if present). WITH --run -> detail workbook (9 charts).")
    ap.add_argument("--lang", default="auto", choices=["auto", "zh", "en"],
                    help="Excel UI language (auto = zh in zh env)")
    ap.add_argument("--parallel", type=int, default=1,
                    help="DETAIL mode only: parallel download workers (e.g. 2); roughly "
                         "divides wall-clock by N. Ignored otherwise.")
    ap.add_argument("--fast", action="store_true",
                    help="DEPRECATED no-op: present/summary already use count facets over "
                         "the full matched population by default. Kept for backward compat.")
    args = ap.parse_args()

    # ── mode resolution (v0.1.18) ──
    # --run            -> DETAIL download (case reports)
    # --out-xlsx (no run) -> Summary Excel from facets (cache reuse)
    # default (neither)   -> PRESENT: print summary + cache, no Excel
    cache_path = "faers_summary_cache.json"
    fetch_reports(args.drug, args.date_from, args.date_to, args.max,
                  args.field, args.api_key, run=args.run, out=args.out,
                  out_csv=args.out_csv, out_xlsx=args.out_xlsx,
                  lang=args.lang, parallel=args.parallel,
                  present=True, cache_path=cache_path)


if __name__ == "__main__":
    main()
