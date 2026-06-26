#!/usr/bin/env python3
"""
Make the 'microsoft' icon provider comprehensive AND offline:

  1. Imports the official Microsoft Power Platform + Dynamics 365 icon packs
     (clean, current brand logos) as bundled microsoft-provider entries.
  2. Downloads every msicons.com 'microsoft' icon that is still web-only and
     bundles it locally, so the whole Microsoft set works offline like aws/azure/gcp.
  3. De-dupes: when an official product logo and an msicons icon share a name,
     the official one wins.

Usage:
    python bundle_microsoft.py --pp /path/to/PowerPlatform --dyn /path/to/Dynamics
    python bundle_microsoft.py --pp ... --dyn ... --skip-msicons-fetch   # only official
"""
import argparse
import concurrent.futures as cf
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "references" / "icon-index.json"
ICONS = ROOT / "assets" / "icons" / "microsoft"

# Clean display names + search aliases for the official packs.
OFFICIAL = {
    # Power Platform
    "AIBuilder": ("AI Builder", "ai builder"),
    "Agent365": ("Agent 365", "agent365"),
    "CopilotStudio": ("Copilot Studio", "copilot studio power virtual agents pva"),
    "Dataverse": ("Dataverse", "dataverse cds common data service"),
    "PowerApps": ("Power Apps", "powerapps canvas model driven app"),
    "PowerAutomate": ("Power Automate", "powerautomate flow"),
    "PowerPages": ("Power Pages", "powerpages portal"),
    "PowerPlatform": ("Power Platform", "power platform"),
    # Dynamics 365 (prefixed)
    "BusinessCentral": ("Dynamics 365 Business Central", "d365 bc erp nav"),
    "Commerce": ("Dynamics 365 Commerce", "d365 retail"),
    "ContactCenter": ("Dynamics 365 Contact Center", "d365 contact center"),
    "CustomerInsights": ("Dynamics 365 Customer Insights", "d365 ci cdp marketing"),
    "CustomerServices": ("Dynamics 365 Customer Service", "d365 cs case"),
    "CustomerVoice": ("Dynamics 365 Customer Voice", "d365 survey"),
    "FieldService": ("Dynamics 365 Field Service", "d365 fs"),
    "Finance": ("Dynamics 365 Finance", "d365 fin"),
    "FinanceOperations": ("Dynamics 365 Finance and Operations", "d365 fno fo"),
    "HumanResources": ("Dynamics 365 Human Resources", "d365 hr"),
    "IntelligentOrderManagement": ("Dynamics 365 Intelligent Order Management", "d365 iom"),
    "ProjectOperations": ("Dynamics 365 Project Operations", "d365 po psa"),
    "SalesInsights": ("Dynamics 365 Sales Insights", "d365 sales insights"),
    "Sales": ("Dynamics 365 Sales", "d365 crm sales"),
    "SupplyChainManagement": ("Dynamics 365 Supply Chain Management", "d365 scm"),
    "Dynamics365": ("Dynamics 365", "d365 dynamics"),
}


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def search_tokens(name, extra=""):
    base = re.sub(r"[^a-z0-9 ]", " ", name.lower())
    return f"{base} {base.replace(' ', '')} {extra}".strip()


def fetch_one(url, dest):
    try:
        safe = urllib.parse.quote(url, safe=":/?#[]@!$&'()*+,;=~")
        data = urllib.request.urlopen(safe, timeout=30).read()
        dest.write_bytes(data)
        return True
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pp", help="Power Platform SVG dir")
    ap.add_argument("--dyn", help="Dynamics 365 SVG dir")
    ap.add_argument("--skip-msicons-fetch", action="store_true")
    args = ap.parse_args()

    index = json.loads(INDEX.read_text("utf-8"))
    for e in index:
        e.setdefault("provider", "microsoft")

    official_dir = ICONS / "official"
    official_dir.mkdir(parents=True, exist_ok=True)
    official_entries, official_names = [], set()
    for src_dir in filter(None, [args.pp, args.dyn]):
        for svg in Path(src_dir).rglob("*.svg"):
            stem = re.sub(r"_scalable$", "", svg.stem)
            if stem not in OFFICIAL:
                continue
            name, alias = OFFICIAL[stem]
            safe = re.sub(r"[^A-Za-z0-9._-]", "_", svg.name)
            (official_dir / safe).write_bytes(svg.read_bytes())
            official_entries.append({
                "provider": "microsoft",
                "name": name,
                "category": "power-platform-dynamics",
                "file": (official_dir / safe).relative_to(ROOT).as_posix(),
                "search": search_tokens(name, alias),
            })
            official_names.add(norm(name))
    print(f"Imported {len(official_entries)} official Power Platform + Dynamics icons")

    # Drop msicons entries that duplicate an official product name.
    before = len(index)
    index = [e for e in index
             if not (e.get("provider") == "microsoft" and norm(e["name"]) in official_names)]
    print(f"Removed {before - len(index)} msicons duplicates of official products")

    # Bundle remaining web-only microsoft icons offline.
    if not args.skip_msicons_fetch:
        web = [e for e in index if e.get("provider") == "microsoft" and e.get("url") and not e.get("file")]
        msdir = ICONS / "msicons"
        msdir.mkdir(parents=True, exist_ok=True)
        print(f"Fetching {len(web)} msicons SVGs offline...")

        def do(e):
            safe = re.sub(r"[^A-Za-z0-9._-]", "_", e["url"].split("/")[-1])
            dest = msdir / safe
            if dest.exists() or fetch_one(e["url"], dest):
                e["file"] = dest.relative_to(ROOT).as_posix()
                return True
            return False

        with cf.ThreadPoolExecutor(max_workers=24) as ex:
            ok = sum(ex.map(do, web))
        print(f"  bundled {ok}/{len(web)} offline")

    index.extend(official_entries)
    INDEX.write_text(json.dumps(index, ensure_ascii=False))
    ms = [e for e in index if e.get("provider") == "microsoft"]
    offline = sum(1 for e in ms if e.get("file"))
    print(f"microsoft total: {len(ms)}  offline(file): {offline}  index total: {len(index)}")


if __name__ == "__main__":
    main()
