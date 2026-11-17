#!/usr/bin/env python3
"""normalize.py - Unified normalization across registries / 多源统一归一化.

Input: per-source raw JSON files (each carries `source` + `records`).
Output: unified trial schema list. / 输出统一 trial schema 列表。
"""
import argparse
import html
import json
import re
import sys


# --- Homepage URL resolver (req4: always emit a full, clickable URL) -------------
# ICTRP records arrive with a *relative* link (e.g. `Trial2.aspx?TrialID=NCT...`).
# Resolve every registry_id to its native portal's canonical URL so the report
# never ships a broken relative link. Unknown shapes fall back to the WHO ICTRP
# portal (which works for any mirrored record via its TrialID).
_PORTAL = [
    (r'^NCT\d+$', lambda r: f"https://clinicaltrials.gov/study/{r}"),
    (r'^CHICT', lambda r: f"https://www.chictr.org.cn/showProj.html?proj={r}"),
    (r'^DRKS', lambda r: f"https://drks.de/drks_web/navigate.php?navigation_id=trials&trial_id={r}"),
    (r'^CTIS', lambda r: f"https://www.clinicaltrialsregister.eu/ctr-search/trial/{r}"),
    (r'JRCT', lambda r: f"https://jrct.niph.go.jp/latest-detail/{r.split('-',1)[1] if r.upper().startswith('JPRN-') else r}"),
    (r'^ACTRN', lambda r: f"https://www.anzctr.org.au/{r}.aspx"),
    (r'^KCT', lambda r: f"https://cris.nih.go.kr/cris/search/detail.do?seq={r[3:]}"),
    (r'^ISRCTN', lambda r: f"https://www.isrctn.com/{r}"),
]


def resolve_homepage(registry_id, fallback=None):
    """Return a full canonical homepage URL for a registry_id, or `fallback`.

    If `registry_id` already looks like a full URL it is returned as-is. Known
    registry prefixes (NCT / ChiCTR / DRKS / CTIS / jRCT / ACTRN / ISRCTN) map to
    their native portal; everything else falls back to the WHO ICTRP portal using
    the id as TrialID (always valid for mirrored records).
    """
    rid = (registry_id or "").strip()
    if not rid:
        return fallback
    if rid.lower().startswith(("http://", "https://")):
        return rid
    for pat, fn in _PORTAL:
        if re.search(pat, rid, re.IGNORECASE):
            try:
                return fn(rid)
            except Exception:
                break
    if fallback and str(fallback).lower().startswith(("http://", "https://")):
        return fallback
    return f"https://trialsearch.who.int/Trial2.aspx?TrialID={rid}"


def _first(x):
    if isinstance(x, list) and x:
        return x[0]
    return x if isinstance(x, str) else None


def _clean(v):
    """Unescape HTML entities (e.g. CDE's &nbsp;) and collapse whitespace."""
    if not isinstance(v, str):
        return v
    v = html.unescape(v)
    v = v.replace("\xa0", " ").strip()
    return re.sub(r"\s+", " ", v) if v else v


def _to_int(v):
    """Best-effort integer parse for sample-size / count fields ('80', '1,200')."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return int(v)
    m = re.search(r"\d[\d,]*", str(v))
    return int(m.group(0).replace(",", "")) if m else None


def _smod_date(v):
    """Read a date out of a CT.gov statusModule field, tolerating shape drift.

    ClinicalTrials.gov v2 returns most date fields as ``{"date": "YYYY-MM-DD",
    "type": "ACTUAL"}`` but has been observed returning ``lastKnownStatus`` as a
    bare enum string (``"RECRUITING"``). Older code assumed dict-only and raised
    ``AttributeError: 'str' object has no attribute 'get'``, aborting the whole
    normalize pass (and therefore the workbench run). A bare string is a status
    value, not a date, so it yields None here — use ``_smod_status`` for it.
    """
    if isinstance(v, dict):
        return v.get("date")
    if isinstance(v, str) and len(v) >= 4 and v[:4].isdigit():
        return v  # rare: plain ISO date string
    return None


def _smod_status(v):
    """Return the status enum when the field is a plain string (v2 shape drift)."""
    return v if isinstance(v, str) else None


def norm_ctgov(study):
    ps = study.get("protocolSection", {})
    im = ps.get("identificationModule", {})
    sm = ps.get("statusModule", {})
    dm = ps.get("designModule", {})
    cm = ps.get("conditionsModule", {})
    aim = ps.get("armsInterventionsModule", {})
    scm = ps.get("sponsorCollaboratorsModule", {})
    clm = ps.get("contactsLocationsModule", {})
    interventions = [i.get("name") for i in aim.get("interventions", [])]
    # De-duplicate country names: CT.gov lists one country per location, so a
    # multi-site trial would otherwise repeat "United States" once per US site.
    # Preserve first-seen order via dict.fromkeys (Py3.7+).
    _raw_countries = [l.get("country") for l in clm.get("locations", []) if l.get("country")]
    countries = list(dict.fromkeys(_raw_countries))
    return {
        "source": "CTGOV",
        "registry_id": im.get("nctId"),
        "title": _clean(im.get("briefTitle")),
        "status": sm.get("overallStatus"),
        # upgrade D (stale-trial detection): CT.gov exposes the real
        # last-update date in statusModule.lastUpdatePosted; also capture the
        # results-first-posted date when present. Feeds stale_check.
        # v2 real field is lastUpdatePostDateStruct (lastUpdatePosted never
        # existed -> this used to be permanently None, breaking stale_check).
        "last_update_posted": _smod_date(sm.get("lastUpdatePostDateStruct"))
                              or _smod_date(sm.get("lastUpdatePosted"))
                              or _smod_date(sm.get("lastKnownStatus")),
        # v2 may hand back a plain enum string here; keep the date when dict,
        # otherwise fall back to the status value so nothing is lost.
        "status_last_known": _smod_date(sm.get("lastKnownStatus"))
                             or _smod_status(sm.get("lastKnownStatus")),
        "results_first_posted": (sm.get("resultsFirstPosted") or {}).get("date"),
        "phase": _first(dm.get("phases")) if dm.get("phases") else None,
        "conditions": [_clean(c) for c in cm.get("conditions", [])],
        "interventions": [_clean(i) for i in interventions],
        "sponsor": _clean((scm.get("leadSponsor") or {}).get("name")),
        "start_date": (sm.get("startDateStruct") or {}).get("date"),
        "primary_completion_date": (sm.get("primaryCompletionDateStruct") or {}).get("date"),
        "countries": countries,
        "enrollment": (dm.get("enrollmentInfo") or {}).get("enrollmentCount"),
        "drug": _first(interventions),
        "url": f"https://clinicaltrials.gov/study/{im.get('nctId')}",
        "documents": study.get("documents") or [],
    }


def _phase_from_text(text):
    """Infer a CT.gov-style phase string from a trial title (CDE LIST shape has
    no 试验分期 field). Returns e.g. 'PHASE 3' / 'PHASE 1/PHASE 2' or None.

    Handles Chinese (I/II/III/IV 期, full-width Ⅰ–Ⅳ) and English
    (Phase I/II/III/IV) combined forms. Heuristic only — callers must flag it.
    """
    if not text:
        return None
    s = text
    # normalise full-width roman numerals + spacing
    s = s.replace("Ⅰ", "I").replace("Ⅱ", "II").replace("Ⅲ", "III").replace("Ⅳ", "IV")
    s = re.sub(r"phase\s*", "phase ", s, flags=re.IGNORECASE)
    res = None
    # combined forms first (avoid partial match)
    combos = [
        (r"i\s*/\s*ii\s*期|phase\s*i\s*/\s*ii\b", "PHASE 1/PHASE 2"),
        (r"ii\s*/\s*iii\s*期|phase\s*ii\s*/\s*iii\b", "PHASE 2/PHASE 3"),
        (r"iii\s*/\s*iv\s*期|phase\s*iii\s*/\s*iv\b", "PHASE 3/PHASE 4"),
        (r"i\s*/\s*iii\s*期", "PHASE 1/PHASE 3"),
    ]
    for pat, val in combos:
        if re.search(pat, s, re.IGNORECASE):
            return val
    # single forms (order: higher first so 'III' wins over 'I' substring)
    singles = [
        (r"iv\s*期|phase\s*iv\b|\biv期", "PHASE 4"),
        (r"iii\s*期|phase\s*iii\b|\biii期", "PHASE 3"),
        (r"ii\s*期|phase\s*ii\b|\bii期", "PHASE 2"),
        (r"i\s*期|phase\s*i\b|\bi期", "PHASE 1"),
    ]
    for pat, val in singles:
        if re.search(pat, s, re.IGNORECASE):
            return val
    return res


# ── R10: cross-source phase canonicalisation ────────────────────────────────
# Every registry spells the same phase differently: CT.gov "PHASE 3" /
# EU CTR "Phase 3" / CDE "III期" / ISRCTN "Phase III" / DRKS "phase 3".
# Passing these through raw fragmented `phase_dist` into one bucket per
# spelling, which silently broke the skill's headline deliverable (phase
# landscape). canon_phase() folds them onto the internal CT.gov-style form
# ("PHASE 3", "PHASE 1/PHASE 2", "EARLY PHASE 1", "NOT APPLICABLE").
# Unrecognised values are returned trimmed-but-unchanged (never destroy info).
_ROMAN = {"i": 1, "ii": 2, "iii": 3, "iv": 4}
_PHASE_NA = {"na", "n/a", "not applicable", "nap", "none", "不适用", "无", "不详",
             "未说明", "未知", "unknown"}


def canon_phase(value):
    """Fold a registry-specific phase string onto the internal canonical form."""
    if value is None:
        return None
    s = str(value).strip()
    if not s:
        return None
    # full-width roman numerals -> ASCII
    for _fw, _ascii in (("Ⅰ", "I"), ("Ⅱ", "II"), ("Ⅲ", "III"), ("Ⅳ", "IV")):
        s = s.replace(_fw, _ascii)
    low = s.lower().strip()
    if low in _PHASE_NA:
        return "NOT APPLICABLE"
    if re.search(r"early\s*[-_ ]?\s*phase\s*[-_ ]?1|^0\s*期$|^phase\s*0$", low):
        return "EARLY PHASE 1"
    # strip the noise words so only the numerals/separators remain
    core = re.sub(r"phase|期|试验|临床|clinical|trial|study", " ", low)
    core = re.sub(r"[^ivx0-9/,、\-\s]", " ", core)
    nums = []
    for tok in re.findall(r"[ivx]+|\d+", core):
        n = _ROMAN.get(tok) if tok.isalpha() else (int(tok) if tok.isdigit() else None)
        if n is not None and 1 <= n <= 4 and n not in nums:
            nums.append(n)
    if not nums:
        return s  # unrecognised -> preserve original (e.g. "其他")
    nums.sort()
    return "/".join(f"PHASE {n}" for n in nums)


# --- Sponsor grouping key ------------------------------------------------
# Same disease as phase: one sponsor is written a different way in every
# registry ("Akeso" / "Akeso, Inc." / "AKESO BIOPHARMA CO., LTD."), so
# `top_sponsors` fragmented into one bucket per spelling and the headline
# competitor ranking was meaningless. sponsor_key() produces a GROUPING KEY
# only -- the human-readable name is never overwritten, callers pick a
# display label from the raw strings inside each group.
#
# Deliberately CONSERVATIVE: it strips legal-entity suffixes and punctuation
# but does NOT strip descriptive words, so "Akeso" and "Akeso Biopharma"
# stay apart. Over-merging distinct companies is worse than under-merging.
_LEGAL_SUFFIX = (
    r"co\.?,?\s*ltd\.?", r"co\.?,?\s*limited", r"company\s+limited", r"limited",
    r"ltd\.?", r"inc\.?", r"incorporated", r"llc", r"l\.l\.c\.", r"plc",
    r"corp\.?", r"corporation", r"gmbh", r"ag", r"a\.?g\.?", r"s\.?a\.?s?\.?",
    r"n\.?v\.?", r"b\.?v\.?", r"a/s", r"aps", r"pty", r"kk", r"k\.k\.",
    r"co\.?", r"company", r"holdings?", r"group",
)
_LEGAL_SUFFIX_RE = re.compile(
    r"(?:[\s,\.]|^)(?:" + "|".join(_LEGAL_SUFFIX) + r")(?=[\s,\.]|$)", re.IGNORECASE)
_CN_SUFFIX_RE = re.compile(
    r"(?:股份)?(?:有限)?(?:责任)?公司$|集团$|控股$")


def sponsor_key(value):
    """Return a conservative grouping key for a sponsor name (not a display name)."""
    if value is None:
        return None
    s = str(value).strip()
    if not s:
        return None
    # full-width punctuation/space -> ASCII so CJK-typed names line up
    s = s.translate({0x3000: 32, 0xFF0C: 44, 0xFF0E: 46, 0xFF08: 40, 0xFF09: 41,
                     0xFF1A: 58, 0xFF0F: 47, 0xFF0D: 45})
    prev = None
    while prev != s:                      # peel nested suffixes: "Co., Ltd."
        prev = s
        s = _LEGAL_SUFFIX_RE.sub(" ", s).strip(" ,.-")
        s = _CN_SUFFIX_RE.sub("", s).strip(" ,.-")
    s = re.sub(r"[\s,\.\-_/&'\"()]+", " ", s).strip().lower()
    return s or None


# --- Status canonicalisation --------------------------------------------
# Third headline distribution hit by the same cross-source spelling problem:
# CT.gov "RECRUITING" / ISRCTN "Recruiting" / DRKS "recruiting" / ChiCTR
# "招募中" / CDE "进行中（招募中）" all mean the same thing but produced one
# bucket each, so "how many competitor trials are still enrolling" — the
# question the landscape report exists to answer — was unanswerable.
#
# CONSERVATIVE by design: this folds SYNONYMOUS SPELLINGS only. It never
# infers semantics that the source did not state (EU CTR "Ongoing" does not
# say whether enrolment is open, so it keeps its own ONGOING bucket rather
# than being forced into ACTIVE_NOT_RECRUITING). Unrecognised values are
# returned unchanged.
_STATUS_RULES = (
    ("NOT_YET_RECRUITING", (r"not\s*yet\s*recruit", r"尚未招募", r"^pending$",
                            r"未开始", r"not\s*yet\s*open")),
    ("ACTIVE_NOT_RECRUITING", (r"active[\s,_-]*not[\s_-]*recruit",
                               r"^not\s*recruiting$", r"不再招募", r"停止招募",
                               r"进行中[（(]?不招募")),
    ("RECRUITING", (r"^recruiting$", r"^open", r"招募中", r"正在招募",
                    r"enrolling\s*by\s*invitation", r"recruiting\s*ongoing")),
    ("COMPLETED", (r"^complete", r"已完成", r"recruiting\s*complete",
                   r"follow[\s-]*up\s*complete", r"^finished")),
    ("TERMINATED", (r"^terminat", r"^stopped", r"终止", r"提前终止", r"^halted")),
    ("SUSPENDED", (r"^suspend", r"暂停")),
    ("WITHDRAWN", (r"^withdraw", r"撤回", r"撤销", r"已撤回")),
    ("ONGOING", (r"^ongoing$", r"^进行中$")),
    ("UNKNOWN", (r"^unknown", r"^未知$", r"status\s*unknown", r"^no\s*longer\s*available$")),
)
_STATUS_COMPILED = tuple(
    (canon, tuple(re.compile(p, re.IGNORECASE) for p in pats))
    for canon, pats in _STATUS_RULES)


def canon_status(value):
    """Fold a registry-specific status string onto a canonical enum value."""
    if value is None:
        return None
    s = str(value).strip()
    if not s:
        return None
    probe = re.sub(r"[\s_]+", " ", s.replace("_", " ")).strip()
    for canon, pats in _STATUS_COMPILED:
        for p in pats:
            if p.search(probe):
                return canon
    return s  # unrecognised (e.g. EU "Authorised") -> preserve verbatim


def norm_cde(t):
    # CDE records come from the external Coze workflow. Field names are Chinese in the
    # workflow output. TWO shapes must both be handled:
    #   * LIST shape (search/combined/multi_keyword): 登记号 / 药物名称 / 适应症 /
    #     试验状态 / 试验通俗题目 / project_id  (summary only -- no sponsor/phase).
    #   * DETAIL shape (mode=detail, 65 fields): 登记号 / 申请人名称 / 试验分期 /
    #     试验专业题目 / 试验通俗题目 / 实际入组总人数 / 首次公示信息日期 / 入选标准 /
    #     排除标准 / 试验药 / 对照药 / 主要终点指标 / ... / project_id.
    # WHO-style keys may also appear when CDE is served through the UNIFIED endpoint
    # (公共标题 / 招募状态 / Main ID / 项目ID / health_condition / ...). Keep a tolerant
    # mapping (list OR detail) and retain a raw copy so nothing is silently dropped.
    reg_id = (t.get("登记号") or t.get("nctNumber") or t.get("regno")
              or t.get("registration_no") or t.get("Main ID") or t.get("main_id")
              or t.get("项目ID") or t.get("project_id") or t.get("source_id"))
    title = (t.get("试验通俗题目") or t.get("试验专业题目")
             or t.get("popularTitle") or t.get("title")
             or t.get("公共标题") or t.get("public_title") or t.get("who_title"))
    drug = (t.get("药物名称") or t.get("试验药") or t.get("drugName") or t.get("drug"))
    indication = (t.get("适应症") or t.get("indication")
                  or t.get("健康状况") or t.get("health_condition"))
    status = (t.get("试验状态") or t.get("testStatus") or t.get("status")
              or t.get("招募状态") or t.get("recruitment_status"))
    # Detail-only fields (sponsor/phase/enrollment/start) -- present ONLY in detail shape.
    sponsor = (t.get("申请人名称") or t.get("申办者") or t.get("sponsor")
               or t.get("appliers"))
    phase = (t.get("试验分期") or t.get("phase"))
    enrollment = _to_int(t.get("实际入组总人数") or t.get("enrollment"))
    start_date = (t.get("首次公示信息日期") or t.get("firstPosted")
                  or t.get("start_date"))
    # Detail-only clinical fields (tolerant: absent in LIST shape -> None).
    inclusion = t.get("入选标准") or t.get("inclusion")
    exclusion = t.get("排除标准") or t.get("exclusion")
    primary_outcome = t.get("主要终点指标") or t.get("primary_outcome")
    secondary_outcome = t.get("次要终点指标") or t.get("secondary_outcome")
    comparator = t.get("对照药") or t.get("comparator")
    study_type = (t.get("研究类型") or t.get("试验设计") or t.get("study_type"))
    age_min = t.get("最小年龄") or t.get("age_min")
    age_max = t.get("最大年龄") or t.get("age_max")
    gender = t.get("性别") or t.get("gender")
    # CDE public detail page is behind SafeDog WAF; the workflow returns NO attachment
    # URLs (verified against cde_detail.json: 0 http(s) links, 0 附件/下载 fields). So we
    # surface a registration-number lookup link as the homepage and leave `documents`
    # empty -- actual PDFs must be downloaded manually from the CDE site.
    url = (f"https://www.chinadrugtrials.org.cn/clinicaltrials.prosearch.dhtml"
           f"?pro=y&keyword={reg_id}" if reg_id else None)
    # Conditions: CDE indications are Chinese (e.g. "EGFR突变非小细胞肺癌").
    # Append an English alias so downstream English-scoped matching
    # (competitor_discovery._same_condition uses "non-small cell lung cancer")
    # can recognise China trials as same-condition competitors.
    base_conds = [indication] if indication else list(t.get("conditions") or [])
    _CDE_COND_ALIAS = {
        "非小细胞肺癌": "non-small cell lung cancer",
        "非小细胞肺": "non-small cell lung cancer",
        "nsclc": "non-small cell lung cancer",
        "肺腺癌": "lung adenocarcinoma",
    }
    norm_conds = list(base_conds)
    blob = (indication or "").lower()
    for _zh, _en in _CDE_COND_ALIAS.items():
        if _zh.lower() in blob and _en not in [c.lower() for c in norm_conds]:
            norm_conds.append(_en)
    # R2: phase inference from title. CDE LIST shape carries no 试验分期 field
    # (only DETAIL shape does). As a lightweight, zero-extra-call fallback, infer
    # the phase from the trial's popular title (I/II/III/IV 期 or Phase I/II/III/IV).
    # Explicitly flagged `phase_inferred=True` so downstream can disclose that the
    # phase is heuristic, not source-reported.
    raw_phase = _clean(phase)
    phase_out = raw_phase
    phase_inferred = False
    if not raw_phase:
        inferred = _phase_from_text(title or "")
        if inferred:
            phase_out, phase_inferred = inferred, True
    # R9: explicit per-record phase provenance (field-level reliability).
    #   source   -> phase reported by the registry (DETAIL shape 试验分期)
    #   inferred -> no source phase; heuristically derived from the title
    #   dna      -> no phase at all (LIST shape + non-informative title)
    if raw_phase:
        phase_provenance = "source"
    elif phase_inferred:
        phase_provenance = "inferred"
    else:
        phase_provenance = "dna"
    return {
        "source": "CDE",
        "registry_id": reg_id,
        "project_id": t.get("project_id"),
        "title": _clean(title),
        "status": _clean(status),
        "phase": phase_out,
        "phase_inferred": phase_inferred,
        "phase_provenance": phase_provenance,
        "sponsor_present": bool(_clean(sponsor)),
        "study_type": _clean(study_type),
        "conditions": norm_conds,
        "interventions": [drug] if drug else (t.get("interventions") or []),
        "sponsor": _clean(sponsor),
        "start_date": start_date,
        "primary_completion_date": t.get("primary_completion_date"),
        "countries": ["China"],
        "enrollment": enrollment,
        "primary_outcome": _clean(primary_outcome),
        "secondary_outcome": _clean(secondary_outcome),
        "inclusion": _clean(inclusion),
        "exclusion": _clean(exclusion),
        "comparator": _clean(comparator),
        "age_min": _clean(age_min),
        "age_max": _clean(age_max),
        "gender": _clean(gender),
        "drug": _clean(drug),
        "url": url,
        "documents": t.get("documents") or [],
        "raw": t,
    }


def norm_isrctn(t):
    return {
        "source": "ISRCTN",
        "registry_id": t.get("isrctn"),
        "title": t.get("title"),
        "status": t.get("status"),
        "phase": t.get("phase"),
        "conditions": t.get("conditions") or [],
        "interventions": t.get("interventions") or [],
        "sponsor": t.get("sponsor"),
        "start_date": None,
        "primary_completion_date": None,
        "countries": t.get("countries") or [],
        "enrollment": None,
        "drug": None,
        "url": f"https://www.isrctn.com/{t.get('isrctn')}" if t.get("isrctn") else None,
        "documents": t.get("documents") or [],
    }


def norm_euctr(t):
    # `documents` (list of {title,type,url}) is populated by fetch_eu_ctr_docs.py from the
    # EU CTIS public retrieve API; empty for list-only records.
    return {
        "source": "EUCTR",
        "registry_id": t.get("ctNumber") or t.get("euctNumber"),
        "title": t.get("title") or t.get("briefTitle"),
        "status": t.get("ctStatus") or t.get("status"),
        "phase": t.get("phase"),
        "conditions": t.get("conditions") or [],
        "interventions": t.get("interventions") or [],
        "sponsor": t.get("sponsor"),
        "start_date": t.get("startDateEU"),
        "primary_completion_date": t.get("endDateEU"),
        "countries": t.get("countries") or [],
        "enrollment": None,
        "drug": None,
        "url": f"https://euclinicaltrials.eu/ctis-public-api/retrieve/{t.get('ctNumber')}" if t.get("ctNumber") else None,
        "documents": t.get("documents") or [],
    }


def norm_chictr(t):
    # ChiCTR 浏览器抓取产出：registry_id (ChiCTRxxxx), title, url, raw
    return {
        "source": "CHICTR",
        "registry_id": t.get("registry_id"),
        "title": t.get("title"),
        "status": None,
        "phase": None,
        "conditions": [],
        "interventions": [],
        "sponsor": None,
        "start_date": None,
        "primary_completion_date": None,
        "countries": ["China"],
        "enrollment": None,
        "drug": None,
        "url": t.get("url"),
        "documents": t.get("documents") or [],
    }


def norm_drks(t):
    # DRKS (German Clinical Trials Register), via external service.
    # External service returns records shaped: drks_id / title / status / phase /
    # conditions[] / interventions[] / sponsor / countries[].
    return {
        "source": "DRKS",
        "registry_id": t.get("drks_id") or t.get("registry_id"),
        "title": t.get("title"),
        "status": t.get("status"),
        "phase": t.get("phase"),
        "conditions": t.get("conditions") or [],
        "interventions": t.get("interventions") or [],
        "sponsor": t.get("sponsor"),
        "start_date": t.get("startDate"),
        "primary_completion_date": t.get("endDate"),
        "countries": t.get("countries") or [],
        "enrollment": t.get("enrollment"),
        "drug": None,
        "url": (f"https://www.drks.de/drks_web/navigate.do?navigationId=detail&"
                f"drksId={t.get('drks_id')}") if t.get("drks_id") else None,
        "documents": t.get("documents") or [],
    }


def norm_ictrp(t):
    # WHO ICTRP, via external service (source="who"). Both list and DETAIL shapes
    # arrive here (the unified endpoint serves WHO records). DETAIL records carry
    # rich English fields with mixed case + spaces + literal parenthesised
    # plurals: "Health condition(s)", "Target sample size", "Study type",
    # "Primary Outcome(s)", "Secondary Outcome(s)", "Inclusion criteria",
    # "Exclusion criteria", "Age minimum/maximum", "Gender". We probe these with a
    # tolerant key matcher (see `first`) so they map onto the unified clinical
    # schema. The FULL record is stashed in `raw` so aggregate.py can bridge on any
    # embedded registry numbers (NCT / JPRN / CTRI / ...).
    def first(*keys):
        # Tolerant key probe: strip ALL non-alphanumeric noise, and additionally
        # allow singular/plural prefix bridging so `health_condition` matches
        # "Health condition(s)" and `primary_outcome` matches "Primary Outcome(s)".
        def nk(s):
            # Keep CJK characters so Chinese keys (e.g. 来源 / 适应症 / 登记号)
            # do NOT collapse to the empty string and collide in key_map. Only
            # ASCII punctuation/whitespace is stripped for tolerant matching.
            return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", s.lower()).strip()
        key_map = {nk(k): k for k in t.keys()}
        for k in keys:
            v = t.get(k)
            if v not in (None, "", []):
                return v
            kk = nk(k)
            for rk, real in key_map.items():
                if rk == kk or rk.startswith(kk + " ") or kk.startswith(rk + " "):
                    v2 = t.get(real)
                    if v2 not in (None, "", []):
                        return v2
        return None

    reg = first("登记号", "Main ID", "main_id", "registration_number",
                "project_id", "trial_id", "id", "registry_id")
    title = first("药物名称", "公共标题", "public_title", "title", "who_title")
    cond = first("适应症", "健康状况", "health_condition")
    status = first("试验状态", "招募状态", "recruitment_status", "trial_status", "status")
    sponsor = first("who_sponsor", "sponsor", "primary sponsor", "申办者", "applicant")
    country = first("who_country", "country", "countries", "countries of recruitment",
                    "recruiting_country")
    phase = first("who_phase", "phase")
    study_type = first("study_type", "研究类型")
    enrollment = _to_int(first("target_sample_size", "样本量", "enrollment"))
    primary_outcome = first("primary_outcome", "主要终点", "主要终点指标")
    secondary_outcome = first("secondary_outcome", "次要终点", "次要终点指标")
    inclusion = first("inclusion_criteria", "入选标准", "inclusion")
    exclusion = first("exclusion_criteria", "排除标准", "exclusion")
    comparator = first("comparator", "对照药", "control_drug")
    age_min = first("age_minimum", "最小年龄")
    age_max = first("age_maximum", "最大年龄")
    gender = first("gender", "性别")
    url = first("detail_url", "url", "来源链接")
    start_date = first("注册日期", "registration_date", "date_registration",
                       "start_date", "date_of_registration")
    raw = json.dumps(t, ensure_ascii=False)

    if isinstance(cond, str):
        conditions = [c.strip() for c in re.split(r"[;；\n]", cond) if c.strip()]
    else:
        conditions = cond if isinstance(cond, list) else ([cond] if cond else [])
    if isinstance(country, str):
        countries = [c.strip() for c in country.split(",") if c.strip()]
    else:
        countries = country if isinstance(country, list) else ([country] if country else [])
    # De-duplicate (WHO/ICTRP may list the same recruiting country multiple times).
    countries = list(dict.fromkeys(countries))

    return {
        "source": "ICTRP",
        "registry_id": reg,
        "title": title,
        "status": status,
        "phase": phase,
        "study_type": study_type,
        "conditions": conditions,
        "interventions": [],  # intervention embedded in raw for bridge scan
        "sponsor": sponsor,
        "start_date": start_date,
        "primary_completion_date": None,
        "countries": countries,
        "enrollment": enrollment,
        "primary_outcome": primary_outcome,
        "secondary_outcome": secondary_outcome,
        "inclusion": inclusion,
        "exclusion": exclusion,
        "comparator": comparator,
        "age_min": age_min,
        "age_max": age_max,
        "gender": gender,
        "drug": None,
        "url": url,
        "documents": t.get("documents") or [],
        "raw": raw,
    }


ADAPTERS = {"CTGOV": norm_ctgov, "CDE": norm_cde, "ISRCTN": norm_isrctn,
            "EUCTR": norm_euctr, "CHICTR": norm_chictr, "DRKS": norm_drks,
            "ICTRP": norm_ictrp,
            # CTIS（2026-09-07 上移）：EudraCT 继任者，字段与 EUCTR 同构
            #（ctNumber/title/ctStatus/sponsor/startDateEU + documents）→ 复用 norm_euctr
            "CTIS": norm_euctr}


# --- RMP (Risk Management Plan) field (R14: trial-layer traceability) ------------
# EU CTIS dossiers expose a documents list that may include a Risk Management Plan
# (document type/title contains "Risk Management Plan" / "RMP"). Surface its URL on
# the unified record so ct-pipeline's traceability chain can light up `rmp`.
_RMP_RE = re.compile(r"risk\s*management\s*plan|\brmp\b", re.I)


def _extract_rmp(docs):
    """Return the URL of a Risk Management Plan document if present, else None."""
    if not docs:
        return None
    for d in docs:
        if not isinstance(d, dict):
            continue
        blob = "%s %s" % (d.get("type") or "", d.get("title") or "")
        if _RMP_RE.search(blob):
            return d.get("url")
    return None


def normalize_file(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    fn = ADAPTERS.get(data.get("source"))
    if not fn:
        print(f"[normalize] skip unknown source in {path}: {data.get('source')}")
        return []
    recs = [fn(r) for r in data.get("records", [])]
    # req4: guarantee every record carries a full (clickable) homepage URL.
    # Sources that already emit a full http(s) URL (CT.gov/CDE/ISRCTN/EUCTR/DRKS)
    # are left untouched; only relative/empty URLs are upgraded via the registry_id.
    for r in recs:
        u = r.get("url")
        if not (u and str(u).lower().startswith(("http://", "https://"))):
            r["url"] = resolve_homepage(r.get("registry_id"), u)
        r["rmp"] = _extract_rmp(r.get("documents"))  # R14: trial-layer RMP linkage
        # R10: fold registry-specific phase spellings onto one canonical form so
        # phase_dist / crosstabs do not fragment across sources. The source's
        # own wording is preserved in `phase_raw` for traceability.
        _p = r.get("phase")
        _c = canon_phase(_p)
        if _c != _p:
            r["phase_raw"] = _p
        r["phase"] = _c
        # R5: attach a conservative sponsor grouping key. The display name in
        # `sponsor` is deliberately left untouched.
        _sk = sponsor_key(r.get("sponsor"))
        if _sk:
            r["sponsor_key"] = _sk
        # R6: fold registry-specific status spellings; original kept in
        # `status_raw` so the source wording stays traceable.
        _st = r.get("status")
        _cs = canon_status(_st)
        if _cs != _st:
            r["status_raw"] = _st
        r["status"] = _cs
        # R7: coerce enrollment to int at the SINGLE funnel. Only the CDE and
        # ICTRP adapters used to call _to_int(); CT.gov / EU CTR / ISRCTN /
        # DRKS / ChiCTR passed the raw value straight through, and
        # export_xlsx filters with isinstance(int, float) -- so every
        # string-typed sample size ("1,200", "200", "约200例") was DROPPED
        # from the enrollment stats silently, with no warning and no error.
        _en = r.get("enrollment")
        _ei = _to_int(_en)
        if _ei != _en:
            r["enrollment_raw"] = _en
        r["enrollment"] = _ei
        # upgrade D (2026-09-29): stale-trial detection tag. Pure-local heuristic
        # on last_update_posted + canonical status so competitors are not
        # mis-scored from abandoned/withdrawn trials. See stale_check.py.
    try:
        import stale_check
        recs = [stale_check.classify_stale(r) for r in recs]
    except Exception as _e:  # noqa: BLE001 - never break normalization
        print("[normalize] stale tag skipped: %s" % _e, file=sys.stderr)
    return recs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ctgov")
    ap.add_argument("--cde")
    ap.add_argument("--chictr")
    ap.add_argument("--isrctn")
    ap.add_argument("--euctr")
    ap.add_argument("--ctis")
    ap.add_argument("--drks")
    ap.add_argument("--ictrp")
    ap.add_argument("--out", default="normalized.json")
    args = ap.parse_args()
    merged = []
    for key, path in [("ctgov", args.ctgov), ("cde", args.cde), ("chictr", args.chictr),
                      ("isrctn", args.isrctn), ("euctr", args.euctr), ("ctis", args.ctis),
                      ("drks", args.drks), ("ictrp", args.ictrp)]:
        if path:
            merged += normalize_file(path)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    print(f"[normalize] {len(merged)} records -> {args.out}")


if __name__ == "__main__":
    main()
