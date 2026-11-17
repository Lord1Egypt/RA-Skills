#!/usr/bin/env python3
"""memory_ledger.py — the reviewable core of a memory that must not be lost.

Pure stdlib, zero dependencies. Reads and writes only the ledger file itself
(never your memory files).

Why this exists
---------------
Memory does not get lost because it was never written — it gets lost because
it was written once and never reviewed. The ledger is a small table where every
must-read memory carries four things:

  why             — why this entry earns a place in every session
  review_by       — the date it gets looked at again
  max_age_days    — how stale it may get before it is treated as expired
  action_on_expiry — what happens when it expires (demote to the change-indexed
                    layer, archive it, re-ask the user …)

Two rules make the ledger bite:

  1. Adding an entry to the must-read layer requires naming an entry that
     gives up its place (the budget is finite, attention is finite).
  2. The must-read layer has a byte budget. Hard cap = 30000 bytes, target
     waterline = 25000. Above the hard cap the ledger is over budget and the
     check fails loudly — that is cheaper than a silent context blow-up.

Usage:
  python scripts/memory_ledger.py --init [--ledger .changsheng/ledger.json]
  python scripts/memory_ledger.py --check
  python scripts/memory_ledger.py --demo

Exit codes:
  0 = ledger clean (or no ledger yet)
  1 = issues found (missing file, incomplete entry, overdue review, stale
      entry, over budget)
  2 = usage error / unreadable ledger

Ledger file format (JSON, so no parser dependency):
{
  "budget_bytes": 30000,
  "target_bytes": 25000,
  "entries": [
    {"name": "rules", "path": "CLAUDE.md",
     "why": "house rules the user set",
     "review_by": "2026-11-05", "max_age_days": 30,
     "action_on_expiry": "demote to the change-indexed layer"}
  ]
}
"""

import argparse
import datetime as dt
import json
import os
import sys
import tempfile

LEDGER = os.path.join(".changsheng", "ledger.json")
BUDGET_DEFAULT = 30000
TARGET_DEFAULT = 25000
REQUIRED_FIELDS = ("why", "review_by", "max_age_days", "action_on_expiry")


def _today():
    return dt.date.today()


def _parse_date(v):
    if not v:
        return None
    try:
        return dt.date.fromisoformat(str(v).strip())
    except ValueError:
        return None


def _load(path):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return None
    except Exception as e:
        raise ValueError(f"cannot read {path}: {e}")
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top level must be an object")
    return data


def _save(path, data):
    d = os.path.dirname(os.path.abspath(path))
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".ledger_tmp_")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(tmp, path)
    except BaseException:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise


def _resolve(base, p):
    if not p:
        return p
    return p if os.path.isabs(p) else os.path.join(base, p)


def _skeleton(base):
    """Build a starter ledger from an existing discovery.json if present.
    Never invents entries — only what is already configured."""
    entries = []
    disc_path = os.path.join(base, ".changsheng", "discovery.json")
    try:
        with open(disc_path, encoding="utf-8") as f:
            disc = json.load(f)
    except Exception:
        disc = None
    if isinstance(disc, dict):
        for role, paths in (disc.get("roles") or {}).items():
            if role == "profile":
                continue
            for p in paths or []:
                if p == "injected":
                    continue
                entries.append({
                    "name": f"{role}: {os.path.basename(p)}",
                    "path": p,
                    "why": "", "review_by": "", "max_age_days": "",
                    "action_on_expiry": "",
                })
    return {"budget_bytes": BUDGET_DEFAULT, "target_bytes": TARGET_DEFAULT,
            "entries": entries}


def cmd_init(base, ledger_path, force):
    if os.path.exists(ledger_path) and not force:
        print(f"ledger already exists: {ledger_path} (use --force to overwrite)")
        return 0
    data = _skeleton(base)
    _save(ledger_path, data)
    print(f"ledger written -> {ledger_path} ({len(data['entries'])} entries)")
    if not data["entries"]:
        print("no existing memory files were found — add entries by hand:")
        print('  {"name": "...", "path": "...", "why": "...", "review_by": "YYYY-MM-DD",')
        print('   "max_age_days": 30, "action_on_expiry": "..."}')
    return 0


def check(data, base):
    """Return (issues, summary). Pure function — easy to test."""
    issues = []
    rows = []
    budget = int(data.get("budget_bytes") or BUDGET_DEFAULT)
    target = int(data.get("target_bytes") or TARGET_DEFAULT)
    today = _today()
    total = 0
    counted = set()          # same file under two roles counts once toward the budget
    entries = data.get("entries") or []
    for i, e in enumerate(entries):
        if not isinstance(e, dict):
            issues.append(f"entry {i}: not an object")
            continue
        name = e.get("name") or f"entry {i}"
        path = e.get("path") or ""
        full = _resolve(base, path)
        missing = [f for f in REQUIRED_FIELDS if not e.get(f)]
        size = 0
        if not path:
            issues.append(f"{name}: no path")
        elif not os.path.exists(full):
            issues.append(f"{name}: file not found ({path})")
        else:
            size = os.path.getsize(full)
            key = os.path.normcase(os.path.abspath(full))
            if key not in counted:
                counted.add(key)
                total += size
        if missing:
            issues.append(f"{name}: missing field(s) {', '.join(missing)}")
        rev = _parse_date(e.get("review_by"))
        if rev is None and e.get("review_by"):
            issues.append(f"{name}: review_by is not a date (YYYY-MM-DD)")
        elif rev is not None and rev < today:
            issues.append(f"{name}: review overdue since {rev.isoformat()}")
        max_age = e.get("max_age_days")
        if isinstance(max_age, (int, float)) and os.path.exists(full):
            age = (today - dt.date.fromtimestamp(os.path.getmtime(full))).days
            if age > max_age:
                issues.append(f"{name}: stale ({age}d > {max_age}d)")
        rows.append({"name": name, "path": path, "bytes": size,
                     "review_by": e.get("review_by") or "-",
                     "max_age_days": max_age if max_age != "" else "-",
                     "action_on_expiry": e.get("action_on_expiry") or "-",
                     "complete": not missing})
    if total > budget:
        issues.append(f"must-read layer over budget: {total}B > {budget}B")
    summary = {
        "entries": len(entries), "total_bytes": total, "budget_bytes": budget,
        "target_bytes": target, "over_budget": total > budget,
        "over_target": total > target, "issues": issues, "rows": rows,
    }
    return issues, summary


def cmd_check(base, ledger_path):
    try:
        data = _load(ledger_path)
    except ValueError as e:
        print(f"ledger error: {e}", file=sys.stderr)
        return 2
    if data is None:
        print(f"no ledger yet ({ledger_path}). Create one: python scripts/memory_ledger.py --init")
        return 0
    issues, s = check(data, base)
    print(f"must-read layer: {s['total_bytes']}B / budget {s['budget_bytes']}B "
          f"(target {s['target_bytes']}B) · entries {s['entries']}")
    for r in s["rows"]:
        flag = "ok " if r["complete"] else "TODO"
        print(f"  [{flag}] {r['name']} — {r['bytes']}B · review_by {r['review_by']} · "
              f"max_age {r['max_age_days']}d · on expiry: {r['action_on_expiry']}")
    if issues:
        print(f"{len(issues)} issue(s):")
        for i in issues:
            print(f"  - {i}")
        if s["over_budget"]:
            print("  fix: demote an entry (name it in the ledger as the one that gives up "
                  "its place) or archive it — the must-read layer does not grow past its budget")
        return 1
    print("ledger clean")
    return 0


def demo():
    import shutil
    d = tempfile.mkdtemp()
    try:
        base = os.path.join(d, "w")
        os.makedirs(base)
        with open(os.path.join(base, "rules.md"), "w", encoding="utf-8") as f:
            f.write("rules\n" * 100)
        with open(os.path.join(base, "todo.md"), "w", encoding="utf-8") as f:
            f.write("todo\n")
        good = {"budget_bytes": 30000, "target_bytes": 25000, "entries": [
            {"name": "rules", "path": "rules.md", "why": "house rules",
             "review_by": (dt.date.today() + dt.timedelta(days=10)).isoformat(),
             "max_age_days": 30, "action_on_expiry": "demote to change-indexed layer"},
        ]}
        issues, s = check(good, base)
        assert not issues, f"A clean ledger reported issues: {issues}"
        assert s["total_bytes"] > 0 and not s["over_budget"]

        bad = json.loads(json.dumps(good))
        bad["entries"][0]["path"] = "nope.md"
        issues, _ = check(bad, base)
        assert any("file not found" in i for i in issues), f"B missing file not caught: {issues}"

        bad = json.loads(json.dumps(good))
        bad["entries"][0]["action_on_expiry"] = ""
        issues, _ = check(bad, base)
        assert any("missing field" in i for i in issues), f"C incomplete not caught: {issues}"

        bad = json.loads(json.dumps(good))
        bad["entries"][0]["review_by"] = (dt.date.today() - dt.timedelta(days=1)).isoformat()
        issues, _ = check(bad, base)
        assert any("review overdue" in i for i in issues), f"D overdue not caught: {issues}"

        old = os.path.join(base, "rules.md")
        old_day = dt.date.today() - dt.timedelta(days=40)
        old_ts = dt.datetime.combine(old_day, dt.time()).timestamp()
        os.utime(old, (old_ts, old_ts))
        bad = json.loads(json.dumps(good))
        bad["entries"][0]["max_age_days"] = 30
        issues, _ = check(bad, base)
        assert any("stale" in i for i in issues), f"E stale not caught: {issues}"

        bad = json.loads(json.dumps(good))
        bad["budget_bytes"] = 10
        issues, s = check(bad, base)
        assert s["over_budget"] and any("over budget" in i for i in issues), \
            f"F over budget not caught: {issues}"

        # G: one file under two roles is counted once toward the budget
        two = json.loads(json.dumps(good))
        two["entries"].append({"name": "rules again", "path": "rules.md", "why": "dup role",
                               "review_by": (dt.date.today() + dt.timedelta(days=10)).isoformat(),
                               "max_age_days": 30, "action_on_expiry": "merge into rules"})
        issues, s = check(two, base)
        one = json.loads(json.dumps(good))
        _, s1 = check(one, base)
        assert s["total_bytes"] == s1["total_bytes"], \
            f"G duplicate file counted twice: {s['total_bytes']} vs {s1['total_bytes']}"

        os.makedirs(os.path.join(base, ".changsheng"))
        with open(os.path.join(base, ".changsheng", "discovery.json"), "w", encoding="utf-8") as f:
            json.dump({"roles": {"rules": ["rules.md"], "profile": ["p.md"],
                                 "journal": ["injected"]}}, f)
        lp = os.path.join(base, ".changsheng", "ledger.json")
        cmd_init(base, lp, force=False)
        data = _load(lp)
        names = [e["name"] for e in data["entries"]]
        assert len(names) == 1 and names[0].startswith("rules:"), f"G init wrong: {names}"
        cmd_init(base, lp, force=False)  # does not overwrite without --force
        print("[demo] memory_ledger: 9/9 PASS")
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", default=LEDGER,
                    help="ledger path (default .changsheng/ledger.json)")
    ap.add_argument("--init", action="store_true", help="create a starter ledger")
    ap.add_argument("--check", action="store_true", help="check the ledger (default action)")
    ap.add_argument("--force", action="store_true", help="overwrite an existing ledger on --init")
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()
    if args.demo:
        return demo()
    base = os.getcwd()
    if args.init:
        return cmd_init(base, args.ledger, args.force)
    return cmd_check(base, args.ledger)


if __name__ == "__main__":
    sys.exit(main())
