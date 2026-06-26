import json
import os
import sys
from curl_cffi import requests
from lxml import html

# v1.6.0 SOTA Integrity: Relative path resolution for community portability
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def unified_search(query):
    print(f"--- [Drission SOTA Toolkit: Unified Search Engine] ---")
    print(f"Query: {query}\n")
    
    results_storage = {}

    # Target 1: arXiv Academic (Scholarly)
    print("[1/2] Penetrating arXiv Academic Archive...")
    try:
        url = f"https://arxiv.org/search/?query={query.replace(' ', '+')}&searchtype=all"
        # Using SOTA impersonate to ensure high-speed, no-captcha access
        r = requests.get(url, impersonate="chrome124", timeout=15)
        tree = html.fromstring(r.content)
        papers = tree.xpath("//p[@class='title is-5 mathjax']/text()")
        paper_list = [" ".join(p.split()) for p in papers[:5]]
        if paper_list:
            print(f"✅ Extracted {len(paper_list)} Papers.")
            results_storage["arXiv"] = paper_list
    except Exception as e:
        print(f"❌ arXiv Access Aborted: {e}")

    # Target 2: DuckDuckGo (Real-time Intel)
    print("\n[2/2] Penetrating DuckDuckGo Intelligence Stream...")
    try:
        url = f"https://duckduckgo.com/html/?q={query.replace(' ', '+')}"
        r = requests.get(url, impersonate="chrome124", timeout=15)
        tree = html.fromstring(r.content)
        results = tree.xpath("//a[@class='result__a']/text()")
        intel_list = [res.strip() for res in results[:5]]
        if intel_list:
            print(f"✅ Extracted {len(intel_list)} Intel Items.")
            results_storage["DDG"] = intel_list
    except Exception as e:
        print(f"❌ DDG Access Aborted: {e}")

    # Save to local assets directory
    os.makedirs(ASSETS_DIR, exist_ok=True)
    report_path = os.path.join(ASSETS_DIR, "SOTA_SEARCH_REPORT.json")
    with open(report_path, "w") as f:
        json.dump(results_storage, f, indent=2, ensure_ascii=False)
    
    print(f"\n--- [Mission Complete. Report Locked at: {report_path}] ---")

if __name__ == "__main__":
    query_str = sys.argv[1] if len(sys.argv) > 1 else "Spatial Intelligence 2026"
    unified_search(query_str)
