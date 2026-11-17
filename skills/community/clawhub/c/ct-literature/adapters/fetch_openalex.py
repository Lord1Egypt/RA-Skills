#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fetch_openalex.py — OpenAlex fetcher (primary source).

Reads the OpenAlex open scholarly graph (https://api.openalex.org/works) — a free,
citation-rich bibliographic API covering PubMed + preprint servers + many
journal full texts. OpenAlex has required an API key since 2026-02-13 (a free key
lifts the cap from 100 to 100k credits/day); provide it via --openalex-key /
OPENALEX_API_KEY / skill .env. Returns normalized work records. Zero confidential
data or information input; reads only public literature.

Unified work schema (also produced by fetch_europepmc / fetch_semantic_scholar):
  { source, id, title, authors, year, publication, type, cited_by_count,
    url, doi, abstract_snippet, mesh, is_safety }
"""
import argparse
import json
import os
import sys
import time
import re
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from adapters import http_utils  # shared GET+retry (exponential backoff, 429 Retry-After, Bearer key)

try:
    import requests  # optional; reserved for future requests-path use
except ImportError:
    requests = None

BASE = "https://api.openalex.org/works"

# Cochrane Database of Systematic Reviews — the journal's ISSN. Filtering on it is
# how the OpenAlex leg serves as a Cochrane channel independent of Europe PMC
# (verified 2026-11-03: 29,212 works carry this ISSN, each with a PMID).
COCHRANE_ISSN = "1469-493X"
COCHRANE_ISSN_FILTER = "primary_location.source.issn:%s" % COCHRANE_ISSN
COCHRANE_JOURNAL_MARK = "cochrane database of systematic reviews"

# OpenAlex type -> our coarse study_type
TYPE_MAP = {
    "article": "article",
    "review": "review",
    "book-chapter": "book-chapter",
    "proceedings": "proceedings",
    "preprint": "preprint",
    "posted-content": "preprint",
    "editorial": "editorial",
    "letter": "letter",
    "comment": "comment",
    "news": "news",
    "correction": "correction",
    "erratum": "correction",
    "dataset": "dataset",
    "report": "report",
    "reference-entry": "reference-entry",
    "peer-review": "peer-review",
}

SAFETY_LEXICON = [
    "adverse event", "adverse reaction", "side effect", "safety", "toxicity",
    "toxic", "case report", "pharmacovigilance", "drug-induced", "drug reaction",
]


def _strip_html(s):
    if not s:
        return s
    import re as _re
    return _re.sub(r"<[^>]+>", "", s)


def _openalex_type_for(review_type):
    """Map our --review-type to an OpenAlex `type:` filter (or None)."""
    if review_type in ("systematic-review", "scoping-review", "meta-analysis"):
        return "review"
    if review_type == "rct":
        return "article"
    if review_type == "case-report":
        return "article"
    return None  # all


def _study_type_from(record, review_type):
    t = record.get("type", "") or ""
    title = (record.get("title") or "").lower()
    abstract = (record.get("abstract_snippet") or "").lower()
    blob = title + " " + abstract
    if review_type in ("systematic-review", "meta-analysis", "scoping-review"):
        if "systematic review" in blob or "meta-analysis" in blob or "meta analysis" in blob:
            return {"systematic-review": "systematic-review",
                    "meta-analysis": "meta-analysis",
                    "scoping-review": "scoping-review"}[review_type]
        return "review"
    if review_type == "rct":
        if "randomized" in blob or "rct" in blob:
            return "rct"
        return "article"
    if review_type == "case-report":
        if "case report" in blob or "case series" in blob:
            return "case-report"
        return "article"
    if "systematic review" in blob or "meta-analysis" in blob:
        return "systematic-review"
    if "case report" in blob or "case series" in blob:
        return "case-report"
    if "randomized controlled trial" in blob or ("randomized" in blob and "trial" in blob):
        return "rct"
    return TYPE_MAP.get(t, t or "article")


def _flag_safety(record):
    blob = " ".join([
        record.get("title") or "",
        record.get("abstract_snippet") or "",
    ]).lower()
    return any(k in blob for k in SAFETY_LEXICON)


def _bare_doi(v):
    """OpenAlex 的 doi 字段是完整 URL（https://doi.org/10.xxxx/…）→ 剥成裸 DOI。
    2026-09-06 实测根因：未归一化会把 URL 形态 DOI 写入统一 schema，导致
    coze/EPMC 端 `DOI:"https://…"` 查询全部落空、PMC-OA 通道整批失效。"""
    if not v:
        return v
    s = str(v).strip()
    low = s.lower()
    for p in ("https://doi.org/", "http://doi.org/",
              "https://dx.doi.org/", "http://dx.doi.org/"):
        if low.startswith(p):
            return s[len(p):]
    return s


# DOI shape: 10.<digits>/<rest>  (e.g. 10.1056/NEJMoa2022847). Used by resolve_seed
# to decide whether a user-supplied seed is a DOI vs a PMID vs a free-text title.
_DOI_RE = re.compile(r"^10\.\d{4,9}/.+$")


def _looks_like_doi(s):
    return bool(_DOI_RE.match(s or ""))


def _extract(record):
    loc = record.get("primary_location") or {}
    src = loc.get("source") or {} if loc else {}
    authorships = record.get("authorships") or []
    authors = []
    for a in authorships[:6]:
        nm = (a.get("author") or {}).get("display_name")
        if nm:
            authors.append(nm)
    if len(authorships) > 6:
        authors.append("et al.")
    abstract = record.get("abstract_inverted_index")
    snippet = None
    if abstract:
        snippet = _invindex_to_text(abstract)
    title = _strip_html(record.get("title") or record.get("display_name") or "")
    # External IDs (pmid, pmcid, etc.)
    ids = record.get("ids") or {}
    # Concepts (top 5 by score)
    concepts = []
    for c in sorted(record.get("concepts") or [], key=lambda x: -(x.get("score") or 0))[:5]:
        dn = c.get("display_name")
        if dn:
            concepts.append(dn)
    # Keywords
    keywords = [k.get("display_name") for k in (record.get("keywords") or [])[:8] if k.get("display_name")]
    # Open access URL — accuracy-first (2026-09-04):
    #   1. best_oa_location.pdf_url (OpenAlex's own best guess)
    #   2. ANY locations[] entry with a pdf_url (OpenAlex sometimes parks the only
    #      PDF in a non-best location — best_oa_location alone under-reports OA)
    #   3. is_oa=True but no PDF anywhere → best_oa landing page (legit OA copy,
    #      just not a direct PDF)
    #   4. else None (the work is genuinely closed) — the generic landing page is
    #      NOT promoted into open_access_url (that was inflating false "OA" hits).
    oa_rec = record.get("open_access") or {}
    is_oa = bool(oa_rec.get("is_oa"))
    oa_status = oa_rec.get("oa_status")
    best_oa = record.get("best_oa_location") or {}
    oa_url = best_oa.get("pdf_url")
    if not oa_url:
        for _loc in record.get("locations") or []:
            u = (_loc or {}).get("pdf_url")
            if u:
                oa_url = u
                break
    if not oa_url and is_oa:
        oa_url = best_oa.get("landing_page_url")
    landing_url = best_oa.get("landing_page_url") or loc.get("landing_page_url") \
        or record.get("doi") or record.get("id")
    # Funders (top 3)
    funders = []
    for f in (record.get("funders") or [])[:3]:
        dn = f.get("display_name")
        if dn:
            funders.append(dn)
    # OpenAlex has no pubTypeList; derive a `pub_types` from its `type` so the field
    # is present and consistent with Europe PMC. Only map explicit review types to
    # avoid false positives (keeps meta-analysis B1 hard signal trustworthy).
    _oa_type = record.get("type")
    pub_types = ["Review"] if _oa_type == "review" else []
    # Biblio (volume/issue/page)
    biblio = record.get("biblio") or {}
    return {
        "source": "OpenAlex",
        "id": record.get("id"),
        "doi": _bare_doi(record.get("doi")),
        "pmid": ids.get("pubmed"),
        "pmcid": ids.get("pmcid"),
        "title": title,
        "authors": authors,
        "year": record.get("publication_year"),
        "publication_date": record.get("publication_date"),
        "publication": src.get("display_name"),
        "type": record.get("type"),
        "study_type": None,  # filled by caller via _study_type_from
        "cited_by_count": record.get("cited_by_count") or 0,
        "url": landing_url,
        "is_oa": is_oa,
        "oa_status": oa_status,
        "open_access_url": oa_url,
        "abstract_snippet": snippet,
        "mesh": None,
        "concepts": concepts or None,
        "keywords": keywords or None,
        "funders": funders or None,
        "language": record.get("language"),
        "is_retracted": record.get("is_retracted") or False,
        "volume": biblio.get("volume"),
        "issue": biblio.get("issue"),
        "page": biblio.get("first_page"),
        "is_safety": False,  # filled by caller
        "pub_types": pub_types,
    }


def _invindex_to_text(inv):
    """OpenAlex stores abstract as an inverted index; reconstruct plaintext."""
    try:
        # inv: {word: [pos1, pos2, ...]}
        # Find max position
        max_pos = max(max(positions) for positions in inv.values() if positions)
        slots = [None] * (max_pos + 1)
        for word, idxs in inv.items():
            for i in idxs:
                if i <= max_pos:
                    slots[i] = word
        return " ".join(w for w in slots if w)
    except Exception:
        return ""


def _evidence_level(w):
    """U4: evidence-level tag for a single work (mirrors normalize._evidence_level)."""
    st = (w.get("study_type") or "").lower()
    if st in ("systematic-review", "meta-analysis", "scoping-review"):
        return "systematic-review"
    if st == "rct":
        return "rct"
    if st == "cohort":
        return "cohort"
    if st == "case-report":
        return "case-report"
    if st == "case-series":
        return "case-series"
    if st == "preprint" or (w.get("type") or "").lower() == "preprint":
        return "preprint"
    if st == "review":
        return "narrative-review"
    return "other"


def _snowball_normalize(rec, seed_id, direction):
    """Normalize one OpenAlex work record into a snowball work (shared by both
    directions + the seed itself)."""
    w = _extract(rec)
    w["study_type"] = _study_type_from(rec, "all")
    w["is_safety"] = _flag_safety(w)
    w["snowball_seed"] = seed_id
    w["snowball_direction"] = direction
    w["evidence_level"] = _evidence_level(w)
    return w


def _fetch_cited_by(seed_id, max_refs, headers, mailto):
    """Forward citations: works that CITE `seed_id` (OpenAlex `filter=cites:W{id}`).

    Replaces the old `/cited_by` sub-endpoint, which (verified 2026-11-09) returns
    the single work object rather than a `results` list — so the previous code
    silently collected zero works. The `cites:` filter is the reliable path.
    """
    out = []
    per = min(max_refs, 50)
    url = "%s?filter=cites:%s&per-page=%d&mailto=%s" % (BASE, seed_id, per, mailto)
    try:
        j = http_utils.get_json(url, headers=headers, timeout=30, max_retries=3)
        for rec in (j.get("results") or [])[:max_refs]:
            out.append(_snowball_normalize(rec, seed_id, "cited_by"))
    except Exception as e:
        print("[WARN] snowball cited_by (cites:%s) failed: %s" % (seed_id, e))
    return out


def _fetch_references(seed_id, max_refs, headers, mailto):
    """Backward references: the seed's `referenced_works` expanded via
    `filter=openalex_id:|W1|W2|...` (batched ≤50/page).

    Replaces the old `/references` sub-endpoint, which (verified 2026-11-09) returns
    the single work object rather than a `results` list — so the previous code
    silently collected zero works.
    """
    out = []
    try:
        seed = http_utils.get_json("%s/%s?mailto=%s" % (BASE, seed_id, mailto),
                                   headers=headers, timeout=30, max_retries=3)
        ref_ids = (seed.get("referenced_works") or [])[:max_refs]
    except Exception as e:
        print("[WARN] snowball seed fetch (W%s) failed: %s" % (seed_id, e))
        return out
    # referenced_works already capped at max_refs → at most one batch.
    for i in range(0, len(ref_ids), 50):
        batch = ref_ids[i:i + 50]
        ids_filter = "|".join(b.strip("/").split("/")[-1] for b in batch)
        url = "%s?filter=openalex_id:%s&per-page=50&mailto=%s" % (BASE, ids_filter, mailto)
        try:
            j = http_utils.get_json(url, headers=headers, timeout=30, max_retries=3)
            for rec in (j.get("results") or []):
                out.append(_snowball_normalize(rec, seed_id, "references"))
        except Exception as e:
            print("[WARN] snowball references batch failed: %s" % e)
    return out[:max_refs]


def resolve_seed(seed, api_key=None, mailto="dev@example.com"):
    """Resolve a user-supplied seed to a single OpenAlex work + OpenAlex ID.

    Accepts three input kinds and cascades through them:
      1. DOI  -> single-work-by-DOI endpoint (URL-encoded https://doi.org/<bare>),
                 falling back to `filter=doi:<bare>`.
      2. PMID -> `filter=pmid:<v>` (all digits, len ≥ 5).
      3. else -> `filter=title.search:<v>` (free-text title / phrase).

    Returns (work_record, openalex_id) or (None, None) if nothing matched.
    `work_record` is the raw OpenAlex JSON; callers normalize via _extract.
    """
    if not seed or not str(seed).strip():
        return None, None
    if api_key is None:
        api_key = http_utils.load_openalex_key()
    headers = http_utils.build_openalex_headers(api_key=api_key, mailto=mailto)
    s = str(seed).strip()

    def _first(query_url):
        try:
            j = http_utils.get_json(query_url, headers=headers, timeout=30, max_retries=3)
        except Exception:
            return None
        if isinstance(j, dict) and j.get("id"):  # single-work endpoint → object
            return j
        res = (j or {}).get("results") or []
        return res[0] if res else None

    rec = None
    if "doi.org" in s.lower() or _looks_like_doi(s):
        bare = _bare_doi(s) if "doi.org" in s.lower() else s
        # 1a. authoritative single-work-by-DOI endpoint (DOI as a path segment)
        enc = urllib.parse.quote("https://doi.org/" + bare, safe="")
        rec = _first("%s/%s?mailto=%s" % (BASE, enc, mailto))
        # 1b. fallback: filter=doi:<bare>
        if rec is None:
            rec = _first("%s?filter=doi:%s&mailto=%s"
                         % (BASE, urllib.parse.quote(bare, safe=""), mailto))
    # 2. PMID
    if rec is None and s.isdigit() and len(s) >= 5:
        rec = _first("%s?filter=pmid:%s&mailto=%s" % (BASE, s, mailto))
    # 3. free-text title / phrase
    if rec is None:
        rec = _first("%s?filter=title.search:%s&per-page=5&mailto=%s"
                     % (BASE, urllib.parse.quote(s, safe=""), mailto))
    if rec is None:
        return None, None
    oa_id = (rec.get("id") or "").strip("/").split("/")[-1]
    return rec, oa_id


def fetch_snowball(seed_work_id, direction="both", max_refs=20, api_key=None, mailto="dev@example.com"):
    """Expand a seed work's citation network via OpenAlex (1-hop, both directions).

    Uses the reliable `cites:` filter (forward) + `referenced_works` expansion
    (backward) — the old `/references` & `/cited_by` sub-endpoints returned a single
    work object instead of a `results` list, so the prior implementation collected
    zero works.

    Args:
        seed_work_id: OpenAlex work ID (e.g. "W3087210493" or full URL)
        direction: "references" (backward), "cited_by" (forward), or "both"
        max_refs: max records to retrieve per direction
        api_key: OpenAlex API key (Bearer)
        mailto: polite-pool email
    Returns a list of normalized work records (no seed record included).
    """
    if api_key is None:
        api_key = http_utils.load_openalex_key()
    headers = http_utils.build_openalex_headers(api_key=api_key, mailto=mailto)
    oa_id = str(seed_work_id).strip("/").split("/")[-1]
    collected = []
    if direction in ("both", "cited_by"):
        collected += _fetch_cited_by(oa_id, max_refs, headers, mailto)
    if direction in ("both", "references"):
        collected += _fetch_references(oa_id, max_refs, headers, mailto)
    return collected


def snowball_from(seed, direction="both", max_refs=20, api_key=None, mailto="dev@example.com"):
    """Citation-network expansion from a USER-SUPPLIED seed (DOI / PMID / title).

    Resolves the seed to an OpenAlex work, then expands its 1-hop citation network
    (backward references + forward cited_by). The FIRST element of the returned list
    is the seed work itself (direction="seed"); the rest are its neighbors.

    Returns [] when the seed cannot be resolved (caller should report not_found).
    """
    rec, oa_id = resolve_seed(seed, api_key=api_key, mailto=mailto)
    if rec is None or not oa_id:
        return []
    if api_key is None:
        api_key = http_utils.load_openalex_key()
    headers = http_utils.build_openalex_headers(api_key=api_key, mailto=mailto)
    seed_w = _snowball_normalize(rec, oa_id, "seed")
    collected = [seed_w]
    if direction in ("both", "cited_by"):
        collected += _fetch_cited_by(oa_id, max_refs, headers, mailto)
    if direction in ("both", "references"):
        collected += _fetch_references(oa_id, max_refs, headers, mailto)
    return collected


def fetch(topic, review_type="all", year_from=None, year_to=None, safety=False,
          max_results=50, run=False, out=None, mailto="dev@example.com",
          api_key=None, include_reviews=True, date_from=None, date_to=None,
          cochrane=False):
    """Fetch from OpenAlex. When include_reviews=False, the `type:review` filter
    is explicitly added so review-type works are excluded at the source.

    When `cochrane=True`, restrict to the Cochrane Database of Systematic Reviews
    via its ISSN — this is the OpenAlex leg's independent Cochrane channel, used
    when Europe PMC is rate-limited/unreachable.

    OpenAlex type values: article, review, book-chapter, preprint, etc.
    (see TYPE_MAP). Passing `type:!review` through the filter param requires
    negation syntax, so instead we append `type:article` when excluding reviews
    (articles are the primary study type for meta-analysis evidence)."""
    if not run:
        print("[PREVIEW] would query OpenAlex for topic=%r review_type=%r include_reviews=%r "
              "cochrane=%r (use --run to execute)"
              % (topic, review_type, include_reviews, cochrane))
        return None

    http_utils.notify_openalex_key_if_missing(api_key)
    # run() passes api_key=None by default; re-resolve from env/.env so the actual
    # request uses the keyed pool (Bearer) instead of silently falling back to the
    # throttled keyless pool. This is the "right path" the config audit guards against.
    if api_key is None:
        api_key = http_utils.load_openalex_key()
    filt = ["has_doi:true"]
    if cochrane:
        # CDSR-only 车道（Europe PMC 不可用时的独立备用通道）。
        filt.append(COCHRANE_ISSN_FILTER)
    oa_type = _openalex_type_for(review_type)
    if oa_type:
        filt.append("type:%s" % oa_type)
    elif not include_reviews:
        # No specific review_type requested (== "all") and reviews excluded →
        # restrict to article-level works to filter out type:review entries.
        filt.append("type:article")
    if date_from:
        filt.append("from_publication_date:%s" % date_from)
    elif year_from:
        filt.append("from_publication_date:%d-01-01" % year_from)
    if date_to:
        filt.append("to_publication_date:%s" % date_to)
    elif year_to:
        filt.append("to_publication_date:%d-12-31" % year_to)

    query = topic
    if review_type == "systematic-review":
        query += " systematic review"
    elif review_type == "meta-analysis":
        query += " meta-analysis"
    elif review_type == "scoping-review":
        query += " scoping review"
    elif review_type == "rct":
        query += " randomized controlled trial"
    elif review_type == "case-report":
        query += " case report"
    if safety:
        query += " (" + " OR ".join(SAFETY_LEXICON[:6]) + ")"

    collected = []
    page = 1
    per = 100
    # Overall fetch budget: each single request already has 45s x 4 retries of
    # protection, but a recomposed query + slow network can push multi-page
    # accumulation past the outer timeout. Add a global budget; stop paging on expiry.
    fetch_deadline = time.time() + 240
    while len(collected) < max_results:
        if time.time() > fetch_deadline:
            print("[WARN] OpenAlex fetch exceeded 240s budget; stopping pagination early")
            break
        params = {
            "search": query,
            "filter": ",".join(filt),
            "per-page": min(per, max_results - len(collected)),
            "page": page,
            "mailto": mailto,
            "select": "id,doi,title,display_name,publication_year,publication_date,type,cited_by_count,primary_location,locations,authorships,abstract_inverted_index,ids,concepts,keywords,funders,best_oa_location,open_access,biblio,language,is_retracted",
        }
        url = BASE + "?" + urllib.parse.urlencode(params)
        headers = http_utils.build_openalex_headers(api_key=api_key, mailto=mailto)
        try:
            j = http_utils.get_json(url, headers=headers, timeout=45, max_retries=4)
        except http_utils.RateLimitError as e:
            # Propagate as a degradation signal (do NOT silently return 0 works):
            # the caller's parallel wrapper catches it and records a friendly notice.
            print("[WARN] OpenAlex rate-limited (HTTP 429%s): %s"
                  % (" keyless" if e.keyless else "", e))
            raise
        except http_utils.HttpError as e:
            print("[WARN] OpenAlex request failed: %s" % e)
            raise
        results = j.get("results", [])
        if not results:
            break
        for rec in results:
            w = _extract(rec)
            w["study_type"] = _study_type_from(rec, review_type)
            w["is_safety"] = _flag_safety(w)
            # 与 fetch_europepmc 对齐：始终按期刊名打标，便于 --cochrane 的
            # 客户端二次过滤在 OpenAlex 段也能识别 CDSR（不改变非 cochrane 行为）。
            w["is_cochrane"] = COCHRANE_JOURNAL_MARK in (
                (w.get("publication") or "")).lower()
            collected.append(w)
        if len(results) < per:
            break
        page += 1
        time.sleep(0.3)  # be polite to the public API

    payload = {
        "source": "OpenAlex",
        "query": query,
        "review_type": review_type,
        "year_from": year_from,
        "year_to": year_to,
        "date_from": date_from,
        "date_to": date_to,
        "safety": safety,
        "cochrane": bool(cochrane),
        "count": len(collected),
        "works": collected,
    }
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print("[OK] OpenAlex wrote %d works -> %s" % (len(collected), out))
    return payload


def main():
    ap = argparse.ArgumentParser(description="Fetch literature via OpenAlex (public, no key).")
    ap.add_argument("--topic", required=True, help="free-text topic / drug / disease")
    ap.add_argument("--review-type", default="all",
                    choices=["all", "systematic-review", "scoping-review",
                             "meta-analysis", "rct", "case-report"])
    ap.add_argument("--year-from", type=int, help="lower bound publication year")
    ap.add_argument("--year-to", type=int, help="upper bound publication year")
    ap.add_argument("--date-from", default=None, metavar="YYYY-MM-DD",
                    help="精确发表日期下界（月份级过滤），优先于 --year-from")
    ap.add_argument("--date-to", default=None, metavar="YYYY-MM-DD",
                    help="精确发表日期上界（默认无；与 --date-from 配合做窗口过滤）")
    ap.add_argument("--safety", action="store_true", help="bias toward safety / AE literature")
    ap.add_argument("--max", type=int, default=30, help="max works to retrieve")
    ap.add_argument("--mailto", default="dev@example.com", help="OpenAlex polite-pool email")
    ap.add_argument("--openalex-key", default=http_utils.load_openalex_key(),
                    help="OpenAlex API key (Bearer). Auto-loaded from env OPENALEX_API_KEY "
                         "or skill .env. Free key lifts rate limit 100 -> 100k credits/day.")
    ap.add_argument("--include-reviews", action=argparse.BooleanOptionalAction,
                    default=True,
                    help="include review-type publications in results (default: on; "
                         "use --no-include-reviews to exclude at the source)")
    ap.add_argument("--cochrane", action="store_true",
                    help="restrict to the Cochrane Database of Systematic Reviews "
                         "(via ISSN %s) — OpenAlex leg's independent Cochrane channel"
                         % COCHRANE_ISSN)
    ap.add_argument("--run", action="store_true", help="execute network request")
    ap.add_argument("--out", help="output JSON path")
    args = ap.parse_args()
    res = fetch(args.topic, args.review_type, args.year_from, args.year_to,
                args.safety, args.max, args.run, args.out, args.mailto, args.openalex_key,
                include_reviews=args.include_reviews, date_from=args.date_from,
                date_to=args.date_to, cochrane=args.cochrane)
    if res and not args.out:
        print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
