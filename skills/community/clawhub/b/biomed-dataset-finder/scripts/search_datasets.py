#!/usr/bin/env python3
"""
Biomed Dataset Finder — NCBI-GEO/SRA + NGDC-GSA + CNGBdb Search CLI

Usage:
    python search_datasets.py --disease "colon cancer" --treatment "immunotherapy" \
        --species human --subtype dMMR --type scRNA-seq --max-results 10

    python search_datasets.py --disease "hepatocellular carcinoma" --treatment "PD-1" \
        --species human --type scRNA-seq --skip-cngb --skip-ngdc
"""

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from typing import Optional


# ─── NCBI E-utilities ────────────────────────────────────────────

def ncbi_search(db: str, term: str, retmax: int = 20) -> list[str]:
    """Search NCBI and return list of IDs."""
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    params = urllib.parse.urlencode({
        "db": db,
        "term": term,
        "retmax": retmax,
        "retmode": "json",
        "sort": "relevance",
    })
    url = f"{base}/esearch.fcgi?{params}"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        print(f"[NCBI Search Error] {e}", file=sys.stderr)
        return []
    err = data.get("esearchresult", {}).get("error", "")
    if err:
        print(f"[NCBI Search Error] {err}", file=sys.stderr)
        return []
    return data.get("esearchresult", {}).get("idlist", [])


def ncbi_summary(db: str, ids: list[str]) -> list[dict]:
    """Get summary details for a list of NCBI IDs."""
    if not ids:
        return []
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    id_str = ",".join(ids)
    params = urllib.parse.urlencode({"db": db, "id": id_str, "retmode": "json"})
    try:
        with urllib.request.urlopen(f"{base}/esummary.fcgi?{params}", timeout=15) as resp:
            raw = json.loads(resp.read())
    except Exception as e:
        print(f"[NCBI Summary Error] {e}", file=sys.stderr)
        return []
    result = raw.get("result", {})
    entries = []
    for uid in ids:
        if uid in result:
            entries.append({"id": uid, **result[uid]})
    return entries


def ncbi_get_article(pmid: str) -> Optional[dict]:
    """Fetch PubMed article info by PMID."""
    if not pmid:
        return None
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    params = urllib.parse.urlencode({"db": "pubmed", "id": pmid, "retmode": "json"})
    try:
        with urllib.request.urlopen(f"{base}/esummary.fcgi?{params}", timeout=15) as resp:
            data = json.loads(resp.read())
    except Exception:
        return None
    articles = data.get("result", {}).get(pmid, {})
    if not articles:
        return None
    return {
        "title": articles.get("title", "Unknown"),
        "authors": ", ".join(a.get("name", "") for a in articles.get("authors", [])),
        "source": articles.get("source", ""),
        "pubdate": articles.get("pubdate", "")[:4],
        "doi": articles.get("elocationid", "").replace("doi: ", ""),
    }


def search_ncbi(args: argparse.Namespace) -> list[dict]:
    """Search NCBI GEO (gds) and SRA databases."""
    keywords = []
    if args.disease:
        keywords.append(args.disease)
    if args.treatment:
        keywords.append(args.treatment)
    if args.species:
        keywords.append(args.species)
    if args.subtype:
        keywords.append(args.subtype)
    if args.data_type:
        if "sc" in args.data_type.lower() or "single" in args.data_type.lower():
            keywords.append("single cell")
        else:
            keywords.append(args.data_type)

    term = " AND ".join(keywords)
    print(f"[NCBI] Searching {len(keywords)} keywords...", file=sys.stderr)

    results = []
    max_results = getattr(args, "max_results", 20)

    # GEO Datasets (db=gds, accession field contains GSE prefix)
    gds_ids = ncbi_search("gds", term, retmax=max_results)
    print(f"[NCBI] GEO found {len(gds_ids)} datasets", file=sys.stderr)

    for gds in ncbi_summary("gds", gds_ids):
        accession = gds.get("accession", "")
        link = f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={accession}"
        pmids = gds.get("pubmedids", [])
        pmid = pmids[0] if pmids else ""
        article = ncbi_get_article(pmid) if pmid else {}

        results.append({
            "source": "NCBI-GEO",
            "dataset_id": f"**{accession}**",
            "dataset_link": link,
            "title": gds.get("title", ""),
            "data_type": args.data_type or "",
            "species": args.species or "",
            "article_authors": article.get("authors", ""),
            "article_title": article.get("title", ""),
            "article_journal": article.get("source", ""),
            "article_year": article.get("pubdate", ""),
            "article_doi": article.get("doi", ""),
        })
        if pmid:
            time.sleep(0.35)

    # SRA for single-cell queries
    if args.data_type and ("sc" in args.data_type.lower() or "single" in args.data_type.lower()):
        sra_ids = ncbi_search("sra", term, retmax=max_results)
        print(f"[NCBI] SRA found {len(sra_ids)} datasets", file=sys.stderr)

        for sra in ncbi_summary("sra", sra_ids):
            sra_acc = sra.get("accession", "") or sra.get("uid", "")
            link = f"https://www.ncbi.nlm.nih.gov/sra/{sra_acc}"
            results.append({
                "source": "NCBI-SRA",
                "dataset_id": f"**{sra_acc}**",
                "dataset_link": link,
                "title": "",
                "data_type": "scRNA-seq",
                "species": args.species or "",
                "article_authors": "",
                "article_title": "",
                "article_journal": "",
                "article_year": "",
                "article_doi": "",
            })
            time.sleep(0.35)

    return results


# ─── NGDC GSA Search ─────────────────────────────────────────────

def search_ngdc(args: argparse.Namespace) -> list[dict]:
    """
    Search NGDC (National Genomics Data Center) GSA database.
    API: https://ngdc.cncb.ac.cn/search/api/specific
    """
    keywords = []
    if args.disease:
        keywords.append(args.disease)
    if args.treatment:
        keywords.append(args.treatment)
    if args.species:
        keywords.append(args.species)
    if args.subtype:
        keywords.append(args.subtype)
    if args.data_type:
        keywords.append(args.data_type)

    query = " ".join(keywords)
    print(f"[NGDC] Searching {len(keywords)} keywords...", file=sys.stderr)

    base = "https://ngdc.cncb.ac.cn/search/api/specific"
    params = urllib.parse.urlencode({
        "q": query,
        "db": "gsa",
        "size": getattr(args, "max_results", 20),
    })

    try:
        req = urllib.request.Request(f"{base}?{params}", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = json.loads(resp.read())
    except Exception as e:
        print(f"[NGDC Search Error] {e}", file=sys.stderr)
        return []

    results = []
    try:
        items = raw.get("result", {}).get("data", {}).get("data", [])
    except Exception:
        print("[NGDC] Failed to parse response", file=sys.stderr)
        return []

    # Filter to only GSA type entries (CRA accessions)
    gsa_items = [x for x in items if x.get("type") == "GSA"]
    print(f"[NGDC] Found {len(gsa_items)} GSA datasets", file=sys.stderr)

    for item in gsa_items:
        cra_id = item.get("id", "")
        title = item.get("title", "")
        url = item.get("url", "") or f"https://ngdc.cncb.ac.cn/gsa/browse/{cra_id}"
        attrs = item.get("attrs", {})

        results.append({
            "source": "NGDC-GSA",
            "dataset_id": f"**{cra_id}**",
            "dataset_link": url,
            "title": title,
            "data_type": args.data_type or attrs.get("strategyName", ""),
            "species": args.species or "",
            "article_authors": "",
            "article_title": "",
            "article_journal": "",
            "article_year": attrs.get("Release date", "")[:4],
            "article_doi": "",
        })

    return results


# ─── CNGB Search ─────────────────────────────────────────────────

def search_cngb(args: argparse.Namespace, token: Optional[str] = None) -> list[dict]:
    """Search CNGBdb."""
    keywords = []
    if args.disease:
        keywords.append(args.disease)
    if args.treatment:
        keywords.append(args.treatment)
    if args.species:
        keywords.append(args.species)
    if args.data_type:
        keywords.append(args.data_type)

    query = " ".join(keywords)
    print(f"[CNGB] Searching {len(keywords)} keywords...", file=sys.stderr)

    base = "https://db.cngb.org/api"
    params = urllib.parse.urlencode({
        "q": query,
        "type": args.data_type or "",
        "species": args.species or "",
        "page": 1,
        "size": getattr(args, "max_results", 20),
    })

    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        req = urllib.request.Request(f"{base}/search/dataset?{params}", headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        print(f"[CNGB Search Error] {e}", file=sys.stderr)
        return []

    results = []
    for item in data.get("data", []):
        pid = item.get("project_id", "")
        results.append({
            "source": "CNGB",
            "dataset_id": f"**{pid}**",
            "dataset_link": f"https://db.cngb.org/project/{pid}",
            "title": item.get("title", ""),
            "data_type": item.get("data_type", ""),
            "species": item.get("organism", ""),
            "article_authors": "",
            "article_title": item.get("pubmed_title", ""),
            "article_journal": "",
            "article_year": item.get("create_time", "")[:4],
            "article_doi": item.get("doi", ""),
        })

    print(f"[CNGB] Found {len(results)} datasets", file=sys.stderr)
    return results


# ─── Output ─────────────────────────────────────────────────────

def print_table(results: list[dict]):
    """Print results as markdown table."""
    if not results:
        print("未找到符合条件的公共数据集，建议尝试调整关键词或更换数据源。")
        return

    print("\n**数据来源: NCBI-GEO / NCBI-SRA / NGDC-GSA / CNGB**\n")
    header = "| # | 来源 | Dataset ID | Species | Data Type | Article | Journal | Year | DOI | Link |"
    sep = "|---|------|------------|---------|-----------|---------|---------|------|-----|------|"
    print(header)
    print(sep)

    for i, r in enumerate(results, 1):
        doi = r["article_doi"]
        if doi and not doi.startswith("http"):
            doi = f"https://doi.org/{doi}"

        article = f"{r['article_authors']} — {r['article_title']}" if r["article_authors"] else r["article_title"]
        journal = r["article_journal"] or ""
        year = r["article_year"] or ""

        print(f"| {i} | {r['source']} | {r['dataset_id']} | {r['species']} | {r['data_type']} | "
              f"{article} | {journal} | {year} | "
              f"{('[DOI]({})'.format(doi) if doi else '-')} | "
              f"{('[Link]({})'.format(r['dataset_link']) if r['dataset_link'].startswith('http') else '-')} |")


# ─── CLI ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Biomed Dataset Finder — NCBI / NGDC / CNGB")
    parser.add_argument("--disease", help="Disease/cancer name")
    parser.add_argument("--treatment", help="Treatment method (e.g. immunotherapy, PD-1)")
    parser.add_argument("--species", default="human", help="Species (human/mouse, default: human)")
    parser.add_argument("--subtype", help="Pathology subtype (e.g. dMMR, KRAS mutant)")
    parser.add_argument("--type", dest="data_type", help="Data type (e.g. scRNA-seq, RNA-seq)")
    parser.add_argument("--max-results", type=int, default=20)
    parser.add_argument("--cngb-token", help="CNGB API token (optional)")
    parser.add_argument("--skip-cngb", action="store_true", help="Skip CNGB search")
    parser.add_argument("--skip-ngdc", action="store_true", help="Skip NGDC-GSA search")

    args = parser.parse_args()

    if not any([args.disease, args.treatment, args.data_type]):
        print("Error: at least one of --disease, --treatment, or --type is required", file=sys.stderr)
        sys.exit(1)

    all_results = []

    # 1. NCBI (primary — always run)
    all_results.extend(search_ncbi(args))

    # 2. NGDC (primary — always run unless skipped)
    if not args.skip_ngdc:
        all_results.extend(search_ngdc(args))

    # 3. CNGB (secondary — on demand with token)
    if not args.skip_cngb:
        all_results.extend(search_cngb(args, token=args.cngb_token))

    print_table(all_results)


if __name__ == "__main__":
    main()