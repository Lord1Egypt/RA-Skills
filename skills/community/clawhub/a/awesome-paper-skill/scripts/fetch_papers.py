#!/usr/bin/env python3
import argparse
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone


def http_get(url: str, timeout: int = 20):
    req = urllib.request.Request(url, headers={"User-Agent": "openclaw-awesome-research-tracker/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="ignore")


def fetch_arxiv(topic: str, limit: int):
    q = urllib.parse.quote(topic)
    url = (
        "https://export.arxiv.org/api/query?search_query=all:"
        f"{q}&start=0&max_results={limit}&sortBy=submittedDate&sortOrder=descending"
    )
    txt = http_get(url)
    root = ET.fromstring(txt)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    papers = []
    for e in root.findall("a:entry", ns):
        title = " ".join((e.findtext("a:title", "", ns) or "").split())
        summary = " ".join((e.findtext("a:summary", "", ns) or "").split())
        published = (e.findtext("a:published", "", ns) or "")[:10]
        abs_url = e.findtext("a:id", "", ns)
        pdf_url = ""
        for lk in e.findall("a:link", ns):
            if lk.attrib.get("title") == "pdf":
                pdf_url = lk.attrib.get("href", "")
        papers.append(
            {
                "title": title,
                "abstract": summary,
                "date": published,
                "arxiv": abs_url,
                "pdf": pdf_url,
                "source": "arxiv",
                "venue": "",
                "published_type": "preprint",
                "doi": "",
                "url": abs_url,
            }
        )
    return papers


def fetch_crossref(topic: str, limit: int):
    q = urllib.parse.quote(topic)
    url = f"https://api.crossref.org/works?query={q}&rows={limit}&sort=published&order=desc"
    txt = http_get(url)
    data = json.loads(txt)
    items = data.get("message", {}).get("items", [])
    out = []
    for it in items:
        title_arr = it.get("title") or []
        title = title_arr[0].strip() if title_arr else ""
        if not title:
            continue
        abstract = re.sub(r"<[^>]+>", "", it.get("abstract", "") or "")
        doi = it.get("DOI", "") or ""
        typ = it.get("type", "") or ""
        venue = ""
        if it.get("container-title"):
            venue = it.get("container-title", [""])[0] or ""
        published_type = "published" if typ in {"journal-article", "proceedings-article"} else "unknown"
        y, m, d = "", "", ""
        dp = it.get("issued", {}).get("date-parts", [[]])
        if dp and dp[0]:
            vals = dp[0]
            y = str(vals[0]) if len(vals) >= 1 else ""
            m = str(vals[1]).zfill(2) if len(vals) >= 2 else "01"
            d = str(vals[2]).zfill(2) if len(vals) >= 3 else "01"
        date = f"{y}-{m}-{d}" if y else ""
        link = f"https://doi.org/{doi}" if doi else (it.get("URL", "") or "")
        out.append(
            {
                "title": title,
                "abstract": " ".join(abstract.split()),
                "date": date,
                "arxiv": "",
                "pdf": "",
                "source": "crossref",
                "venue": venue,
                "published_type": published_type,
                "doi": doi,
                "url": link,
            }
        )
    return out


def fetch_semantic(topic: str, limit: int):
    q = urllib.parse.quote(topic)
    fields = "title,abstract,year,venue,url,externalIds,publicationTypes"
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={q}&limit={limit}&fields={fields}"
    txt = http_get(url)
    data = json.loads(txt)
    out = []
    for it in data.get("data", []):
        title = (it.get("title") or "").strip()
        if not title:
            continue
        pub_types = it.get("publicationTypes") or []
        ptype = "published" if pub_types else "unknown"
        year = it.get("year")
        date = f"{year}-01-01" if year else ""
        ext = it.get("externalIds") or {}
        arxiv = ""
        if ext.get("ArXiv"):
            arxiv = f"https://arxiv.org/abs/{ext['ArXiv']}"
        out.append(
            {
                "title": title,
                "abstract": " ".join((it.get("abstract") or "").split()),
                "date": date,
                "arxiv": arxiv,
                "pdf": "",
                "source": "semantic_scholar",
                "venue": it.get("venue") or "",
                "published_type": ptype,
                "doi": ext.get("DOI", "") or "",
                "url": it.get("url") or arxiv,
            }
        )
    return out


def dedupe(records):
    seen = set()
    out = []
    for r in records:
        key = (r.get("title", "").strip().lower(), r.get("doi", "").strip().lower())
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", required=True)
    ap.add_argument("--max-arxiv", type=int, default=30)
    ap.add_argument("--max-crossref", type=int, default=30)
    ap.add_argument("--max-semantic", type=int, default=30)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    rows = []
    errs = []
    for fn, lim in [
        (fetch_arxiv, args.max_arxiv),
        (fetch_crossref, args.max_crossref),
        (fetch_semantic, args.max_semantic),
    ]:
        try:
            rows.extend(fn(args.topic, lim))
        except Exception as e:
            errs.append(f"{fn.__name__}: {e}")

    rows = dedupe(rows)
    rows.sort(key=lambda x: x.get("date", ""), reverse=True)
    payload = {
        "topic": args.topic,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "errors": errs,
        "count": len(rows),
        "papers": rows,
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(rows)} papers -> {args.out}")
    if errs:
        print("Warnings:")
        for e in errs:
            print("-", e)


if __name__ == "__main__":
    main()
