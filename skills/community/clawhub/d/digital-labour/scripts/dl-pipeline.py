#!/usr/bin/env python3
"""Digital Labour Pipeline Runner — execute multi-agent workflows.

Usage:
    python3 dl-pipeline.py lead_to_close --industry fintech --region "North America" --role CTO
    python3 dl-pipeline.py content_engine --topic "AI automation" --keyword "ai tools 2026"
    python3 dl-pipeline.py client_onboarding --doc-file client_docs.txt
    python3 dl-pipeline.py launch_blitz --idea "AI tutoring" --market "K-12"
    python3 dl-pipeline.py list
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE_URL = os.environ.get(
    "DIGITAL_LABOUR_API_URL",
    "https://bitrage-labour-api-production.up.railway.app",
).rstrip("/")

API_KEY = os.environ.get("DIGITAL_LABOUR_API_KEY", "")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKFLOWS_FILE = os.path.join(SCRIPT_DIR, "..", "workflows", "pipelines.json")


def _headers():
    h = {"Content-Type": "application/json", "Accept": "application/json"}
    if API_KEY:
        h["X-Api-Key"] = API_KEY
    return h


def _post(path, payload):
    url = f"{BASE_URL}{path}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=_headers(), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"  HTTP {e.code}: {body}", file=sys.stderr)
        return {"error": body, "status": "failed"}
    except urllib.error.URLError as e:
        print(f"  Connection error: {e.reason}", file=sys.stderr)
        return {"error": str(e.reason), "status": "failed"}


def load_pipelines():
    with open(WORKFLOWS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def substitute_vars(obj, variables):
    """Replace $VAR placeholders in inputs with actual values."""
    if isinstance(obj, str):
        for key, val in variables.items():
            obj = obj.replace(f"${key}", str(val))
        return obj
    if isinstance(obj, dict):
        return {k: substitute_vars(v, variables) for k, v in obj.items()}
    if isinstance(obj, list):
        return [substitute_vars(v, variables) for v in obj]
    return obj


def run_pipeline(pipeline_name, user_vars):
    pipelines = load_pipelines()
    pipeline = None
    for p in pipelines:
        if p["name"] == pipeline_name:
            pipeline = p
            break

    if not pipeline:
        print(f"Unknown pipeline: {pipeline_name}", file=sys.stderr)
        print(f"Available: {', '.join(p['name'] for p in pipelines)}", file=sys.stderr)
        sys.exit(1)

    print(f"\n{'='*60}", file=sys.stderr)
    print(f"  Pipeline: {pipeline['name']}", file=sys.stderr)
    print(f"  {pipeline['description']}", file=sys.stderr)
    print(f"  Steps: {len(pipeline['steps'])}", file=sys.stderr)
    print(f"{'='*60}\n", file=sys.stderr)

    results = []
    for i, step in enumerate(pipeline["steps"]):
        # Build variable context with prior step results
        vars_ctx = dict(user_vars)
        for j, prev in enumerate(results):
            vars_ctx[f"FROM_STEP_{j + 1}"] = json.dumps(prev.get("result", {}))

        agent = step["agent"]
        inputs = substitute_vars(step["inputs"], vars_ctx)

        print(f"  [{i + 1}/{len(pipeline['steps'])}] {agent}...", file=sys.stderr)
        start = time.time()
        result = _post("/v1/run", {"agent": agent, "inputs": inputs})
        elapsed = time.time() - start
        qa = result.get("qa_status", "N/A")
        status = result.get("status", "unknown")
        print(f"      Done in {elapsed:.1f}s — status: {status}, QA: {qa}", file=sys.stderr)
        results.append(result)

    print(f"\n{'='*60}", file=sys.stderr)
    print(f"  Pipeline complete: {len(results)} steps", file=sys.stderr)
    print(f"{'='*60}\n", file=sys.stderr)

    print(json.dumps(results, indent=2))


def parse_args(args):
    """Parse --key value pairs into a dict."""
    result = {}
    i = 0
    while i < len(args):
        if args[i].startswith("--"):
            key = args[i][2:].upper().replace("-", "_")
            if i + 1 < len(args) and not args[i + 1].startswith("--"):
                result[key] = args[i + 1]
                i += 2
            else:
                result[key] = "true"
                i += 1
        else:
            i += 1
    return result


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "list":
        pipelines = load_pipelines()
        for p in pipelines:
            print(f"  {p['name']:20s} — {p['description']}")
        return

    user_vars = parse_args(sys.argv[2:])
    run_pipeline(cmd, user_vars)


if __name__ == "__main__":
    main()
