import os
import sys
import json
import subprocess
from curl_cffi import requests
from lxml import html

# v2.1.0 SOTA Fortress: Mandatory Global Security Gate
def check_gate():
    if os.environ.get('SOTA_NUCLEAR_CONFIRMED') != 'true':
        print("!!! [SECURITY ABORT] Unauthorized autonomous execution blocked.")
        print("!!! This toolkit requires manual human gating via 'secure_wrapper.py'.")
        sys.exit(1)

# Dynamically resolve paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def unified_search(query):
    check_gate() # Hard gate check
    print(f"--- [Drission SOTA Toolkit: Unified Search Engine] ---")
    print(f"Query: {query}\n")
    
    results_storage = {}
    try:
        url = f"https://arxiv.org/search/?query={query.replace(' ', '+')}&searchtype=all"
        r = requests.get(url, impersonate="chrome124", timeout=15)
        tree = html.fromstring(r.content)
        papers = tree.xpath("//p[@class='title is-5 mathjax']/text()")
        paper_list = [" ".join(p.split()) for p in papers[:5]]
        if paper_list:
            results_storage["arXiv"] = paper_list
    except Exception as e:
        print(f"❌ arXiv Error: {e}")

    os.makedirs(ASSETS_DIR, exist_ok=True)
    report_path = os.path.join(ASSETS_DIR, "SOTA_SEARCH_REPORT.json")
    with open(report_path, "w") as f:
        json.dump(results_storage, f, indent=2, ensure_ascii=False)
    print(f"\n--- [Mission Complete. Result: {report_path}] ---")

if __name__ == "__main__":
    unified_search(sys.argv[1] if len(sys.argv) > 1 else "Spatial Intelligence 2026")
