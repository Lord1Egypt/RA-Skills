#!/usr/bin/env python3
"""
Find the best msicons.com icon(s) for a service name, and optionally download
the SVG.

Why this exists: there are ~2400 icons. Eyeballing the index is slow and you'll
miss the right variant. This scores every icon against your query using token
overlap + fuzzy string similarity, with a light bias toward the canonical
brand icons (power-platform, dynamics-365, Copilot-studio, ...) over the
hundreds of monochrome Fluent glyphs in the "Microsoft" category, which are
rarely what an architecture diagram wants.

Usage:
    python find_icon.py "Azure AI Search"                 # top matches, human view
    python find_icon.py "Power Automate" --json           # machine-readable
    python find_icon.py "Dataverse" --fetch ./_icons      # download best match
    python find_icon.py "Entra ID" -n 8                   # show 8 candidates

Exit code is 0 even on weak matches; inspect the score. A score < ~0.35 usually
means "no good icon — fall back to a plain labeled box."
"""
import argparse
import json
import re
import sys
import urllib.request
import urllib.parse
from difflib import SequenceMatcher
from pathlib import Path

INDEX = Path(__file__).resolve().parent.parent / "references" / "icon-index.json"
SKILL_ROOT = Path(__file__).resolve().parent.parent
SITE = "https://msicons.com"

# Brand/product categories an architecture diagram usually wants.
PREFERRED = {
    "power-platform", "dynamics-365", "Copilot-studio", "agent-365",
    "fabric", "entra", "intune", "microsoft-teams", "sharepoint", "Planner",
    "ai-machine-learning", "analytics", "app-services", "compute",
    "containers", "databases", "integration", "iot", "networking",
    "security", "storage", "identity", "web", "devops",
    "management-governance", "monitor", "azure-ecosystem",
}
# Color/theme variants we'd rather not pick unless asked.
DEMOTE_RE = re.compile(r"(dark|light|gray|grey)\b", re.I)


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).strip()


GENERIC = {"microsoft", "icon", "color", "bw", "mono", "product", "family",
           "scalable", "service", "azure"}

# Common AWS abbreviations -> the canonical service's cleaned name. When the
# query is exactly the abbreviation, the canonical service icon is hard-boosted
# so it beats sub-variants that happen to contain the abbreviation literally
# (e.g. "S3" should win "Amazon Simple Storage Service", not "S3 on Outposts").
CANON_ALIAS = {
    "s3": "amazon simple storage service",
    "vpc": "amazon virtual private cloud",
    "ec2": "amazon ec2",
    "ecs": "amazon elastic container service",
    "eks": "amazon elastic kubernetes service",
    "rds": "amazon rds",
    "sns": "amazon simple notification service",
    "sqs": "amazon simple queue service",
    "iam": "aws identity and access management",
    "elb": "elastic load balancing",
    "sagemaker": "amazon sagemaker",
}


def score(query: str, item: dict) -> float:
    q = norm(query)
    qc = q.replace(" ", "")
    name = norm(item["name"])
    namec = name.replace(" ", "")
    search = item["search"]

    s = 0.0
    if q == name:
        s += 1.0
    if qc and qc == namec:
        s += 0.9
    if q and q in search:
        s += 0.5
    if qc and qc in search.replace(" ", ""):
        s += 0.4
    # token overlap
    qt, nt = set(q.split()), set(name.split())
    if qt:
        s += 0.6 * len(qt & nt) / len(qt)
    # fuzzy ratio on the name
    s += 0.5 * SequenceMatcher(None, q, name).ratio()

    # Prefer concise canonical names: penalize meaningful extra tokens.
    extra = (nt - qt) - GENERIC
    s -= 0.06 * len(extra)
    # Variant preference: color brand logos over BW/mono outlines.
    nl = name.lower()
    if "color" in nt:
        s += 0.12
    if "bw" in nt or "mono" in nl:
        s -= 0.15

    if item.get("category") in PREFERRED:
        s += 0.15
    locator = item.get("path", "") + item.get("file", "")
    if DEMOTE_RE.search(locator):
        s -= 0.25
    # Tier preference for the AWS pack: canonical service icons (Arch_) beat
    # resource icons (Res_) and category tiles when the query is ambiguous.
    if "/Res_" in locator:
        s -= 0.30
    elif "/Arch-Category_" in locator:
        s -= 0.15
    elif "/Arch_" in locator:
        s += 0.10
    # Exact abbreviation -> canonical service hard-boost.
    if CANON_ALIAS.get(q) == name:
        s += 2.0
    # Exact whole-token match anywhere in the search text (incl. aliases like
    # "gcs", "gce", "bq") — lifts valid abbreviations over the confidence bar.
    toks = set(search.split())
    if q in toks or (qc and qc in toks):
        s += 0.3
    # Microsoft Fabric pack ships every size + variant of each icon. When the
    # query doesn't pin a size, prefer a diagram-friendly default (48px) and the
    # colored product variant, so a bare "Data Warehouse" returns one good icon
    # while "Data Warehouse 16" still resolves exactly.
    if item.get("provider") == "fabric":
        nt = set(name.split())
        if not (nt & {"12", "16", "20", "24", "28", "32", "40", "48", "64"} & qt):
            size_pref = {"48": 0.30, "32": 0.24, "40": 0.20, "64": 0.18,
                         "24": 0.14, "28": 0.10, "20": 0.06, "16": 0.03}
            for sz, b in size_pref.items():
                if sz in nt:
                    s += b
                    break
            if "color" in nt:
                s += 0.20
            elif "item" in nt and "non" not in nt:
                s += 0.10
    return s


def search(query, n, index, providers=None):
    pool = index
    if providers:
        allow = set(providers)
        pool = [it for it in index if it.get("provider", "microsoft") in allow]
    ranked = sorted(pool, key=lambda it: score(query, it), reverse=True)
    out = []
    for it in ranked[:n]:
        d = dict(it)
        d["score"] = round(score(query, it), 3)
        out.append(d)
    return out


def fetch(url: str, dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    fname = url.rstrip("/").split("/")[-1]
    dest = dest_dir / fname
    safe = urllib.parse.quote(url, safe=":/?#[]@!$&'()*+,;=~")
    data = urllib.request.urlopen(safe, timeout=30).read()
    dest.write_bytes(data)
    return dest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("-n", type=int, default=5, help="number of candidates")
    ap.add_argument("--provider", help="restrict to providers (comma list): "
                    "aws, azure, microsoft")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--fetch", metavar="DIR", help="download/copy best match into DIR")
    args = ap.parse_args()

    if not INDEX.exists():
        sys.exit(f"Index missing at {INDEX}. Run build_icon_index.py first.")
    index = json.loads(INDEX.read_text("utf-8"))
    providers = [p.strip() for p in args.provider.split(",")] if args.provider else None
    results = search(args.query, args.n, index, providers)

    if args.fetch and results:
        top = results[0]
        if top.get("file"):  # bundled local icon
            src = SKILL_ROOT / top["file"]
            Path(args.fetch).mkdir(parents=True, exist_ok=True)
            dst = Path(args.fetch) / src.name
            dst.write_bytes(src.read_bytes())
            top["local_path"] = str(dst)
        elif top.get("url"):
            top["local_path"] = str(fetch(top["url"], Path(args.fetch)))

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            loc = r.get("file") or r.get("url", "")
            print(f"{r['score']:>5}  [{r.get('provider','?'):<9}] "
                  f"{r['name']:<40} {loc}")
        if args.fetch and results and results[0].get("local_path"):
            print(f"\nFetched -> {results[0]['local_path']}")


if __name__ == "__main__":
    main()
