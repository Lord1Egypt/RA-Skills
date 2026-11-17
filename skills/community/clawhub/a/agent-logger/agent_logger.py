#!/usr/bin/env python3
"""
agent-logger.py - analyze agent run logs for errors, token spikes, and failures.

Point it at a log file (or directory of logs) and get a structured report: error
lines, warning counts, suspected token spikes, and a health verdict. Stdlib only.

Usage:
  python agent-logger.py scan <logfile|dir> [--json]
  python agent-logger.py self-test
"""
import argparse
import json
import os
import re
import sys

ERR = re.compile(r'\b(error|exception|traceback|failed|fatal)\b', re.I)
WARN = re.compile(r'\b(warn|deprecat|retry|timeout)\b', re.I)
TOKEN = re.compile(r'tokens?[:=]\s*(\d+)', re.I)


def scan(path, as_json):
    files = []
    if os.path.isdir(path):
        for root, _, fs in os.walk(path):
            for fn in fs:
                if fn.endswith((".log", ".txt", ".json")):
                    files.append(os.path.join(root, fn))
    else:
        files.append(path)
    errors, warns, token_vals = [], [], []
    for fp in files:
        for i, line in enumerate(open(fp, encoding="utf-8", errors="ignore"), 1):
            if ERR.search(line):
                errors.append(f"{os.path.basename(fp)}:{i}: {line.strip()[:120]}")
            if WARN.search(line):
                warns.append(f"{os.path.basename(fp)}:{i}")
            for m in TOKEN.finditer(line):
                token_vals.append(int(m.group(1)))
    # token spike = any single value > 3x the median
    spike = False
    if len(token_vals) > 3:
        med = sorted(token_vals)[len(token_vals) // 2]
        spike = any(v > 3 * med for v in token_vals)
    health = "UNHEALTHY" if errors else ("DEGRADED" if warns else "HEALTHY")
    res = {"files": len(files), "errors": len(errors), "warns": len(warns),
           "token_spike": spike, "health": health,
           "error_samples": errors[:5]}
    if as_json:
        print(json.dumps(res, indent=2))
    else:
        print(f"files={res['files']} errors={res['errors']} warns={res['warns']} "
              f"token_spike={res['token_spike']} -> {res['health']}")
        for e in res["error_samples"]:
            print("  !", e)
    return res


def self_test():
    import tempfile
    good = tempfile.NamedTemporaryFile("w", suffix=".log", delete=False)
    good.write("info: started\ninfo: done\n")
    good.close()
    bad = tempfile.NamedTemporaryFile("w", suffix=".log", delete=False)
    bad.write("info: started\nERROR: traceback exception failed\nwarn: timeout retrying\n")
    bad.close()
    g = scan(good.name, False); b = scan(bad.name, False)
    os.unlink(good.name); os.unlink(bad.name)
    ok = g["health"] == "HEALTHY" and b["health"] == "UNHEALTHY" and b["errors"] == 1
    print("self-test:", "PASS" if ok else "FAIL", f"(good={g['health']} bad={b['health']})")
    return 0 if ok else 1


def main():
    p = argparse.ArgumentParser(description="agent-logger")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan"); s.add_argument("path"); s.add_argument("--json", action="store_true")
    sub.add_parser("self-test")
    a = p.parse_args()
    if a.cmd == "self-test": return self_test()
    if a.cmd == "scan": scan(a.path, a.json); return 0


if __name__ == "__main__":
    sys.exit(main())
