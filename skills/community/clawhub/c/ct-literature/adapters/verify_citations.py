#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""verify_citations.py — citation verification (anti-hallucination, ct-base §17.1).

Each merged work is checked against its public identifier(s):
  - doi        -> resolves via https://doi.org/<doi> (final HTTP 2xx: 200 OK or 206
                 Partial Content after redirects; big publishers answer a Range request
                 with 206, which still means the DOI is live)
  - pmid       -> resolves via Europe PMC EXT_ID lookup (JSON)
  - OpenAlex id -> resolves via api.openalex.org/works/<id> (JSON)

Each work gets additive fields:
  citation_verified       (bool)
  citation_verify_status   "verified" | "unresolved" | "no_identifier" | "suspicious"
                            | "bot_blocked" | "mismatch" | "retracted" | "not_found"
  citation_verify_note     (str, human readable)
  citation_consistency     (bool | None)  title/author cross-check result
  citation_title_ratio    (float | None)  normalized title similarity to the resolved paper

Title/author consistency (anti-hallucination depth): once an identifier resolves to a
LIVE resource, we fetch that resource's canonical metadata (title + first-author surname)
from the authoritative, bot-friendly API — Crossref for DOIs, Europe PMC for PMIDs,
OpenAlex for OpenAlex ids — and compare it to the work we hold. A resolved-but-mismatched
identifier (e.g. a real-but-wrong DOI, or a hallucinated DOI that happens to exist) is
flagged ``mismatch`` instead of ``verified``. Metadata-fetch failures degrade gracefully
to "verified, consistency unchecked" — they NEVER invent a mismatch.

Network runs ONLY when run=True (SAFE PREVIEW). A single verification failure marks
that work "unresolved" — it never aborts the whole pipeline. Pure stdlib + http_utils.
"""
import os
import re
import sys
import difflib
import threading
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from adapters import http_utils  # shared GET + retry; UA; get_json

_DOI_RE = re.compile(r"10\.\d{4,9}/[^\s]+")
_OA_ID_RE = re.compile(r"W\d+")


def _strip_doi_tail(s):
    """Drop a trailing terminal punctuation a source may have appended to a DOI
    (e.g. "10.1056/NEJMoa2403614."). Split into two rstrip calls so the bracket
    chars never sit adjacent to a string-quote (avoids an accidental tokenization)."""
    return s.rstrip(".,;:").rstrip(")]")


_ESUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"


def _crossref_retracted(msg):
    """CrossRef 撤稿判定（多标记，覆盖 retraction-watch）。

    反向移植自 meta-analysis ``ref_verify.py``（P4，2026-11-03），并修复其漏检：
    meta 原实现只查 ``"retraction"`` 子串，而 CrossRef 对撤稿文献实际有多种标记形态——
    ``type=retracted-article`` / ``title`` 前缀 ``"RETRACTED:"`` /
    ``relation.is-retraction-of`` / ``updated-by[].type="retraction"``（retraction-watch
    源）/ ``update-to[].type="retraction"``（**publisher 撤稿标记**）。
    **``"RETRACTED"`` 不含 ``"retraction"`` 子串**，故原检查对最常见的两种形态
    漏检（2026-11-03 用 Wakefield Lancet 1998 实测确认：title 前缀 RETRACTED、
    relation 为空、只有 updated-by 带 retraction）。这里统一用 ``"retract"`` 前缀匹配，
    覆盖 retract / retracted / retraction。

    2026-11-05 补 ``update-to``：Surgisphere Lancet 2020 撤稿论文的 publisher 撤稿标记
    只在 ``update-to``（``updated-by`` 是 retraction-watch 的 expression_of_concern），
    故原实现虽靠 title 前缀侥幸检出该篇，但遇到 title 未加前缀的撤稿文仍会漏。
    与 coze 侧 ``citation_verify_node._crossref_is_retracted`` 保持同源。
    """
    if not msg:
        return False
    rtype = str(msg.get("type") or "").lower()
    if "retract" in rtype:
        return True
    title = str((msg.get("title") or [""])[0] or "").lower()
    if title.startswith(("retracted", "withdrawn")):
        return True
    for ri in (msg.get("relation") or {}).get("is-retraction-of", []) or []:
        if ri:
            return True
    for key in ("updated-by", "update-to"):
        for item in (msg.get(key) or []):
            if "retract" in str((item or {}).get("type") or "").lower():
                return True
    return False


def _pubmed_retracted(rec):
    """PubMed 撤稿判定：``pubtype`` 含 ``Retracted Publication``（NCBI 官方标记）。

    反向移植自 meta-analysis ``ref_verify.py``（P4，2026-11-03），并修复其漏检：
    meta 原实现查 ``"retraction"`` 子串，而 NCBI 实际返回 ``"Retracted Publication"``
    （``"retracted"`` 不含 ``"retraction"`` 子串）→ 漏检。统一用 ``"retract"`` 前缀。
    """
    for p in (rec or {}).get("pubtype") or []:
        if "retract" in str(p).lower():
            return True
    return False


def _pubmed_summary(pmid, timeout=15):
    """PubMed esummary：取 PMID 的元数据 + 撤稿标记（NCBI 通道）。

    lit 的 ``_resolve_pmid`` 走 Europe PMC（search result 无撤稿字段，只有
    ``pubType=journal article``），而 PubMed 的 ``pubtype`` 是 NCBI 官方的撤稿标记，
    故撤稿检测需补这条通道。失败返回 None（不阻塞主流程）。
    """
    pmid = str(pmid or "").strip()
    if not pmid.isdigit():
        return None
    url = "%s?db=pubmed&id=%s&retmode=json" % (_ESUMMARY_URL, urllib.parse.quote(pmid))
    try:
        j = http_utils.get_json(url, headers={"User-Agent": http_utils.UA},
                                timeout=timeout, max_retries=2)
        return (j.get("result") or {}).get(pmid) or None
    except Exception:
        return None


_PUBMED_RETRACT_CACHE = {}


def _pmid_retracted(pmid, timeout=15):
    """PMID 撤稿判定（PubMed esummary pubtype）。进程内缓存，同一 PMID 只查一次。"""
    key = str(pmid)
    if key in _PUBMED_RETRACT_CACHE:
        return _PUBMED_RETRACT_CACHE[key]
    rec = _pubmed_summary(pmid, timeout)
    flag = _pubmed_retracted(rec) if rec else False
    _PUBMED_RETRACT_CACHE[key] = flag
    return flag


def _cross_check_ids(doi, pmid, timeout=15):
    """DOI+PMID 双侧交叉验证（meta-analysis 独有能力，P4 反向移植）。

    防「拼接幻觉」：DOI 与 PMID 指向不同文献（DOI 是真的、PMID 也是真的，但两者
    不是同一篇）。返回 ``(ok, note)``；``ok=None`` 表示元数据不足、无法判定
    （不阻断，避免把「查不到」误判为「不一致」）。
    """
    if not (doi and pmid):
        return None, ""
    rec = _pubmed_summary(pmid, timeout)
    if not rec:
        return None, ""
    notes = []
    pdoi = None
    for aid in (rec.get("articleids") or []):
        if str(aid.get("idtype")).lower() == "doi":
            pdoi = aid.get("value")
            break
    if pdoi:
        a = _strip_doi_tail(str(pdoi)).lower().strip()
        b = _strip_doi_tail(str(doi)).lower().strip()
        if a and b and a != b and not b.startswith(a) and not a.startswith(b):
            notes.append("DOI 交叉不一致：传入 %s，PubMed 记录 %s" % (b, a))
    if notes:
        return False, "；".join(notes)
    return None, ""


def _resolve_doi(doi, timeout=15):
    """Resolve a DOI, returning one of: ``"ok"`` | ``"bot_blocked"`` | ``"unresolved"``.

    - ``"ok"``: final HTTP 2xx (200 OK or 206 Partial Content after the
      doi.org 302 redirect). Major publishers answer a ``Range: bytes=0-0``
      probe with 206 — that is still a live, resolvable DOI.
    - ``"bot_blocked"``: doi.org redirected to a *real* publisher page, but that
      publisher returned **403** to a programmatic request. The DOI EXISTS
      (the redirect succeeded; the publisher simply will not serve content to
      bots). This is a FALSE NEGATIVE and must be reported distinctly from a
      genuinely missing identifier — NEJM / JCO / JAMA / JNCCN / Wiley / MDPI
      all do this, so the most authoritative, highest-cited papers get caught
      here, not because they are suspect but because they are bot-blocked.
    - ``"unresolved"``: the DOI did not resolve to a live resource (404 / 410 /
      5xx), or the string was not a recognizable DOI at all.

    *P4 反向移植（2026-11-03）``"not_found"``：404/410 与其它失败分开——只有
    "API 明确未收录" 才可被下游判为「疑似虚构」；网络不可达/5xx 必须留在
    ``"unresolved"``（不得当作不存在，否则断网时真实文献会被误判）。

    Robust to mixed DOI formats: OpenAlex stores the full URL
    (https://doi.org/10.x/...), Europe PMC stores the bare DOI (10.x/...).
    We extract the canonical 10.x/... suffix via _DOI_RE and always build the
    resolution URL ourselves, so no double-prefix can occur.
    """
    raw = str(doi).strip()
    m = _DOI_RE.search(raw)
    if not m:
        # not a recognizable DOI — leave malformed/None handling to the caller
        return "unresolved"
    # strip a trailing terminal punctuation a source may have appended to the DOI
    # (e.g. "10.1056/NEJMoa2403614.") so the resolution URL is clean.
    url = "https://doi.org/" + _strip_doi_tail(m.group(0))
    hdrs = {"User-Agent": http_utils.UA, "Range": "bytes=0-0"}
    try:
        # pooled request: manual redirect following (doi.org 302 -> publisher),
        # keep-alive connection reuse; 4xx/5xx raise HTTPError, network issues
        # raise URLError — semantics identical to the old urllib.urlopen path.
        http_utils._pooled_request(url, hdrs, timeout)
        # 2xx (200 OK or 206 Partial Content) => resolved live resource
        return "ok"
    except urllib.error.HTTPError as e:
        # urllib raises HTTPError for any 4xx/5xx final status (post-redirect).
        # A 403 from the publisher is bot-blocking; 404/410 mean the DOI is gone.
        try:
            e.close()
        except Exception:
            pass
        if e.code == 403:
            return "bot_blocked"
        if e.code in (404, 410):
            return "not_found"     # API 明确未收录（可怀疑虚构）
        return "unresolved"        # 5xx / 其他 4xx → 未能核验（不判虚构）
    except Exception:
        return "unresolved"        # 网络不可达 → 未能核验


def _resolve_pmid(pmid, timeout=15):
    """Resolve a PMID via Europe PMC EXT_ID lookup.

    Returns ``(ok, meta)`` where ``meta`` is ``(title, [surnames], "Europe PMC")`` or
    None. Reusing the same response for the consistency check avoids a second call.
    """
    url = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%s"
           "&format=json&pageSize=1") % urllib.parse.quote("EXT_ID:%s" % pmid)
    try:
        j = http_utils.get_json(url, headers={"User-Agent": http_utils.UA},
                                timeout=timeout, max_retries=2)
        res = (j.get("resultList") or {}).get("result") or []
        if not res:
            return False, None
        r0 = res[0]
        title = r0.get("title", "")
        al = (r0.get("authorList") or {}).get("author") or []
        surnames = [a.get("lastName", "") for a in al if a.get("lastName")]
        meta = (title, surnames, "Europe PMC") if (title or surnames) else None
        return True, meta
    except Exception:
        return False, None


def _fetch_meta_doi(doi, timeout=15):
    """Fetch canonical title + author surnames for a DOI from Crossref (bot-friendly).

    Returns ``(title, [surnames], "Crossref", is_retracted)`` or None on any failure /
    missing fields. The retraction flag is read from the SAME CrossRef response (no
    extra call). Crossref is used (not doi.org content negotiation) because it returns
    cleanly structured ``title[0]`` + ``author[].family`` even when the publisher
    bot-blocks doi.org with a 403 — so a ``bot_blocked`` DOI can STILL be
    consistency-checked.
    """
    m = _DOI_RE.search(str(doi))
    if not m:
        return None
    bare = _strip_doi_tail(m.group(0))
    url = "https://api.crossref.org/works/%s" % urllib.parse.quote(bare)
    try:
        j = http_utils.get_json(url, headers={"User-Agent": http_utils.UA},
                                timeout=timeout, max_retries=2)
        msg = (j.get("message") or {})
        title = (msg.get("title") or [""])[0] if msg.get("title") else ""
        surnames = [a.get("family", "") for a in (msg.get("author") or [])
                    if a.get("family")]
        if not title and not surnames:
            return None
        return (title, surnames, "Crossref", _crossref_retracted(msg))
    except Exception:
        return None


def _resolve_openalex(oid, timeout=15):
    """Resolve an OpenAlex id via api.openalex.org/works/<id>.

    Returns ``(ok, meta)`` where ``meta`` is ``(title, [surnames], "OpenAlex")`` or None.
    """
    m = _OA_ID_RE.search(str(oid))
    if not m:
        return False, None
    url = "https://api.openalex.org/works/%s" % m.group(0)
    try:
        j = http_utils.get_json(url, headers={"User-Agent": http_utils.UA},
                                timeout=timeout, max_retries=2)
        title = j.get("title", "")
        auths = j.get("authorships") or []
        surnames = []
        for a in auths:
            dn = (a.get("author") or {}).get("display_name") or ""
            if dn:
                toks = _norm_name(dn).split()
                if toks:
                    surnames.append(toks[-1])
        meta = (title, surnames, "OpenAlex") if (title or surnames) else None
        return True, meta
    except Exception:
        return False, None


# ---------------------------------------------------------------------------
# Title / author consistency check (anti-hallucination depth)
# ---------------------------------------------------------------------------
_TITLE_THRESHOLD = 0.80  # normalized title similarity needed to call it "the same paper"
_AUTHOR_THRESHOLD = 0.85  # first-author surname fuzzy-match threshold
# 团体 / 协作组署名（"CheckMate 057 Investigators" 等）不是可比的姓氏信号，
# 不得据此断定作者矛盾（2026-11-04 与 Coze 0.3.98 citation_verify_node 同源修复）。
_GROUP_HINT = ("investigators", "consortium", "collaborat", "group", "study",
               "trial", "team", "committee", "et al")


def _fold_unicode(s):
    """NFKD-fold a string down to ASCII letters: 'Jänne' -> 'janne', 'Núñez' -> 'nunez'.

    WHY: the old pipeline ran ``re.sub(r"[^a-z\\s]", " ", ...)`` directly on raw Unicode,
    so any diacritic became a *word break* — "Jänne" collapsed to ``"j nne"`` and could
    never match token "janne" from the resolved metadata. That silently flagged real
    papers (2026-09-08: NEJM FLAURA2 OS, doi 10.1056/nejmoa2510308, Pasi A. Jänne) as
    ``mismatch`` / "possible hallucinated id". Folding first keeps ASCII behaviour
    byte-identical while making accented surnames comparable.
    """
    try:
        import unicodedata
        decomposed = unicodedata.normalize("NFKD", str(s))
        return "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    except Exception:
        return str(s)


def _norm_title(s):
    if not s:
        return ""
    s = _fold_unicode(s).lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _norm_name(s):
    if not s:
        return ""
    s = _fold_unicode(s).lower()
    s = re.sub(r"[^a-z\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _first_author_tokens(authors):
    """Return ``(tokens_set, longest_token)`` for the FIRST author of a messy field.

    Handles "Last, First", "First Last", "First Initial", and list-of-strings. Order
    independent so both "Ramalingam V" and "V Ramalingam" surface "ramalingam".
    """
    if not authors:
        return set(), ""
    if isinstance(authors, list):
        authors = authors[0] if authors else ""
    if not authors:
        return set(), ""
    first = str(authors).split(",")[0].split(";")[0].strip()
    toks = [t for t in _norm_name(first).split() if t]
    return set(toks), (max(toks, key=len) if toks else "")


def _first_surname(surnames):
    """From a metadata surname list, return the normalized FIRST surname (or '')."""
    if not surnames:
        return ""
    if isinstance(surnames, list):
        for s in surnames:
            n = _norm_name(s)
            if n:
                return n
    return _norm_name(surnames)


def _author_ok(work_authors, meta_surname):
    """First-author check: True / False / None (None = inconclusive, never vetoes).

    2026-11-04 根因修复（与 Coze 0.3.98 citation_verify_node._author_ok 同源对齐）：
    CheckMate 057 ``authors=["Borghaei H"]`` + 正确标题被判 ``mismatch``。旧实现有
    两处缺陷 —— ① 把**元数据姓氏整体**（"Borghaei Hossein" / "Borghaei, H"）当成
    一个字符串去和 work 侧**单个** token 做 SequenceMatcher，长串把相似度稀释到
    阈值以下；② 把「分数不足」直接当成 False，灰色地带没有 None，于是弱作者信号
    一票否决已过标题阈值的真实文献。

    现改为姓氏 token 级双向比对：两侧都拆 token、丢弃单字母 initials；命中即 True；
    仅当两侧都是实词姓氏且明显不同才 False；其余灰色地带返回 None（不断定），让标题
    主导判断。团体署名不作为姓氏信号。幻觉 id 指向他文的反幻觉能力仍由「纯姓氏明显
    矛盾 → False」保留。
    """
    ms = _norm_name(meta_surname)
    if not ms:
        return None
    toks, _ = _first_author_tokens(work_authors)
    if not toks:
        return None
    if any(h in ms for h in _GROUP_HINT):
        return None
    # 本地历史 fix 保留：空格剥离等价，处理 NFKD 残余 token 分裂（"j nne" ↔ "jnne"）。
    if ms in toks or ms.replace(" ", "") in {t.replace(" ", "") for t in toks}:
        return True
    # 单字母 token 是 initials（"h" / "pa"），不参与姓氏比对。
    meta_toks = [t for t in ms.split() if len(t) >= 2]
    work_toks = [t for t in toks if len(t) >= 2]
    if not meta_toks or not work_toks:
        return None
    # ① token 级精确命中："borghaei hossein" ↔ {"borghaei", "h"} 命中 borghaei
    if set(meta_toks) & set(work_toks):
        return True
    # ② 模糊兜底：token × token 取最高，不再让整体长串稀释分值
    best = max((difflib.SequenceMatcher(None, m, w).ratio()
                for m in meta_toks for w in work_toks), default=0.0)
    if best >= _AUTHOR_THRESHOLD:
        return True
    # ③ 仅「双方各为实词姓氏且明显不同」才断定矛盾；其余不断定，
    #    避免弱作者信号误杀真实文献（反幻觉主要靠标题阈值把关）。
    m_best = max(meta_toks, key=len)
    w_best = max(work_toks, key=len)
    if len(m_best) >= 3 and len(w_best) >= 3 and best < 0.5:
        return False
    return None


def _consistency(work, meta):
    """Compare the work we hold against the resolved paper's canonical metadata.

    ``meta`` is ``(title, [surnames], source)`` or, from ``_fetch_meta_doi``, a
    4-tuple with a trailing ``is_retracted`` flag — the first three items are used,
    so both shapes are accepted. Returns a dict with ``consistent`` (bool | None —
    None when metadata is too incomplete to judge), ``title_ratio`` and ``author_ok``.
    """
    title, surnames, source = (meta or (None, None, None))[:3]
    wt = _norm_title(work.get("title"))
    mt = _norm_title(title)
    if not wt or not mt:
        return {"consistent": None, "title_ratio": None, "author_ok": None, "source": source}
    ratio = difflib.SequenceMatcher(None, wt, mt).ratio()
    ms = _first_surname(surnames)
    author_ok = _author_ok(work.get("authors"), ms)
    # Title must match; author must NOT contradict (an unknown author signal is not fatal).
    consistent = (ratio >= _TITLE_THRESHOLD) and (author_ok is not False)
    return {"consistent": consistent, "title_ratio": round(ratio, 3),
            "author_ok": author_ok, "source": source}


def _emit(work, via, base_status, meta, check_consistency, is_retracted=False):
    """Build the citation_* result after a positive identifier resolution.

    - ``meta is None`` or ``check_consistency=False``  -> keep ``base_status`` (verified /
      bot_blocked), note "consistency unchecked".
    - metadata present + consistent -> status "verified" (a bot_blocked DOI is upgraded
      to fully verified once its title/author are confirmed).
    - metadata present + MISMATCH  -> status "mismatch", citation_verified=False.
    - ``is_retracted=True`` -> status "retracted"（**最高优先级**：撤稿文献即使标题吻
      合也不得作为证据）。保留一致性判定供人工参考。
    """
    via_note = {"doi": "doi resolved", "pmid": "pmid resolved",
                "openalex": "openalex-id resolved"}[via]
    out = {"citation_verified": True, "citation_verify_status": base_status,
           "citation_verify_note": via_note,
           "citation_consistency": None, "citation_title_ratio": None}
    # 回写 API 解析出的真实元数据（P4：让 lit work 自描述，供 meta-analysis 等
    # 下游直接采纳，避免执行层归一后丢失本地引擎原有的 API 值；纯新增、向后兼容）。
    # meta 为 None（元数据抓取失败）时不回写——下游保留输入值自行处理。
    if meta:
        _mt = (meta or (None, None))[0]
        _ms = (meta or (None, None))[1]
        if _mt:
            out["verified_title"] = _mt
        _s0 = None
        if isinstance(_ms, list):
            _s0 = next((s for s in _ms if s), None)
        elif _ms:
            _s0 = _ms
        if _s0:
            out["verified_first_author"] = _s0
    if not check_consistency or meta is None:
        if check_consistency and meta is None:
            out["citation_verify_note"] = via_note + "; consistency unchecked (metadata unavailable)"
        return _apply_retraction(out, is_retracted)
    cmp = _consistency(work, meta)
    out["citation_title_ratio"] = cmp["title_ratio"]
    if cmp["consistent"] is None:
        out["citation_consistency"] = None
        out["citation_verify_note"] = via_note + "; consistency unchecked (metadata incomplete)"
        return _apply_retraction(out, is_retracted)
    if cmp["consistent"]:
        out["citation_verify_status"] = "verified"  # upgrade bot_blocked -> verified
        out["citation_consistency"] = True
        out["citation_verify_note"] = ("%s; title/author consistent (%s, ratio=%.2f)"
                                       % (via_note, cmp["source"], cmp["title_ratio"]))
    else:
        out["citation_verify_status"] = "mismatch"
        out["citation_verified"] = False
        out["citation_consistency"] = False
        out["citation_verify_note"] = (
            "%s but TITLE/AUTHOR MISMATCH (%s, ratio=%.2f) — identifier resolves to a "
            "different paper; possible hallucinated/incorrect id"
            % (via_note, cmp["source"], cmp["title_ratio"]))
    return _apply_retraction(out, is_retracted)


def _apply_retraction(out, is_retracted):
    """撤稿优先：撤稿文献即使标题吻合也不得作为证据（红线）。

    保留 ``citation_consistency`` / ``citation_title_ratio`` 供人工参考，但 status 与
    ``citation_verified`` 必须反映撤稿。
    """
    if not is_retracted:
        return out
    out = dict(out)
    out["citation_verified"] = False
    out["citation_verify_status"] = "retracted"
    out["citation_verify_note"] = (
        (out.get("citation_verify_note") or "") + "; RETRACTED (per CrossRef/PubMed)")
    return out


def verify_one(work, timeout=15, skip_sources=None, check_consistency=True,
               check_retraction=True, cross_check=False):
    """Return the citation_* fields for one work (dict).

    Verification order (first positive wins), with title/author consistency depth:
      DOI (via doi.org)  -> fetch Crossref metadata
        -> PMID (Europe PMC EXT_ID, bot-friendly) -> reuse its metadata
        -> OpenAlex id (api.openalex.org, bot-friendly) -> reuse its metadata

    skip_sources is retained for API compatibility but no longer suppresses the
    reliable same-source fallback. When the DOI fails — and the dominant failure
    on big publishers is exactly a 403 bot-block while the Europe PMC / OpenAlex
    APIs still resolve cleanly — the PMID / OpenAlex id are the dependable
    bot-friendly path and MUST be tried. Skipping them produced false negatives
    (e.g. a Europe PMC work whose real PMID was never checked because its DOI
    hit a 403). See ct-literature CHANGELOG v0.6.6.

    After a positive resolution, if ``check_consistency`` is True we fetch the
    resolved paper's canonical metadata and compare title + first-author surname
    (see ``_emit`` / ``_consistency``). A resolved-but-different paper becomes
    ``mismatch`` instead of ``verified`` — this is the catch for a real-but-wrong
    or hallucinated DOI that still resolves to a LIVE resource.

    citation_verify_status values:
      verified      — identifier resolved AND title/author consistent (bot_blocked
                      DOIs are upgraded to verified once Crossref confirms them)
      bot_blocked   — DOI redirected to a real publisher but that publisher
                      returned 403 to a programmatic request; the DOI is REAL
                      (false negative, not a suspect/missing identifier)
      mismatch      — identifier resolved to a LIVE resource but its title/author
                      do NOT match this work (possible hallucinated/incorrect id)
      unresolved    — no identifier resolved to a live resource
      not_found     — DOI 被 API 明确返回 404/410（**可怀疑虚构**；P4 反向移植自
                      meta-analysis，与 unresolved 分开以避免离线误杀）
      no_identifier — the work carried no doi/pmid/openalex-id at all
      suspicious    — the DOI string was malformed (possible hallucinated id)
      retracted     — 已撤稿（**优先级最高**，覆盖 verified；P4 反向移植自 meta-analysis：
                      CrossRef updated-by / title 前缀 / relation / type + PubMed pubtype）

    ``check_retraction``（默认 True）启用撤稿检测：DOI 用 CrossRef **同一响应**的
    updated-by / title / relation / type（无额外调用）；PMID 补一条 PubMed esummary
    （Europe PMC search result 无撤稿字段）。``cross_check``（默认 False）启用
    DOI+PMID 双侧交叉验证（meta 独有能力，P4 反向移植）——仅两者同时存在时生效，
    防「拼接幻觉」。
    """
    doi = work.get("doi")
    pmid = work.get("pmid")
    oid = work.get("id") or ""
    skip = set(skip_sources or [])

    # malformed DOI => suspicious (possible hallucinated identifier)
    if doi and not _DOI_RE.search(str(doi)):
        return _with_doi_flags({"citation_verified": False,
                "citation_verify_status": "suspicious",
                "citation_verify_note": "malformed DOI: %s" % doi,
                "citation_consistency": False, "citation_title_ratio": None}, doi)

    # DOI first (canonical cross-source id). ok / bot_blocked both mean the DOI is
    # REAL; either way we can still pull Crossref metadata for the consistency check
    # (Crossref is bot-friendly even when the publisher bot-blocks doi.org).
    # ── 双侧交叉验证（meta 独有能力，P4 反向移植）──
    if cross_check and doi and pmid:
        xok, xnote = _cross_check_ids(doi, pmid, timeout)
        if xok is False:
            return _with_doi_flags({
                "citation_verified": False, "citation_verify_status": "mismatch",
                "citation_verify_note": xnote or "DOI/PMID 交叉不一致",
                "citation_consistency": False, "citation_title_ratio": None}, doi)

    doi_state = None
    if doi:
        st = _resolve_doi(doi, timeout)
        doi_state = st
        if st in ("ok", "bot_blocked"):
            meta = _fetch_meta_doi(doi, timeout)
            retracted = bool(check_retraction and meta and meta[3])
            return _with_doi_flags(
                _emit(work, "doi", "verified" if st == "ok" else "bot_blocked",
                      meta, check_consistency, is_retracted=retracted), doi)

    # PMID + OpenAlex id: reliable, bot-friendly API lookups. Always attempt when
    # the DOI did NOT positively verify — the fallback that keeps real papers from
    # being mislabeled "unresolved". Their responses already carry the metadata we
    # need for the consistency check (no extra call).
    if pmid:
        ok, meta = _resolve_pmid(pmid, timeout)
        if ok:
            retracted = bool(check_retraction and _pmid_retracted(pmid, timeout))
            return _emit(work, "pmid", "verified", meta, check_consistency,
                         is_retracted=retracted)
    if oid:
        ok, meta = _resolve_openalex(oid, timeout)
        if ok:
            return _emit(work, "openalex", "verified", meta, check_consistency)

    notes = []
    if doi:
        notes.append("doi-unresolved")
    if pmid:
        notes.append("pmid-unresolved")
    if oid:
        notes.append("openalex-unresolved")
    if not (doi or pmid or oid):
        return {"citation_verified": False, "citation_verify_status": "no_identifier",
                "citation_verify_note": "no doi/pmid/openalex-id",
                "citation_consistency": None, "citation_title_ratio": None}
    # DOI 明确未收录（404/410）且无其他标识成功 → not_found（才可怀疑虚构）
    if doi_state == "not_found":
        return {"citation_verified": False, "citation_verify_status": "not_found",
                "citation_verify_note": "DOI did not resolve (404/410)",
                "citation_consistency": None, "citation_title_ratio": None}
    return {"citation_verified": False, "citation_verify_status": "unresolved",
            "citation_verify_note": "; ".join(notes) or "could not verify",
            "citation_consistency": None, "citation_title_ratio": None}


def verify_doi_only(work, timeout=15):
    """DOI-scoped verification (used by scripts/verify_dois.py, `--verify-dois`).

    Resolves the DOI and Crossref-checks title + first-author surname, returning the
    additive ``doi_*`` fields. Unlike ``verify_one`` it NEVER falls back to the
    PMID / OpenAlex path — a work without a resolvable DOI is reported as such, which
    is exactly what a DOI-focused audit wants. Network runs only when called.
    """
    doi = work.get("doi")
    if not doi:
        return {"doi": None, "doi_checked": False, "doi_verified": False,
                "doi_mismatch": False, "doi_mismatch_note": "no DOI on this work"}
    if not _DOI_RE.search(str(doi)):
        return _with_doi_flags({"citation_verified": False,
                "citation_verify_status": "suspicious",
                "citation_verify_note": "malformed DOI: %s" % doi,
                "citation_consistency": False, "citation_title_ratio": None}, doi)
    st = _resolve_doi(doi, timeout)
    if st not in ("ok", "bot_blocked"):
        return _with_doi_flags({"citation_verified": False,
                "citation_verify_status": "unresolved",
                "citation_verify_note": "DOI did not resolve to a live resource",
                "citation_consistency": None, "citation_title_ratio": None}, doi)
    meta = _fetch_meta_doi(doi, timeout)
    retracted = bool(meta and meta[3])
    return _with_doi_flags(
        _emit(work, "doi", "verified" if st == "ok" else "bot_blocked", meta, True,
              is_retracted=retracted), doi)


def work_key(work):
    """Stable key for a work, used to attach verification results across
    merge/dedupe (the same paper may arrive from two sources).

    Priority: doi -> pmid -> OpenAlex id -> normalized title -> object id.
    """
    doi = work.get("doi")
    if doi:
        # normalize mixed formats: OpenAlex stores "https://doi.org/10.x/..." while
        # Europe PMC stores bare "10.x/...". Extract the canonical suffix so both
        # forms of the same paper share one key. Strip a trailing terminal
        # punctuation a source may have appended (e.g. "10.1056/x.").
        m = _DOI_RE.search(str(doi))
        _bare = (_strip_doi_tail(m.group(0)) if m else str(doi))
        return "doi:" + _bare.lower().strip()
    pmid = work.get("pmid")
    if pmid:
        return "pmid:" + str(pmid)
    oid = work.get("id") or ""
    m = _OA_ID_RE.search(str(oid))
    if m:
        return "oa:" + m.group(0)
    title = work.get("title")
    if title:
        return "title:" + re.sub(r"\s+", " ", str(title)).strip().lower()
    return "idx:" + str(id(work))


def summarize_results(results_map):
    """Build the verification summary dict from a {key: verify_one_result} map."""
    s = {"total": 0, "verified": 0, "bot_blocked": 0, "unresolved": 0,
         "no_identifier": 0, "suspicious": 0, "mismatch": 0, "not_found": 0,
         "retracted": 0, "skipped_preview": False}
    for r in results_map.values():
        s["total"] += 1
        st = r.get("citation_verify_status", "unresolved")
        s[st] = s.get(st, 0) + 1
    return s


def _with_doi_flags(res, doi):
    """Add DOI-specific additive fields on top of a citation-verify result.

    Consumed by the DOI-focused report (`scripts/verify_dois.py` + `--verify-dois`).
    Purely additive — older consumers ignore these keys. ``doi_verified`` answers
    "does this DOI resolve AND match the paper we hold?"; ``doi_mismatch`` isolates
    the real-but-wrong / hallucinated-DOI case (the error the ct-literature error
    table calls "DOI dedupe merged too aggressively / shared DOI typo").
    """
    st = res.get("citation_verify_status")
    res = dict(res)
    res["doi"] = (str(doi).strip() if doi else None)
    res["doi_checked"] = True
    res["doi_verified"] = bool(res.get("citation_verified"))
    res["doi_mismatch"] = (st == "mismatch")
    if st == "mismatch":
        res["doi_mismatch_note"] = ("DOI resolves to a DIFFERENT paper "
                                    "(title/author mismatch) — human review advised")
    elif st == "suspicious":
        res["doi_mismatch_note"] = "malformed DOI — human review advised"
    elif st == "bot_blocked":
        res["doi_mismatch_note"] = ("publisher bot-blocked the DOI; "
                                    "existence confirmed via redirect")
    else:
        res["doi_mismatch_note"] = ""
    return res


def collect_doi_mismatches(works):
    """Return the works whose DOI resolves to a different paper (or is malformed).

    Reads the additive ``doi_mismatch`` field when present, else falls back to the
    generic ``citation_verify_status == 'mismatch'`` / ``'suspicious'`` signal so a
    report can be produced even from an older verification pass.
    """
    out = []
    for w in works or []:
        flag = w.get("doi_mismatch")
        st = w.get("citation_verify_status")
        if flag is None:
            flag = st in ("mismatch", "suspicious")
        if flag:
            out.append(w)
    return out


def render_doi_mismatch_report(works, topic=None):
    """Build a Markdown report highlighting DOI mismatches (human review list)."""
    mis = collect_doi_mismatches(works)
    total_doi = sum(1 for w in (works or []) if w.get("doi"))
    lines = ["# DOI verification report · 引文 DOI 校验报告", ""]
    if topic:
        lines.append("- **topic**: %s" % topic)
    lines.append("- **works with a DOI**: %d" % total_doi)
    lines.append("- **DOI mismatches / malformed (needs human review)**: %d" % len(mis))
    lines.append("")
    if not mis:
        lines.append("✅ 未发现 DOI 与文献标题/作者不一致的情况。")
        return "\n".join(lines) + "\n"
    lines.append("| # | DOI | 标题（截断） | 状态 | 说明 |")
    lines.append("|---|---|---|---|---|")
    for i, w in enumerate(mis, 1):
        title = str(w.get("title") or "").replace("|", "/")[:70]
        note = str(w.get("doi_mismatch_note") or w.get("citation_verify_note") or "").replace("|", "/")[:90]
        lines.append("| %d | %s | %s | ⚠️ %s | %s |"
                     % (i, w.get("doi") or "—", title,
                        w.get("citation_verify_status") or "mismatch", note))
    lines.append("")
    lines.append("> ⚠️ 以上条目建议人工复核：DOI 可能指向另一篇文献或存在笔误。")
    return "\n".join(lines) + "\n"


def attach_verifications(works, results_map):
    """In-place attach a verification result onto each merged work (matched by work_key).

    Thread-safe: results_map is populated by the consumer pool before this is called;
    verify_one never mutates the caller's work objects, so no shared state is touched here.
    """
    for w in works:
        res = results_map.get(work_key(w))
        if res:
            w.update(res)


def verify_works(works, run=True, timeout=15, skip_sources=None, check_consistency=True,
                 check_retraction=True, cross_check=False):
    """Annotate works (copy-safe) with citation_* fields. Returns (works, summary).

    summary keys: total, verified, bot_blocked, unresolved, no_identifier,
                  suspicious, mismatch, retracted, skipped_preview (bool).

    Parallelized with a bounded thread pool: per-work verification is fully
    independent (no shared work object), so the only shared mutable state is the
    ``summary`` accumulator, which is guarded by a lock. The upstream network layer
    (http_utils) already caps per-host concurrency and retries on 429/5xx, so this
    will not hammer Crossref / Europe PMC / OpenAlex. Input order is preserved in
    the returned list. SAFE PREVIEW (run=False) stays single-threaded and never
    touches the network.
    """
    summary = {"total": 0, "verified": 0, "bot_blocked": 0, "unresolved": 0,
               "no_identifier": 0, "suspicious": 0, "mismatch": 0, "not_found": 0,
               "retracted": 0, "skipped_preview": False}
    if not works:
        return [], summary
    if not run:
        # SAFE PREVIEW: copy only, no network, total stays 0.
        summary["skipped_preview"] = True
        return [dict(w) for w in works], summary

    n = len(works)
    _nw = min(8, n)
    out = [None] * n
    _lock = threading.Lock()

    def _verify_at(idx, w):
        wc = dict(w)  # copy-safe: never mutate the caller's work object
        res = verify_one(wc, timeout=timeout, skip_sources=skip_sources,
                         check_consistency=check_consistency,
                         check_retraction=check_retraction, cross_check=cross_check)
        wc.update(res)
        return idx, wc, res

    with ThreadPoolExecutor(max_workers=_nw) as _ex:
        _futs = [_ex.submit(_verify_at, i, w) for i, w in enumerate(works)]
        for _f in as_completed(_futs):
            idx, wc, res = _f.result()
            out[idx] = wc
            with _lock:
                summary["total"] += 1
                _st = res["citation_verify_status"]
                summary[_st] = summary.get(_st, 0) + 1
    return out, summary


def main():
    ap = argparse.ArgumentParser(description="Verify citation identifiers (offline-safe preview).")
    ap.add_argument("--in", default=".merged.json", dest="inp", help=".merged.json path")
    ap.add_argument("--run", action="store_true", help="perform live verification")
    ap.add_argument("--no-consistency", action="store_true",
                   help="skip title/author consistency cross-check "
                        "(⚠️ weakens the anti-hallucination guarantee; debugging only)")
    ap.add_argument("--timeout", type=int, default=15)
    args = ap.parse_args()
    import json
    data = json.load(open(args.inp, encoding="utf-8"))
    works = data.get("works", [])
    out, summary = verify_works(works, run=args.run, timeout=args.timeout,
                                check_consistency=not args.no_consistency)
    print("[verify] %s" % json.dumps(summary, ensure_ascii=False))
    if args.run:
        # write back annotated works
        data["works"] = out
        json.dump(data, open(args.inp, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        print("[OK] annotated %d works -> %s" % (len(out), args.inp))


if __name__ == "__main__":
    import argparse  # late import so module import (pipeline) stays cheap
    main()
