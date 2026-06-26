#!/usr/bin/env python3
"""Query tool ratings from EchoMark."""
import sys
import os

# Add current directory to path for config import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
from config import ECHO_MARK_API_URL, API_TIMEOUT, API_KEY_FILE
from local_db import query_ratings as local_query_ratings, list_tools as local_list_tools


def load_api_key():
    """Load API Key from config file."""
    if not os.path.exists(API_KEY_FILE):
        raise FileNotFoundError(
            f"API Key not found at {API_KEY_FILE}. "
            "Run './register.py' or 'python register.py' first."
        )
    with open(API_KEY_FILE, "r") as f:
        return f.read().strip()


def query_cloud_rating(tool_name):
    """Query ratings for a specific tool from cloud server."""
    api_key = load_api_key()
    url = f"{ECHO_MARK_API_URL}/api/v1/ratings/{tool_name}"

    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers, timeout=API_TIMEOUT)
    response.raise_for_status()

    return response.json()


def print_local_result(result):
    """Print local rating result."""
    print(f"\n=== {result['tool_name']} Ratings (local) ===")
    print(f"Total Ratings: {result['total_ratings']}")
    print(f"Average Overall: {result['avg_overall']}")
    print(f"  Accuracy:   {result['avg_accuracy']}")
    print(f"  Efficiency: {result['avg_efficiency']}")
    print(f"  Usability:  {result['avg_usability']}")
    print(f"  Stability:  {result['avg_stability']}")
    print(f"Last Updated: {result['last_updated']}")


def print_cloud_result(result):
    """Print cloud rating result."""
    stats = result["stats"]
    print(f"\n=== {result['tool_name']} Ratings (cloud) ===")
    print(f"Total Ratings: {stats['total_ratings']}")
    print(f"Average Overall: {stats['avg_overall']}")
    print(f"  Accuracy:   {stats['avg_accuracy']}")
    print(f"  Efficiency: {stats['avg_efficiency']}")
    print(f"  Usability:  {stats['avg_usability']}")
    print(f"  Stability:  {stats['avg_stability']}")
    print(f"Last Updated: {stats['last_updated']}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Query tool ratings from EchoMark")
    parser.add_argument("--tool", required=True, help="Tool name to query")
    parser.add_argument("--cloud", action="store_true", help="Query cloud server instead of local DB")

    args = parser.parse_args()

    try:
        if args.cloud:
            result = query_cloud_rating(args.tool)
            print_cloud_result(result)
        else:
            result = local_query_ratings(args.tool)
            if result is None:
                print(f"No local ratings found for tool: {args.tool}")
                print("Use --cloud to query the community ratings from the server.")
            else:
                print_local_result(result)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except requests.RequestException as e:
        print(f"Failed to query rating: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
