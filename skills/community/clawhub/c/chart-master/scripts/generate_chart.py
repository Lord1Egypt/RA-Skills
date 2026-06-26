#!/usr/bin/env python3

import argparse
import yfinance as yf
import mplfinance as mpf
import pandas as pd
from datetime import datetime
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="Generate a financial chart.")
    parser.add_argument("--ticker", required=True, help="Stock ticker symbol (e.g., AAPL, ^NDX)")
    parser.add_argument("--period", default="1mo", help="Data period (e.g., 1d, 5d, 1mo, 3mo, 6mo, 1y, ytd, max)")
    parser.add_argument("--interval", default="1d", help="Bar interval (e.g., 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)")
    parser.add_argument("--type", default="candle", help="Chart type (candle, line, renko, pnf)")
    parser.add_argument("--style", default="yahoo", help="Chart style (binance, blueskies, charles, checkers, classic, default, mike, nightclouds, sas, starsandstripes, yahoo)")
    parser.add_argument("--mav", help="Moving averages (comma-separated, e.g., 20,50,200)")
    parser.add_argument("--volume", action="store_true", default=True, help="Show volume pane")
    parser.add_argument("--title", help="Chart title")
    parser.add_argument("--output-dir", default=".", help="Directory to save the chart")
    
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # Fetch data
    try:
        data = yf.Ticker(args.ticker).history(period=args.period, interval=args.interval)
        
        if data.empty:
            print(f"Error: No data found for ticker '{args.ticker}' with period '{args.period}' and interval '{args.interval}'.")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)

    # Moving averages
    mav = ()
    if args.mav:
        try:
            mav = tuple(map(int, args.mav.split(",")))
        except ValueError:
            print("Warning: Invalid moving average format. Using default (none).")

    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_ticker = args.ticker.replace("^", "").replace("=", "").replace("-", "_")
    filename = f"chart_{clean_ticker}_{timestamp}.png"
    filepath = os.path.join(args.output_dir, filename)

    # Plot
    kwargs = dict(
        type=args.type,
        style=args.style,
        mav=mav,
        volume=args.volume,
        title=args.title if args.title else f"{args.ticker} ({args.period})",
        savefig=filepath
    )
    
    try:
        mpf.plot(data, **kwargs)
        print(f"Chart generated successfully: {filepath}")
        # Signal specifically for OpenClaw to attach the media
        print(f"MEDIA: {os.path.abspath(filepath)}") 
    except Exception as e:
        print(f"Error generating chart: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
