#!/usr/bin/env python3
"""
AI Hedge Fund - Run multi-agent stock analysis
Auto-detects model from current OpenClaw session, NOT hardcoded.
"""
import os
import sys
import json
import subprocess

def get_current_model():
    """Get primary model from current OpenClaw session only."""
    cfg_path = "/root/.openclaw/openclaw.json"
    if os.path.exists(cfg_path):
        try:
            cfg = json.load(open(cfg_path))
            # Get primary model from main agent
            agents = cfg.get("agents", {})
            primary = agents.get("main", {}).get("model", {}).get("primary")
            if primary:
                return primary
            # Fallback to default primary
            default = agents.get("defaults", {}).get("model", {}).get("primary")
            if default:
                return default
        except Exception as e:
            print(f"Config error: {e}")
    
    print("Error: No model detected from OpenClaw session.")
    print("Specify --model manually: python3 run.py --tickers NVDA --model 'minimax/minimax-m2.5:free'")
    sys.exit(1)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="AI Hedge Fund")
    parser.add_argument("--tickers", required=True, help="Comma-separated tickers")
    parser.add_argument("--start-date", default="2026-01-01")
    parser.add_argument("--end-date", default="2026-04-12")
    parser.add_argument("--model", help="Model (auto-detected from session if not specified)")
    parser.add_argument("--analysts", help="Comma-separated analysts")
    parser.add_argument("--analysts-all", action="store_true")
    parser.add_argument("--show-reasoning", action="store_true")
    parser.add_argument("--initial-cash", default="100000")
    
    args = parser.parse_args()
    
    if not args.model:
        args.model = get_current_model()
        print(f"Session model: {args.model}")
    
    # Build command
    cmd = [
        "python3", "/data/workspace/ai-hedge-fund/src/main.py",
        "--tickers", args.tickers,
        "--start-date", args.start_date,
        "--end-date", args.end_date,
        "--model", args.model,
    ]
    
    if args.analysts_all:
        cmd.append("--analysts-all")
    elif args.analysts:
        cmd.extend(["--analysts", args.analysts])
    
    if args.show_reasoning:
        cmd.append("--show-reasoning")
    
    cmd.extend(["--initial-cash", args.initial_cash])
    
    result = subprocess.run(cmd)
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()