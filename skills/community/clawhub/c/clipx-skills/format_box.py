"""
Read ClipX JSON from stdin and print box-style table to stdout.
Optional: pass --analysis-type (and --interval, --timezone) to fetch and format in one step.

Examples:
  # Fetch + format in one command
  python format_box.py --analysis-type tvl_rank
  python format_box.py --analysis-type meme_rank --interval 24 --timezone UTC
  python format_box.py --analysis-type fees_rank --interval 7d

  # Or pipe from api_client_cli
  python api_client_cli.py --mode clipx --analysis-type tvl_rank --timezone UTC | python format_box.py
"""
import argparse
import json
import os
import subprocess
import sys

ANALYSIS_TYPES = (
    "tvl_rank",
    "fees_rank",
    "revenue_rank",
    "dapps_rank",
    "fulleco",
    "social_hype",
    "meme_rank",
    "market_insight",
    "market_insight_live",
    "binance_announcements",
    "dex_volume",
)


def get_json_from_stdin() -> str:
    # Use utf-8-sig to strip BOM when piping on Windows
    return sys.stdin.buffer.read().decode("utf-8-sig").strip()


def get_json_from_api(analysis_type: str, interval: str, timezone: str) -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cli_path = os.path.join(script_dir, "api_client_cli.py")
    cmd = [
        sys.executable,
        cli_path,
        "--mode", "clipx",
        "--analysis-type", analysis_type,
        "--interval", interval,
        "--timezone", timezone,
        "--no-formatted",
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=script_dir,
        timeout=200,
    )
    if result.returncode != 0 and not result.stdout.strip():
        err = result.stderr.strip() or result.stdout.strip() or "Unknown error"
        raise SystemExit(f"API client failed: {err}")
    return result.stdout.strip()


def main():
    p = argparse.ArgumentParser(
        description="Format ClipX API JSON as a box-style table. Read from stdin or fetch by analysis type."
    )
    p.add_argument(
        "--analysis-type",
        type=str,
        choices=ANALYSIS_TYPES,
        help="Fetch this analysis from the API and format (skips stdin).",
    )
    p.add_argument(
        "--interval",
        type=str,
        default="24h",
        help="Interval for API (24h, 7d, 30d, 24, etc.). Default: 24h",
    )
    p.add_argument(
        "--timezone",
        type=str,
        default="UTC",
        help="Timezone for API. Default: UTC",
    )
    args = p.parse_args()

    if args.analysis_type:
        try:
            raw = get_json_from_api(args.analysis_type, args.interval, args.timezone)
        except subprocess.TimeoutExpired:
            print("Error: API request timed out", file=sys.stderr)
            sys.exit(1)
        except FileNotFoundError:
            print("Error: api_client_cli.py not found next to format_box.py", file=sys.stderr)
            sys.exit(1)
    else:
        raw = get_json_from_stdin()
        if not raw:
            print("No input. Pipe JSON from api_client_cli.py or use --analysis-type.", file=sys.stderr)
            sys.exit(1)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    if not data.get("ok"):
        print("Error:", data.get("error", "unknown"), file=sys.stderr)
        sys.exit(1)

    analysis_type = data.get("analysis_type", "")
    items = data.get("items", [])
    if not items:
        print(data.get("caption", ""))
        return

    # binance_announcements: plain markdown, 40 chars/line, 🔸 bullets, blank line after each
    if analysis_type == "binance_announcements" and items:
        def _wrap(prefix: str, text: str, w: int = 40) -> list:
            avail = w - len(prefix)
            words = text.split()
            out, cur, cur_len = [], [], 0
            for word in words:
                add = len(word) + (1 if cur else 0)
                if cur_len + add <= avail:
                    cur.append(word)
                    cur_len += add
                else:
                    if cur:
                        out.append(prefix + " ".join(cur))
                    cur, cur_len = [word], len(word)
                    prefix, avail = " " * len(prefix), w - len(prefix)
            if cur:
                out.append(prefix + " ".join(cur))
            return out
        print()
        print("**📢 Binance Announcements**")
        print()
        for it in items:
            name = (it.get("name") or "").strip()
            if name:
                for line in _wrap("🔸 ", name, 40):
                    print(line)
                print()
        print()
        return

    # market_insight_live: 3 sections (Volume Leaders, Gainers, Losers)
    if analysis_type == "market_insight_live" and items:
        vol_items = [it for it in items if it.get("section") == "volume"]
        gain_items = [it for it in items if it.get("section") == "gainer"]
        lose_items = [it for it in items if it.get("section") == "loser"]
        sep = "=" * 72
        sep_s = "-" * 72
        print()
        print(sep)
        print("🟢 LIVE BINANCE DATA")
        print(sep)
        if vol_items:
            print("\n💰 24H VOLUME LEADERS:")
            print(sep_s)
            print(f"{'#':<3} | {'NAME':<10} | {'PRICE':<14} | {'24H VOLUME':<14}")
            print(sep_s)
            for it in vol_items:
                print(f"{it.get('rank',''):<3} | {(it.get('name') or '')[:8]:<10} | {it.get('price',''):<14} | {it.get('metric_value',''):<14}")
        if gain_items:
            print("\n📈 TOP GAINERS (24H):")
            print(sep_s)
            print(f"{'#':<3} | {'NAME':<10} | {'PRICE':<14} | {'24H CHANGE':<12}")
            print(sep_s)
            for it in gain_items:
                print(f"{it.get('rank',''):<3} | {(it.get('name') or '')[:8]:<10} | {it.get('price',''):<14} | {it.get('metric_value',''):<12}")
        if lose_items:
            print("\n📉 TOP LOSERS (24H):")
            print(sep_s)
            print(f"{'#':<3} | {'NAME':<10} | {'PRICE':<14} | {'24H CHANGE':<12}")
            print(sep_s)
            for it in lose_items:
                print(f"{it.get('rank',''):<3} | {(it.get('name') or '')[:8]:<10} | {it.get('price',''):<14} | {it.get('metric_value',''):<12}")
        print("\n" + sep)
        if data.get("source"):
            print(f"Source: {data['source']}")
        print()
        return

    # fulleco: Name | Category | Users (no rank column)
    if analysis_type == "fulleco" and items:
        w2, w3 = 12, 8
        sep_double = "=" * 40
        sep_single = "-" * 40
        print()
        print(sep_double)
        print("🚀 FULL ECOSYSTEM LEADERS")
        print(sep_double)
        print(sep_single)
        print(f"{'NAME':<{w2}} | {'CATEGORY':<{w3}} | {'USERS'}")
        print(sep_single)
        for it in items:
            name = (it.get("name") or "")[:w2]
            cat = (it.get("category") or "—")[:w3]
            users = it.get("metric_value", "")
            print(f"{name:<{w2}} | {cat:<{w3}} | {users}")
        print(sep_double)
        if data.get("source"):
            print(f"Source: {data['source']}")
        print()
        return

    # meme_rank: match VPS "FETCHED MEME TOKENS (FOR VERIFICATION)" (RANK|NAME|SCORE|MCAP|B.HOLDERS)
    if analysis_type == "meme_rank" and items and (items[0].get("mcap") is not None or items[0].get("bHolders") is not None):
        sep = "=" * 62
        sep_s = "-" * 62
        print()
        print(sep)
        print("🚀 FETCHED MEME TOKENS (FOR VERIFICATION)")
        print(sep)
        print(f"{'RANK':<5} | {'NAME':<20} | {'SCORE':<8} | {'MCAP':<12} | {'B.HOLDERS':<10}")
        print(sep_s)
        for it in items:
            rank = f"#{it.get('rank', '')}"
            name = (it.get("name") or "")[:18]
            score = str(it.get("metric_value", it.get("score", "")))
            mcap = str(it.get("mcap", ""))
            holders = str(it.get("bHolders", ""))
            print(f"{rank:<5} | {name:<20} | {score:<8} | {mcap:<12} | {holders:<10}")
        print(sep)
        if data.get("source"):
            print(f"Source: {data['source']}")
        print()
        return

    # Standard 4-column format for other analysis types
    titles = {
        "tvl_rank": ("TOP 10 TVL PROTOCOLS ON BSC", "#", "NAME", "CATEGORY", "TVL"),
        "fees_rank": ("TOP 10 FEES PAID PROTOCOLS ON BSC", "#", "NAME", "CATEGORY", "FEES"),
        "revenue_rank": ("TOP 10 REVENUE PROTOCOLS ON BSC", "#", "NAME", "CATEGORY", "REVENUE"),
        "dapps_rank": ("TOP 10 DAPPS BY USERS (7D)", "#", "NAME", "CATEGORY", "USERS"),
        "fulleco": ("FULL ECOSYSTEM LEADERS", "#", "NAME", "CATEGORY", "METRIC"),
        "social_hype": ("TOP 10 SOCIAL HYPE TOKENS", "#", "NAME", "SENTIMENT", "HYPE SCORE"),
        "meme_rank": ("TOP 10 MEME TOKENS BY SCORE", "#", "NAME", "—", "SCORE"),
        "market_insight": ("BINANCE 24H VOLUME LEADERS", "#", "NAME", "CATEGORY", "24H VOLUME"),
        "market_insight_live": ("LIVE BINANCE DATA", "#", "NAME", "CATEGORY", "VALUE"),
        "dex_volume": ("TOP 10 DEX VOLUME ON BNB CHAIN", "#", "NAME", "CATEGORY", "VOLUME"),
    }
    title_line, col1, col2, col3, col4 = titles.get(
        analysis_type, ("RANKING", "#", "NAME", "CATEGORY", "VALUE")
    )
    meta = data.get("meta") or {}
    interval = (meta.get("interval") or data.get("interval") or "").strip().upper()
    if interval and analysis_type in ("fees_rank", "revenue_rank", "dex_volume"):
        title_line = f"{title_line} ({interval})"

    # Mobile-friendly width (~40 chars) so table doesn't wrap on small screens
    w2, w3 = 12, 8
    sep_double = "=" * 40
    sep_single = "-" * 40

    print()
    print(sep_double)
    print(f"🚀 {title_line}")
    print(sep_double)
    print(sep_single)
    print(f"{col1:<3} | {col2:<{w2}} | {col3:<{w3}} | {col4}")
    print(sep_single)
    for it in items:
        rank = it.get("rank", "")
        name = (it.get("name") or "")[:w2]
        cat = (it.get("category") or "—")[:w3]
        val = it.get("metric_value", "")
        print(f"{rank:<3} | {name:<{w2}} | {cat:<{w3}} | {val}")
    print(sep_double)
    if data.get("source"):
        print(f"Source: {data['source']}")
    print()

if __name__ == "__main__":
    main()
