#!/usr/bin/env python3
"""Deep Research API health check and query tool."""

import sys
import json
import urllib.request
import urllib.error

API_BASE = "http://localhost:18888"

def health_check():
    """Check if the API is running."""
    try:
        req = urllib.request.Request(f"{API_BASE}/health", method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            print(f"✅ API healthy: {data.get('status', 'ok')}")
            return True
    except (urllib.error.URLError, ConnectionRefusedError, OSError):
        print("❌ API unavailable")
        return False

def query(question):
    """Send a research query."""
    payload = json.dumps({"question": question}).encode("utf-8")
    req = urllib.request.Request(
        f"{API_BASE}/api/analyze",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return data
    except (urllib.error.URLError, ConnectionRefusedError, OSError) as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python api_call.py <question>")
        print("       python api_call.py --health")
        sys.exit(1)

    if sys.argv[1] == "--health":
        ok = health_check()
        sys.exit(0 if ok else 1)

    question = " ".join(sys.argv[1:])
    print(f"Searching: {question}")
    result = query(question)

    if "error" in result:
        print(f"Error: {result['error']}")
        sys.exit(1)

    print(f"\nAnswer:\n{result.get('answer', 'No answer')}")
    if result.get("contradictions"):
        print(f"\nContradictions:\n{result['contradictions']}")
    print(f"\nSources: {len(result.get('sources', []))}")
