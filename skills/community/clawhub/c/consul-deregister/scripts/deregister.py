#!/usr/bin/env python3
"""
Consul Service Deregister Tool
Usage:
  # Deregister by service ID on specific agents
  python3 deregister.py --service-id <id> --agents 10.90.81.37:8500 10.90.81.32:8500

  # Deregister from a single agent
  python3 deregister.py --service-id <id> --agents 10.90.81.37:8500

  # Batch deregister from a file (one agent per line)
  python3 deregister.py --service-id <id> --agents-file agents.txt

  # Parse and replay raw curl commands
  python3 deregister.py --from-curl "curl -XPUT http://10.90.81.37:8500/v1/agent/service/deregister/my-svc"

  # Dry run (preview only, no actual requests)
  python3 deregister.py --service-id <id> --agents 10.90.81.37:8500 --dry-run
"""

import argparse
import sys
import re
import urllib.request
import urllib.error
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

CONSUL_DEREGISTER_PATH = "/v1/agent/service/deregister/"


def build_url(agent: str, service_id: str) -> str:
    if not agent.startswith("http"):
        agent = "http://" + agent
    return agent.rstrip("/") + CONSUL_DEREGISTER_PATH + service_id


def deregister(agent: str, service_id: str, token: str = None, dry_run: bool = False) -> dict:
    url = build_url(agent, service_id)
    if dry_run:
        return {"agent": agent, "service_id": service_id, "url": url, "status": "DRY_RUN", "ok": True}
    try:
        req = urllib.request.Request(url, method="PUT")
        if token:
            req.add_header("X-Consul-Token", token)
        with urllib.request.urlopen(req, timeout=10) as resp:
            status = resp.status
            ok = status == 200
            return {"agent": agent, "service_id": service_id, "url": url, "status": status, "ok": ok}
    except urllib.error.HTTPError as e:
        return {"agent": agent, "service_id": service_id, "url": url, "status": e.code, "ok": False, "error": str(e)}
    except Exception as e:
        return {"agent": agent, "service_id": service_id, "url": url, "status": "ERROR", "ok": False, "error": str(e)}


def parse_curl_commands(raw: str) -> list[dict]:
    """Parse one or more curl -XPUT deregister commands and return list of {agent, service_id}."""
    pattern = re.compile(
        r"curl\s+(?:-X\s*PUT|-XPUT)\s+(https?://[^\s/]+)/v1/agent/service/deregister/([^\s]+)",
        re.IGNORECASE,
    )
    results = []
    for m in pattern.finditer(raw):
        results.append({"agent": m.group(1), "service_id": m.group(2)})
    return results


def print_result(r: dict):
    icon = "✅" if r["ok"] else "❌"
    status = r["status"]
    if r.get("error"):
        print(f"  {icon} [{status}] {r['url']}  — {r['error']}")
    else:
        print(f"  {icon} [{status}] {r['url']}")


def main():
    parser = argparse.ArgumentParser(description="Consul service deregister tool")
    parser.add_argument("--service-id", help="Service instance ID to deregister")
    parser.add_argument("--agents", nargs="+", help="Consul agent addresses (host:port)")
    parser.add_argument("--agents-file", help="File with one agent address per line")
    parser.add_argument("--from-curl", help="Raw curl command(s) to parse and replay")
    parser.add_argument("--token", help="Consul ACL token (X-Consul-Token header)")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no actual requests")
    parser.add_argument("--parallel", action="store_true", default=True, help="Run requests in parallel (default: true)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    tasks = []  # list of (agent, service_id)

    if args.from_curl:
        parsed = parse_curl_commands(args.from_curl)
        if not parsed:
            print("❌ No valid consul deregister curl commands found in input.", file=sys.stderr)
            sys.exit(1)
        tasks = [(p["agent"], p["service_id"]) for p in parsed]
    else:
        if not args.service_id:
            parser.error("--service-id is required unless using --from-curl")
        agents = list(args.agents or [])
        if args.agents_file:
            with open(args.agents_file) as f:
                agents += [line.strip() for line in f if line.strip() and not line.startswith("#")]
        if not agents:
            parser.error("Provide at least one agent via --agents or --agents-file")
        tasks = [(a, args.service_id) for a in agents]

    if args.dry_run:
        print(f"🔍 DRY RUN — {len(tasks)} deregister request(s) would be sent:\n")
    else:
        print(f"🚀 Deregistering service on {len(tasks)} agent(s)...\n")

    results = []
    if args.parallel and len(tasks) > 1:
        with ThreadPoolExecutor(max_workers=min(len(tasks), 10)) as ex:
            futures = {ex.submit(deregister, a, sid, args.token, args.dry_run): (a, sid) for a, sid in tasks}
            for fut in as_completed(futures):
                results.append(fut.result())
    else:
        for a, sid in tasks:
            results.append(deregister(a, sid, args.token, args.dry_run))

    # Sort by agent for stable output
    results.sort(key=lambda r: r["agent"])

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print_result(r)

    ok_count = sum(1 for r in results if r["ok"])
    fail_count = len(results) - ok_count
    print(f"\n{'─'*50}")
    print(f"  Total: {len(results)}  ✅ OK: {ok_count}  ❌ Failed: {fail_count}")

    if fail_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
