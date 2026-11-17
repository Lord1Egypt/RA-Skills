#!/usr/bin/env python3
"""Minimal SQLite trace store (stdlib only).

python3 trace_store.py init
python3 trace_store.py add --task-id X --type Y --outcome success --duration-ms 1200 --tools a b
python3 trace_store.py summary --since 7
"""
import argparse
import json
import os
import sqlite3
from datetime import datetime, timedelta, timezone

DB = os.environ.get("TRACE_DB", "state/traces.sqlite")

SCHEMA = """
CREATE TABLE IF NOT EXISTS traces (
  task_id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  source TEXT DEFAULT 'manual',
  started_at TEXT NOT NULL,
  duration_ms INTEGER DEFAULT 0,
  tools TEXT DEFAULT '[]',
  retries INTEGER DEFAULT 0,
  tokens_in INTEGER DEFAULT 0,
  tokens_out INTEGER DEFAULT 0,
  outcome TEXT NOT NULL,
  error_class TEXT DEFAULT '',
  artifact TEXT DEFAULT '',
  notes TEXT DEFAULT '',
  constraint_fail INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_traces_type ON traces(type);
CREATE INDEX IF NOT EXISTS idx_traces_started ON traces(started_at);
"""


def con():
    os.makedirs(os.path.dirname(DB) or ".", exist_ok=True)
    c = sqlite3.connect(DB)
    c.executescript(SCHEMA)
    return c


def add(a):
    c = con()
    c.execute(
        """INSERT OR REPLACE INTO traces
           (task_id,type,source,started_at,duration_ms,tools,retries,tokens_in,tokens_out,
            outcome,error_class,artifact,notes,constraint_fail)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            a.task_id, a.type, a.source, a.started_at or datetime.now(timezone.utc).isoformat(timespec="seconds"),
            a.duration_ms, json.dumps(a.tools or []), a.retries, a.tokens_in, a.tokens_out,
            a.outcome, a.error_class, a.artifact, a.notes, a.constraint_fail,
        ),
    )
    c.commit()
    print(json.dumps({"ok": True, "task_id": a.task_id, "db": DB}))


def summary(days):
    c = con()
    since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat(timespec="seconds")
    rows = c.execute(
        """SELECT type, COUNT(*), SUM(outcome='success'), SUM(outcome!='success'),
                  ROUND(AVG(duration_ms)), SUM(constraint_fail)
           FROM traces WHERE started_at >= ? GROUP BY type ORDER BY type""",
        (since,),
    ).fetchall()
    out = [
        {"type": r[0], "runs": r[1], "success": r[2], "fail": r[3],
         "avg_ms": r[4], "constraint_fail": r[5]}
        for r in rows
    ]
    print(json.dumps({"since_days": days, "db": DB, "by_type": out}, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    a = sub.add_parser("add")
    a.add_argument("--task-id", required=True)
    a.add_argument("--type", required=True)
    a.add_argument("--source", default="manual")
    a.add_argument("--started-at", default="")
    a.add_argument("--duration-ms", type=int, default=0)
    a.add_argument("--tools", nargs="*", default=[])
    a.add_argument("--retries", type=int, default=0)
    a.add_argument("--tokens-in", type=int, default=0)
    a.add_argument("--tokens-out", type=int, default=0)
    a.add_argument("--outcome", required=True)
    a.add_argument("--error-class", default="")
    a.add_argument("--artifact", default="")
    a.add_argument("--notes", default="")
    a.add_argument("--constraint-fail", type=int, default=0)
    s = sub.add_parser("summary")
    s.add_argument("--since", type=int, default=7)
    args = ap.parse_args()

    if args.cmd == "init":
        con().close()
        print(json.dumps({"ok": True, "db": DB}))
    elif args.cmd == "add":
        add(args)
    else:
        summary(args.since)


if __name__ == "__main__":
    main()
