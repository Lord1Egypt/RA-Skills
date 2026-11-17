#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fetch_prospero.py — PROSPERO fetcher (systematic-review registry, P1).

PROSPERO (Centre for Reviews and Dissemination, Univ. of York) is the international
prospective register of systematic reviews. For ct-literature it answers a distinct
question from the bibliographic sources: *"is a review on this topic already
registered / ongoing?"* — i.e. duplication-avoidance + protocol discovery. It is a
review/protocol registry (not primary studies), so it is opt-in (default OFF) and
treated as a supplementary source (normalize._SOURCE_PRIORITY["PROSPERO"] = 1).

✅ VERIFIED SOURCE (2026-11-03): the POST /PROSPERO/api/search path was reverse-ported
from meta-analysis and verified against the live registry (topic "efficacy of PD-1
inhibitors in advanced non-small cell lung cancer" -> 1479 records). Public search
needs NO login — it only requires a self-made `prospero-auth-token` header
(base64 of a millisecond timestamp); without that header the server answers
`{"status":"error","errormessage":"Error code: header value undefined"}`.
The original GET + `PROSPERO-ACCESS-TOKEN` path is retained as a fallback for callers
holding a formal token, but it stays UNVERIFIED (never confirmed against a live 200).

Zero confidential data or information input; reads only public registry records.
"""
import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from adapters import http_utils  # shared GET + retry

BASE = "https://www.crd.york.ac.uk/prospero/api/search/"

# 实测可用的公开检索端点（POST，2026-11-03 由 meta-analysis 反向移植并验证：
# PD-1 主题 1479 条命中）。注意大小写与 BASE 不同（PROSPERO 大写、无尾斜杠）。
POST_API = "https://www.crd.york.ac.uk/PROSPERO/api/search"
AUTH_HEADER = "prospero-auth-token"

DEFAULT_HEADER = "PROSPERO-ACCESS-TOKEN"


def _auth_headers(token=None, header_name=DEFAULT_HEADER):
    """鉴权头。默认走公开检索路径：自造 `prospero-auth-token`（base64 毫秒时间戳）。

    PROSPERO 公开检索无需登录，缺这个头服务端才报 "header value undefined"。
    提供 `token` 时额外附加 `header_name` 头（供已申请正式 token 的调用方；原 GET
    路径保留为 fallback）。
    """
    ts = str(int(time.time() * 1000))
    h = {
        "Content-Type": "application/json",
        AUTH_HEADER: base64.b64encode(ts.encode("utf-8")).decode("ascii"),
        "User-Agent": http_utils.UA,
        "Accept": "application/json",
    }
    if token:
        h[header_name] = token
    return h


def _is_error_envelope(node):
    """PROSPERO 新版接口在后端异常时返回嵌套错误信封（非顶层），例如：
        {"note":{"status":"error","errormessage":{"errorcode":20000,
         "errormessage":"connect ETIMEDOUT 86.188.140.222:9200"}}, "hits":0, ...}
    必须把这种「后端挂了」与真正的「0 命中」区分开，否则会误报成「无同类综述」。
    """
    note = (node or {}).get("note")
    if not isinstance(note, dict):
        return None
    if note.get("status") == "error" or "errormessage" in note:
        msg = note.get("errormessage")
        if isinstance(msg, dict):
            msg = msg.get("errormessage") or msg.get("errorcode") or json.dumps(msg, ensure_ascii=False)
        return str(msg or "unknown upstream error")
    return None


def _build_query(topic, review_type="all", year_from=None, year_to=None, safety=False):
    q = topic
    if review_type in ("systematic-review", "meta-analysis"):
        q += " AND (systematic review OR meta-analysis)"
    elif review_type == "scoping-review":
        q += " AND scoping review"
    if safety:
        q += " AND (adverse event OR safety OR toxicity)"
    if year_from or year_to:
        lo = str(year_from) if year_from else ""
        hi = str(year_to) if year_to else ""
        if lo and hi:
            q += " AND (%s:%s)" % (lo, hi)
    return q


def _parse_response(text):
    """Best-effort parse of a PROSPERO search response into unified works.

    Tolerant of both JSON and XML shapes; returns [] on parse failure (never raises).
    Fields mapped defensively; unknown keys are ignored.
    """
    text = (text or "").strip()
    if not text:
        return []
    works = []
    # ---- try JSON first ----
    try:
        j = json.loads(text)
        if isinstance(j, dict) and j.get("status") == "error":
            return []  # API error payload (e.g. missing token) -> degrade
        reviews = (j.get("reviewlist") or j.get("resultList") or j.get("reviews")
                   or (j.get("return") or {}).get("reviewlist") or [])
        for rv in (reviews if isinstance(reviews, list) else []):
            w = _map_review(rv)
            if w:
                works.append(w)
        if works:
            return works
    except Exception:
        pass
    # ---- fall back to XML (legacy PROSPERO schema) ----
    try:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(text)
        for rv in root.iter("review"):
            w = _map_review_xml(rv)
            if w:
                works.append(w)
    except Exception:
        pass
    return works


def _map_review(rv):
    if not isinstance(rv, dict):
        return None
    rid = rv.get("id") or rv.get("recordid") or rv.get("PROSPERO_ID")
    title = rv.get("displayName") or rv.get("title") or rv.get("reviewTitle")
    if not rid and not title:
        return None
    status = rv.get("status") or rv.get("reviewStatus") or ""
    reg = rv.get("registrationDate") or rv.get("dateRegistered") or ""
    url = ("https://www.crd.york.ac.uk/prospero/display_record.php?RecordID=%s"
           % rid) if rid else None
    return {
        "source": "PROSPERO",
        "id": rid,
        "doi": None, "pmid": None, "pmcid": None,
        "title": title,
        "authors": [],
        "year": int(reg[:4]) if (reg and reg[:4].isdigit()) else None,
        "publication_date": reg or None,
        "publication": "PROSPERO",
        "journal_iso": "PROSPERO",
        "type": "systematic-review-protocol",
        "study_type": "systematic-review",
        "cited_by_count": 0,
        "url": url,
        "open_access_url": None,
        "abstract_snippet": rv.get("description") or rv.get("objective") or "",
        "mesh": None,
        "concepts": None, "keywords": None, "funders": None,
        "language": None, "is_retracted": False, "is_safety": False,
        "is_preprint": False,
        "volume": None, "issue": None, "page": None,
        "affiliations": None,
        "sources": ["PROSPERO"],
        "prospero_status": status,
    }


def _map_review_xml(rv):
    def gt(tag):
        el = rv.find(tag)
        return el.text.strip() if el is not None and el.text else None
    rid = gt("id") or gt("recordid") or gt("PROSPERO_ID")
    title = gt("displayName") or gt("title") or gt("reviewTitle")
    if not (rid or title):
        return None
    status = gt("status") or gt("reviewStatus") or ""
    reg = gt("registrationDate") or gt("dateRegistered") or ""
    url = ("https://www.crd.york.ac.uk/prospero/display_record.php?RecordID=%s"
           % rid) if rid else None
    return {
        "source": "PROSPERO",
        "id": rid,
        "doi": None, "pmid": None, "pmcid": None,
        "title": title,
        "authors": [],
        "year": int(reg[:4]) if (reg and reg[:4].isdigit()) else None,
        "publication_date": reg or None,
        "publication": "PROSPERO",
        "journal_iso": "PROSPERO",
        "type": "systematic-review-protocol",
        "study_type": "systematic-review",
        "cited_by_count": 0,
        "url": url,
        "open_access_url": None,
        "abstract_snippet": gt("description") or gt("objective") or "",
        "mesh": None, "concepts": None, "keywords": None, "funders": None,
        "language": None, "is_retracted": False, "is_safety": False,
        "is_preprint": False,
        "volume": None, "issue": None, "page": None, "affiliations": None,
        "sources": ["PROSPERO"],
        "prospero_status": status,
    }


def _map_post_hit(h):
    """POST /search 响应 `retvals.hits.hits[*]` 元素 -> 统一 work schema。

    与 `_map_review`（GET stub 路径）字段对齐，差异仅在取值来源（`_source` 子对象）。
    """
    src = (h or {}).get("_source") or {}
    rid = src.get("accessionnumber") or src.get("recordid")
    # PROSPERO 的 title 带 <p> 等富文本标签，剥掉（否则原样显示标签）；
    # 个别记录还带 BOM 前缀，一并清掉。
    title = re.sub(r"<[^>]+>", "", str(src.get("title") or "")).strip().lstrip("\ufeff")
    if not (rid or title):
        return None
    reg = src.get("dateaccepted") or src.get("registrationdate") or ""
    year = src.get("yearfirstpublished")
    try:
        year = int(str(year)[:4]) if year else None
    except (TypeError, ValueError):
        year = None
    if year is None and reg[:4].isdigit():
        year = int(reg[:4])
    status = src.get("reviewstatus") or src.get("status") or ""
    url = ("https://www.crd.york.ac.uk/prospero/display_record.php?RecordID=%s"
           % rid) if rid else None
    return {
        "source": "PROSPERO",
        "id": rid,
        "doi": None, "pmid": None, "pmcid": None,
        "title": title,
        "authors": [],
        "year": year,
        "publication_date": reg or None,
        "publication": "PROSPERO",
        "journal_iso": "PROSPERO",
        "type": "systematic-review-protocol",
        "study_type": "systematic-review",
        "cited_by_count": 0,
        "url": url,
        "open_access_url": None,
        "abstract_snippet": src.get("description") or src.get("objective") or "",
        "mesh": None,
        "concepts": None, "keywords": None, "funders": None,
        "language": None, "is_retracted": False, "is_safety": False,
        "is_preprint": False,
        "volume": None, "issue": None, "page": None,
        "affiliations": None,
        "sources": ["PROSPERO"],
        "prospero_status": status,
    }


def _post_search(term, timeout=45, nperpage=50, token=None,
                 header_name=DEFAULT_HEADER):
    """POST /PROSPERO/api/search —— 实测可用的公开检索路径（2026-11-03 反向移植）。

    返回 `(hit_count, works, normalized_term)`。后端异常（ES 超时等）抛 RuntimeError
    由调用方降级——必须把「后端挂了」与「真 0 命中」区分开。

    排序（2026-10-25 实测）：服务端**忽略 `sort` 字段**，只有 `sortorder` 会改变结果。
    这里仍按约定下发 `sort=yearfirstpublished&sortorder=desc`（上游将来支持即自动生效），
    是否本地二次排序由调用方决定。
    """
    body = json.dumps({
        "term": term,
        "actual": term,
        "line": 0,
        "page": 1,
        "nperpage": max(1, int(nperpage)),
        "sort": "yearfirstpublished",
        "sortorder": "desc",
        "filters": [],          # 必须是数组；传 {} 会触发服务端类型错误
        "download": False,
    }).encode("utf-8")
    text = http_utils.post_text(POST_API, body,
                                headers=_auth_headers(token, header_name),
                                timeout=timeout, max_retries=3)
    j = json.loads(text)
    node = {}
    if isinstance(j, list) and j:
        node = j[0] if isinstance(j[0], dict) else {}
    elif isinstance(j, dict):
        node = j
    # 服务端错误信封：① 顶层 {"status":"error","errormessage":…}；
    # ② 新版嵌套在 note 里（后端 ES 超时等）。
    if node.get("status") == "error" or ("errormessage" in node and "hits" not in node):
        msg = node.get("errormessage")
        if isinstance(msg, dict):
            msg = msg.get("errormessage") or msg.get("errorcode") or json.dumps(msg, ensure_ascii=False)
        raise RuntimeError("PROSPERO API error: %s" % (msg or "unknown"))
    _env = _is_error_envelope(node)
    if _env:
        raise RuntimeError("PROSPERO API error (nested): %s" % _env)

    hits = node.get("hits")
    if not isinstance(hits, int):
        total = (((node.get("retvals") or {}).get("hits") or {}).get("total") or {})
        hits = total.get("value") if isinstance(total, dict) else None
    works = []
    for h in (((node.get("retvals") or {}).get("hits") or {}).get("hits") or []):
        w = _map_post_hit(h)
        if w:
            works.append(w)
    return hits, works, (node.get("term") or term)


def fetch(topic, review_type="all", year_from=None, year_to=None, safety=False,
          max_results=30, run=False, out=None, token=None,
          header_name=DEFAULT_HEADER, raw_query=None):
    """Fetch systematic-review registrations from PROSPERO.

    `raw_query`（2026-11-03 新增，向后兼容）:
        非空时**直接**用作检索词，跳过下方内部 `_build_query` 拼接（review_type /
        safety / 日期窗）——调用方应已把这些条件编进 `raw_query`。这样
        meta-analysis 等已用真值集调优过候选词与 PICOS 前置的技能，可以复用本模块
        的「执行器」能力（HTTP / 重试 / 解析 / hitCount 提取），而不必丢失检索式。

    执行路径：
      1. 主路径 POST /PROSPERO/api/search（公开检索，自造 token 头，已实测）
      2. 降级  GET + `token`（原 stub 路径，供已申请正式 token 的调用方；未验证）
    """
    if not run:
        print("[PREVIEW] would query PROSPERO for topic=%r review_type=%r "
              "(use --run to execute)" % (topic, review_type))
        if raw_query:
            print("[PREVIEW] raw_query=%r（内部构造已跳过）" % raw_query)
        return None

    q = raw_query or _build_query(topic, review_type, year_from, year_to, safety)

    # 主路径：POST（实测可用，公开检索免登录）
    try:
        hits, works, norm = _post_search(q, timeout=45, nperpage=max_results,
                                         token=token, header_name=header_name)
        payload = {
            "source": "PROSPERO",
            "query": norm,
            "review_type": review_type,
            "year_from": year_from,
            "year_to": year_to,
            "safety": safety,
            "hit_count": hits,
            "count": len(works),
            "works": works,
        }
        if out:
            with open(out, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            print("[OK] PROSPERO wrote %d works -> %s" % (len(works), out))
        return payload
    except Exception as e:  # noqa: BLE001
        print("[WARN] PROSPERO POST failed for %r: %s" % (q, e))

    # 降级路径：GET + token（原 stub，未验证；仅在有 token 时尝试）
    if not token:
        return None
    params = {"search": q, "limit": max_results, "offset": 0}
    url = BASE + "?" + urllib.parse.urlencode(params)
    headers = {"User-Agent": http_utils.UA, header_name: token}
    try:
        text = http_utils.get_text(url, headers=headers, timeout=45, max_retries=3)
    except http_utils.HttpError as e:
        print("[WARN] PROSPERO request failed: %s" % e)
        return None
    except Exception as e:  # noqa: BLE001
        print("[WARN] PROSPERO request error: %s" % e)
        return None

    works = _parse_response(text)
    payload = {
        "source": "PROSPERO",
        "query": q,
        "review_type": review_type,
        "year_from": year_from,
        "year_to": year_to,
        "safety": safety,
        "hit_count": len(works),
        "count": len(works),
        "works": works,
    }
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print("[OK] PROSPERO wrote %d works -> %s" % (len(works), out))
    return payload


def main():
    ap = argparse.ArgumentParser(description="Fetch systematic-review registrations via PROSPERO.")
    ap.add_argument("--topic", required=True)
    ap.add_argument("--review-type", default="all",
                    choices=["all", "systematic-review", "scoping-review",
                             "meta-analysis", "rct", "case-report"])
    ap.add_argument("--year-from", type=int)
    ap.add_argument("--year-to", type=int)
    ap.add_argument("--safety", action="store_true")
    ap.add_argument("--max", type=int, default=30)
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--prospero-token", default=os.environ.get("PROSPERO_API_TOKEN"))
    ap.add_argument("--prospero-header", default=DEFAULT_HEADER)
    ap.add_argument("--raw-query", default=None, metavar="TERM",
                    help="直接用作检索词，跳过内部 review_type/safety/日期窗拼接")
    args = ap.parse_args()
    res = fetch(args.topic, args.review_type, args.year_from, args.year_to,
                args.safety, args.max, args.run, args.out,
                token=args.prospero_token, header_name=args.prospero_header,
                raw_query=args.raw_query)
    if res and not args.out:
        print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
