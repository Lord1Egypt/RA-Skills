"""
Thin public client for the private ClipX BNBChain API.

This file is safe to publish on ClawHub. It contains:
- No scraping logic
- No Playwright usage
- No DefiLlama / DappBay / Binance page structure knowledge

It only calls your hosted API and prints the JSON response.
"""

import argparse
import json
import os
import sys
import time
from typing import Any, Dict

import requests


def _clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def get_api_base() -> str:
    # Prefer env var so you can change base URL without republishing the skill.
    env_base = os.getenv("CLIPX_API_BASE")
    if env_base:
        return env_base.rstrip("/")
    # Fallback: hard-code your public API URL here
    return "https://skill.clipx.app"


def call_api(path: str, params: Dict[str, Any]) -> Dict[str, Any]:
    base = get_api_base()
    url = f"{base}{path}"
    try:
        resp = requests.get(url, params=params, timeout=180)
    except requests.RequestException as exc:  # noqa: BLE001
        return {"ok": False, "error": f"Network error: {exc}"}

    if resp.status_code != 200:
        return {"ok": False, "error": f"HTTP {resp.status_code}: {resp.text}"}

    try:
        data = resp.json()
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": f"Invalid JSON from API: {exc}"}

    return data


def parse_args(argv: Any = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="ClipX BNBChain API client (text-only JSON)."
    )
    p.add_argument(
        "--mode",
        required=True,
        choices=["metrics_basic", "metrics_block", "metrics_address", "clipx"],
        help="Which API group to call.",
    )
    p.add_argument("--blocks", type=int, help="Recent blocks for metrics_block.")
    p.add_argument("--address", type=str, help="Address for metrics_address.")
    p.add_argument(
        "--analysis-type",
        type=str,
        help="ClipX analysis_type (tvl_rank, fees_rank, revenue_rank, dapps_rank, fulleco, social_hype, meme_rank, market_insight, market_insight_live, binance_announcements, dex_volume).",
    )
    p.add_argument(
        "--interval",
        type=str,
        default="24h",
        help="Interval for some ClipX analyses (24h, 7d, 30d, 24, etc.).",
    )
    p.add_argument(
        "--timezone",
        type=str,
        default="UTC",
        help="Timezone name for timestamps (e.g. UTC, Europe/London).",
    )
    p.add_argument(
        "--formatted",
        action="store_true",
        default=True,
        help="For clipx mode: print server-formatted table (default). Same as VPS output.",
    )
    p.add_argument(
        "--no-formatted",
        dest="formatted",
        action="store_false",
        help="For clipx mode: print raw JSON instead of formatted table.",
    )
    p.add_argument(
        "--live",
        action="store_true",
        help="For clipx mode: keep refreshing in real time (Ctrl+C to stop).",
    )
    p.add_argument(
        "--refresh-interval",
        type=int,
        default=1,
        help="Seconds between refreshes when --live (default: 1 for full real time).",
    )
    return p.parse_args(argv)


def main(argv: Any = None) -> int:
    args = parse_args(argv)

    if args.mode == "metrics_basic":
        result = call_api("/api/bnb/metrics/basic", {})
    elif args.mode == "metrics_block":
        if not args.blocks or args.blocks <= 1:
            print(json.dumps({"ok": False, "error": "blocks>1 required"}))
            return 1
        result = call_api("/api/bnb/metrics/block-stats", {"blocks": args.blocks})
    elif args.mode == "metrics_address":
        if not args.address:
            print(json.dumps({"ok": False, "error": "address required"}))
            return 1
        result = call_api("/api/bnb/metrics/address", {"address": args.address})
    elif args.mode == "clipx":
        if not args.analysis_type:
            print(json.dumps({"ok": False, "error": "analysis-type required"}))
            return 1
        params = {"t": args.analysis_type, "interval": args.interval, "tz": args.timezone}
        if args.live:
            try:
                while True:
                    result = call_api("/api/clipx/analysis", params)
                    _clear_screen()
                    if result.get("ok") and result.get("formatted_table") and args.formatted:
                        print(result["formatted_table"], end="")
                    else:
                        print(json.dumps(result, separators=(",", ":")))
                    print(f"\nRefreshing in {args.refresh_interval}s... (Ctrl+C to stop)")
                    time.sleep(args.refresh_interval)
            except KeyboardInterrupt:
                print("\nStopped.")
                return 0
        result = call_api("/api/clipx/analysis", params)
        if result.get("ok") and result.get("formatted_table") and args.formatted:
            print(result["formatted_table"], end="")
            return 0
    else:
        print(json.dumps({"ok": False, "error": "unknown mode"}))
        return 1

    print(json.dumps(result, separators=(",", ":")))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())

