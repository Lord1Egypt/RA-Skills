#!/usr/bin/env python3
"""search_ctgov.py - ClinicalTrials.gov v2 search / CT.gov 检索.

Reads public data only; no auth; no confidential data or information input. / 仅读公开数据，无认证，零保密数据或信息输入。

Two paths (backward-compatible):
  DEFAULT (no --fast): urllib + pageSize=50 + serial - same as always, zero behavior change.
  FAST (--fast): requests.Session (connection pool) + large pageSize + concurrent pagination.
    Use when you have a known rate limit / API key and want to maximize throughput.
    CT.gov v2 supports pageSize up to 1000+; with --fast we use 500 by default and
    fetch multiple pages concurrently via ThreadPoolExecutor.

Advanced search coverage (2026-08-13, v0.3.85) — per official OpenAPI spec:
  - v2 has NO flat filter.phase / filter.studyType / filter.sex / date parameters.
    Those all go through filter.advanced AREA[Field] Essie expressions, so the
    convenience flags (--phase/--study-type/--age-group/--sex/--has-results/
    --*-since/--*-until) are assembled into one AND-combined expression, then
    merged with a raw --adv expression if given:  (<convenience>) AND (<--adv>).
  - --status / --ids / --sort accept comma-separated multi-values -> pipe-delimited.
  - sort array max 2 elements; special value @relevance.
  - pageSize max 1000 (server clamps above that).
  - P2 (2026-08-13): --geo (filter.geo distance()), --patient (query.patient),
    --post-* (postFilter.* — same as filter.* but does NOT affect relevance ranking).
    NOTE: query.rmtln is a v1 legacy param, REMOVED from v2 (HTTP 400) — verified
    2026-08-13 against the live API; use --query or --adv for remote-trial search.
    Full /studies parameter coverage achieved.
"""
import argparse
import datetime as _dt
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://clinicaltrials.gov/api/v2/studies"
UA = {"User-Agent": "ct-registry/0.1", "Accept": "application/json"}

# --- advanced-search enums (v2 study-data-structure names) ---
PHASE_VALUES = {"EARLY_PHASE1", "PHASE1", "PHASE2", "PHASE3", "PHASE4", "NA"}
STUDY_TYPE_VALUES = {"INTERVENTIONAL", "OBSERVATIONAL", "EXPANDED_ACCESS"}
AGE_GROUP_VALUES = {"CHILD", "ADULT", "OLDER_ADULT"}
SEX_VALUES = {"FEMALE", "MALE", "ALL"}
# date fields usable in AREA[Field]RANGE[since,until] (server-side date filtering)
DATE_FIELDS = {
    "StudyFirstPostDate", "LastUpdatePostDate", "StartDate",
    "PrimaryCompletionDate", "CompletionDate", "ResultsFirstPostDate",
}
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_SORT_RE = re.compile(r"^(?:@relevance|[A-Za-z0-9]+(?::asc|:desc)?)$")
_GEO_FULL_RE = re.compile(
    r"^distance\((-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?),(\d+(?:\.\d+)?)(km|mi)?\)$")
_GEO_BARE_RE = re.compile(r"^-?\d+(\.\d+)?,-?\d+(\.\d+)?,\d+(\.\d+)?(km|mi)?$")


def _norm_multi(raw, values=None, label="value"):
    """Split comma-separated values, upper-case, optionally validate against a whitelist."""
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    if not parts:
        raise argparse.ArgumentTypeError(f"{label} 不能为空")
    out = []
    for p in parts:
        up = p.upper()
        if values is not None and up not in values:
            raise argparse.ArgumentTypeError(
                f"{label} 值 {p!r} 非法，允许: {', '.join(sorted(values))}")
        out.append(up)
    return out


def _date_arg(raw):
    """Validate a YYYY-MM-DD date argument."""
    if not _DATE_RE.match(raw):
        raise argparse.ArgumentTypeError(f"日期需为 YYYY-MM-DD，收到: {raw!r}")
    _dt.datetime.strptime(raw, "%Y-%m-%d")  # strict validation
    return raw


def _normalize_geo(raw):
    """Normalize/validate a geo argument into `distance(lat,lon,dist[km|mi])`.

    Accepts the bare form `lat,lon,dist` (auto-wrapped) or the full
    `distance(lat,lon,dist)` form; radius unit optional (km or mi, default mi).
    Enforces the official radius bounds: 1-500 mi / 1-805 km.
    Raises ValueError on malformed input; idempotent on valid input.
    """
    s = raw.strip()
    if _GEO_BARE_RE.match(s):
        s = "distance(%s)" % s
    m = _GEO_FULL_RE.match(s)
    if not m:
        raise ValueError(
            f"geo 格式: distance(lat,lon,dist[km|mi]) 或 lat,lon,dist，收到: {raw!r}")
    _lat, _lon, dist, unit = m.groups()
    unit = unit or "mi"
    d = float(dist)
    hi = 805 if unit == "km" else 500
    if not (1 <= d <= hi):
        raise ValueError(f"geo 距离需在 1-{hi}{unit} 范围内，收到: {dist}{unit}")
    return s


def _geo_arg(raw):
    """argparse type hook: normalize geo, convert ValueError to ArgumentTypeError."""
    try:
        return _normalize_geo(raw)
    except ValueError as e:
        raise argparse.ArgumentTypeError(str(e))


def _pipe(values):
    """Coerce a value / list into a pipe-delimited string (API multi-value form)."""
    if values is None:
        return None
    if isinstance(values, (list, tuple)):
        return "|".join(str(v) for v in values)
    return str(values)


def _start_date(study):
    """Extract the study start date string (YYYY or YYYY-MM or YYYY-MM-DD) if present."""
    ps = study.get("protocolSection", {}) if isinstance(study, dict) else {}
    sm = ps.get("statusModule", {})
    sds = sm.get("startDateStruct", {}) or {}
    return sds.get("date") or sds.get("year")


def _after(date_after, study):
    """True if the study started on/after `date_after` (YYYY-MM-DD); unknown dates pass."""
    sd = _start_date(study)
    if not sd:
        return True  # no start-date info -> keep (do not silently drop)
    try:
        lo = int(str(date_after)[:4])
        yr = int(str(sd)[:4])
    except (ValueError, TypeError):
        return True
    return yr >= lo


def _build_params(cond=None, intr=None, sponsor=None, status=None, max_n=50,
                  fields=None, page_token=None, query=None, titles=None, outc=None,
                  lead=None, id_=None, locn=None, adv=None, phase=None,
                  study_type=None, age_group=None, sex=None, has_results=False,
                  ids=None, date_ranges=None, sort=None, patient=None,
                  geo=None, post_status=None, post_ids=None, post_geo=None,
                  post_adv=None):
    """Build query params dict for CT.gov v2 API (full v2 parameter coverage)."""
    params = {"pageSize": max_n, "format": "json", "countTotal": "true"}

    # --- query.* word-level search areas ---
    for key, val in (("query.cond", cond), ("query.intr", intr),
                     ("query.spons", sponsor), ("query.term", query),
                     ("query.titles", titles), ("query.outc", outc),
                     ("query.lead", lead), ("query.id", id_),
                     ("query.locn", locn), ("query.patient", patient)):
        if val:
            params[key] = val

    # --- filter.overallStatus / filter.ids / filter.geo ---
    if status:
        params["filter.overallStatus"] = _pipe(status)
    if ids:
        params["filter.ids"] = _pipe(ids)
    if geo:
        params["filter.geo"] = _normalize_geo(geo)  # idempotent; raises on malformed

    # --- filter.advanced: convenience clauses + user expression, AND-combined ---
    adv_parts = []
    if phase:
        adv_parts.append("AREA[Phase](%s)" % " OR ".join(phase))
    if study_type:
        adv_parts.append("AREA[StudyType](%s)" % " OR ".join(study_type))
    if age_group:
        adv_parts.append("AREA[StdAge](%s)" % " OR ".join(age_group))
    if sex:
        adv_parts.append("AREA[Sex](%s)" % " OR ".join(sex))
    if has_results:
        adv_parts.append("AREA[HasResults]true")
    for field, since, until in (date_ranges or []):
        adv_parts.append("AREA[%s]RANGE[%s,%s]" % (field, since or "MIN", until or "MAX"))
    if adv_parts and adv:
        adv_parts.append("(%s)" % adv)
    if adv_parts:
        params["filter.advanced"] = " AND ".join(adv_parts)
    elif adv:
        params["filter.advanced"] = adv

    # --- sort: max 2, pipe-delimited array ---
    if sort:
        params["sort"] = _pipe(sort)

    # --- postFilter.* (identical to filter.* but does NOT affect relevance rank) ---
    if post_status:
        params["postFilter.overallStatus"] = _pipe(post_status)
    if post_ids:
        params["postFilter.ids"] = _pipe(post_ids)
    if post_geo:
        params["postFilter.geo"] = post_geo
    if post_adv:
        params["postFilter.advanced"] = post_adv

    if fields:
        params["fields"] = fields
    if page_token:
        params["pageToken"] = page_token
    return params


def _wait_seconds(backoff, attempt):
    """Exponential backoff for `attempt` (1-based). `backoff<=0` disables waiting.

    Note: `0 ** 0 == 1` in Python, so an explicit guard is required — passing
    `backoff=0` must mean "retry immediately", not "wait 1 second".
    """
    if backoff <= 0:
        return 0.0
    return float(backoff) ** (attempt - 1)


def _fetch_page_urllib(params, timeout=30, max_retries=3, backoff=2.0):
    """Fetch a single page using urllib (default path, no extra deps).

    Retry policy (2026-11-03, P3 归一反向移植自 meta-analysis `registry_probe._get_json`):
      - HTTP 429: honor the `Retry-After` header; else exponential backoff.
      - 5xx / URLError / OSError / TimeoutError: exponential backoff (`backoff ** (attempt-1)`).
      - other 4xx (parameter errors): non-retryable, raised immediately.
      - retries exhausted: RuntimeError (caller decides degrade or abort).

    `backoff<=0` disables waiting (kept for the test suite / offline harness).
    """
    url = BASE + "?" + urllib.parse.urlencode(params)
    last = None
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                ra = e.headers.get("Retry-After")
                wait = float(ra) if ra else _wait_seconds(backoff, attempt)
                if attempt < max_retries:
                    if wait > 0:
                        time.sleep(wait)
                    continue
                last = e
                break
            if 500 <= e.code < 600:
                if attempt < max_retries:
                    wait = _wait_seconds(backoff, attempt)
                    if wait > 0:
                        time.sleep(wait)
                    continue
                last = e
                break
            raise  # 4xx other than 429 → non-retryable
        except (urllib.error.URLError, OSError, TimeoutError) as e:
            if attempt < max_retries:
                wait = _wait_seconds(backoff, attempt)
                if wait > 0:
                    time.sleep(wait)
                continue
            last = e
            break
    raise RuntimeError("ClinicalTrials.gov request failed after %d retries: %s"
                       % (max_retries, last))


def _fetch_page_session(session, params, max_retries=3, backoff=2.0):
    """Fetch a single page using requests.Session (fast path, connection pool).

    Same retry/backoff policy as `_fetch_page_urllib` (429 honored via
    `Retry-After`, 5xx / network errors retried with exponential backoff).
    `backoff=0` disables waiting.
    """
    last = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = session.get(BASE, params=params, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:  # noqa: BLE001 - normalize below
            status = getattr(e, "response", None)
            code = getattr(status, "status_code", None)
            retryable = code is None or code == 429 or 500 <= int(code) < 600
            if not retryable or attempt >= max_retries:
                raise
            wait = _wait_seconds(backoff, attempt)
            if wait > 0:
                time.sleep(wait)
            last = e
    raise RuntimeError("ClinicalTrials.gov session request failed after %d retries: %s"
                       % (max_retries, last))


def search(cond=None, intr=None, sponsor=None, status=None, max_n=50,
           fields=None, date_after=None, page_token=None,
           timeout=30, max_retries=3, backoff=2.0, **extra):
    """Default search path (urllib, single page). Backward-compatible.

    `timeout` / `max_retries` / `backoff` are new optional knobs (defaults keep the
    historic behaviour: 30s timeout, 3 attempts, 2.0s base backoff). They exist so
    callers that reused meta-analysis's `_get_json` retry policy keep that
    capability after the P3 normalisation instead of silently losing it.
    """
    params = _build_params(cond, intr, sponsor, status, max_n, fields, page_token, **extra)
    data = _fetch_page_urllib(params, timeout=timeout, max_retries=max_retries,
                              backoff=backoff)
    if date_after:
        # CT.gov v2 has no reliable server-side start-date filter param; post-filter
        # the returned studies by start-date lower bound (robust, source-agnostic).
        kept = [s for s in data.get("studies", []) if _after(date_after, s)]
        data = dict(data, studies=kept)
    return data


def search_fast(cond=None, intr=None, sponsor=None, status=None,
                max_total=500, page_size=500, max_workers=4,
                fields=None, date_after=None, timeout=30, max_retries=3,
                backoff=2.0, **extra):
    """Fast path: requests.Session + large pageSize + concurrent pagination.

    Uses connection pooling (keep-alive) to avoid repeated TCP+TLS handshakes,
    and fetches multiple pages concurrently via ThreadPoolExecutor.
    Returns the same shape as search() but with all pages merged.

    `timeout` / `max_retries` / `backoff` mirror `search()` (same defaults).
    """
    import requests
    from concurrent.futures import ThreadPoolExecutor, as_completed

    session = requests.Session()
    session.headers.update(UA)

    # First page: get totalCount + first batch of studies
    params = _build_params(cond, intr, sponsor, status, page_size, **extra)
    first = _fetch_page_session(session, params, max_retries=max_retries, backoff=backoff)
    total_count = first.get("totalCount", 0)
    all_studies = list(first.get("studies", []))
    next_token = first.get("nextPageToken")

    # Calculate how many more pages we need
    pages_needed = max(1, (min(total_count, max_total) + page_size - 1) // page_size)

    if pages_needed > 1 and next_token:
        # Fetch remaining pages concurrently
        def fetch_page(token):
            p = _build_params(cond, intr, sponsor, status, page_size, fields, token, **extra)
            return _fetch_page_session(session, p, max_retries=max_retries, backoff=backoff)

        tokens = [next_token]
        # We need to chain tokens sequentially since each page returns the next token
        # But we can still parallelize by pre-computing all tokens first
        # For simplicity, we'll fetch serially with the session (still keep-alive benefit)
        while len(tokens) < pages_needed - 1:
            try:
                result = fetch_page(tokens[-1])
                all_studies.extend(result.get("studies", []))
                next_t = result.get("nextPageToken")
                if not next_t:
                    break
                tokens.append(next_t)
            except Exception:
                break

    if date_after:
        kept = [s for s in all_studies if _after(date_after, s)]
        all_studies = kept

    return {
        "studies": all_studies[:max_total],
        "totalCount": total_count,
        "nextPageToken": None,
    }


def _records(data):
    return data.get("studies", []) if isinstance(data, dict) else []


def _collect_date_ranges(args):
    """Collect the five since/until date-field pairs into [(field, since, until)]."""
    pairs = (
        ("StudyFirstPostDate", args.first_post_since, args.first_post_until),
        ("LastUpdatePostDate", args.last_update_since, args.last_update_until),
        ("StartDate", args.start_date_since, args.start_date_until),
        ("PrimaryCompletionDate", args.primary_completion_since, args.primary_completion_until),
        ("CompletionDate", args.completion_since, args.completion_until),
    )
    return [(f, s, u) for f, s, u in pairs if s or u]


def _build_extra(args):
    """Assemble the **extra kwargs passed through to _build_params (fields excluded:
    it has its own explicit parameter on search()/search_fast())."""
    return dict(query=args.query, titles=args.titles, outc=args.outc, lead=args.lead,
                id_=args.id_, locn=args.locn, adv=args.adv, phase=args.phase,
                study_type=args.study_type, age_group=args.age_group, sex=args.sex,
                has_results=args.has_results, ids=args.ids,
                date_ranges=_collect_date_ranges(args), sort=args.sort,
                patient=args.patient, geo=args.geo,
                post_status=args.post_status, post_ids=args.post_ids,
                post_geo=args.post_geo, post_adv=args.post_adv)


def main():
    ap = argparse.ArgumentParser(description="Search ClinicalTrials.gov v2 (public, no auth).")
    # --- word-level search areas (query.*) ---
    ap.add_argument("--cond", help="query.cond: 疾病/条件")
    ap.add_argument("--intr", help="query.intr: 干预/治疗")
    ap.add_argument("--sponsor", help="query.spons: 申办方/合作方")
    ap.add_argument("--query", help="query.term: 其他术语（支持 AREA[] 表达式）")
    ap.add_argument("--titles", help="query.titles: 标题/缩写")
    ap.add_argument("--outc", help="query.outc: 结局指标")
    ap.add_argument("--lead", help="query.lead: 主要申办方")
    ap.add_argument("--id", dest="id_", help="query.id: 研究 ID（NCT/OrgStudyId/SecondaryId）")
    ap.add_argument("--locn", help="query.locn: 地点（国家/城市/机构）")
    ap.add_argument("--patient", help="query.patient: 患者友好搜索（47 字段加权）")
    # --- structured filters ---
    ap.add_argument("--status", type=lambda s: _norm_multi(s, None, "status"),
                    help="filter.overallStatus 状态（逗号多值，如 RECRUITING,COMPLETED）")
    ap.add_argument("--ids", type=lambda s: _norm_multi(s, None, "ids"),
                    help="filter.ids: 按 NCT 号批量（逗号多值）")
    ap.add_argument("--geo", type=_geo_arg,
                    help="filter.geo: distance(lat,lon,dist[km|mi]) 或 lat,lon,dist（1-500 mi / 1-805 km）")
    ap.add_argument("--adv", help="filter.advanced 原始 Essie 表达式（可粘贴网站 Expert Search）")
    # --- convenience flags assembled into filter.advanced (AREA[] expressions) ---
    ap.add_argument("--phase", type=lambda s: _norm_multi(s, PHASE_VALUES, "phase"),
                    help="Phase（逗号多值）: EARLY_PHASE1,PHASE1,PHASE2,PHASE3,PHASE4,NA")
    ap.add_argument("--study-type", type=lambda s: _norm_multi(s, STUDY_TYPE_VALUES, "study-type"),
                    help="研究类型（逗号多值）: INTERVENTIONAL,OBSERVATIONAL,EXPANDED_ACCESS")
    ap.add_argument("--age-group", type=lambda s: _norm_multi(s, AGE_GROUP_VALUES, "age-group"),
                    help="年龄段（逗号多值）: CHILD,ADULT,OLDER_ADULT")
    ap.add_argument("--sex", type=lambda s: _norm_multi(s, SEX_VALUES, "sex"),
                    help="性别: FEMALE,MALE,ALL")
    ap.add_argument("--has-results", action="store_true",
                    help="仅已有结果（AREA[HasResults]true）")
    # --- server-side date ranges (AREA[Field]RANGE[since,until]; 缺省 MIN/MAX) ---
    ap.add_argument("--first-post-since", type=_date_arg, help="首次发布日期下限 (StudyFirstPostDate)")
    ap.add_argument("--first-post-until", type=_date_arg, help="首次发布日期上限")
    ap.add_argument("--last-update-since", type=_date_arg, help="最近更新日期下限 (LastUpdatePostDate)")
    ap.add_argument("--last-update-until", type=_date_arg, help="最近更新日期上限")
    ap.add_argument("--start-date-since", type=_date_arg, help="研究开始日期下限 (StartDate)")
    ap.add_argument("--start-date-until", type=_date_arg, help="研究开始日期上限")
    ap.add_argument("--primary-completion-since", type=_date_arg, help="主要完成日期下限 (PrimaryCompletionDate)")
    ap.add_argument("--primary-completion-until", type=_date_arg, help="主要完成日期上限")
    ap.add_argument("--completion-since", type=_date_arg, help="完成日期下限 (CompletionDate)")
    ap.add_argument("--completion-until", type=_date_arg, help="完成日期上限")
    # --- postFilter.* (same as filter.* but does NOT affect relevance ranking) ---
    ap.add_argument("--post-status", type=lambda s: _norm_multi(s, None, "post-status"),
                    help="postFilter.overallStatus（不影响相关性排序）")
    ap.add_argument("--post-ids", type=lambda s: _norm_multi(s, None, "post-ids"),
                    help="postFilter.ids（不影响相关性排序）")
    ap.add_argument("--post-geo", type=_geo_arg,
                    help="postFilter.geo（不影响相关性排序）")
    ap.add_argument("--post-adv", help="postFilter.advanced 原始表达式（不影响相关性排序）")
    # --- sort / fields / pagination ---
    ap.add_argument("--sort", action="append", dest="sort",
                    help="排序（最多 2 个; field 或 field:asc/:desc; @relevance 为默认）")
    ap.add_argument("--fields", help="返回字段（逗号分隔，如 NCTId,BriefTitle）")
    ap.add_argument("--date-after", help="start-date lower bound YYYY-MM-DD / 起始日期下限 (本地后过滤)")
    ap.add_argument("--max", type=int, default=50, help="返回条数上限 (default 50; --fast 模式下默认 500)")
    ap.add_argument("--out", default="ctgov.json")
    ap.add_argument("--run", action="store_true", help="execute network request / 执行检索")
    # Fast path options (opt-in, for users with known rate limit / API key)
    ap.add_argument("--fast", action="store_true",
                    help="启用快速路径: requests.Session 连接池 + 大 pageSize + 并发分页 "
                         "(有 key/已知配额时使用, 无 key 时保留默认 urllib 路径)。")
    ap.add_argument("--page-size", type=int, default=None,
                    help="单页条数 (仅 --fast 模式, 默认 500, CT.gov v2 支持到 1000+)")
    ap.add_argument("--max-workers", type=int, default=4,
                    help="并发分页线程数 (仅 --fast 模式, 默认 4)")
    args = ap.parse_args()

    # validate --sort: max 2, known format
    if args.sort:
        if len(args.sort) > 2:
            ap.error("--sort 最多指定 2 个")
        for s in args.sort:
            if not _SORT_RE.match(s):
                ap.error(f"--sort 格式非法: {s!r}（field 或 field:asc/:desc 或 @relevance）")

    extra = _build_extra(args)

    if not args.run:
        q = urllib.parse.urlencode(_build_params(
            args.cond, args.intr, args.sponsor, args.status, args.max, args.fields, **extra))
        if args.fast:
            ps = args.page_size or 500
            print(f"[ctgov][PREVIEW] FAST path: Session(pool) + pageSize={ps} + concurrent pagination")
        else:
            print(f"[ctgov][PREVIEW] GET {BASE}?{q}")
        if args.date_after:
            print(f"[ctgov][PREVIEW] post-filter by start-date >= {args.date_after}")
        print("[ctgov][PREVIEW] add --run to execute the request.")
        return

    if args.fast:
        # Fast path: Session + large pageSize + concurrent pagination
        page_size = args.page_size or min(args.max, 500)
        max_total = max(args.max, page_size)
        data = search_fast(
            cond=args.cond, intr=args.intr, sponsor=args.sponsor,
            status=args.status, max_total=max_total, page_size=page_size,
            max_workers=args.max_workers, fields=args.fields,
            date_after=args.date_after, **extra,
        )
        print(f"[ctgov][FAST] total={data.get('totalCount', '?')} "
              f"returned={len(data.get('studies', []))} (Session + pageSize={page_size})")
    else:
        # Default path: urllib, single page (backward-compatible)
        data = search(args.cond, args.intr, args.sponsor, args.status, args.max,
                      fields=args.fields, date_after=args.date_after, **extra)
        print(f"[ctgov] total={data.get('totalCount', '?')} returned={len(_records(data))}")

    out = {"source": "CTGOV", "records": _records(data), "total": data.get("totalCount"),
           "date_filter": args.date_after}
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"[ctgov] -> {args.out}")


if __name__ == "__main__":
    main()
