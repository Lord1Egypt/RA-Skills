#!/usr/bin/env python3
"""
atl_check.py - CheapCharts All-Time-Low (ATL) checker

Verifies whether current CheapCharts deals are at their all-time low
using the authoritative priceHdIsLowest / priceSdIsLowest flags from
DetailData. Use the SKILL.md ATL recipe for full context.

Coverage reality (verified 2026-06-23): iTunes has the most complete
catalog and the most stable Deals endpoint. Amazon, Vudu, and Google
Play are supported mechanically (the script accepts --store for all
four) but the underlying CheapCharts data is sparser on those stores
and the Deals endpoint is more likely to return a server-side error.
For non-iTunes stores, --title lookups work more reliably than batch
mode.

The API has no rate limits - parallel DetailData calls are safe (the
script uses 8 concurrent workers by default).

Usage:
    python atl_check.py                       # batch: all current deals at ATL (iTunes)
    python atl_check.py --title "Fight Club"  # single title lookup
    python atl_check.py --store amazon        # batch on a specific store
    python atl_check.py --store amazon --title "Fight Club"  # single lookup on a specific store
    python atl_check.py --type seasons        # check TV seasons instead of movies
    python atl_check.py --type rentalmovies   # check rental movie deals
    python atl_check.py --sort latestPricechange  # sort by most recent price change
    python atl_check.py --genre Horror        # filter to a specific genre
    python atl_check.py --max-price 4.99      # only deals under $5
    python atl_check.py --release-year 2020-2025  # filter by release year range
    python atl_check.py --quality 4k         # only 4K items
    python atl_check.py --limit 30            # narrower deal pool
    python atl_check.py --min-savings 5       # only show items with $5+ savings
    python atl_check.py --json                # machine-readable output

Combined filters (per llms.txt guideline #11):
    python atl_check.py --genre Horror --max-price 4.99 --min-savings 3

Exit codes:
    0 - success (at least one ATL item or single-title check completed)
    1 - no ATL items found / single title not found
    2 - API error
"""

import argparse
import json
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote, urlencode

API_BASE = "https://buster.cheapcharts.de/v1"
DEFAULT_STORE = "itunes"
DEFAULT_COUNTRY = "us"
DEFAULT_LIMIT = 80
DEFAULT_SORT = "greatestSavings"
HTTP_TIMEOUT = 20
MAX_WORKERS = 8

# Valid sort options for Deals endpoint (per llms.txt + empirically discovered)
VALID_SORTS = (
    "latestPricechange",
    "price",
    "greatestSavings",
    "greatestPercentageSavings",
    "popularity",
    "alphabetical",
    "releaseDate",  # empirically discovered, ascending only (Pitfall #11)
)

# Valid genres (per llms.txt)
VALID_GENRES = (
    "All", "ActionAdventure", "Comedy", "Docus", "Drama", "MadeForTV",
    "Horror", "Classical", "Romance", "Independent", "KidsFamily",
    "MusicDocumentation", "SciFiFantasy", "Sport", "Thriller", "Western",
    "Anime", "Musicals",
)

# Valid quality values (per llms.txt)
VALID_QUALITIES = ("hd4k", "hd", "sd", "4k", "sdOnly")


def fetch(url):
    """Fetch URL with a User-Agent. Returns parsed JSON or raises."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
        return json.loads(r.read())


def get_id_from_url(url):
    """Extract (itemType, idInStore) from cheapChartsProductPageUrl."""
    m = re.search(r"/(movies|seasons)/(\d+)", url)
    return (m.group(1), m.group(2)) if m else (None, None)


def fetch_detail(itype, sid, store=DEFAULT_STORE, country=DEFAULT_COUNTRY):
    """Hit DetailData for a single title. Returns the inner node dict.

    Also returns error messages from the API if status=error (Pitfall #15).
    """
    url = f"{API_BASE}/DetailData.php?store={store}&country={country}&itemType={itype}&idInStore={sid}"
    data = fetch(url)
    # DetailData does NOT use the standard 'status' field - it uses results.<itemType>
    # But if it returns an error, it may have status=error
    if data.get("status") == "error":
        return {"_error": data.get("message", "unknown DetailData error")}
    return data.get("results", {}).get(itype, {})


def search_id(title, store=DEFAULT_STORE, country=DEFAULT_COUNTRY):
    """Search for a title, return (itype, sid, error_msg) tuple.

    Returns (None, None, error_msg) on API error so caller can display it.
    Returns (None, None, None) if title simply not found.
    Returns (itype, sid, None) on success.
    """
    url = (
        f"{API_BASE}/gptapi/Search.php?action=search&store={store}"
        f"&country={country}&itemType=all&query={quote(title)}&limit=1"
    )
    data = fetch(url)
    if data.get("status") == "error":
        return None, None, data.get("message", "unknown Search error")
    results = data.get("results", [])
    if not results:
        return None, None, None
    itype, sid = get_id_from_url(results[0].get("cheapChartsProductPageUrl", ""))
    return itype, sid, None


def is_atl(node):
    """True if HD or SD current price is at the all-time low (authoritative flag)."""
    return node.get("priceHdIsLowest") == 1 or node.get("priceSdIsLowest") == 1


def format_atl_line(a):
    """Pretty-print one ATL item."""
    price = a.get("price")
    was = a.get("was")
    if price is not None and was is not None and was != price:
        try:
            save = float(was) - float(price)
            pct = (save / float(was) * 100) if float(was) > 0 else 0
            save_str = f" (was ${was}, save ${save:.2f} / {pct:.0f}%)"
        except (TypeError, ValueError):
            save_str = f" (was ${was})"
    else:
        save_str = ""
    atl_label = "HD" if a.get("is_atl_hd") and not a.get("is_atl_sd") else (
        "SD" if a.get("is_atl_sd") and not a.get("is_atl_hd") else "BOTH"
    )
    store_url = a.get("store_url")
    url_part = f" | buy: {store_url}" if store_url else ""
    return f"  [{atl_label}] {a['title']} | ${price}{save_str} | changed {a.get('change_date', '?')}{url_part} | {a['url']}"


def check_single_title(title, store=DEFAULT_STORE, country=DEFAULT_COUNTRY):
    """Resolve a title via Search, then check DetailData for ATL status."""
    itype, sid, err = search_id(title, store, country)
    if err:
        print(f"  search error: {err}", file=sys.stderr)
        return 2
    if not sid:
        print(f"  not found: '{title}'")
        return 1
    node = fetch_detail(itype, sid, store, country)
    if not node or node.get("_error"):
        err_msg = node.get("_error", "unknown") if node else "empty response"
        print(f"  detail lookup failed for '{title}': {err_msg}", file=sys.stderr)
        return 2
    price = node.get("priceHd") or node.get("priceSd")
    print(f"  {node.get('title')}: ${price}")
    print(f"    ATL (IsLowest):      hd={node.get('priceHdIsLowest')} sd={node.get('priceSdIsLowest')}")
    print(f"    Current-sale floor (IsBest): hd={node.get('priceHdIsBest')} sd={node.get('priceSdIsBest')}")
    print(f"    Last change: {node.get('priceHdLastChangeDate') or node.get('priceSdLastChangeDate')}")
    # Store links (from DetailData)
    product_url = node.get("productPageUrl")
    itunes_url = node.get("iTunesUrl")
    cc_url = node.get("cheapChartsProductPageUrl")
    if product_url:
        print(f"    Buy on Apple TV: {product_url}")
    if itunes_url and itunes_url != product_url:
        print(f"    iTunes: {itunes_url}")
    if cc_url:
        print(f"    Price history: {cc_url}")
    if is_atl(node):
        print("    --> Currently at ATL")
    return 0


def build_deals_url(item_type, store, country, limit, sort, genre=None,
                    max_price=None, release_year=None, quality=None):
    """Build the Deals API URL with optional filters."""
    params = {
        "action": "getDeals",
        "store": store,
        "country": country,
        "itemType": item_type,
        "sort": sort,
        "limit": limit,
    }
    if genre and genre != "All":
        params["genre"] = genre
    if max_price is not None:
        params["maxPrice"] = max_price
    if release_year:
        params["releaseYear"] = release_year
    if quality and quality != "hd4k":
        params["quality"] = quality
    return f"{API_BASE}/gptapi/Deals.php?{urlencode(params)}"


def check_batch(item_type, store=DEFAULT_STORE, country=DEFAULT_COUNTRY, limit=DEFAULT_LIMIT,
                min_savings=None, output_json=False, sort=DEFAULT_SORT,
                genre=None, max_price=None, release_year=None, quality=None):
    """Pull current deals with optional filters, then in parallel verify
    each via DetailData's IsLowest flag."""
    deals_url = build_deals_url(
        item_type, store, country, limit, sort, genre, max_price, release_year, quality
    )
    data = fetch(deals_url)
    if data.get("status") != "success":
        msg = data.get("message", "unknown")
        print(f"  deals fetch failed: {msg}", file=sys.stderr)
        if store != DEFAULT_STORE:
            print(f"  note: CheapCharts' Deals endpoint is most stable for iTunes. For {store},", file=sys.stderr)
            print(f"  try --title <name> for a single-title lookup, or use --store itunes for batch.", file=sys.stderr)
        return 2
    deals = data.get("results", {}).get(item_type, [])
    if not deals:
        print(f"  no {item_type} deals returned")
        return 1

    # Map each deal to (deal, itype, sid) up front
    candidates = []
    for d in deals:
        itype, sid = get_id_from_url(d.get("cheapChartsProductPageUrl", ""))
        if itype and sid:
            candidates.append((d, itype, sid))

    # Parallel DetailData fetches
    atl = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        future_to_deal = {
            pool.submit(fetch_detail, itype, sid, store, country): (d, itype)
            for d, itype, sid in candidates
        }
        for fut in as_completed(future_to_deal):
            d, itype = future_to_deal[fut]
            try:
                node = fut.result()
            except Exception:
                continue
            if not node or node.get("_error"):
                continue
            if not is_atl(node):
                continue
            price = node.get("priceHd") or node.get("priceSd")
            was = node.get("priceHdBefore") or node.get("priceSdBefore")
            if min_savings is not None and price is not None and was is not None:
                try:
                    if float(was) - float(price) < min_savings:
                        continue
                except (TypeError, ValueError):
                    pass
            atl.append({
                "title": node.get("title"),
                "price": price,
                "was": was,
                "change_date": node.get("priceHdLastChangeDate") or node.get("priceSdLastChangeDate"),
                "is_atl_hd": node.get("priceHdIsLowest") == 1,
                "is_atl_sd": node.get("priceSdIsLowest") == 1,
                "url": d.get("cheapChartsProductPageUrl"),
                "store_url": node.get("productPageUrl") or node.get("iTunesUrl"),
            })

    if output_json:
        print(json.dumps(atl, indent=2))
    else:
        filter_desc = []
        if genre and genre != "All":
            filter_desc.append(f"genre={genre}")
        if max_price is not None:
            filter_desc.append(f"maxPrice=${max_price}")
        if release_year:
            filter_desc.append(f"releaseYear={release_year}")
        if quality and quality != "hd4k":
            filter_desc.append(f"quality={quality}")
        filter_str = f" [{', '.join(filter_desc)}]" if filter_desc else ""
        print(f"=== {len(atl)} {item_type} currently at ATL (out of {len(candidates)} checked){filter_str} ===\n")
        for a in atl:
            print(format_atl_line(a))
    return 0 if atl else 1


def main():
    p = argparse.ArgumentParser(
        description="CheapCharts All-Time-Low (ATL) checker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Combined filters example: python atl_check.py --genre Horror --max-price 4.99 --min-savings 3"
    )
    p.add_argument("--title", help="Check a single title (resolves via Search)")
    p.add_argument("--type", choices=("buymovies", "seasons", "rentalmovies"), default="buymovies",
                   help="Item type for batch mode (default: buymovies)")
    p.add_argument("--store", default=DEFAULT_STORE, help=f"Store (default: {DEFAULT_STORE})")
    p.add_argument("--country", default=DEFAULT_COUNTRY, help=f"Country code (default: {DEFAULT_COUNTRY})")
    p.add_argument("--limit", type=int, default=DEFAULT_LIMIT,
                   help=f"Deals pool size for batch mode (default: {DEFAULT_LIMIT})")
    p.add_argument("--min-savings", type=float, default=None,
                   help="Only show ATL items with at least this $ savings vs priceBefore")
    p.add_argument("--sort", choices=VALID_SORTS, default=DEFAULT_SORT,
                   help=f"Sort order for Deals (default: {DEFAULT_SORT})")
    p.add_argument("--genre", default=None,
                   help=f"Genre filter (e.g. Horror, ActionAdventure, Comedy). Unknown values silently fall back to All.")
    p.add_argument("--max-price", type=float, default=None,
                   help="Maximum price filter (e.g. 4.99)")
    p.add_argument("--release-year", default=None,
                   help="Release year range (e.g. 2020-2025 or 2026-2026)")
    p.add_argument("--quality", choices=VALID_QUALITIES, default="hd4k",
                   help="Quality filter (default: hd4k)")
    p.add_argument("--json", action="store_true", help="Emit JSON (batch mode only)")
    args = p.parse_args()

    try:
        if args.title:
            return check_single_title(args.title, args.store, args.country)
        if args.store == "games":
            print("  CheapCharts Games has no public API (verified 2026-06-23).", file=sys.stderr)
            print("  For current game deals, see: https://games.cheapcharts.com", file=sys.stderr)
            print("  Or use the CheapCharts Games mobile apps (iOS: id1622193150, Android: com.cheapcharts.cheapcharts_games).", file=sys.stderr)
            return 2
        return check_batch(
            item_type=args.type,
            store=args.store,
            country=args.country,
            limit=args.limit,
            min_savings=args.min_savings,
            output_json=args.json,
            sort=args.sort,
            genre=args.genre,
            max_price=args.max_price,
            release_year=args.release_year,
            quality=args.quality,
        )
    except Exception as e:
        print(f"  error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
