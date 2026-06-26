#!/usr/bin/env python3
"""
Download historical candle data from data.binance.vision.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Data source: https://data.binance.vision/data/futures/um/daily/klines/
- Free, no API key needed
- Daily ZIP files containing 1-minute CSV candle data
- USDT-M Futures (most liquid markets)

Usage:
    python download_data.py --ticker BTC --interval 1m --days 180
    python download_data.py --ticker BTC ETH SOL --interval 1m --days 180
"""

import argparse
import csv
import io
import sys
import time
import zipfile
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.request import Request, urlopen, ProxyHandler, build_opener, install_opener
from urllib.error import HTTPError, URLError

# Bypass system proxy (macOS Shimo VPN etc.) — connect directly to Binance
install_opener(build_opener(ProxyHandler({})))

# https://data.binance.vision/data/futures/um/daily/klines/{PAIR}/{interval}/{PAIR}-{interval}-{date}.zip
BASE_URL = "https://data.binance.vision/data/futures/um/daily/klines"
DATA_DIR = Path(__file__).parent.parent / "data" / "candles"


def download_day(symbol: str, interval: str, date_str: str) -> list:
    """Download one day's kline ZIP from data.binance.vision."""
    pair = f"{symbol}USDT"
    url = f"{BASE_URL}/{pair}/{interval}/{pair}-{interval}-{date_str}.zip"
    req = Request(url, headers={"User-Agent": "ClawSwap/1.0"})

    for attempt in range(3):
        try:
            with urlopen(req, timeout=30) as resp:
                zip_bytes = resp.read()
            break
        except HTTPError as e:
            if e.code == 404:
                return []  # No data for this day (not yet published)
            if attempt < 2:
                time.sleep(1)
                continue
            return []
        except (URLError, Exception) as e:
            if attempt < 2:
                time.sleep(1)
                continue
            print(f"  [!] {date_str}: {e}", file=sys.stderr)
            return []

    candles = []
    try:
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
            for name in zf.namelist():
                if name.endswith(".csv"):
                    with zf.open(name) as f:
                        reader = csv.reader(io.TextIOWrapper(f))
                        for row in reader:
                            if len(row) < 6:
                                continue
                            try:
                                candles.append([
                                    int(row[0]),    # open_time ms
                                    float(row[1]),  # open
                                    float(row[2]),  # high
                                    float(row[3]),  # low
                                    float(row[4]),  # close
                                    float(row[5]),  # volume
                                ])
                            except (ValueError, IndexError):
                                continue
    except zipfile.BadZipFile:
        return []

    return candles


def download_ticker(ticker: str, interval: str, days: int):
    """Download candle data for a single ticker."""
    symbol = ticker.upper()
    today = datetime.now(timezone.utc).date()
    start_date = today - timedelta(days=days)

    all_candles = []
    total_days = (today - start_date).days
    good = 0
    skipped = 0

    print(f"  [{symbol}] Downloading {days}d of {interval} from data.binance.vision...")

    current = start_date
    while current < today:  # today's data isn't published yet
        date_str = current.strftime("%Y-%m-%d")
        day_num = (current - start_date).days + 1

        candles = download_day(symbol, interval, date_str)

        if candles:
            all_candles.extend(candles)
            good += 1
            sys.stdout.write(f"\r  [{symbol}] {date_str} | {len(all_candles):,} candles | {day_num}/{total_days} days")
            sys.stdout.flush()
        else:
            skipped += 1

        current += timedelta(days=1)

    print()  # newline after progress

    if not all_candles:
        print(f"  [{symbol}] No data downloaded!")
        return

    # Dedup + sort
    seen = set()
    deduped = []
    for c in all_candles:
        if c[0] not in seen:
            seen.add(c[0])
            deduped.append(c)
    deduped.sort(key=lambda x: x[0])

    # Save
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{symbol}-{interval}-{days}d.csv"
    filepath = DATA_DIR / filename

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "open", "high", "low", "close", "volume"])
        writer.writerows(deduped)

    size_mb = filepath.stat().st_size / (1024 * 1024)
    start_dt = datetime.fromtimestamp(deduped[0][0] / 1000, tz=timezone.utc)
    end_dt = datetime.fromtimestamp(deduped[-1][0] / 1000, tz=timezone.utc)
    print(f"  [{symbol}] ✓ {len(deduped):,} candles → {filepath.name} ({size_mb:.1f} MB)")
    print(f"  [{symbol}]   {start_dt:%Y-%m-%d} → {end_dt:%Y-%m-%d} | {good} days downloaded, {skipped} skipped")


def main():
    parser = argparse.ArgumentParser(description="Download candle data from data.binance.vision")
    parser.add_argument("--ticker", nargs="+", default=["BTC", "ETH", "SOL"],
                        help="Tickers to download (default: BTC ETH SOL)")
    parser.add_argument("--interval", default="1m",
                        help="Interval: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d")
    parser.add_argument("--days", type=int, default=180,
                        help="Days of history (default: 180)")
    args = parser.parse_args()

    print(f"━━━ ClawSwap Data Downloader ━━━")
    print(f"Source:   data.binance.vision (USDT-M Futures daily ZIPs)")
    print(f"Tickers:  {', '.join(args.ticker)}")
    print(f"Interval: {args.interval} | Days: {args.days}")
    print()

    for ticker in args.ticker:
        download_ticker(ticker, args.interval, args.days)
        print()

    print("Done!")


if __name__ == "__main__":
    main()
