#!/usr/bin/env python3
import json, sys, urllib.request, urllib.error, os

LANGGRAPH_URL = os.environ.get("DEERFLOW_LANGGRAPH", "http://localhost:2024")


def check_status(thread_id, run_id=None):
    url = f"{LANGGRAPH_URL}/threads/{thread_id}"
    if run_id:
        url += f"/runs/{run_id}"
    else:
        url += "/runs"

    req = urllib.request.Request(url, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 check_status.py <thread_id> [run_id]")
        sys.exit(1)

    thread_id = sys.argv[1]
    run_id = sys.argv[2] if len(sys.argv) > 2 else None

    result = check_status(thread_id, run_id)
    if result:
        print(json.dumps(result, indent=2))
