#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""preprint_fallback.py — 非开放获取文献的预印本候选标注（opt-in）。

对合并后 works 中「无 OA 全文」的文献（is_oa 为假 / open_access_url 为空），
按标题在预印本服务器检索候选版本并标注到 work["preprint"]：

  * bioRxiv / medRxiv — Europe PMC 预印本合集（PPR）标题检索，无需密钥；
  * arXiv            — arXiv API 标题检索，无需密钥。

⚠️ 同篇校验（作者级，移植自 meta-analysis/adapters/pdf_fetch.py 的实测实现）：
预印本按标题模糊匹配，标题相近 ≠ 同一篇。故每个候选与原始文献作者逐姓氏比对，
**宁可缺漏不能弄错**：任一方缺作者、无共同姓氏、或第一作者不一致均丢弃候选。

work["preprint"] = {venue, doi|arxiv_id, url, author_check}
    venue ∈ {biorxiv, medrxiv, biorxiv_medrxiv, arxiv}

enrich(works, biorxiv=True, medrxiv=True, arxiv=True) → stats dict。
纯标准库（urllib），零第三方依赖；网络失败逐条跳过、不阻塞。
"""

import ast
import json
import re
import time
import urllib.parse
import urllib.request

# ---------------------------------------------------------------------------
# HTTP helper（带重试；与 meta-analysis pdf_fetch._get 同款）
# ---------------------------------------------------------------------------
def _get(url, timeout=30, retries=2):
    last = None
    for _ in range(retries + 1):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "ct-literature-skill/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (403, 404, 429):
                time.sleep(1)
                last = "HTTP %s" % e.code
                continue
            raise
        except Exception as e:
            last = "%s: %s" % (type(e).__name__, e)
            time.sleep(0.5)
    raise RuntimeError(str(last))


# ---------------------------------------------------------------------------
# 作者归一化 / 同篇校验（移植自 meta-analysis pdf_fetch，「不能弄错」原则）
# ---------------------------------------------------------------------------
def _norm_lastname(s):
    if not s:
        return ""
    s = str(s).strip().lower()
    # NFKD 折叠变音符号（"Jänne" → "janne"），与 verify_citations._norm_name /
    # Coze 0.3.98 归一内核保持一致；否则 "ä" 会被下面的字符类直接删成 "jnne"。
    try:
        import unicodedata
        s = "".join(ch for ch in unicodedata.normalize("NFKD", s)
                    if not unicodedata.combining(ch))
    except Exception:
        pass
    s = re.sub(r"[^一-鿿a-z0-9]", "", s)
    return s


def _surname_from_name(a):
    """从单个作者姓名字符串取姓氏，兼容常见著录格式。

    2026-11-04 修复（与 Coze 0.3.98 归一内核对齐）：旧实现一律取最后一个 token，
    "Borghaei H" / "Paz-Ares L" 会把 initial 当成姓氏（"h" / "l"），导致预印本
    同篇校验的第一作者永远比对不上，候选被 "first_author_mismatch" 全部丢弃。
    """
    s = str(a or "").strip().strip("'\"")
    if not s:
        return ""
    # "Last, First" / "Last; First" → 逗号/分号前为姓
    head = re.split(r"[,;]", s)[0].strip()
    if head:
        s = head
    toks = s.split()
    # 丢弃单字母 initials（H / L / A.）与全大写短缩写（PA / JP）；
    # 仅在还有实词可保留时丢弃，避免把 "LI" 这类短姓整条丢掉。
    def _initial(t):
        core = t.strip(".")
        return len(core) < 2 or (core.isupper() and len(core) <= 2)
    real = [t for t in toks if not _initial(t)]
    if not real:
        real = toks
    return real[-1]


def _lastnames_from_authors(authors):
    """多种作者表示 → 有序归一化姓氏列表（[0] 即第一作者）。

    兼容：list[str] / list[dict]（family|lastName|fullName…）/
    dict（单作者）；以及 str —— 含 Python list 的 repr（'[' 开头，
    fetcher 输出的作者字段曾以该形态落盘）与逗号/分号分隔的纯文本。
    """
    out = []
    if isinstance(authors, str):
        s = authors.strip()
        if s.startswith("["):
            # Python list repr / JSON 数组字符串 → 转 list 后递归
            try:
                parsed = ast.literal_eval(s)
            except Exception:
                try:
                    parsed = json.loads(s)
                except Exception:
                    parsed = None
            if isinstance(parsed, (list, tuple)):
                return _lastnames_from_authors(list(parsed))
            # 解析失败 → 退化为逐项清洗（去掉引号/方括号残留）
            s = s.strip("[]")
        # 单个 "Last, First" 不能拆成两个作者；多作者纯文本仍按逗号/分号拆。
        parts = [s] if (";" not in s and s.count(",") == 1) else re.split(r"[;,]", s)
        for part in parts:
            part = part.strip().strip("'\"")
            out.append(_norm_lastname(_surname_from_name(part)))
        return [x for x in out if x]
    if isinstance(authors, dict):
        authors = [authors]
    if not isinstance(authors, (list, tuple)):
        return []
    for a in authors:
        if isinstance(a, dict):
            ln = (a.get("family") or a.get("lastName") or a.get("lastname") or "")
            if not ln:
                fn = (a.get("fullName") or a.get("name") or a.get("full_name") or "")
                ln = _surname_from_name(fn)
            out.append(_norm_lastname(ln))
        elif isinstance(a, str):
            out.append(_norm_lastname(_surname_from_name(a)))
    return [x for x in out if x]


def _author_check(orig_ln, cand_ln):
    """作者校验：宁可缺漏不能弄错。返回 (passed, reason)。"""
    if not orig_ln or not cand_ln:
        return False, "missing_author_info"
    inter = set(orig_ln) & set(cand_ln)
    if not inter:
        return False, "no_shared_author"
    if orig_ln[0] != cand_ln[0]:
        return False, "first_author_mismatch"
    return True, "%d_shared_first_author_match" % len(inter)


_PREPRINT_STOPWORDS = frozenset(
    "a an the and or of in on at by for to with without from into during after before "
    "between among against across within about over under up down out off is are was were "
    "be been being have has had do does did will would can could should may might must its "
    "it's its it this that these those their our your his her their as than so but not no "
    "nor if then else when where which who whom whose how why what vs versus via per et al".split())


def _title_tokens(title, maxn=5):
    if not title:
        return []
    t = re.sub(r"[^a-z0-9\s]+", " ", title.lower())
    return [w for w in t.split() if len(w) > 1 and w not in _PREPRINT_STOPWORDS][:maxn]


# ---------------------------------------------------------------------------
# bioRxiv / medRxiv — Europe PMC PPR 标题检索（两段式：短语优先 → 内容词 AND 兜底）
# ---------------------------------------------------------------------------
def _epmc_preprint_search(title):
    if not title or len(title.strip()) < 8:
        return []

    def _run(q_expr, page_size=15):
        url = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search"
               "?query=%s&format=json&resultType=core&pageSize=%d&src=PPR"
               % (urllib.parse.quote(q_expr), page_size))
        try:
            import json
            d = json.loads(_get(url).decode("utf-8"))
            return (d.get("resultList") or {}).get("result", [])
        except Exception:
            return []

    recs = [r for r in _run('(TITLE:"%s")' % title.strip())
            if str(r.get("source", "")).upper() == "PPR"]
    if not recs:
        toks = _title_tokens(title)
        if len(toks) >= 3:
            q2 = "(" + " AND ".join("TITLE:%s" % w for w in toks) + ")"
            recs = [r for r in _run(q2)
                    if str(r.get("source", "")).upper() == "PPR"]
    out = []
    for rec in recs:
        pdf_url = ""
        for ft in (rec.get("fullTextUrlList") or {}).get("fullTextUrl", []):
            if (ft.get("documentStyle") == "pdf"
                    and str(ft.get("availability", "")).lower().startswith("open")):
                pdf_url = ft.get("url")
                break
        host = (urllib.parse.urlparse(pdf_url).hostname or "").lower() if pdf_url else ""
        doi = str(rec.get("doi", ""))
        if "medrxiv.org" in host:
            venue = "medrxiv"
        elif "biorxiv.org" in host:
            venue = "biorxiv"
        elif doi.startswith("10.1101"):
            venue = "biorxiv_medrxiv"
        else:
            venue = "other"
        cand_authors = _lastnames_from_authors(
            (rec.get("authorList") or {}).get("author", []))
        out.append({"doi": doi, "venue": venue, "pdf_url": pdf_url,
                    "authors": cand_authors})
    return out


# ---------------------------------------------------------------------------
# arXiv — Atom API 标题检索（两段式同上）
# ---------------------------------------------------------------------------
def _arxiv_search(title):
    if not title or len(title.strip()) < 8:
        return []

    def _run(q_expr):
        url = ("http://export.arxiv.org/api/query?search_query="
               "%s&max_results=5&sortBy=relevance" % urllib.parse.quote(q_expr))
        try:
            return _get(url, timeout=30).decode("utf-8", "ignore")
        except Exception:
            return ""

    def _parse(text):
        out = []
        for m in re.finditer(r"<entry>(.*?)</entry>", text, re.S):
            entry = m.group(1)
            idm = re.search(r"<id>(.*?)</id>", entry, re.S)
            if not idm:
                continue
            aid = idm.group(1).strip().rsplit("/", 1)[-1]
            if not re.match(r"\d{4}\.\d{4,5}", aid):
                continue
            cand_authors = []
            for am in re.finditer(r"<author>(.*?)</author>", entry, re.S):
                nm = re.search(r"<name>(.*?)</name>", am.group(1), re.S)
                if nm:
                    toks = nm.group(1).strip().split()
                    if toks:
                        cand_authors.append(_norm_lastname(toks[-1]))
            out.append({"arxiv_id": aid, "pdf_url": "https://arxiv.org/pdf/%s" % aid,
                        "authors": cand_authors})
        return out

    out = _parse(_run('ti:"%s"' % title.strip()))
    if not out:
        toks = _title_tokens(title)
        if len(toks) >= 3:
            out = _parse(_run(" AND ".join("ti:%s" % w for w in toks)))
    return out


# ---------------------------------------------------------------------------
# enrich：对无 OA 全文的 works 逐条检索并标注预印本候选
# ---------------------------------------------------------------------------
def _needs_fallback(w):
    """无 OA 全文的文献才需要预印本候选。"""
    if not isinstance(w, dict):
        return False
    if w.get("open_access_url"):
        return False
    if w.get("is_oa"):
        return False
    # 已标注过的（重跑 / 历史回填）不重复检索
    if w.get("preprint"):
        return False
    return bool(w.get("title"))


def enrich(works, biorxiv=True, medrxiv=True, arxiv=True,
           progress=None, limit=None):
    """为 works 中的非 OA 文献标注预印本候选。返回 stats dict。

    Args:
        works: normalize.merge 输出的统一 works 列表（就地修改）。
        biorxiv/medrxiv/arxiv: 各服务器开关（任一开启才发起检索）。
        progress: 可选回调 fn(msg)（CLI 打印进度）。
        limit: 最多处理的文献数（None = 全部；预印本检索按标题逐条发请求，
               大结果集时可限流）。
    Returns:
        {"scanned", "candidates", "rejected", "skipped_no_authors", "servers"}
    """
    if not (biorxiv or medrxiv or arxiv):
        return {"scanned": 0, "candidates": 0, "rejected": 0,
                "skipped_no_authors": 0, "servers": []}
    stats = {"scanned": 0, "candidates": 0, "rejected": 0,
             "skipped_no_authors": 0,
             "servers": [s for s, on in (("biorxiv", biorxiv), ("medrxiv", medrxiv),
                                         ("arxiv", arxiv)) if on]}
    for w in works:
        if limit is not None and stats["scanned"] >= limit:
            break
        if not _needs_fallback(w):
            continue
        stats["scanned"] += 1
        title = (w.get("title") or "").strip()
        orig_ln = _lastnames_from_authors(w.get("authors") or [])
        if not orig_ln:
            # 宁可缺漏：无原始作者可校验 → 不标注任何候选（不能弄错）
            stats["skipped_no_authors"] += 1
            continue
        candidates = []
        if biorxiv or medrxiv:
            for c in _epmc_preprint_search(title):
                v = c["venue"]
                if (v == "biorxiv" and biorxiv) or (v == "medrxiv" and medrxiv) \
                        or (v == "biorxiv_medrxiv" and (biorxiv or medrxiv)):
                    candidates.append(c)
        if arxiv:
            for c in _arxiv_search(title):
                candidates.append({"venue": "arxiv", "pdf_url": c["pdf_url"],
                                   "authors": c["authors"], "arxiv_id": c["arxiv_id"],
                                   "doi": ""})
        if progress:
            progress("[preprint] %d candidate(s) for %r" % (len(candidates), title[:60]))
        for c in candidates:
            passed, reason = _author_check(
                orig_ln, _lastnames_from_authors(c.get("authors") or []))
            if not passed:
                stats["rejected"] += 1
                continue
            # CSHL 双库模糊命中（biorxiv_medrxiv）按 DOI 前缀不可分辨时统一标 biorxiv_medrxiv
            w["preprint"] = {
                "venue": c["venue"],
                "doi": c.get("doi") or "",
                "arxiv_id": c.get("arxiv_id") or "",
                "url": c.get("pdf_url") or (
                    ("https://doi.org/" + c["doi"]) if c.get("doi") else ""),
                "author_check": reason,
            }
            stats["candidates"] += 1
            break  # 一篇文献只取第一个通过校验的候选
    return stats
