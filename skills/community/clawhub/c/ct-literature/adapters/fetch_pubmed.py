#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fetch_pubmed.py — NCBI PubMed (E-utilities) fetcher.

WHY / 设计动机（2026-11-03）
────────────────────────────
ct-literature 此前**只有 Europe PMC 一个源**同时覆盖 PubMed/MEDLINE 与 Cochrane
Database of Systematic Reviews（CDSR）。它一旦限流或不可达，Cochrane 检索直接归零
（`--cochrane` 的期刊过滤只推给本地 Europe PMC 腿）。本模块接入 NCBI E-utilities
作为**独立冗余通道**：

  - `db=pubmed`                       → MEDLINE / PubMed 记录（带 PMID + PMCID + DOI）
  - `Cochrane Database Syst Rev[ta]`  → 同一个库里的 CDSR 期刊字段过滤

一次检索即可同时覆盖两者，且与 ebi.ac.uk 是完全不同的基础设施（不同 CDN / 限额 /
故障域），因此是真正有效的故障转移目标，而不是「换个域名继续锤同一家」。

调用链
──────
  esearch.fcgi  →  ID 列表 + 命中总数（retmax = max_results）
  efetch.fcgi   →  PubMed XML 全记录（题录 + 摘要 + MeSH + 文献类型）——主路径
  esummary.fcgi →  JSON 题录（无摘要）——efetch 失败时的降级路径

限速（NCBI 官方）
────────────────
  无 API key：3 次/秒；有 `NCBI_API_KEY`：10 次/秒。本模块用模块级锁做本地节流，
  无 key 时按 0.34s/请求、有 key 时按 0.12s/请求串行化，并发送 `tool` + `email`
  进入官方 polite pool。

零外部依赖：仅标准库。无机密输入；只读公共题录。
"""
import argparse
import json
import os
import sys
import threading
import time
import urllib.parse
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from adapters import http_utils  # shared GET+retry (exponential backoff, 429 Retry-After)

ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
ESUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

# Cochrane Database of Systematic Reviews —— PubMed 的期刊缩写（[ta] 字段）。
# 与 Europe PMC 的 `JOURNAL:"The Cochrane database of systematic reviews"` 是
# **同一本期刊的两套检索语法**，跨源命中数应可互相印证。
COCHRANE_JOURNAL_TAG = "Cochrane Database Syst Rev[ta]"
COCHRANE_JOURNAL_MARK = "cochrane database of systematic reviews"

# ── 限速 ────────────────────────────────────────────────────────────────────
# NCBI 官方上限：无 key 3 req/s，有 key 10 req/s。留出余量取 0.34s / 0.12s。
_NO_KEY_INTERVAL = 0.34
_WITH_KEY_INTERVAL = 0.12
_throttle_lock = threading.Lock()
_last_req_ts = 0.0

POLITE_TOOL_DEFAULT = "ct-literature"
POLITE_EMAIL_ENV = "CT_LIT_NCBI_EMAIL"
NCBI_KEY_ENV = "NCBI_API_KEY"

SAFETY_LEXICON = [
    "adverse event", "adverse reaction", "side effect", "safety", "toxicity",
    "toxic", "case report", "pharmacovigilance", "drug-induced", "drug reaction",
]


def load_ncbi_key(env_var=NCBI_KEY_ENV):
    """读取 NCBI API key（env 优先，其次技能根 .env）。key 永不打印。"""
    v = (os.environ.get(env_var) or "").strip()
    if v:
        return v
    try:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(root, ".env"), encoding="utf-8", errors="ignore") as f:
            for line in f:
                if line.strip().startswith(env_var + "="):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if val and val.lower() not in ("", "none", "changeme"):
                        os.environ[env_var] = val
                        return val
    except Exception:
        pass
    return None


def _throttle(api_key=None):
    """模块级串行节流：保证两次 eutils 请求间隔不低于当前配额对应的下限。"""
    global _last_req_ts
    interval = _WITH_KEY_INTERVAL if (api_key or load_ncbi_key()) else _NO_KEY_INTERVAL
    with _throttle_lock:
        wait = interval - (time.time() - _last_req_ts)
        if wait > 0:
            time.sleep(wait)
        _last_req_ts = time.time()


def _polite_params(api_key=None, email=None, tool=None):
    """NCBI polite-pool 标识 + api_key。空值不发，绝不发空串。"""
    t = str(tool if tool is not None else POLITE_TOOL_DEFAULT).strip()
    e = str(email if email is not None
            else (os.environ.get(POLITE_EMAIL_ENV) or "")).strip()
    k = api_key if api_key is not None else load_ncbi_key()
    out = {}
    if t:
        out["tool"] = t
    if e:
        out["email"] = e
    if k:
        out["api_key"] = k
    return out


# ── 检索式构造 ──────────────────────────────────────────────────────────────
# review_type 用 PubMed 的 [pt]（Publication Type）字段，比自由词更精确：
# 这是**备用通道**，精度优先于召回（召回由主通道 Europe PMC 负责）。
_REVIEW_TYPE_PT = {
    "systematic-review": "(systematic review[pt] OR meta-analysis[pt])",
    "meta-analysis": "meta-analysis[pt]",
    "scoping-review": "scoping review[tiab]",
    "rct": "randomized controlled trial[pt]",
    "case-report": "case reports[pt]",
}

_REVIEW_EXCLUDE_PT = ("Review[pt] OR Systematic Review[pt] OR Meta-Analysis[pt]")


def _safety_clause():
    """安全性偏向子句：标题/摘要里出现 AE / 毒性 / 药物不良反应等信号词。"""
    terms = ["adverse event", "adverse reaction", "side effect", "safety",
             "toxicity", "drug-induced", "pharmacovigilance", "case report"]
    parts = []
    for k in terms:
        parts.append("%s[tiab]" % k)
    return "(%s)" % " OR ".join(parts)


def _year_from_date(s):
    """从 '2025 May 27' / '2025/05/27 00:00' / '2025' 等形态里取 4 位年份。"""
    if not s:
        return None
    s = str(s).strip()
    if len(s) >= 4 and s[:4].isdigit():
        return int(s[:4])
    return None


def _month_num(m):
    """PubMed 的 Month 可能是 'May' / '5' / '05'。统一成数字（识别不了返回 1）。"""
    if not m:
        return 1
    m = str(m).strip()
    if m.isdigit():
        return int(m)
    names = ["jan", "feb", "mar", "apr", "may", "jun",
             "jul", "aug", "sep", "oct", "nov", "dec"]
    low = m.lower()[:3]
    return names.index(low) + 1 if low in names else 1


def _build_query(topic, review_type="all", safety=False, cochrane=False,
                 include_reviews=True, date_from=None, date_to=None,
                 year_from=None, year_to=None):
    """构造 PubMed 检索式。各子句之间 AND；任一子句失败不应影响其余。"""
    parts = [topic]
    if review_type in _REVIEW_TYPE_PT:
        parts.append(_REVIEW_TYPE_PT[review_type])
    if safety:
        parts.append(_safety_clause())
    if cochrane:
        parts.append(COCHRANE_JOURNAL_TAG)
    if not include_reviews:
        parts.append("NOT (%s)" % _REVIEW_EXCLUDE_PT)
    # 日期窗口：月份级（route B）优先，年份级兜底。PubMed 的日期字段是
    # [Date - Publication]，区间写法为 "lo"[DP] : "hi"[DP]。
    if date_from or date_to:
        lo = (date_from or "1900/01/01").replace("-", "/")
        hi = (date_to or time.strftime("%Y/%m/%d")).replace("-", "/")
        parts.append('("%s"[Date - Publication] : "%s"[Date - Publication])' % (lo, hi))
    elif year_from or year_to:
        lo = "%d/01/01" % year_from if year_from else "1900/01/01"
        hi = "%d/12/31" % year_to if year_to else "3000/12/31"
        parts.append('("%s"[Date - Publication] : "%s"[Date - Publication])' % (lo, hi))
    return " AND ".join(parts)


# ── esearch / efetch / esummary ─────────────────────────────────────────────
def _esearch(query, max_results, api_key=None, email=None, tool=None):
    """返回 (pmid_list, total_count)。total_count 独立于 max_results。"""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": min(max_results, 10000),
        "sort": "relevance",
    }
    params.update(_polite_params(api_key=api_key, email=email, tool=tool))
    _throttle(api_key)
    url = ESEARCH_URL + "?" + urllib.parse.urlencode(params)
    j = http_utils.get_json(url, timeout=30, max_retries=3)
    r = j.get("esearchresult") or {}
    if r.get("error"):
        raise RuntimeError("NCBI esearch error: %s" % r.get("error"))
    ids = r.get("idlist") or []
    try:
        total = int(r.get("count") or 0)
    except (TypeError, ValueError):
        total = len(ids)
    return ids, total


def _efetch_xml(ids, api_key=None, email=None, tool=None):
    """批量取 PubMed XML 全记录（题录 + 摘要 + MeSH + 文献类型）。"""
    if not ids:
        return []
    out = []
    # efetch 单批过大时响应可能被网关截断，按 150 一批稳妥。
    for i in range(0, len(ids), 150):
        chunk = ids[i:i + 150]
        params = {"db": "pubmed", "id": ",".join(chunk), "retmode": "xml"}
        params.update(_polite_params(api_key=api_key, email=email, tool=tool))
        _throttle(api_key)
        url = EFETCH_URL + "?" + urllib.parse.urlencode(params)
        raw = http_utils.get_text(url, timeout=60, max_retries=3)
        out.extend(_parse_pubmed_xml(raw))
    return out


def _esummary(ids, api_key=None, email=None, tool=None):
    """降级路径：只取 JSON 题录（无摘要）。efetch 挂掉时保住题录覆盖。"""
    if not ids:
        return []
    out = []
    for i in range(0, len(ids), 150):
        chunk = ids[i:i + 150]
        params = {"db": "pubmed", "id": ",".join(chunk), "retmode": "json"}
        params.update(_polite_params(api_key=api_key, email=email, tool=tool))
        _throttle(api_key)
        url = ESUMMARY_URL + "?" + urllib.parse.urlencode(params)
        j = http_utils.get_json(url, timeout=30, max_retries=3)
        r = j.get("result") or {}
        for uid in r.get("uids") or []:
            rec = r.get(uid)
            if isinstance(rec, dict):
                out.append(_norm_from_summary(rec))
    return out


# ── XML 解析 ────────────────────────────────────────────────────────────────
def _all_text(elem):
    """元素全部后代文本拼接（处理 <i>/<b>/<sup> 等内联标签）。"""
    if elem is None:
        return ""
    return " ".join("".join(elem.itertext()).split())


def _parse_pubmed_xml(raw):
    """把 efetch 的 PubMed XML 解析成中间归一 dict 列表。"""
    out = []
    try:
        root = ET.fromstring(raw.encode("utf-8") if isinstance(raw, str) else raw)
    except ET.ParseError as e:
        print("[WARN] PubMed XML 解析失败: %s" % e)
        return out
    for art in root.findall(".//PubmedArticle"):
        try:
            out.append(_norm_from_xml(art))
        except Exception as e:  # 单条解析失败不拖垮整批
            print("[WARN] PubMed 单条解析失败: %s" % e)
    return out


def _norm_from_xml(art):
    cite = art.find(".//MedlineCitation")
    if cite is None:
        cite = art
    pmid = (cite.findtext("PMID") or "").strip()
    title = _all_text(cite.find(".//ArticleTitle"))
    # 摘要：多段 AbstractText，带 Label 的保留 "LABEL: text" 结构
    abs_parts = []
    for ab in cite.findall(".//Abstract/AbstractText"):
        txt = _all_text(ab)
        if not txt:
            continue
        label = (ab.get("Label") or "").strip()
        if label and label.upper() != "UNLABELLED":
            abs_parts.append("%s: %s" % (label, txt))
        else:
            abs_parts.append(txt)
    abstract = " ".join(abs_parts) or ""
    journal = _all_text(cite.find(".//Journal/Title"))
    journal_iso = _all_text(cite.find(".//Journal/ISOAbbreviation"))
    authors = []
    for a in cite.findall(".//AuthorList/Author"):
        collective = _all_text(a.find("CollectiveName"))
        ln = _all_text(a.find("LastName"))
        fn = _all_text(a.find("ForeName")) or _all_text(a.find("Initials"))
        if collective:
            authors.append(collective)
        elif ln:
            authors.append(("%s %s" % (fn, ln)).strip() if fn else ln)
    # 日期：PubDate 可能是 Year/Month/Day，也可能是 MedlineDate（如 "2025 May-Jun"）
    pd = cite.find(".//JournalIssue/PubDate")
    if pd is None:
        pd = cite.find(".//ArticleDate")
    year = month = day = None
    medline_date = ""
    if pd is not None:
        y = _all_text(pd.find("Year"))
        if y.isdigit():
            year = int(y)
        m = _all_text(pd.find("Month"))
        month = _month_num(m) if m else None
        d = _all_text(pd.find("Day"))
        day = int(d) if d.isdigit() else None
        medline_date = _all_text(pd.find("MedlineDate"))
    pub_date = None
    if year:
        pub_date = "%04d" % year
        if month:
            pub_date += "-%02d" % month
            if day:
                pub_date += "-%02d" % day
    if not pub_date and medline_date:
        pub_date = medline_date
    # 标识符：只取本文的 PubmedData/ArticleIdList。
    # 注意：文末 <ReferenceList> 里被引文献也各带 ArticleIdList，
    # 若用 .//ArticleId 后代匹配会把别人的 PMCID/DOI 覆盖到本文头上。
    doi = pmcid = None
    own_ids = art.findall("./PubmedData/ArticleIdList/ArticleId")
    for aid in own_ids:
        t = (aid.get("IdType") or "").lower()
        v = (aid.text or "").strip()
        if t == "doi" and v:
            doi = v
        elif t == "pmc" and v:
            pmcid = v
    for eid in cite.findall(".//ELocationID"):
        if (eid.get("EIdType") or "").lower() == "doi" and (eid.text or "").strip():
            doi = doi or eid.text.strip()
    mesh = [(_all_text(m)) for m in cite.findall(".//MeshHeadingList/MeshHeading/DescriptorName")]
    pub_types = [(_all_text(p)) for p in cite.findall(".//PublicationTypeList/PublicationType")]
    return {
        "pmid": pmid,
        "title": title,
        "abstract": abstract,
        "journal": journal or journal_iso,
        "journal_iso": journal_iso,
        "year": year,
        "date": pub_date,
        "authors": authors,
        "doi": doi,
        "pmcid": pmcid,
        "mesh": mesh or None,
        "pub_types": pub_types or None,
    }


def _norm_from_summary(rec):
    """esummary JSON → 同一中间结构（无摘要）。"""
    ids = {}
    for aid in rec.get("articleids") or []:
        t = (aid.get("idtype") or "").lower()
        v = (aid.get("value") or "").strip()
        if t and v:
            ids[t] = v
    authors = [a.get("name") for a in (rec.get("authors") or []) if a.get("name")]
    sortpubdate = rec.get("sortpubdate") or rec.get("pubdate")
    return {
        "pmid": (rec.get("uid") or "").strip(),
        "title": (rec.get("title") or "").strip(),
        "abstract": "",
        "journal": rec.get("fulljournalname") or rec.get("source"),
        "journal_iso": rec.get("source"),
        "year": _year_from_date(sortpubdate),
        "date": sortpubdate,
        "authors": authors,
        "doi": ids.get("doi"),
        "pmcid": ids.get("pmc"),
        "mesh": None,
        "pub_types": rec.get("pubtype"),
    }


# ── 统一 work schema ────────────────────────────────────────────────────────
def _study_type_from(pub_types, title, abstract):
    blob = ((title or "") + " " + (abstract or "")).lower()
    pts = " ".join(pub_types or []).lower()
    if "systematic review" in blob or "meta-analysis" in blob:
        return "systematic-review"
    if "case report" in blob or "case series" in blob:
        return "case-report"
    if "randomized controlled trial" in blob or ("randomized" in blob and "trial" in blob):
        return "rct"
    if "review" in pts:
        return "review"
    return "article"


def _flag_safety(title, abstract):
    blob = ((title or "") + " " + (abstract or "")).lower()
    return any(k in blob for k in SAFETY_LEXICON)


def _extract(n):
    """中间归一 dict → 统一 work schema（与其他 fetch_* 完全同形）。"""
    pmid = n.get("pmid") or ""
    pmcid = n.get("pmcid") or ""
    title = (n.get("title") or "").strip()
    journal = n.get("journal") or ""
    is_cochrane = COCHRANE_JOURNAL_MARK in journal.lower()
    return {
        "source": "PubMed",
        "id": pmid,
        "pmid": pmid,
        "pmcid": pmcid,
        "doi": n.get("doi") or None,
        "title": title,
        "authors": n.get("authors") or None,
        "year": n.get("year"),
        "publication_date": n.get("date"),
        "publication": journal,
        "journal_iso": n.get("journal_iso"),
        "type": "article",
        "study_type": _study_type_from(n.get("pub_types"), title, n.get("abstract")),
        "cited_by_count": 0,
        "url": ("https://pubmed.ncbi.nlm.nih.gov/%s/" % pmid) if pmid else None,
        "open_access_url": ("https://pmc.ncbi.nlm.nih.gov/articles/%s/" % pmcid) if pmcid else None,
        "abstract_snippet": n.get("abstract") or "",
        "mesh": n.get("mesh"),
        "is_safety": _flag_safety(title, n.get("abstract")),
        "is_cochrane": is_cochrane,
        "pub_types": n.get("pub_types"),
    }


# ── 主入口 ──────────────────────────────────────────────────────────────────
def fetch(topic, review_type="all", year_from=None, year_to=None, safety=False,
          max_results=30, run=False, out=None, cochrane=False,
          include_reviews=True, date_from=None, date_to=None,
          api_key=None, email=None, tool=None,
          raw_query=None, strict_raw_query=None):
    """检索 PubMed。返回与其余 fetch_* 同形的 payload。

    cochrane=True 时用 `Cochrane Database Syst Rev[ta]` 限定 CDSR——这是
    Europe PMC 不可用时的独立 Cochrane 通道。

    raw_query / strict_raw_query（2026-11-03 新增，向后兼容）:
        非空时**直接**用作检索式，跳过内部 `_build_query()` 拼接——供
        meta-analysis 等已有实测调优检索式的技能复用本模块的执行器能力
        （esearch / efetch / esummary、限速、降级），而不必把检索式降级成
        自由词。此时 review_type / safety / cochrane / include_reviews /
        日期参数一律忽略，调用方应已把它们编进 raw_query。
        strict_raw_query 非空时额外做一次 esearch（retmax=1，count 独立于
        retmax）取严格口径命中数，失败降级为 None，不影响主结果。
    """
    if not run:
        print("[PREVIEW] would query PubMed for topic=%r review_type=%r cochrane=%r "
              "(use --run to execute)" % (topic, review_type, cochrane))
        if raw_query:
            print("[PREVIEW] raw_query=%r（内部构造已跳过）" % raw_query)
        return None

    if raw_query:
        query = raw_query
    else:
        query = _build_query(topic, review_type=review_type, safety=safety,
                             cochrane=cochrane, include_reviews=include_reviews,
                             date_from=date_from, date_to=date_to,
                             year_from=year_from, year_to=year_to)

    # 严格口径（可选）：只需命中数，retmax=1 即可（esearch 的 count 独立于
    # retmax）；失败降级 None，不拖垮主检索。
    strict_hit = None
    if strict_raw_query:
        try:
            _, strict_hit = _esearch(strict_raw_query, 1, api_key=api_key,
                                     email=email, tool=tool)
        except Exception as e:  # noqa: BLE001 - 严格层失败不拖垮主检索
            print("[WARN] PubMed 严格口径 esearch 失败：%s" % e)
            strict_hit = None

    ids, total = _esearch(query, max_results, api_key=api_key, email=email, tool=tool)
    if not ids:
        payload = {
            "source": "PubMed", "query": query, "review_type": review_type,
            "year_from": year_from, "year_to": year_to, "date_from": date_from,
            "date_to": date_to, "safety": safety, "cochrane": bool(cochrane),
            "hit_count": total, "count": 0, "works": [],
            "provenance": "esearch_only",
            "strict_hit_count": strict_hit, "strict_query": strict_raw_query,
        }
        if out:
            _write(payload, out)
        return payload

    # 主路径：efetch XML（含摘要）；失败降级 esummary（题录，无摘要）。
    provenance = "efetch"
    try:
        norms = _efetch_xml(ids, api_key=api_key, email=email, tool=tool)
        if not norms:
            raise RuntimeError("efetch 返回 0 条可解析记录")
    except Exception as e:
        print("[WARN] PubMed efetch 失败，降级 esummary（无摘要）：%s" % e)
        provenance = "esummary_fallback"
        try:
            norms = _esummary(ids, api_key=api_key, email=email, tool=tool)
        except Exception as e2:
            print("[WARN] PubMed esummary 也失败：%s" % e2)
            norms = []

    works = [_extract(n) for n in norms]
    payload = {
        "source": "PubMed",
        "query": query,
        "review_type": review_type,
        "year_from": year_from,
        "year_to": year_to,
        "date_from": date_from,
        "date_to": date_to,
        "safety": safety,
        "cochrane": bool(cochrane),
        "hit_count": total,
        "count": len(works),
        "works": works,
        "provenance": provenance,
        # 严格口径（2026-11-03）：仅在传入 strict_raw_query 时有值，否则 None。
        "strict_hit_count": strict_hit,
        "strict_query": strict_raw_query,
    }
    if out:
        _write(payload, out)
    return payload


def _write(payload, out):
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print("[OK] PubMed wrote %d works -> %s" % (payload.get("count", 0), out))


def main():
    ap = argparse.ArgumentParser(
        description="Fetch literature via NCBI PubMed E-utilities (public).")
    ap.add_argument("--topic", required=True)
    ap.add_argument("--review-type", default="all",
                    choices=["all", "systematic-review", "scoping-review",
                             "meta-analysis", "rct", "case-report"])
    ap.add_argument("--year-from", type=int)
    ap.add_argument("--year-to", type=int)
    ap.add_argument("--date-from", default=None, metavar="YYYY-MM-DD")
    ap.add_argument("--date-to", default=None, metavar="YYYY-MM-DD")
    ap.add_argument("--safety", action="store_true")
    ap.add_argument("--cochrane", action="store_true",
                    help="restrict to the Cochrane Database of Systematic Reviews "
                         "(via %s)" % COCHRANE_JOURNAL_TAG)
    ap.add_argument("--include-reviews", action=argparse.BooleanOptionalAction,
                    default=True)
    ap.add_argument("--max", type=int, default=30)
    ap.add_argument("--ncbi-key", default=None,
                    help="NCBI API key (default: env %s)" % NCBI_KEY_ENV)
    ap.add_argument("--email", default=None,
                    help="NCBI polite-pool email (default: env %s)" % POLITE_EMAIL_ENV)
    ap.add_argument("--tool", default=None,
                    help="NCBI polite-pool tool name (default: %s)" % POLITE_TOOL_DEFAULT)
    ap.add_argument("--raw-query", default=None, metavar="QUERY",
                    help="直接用作检索式，跳过内部 review_type/日期/Cochrane 拼接；"
                         "供已有调优检索式的技能复用本模块的执行器能力")
    ap.add_argument("--strict-raw-query", default=None, metavar="QUERY",
                    help="严格口径检索式，只取命中数（不取题录），结果见 "
                         "strict_hit_count")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--out")
    args = ap.parse_args()
    res = fetch(args.topic, args.review_type, args.year_from, args.year_to,
                args.safety, args.max, args.run, args.out, cochrane=args.cochrane,
                include_reviews=args.include_reviews, date_from=args.date_from,
                date_to=args.date_to, api_key=args.ncbi_key, email=args.email,
                tool=args.tool, raw_query=args.raw_query,
                strict_raw_query=args.strict_raw_query)
    if res and not args.out:
        print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
