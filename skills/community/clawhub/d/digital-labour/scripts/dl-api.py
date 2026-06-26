#!/usr/bin/env python3
"""Digital Labour API client — stdlib only, zero pip installs.

Usage:
    python3 dl-api.py health
    python3 dl-api.py agents
    python3 dl-api.py run <agent> '<json_inputs>'
    python3 dl-api.py batch <file.json>
"""

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

BASE_URL = os.environ.get(
    "DIGITAL_LABOUR_API_URL",
    "https://bitrage-labour-api-production.up.railway.app",
).rstrip("/")

API_KEY = os.environ.get("DIGITAL_LABOUR_API_KEY", "")

VALID_AGENTS = [
    "sales_outreach", "support_ticket", "content_repurpose", "doc_extract",
    "lead_gen", "email_marketing", "seo_content", "social_media",
    "data_entry", "web_scraper", "crm_ops", "bookkeeping",
    "proposal_writer", "product_desc", "resume_writer", "ad_copy",
    "market_research", "business_plan", "press_release", "tech_docs",
    "context_manager", "qa_manager", "production_manager", "automation_manager",
]

# ── Helpers ─────────────────────────────────────────────────────


def _headers():
    h = {"Content-Type": "application/json", "Accept": "application/json"}
    if API_KEY:
        h["X-Api-Key"] = API_KEY
    return h


def _get(path):
    """GET request, returns parsed JSON."""
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, headers=_headers(), method="GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def _post(path, payload):
    """POST request with JSON body, returns parsed JSON."""
    url = f"{BASE_URL}{path}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=_headers(), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def _validate_agent(name):
    """Validate agent name against allowlist."""
    if name not in VALID_AGENTS:
        print(f"Unknown agent: {name}", file=sys.stderr)
        print(f"Valid agents: {', '.join(VALID_AGENTS)}", file=sys.stderr)
        sys.exit(1)


# ── Commands ────────────────────────────────────────────────────


def cmd_health():
    """Check API health."""
    result = _get("/health")
    print(json.dumps(result, indent=2))


def cmd_agents():
    """List all agents with input schemas."""
    result = _get("/agents")
    print(json.dumps(result, indent=2))


def cmd_run(agent, inputs_json):
    """Run a single agent."""
    _validate_agent(agent)
    try:
        inputs = json.loads(inputs_json)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON inputs: {e}", file=sys.stderr)
        sys.exit(1)

    payload = {"agent": agent, "inputs": inputs}
    print(f"Running {agent}...", file=sys.stderr)
    start = time.time()
    result = _post("/v1/run", payload)
    elapsed = time.time() - start
    print(f"Completed in {elapsed:.1f}s", file=sys.stderr)
    print(json.dumps(result, indent=2))


def cmd_batch(filepath):
    """Run multiple agents from a JSON file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            tasks = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error reading batch file: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(tasks, list):
        print("Batch file must contain a JSON array of tasks", file=sys.stderr)
        sys.exit(1)

    results = []
    for i, task in enumerate(tasks):
        agent = task.get("agent", "")
        inputs = task.get("inputs", {})
        _validate_agent(agent)
        print(f"[{i + 1}/{len(tasks)}] Running {agent}...", file=sys.stderr)
        start = time.time()
        result = _post("/v1/run", {"agent": agent, "inputs": inputs})
        elapsed = time.time() - start
        print(f"  Done in {elapsed:.1f}s — QA: {result.get('qa_status', 'N/A')}", file=sys.stderr)
        results.append(result)

    print(json.dumps(results, indent=2))


# ── Main ────────────────────────────────────────────────────────


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "health":
        cmd_health()
    elif cmd == "agents":
        cmd_agents()
    elif cmd == "run":
        if len(sys.argv) < 4:
            print("Usage: dl-api.py run <agent> '<json_inputs>'", file=sys.stderr)
            sys.exit(1)
        cmd_run(sys.argv[2], sys.argv[3])
    elif cmd == "batch":
        if len(sys.argv) < 3:
            print("Usage: dl-api.py batch <file.json>", file=sys.stderr)
            sys.exit(1)
        cmd_batch(sys.argv[2])
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        print("Commands: health, agents, run, batch", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
