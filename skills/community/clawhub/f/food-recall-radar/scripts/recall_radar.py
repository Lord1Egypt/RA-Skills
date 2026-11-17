#!/usr/bin/env python3
"""
recall_radar.py — personal pantry inventory matched against live FDA food recalls.

Data: openFDA food enforcement endpoint (no key needed for light use).
Pantry: local JSON (default ~/.pantry.json). Pure stdlib.

Subcommands:
  add, import-receipt, list, remove    — pantry management
  match                                — pantry vs live/cached recalls
  audit                                — match + category heuristics (weekly use)
  report                               — history of hits
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from difflib import SequenceMatcher

DEFAULT_PANTRY = os.path.join(os.path.expanduser("~"), ".pantry.json")
OPENFDA = "https://api.openfda.gov/food/enforcement.json"

# ---------------------------------------------------------------- normalize

STOP = {
    "inc", "ltd", "llc", "co", "corp", "company", "brands", "brand",
    "the", "and", "of", "for", "a", "an", "oz", "ounce", "ounces", "lb", "lbs",
    "g", "gram", "grams", "ct", "count", "pack", "size", "new", "usa",
}
GENERIC_PRODUCT = {
    "natural", "organic", "fresh", "original", "premium", "select", "value",
    "food", "foods", "product", "products", "frozen", "item",
}

def norm(s: str) -> str:
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    return " ".join(w for w in s.split() if w and w not in STOP)

def tokens(s: str, extra_drop=None):
    drop = STOP | (extra_drop or set())
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    return [w for w in s.split() if w not in drop]

def fuzzy_contains(hay: str, needle: str, floor=0.82) -> bool:
    """True if some window of `hay` resembles `needle` closely."""
    h, n = norm(hay), norm(needle)
    if not h or not n:
        return False
    if n in h:
        return True
    ntoks = n.split()
    width = len(ntoks)
    for i in range(0, max(1, len(h.split()) - width + 1)):
        window = " ".join(h.split()[i:i + width])
        if window and SequenceMatcher(None, window, n).ratio() >= floor:
            return True
    return False

# ---------------------------------------------------------------- pantry

def load(path):
    if os.path.exists(path):
        try:
            return json.load(open(path))
        except Exception as e:
            die(f"pantry file unreadable: {e}")
    return {"items": [], "hits": []}

def save(db, path):
    with open(path, "w") as f:
        json.dump(db, f, indent=2)

def die(msg, code=1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)

def add_item(db, brand, product, upc=None, lot=None, notes=None):
    item = {
        "brand": brand, "product": product,
        "upc": (upc or "").replace(" ", "") or None,
        "lot": lot or None, "notes": notes or None,
        "added": dt.date.today().isoformat(),
    }
    db["items"].append(item)
    return item

# ---------------------------------------------------------------- recalls

def fetch_recalls(api_key=None, limit=1000, verbose=False):
    q = urllib.parse.quote('status:"Ongoing"')
    url = f"{OPENFDA}?search={q}&limit={limit}"
    if api_key:
        url += f"&api_key={api_key}"
    if verbose:
        print(f"# fetching {url}", file=sys.stderr)
    req = urllib.request.Request(url, headers={"User-Agent": "food-recall-radar/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode())
    return [
        {
            "id": r.get("recall_number", ""),
            "class": (r.get("classification") or "").replace("Classification", "").strip(),
            "firm": r.get("recalling_firm", ""),
            "product": r.get("product_description", ""),
            "reason": r.get("reason_for_recall", ""),
            "code_info": r.get("code_info", ""),
            "report_date": r.get("report_date", ""),
            "initiation": r.get("recall_initiation_date", ""),
            "url": r.get("url") or (r.get("more_repo_info") or [{}])[0].get("link", ""),
            "distribution": r.get("distribution_pattern", ""),
        }
        for r in data.get("results", [])
    ]

def load_cached(path):
    raw = json.load(open(path))
    if isinstance(raw, dict) and "results" in raw:
        raw = raw["results"]
    out = []
    for r in raw:
        out.append({
            "id": r.get("recall_number", r.get("id", "")),
            "class": r.get("classification", r.get("class", "")),
            "firm": r.get("recalling_firm", r.get("firm", "")),
            "product": r.get("product_description", r.get("product", "")),
            "reason": r.get("reason_for_recall", r.get("reason", "")),
            "code_info": r.get("code_info", r.get("code_info", "")),
            "report_date": r.get("report_date", ""),
            "initiation": r.get("file", ""),
            "url": r.get("url", ""),
            "distribution": r.get("distribution_pattern", ""),
        })
    return out

LOT_PATTERNS = [
    (r"(?:lot|batch)[\s#:]*([A-Z0-9][A-Z0-9\-./]{3,})", "lot/batch code"),
    (r"best\s*by[\s:]*([A-Z0-9/.\- ]{4,20})", "best-by date"),
    (r"use\s*by[\s:]*([A-Z0-9/.\- ]{4,20})", "use-by date"),
    (r"EXP?[\s:]*([A-Z0-9/.\- ]{4,20})", "expiry"),
    (r"(?:sell|freeze)\s*by[\s:]*([A-Z0-9/.\- ]{4,20})", "sell/freeze-by"),
]

def extract_lot_intel(recall):
    text = " ".join(x for x in (recall.get("code_info"), recall.get("product")) if x)
    found = []
    for pat, label in LOT_PATTERNS:
        for m in re.finditer(pat, text, flags=re.I):
            val = m.group(1).strip()
            if val and (label, val) not in found:
                found.append((label, val))
    return found

# ---------------------------------------------------------------- scoring

def score(item, recall):
    """Return (kind, score, detail) where kind in MATCH/VERIFY/WATCH."""
    hay = " ".join([recall["firm"], recall["product"]])
    rproduct_toks = set(tokens(recall["product"], GENERIC_PRODUCT))
    pproduct_toks = set(tokens(item["product"], GENERIC_PRODUCT))
    overlap = rproduct_toks & pproduct_toks
    jac = len(overlap) / len(rproduct_toks | pproduct_toks) if (rproduct_toks | pproduct_toks) else 0.0
    brand_hit = fuzzy_contains(hay, item["brand"] or "")
    seq = SequenceMatcher(None, norm(item["product"]), norm(recall["product"])).ratio()

    # UPC shortcut — near-exact
    if item.get("upc"):
        for upc in re.findall(r"\d{12,14}", hay):
            if upc == item["upc"]:
                return "MATCH", 1.0, "UPC equality"

    s = 0.0
    if brand_hit:
        s += 0.45
    s += 0.35 * min(1.0, jac * 2.0)          # product-token overlap
    s += 0.20 * seq                            # whole-string similarity

    if brand_hit and jac >= 0.25:
        return "VERIFY", max(s, 0.80), f"brand+product (overlap={sorted(overlap)})"
    if brand_hit and seq >= 0.55:
        return "VERIFY", max(s, 0.70), f"brand+sequence (seq={seq:.2f})"
    if s >= 0.72:
        return "VERIFY", s, f"composite (overlap={sorted(overlap)}, seq={seq:.2f})"
    # audit-only: strong product overlap without brand hit (store-brand case)
    if jac >= 0.34 and len(overlap) >= 2:
        return "WATCH", 0.55, f"product-only (store-brand suspect, overlap={sorted(overlap)})"
    return None, s, ""

CLASS_RANK = {"Class I": 1, "Class II": 2, "Class III": 3, "": 4}

# ---------------------------------------------------------------- commands

def cmd_add(a):
    db = load(a.file)
    item = add_item(db, a.brand, a.product, a.upc, a.lot, a.notes)
    save(db, a.file)
    print(f"added: {item['brand']} / {item['product']}" +
          (f" (upc {item['upc']})" if item["upc"] else ""))

def cmd_import(a):
    db = load(a.file)
    print("Paste lines of 'Brand Product' (Ctrl-D to finish):", file=sys.stderr)
    n = 0
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        m = re.match(r"^(\d{12,14})\s+(.*)$", line)
        upc, rest = (m.group(1), m.group(2)) if m else (None, line)
        parts = rest.split(None, 1)
        if len(parts) == 2:
            brand, product = parts
        else:
            brand, product = parts[0] if parts else "", ""
        add_item(db, brand, product, upc=upc)
        n += 1
        print(f"  + {brand} / {product}")
    save(db, a.file)
    print(f"imported {n} items → {a.file}")

def cmd_list(a):
    db = load(a.file)
    if not db["items"]:
        print("(pantry empty — add items first)")
        return
    print(f"{len(db['items'])} items in {a.file}:")
    for i, it in enumerate(db["items"]):
        lot = f" lot={it['lot']}" if it.get("lot") else ""
        upc = f" upc={it['upc']}" if it.get("upc") else ""
        print(f"  [{i}] {it['brand']} / {it['product']}{upc}{lot}")

def cmd_remove(a):
    db = load(a.file)
    before = len(db["items"])
    kept = []
    for it in db["items"]:
        same_brand = norm(it["brand"]) == norm(a.brand or "")
        same_product = a.product and norm(it["product"]) == norm(a.product)
        if not (same_brand and same_product):
            kept.append(it)
    db["items"] = kept
    save(db, a.file)
    print(f"removed {before - len(kept)} item(s)")

def get_recalls(a):
    if a.offline:
        if not a.data:
            die("--offline requires --data <cached.json>")
        if a.verbose:
            print(f"# using cached data: {a.data}", file=sys.stderr)
        return load_cached(a.data)
    api_key = a.api_key or os.environ.get("OPENFDA_API_KEY")
    try:
        return fetch_recalls(api_key=api_key, verbose=a.verbose)
    except Exception as e:
        hint = " (try --offline --data <file> if the network is down)" if not a.data else ""
        die(f"openFDA unreachable: {e}{hint}")

def render_hits(hits, db=None):
    if not hits:
        print("✅ No matches against ongoing FDA food recalls.")
        return
    hits.sort(key=lambda h: (CLASS_RANK.get(h["recall"]["class"], 4), -h["score"]))
    for h in hits:
        r = h["recall"]
        print(f"[{h['kind']}] {r['class'] or 'unclassified'}  (score {h['score']:.2f}) ── {h['detail']}")
        print(f"  your item: {h['item']['brand']} / {h['item']['product']}")
        print(f"  recall:    {(r['product'] or '(no description)')[:120]}")
        print(f"  firm:      {r['firm']}")
        print(f"  reason:    {r['reason']}")
        if r["initiation"]:
            print(f"  initiated: {r['initiation']}")
        intel = extract_lot_intel(r)
        if intel:
            print("  lot intel: " + "; ".join(f"{label}: {val}" for label, val in intel[:4]))
        if h["kind"] == "WATCH":
            print("  action:    WATCH — store-brand/co-packer overlap; read the notice")
        else:
            print("  action:    DO NOT EAT — check package vs notice; return for refund or discard")
        if r["url"]:
            print(f"  notice:    {r['url']}")
        print()

def cmd_match(a, audit_mode=False):
    db = load(a.file)
    if not db["items"]:
        die("pantry empty — run `add` first")
    recalls = get_recalls(a)
    print(f"# {len(recalls)} ongoing recalls loaded; matching {len(db['items'])} pantry items",
          file=sys.stderr)
    hits = []
    for item in db["items"]:
        for r in recalls:
            kind, s, detail = score(item, r)
            if kind and (audit_mode or kind != "WATCH"):
                hits.append({"kind": kind, "score": s, "detail": detail,
                             "item": item, "recall": r})
    render_hits(hits)
    if hits:
        db.setdefault("hits", []).append({
            "ts": dt.datetime.now().isoformat(timespec="minutes"),
            "mode": "audit" if audit_mode else "match",
            "found": [{"kind": h["kind"], "item": h["item"]["brand"] + " / " + h["item"]["product"],
                       "recall_id": h["recall"]["id"], "class": h["recall"]["class"],
                       "reason": h["recall"]["reason"]} for h in hits],
        })
        save(db, a.file)

def cmd_audit(a):
    cmd_match(a, audit_mode=True)

def cmd_report(a):
    db = load(a.file)
    hist = db.get("hits", [])
    if not hist:
        print("(no recall hits recorded — either clean or not yet run)")
        return
    for run in hist:
        print(f"— {run['ts']} ({run['mode']}):")
        for fnd in run["found"]:
            print(f"    [{fnd['kind']}] {fnd['class']} {fnd['item']} ← recall {fnd['recall_id']} ({fnd['reason']})")

# ---------------------------------------------------------------- cli

def main():
    p = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--file", default=DEFAULT_PANTRY, help="pantry JSON path")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("add", help="add one item")
    sp.add_argument("--brand", required=True)
    sp.add_argument("--product", required=True)
    spl = sp.add_argument("--upc")
    sp.add_argument("--lot")
    sp.add_argument("--notes")
    sp.set_defaults(func=cmd_add)

    sp = sub.add_parser("import-receipt", help="bulk add 'Brand Product' lines from stdin")
    sp.set_defaults(func=cmd_import)

    sp = sub.add_parser("list", help="list pantry")
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("remove", help="remove item by brand+product")
    sp.add_argument("--brand", required=True)
    sp.add_argument("--product", required=True)
    sp.set_defaults(func=cmd_remove)

    for name, fn, help_ in (("match", cmd_match, "match pantry vs live/cached recalls"),
                            ("audit", cmd_audit, "match + category heuristics (weekly)"),
                            ("report", cmd_report, "show history of hits")):
        sp = sub.add_parser(name, help=help_)
        sp.add_argument("--offline", action="store_true")
        sp.add_argument("--data", help="cached recalls JSON (openFDA format or simple list)")
        sp.add_argument("--api-key", help="openFDA key (or OPENFDA_API_KEY env)")
        sp.add_argument("--verbose", action="store_true")
        sp.set_defaults(func=fn)

    a = p.parse_args()
    a.func(a)

if __name__ == "__main__":
    main()
