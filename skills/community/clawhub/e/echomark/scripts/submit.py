#!/usr/bin/env python3
"""Submit a tool rating to EchoMark."""
import sys
import os

# Add current directory to path for config import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
from config import ECHO_MARK_API_URL, API_TIMEOUT, API_KEY_FILE
from local_db import save_rating


def load_api_key():
    """Load API Key from config file."""
    if not os.path.exists(API_KEY_FILE):
        raise FileNotFoundError(
            f"API Key not found at {API_KEY_FILE}. "
            "Run './register.py' or 'python register.py' first."
        )
    with open(API_KEY_FILE, "r") as f:
        return f.read().strip()


def submit_rating(tool_name, accuracy, efficiency, usability, stability, comment=""):
    """Submit a tool rating to cloud server."""
    api_key = load_api_key()
    url = f"{ECHO_MARK_API_URL}/api/v1/ratings"

    payload = {
        "tool_name": tool_name,
        "accuracy": accuracy,
        "efficiency": efficiency,
        "usability": usability,
        "stability": stability,
        "comment": comment,
    }

    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(url, json=payload, headers=headers, timeout=API_TIMEOUT)
    response.raise_for_status()

    return response.json()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Submit a tool rating to EchoMark")
    parser.add_argument("--tool", required=True, help="Tool name")
    parser.add_argument("--accuracy", type=int, required=True, choices=[1, 2, 3, 4, 5], help="Accuracy (1-5)")
    parser.add_argument("--efficiency", type=int, required=True, choices=[1, 2, 3, 4, 5], help="Efficiency (1-5)")
    parser.add_argument("--usability", type=int, required=True, choices=[1, 2, 3, 4, 5], help="Usability (1-5)")
    parser.add_argument("--stability", type=int, required=True, choices=[1, 2, 3, 4, 5], help="Stability (1-5)")
    parser.add_argument("--comment", default="", help="Comment (max 20 chars)")
    parser.add_argument("--local-only", action="store_true", help="Save locally only, skip cloud submission")

    args = parser.parse_args()

    overall = round(
        args.accuracy * 0.40 + args.stability * 0.30 +
        args.efficiency * 0.20 + args.usability * 0.10, 1
    )

    # Always save locally
    save_rating(
        tool_name=args.tool,
        accuracy=args.accuracy,
        efficiency=args.efficiency,
        usability=args.usability,
        stability=args.stability,
        overall=overall,
        comment=args.comment,
    )

    if args.local_only:
        print(f"Rating saved locally! Tool: {args.tool}, Overall: {overall}")
        return

    # Submit to cloud
    try:
        result = submit_rating(
            tool_name=args.tool,
            accuracy=args.accuracy,
            efficiency=args.efficiency,
            usability=args.usability,
            stability=args.stability,
            comment=args.comment,
        )
        print(f"Rating submitted! ID: {result['id']}")
    except FileNotFoundError as e:
        print(f"Saved locally but cloud submission skipped: {e}", file=sys.stderr)
    except requests.RequestException as e:
        print(f"Saved locally but cloud submission failed: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
