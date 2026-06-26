#!/usr/bin/env python3
"""Discover candidate products for the weekly newsletter lookbook.

Spec: references/headless-mode.md § "Recurring weekly newsletter".

Two filters in priority order:
  1. /seasonal?days=N — products set live on buckmason.com in the last N days
  2. General catalog backfill, filtered against the wishlist (items the
     customer has been pitched before)

The output is a JSON list of candidates with full product detail + variant
matching the customer's stated size. The agent (taste-aware) reads the list
and picks the final ~4-6 pieces; this script doesn't curate.

Usage:
  scripts/discover-weekly-candidates.py \
    --gender m \
    --since-days 14 \
    --wishlist ~/.buck-mason-stylist/wishlist.jsonl \
    --sizes '{"shirt":"L","tee":"L","pant":"31","short":"L"}' \
    --avoid-colors 'vintage_product,Black' \
    [--max 30] \
    > candidates.json

Stdout is JSON, side-effect-free. The script never writes to wishlist.jsonl
itself — the agent is responsible for logging what gets actually proposed
after picking the final set.

Exit codes: 0 always (an empty candidate list is a valid result that the
agent handles by surfacing "nothing new this week" or backfilling from the
recommend endpoint).
"""
import argparse, json, pathlib, subprocess, sys, time, urllib.parse

ap = argparse.ArgumentParser(description="Discover weekly newsletter candidates.")
ap.add_argument("--gender",         required=True, choices=["m", "w", "u"])
ap.add_argument("--since-days",     type=int, default=14)
ap.add_argument("--wishlist",       type=pathlib.Path, required=True)
ap.add_argument("--sizes",          required=True, help='JSON: {"shirt":"L","pant":"31",...}')
ap.add_argument("--avoid-colors",   default="vintage_product",
                help="Comma-separated color values to drop (default: vintage_product). Catches Mason Made / archival noise.")
ap.add_argument("--max",            type=int, default=30, help="Max candidates returned")
ap.add_argument("--re-propose-after-weeks", type=int, default=8,
                help="A piece can re-appear in a candidate list after this many weeks since proposed_at. Default 8.")
args = ap.parse_args()

SIZES = json.loads(args.sizes)
AVOID = {c.strip() for c in args.avoid_colors.split(",") if c.strip()}
MIN_AGE_TO_RE_PROPOSE_S = args.re_propose_after_weeks * 7 * 86400

def curl(url):
    for _ in range(3):
        r = subprocess.run(["curl", "-sS", "--max-time", "20", url], capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.startswith("{"):
            return json.loads(r.stdout)
        time.sleep(0.5)
    raise RuntimeError(f"failed: {url}")

# ── Load wishlist (long-term proposed-or-purchased SKU set) ─────────────────

proposed = {}  # sku -> latest proposed_at (UTC ISO string)
if args.wishlist.exists():
    for line in args.wishlist.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        sku = r.get("sku")
        ts  = r.get("proposed_at") or r.get("purchased_at")
        if sku and ts:
            # Keep the most recent timestamp seen for each SKU.
            if sku not in proposed or ts > proposed[sku]:
                proposed[sku] = ts

now = time.time()
def is_eligible(sku):
    """Drop if proposed within the re-propose lockout window."""
    ts = proposed.get(sku)
    if not ts:
        return True
    try:
        ts_epoch = time.mktime(time.strptime(ts.split(".")[0].rstrip("Z"), "%Y-%m-%dT%H:%M:%S"))
    except (ValueError, TypeError):
        return True  # Garbled timestamp — don't block on it; better to risk a re-propose than to skip forever.
    return (now - ts_epoch) > MIN_AGE_TO_RE_PROPOSE_S

# ── Source 1: recently-live products ────────────────────────────────────────
# /products?recently_live=true orders by created_at DESC, so freshest first.
# (Verified against pima-master#products controller.)

PER = max(args.max * 4, 60)  # over-fetch — vintage_product noise drops a lot pre-dedup
recent_url = f"https://pima.io/mcp/buckmason/products?gender={args.gender}&recently_live=true&recently_live_days={args.since_days}&per_page={PER}"
recent = curl(recent_url)
recent_products = recent.get("products") or []

# ── Source 2: backfill (general catalog, alphabetical) ──────────────────────

backfill_url = f"https://pima.io/mcp/buckmason/products?gender={args.gender}&per_page={PER}"
backfill = curl(backfill_url)
backfill_products = backfill.get("products") or []

# ── Combine + filter + size-match ───────────────────────────────────────────

def category_size_for(product):
    """Pick the right --sizes key for a product based on its category."""
    cat = (product.get("category") or "").lower()
    if "shirt" in cat:                       return SIZES.get("shirt")
    if "tee" in cat or "polo" in cat:        return SIZES.get("tee")
    if "pant" in cat or "trouser" in cat:    return SIZES.get("pant")
    if "short" in cat:                       return SIZES.get("short")
    if "jacket" in cat or "outerwear" in cat: return SIZES.get("jacket")
    if "shoe" in cat:                        return SIZES.get("shoe")
    return None

candidates = []
seen_ids = set()
for source, plist in [("recently_live", recent_products), ("backfill", backfill_products)]:
    for p in plist:
        pid = p.get("id")
        if not pid or pid in seen_ids:
            continue
        if p.get("color") in AVOID:
            continue
        # Need a size for this category, otherwise skip
        target_size = category_size_for(p)
        if not target_size:
            continue
        # Skip vintage_product sentinels even if the name slipped past
        if p.get("color_rgb") == "#ff0000" and p.get("color") == "vintage_product":
            continue

        # Need to look up the SKU to dedup against the wishlist properly,
        # since the products list doesn't carry per-variant SKU.
        try:
            detail = curl(f"https://pima.io/mcp/buckmason/products/{pid}")
        except Exception as e:
            print(f"warn: failed to load detail for {pid}: {e}", file=sys.stderr)
            continue
        variant = next((v for v in detail.get("variants", []) if v.get("size") == target_size), None)
        if not variant:
            continue
        sku = variant.get("sku")
        if not sku:
            continue
        if not is_eligible(sku):
            continue
        # Stock check — drop pieces that are out everywhere
        online = variant.get("online") or {}
        if isinstance(online, dict) and not online.get("in_stock", True):
            continue

        candidates.append({
            "source":      source,
            "id":          pid,
            "slug":        detail.get("slug"),
            "name":        detail.get("name"),
            "color":       detail.get("color"),
            "category":    detail.get("category"),
            "price":       detail.get("price"),
            "price_cents": detail.get("price_cents"),
            "url":         detail.get("url"),
            "size":        target_size,
            "sku":         sku,
            "shopify_variant_id": variant.get("shopify_variant_id"),
            "in_stock_online":    variant.get("online"),
            "image_url":   detail.get("image_url"),
            "previously_proposed_at": proposed.get(sku),
        })
        seen_ids.add(pid)
        if len(candidates) >= args.max:
            break
    if len(candidates) >= args.max:
        break

print(json.dumps({
    "generated_at":     time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "filter": {
        "gender": args.gender, "since_days": args.since_days,
        "sizes": SIZES, "avoid_colors": sorted(AVOID),
        "wishlist_size": len(proposed),
    },
    "candidate_count": len(candidates),
    "candidates":      candidates,
}, indent=2))
