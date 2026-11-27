#!/usr/bin/env python3
"""run_checks.py - runs checks/questions.json through scripts/near_town.py and reports pass or fail.

This checks OUR DATA PATH (the live API and the script), not a language model.
Python standard library only; it runs near_town.py in this same process (no subprocess).
Read-only. About 60 paced calls (it asks each camp record's page for a 200). Usage:

  python run_checks.py            run all 8
  python run_checks.py t4 t6      run only those
Exit code 0 = all passed, 1 = at least one failed.
"""
import contextlib
import importlib.util
import io
import json
import os
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
NT = os.path.join(HERE, "..", "scripts", "near_town.py")
ENVELOPE_KEYS = ("request_url", "source", "record_date", "fetched_at", "credit")

_spec = importlib.util.spec_from_file_location("near_town", NT)
nt = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(nt)


def run(args):
    """Runs near_town.py main(args) in this process. Returns (json, None, exit_code) or (None, stderr text, exit_code)."""
    out, err = io.StringIO(), io.StringIO()
    code = 0
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            nt.main(list(args) + ["--json"])
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else 1
    except Exception as e:
        return None, "%s: %s" % (type(e).__name__, e), 1
    if code:
        return None, err.getvalue().strip(), code
    try:
        return json.loads(out.getvalue()), None, 0
    except ValueError:
        return None, out.getvalue()[:300], 1


def status_of(url):
    """The HTTP status of a record page (one GET, paced)."""
    time.sleep(0.5)
    req = urllib.request.Request(url, headers={"User-Agent": nt.UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def envelope_ok(o):
    return [k for k in ENVELOPE_KEYS if not o.get(k)]


def check(c):
    """Returns a list of problems (empty = pass)."""
    args = [c["town"], "--state", c["state"]]
    if "radius" in c:
        args += ["--radius", c["radius"]]
    if "limit" in c:
        args += ["--limit", str(c["limit"])]
    o, err, code = run(args)
    bad = []
    kind = c["kind"]
    if kind == "not_found":
        if code != 2 or "town not found" not in (err or ""):
            bad.append("expected a clean 'town not found' (exit 2), got exit %s: %s" % (code, err))
        return bad
    if o is None:
        return ["could not run: %s" % err]
    bad += ["envelope is missing %s" % k for k in envelope_ok(o)]
    if kind == "town":
        if not o["camps"]:
            bad.append("no free camp listed")
        for cp in o["camps"]:
            if cp.get("cost") != "free":
                bad.append("%s is listed but its cost is %r" % (cp.get("name"), cp.get("cost")))
            url = cp.get("record_url") or ""
            if not url.startswith("https://davelalande.com/camps/"):
                bad.append("%s has no camps record url" % cp.get("name"))
            elif status_of(url) != 200:
                bad.append("%s record url did not answer 200" % cp.get("name"))
    elif kind == "zero_result":
        z = o.get("zero_result") or {}
        if o["camps"] or o["free_count"] != 0:
            bad.append("expected no free camp inside %s miles" % c["radius"])
        if not z.get("said") or not (z.get("nearest_free_camp") or {}).get("miles"):
            bad.append("zero-result path gave no nearest free camp with miles")
        elif z["nearest_free_camp"].get("cost") != "free":
            bad.append("the nearest camp given is not free")
    elif kind == "limit":
        if len(o["camps"]) != c["limit"]:
            bad.append("expected %d camps, got %d" % (c["limit"], len(o["camps"])))
    return bad


def main():
    want = set(sys.argv[1:])
    checks = json.load(open(os.path.join(HERE, "questions.json"), encoding="utf-8"))["checks"]
    passed, failed = 0, []
    for c in checks:
        if want and c["id"] not in want:
            continue
        label = "%s  %s %s %s" % (c["id"], c["kind"], c["town"], c["state"])
        problems = check(c)
        if problems:
            failed.append(c["id"])
            print("FAIL %s\n     %s" % (label, "; ".join(problems)))
        else:
            passed += 1
            print("PASS %s" % label)
    print("\n%d passed, %d failed." % (passed, len(failed)))
    if failed:
        print("FAILED: " + ", ".join(failed) + ". Read each one: a failure may be a data change or a real data problem.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
