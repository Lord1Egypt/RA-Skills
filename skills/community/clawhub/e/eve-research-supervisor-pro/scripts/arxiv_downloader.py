#!/usr/bin/env python3
"""
arxiv_downloader.py — Download real PDFs + metadata from arXiv
Usage: python3 arxiv_downloader.py "<topic>" <max_results> [output_dir]
"""

import requests
import os
import sys
import json
import time
from xml.etree import ElementTree

def download_papers(query, max_results=30, output_dir="papers_pdf"):
    os.makedirs(output_dir, exist_ok=True)
    metadata_list = []

    url = (
        f"http://export.arxiv.org/api/query"
        f"?search_query=all:{requests.utils.quote(query)}"
        f"&start=0&max_results={max_results}"
        f"&sortBy=relevance&sortOrder=descending"
    )

    print(f"🔍 Searching arXiv for: {query}")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to query arXiv: {e}")
        sys.exit(1)

    root = ElementTree.fromstring(response.content)
    ns = "{http://www.w3.org/2005/Atom}"
    entries = root.findall(f"{ns}entry")

    print(f"📄 Found {len(entries)} papers. Downloading...")

    for i, entry in enumerate(entries):
        try:
            arxiv_id_raw = entry.find(f"{ns}id").text.strip()
            arxiv_id = arxiv_id_raw.split("/abs/")[-1].replace("/", "_")
            title = entry.find(f"{ns}title").text.strip().replace("\n", " ")
            abstract = entry.find(f"{ns}summary").text.strip().replace("\n", " ")
            authors = [
                a.find(f"{ns}name").text
                for a in entry.findall(f"{ns}author")
            ]
            published = entry.find(f"{ns}published").text.strip()

            pdf_url = arxiv_id_raw.replace("/abs/", "/pdf/") + ".pdf"
            filename = f"{output_dir}/paper_{i:03d}_{arxiv_id}.pdf"

            # Save metadata
            metadata_list.append({
                "index": i,
                "arxiv_id": arxiv_id,
                "title": title,
                "authors": authors,
                "published": published,
                "abstract": abstract,
                "pdf_url": pdf_url,
                "filename": filename
            })

            # Download PDF with rate limiting
            if not os.path.exists(filename):
                time.sleep(1.5)  # Respect arXiv rate limits
                pdf_resp = requests.get(pdf_url, timeout=60)
                if pdf_resp.status_code == 200:
                    with open(filename, "wb") as f:
                        f.write(pdf_resp.content)
                    print(f"  ✅ [{i+1}/{len(entries)}] {title[:60]}...")
                else:
                    print(f"  ⚠️  [{i+1}/{len(entries)}] Skipped (HTTP {pdf_resp.status_code}): {title[:50]}")
            else:
                print(f"  ⏭️  [{i+1}/{len(entries)}] Already exists: {title[:60]}")

        except Exception as e:
            print(f"  ❌ [{i+1}] Error: {e}")
            continue

    # Save metadata JSON for other scripts to use
    with open(f"{output_dir}/metadata.json", "w") as f:
        json.dump(metadata_list, f, indent=2)

    print(f"\n✅ Downloaded {len(metadata_list)} papers to {output_dir}/")
    print(f"📋 Metadata saved to {output_dir}/metadata.json")
    return metadata_list


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 arxiv_downloader.py \"<topic>\" <max_results> [output_dir]")
        sys.exit(1)

    query = sys.argv[1]
    max_results = int(sys.argv[2])
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "papers_pdf"

    download_papers(query, max_results, output_dir)
