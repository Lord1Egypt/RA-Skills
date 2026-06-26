import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from importlib.metadata import PackageNotFoundError, version as _pkg_version
from .api import Journal, LegacyJournal
from .review import review_state
from .doctor_v2 import doctor_verify
from .migrate import import_legacy_workspace
from .analytics import memory_stats, memory_topics, memory_cadence, memory_digest, extract_candidates
from .promote import collect_candidates, DEFAULT_TRIGGERS
from .episodic_recall import recall_episodic, recall_recent


def _resolve_version() -> str:
    try:
        return _pkg_version('agent-memory-journal')
    except PackageNotFoundError:
        return '0.0.0+dev'


def parse_iso_date(value: str):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Invalid date '{value}', expected YYYY-MM-DD") from exc


def main():
    ap = argparse.ArgumentParser(description="Agent Memory Journal V2")
    ap.add_argument("--root", default=os.environ.get("AGENT_MEMORY_ROOT", "."), help="Memory root directory")
    ap.add_argument("--memory-dir", default="memory", help="Legacy memory directory")
    ap.add_argument("--long-file", default="MEMORY.md", help="Legacy long file")
    ap.add_argument("--version", action="version", version=_resolve_version())
    sub = ap.add_subparsers(dest="cmd", required=True)

    # Note command
    n = sub.add_parser("note", help="Add an episodic note")
    n.add_argument("text")
    n.add_argument("--category", help="Optional category")
    n.add_argument("--importance", default="normal", choices=["normal", "high"])

    # Legacy Add command
    a = sub.add_parser("add", help="Add a note (legacy compatibility)")
    a.add_argument("--note", required=True)
    a.add_argument("--long", action="store_true")

    # Remember command
    r = sub.add_parser("remember", help="Add a core memory")
    r.add_argument("text")
    r.add_argument("--category", required=True)
    r.add_argument("--pinned", action="store_true")

    # Forget command
    f = sub.add_parser("forget", help="Supersede a core memory by ID")
    f.add_argument("id")

    # Ingest command
    sub.add_parser("ingest", help="Run ingestion cycle (promote & rebuild)")

    # Review command
    rv = sub.add_parser("review", help="Show memory layer status report")
    rv.add_argument("--json", action="store_true")

    # Doctor command
    dc = sub.add_parser("doctor", help="Verify integrity of core memory")
    dc.add_argument("--json", action="store_true")
    dc.add_argument("--strict", action="store_true")
    dc.add_argument("--fix", action="store_true")
    dc.add_argument("--after", type=parse_iso_date)
    dc.add_argument("--before", type=parse_iso_date)

    # Migrate command
    sub.add_parser("migrate", help="Import legacy memory files into V2 layout")

    # Stats command
    st = sub.add_parser("stats", help="Show episodic memory statistics")
    st.add_argument("--days", type=int, default=7)
    st.add_argument("--json", action="store_true")

    # Topics command
    tp = sub.add_parser("topics", help="Surface recurring topics")
    tp.add_argument("--days", type=int, default=14)
    tp.add_argument("--json", action="store_true")

    # Cadence command
    cd = sub.add_parser("cadence", help="Show daily note volume")
    cd.add_argument("--days", type=int, default=14)
    cd.add_argument("--json", action="store_true")

    # Digest command
    dg = sub.add_parser("digest", help="Print operational digest")
    dg.add_argument("--days", type=int, default=7)
    dg.add_argument("--json", action="store_true")

    # Candidates command
    can = sub.add_parser("candidates", help="Surface promotion candidates")
    can.add_argument("--days", type=int, default=7)
    can.add_argument("--json", action="store_true")

    # Extract command
    ex = sub.add_parser("extract", help="Extract memory lines from text")
    ex.add_argument("--file", type=Path)

    # Recent command
    rc = sub.add_parser("recent", help="Show recent episodic notes")
    rc.add_argument("--days", type=int, default=2)
    rc.add_argument("--json", action="store_true")
    rc.add_argument("--grep")

    # Search command
    sh = sub.add_parser("search", help="Search memory")
    sh.add_argument("--query", required=True)
    sh.add_argument("--tier", choices=["all", "warm", "cold"], default="all")
    sh.add_argument("--json", action="store_true")

    # Init command
    it = sub.add_parser("init", help="Initialize memory root")
    it.add_argument("--with-config", action="store_true")

    args = ap.parse_args()
    journal = Journal(root=args.root)

    if args.cmd == "note":
        path = journal.note(args.text, category=args.category, importance=args.importance)
        print(f"Note added to {path}")
    elif args.cmd == "add":
        if args.long:
            path = journal.remember(args.note, category="decision")
            print(f"Memory remembered in {path}")
        else:
            path = journal.note(args.note)
            print(f"Note added to {path}")
    elif args.cmd == "remember":
        path = journal.remember(args.text, category=args.category, pinned=args.pinned)
        print(f"Memory remembered in {path}")
    elif args.cmd == "forget":
        success = journal.forget(args.id)
        if success:
            print(f"Memory {args.id} superseded.")
        else:
            print(f"Memory {args.id} not found.")
    elif args.cmd == "ingest":
        report = journal.ingest()
        print(json.dumps(report.__dict__ if hasattr(report, "__dict__") else report, indent=2))
    elif args.cmd == "review":
        report = review_state(journal.v2_root)
        if args.json:
            print(json.dumps(report.__dict__ if hasattr(report, "__dict__") else report, indent=2))
        else:
            print(f"Status: {report.status}")
            print(f"Episodic candidates: {report.episodic_candidates}")
            print(f"Pinned items: {report.pinned_core_items}")
    elif args.cmd == "doctor":
        report = doctor_verify(journal.v2_root, fix=args.fix)
        if args.json:
            print(json.dumps(report.__dict__ if hasattr(report, "__dict__") else report, indent=2))
        else:
            print(f"Status: {report.status}")
        if args.strict and report.status != "OK":
            sys.exit(1)
    elif args.cmd == "migrate":
        results = import_legacy_workspace(journal.root if journal.root.name != ".memory" else journal.root.parent)
        print(json.dumps(results, indent=2))
    elif args.cmd == "stats":
        stats = memory_stats(journal.v2_root, days=args.days)
        print(json.dumps(stats, indent=2))
    elif args.cmd == "topics":
        topics = memory_topics(journal.v2_root, days=args.days)
        print(json.dumps(topics, indent=2))
    elif args.cmd == "cadence":
        cadence = memory_cadence(journal.v2_root, days=args.days)
        print(json.dumps(cadence, indent=2))
    elif args.cmd == "digest":
        digest = memory_digest(journal.v2_root, days=args.days)
        print(json.dumps(digest, indent=2))
    elif args.cmd == "candidates":
        candidates = collect_candidates(journal.v2_root)
        print(json.dumps([c.__dict__ for c in candidates], indent=2))
    elif args.cmd == "extract":
        text = args.file.read_text(encoding="utf-8") if args.file else sys.stdin.read()
        lines = extract_candidates(text, triggers=DEFAULT_TRIGGERS)
        print(json.dumps(lines, indent=2))
    elif args.cmd == "recent":
        if args.grep:
            hits = recall_episodic(journal.v2_root, query=args.grep, k=100)
        else:
            hits = recall_recent(journal.v2_root, days=args.days, k=100)
        if args.json:
            print(json.dumps([h.__dict__ for h in hits], indent=2))
        else:
            for h in hits:
                print(f"- {h.text}")
    elif args.cmd == "search":
        hits = journal.recall(args.query, tier=args.tier)
        if args.json:
            print(json.dumps([{"text": h.text, "path": h.path, "score": h.score, "tier": getattr(h, "tier", "cold")} for h in hits], indent=2))
        else:
            for h in hits:
                tier = getattr(h, "tier", "cold")
                print(f"[{tier}] {h.text}")
    elif args.cmd == "init":
        journal.init()
        print(json.dumps({"created": [], "root": str(journal.v2_root)}))


if __name__ == "__main__":
    main()
