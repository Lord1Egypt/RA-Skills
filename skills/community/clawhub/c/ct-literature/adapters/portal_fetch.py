#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
portal_fetch.py — BUILD-TIME lightweight fetchers for guideline orgs that have NO
free keyword-search API in the 13-source library (NCCN / ADA / AHA / SIGN / CMA / CPIC).

Called ONLY by build_guidelines.build(run=True) at corpus-build time (network ALLOWED).
At analysis time, guideline_corpus.load() reads the persisted results — ZERO network.

Why this module exists
----------------------
The 13-source library (fetch_guidelines.py) covers OpenAlex / EuropePMC / GIN / WHO /
NICE / MAGICapp / TRIP via real or key-gated APIs. The six orgs above have no free
keyword API, so they were emitted as honest `portal` pointers (retrieved:false). This
module upgrades them at BUILD time: when the builder runs (author action, open internet),
it tries a lightweight fetch; if that yields records they are stored as real `api`
records (retrieved:true), otherwise we fall back to the honest pointer. Either way the
analysis-time loader stays offline.

Honesty / robustness
--------------------
  * CPIC ships a real, free, keyless PostgREST API (https://api.cpicpgx.org/v1) -> genuine fetch.
  * NCCN content sits behind a free-account login wall; ADA / AHA / SIGN / CMA are HTML
    portals. For these we do a best-effort public-listing scrape (link extraction). It is
    schema-tolerant and WILL degrade to [] on login walls / JS rendering / network blocks,
    in which case build_guidelines falls back to the portal pointer. NOTHING is fabricated.
  * Every fetcher is wrapped so it NEVER raises; on any failure it returns [].
"""
import os
import re
import sys
import urllib.parse

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                       # sibling imports within adapters/
sys.path.insert(0, os.path.dirname(_HERE))      # skill root -> `from adapters import fetch_guidelines`
from adapters import fetch_guidelines as fg     # reuse _normalize / _looks_like_guideline / _as_int


# ── low-level network (lazy requests; requests bundles its own CA, unlike urllib here) ──
def _get_json(url, timeout=20):
    import requests
    r = requests.get(url, timeout=timeout,
                     headers={"User-Agent": "ct-literature-guideline-builder/0.1"})
    r.raise_for_status()
    return r.json()


def _get_text(url, timeout=20):
    import requests
    r = requests.get(url, timeout=timeout,
                     headers={"User-Agent": "Mozilla/5.0 (ct-literature-guideline-builder)"})
    r.raise_for_status()
    return r.text


# ── CPIC: real PostgREST API ──────────────────────────────────────────────────────
def _cpic(topic, max_results):
    """Genuine fetch from CPIC's free keyless API. Returns normalized api records."""
    out = []
    # 1) guideline table (name is the human-readable guideline title)
    params = {"select": "guidelineid,name,url",
              "name": "ilike.*%s*" % topic, "limit": str(max_results)}
    url = "https://api.cpicpgx.org/v1/guideline?" + urllib.parse.urlencode(params)
    try:
        rows = _get_json(url) or []
    except Exception:
        rows = []
    if not rows:
        # 2) fallback: guideline publications carry the title + pmid
        params2 = {"select": "title,pmid,year,guidelineid",
                   "title": "ilike.*%s*" % topic, "limit": str(max_results)}
        url2 = "https://api.cpicpgx.org/v1/publication?" + urllib.parse.urlencode(params2)
        try:
            rows = _get_json(url2) or []
        except Exception:
            rows = []
    for r in rows[:max_results]:
        title = (r.get("name") or r.get("title") or "").strip()
        if not title:
            continue
        out.append(fg._normalize(
            "CPIC", "api", title,
            year=fg._as_int(r.get("year") or r.get("version")),
            url=r.get("url") or (("https://cpicpgx.org/guidelines/%s" % r["guidelineid"])
                                 if r.get("guidelineid") else None),
            org_url="https://cpicpgx.org/guidelines",
            retrieved=True, topic=topic,
            extra={"guidelineid": r.get("guidelineid"), "pmid": r.get("pmid"),
                   "version": r.get("version")}))
    return out


# ── HTML-portal best-effort scrape (NCCN / ADA / AHA / SIGN / CMA) ────────────────
_LINK_RE = re.compile(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', re.I | re.S)


def _html_links(org, topic, url, max_results):
    """Extract plausible guideline links from an org's public listing page.

    Keeps only anchors whose text looks guideline-ish OR contains the topic keyword.
    Relative hrefs are resolved against the page URL. Best-effort; tolerates mess.
    """
    html = _get_text(url)
    tlow = (topic or "").lower()
    recs = []
    for m in _LINK_RE.finditer(html):
        href, txt = m.group(1), re.sub(r"<[^>]+>", "", m.group(2))
        txt = txt.strip()
        if not txt:
            continue
        if not (fg._looks_like_guideline(txt) or (tlow and tlow in txt.lower())):
            continue
        if href.startswith("//"):
            href = "https:" + href
        elif not href.startswith("http"):
            href = urllib.parse.urljoin(url, href)
        if href.rstrip("/") in (url.rstrip("/"), ""):
            continue  # skip self-links
        recs.append(fg._normalize(
            org, "api", txt, url=href, org_url=url,
            retrieved=True, topic=topic))
        if len(recs) >= max_results:
            break
    return recs


def _nccn(topic, max_results):
    # NCCN guidelines are behind a free-account login wall; best-effort public topic list.
    return _html_links("NCCN", topic,
                       "https://www.nccn.org/professionals/physician_gls/default.aspx",
                       max_results)


def _ada(topic, max_results):
    return _html_links("ADA", topic, "https://professional.diabetes.org/SOC", max_results)


def _aha(topic, max_results):
    return _html_links("AHA", topic, "https://www.ahajournals.org/action/showGuidelines",
                       max_results)


def _sign(topic, max_results):
    return _html_links("SIGN", topic, "https://www.sign.ac.uk/our-guidelines/", max_results)


def _cma(topic, max_results):
    return _html_links("CMA", topic, "https://www.cma.org.cn/", max_results)


_FETCHERS = {
    "CPIC": _cpic, "NCCN": _nccn, "ADA": _ada,
    "AHA": _aha, "SIGN": _sign, "CMA": _cma,
}


def fetch_portal(org, topic, max_results=10):
    """Build-time fetcher for one portal org. Returns a list of normalized records
    (access='api', retrieved=True) or [] on any failure (graceful, never raises)."""
    fn = _FETCHERS.get(org)
    if not fn:
        return []
    try:
        return fn(topic, max_results) or []
    except Exception:
        return []
