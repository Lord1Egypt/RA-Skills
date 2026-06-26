#!/usr/bin/env python3
"""
Clawdible CLI — Audible management for OpenClaw.

Commands:
  status                        Show auth status, account, locale, library count
  search <query>                Search Audible catalogue
  library [--limit N]           List your library
  info <asin>                   Get book details
  buy <asin> --confirm          Purchase (requires --confirm flag)
  wishlist                      Show wishlist
  wishlist add <asin>           Add to wishlist

Flags:
  --locale LOCALE               Override marketplace locale (default: auto from auth file)
  --json                        Output as JSON
  --limit N                     Limit results (default varies per command)
"""

import sys
import os
import json
import argparse
import subprocess
from pathlib import Path

# ── Dependency check & auto-install ──────────────────────────────────────────
def ensure_deps():
    missing = []
    for pkg in ["audible", "httpx"]:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"Installing missing dependencies: {', '.join(missing)}...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--quiet"] + missing
            )
            print("Dependencies installed.\n")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to install dependencies: {e}")
            print(f"Run manually: pip3 install {' '.join(missing)}")
            sys.exit(1)

ensure_deps()

import audible
import httpx
from urllib.parse import parse_qs

# ── Constants ─────────────────────────────────────────────────────────────────
AUTH_FILE = Path.home() / ".config" / "audible" / "auth.json"

MARKETPLACE_DOMAINS = {
    "us": "audible.com",
    "au": "audible.com.au",
    "uk": "audible.co.uk",
    "de": "audible.de",
    "ca": "audible.ca",
    "fr": "audible.fr",
    "in": "audible.in",
    "it": "audible.it",
    "jp": "audible.co.jp",
    "es": "audible.es",
}

# ── Auth helpers ──────────────────────────────────────────────────────────────
def load_auth():
    if not AUTH_FILE.exists():
        print(f"ERROR: No auth file found at {AUTH_FILE}")
        print("Run the auth setup script first:")
        print("  python3 <skill_dir>/scripts/audible_auth.py")
        sys.exit(1)
    try:
        return audible.Authenticator.from_file(AUTH_FILE)
    except Exception as e:
        print(f"ERROR: Failed to load auth: {e}")
        print("Try re-authenticating: python3 <skill_dir>/scripts/audible_auth.py")
        sys.exit(1)

def detect_locale():
    """Read locale from auth file, default to 'us'."""
    if AUTH_FILE.exists():
        try:
            data = json.loads(AUTH_FILE.read_text())
            return data.get("locale_code", "us")
        except Exception:
            pass
    return "us"

def get_client(locale):
    auth = load_auth()
    try:
        auth.locale = locale
    except Exception:
        pass
    return audible.Client(auth=auth)

def fallback_url(asin, locale):
    domain = MARKETPLACE_DOMAINS.get(locale, "audible.com")
    return f"https://www.{domain}/pd/{asin}"

# ── Output helpers ────────────────────────────────────────────────────────────
def output(data, as_json=False):
    if as_json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        if isinstance(data, str):
            print(data)
        elif isinstance(data, list):
            for item in data:
                print(item)

# ── Commands ──────────────────────────────────────────────────────────────────
def cmd_status(args):
    locale = args.locale or detect_locale()
    try:
        with get_client(locale) as client:
            result = client.get("1.0/library", num_results=1, response_groups="product_desc")
            # Try to get account info
            customer = {}
            try:
                me = client.get("1.0/customer/information", response_groups="migration_details")
                customer = me.get("customer_information", {})
            except Exception:
                pass

            total = result.get("total_count", "unknown")
            name = customer.get("given_name") or customer.get("name") or "Unknown"

            if args.json:
                output({"status": "authenticated", "account": name,
                        "locale": locale, "library_count": total}, as_json=True)
            else:
                print(f"Status:        ✅ Authenticated")
                print(f"Locale:        {locale}")
                print(f"Library:       {total} titles")
                print(f"Auth file:     {AUTH_FILE}")
    except audible.exceptions.NetworkError as e:
        print(f"ERROR: Network error — {e}")
        sys.exit(1)
    except Exception as e:
        msg = str(e)
        if "401" in msg or "403" in msg:
            print("ERROR: Auth token expired. Re-run audible_auth.py to re-authenticate.")
        else:
            print(f"ERROR: {e}")
        sys.exit(1)

def cmd_search(args):
    locale = args.locale or detect_locale()
    query = " ".join(args.query)
    try:
        with get_client(locale) as client:
            results = client.get(
                "1.0/catalog/products",
                num_results=args.limit,
                keywords=query,
                response_groups="product_desc,media,product_attrs,contributors",
            )
    except audible.exceptions.NetworkError as e:
        print(f"ERROR: Network error — {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Search failed — {e}")
        sys.exit(1)

    products = results.get("products", [])
    if not products:
        print("No results found.")
        return

    if args.json:
        out = []
        for p in products:
            out.append({
                "title": p.get("title"),
                "authors": [a.get("name") for a in p.get("authors", [])],
                "asin": p.get("asin"),
                "runtime_min": p.get("runtime_length_min", 0),
            })
        output(out, as_json=True)
    else:
        for i, p in enumerate(products, 1):
            title = p.get("title", "Unknown")
            authors = ", ".join(a.get("name", "") for a in p.get("authors", []))
            asin = p.get("asin", "")
            runtime = p.get("runtime_length_min", 0)
            h, m = divmod(runtime, 60)
            print(f"{i}. {title}")
            print(f"   Author: {authors}")
            print(f"   ASIN: {asin}  |  Length: {h}h {m}m")
            print()

def cmd_library(args):
    locale = args.locale or detect_locale()
    try:
        with get_client(locale) as client:
            library = client.get(
                "1.0/library",
                num_results=args.limit,
                response_groups="product_desc,media,product_attrs,contributors",
                sort_by="-PurchaseDate",
            )
    except audible.exceptions.NetworkError as e:
        print(f"ERROR: Network error — {e}")
        sys.exit(1)
    except Exception as e:
        msg = str(e)
        if "401" in msg or "403" in msg:
            print("ERROR: Auth token expired. Re-run audible_auth.py.")
        else:
            print(f"ERROR: {e}")
        sys.exit(1)

    items = library.get("items", [])
    if not items:
        print("Library is empty or no items returned.")
        return

    if args.json:
        out = [{"title": i.get("title"), "authors": [a.get("name") for a in i.get("authors", [])],
                "asin": i.get("asin")} for i in items]
        output(out, as_json=True)
    else:
        print(f"Library ({len(items)} items shown):\n")
        for i, item in enumerate(items, 1):
            title = item.get("title", "Unknown")
            authors = ", ".join(a.get("name", "") for a in item.get("authors", []))
            asin = item.get("asin", "")
            print(f"{i}. {title}")
            print(f"   Author: {authors}  |  ASIN: {asin}")
            print()

def cmd_info(args):
    locale = args.locale or detect_locale()
    try:
        with get_client(locale) as client:
            result = client.get(
                f"1.0/catalog/products/{args.asin}",
                response_groups="product_desc,media,product_attrs,contributors,product_extended_attrs",
            )
    except Exception as e:
        msg = str(e)
        if "404" in msg:
            print(f"ERROR: ASIN '{args.asin}' not found in {locale} marketplace.")
            print(f"Try a different --locale or check the ASIN.")
        else:
            print(f"ERROR: {e}")
        sys.exit(1)

    p = result.get("product", {})
    title = p.get("title", "Unknown")
    authors = ", ".join(a.get("name", "") for a in p.get("authors", []))
    narrators = ", ".join(n.get("name", "") for n in p.get("narrators", []))
    summary = p.get("merchandising_summary", "")
    # Strip HTML tags
    import re
    summary = re.sub(r"<[^>]+>", "", summary).strip()
    runtime = p.get("runtime_length_min", 0)
    h, m = divmod(runtime, 60)

    if args.json:
        output({"title": title, "authors": authors, "narrators": narrators,
                "length_min": runtime, "asin": args.asin, "summary": summary}, as_json=True)
    else:
        print(f"Title:    {title}")
        print(f"Author:   {authors}")
        print(f"Narrator: {narrators}")
        print(f"Length:   {h}h {m}m")
        print(f"ASIN:     {args.asin}")
        if summary:
            print(f"\n{summary[:500]}{'...' if len(summary) > 500 else ''}")

def cmd_buy(args):
    if not args.confirm:
        print("ERROR: Purchase requires --confirm flag.")
        print(f"  buy {args.asin} --confirm")
        print("\nAlways confirm with the user before purchasing.")
        sys.exit(1)

    locale = args.locale or detect_locale()
    try:
        with get_client(locale) as client:
            # Get title first for confirmation
            try:
                r = client.get(f"1.0/catalog/products/{args.asin}", response_groups="product_desc")
                title = r.get("product", {}).get("title", args.asin)
                print(f"Purchasing: {title}")
            except Exception:
                print(f"Purchasing ASIN: {args.asin}")

            client.post("1.0/orders", body={"asin": args.asin, "audibleCreditApplied": True})
            print(f"✅ Purchased successfully! Check your library.")
    except audible.exceptions.NetworkError as e:
        print(f"ERROR: Network error — {e}")
        url = fallback_url(args.asin, locale)
        print(f"Try purchasing manually: {url}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Purchase failed — {e}")
        url = fallback_url(args.asin, locale)
        print(f"Purchase manually at: {url}")
        sys.exit(1)

def cmd_wishlist(args):
    locale = args.locale or detect_locale()
    if getattr(args, "action", None) == "add" and getattr(args, "asin", None):
        try:
            with get_client(locale) as client:
                client.post("1.0/wishlist", body={"asin": args.asin})
            print(f"✅ Added {args.asin} to wishlist.")
        except Exception as e:
            print(f"ERROR: {e}")
            sys.exit(1)
    else:
        try:
            with get_client(locale) as client:
                result = client.get("1.0/wishlist", num_results=50,
                                    response_groups="product_desc,contributors")
        except Exception as e:
            print(f"ERROR: {e}")
            sys.exit(1)

        items = result.get("products", [])
        if not items:
            print("Wishlist is empty.")
            return

        if args.json:
            out = [{"title": p.get("title"), "asin": p.get("asin")} for p in items]
            output(out, as_json=True)
        else:
            print(f"Wishlist ({len(items)} items):\n")
            for i, p in enumerate(items, 1):
                title = p.get("title", "Unknown")
                authors = ", ".join(a.get("name", "") for a in p.get("authors", []))
                print(f"{i}. {title}")
                print(f"   Author: {authors}  |  ASIN: {p.get('asin', '')}")
                print()

# ── Argument parser ───────────────────────────────────────────────────────────
def main():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--locale", default=None,
                        help="Marketplace locale: us, au, uk, de, ca, fr, in, it, jp, es")
    common.add_argument("--json", action="store_true", help="Output as JSON")

    parser = argparse.ArgumentParser(
        description="Clawdible — Audible CLI for OpenClaw",
        parents=[common],
    )
    subparsers = parser.add_subparsers(dest="command")

    p_status = subparsers.add_parser("status", parents=[common], add_help=True)

    p_search = subparsers.add_parser("search", parents=[common], add_help=True)
    p_search.add_argument("query", nargs="+")
    p_search.add_argument("--limit", type=int, default=10)

    p_lib = subparsers.add_parser("library", parents=[common], add_help=True)
    p_lib.add_argument("--limit", type=int, default=20)

    p_info = subparsers.add_parser("info", parents=[common], add_help=True)
    p_info.add_argument("asin")

    p_buy = subparsers.add_parser("buy", parents=[common], add_help=True)
    p_buy.add_argument("asin")
    p_buy.add_argument("--confirm", action="store_true")

    p_wish = subparsers.add_parser("wishlist", parents=[common], add_help=True)
    p_wish.add_argument("action", nargs="?", choices=["add"])
    p_wish.add_argument("asin", nargs="?")

    args = parser.parse_args()

    dispatch = {
        "status": cmd_status,
        "search": cmd_search,
        "library": cmd_library,
        "info": cmd_info,
        "buy": cmd_buy,
        "wishlist": cmd_wishlist,
    }

    if args.command in dispatch:
        dispatch[args.command](args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
