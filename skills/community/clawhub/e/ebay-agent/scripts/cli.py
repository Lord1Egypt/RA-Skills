#!/usr/bin/env python3
"""
ebay-agent CLI entry point.

Usage:
    uv run --project <skill_dir> ebay-agent search "Sony 85mm lens"
    uv run --project <skill_dir> ebay-agent value "iPhone 15 Pro"
    uv run --project <skill_dir> ebay-agent deal "Sony FE 85mm f/1.8"
    uv run --project <skill_dir> ebay-agent prefs
    uv run --project <skill_dir> ebay-agent watch add "Sony FE 85mm f/1.8" --max-price 300
    uv run --project <skill_dir> ebay-agent watch list
    uv run --project <skill_dir> ebay-agent watch remove <id>
    uv run --project <skill_dir> ebay-agent watch check
"""

import argparse
import json


def cmd_search(args):
    from .search import search_items
    from .preferences import load_preferences
    from .scoring import rank_results
    from .relevance import filter_relevant

    prefs = load_preferences()
    if args.max_price:
        prefs.budget_default = args.max_price

    try:
        # Fetch extra results to compensate for relevance filtering
        fetch_limit = min(args.limit * 2, 200)
        items = search_items(
            args.query,
            max_price=args.max_price,
            condition=args.condition,
            limit=fetch_limit,
        )
        if not items:
            print("No results found on eBay.")
            return
        items = filter_relevant(items, args.query)
        if not items:
            print("Results found but all filtered as accessories/irrelevant. Try a more specific query.")
            return
        ranked = rank_results(items, prefs)
        if not ranked:
            print(f"Found {len(items)} listings but all filtered out by preferences (min seller score: {prefs.min_seller_score}%, min condition: {prefs.min_condition}). Try: ebay-agent prefs")
            return

        # Apply sort override
        if args.sort == "price":
            ranked.sort(key=lambda x: x["total_price"])
        elif args.sort == "seller":
            ranked.sort(key=lambda x: float(x.get("seller_feedback_pct") or 0), reverse=True)

        if args.json:
            print(json.dumps(ranked[:args.limit], indent=2))
            return

        try:
            from rich.table import Table
            from rich.console import Console
            console = Console()
            table = Table(title=f"Search: {args.query}")
            table.add_column("#", style="dim", width=3)
            table.add_column("Title", max_width=38)
            table.add_column("Price", justify="right")
            table.add_column("Condition")
            table.add_column("Score", justify="right")
            table.add_column("Link", style="dim blue")
            for i, item in enumerate(ranked[:args.limit], 1):
                url = item.get("item_url", "")
                table.add_row(
                    str(i),
                    item.get("title", "")[:38],
                    f"${item.get('total_price', 0):.2f}",
                    item.get("condition", ""),
                    str(item.get("score", "")),
                    f"[link={url}]view[/link]" if url else "",
                )
            console.print(table)
        except ImportError:
            for i, item in enumerate(ranked[:args.limit], 1):
                url = item.get("item_url", "")
                print(f"{i}. {item.get('title', '')[:50]} | ${item.get('total_price', 0):.2f} | {url}")
    except Exception as e:
        print(f"Search failed: {e}")


def cmd_value(args):
    from .valuation import get_valuation

    from .valuation import CONDITION_ADJUSTMENTS

    try:
        result = get_valuation(args.query, condition=args.condition, limit=args.limit)
        if result["count"] == 0:
            print(f"No results found for '{args.query}'.")
            return
        if args.json:
            print(json.dumps(result, indent=2))
            return
        adj_pct = CONDITION_ADJUSTMENTS.get(args.condition.lower(), 0.8)
        print(f"Valuation for '{args.query}' (condition: {args.condition}):")
        print(f"  Fair range:        ${result['fair_low']:.2f} - ${result['fair_high']:.2f}")
        print(f"  Median:            ${result['median']:.2f}")
        print(f"  Confidence:        {result['confidence']}")
        print(f"  Full range:        ${result['min']:.2f} - ${result['max']:.2f}")
        print(f"  Listings analyzed: {result['count']} ({result['trimmed_count']} after trimming)")
        print(f"  Source:            {result['source']}")
        print(f"  Condition adj:     {args.condition} ({adj_pct:.0%} of avg = ${result['adjusted_avg']:.2f})")
        print(f"  Recommended price: ${result['recommended_price']:.2f}")
    except Exception as e:
        print(f"Valuation failed: {e}")


def cmd_deal(args):
    from .deal import evaluate_deal

    try:
        result = evaluate_deal(
            args.query,
            condition=args.condition,
            limit=args.limit,
            target_price=args.price,
        )
        if result["comps_used"] == 0 and result["confidence"] == "low":
            print(f"Not enough data to evaluate '{args.query}'.")
            if result["explanation"]:
                print(f"  {result['explanation']}")
            return
        if args.json:
            print(json.dumps(result, indent=2))
            return

        print(f"Deal evaluation: {args.query}")
        print(f"  Fair range:     ${result['fair_low']:.2f} - ${result['fair_high']:.2f}")
        print(f"  Median:         ${result['median']:.2f}")
        print(f"  Confidence:     {result['confidence']}")
        print(f"  Buy below:      ${result['buy_below']:.2f}")

        if args.price is not None:
            print(f"  Your price:     ${args.price:.2f}")
            print(f"  Rating:         {result['rating']}")

        print(f"  Why:            {result['explanation']}")
        print(f"  Source:         {result['source']}")

        if result.get("comp_listings"):
            print(f"  Top comps:")
            for i, comp in enumerate(result["comp_listings"], 1):
                print(f"    {i}. ${comp['price']:.2f} | {comp['condition']} | {comp['title']}")
    except Exception as e:
        print(f"Deal evaluation failed: {e}")


def cmd_prefs(args):
    from .preferences import load_preferences
    prefs = load_preferences()
    print("Current preferences:")
    for k, v in vars(prefs).items():
        print(f"  {k}: {v}")


def cmd_watch(args):
    from .watch import add_watch, list_watches, remove_watch, check_watches

    state_file = getattr(args, "state_file", None)

    if args.watch_command == "add":
        watch = add_watch(args.query, args.max_price, condition=args.condition, state_file=state_file)
        print(f"Added watch '{watch['id']}' for \"{watch['query']}\" (condition: {watch['condition']}, max: ${watch['max_price']:.2f})")

    elif args.watch_command == "list":
        watches = list_watches(state_file)
        if not watches:
            print("No active watches.")
            return
        try:
            from rich.table import Table
            from rich.console import Console
            console = Console()
            table = Table(title="Watches")
            table.add_column("ID", style="dim")
            table.add_column("Query")
            table.add_column("Condition")
            table.add_column("Max Price", justify="right")
            table.add_column("Last Checked", style="dim")
            table.add_column("Best Price", justify="right")
            for w in watches:
                checked = w.get("last_checked_at") or "never"
                best = f"${w['last_best_price']:.2f}" if w.get("last_best_price") is not None else "-"
                table.add_row(w["id"], w["query"], w.get("condition", ""), f"${w['max_price']:.2f}", checked, best)
            console.print(table)
        except ImportError:
            for w in watches:
                checked = w.get("last_checked_at") or "never"
                best = f"${w['last_best_price']:.2f}" if w.get("last_best_price") is not None else "-"
                print(f"  {w['id']} | {w['query']} | {w.get('condition', '')} | max ${w['max_price']:.2f} | checked {checked} | best {best}")

    elif args.watch_command == "remove":
        if remove_watch(args.id, state_file):
            print(f"Removed watch '{args.id}'.")
        else:
            print(f"Watch '{args.id}' not found.")

    elif args.watch_command == "check":
        triggered = check_watches(state_file)
        if not triggered:
            print("No matches found.")
            return
        print(f"{len(triggered)} watch(es) triggered:\n")
        for t in triggered:
            w = t["watch"]
            listing = t["listing"]
            print(f"  [{w['id']}] {w['query']}")
            print(f"    {listing['title']}")
            print(f"    ${listing['total_price']:.2f}  (max: ${w['max_price']:.2f})")
            if listing["url"]:
                print(f"    {listing['url']}")
            print()

    else:
        print("Usage: ebay-agent watch {add,list,remove,check}")


def main():
    parser = argparse.ArgumentParser(prog="ebay-agent", description="eBay search and valuation agent")
    subparsers = parser.add_subparsers(dest="command")

    p_search = subparsers.add_parser("search", help="Search eBay listings")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument("--max-price", "-p", type=float, default=None, help="Maximum price in USD")
    p_search.add_argument("--condition", "-c", default=None, help="Condition: new, used, very_good, good, acceptable")
    p_search.add_argument("--limit", "-n", type=int, default=10, help="Number of results (default: 10)")
    p_search.add_argument("--sort", "-s", choices=["score", "price", "seller"], default="score", help="Sort order (default: score)")
    p_search.add_argument("--json", action="store_true", help="Output results as JSON")

    p_value = subparsers.add_parser("value", help="Get market valuation")
    p_value.add_argument("query", help="Item to value")
    p_value.add_argument("--condition", "-c", default="used", help="Condition (default: used)")
    p_value.add_argument("--limit", "-n", type=int, default=20, help="Listings to analyze (default: 20)")
    p_value.add_argument("--json", action="store_true", help="Output results as JSON")

    p_deal = subparsers.add_parser("deal", help="Evaluate if an item is a good deal")
    p_deal.add_argument("query", help="Item to evaluate (search query)")
    p_deal.add_argument("--condition", "-c", default="used", help="Condition (default: used)")
    p_deal.add_argument("--price", "-p", type=float, default=None, help="Specific price to evaluate")
    p_deal.add_argument("--limit", "-n", type=int, default=25, help="Comps to analyze (default: 25)")
    p_deal.add_argument("--json", action="store_true", help="Output results as JSON")

    subparsers.add_parser("prefs", help="Show current preferences")

    p_watch = subparsers.add_parser("watch", help="Manage saved search watches")
    watch_sub = p_watch.add_subparsers(dest="watch_command")

    _sf_help = "Override state file path (default: ~/.ebay-agent/watches.json)"

    p_watch_add = watch_sub.add_parser("add", help="Add a new watch")
    p_watch_add.add_argument("query", help="Search query to watch")
    p_watch_add.add_argument("--max-price", "-p", type=float, required=True, help="Maximum price threshold (USD)")
    p_watch_add.add_argument("--condition", "-c", default="used", help="Condition filter (default: used)")
    p_watch_add.add_argument("--state-file", default=None, help=_sf_help)

    p_watch_list = watch_sub.add_parser("list", help="List active watches")
    p_watch_list.add_argument("--state-file", default=None, help=_sf_help)

    p_watch_rm = watch_sub.add_parser("remove", help="Remove a watch by ID")
    p_watch_rm.add_argument("id", help="Watch ID to remove")
    p_watch_rm.add_argument("--state-file", default=None, help=_sf_help)

    p_watch_check = watch_sub.add_parser("check", help="Check all watches against live eBay data")
    p_watch_check.add_argument("--state-file", default=None, help=_sf_help)

    args = parser.parse_args()

    if args.command == "search":
        cmd_search(args)
    elif args.command == "value":
        cmd_value(args)
    elif args.command == "deal":
        cmd_deal(args)
    elif args.command == "prefs":
        cmd_prefs(args)
    elif args.command == "watch":
        cmd_watch(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
