#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fetch_faers.py / FAERS 数据抓取

Reads FDA FAERS public adverse-event data via the openFDA public REST API
(https://api.fda.gov/drug/event.json). No API key required for low-volume use
(rate-limited); an optional --api-key raises the quota. Zero confidential data or information input;
reads only public data. / 经 openFDA 公开 REST API 读取 FDA FAERS 公开不良事件数据。
无需密钥（低频可用，限流）；可选 --api-key 提升配额。零保密数据或信息输入，仅读公开数据。

2x2 table components obtained for disproportionality:
  a = drug AND event pair count
  drug_total = a + b
  event_total = a + c
  N (grand_total) = all FAERS reports
  b = drug_total - a ; c = event_total - a ; d = N - a - b - c
"""
import argparse
import base64
import json
import os
import sys

try:
    import requests
except ImportError:
    requests = None

BASE = "https://api.fda.gov/drug/event.json"
# MAUDE（医疗器械不良事件）端点：与 FAERS 同为 openFDA 公开、免密钥来源。
# 注意：器械事件的「药品」维度对应「器械」维度（patient.device.*）。
BASE_DEVICE = "https://api.fda.gov/device/event.json"

# 数据源注册表：端点 + 默认维度字段 + 展示名。新增来源在此登记，默认 faers 行为不变。
# field  = 检索主体维度（药物名 / 器械品牌名）
# ev_field = 不良事件维度（FAERS 用 reaction MedDRA PT；MAUDE 用 event_type 分类，
#           因 device/event.json 无 patient.reaction，事件以 Malfunction/Injury/Death/
#           Other 等 event_type 表达）
SOURCE_DEFAULTS = {
    "faers": {
        "base": BASE,
        "field": "patient.drug.medicinalproduct",
        "ev_field": "patient.reaction.reactionmeddrapt",
        "date_field": "receivedate",
        "label": "FAERS",
        "api_label": "openFDA drug/event.json",
    },
    "maude": {
        "base": BASE_DEVICE,
        "field": "device.brand_name",
        "ev_field": "event_type",
        "date_field": "date_received",
        "label": "MAUDE (device)",
        "api_label": "openFDA device/event.json",
    },
}

# Skill root (parent of the scripts/ dir). Used to locate a local .env that
# holds the openFDA key WITHOUT shipping it inside the published package.
_SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DOTENV = os.path.join(_SKILL_ROOT, ".env")

# OpenFDA key obfuscation (ct-base §5, private-credential best practice).
# A skill-root .env may store either a plaintext key OR an `obf:`-prefixed
# XOR+base64 obfuscated blob. `resolve_api_key` auto-detects the prefix and
# decodes the latter; plaintext values pass through unchanged. Obfuscation is
# NOT real encryption — it only prevents the plaintext key from being caught by
# naive scanners or accidentally copied when a .env is moved around.
_OBF_KEY = b"ct-safety-openfda-obf-v1-8c2f"


def _deobfuscate(val):
    """Decode an `obf:`-prefixed XOR+base64 blob; return *val* unchanged otherwise."""
    if not val or not val.startswith("obf:"):
        return val
    try:
        raw = base64.b64decode(val[len("obf:"):].strip())
        dec = bytes(c ^ _OBF_KEY[i % len(_OBF_KEY)] for i, c in enumerate(raw))
        return dec.decode("utf-8")
    except Exception:
        return val


def resolve_api_key(cli_key, dotenv_path=None):
    """Resolve an openFDA API key. Priority (highest first):

    1. CLI ``--api-key`` (explicit, always wins)
    2. Environment variable ``OPENFDA_API_KEY``
    3. A ``.env`` file at the skill root (``OPENFDA_API_KEY=...``)

    Returns ``None`` when no key is available — keyless anonymous access still
    works for low-volume use. A skill-root ``.env`` is git-ignored (and listed
    in ``.clawhubignore``), so a user's key never leaks into a packaged skill.
    """
    if cli_key:
        return cli_key
    env = os.environ.get("OPENFDA_API_KEY")
    if env:
        return env
    if dotenv_path is None:
        dotenv_path = _DOTENV
    if dotenv_path and os.path.isfile(dotenv_path):
        try:
            with open(dotenv_path, "r", encoding="utf-8") as fh:
                for line in fh:
                    s = line.strip()
                    if not s or s.startswith("#"):
                        continue
                    if s.startswith("OPENFDA_API_KEY="):
                        val = s.split("=", 1)[1].strip().strip('"').strip("'")
                        if val:
                            return _deobfuscate(val)
        except Exception:
            pass
    return None


def _q(search, count=None, limit=1, api_key=None, skip=None):
    params = {"search": search, "limit": limit}
    if count:
        params["count"] = count
    if skip is not None:
        params["skip"] = skip
    api_key = resolve_api_key(api_key, _DOTENV)
    if api_key:
        params["api_key"] = api_key
    return params


def _date_clause(date_from=None, date_to=None, date_field="receivedate"):
    """Build an openFDA date range clause (YYYYMMDD). Empty if no bounds.

    *date_field* selects the date dimension: FAERS uses ``receivedate``, while
    MAUDE device events use ``date_received`` (``receivedate`` does not exist in
    device/event.json and makes the whole search 404).
    """
    if not date_from and not date_to:
        return ""
    lo = date_from or "19000101"
    hi = date_to or "20991231"
    return " AND %s:[%s TO %s]" % (date_field, lo, hi)


# openFDA occasionally returns 404 "NOT_FOUND / No matches found!" for VALID
# queries that contain multi-word phrases (transient parser hiccup, not a real
# empty result). Retry with backoff on transient statuses; do NOT retry on 400
# (genuine syntax error).
_RETRY_STATUSES = {404, 429, 500, 502, 503, 504}


def _get_json(params, retries=3, delay=1.5, api_key=None, timeout=120, base=None):
    """requests.get against BASE (or *base*) with transient-error retry.

    Returns parsed JSON. *base* lets a caller target another openFDA endpoint
    (e.g. device/event.json for MAUDE); defaults to the FAERS BASE so existing
    behaviour is unchanged.

    timeout defaults to 120s: a single FAERS `limit=100` page for a large-result
    drug (e.g. candesartan, 30k+ reports) can take 50-60s to respond, so a 60s
    timeout was a critical edge that triggered needless retries. 120s leaves
    comfortable headroom.
    """
    api_key = resolve_api_key(api_key, _DOTENV)
    if api_key:
        params = dict(params)
        params["api_key"] = api_key
    last = None
    url = base or BASE
    for attempt in range(1, retries + 1):
        r = requests.get(url, params=params, timeout=timeout)
        if r.status_code == 200:
            return r.json()
        last = r
        if r.status_code not in _RETRY_STATUSES or attempt == retries:
            r.raise_for_status()
        import time
        time.sleep(delay * attempt)
    last.raise_for_status()


def fetch_counts(drug, event=None, field=None, top=10, api_key=None, run=False,
                 out=None, date_from=None, date_to=None, timeout=120, retries=3,
                 source="faers"):
    """取某个 openFDA 源（默认 faers）的药品-事件计数。

    source='maude' 时改用 device/event.json（器械不良事件）且默认维度字段切换为
    patient.device.brand_name；返回结构与 FAERS 完全同构，故下游 2x2 不均衡计算
    （disproportionality.compute）可直接复用，无需改动。
    """
    if requests is None:
        raise RuntimeError("requests not installed: pip install requests")
    cfg = SOURCE_DEFAULTS.get(source)
    if cfg is None:
        raise ValueError("fetch_counts: unknown source %r (allowed: %s)"
                         % (source, sorted(SOURCE_DEFAULTS)))
    base = cfg["base"]
    if field is None:
        field = cfg["field"]
    if not run:
        print("[PREVIEW] would query openFDA %s for drug=%r event=%r (use --run to execute)"
              % (cfg["label"], drug, event))
        return None

    date_field = cfg.get("date_field", "receivedate")
    ev_field_cfg = cfg.get("ev_field", "patient.reaction.reactionmeddrapt")
    clause = _date_clause(date_from, date_to, date_field=date_field)

    def total(search, timeout=timeout, retries=retries):
        j = _get_json(_q(search, limit=1, api_key=api_key), timeout=timeout,
                      retries=retries, base=base)
        return int(j.get("meta", {}).get("results", {}).get("total", 0))

    def top_events(search, timeout=timeout, retries=retries):
        j = _get_json(_q(search, count=ev_field_cfg + ".exact",
                         limit=top, api_key=api_key), timeout=timeout,
                      retries=retries, base=base)
        return [{"term": x.get("term"), "count": x.get("count")}
                for x in j.get("results", [])]

    drug_term = '%s:"%s"%s' % (field, drug, clause)
    drug_total = total(drug_term)
    top_ev = top_events(drug_term)
    # grand total scoped to the same date window so the 2x2 denominator is consistent
    grand_total = total("*:*" + clause, timeout=timeout, retries=retries)

    result = {
        "source": cfg["label"],
        "api": cfg["api_label"],
        "drug": drug,
        "field": field,
        "date_from": date_from,
        "date_to": date_to,
        "drug_total": drug_total,
        "grand_total": grand_total,
        "top_events": top_ev,
        "event": None,
        "counts": None,
    }

    if event:
        ev_field = cfg.get("ev_field", "patient.reaction.reactionmeddrapt")
        pair_search = '%s AND %s:"%s"' % (drug_term, ev_field, event)
        pair = total(pair_search)
        event_total = total('%s:"%s"%s' % (ev_field, event, clause))
        a = pair
        b = drug_total - a
        c = event_total - a
        d = grand_total - a - b - c
        result["event"] = event
        result["event_total"] = event_total
        result["counts"] = {"a": a, "b": b, "c": c, "d": d,
                            "drug_total": drug_total, "event_total": event_total,
                            "grand_total": grand_total}

    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("[OK] wrote", out)
    return result


def query_total(search, api_key=None, timeout=120, retries=3, source="faers"):
    """Module-level single openFDA total-count query. Used by the multi-event
    sweep to fetch only the pair (a) and event-total (c+a) counts per event,
    reusing the drug-total / grand-total already obtained once up front — this
    avoids the redundant top_events / repeated grand-total queries inside
    fetch_counts and keeps the per-event request count (and thus wall-clock)
    low enough to survive rate-limiting without stalling the whole run.

    *source* selects the openFDA endpoint (default "faers" -> drug/event.json;
    "maude" -> device/event.json) so the same helper works for both FAERS and
    MAUDE without callers hard-coding an endpoint. Existing behaviour (drug
    endpoint) is preserved when *source* is omitted.
    """
    cfg = SOURCE_DEFAULTS.get(source)
    base = cfg["base"] if cfg is not None else BASE
    j = _get_json(_q(search, limit=1, api_key=api_key), timeout=timeout,
                  retries=retries, base=base)
    return int(j.get("meta", {}).get("results", {}).get("total", 0))


def count_field(search, field, api_key=None, limit=1000, timeout=60, source="faers"):
    """Run a single openFDA `count` facet query; return [{term, count}, ...].

    A failing facet (transient 404/500) must NOT abort the whole fast run, so
    errors are swallowed and an empty list is returned. NOTE: openFDA `count`
    ignores `limit` for some date fields (e.g. receivedate) and returns all
    buckets — the caller aggregates as needed.

    *source* selects the openFDA endpoint (default "faers" -> drug/event.json;
    "maude" -> device/event.json) so MAUDE trend/verify reuse this helper with
    the correct endpoint.
    """
    cfg = SOURCE_DEFAULTS.get(source)
    base = cfg["base"] if cfg is not None else BASE
    try:
        j = _get_json(_q(search, count=field, limit=limit, api_key=api_key),
                      api_key=api_key, timeout=timeout, base=base)
        # openFDA count results use `term` for most fields but `time` for
        # receivedate — normalize both to `term` so callers can rely on one key.
        return [{"term": x.get("term") or x.get("time"), "count": x.get("count")}
                for x in j.get("results", [])]
    except Exception as e:
        # swallow but surface, so a single bad facet doesn't silently empty a block
        print("[WARN] count facet %r failed: %s" % (field, e))
        return []


def fetch_case_reports(drug, event=None, field="patient.drug.medicinalproduct",
                       n=20, api_key=None, run=False, out=None,
                       date_from=None, date_to=None, timeout=120, retries=3,
                       source="faers"):
    """Individual case safety reports for a drug (optionally drug-event) pair.

    Returns a list of case dicts: {safetyreportid, safetyreportversion,
    receivedate, seriousness, outcome, reaction_pt[], drug[], patientsex,
    patientonsetage, patientonsetageunit, occurcountry, reportercountry}.
    Enables per-case traceability (the R14 signal chain in ct-pipeline).
    Public FAERS only; no confidential data.
    Use --run (or run=True) to execute the network request.

    P1-A (2026-08-29): the demographic + version fields are extracted so that
    `faers_dedup.py` can collapse follow-up report versions and flag suspected
    duplicate cases. FAERS is well known to contain the same case multiple
    times (initial + follow-up submissions, and the same case reported by
    manufacturer and consumer), which inflates raw case counts. These are
    extracted from the response already being fetched -- no extra request,
    no extra network traffic.

    *source* selects the openFDA endpoint (default "faers" -> drug/event.json;
    "maude" -> device/event.json) so MAUDE device case retrieval hits the
    device library rather than the drug library.
    """
    if requests is None:
        raise RuntimeError("requests not installed: pip install requests")
    cfg = SOURCE_DEFAULTS.get(source)
    base = cfg["base"] if cfg is not None else BASE
    src_label = (cfg["label"] if cfg is not None else "FAERS")
    if not run:
        print("[PREVIEW] would fetch up to %d case reports for drug=%r event=%r (use --run)"
              % (n, drug, event))
        return None
    clause = _date_clause(date_from, date_to,
                          date_field=cfg.get("date_field", "receivedate"))
    ev_field = cfg.get("ev_field", "patient.reaction.reactionmeddrapt")
    drug_term = '%s:"%s"' % (field, drug)
    if event:
        search = '%s AND %s:"%s"%s' % (drug_term, ev_field, event, clause)
    else:
        search = drug_term + clause
    # HARD LIMIT (single page, no pagination): this helper issues ONE request,
    # so anything above PAGE_MAX is silently dropped. Warn loudly instead of
    # truncating without a word, and point at the paginating path for large
    # pulls (mirrors fetch_reports.py's clamp warning, §13.7 "触顶行为").
    PAGE_MAX = 100
    limit = min(int(n), PAGE_MAX)
    if int(n) > PAGE_MAX:
        print("[WARN] requested %d case reports, but this single-page helper "
              "caps at %d — truncated to %d. For larger pulls use the "
              "paginating path instead: scripts/fetch_reports.py --max <n> "
              "(hard cap %d, ~60s per 100-record page)."
              % (n, PAGE_MAX, PAGE_MAX, 10000))
    j = _get_json(_q(search, limit=limit, api_key=api_key), timeout=timeout,
                  retries=retries, base=base)
    cases = []
    for rec in j.get("results", []):
        pat = rec.get("patient", {}) or {}
        reacts = pat.get("reaction", []) or []
        drugs = pat.get("drug", []) or []
        src = rec.get("primarysource", {}) or {}
        cases.append({
            "safetyreportid": rec.get("safetyreportid"),
            # P1-A: version + demographics feed the local de-duplication layer.
            "safetyreportversion": rec.get("safetyreportversion"),
            "receivedate": rec.get("receivedate"),
            "seriousness": rec.get("serious") or rec.get("seriousness"),
            "outcome": pat.get("patientoutcome") or pat.get("outcome"),
            "reaction_pt": [x.get("reactionmeddrapt") for x in reacts],
            "drug": [d.get("medicinalproduct") or d.get("patientdrugname") for d in drugs],
            "patientsex": pat.get("patientsex"),
            "patientonsetage": pat.get("patientonsetage"),
            "patientonsetageunit": pat.get("patientonsetageunit"),
            "occurcountry": rec.get("occurcountry"),
            "reportercountry": src.get("reportercountry"),
        })
    result = {"source": src_label, "drug": drug, "event": event,
              "n_fetched": len(cases), "cases": cases}
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("[OK] wrote", out)
    return result


def main():
    ap = argparse.ArgumentParser(description="Fetch FAERS counts via openFDA (public).")
    ap.add_argument("--drug", required=True)
    ap.add_argument("--event", help="specific MedDRA PT to pair with the drug")
    ap.add_argument("--field", default="patient.drug.medicinalproduct")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--api-key", help="openFDA API key (raises quota to 120k/day). "
                                        "Also read from env OPENFDA_API_KEY or skill-root .env (git-ignored). "
                                        "Optional: keyless anonymous quota works for low-volume use.")
    ap.add_argument("--date-from", help="filter receivedate >= YYYYMMDD (e.g. 20200101)")
    ap.add_argument("--date-to", help="filter receivedate <= YYYYMMDD (e.g. 20261231)")
    ap.add_argument("--run", action="store_true", help="execute network request")
    ap.add_argument("--out", help="output JSON path")
    ap.add_argument("--case-level", type=int, default=0,
                    help="fetch up to N individual case safety reports (safetyreportid + reaction + outcome) for traceability")
    args = ap.parse_args()

    if args.case_level:
        case_out = (args.out.replace(".json", "_cases.json")
                    if args.out else "faers_cases.json")
        cr = fetch_case_reports(args.drug, args.event, args.field, args.case_level,
                                args.api_key, True, case_out,
                                args.date_from, args.date_to)
        if cr and not args.out:
            print(json.dumps(cr, ensure_ascii=False, indent=2))

    res = fetch_counts(args.drug, args.event, args.field, args.top,
                       args.api_key, args.run, args.out,
                       args.date_from, args.date_to)
    if res and not args.out:
        print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
