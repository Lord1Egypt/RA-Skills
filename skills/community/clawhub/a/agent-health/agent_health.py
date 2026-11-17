#!/usr/bin/env python3
"""
agent-health.py - probe an agent's dependency endpoints and report health.

Checks URLs/ports your agent depends on (gateways, APIs, databases) and prints a
table of up/down + latency. Zero deps (stdlib urllib). Honest: only probes, no fixes.

Usage:
  python agent-health.py check <endpoints.txt> [--json]
      endpoints.txt: one URL per line, optionally "name url"
  python agent-health.py self-test
"""
import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error

TIMEOUT = 8


def probe(url):
    t = time.time()
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as r:
            return {"url": url, "up": True, "status": r.status, "ms": int((time.time() - t) * 1000)}
    except urllib.error.HTTPError as e:
        return {"url": url, "up": True, "status": e.code, "ms": int((time.time() - t) * 1000)}
    except Exception as e:
        return {"url": url, "up": False, "status": 0, "ms": -1, "error": str(e)[:60]}


def check(path, as_json):
    rows = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        url = parts[-1]
        if not url.startswith("http"):
            continue
        rows.append(probe(url))
    up = sum(1 for r in rows if r["up"])
    res = {"checked": len(rows), "up": up, "down": len(rows) - up, "endpoints": rows}
    if as_json:
        print(json.dumps(res, indent=2))
    else:
        for r in rows:
            state = "UP " if r["up"] else "DOWN"
            ms = f"{r['ms']}ms" if r["ms"] >= 0 else "timeout"
            print(f"  [{state}] {r['status']:>4} {ms:>8}  {r['url']}")
        print(f"  {up}/{len(rows)} endpoints healthy")
    return res


def self_test():
    import tempfile
    f = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False)
    f.write("local http://127.0.0.1:1/should-fail\n")
    f.close()
    r = check(f.name, False)
    os.unlink(f.name)
    ok = r["checked"] == 1 and r["down"] == 1
    print("self-test:", "PASS" if ok else "FAIL", f"(down={r['down']})")
    return 0 if ok else 1


def main():
    p = argparse.ArgumentParser(description="agent-health")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check"); c.add_argument("path"); c.add_argument("--json", action="store_true")
    sub.add_parser("self-test")
    a = p.parse_args()
    if a.cmd == "self-test": return self_test()
    if a.cmd == "check": check(a.path, a.json); return 0


if __name__ == "__main__":
    sys.exit(main())
