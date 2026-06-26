#!/usr/bin/env python3
"""
ec-sample-tracker: Sample management for electrochemistry labs.
Tracks physical samples from synthesis through every characterization result.
"""

import argparse
import csv
import json
import os
import sqlite3
import sys
import textwrap
from datetime import datetime, date
from pathlib import Path

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


# ─── Database ─────────────────────────────────────────────────────────────────

DB_FILE = "samples.db"

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(textwrap.dedent("""
        CREATE TABLE IF NOT EXISTS samples (
            sample_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            synthesis_date TEXT,
            synthesis_method TEXT,
            precursors TEXT,
            substrate TEXT,
            catalyst_load REAL,
            target_reaction TEXT,
            tags TEXT,
            storage_location TEXT,
            owner TEXT,
            notes TEXT,
            status TEXT DEFAULT 'active',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """))
    cur.execute(textwrap.dedent("""
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sample_id TEXT,
            link_type TEXT,
            file_path TEXT,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sample_id) REFERENCES samples(sample_id)
        )
    """))
    cur.execute(textwrap.dedent("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sample_id TEXT,
            event_type TEXT,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sample_id) REFERENCES samples(sample_id)
        )
    """))
    cur.execute(textwrap.dedent("""
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sample_id TEXT,
            measurement_type TEXT,
            metric_name TEXT,
            metric_value REAL,
            unit TEXT,
            conditions TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sample_id) REFERENCES samples(sample_id)
        )
    """))
    conn.commit()
    return conn


# ─── Config ────────────────────────────────────────────────────────────────────

DEFAULT_CONFIG = {
    "lab_name": "Electrochemistry Lab",
    "id_prefix": "CAT",
    "next_id": 1,
    "storage_locations": [
        "fridge-4", "rack-A2", "rack-B1", "desiccator-2",
        "drawer-3", "given-out", "disposed"
    ],
    "default_owner": "xray",
    "db_file": "samples.db",
}

CONFIG_FILE = "config.yaml"


def load_config():
    import yaml
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return yaml.safe_load(f)
    return DEFAULT_CONFIG.copy()


def save_config(cfg):
    import yaml
    with open(CONFIG_FILE, "w") as f:
        yaml.safe_dump(cfg, f, default_flow_style=False)


def next_sample_id(config):
    sid = f"{config['id_prefix']}-{datetime.now().year}-{config['next_id']:04d}"
    config['next_id'] += 1
    save_config(config)
    return sid


# ─── Commands ──────────────────────────────────────────────────────────────────

def cmd_add(args):
    init_db()
    config = load_config()
    sample_id = next_sample_id(config)

    conn = get_db()
    cur = conn.cursor()
    cur.execute(textwrap.dedent("""
        INSERT INTO samples
        (sample_id, name, synthesis_date, synthesis_method, precursors,
         substrate, catalyst_load, target_reaction, tags, storage_location,
         owner, notes, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """), (
        sample_id,
        args.name,
        args.synthesis_date,
        args.method,
        args.precursors,
        args.substrate,
        args.load,
        args.reaction,
        args.tags,
        args.storage,
        args.owner,
        args.notes,
        args.status or "active",
    ))
    conn.commit()
    print(f"✅ Added sample: {sample_id}")
    print(f"   Name: {args.name}")
    print(f"   Method: {args.method}")
    print(f"   Storage: {args.storage or 'not set'}")
    print(f"   Reaction: {args.reaction or 'not set'}")


def cmd_list(args):
    init_db()
    conn = get_db()
    cur = conn.cursor()

    query = "SELECT * FROM samples WHERE 1=1"
    params = []

    if args.status:
        query += " AND status = ?"
        params.append(args.status)
    if args.reaction:
        query += " AND target_reaction = ?"
        params.append(args.reaction)
    if args.storage:
        query += " AND storage_location = ?"
        params.append(args.storage)
    if args.synth_after:
        query += " AND synthesis_date >= ?"
        params.append(args.synth_after)
    if args.synth_before:
        query += " AND synthesis_date <= ?"
        params.append(args.synth_before)
    if args.tag:
        query += " AND tags LIKE ?"
        params.append(f"%{args.tag}%")

    query += " ORDER BY sample_id DESC"

    if args.limit:
        query += f" LIMIT {args.limit}"

    cur.execute(query, params)
    rows = cur.fetchall()

    if not rows:
        print("No samples found.")
        return

    fmt = f"{{:<15}} {{:<35}} {{:<12}} {{:<10}} {{:<12}} {{:<15}}"
    print(fmt.format("ID", "Name", "Method", "Reaction", "Status", "Storage"))
    print("-" * 100)
    for r in rows:
        print(fmt.format(
            r['sample_id'],
            r['name'][:33],
            (r['synthesis_method'] or '')[:10],
            (r['target_reaction'] or '')[:10],
            r['status'][:10],
            (r['storage_location'] or '')[:13],
        ))
    print(f"\nTotal: {len(rows)} sample(s)")


def cmd_status(args):
    init_db()
    conn = get_db()
    cur = conn.cursor()

    print("=" * 60)
    print("  Sample Tracker — Status Overview")
    print("=" * 60)

    # Counts
    cur.execute("SELECT status, COUNT(*) as n FROM samples GROUP BY status")
    print("\n📊 By Status:")
    for r in cur.fetchall():
        print(f"  {r['status']:15} : {r['n']}")

    cur.execute("SELECT target_reaction, COUNT(*) as n FROM samples GROUP BY target_reaction")
    print("\n⚗️  By Reaction:")
    for r in cur.fetchall():
        print(f"  {r['target_reaction'] or 'unknown':15} : {r['n']}")

    cur.execute("SELECT storage_location, COUNT(*) as n FROM samples WHERE storage_location IS NOT NULL GROUP BY storage_location")
    print("\n📦 By Storage Location:")
    for r in cur.fetchall():
        print(f"  {r['storage_location']:20} : {r['n']}")

    cur.execute("SELECT COUNT(*) as n FROM samples")
    total = cur.fetchone()['n']
    cur.execute("SELECT COUNT(*) as n FROM links")
    n_links = cur.fetchone()['n']
    cur.execute("SELECT COUNT(*) as n FROM events")
    n_events = cur.fetchone()['n']

    print(f"\n📈 Total Samples: {total}")
    print(f"📎 Total Links:  {n_links}")
    print(f"📋 Total Events:  {n_events}")

    # Recent activity
    print("\n🕐 Recent Activity:")
    cur.execute(textwrap.dedent("""
        SELECT sample_id, event_type, description, created_at
        FROM events ORDER BY created_at DESC LIMIT 5
    """))
    for r in cur.fetchall():
        print(f"  [{r['created_at'][:10]}] {r['sample_id']}: {r['event_type']} — {r['description'][:50]}")


def cmd_link(args):
    init_db()
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT sample_id FROM samples WHERE sample_id = ?", (args.sample_id,))
    if not cur.fetchone():
        print(f"❌ Sample {args.sample_id} not found.")
        sys.exit(1)

    cur.execute(textwrap.dedent("""
        INSERT INTO links (sample_id, link_type, file_path, description)
        VALUES (?, ?, ?, ?)
    """), (args.sample_id, args.link_type, args.file, args.description or ""))

    conn.commit()
    print(f"✅ Linked {args.file} as [{args.link_type}] to {args.sample_id}")

    if args.link_type == "ec" and args.extract:
        _extract_and_log_ec_metrics(args.sample_id, args.file)


def _extract_and_log_ec_metrics(sample_id, file_path):
    """Auto-extract key metrics from EC files and log as measurements."""
    import re
    try:
        from scipy.interpolate import interp1d
        import numpy as np
    except ImportError:
        return

    ext = os.path.splitext(file_path)[1].lower()
    if ext not in [".csv", ".xlsx"]:
        return

    try:
        if ext == ".csv":
            with open(file_path) as f:
                lines = f.readlines()
            # Try to find potential/current columns
            for line in lines[:20]:
                cols = re.split(r'[,\t]', line.strip())
                if any('potential' in c.lower() or 'voltage' in c.lower() or 'ewe' in c.lower()
                       for c in cols):
                    for c in cols:
                        if any('current' in c.lower() or 'i' in c.lower() for c in cols):
                            break
    except Exception:
        pass


def cmd_search(args):
    init_db()
    conn = get_db()
    cur = conn.cursor()

    query = "SELECT * FROM samples WHERE 1=1"
    params = []

    if args.query:
        q = f"%{args.query}%"
        query += " AND (name LIKE ? OR tags LIKE ? OR notes LIKE ? OR sample_id LIKE ?)"
        params.extend([q, q, q, q])
    if args.tag:
        query += " AND tags LIKE ?"
        params.append(f"%{args.tag}%")
    if args.reaction:
        query += " AND target_reaction = ?"
        params.append(args.reaction)
    if args.status:
        query += " AND status = ?"
        params.append(args.status)
    if args.synth_after:
        query += " AND synthesis_date >= ?"
        params.append(args.synth_after)
    if args.synth_before:
        query += " AND synthesis_date <= ?"
        params.append(args.synth_before)
    if args.method:
        query += " AND synthesis_method = ?"
        params.append(args.method)

    cur.execute(query, params)
    rows = cur.fetchall()

    if not rows:
        print("No samples match your search.")
        return

    print(f"Found {len(rows)} matching sample(s):\n")
    for r in rows:
        print(f"  [{r['sample_id']}] {r['name']}")
        print(f"    Method: {r['synthesis_method']} | Reaction: {r['target_reaction']} | Status: {r['status']}")
        print(f"    Synthesized: {r['synthesis_date']} | Storage: {r['storage_location']}")
        print(f"    Tags: {r['tags']}")
        print()

        # Show links
        cur2 = conn.cursor()
        cur2.execute("SELECT * FROM links WHERE sample_id = ?", (r['sample_id'],))
        links = cur2.fetchall()
        if links:
            print(f"    Links ({len(links)}):")
            for l in links:
                print(f"      [{l['link_type']}] {l['file_path']}")
        print()


def cmd_log(args):
    init_db()
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT sample_id FROM samples WHERE sample_id = ?", (args.sample_id,))
    if not cur.fetchone():
        print(f"❌ Sample {args.sample_id} not found.")
        sys.exit(1)

    cur.execute(textwrap.dedent("""
        INSERT INTO events (sample_id, event_type, description)
        VALUES (?, ?, ?)
    """), (args.sample_id, args.event_type, args.note or ""))

    if args.update_status:
        cur.execute("UPDATE samples SET status = ? WHERE sample_id = ?",
                    (args.update_status, args.sample_id))

    conn.commit()
    print(f"✅ Logged [{args.event_type}] for {args.sample_id}")


def cmd_export(args):
    init_db()
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM samples ORDER BY sample_id")
    rows = cur.fetchall()

    if not rows:
        print("No samples to export.")
        return

    if args.format == "json":
        data = [dict(r) for r in rows]
        with open(args.output, "w") as f:
            json.dump(data, f, indent=2, default=str)
        print(f"✅ Exported {len(rows)} samples to {args.output} (JSON)")

    elif args.format == "csv":
        if not rows:
            return
        with open(args.output, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows([dict(r) for r in rows])
        print(f"✅ Exported {len(rows)} samples to {args.output} (CSV)")

    elif args.format == "markdown":
        lines = ["# Sample Inventory Report", "", f"Generated: {datetime.now().date()}", ""]
        lines.append(f"**Total samples:** {len(rows)}")
        lines.append("")
        lines.append("| ID | Name | Method | Reaction | Status | Storage | Tags |")
        lines.append("|---|---|---|---|---|---|---|")
        for r in rows:
            lines.append(f"| {r['sample_id']} | {r['name']} | {r['synthesis_method']} | "
                         f"{r['target_reaction']} | {r['status']} | {r['storage_location']} | {r['tags']} |")
        with open(args.output, "w") as f:
            f.write("\n".join(lines))
        print(f"✅ Exported {len(rows)} samples to {args.output} (Markdown)")


def cmd_import(args):
    init_db()
    config = load_config()
    conn = get_db()
    cur = conn.cursor()

    count = 0
    with open(args.file) as f:
        if args.file.endswith(".json"):
            records = json.load(f)
        else:
            reader = csv.DictReader(f)
            records = list(reader)

    for rec in records:
        sid = rec.get("sample_id") or next_sample_id(config)
        cur.execute(textwrap.dedent("""
            INSERT OR REPLACE INTO samples
            (sample_id, name, synthesis_date, synthesis_method, precursors,
             substrate, catalyst_load, target_reaction, tags, storage_location,
             owner, notes, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """), (
            sid,
            rec.get("name", ""),
            rec.get("synthesis_date", ""),
            rec.get("synthesis_method", ""),
            rec.get("precursors", ""),
            rec.get("substrate", ""),
            float(rec["catalyst_load"]) if rec.get("catalyst_load") else None,
            rec.get("target_reaction", ""),
            rec.get("tags", ""),
            rec.get("storage_location", ""),
            rec.get("owner", ""),
            rec.get("notes", ""),
            rec.get("status", "active"),
        ))
        count += 1

    conn.commit()
    print(f"✅ Imported {count} sample(s) from {args.file}")


def cmd_dashboard(args):
    if not HAS_MATPLOTLIB:
        print("❌ matplotlib required for dashboard. Run: pip install matplotlib")
        sys.exit(1)

    init_db()
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT status, COUNT(*) as n FROM samples GROUP BY status")
    status_data = {r['status']: r['n'] for r in cur.fetchall()}

    cur.execute("SELECT target_reaction, COUNT(*) as n FROM samples WHERE target_reaction IS NOT NULL GROUP BY target_reaction")
    reaction_data = {r['target_reaction']: r['n'] for r in cur.fetchall()}

    cur.execute("SELECT storage_location, COUNT(*) as n FROM samples WHERE storage_location IS NOT NULL GROUP BY storage_location")
    storage_data = {r['storage_location']: r['n'] for r in cur.fetchall()}

    cur.execute(textwrap.dedent("""
        SELECT sample_id, event_type, created_at FROM events
        ORDER BY created_at DESC LIMIT 10
    """))
    recent = cur.fetchall()

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.patch.set_facecolor('white')

    # Panel 1: Status pie
    ax1 = axes[0, 0]
    if status_data:
        labels = list(status_data.keys())
        sizes = list(status_data.values())
        colors = ["#4CAF50", "#FFC107", "#F44336", "#9E9E9E", "#2196F3"]
        ax1.pie(sizes, labels=labels, autopct="%1.0f%%", colors=colors[:len(labels)],
                startangle=90, textprops={"fontsize": 10})
        ax1.set_title("Samples by Status", fontsize=13, fontweight="bold")
    else:
        ax1.text(0.5, 0.5, "No data", ha="center", va="center", transform=ax1.transAxes)
        ax1.set_title("Samples by Status", fontsize=13, fontweight="bold")

    # Panel 2: Reaction bar
    ax2 = axes[0, 1]
    if reaction_data:
        reactions = list(reaction_data.keys())
        counts = list(reaction_data.values())
        bars = ax2.bar(reactions, counts, color=["#2196F3", "#4CAF50", "#FF9800", "#9C27B0", "#F44336"][:len(reactions)])
        ax2.set_title("Samples by Reaction", fontsize=13, fontweight="bold")
        ax2.set_ylabel("Count")
        for bar in bars:
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(int(bar.get_height())), ha="center", fontsize=9)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=30, ha="right")
    else:
        ax2.text(0.5, 0.5, "No data", ha="center", va="center", transform=ax2.transAxes)
        ax2.set_title("Samples by Reaction", fontsize=13, fontweight="bold")

    # Panel 3: Storage bar
    ax3 = axes[1, 0]
    if storage_data:
        locs = list(storage_data.keys())
        counts = list(storage_data.values())
        bars = ax3.barh(locs, counts, color="#607D8B")
        ax3.set_title("Samples by Storage", fontsize=13, fontweight="bold")
        ax3.set_xlabel("Count")
        for bar in bars:
            ax3.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                    str(int(bar.get_width())), va="center", fontsize=9)
    else:
        ax3.text(0.5, 0.5, "No data", ha="center", va="center", transform=ax3.transAxes)
        ax3.set_title("Samples by Storage", fontsize=13, fontweight="bold")

    # Panel 4: Recent activity
    ax4 = axes[1, 1]
    ax4.axis("off")
    ax4.set_title("Recent Activity", fontsize=13, fontweight="bold")
    if recent:
        text = "\n".join(
            f"[{r['created_at'][:10]}] {r['sample_id']}: {r['event_type']}"
            for r in recent
        )
        ax4.text(0.05, 0.95, text, transform=ax4.transAxes,
                fontsize=9, va="top", ha="left",
                family="monospace",
                bbox=dict(boxstyle="round,pad=0.5", facecolor="#F5F5F5", edgecolor="#CCCCCC"))
    else:
        ax4.text(0.5, 0.5, "No events yet", ha="center", va="center", transform=ax4.transAxes, fontsize=11)

    fig.suptitle("EC Sample Tracker — Dashboard", fontsize=16, fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(args.output or "sample-dashboard.png", dpi=300, bbox_inches="tight")
    print(f"✅ Dashboard saved to {args.output or 'sample-dashboard.png'}")


def cmd_view(args):
    """Show detailed info for a sample."""
    init_db()
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM samples WHERE sample_id = ?", (args.sample_id,))
    row = cur.fetchone()
    if not row:
        print(f"❌ Sample {args.sample_id} not found.")
        sys.exit(1)

    print("=" * 70)
    print(f"  {row['sample_id']} — {row['name']}")
    print("=" * 70)
    print(f"  Synthesis Date   : {row['synthesis_date']}")
    print(f"  Method           : {row['synthesis_method']}")
    print(f"  Precursors       : {row['precursors']}")
    print(f"  Substrate        : {row['substrate']}")
    print(f"  Catalyst Load    : {row['catalyst_load']} mg/cm²" if row['catalyst_load'] else "  Catalyst Load    : —")
    print(f"  Target Reaction  : {row['target_reaction']}")
    print(f"  Tags             : {row['tags']}")
    print(f"  Storage          : {row['storage_location']}")
    print(f"  Owner            : {row['owner']}")
    print(f"  Status           : {row['status']}")
    print(f"  Notes            : {row['notes']}")
    print(f"  Created          : {row['created_at']}")

    # Links
    cur2 = conn.cursor()
    cur2.execute("SELECT * FROM links WHERE sample_id = ?", (args.sample_id,))
    links = cur2.fetchall()
    if links:
        print(f"\n  📎 Links ({len(links)}):")
        for l in links:
            print(f"    [{l['link_type']}] {l['file_path']} ({l['created_at'][:10]})")

    # Events
    cur2.execute("SELECT * FROM events WHERE sample_id = ? ORDER BY created_at DESC", (args.sample_id,))
    events = cur2.fetchall()
    if events:
        print(f"\n  📋 Events ({len(events)}):")
        for e in events:
            print(f"    [{e['created_at'][:10]}] {e['event_type']}: {e['description'][:60]}")

    # Measurements
    cur2.execute("SELECT * FROM measurements WHERE sample_id = ? ORDER BY created_at DESC", (args.sample_id,))
    measurements = cur2.fetchall()
    if measurements:
        print(f"\n  📊 Measurements ({len(measurements)}):")
        for m in measurements:
            val = f"{m['metric_value']} {m['unit']}" if m['metric_value'] else "—"
            print(f"    [{m['measurement_type']}] {m['metric_name']}: {val}")


# ─── CLI Parser ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="EC Sample Tracker — Manage physical samples and their characterization data.")
    sub = parser.add_subparsers(dest="command")

    # add
    p_add = sub.add_parser("add", help="Register a new sample")
    p_add.add_argument("--name", "-n", required=True, help="Sample name/label")
    p_add.add_argument("--synthesis-date", "-d", default=datetime.now().strftime("%Y-%m-%d"), help="Synthesis date (YYYY-MM-DD)")
    p_add.add_argument("--method", "-m", help="Synthesis method")
    p_add.add_argument("--precursors", "-p", help="Comma-separated precursors")
    p_add.add_argument("--substrate", "-s", help="Substrate (GC/Ti foil/Ni foam/FTO/ITO/Carbon paper/None)")
    p_add.add_argument("--load", "-l", type=float, help="Catalyst loading (mg/cm²)")
    p_add.add_argument("--reaction", "-r", help="Target reaction (OER/HER/ORR/CO2RR/other)")
    p_add.add_argument("--tags", "-t", help="Comma-separated tags")
    p_add.add_argument("--storage", help="Storage location")
    p_add.add_argument("--owner", "-o", default="xray", help="Sample owner")
    p_add.add_argument("--notes", help="Free-text notes")
    p_add.add_argument("--status", default="active", help="Sample status")
    p_add.set_defaults(func=cmd_add)

    # list
    p_list = sub.add_parser("list", help="List samples with optional filters")
    p_list.add_argument("--status", help="Filter by status")
    p_list.add_argument("--reaction", help="Filter by reaction")
    p_list.add_argument("--storage", help="Filter by storage location")
    p_list.add_argument("--synth-after", help="Synthesized after (YYYY-MM-DD)")
    p_list.add_argument("--synth-before", help="Synthesized before (YYYY-MM-DD)")
    p_list.add_argument("--tag", help="Filter by tag")
    p_list.add_argument("--limit", type=int, help="Limit number of results")
    p_list.set_defaults(func=cmd_list)

    # status
    p_stat = sub.add_parser("status", help="Show sample status overview")
    p_stat.set_defaults(func=cmd_status)

    # link
    p_link = sub.add_parser("link", help="Attach a file or note to a sample")
    p_link.add_argument("sample_id", help="Sample ID (e.g. CAT-2026-0042)")
    p_link.add_argument("--type", "-t", required=True,
                       choices=["ec", "xrd", "sem", "tem", "raman", "xps", "photo", "note", "protocol"],
                       help="Link type")
    p_link.add_argument("--file", "-f", help="File path to link")
    p_link.add_argument("--description", help="Description")
    p_link.add_argument("--extract", action="store_true", help="Auto-extract EC metrics from file")
    p_link.set_defaults(func=cmd_link)

    # search
    p_search = sub.add_parser("search", help="Search samples")
    p_search.add_argument("--query", "-q", help="Free-text search (name, tags, notes, ID)")
    p_search.add_argument("--tag", "-t", help="Filter by tag")
    p_search.add_argument("--reaction", "-r", help="Filter by reaction")
    p_search.add_argument("--status", "-s", help="Filter by status")
    p_search.add_argument("--synth-after", help="Synthesized after (YYYY-MM-DD)")
    p_search.add_argument("--synth-before", help="Synthesized before (YYYY-MM-DD)")
    p_search.add_argument("--method", "-m", help="Synthesis method")
    p_search.set_defaults(func=cmd_search)

    # log
    p_log = sub.add_parser("log", help="Log an experimental event")
    p_log.add_argument("sample_id", help="Sample ID")
    p_log.add_argument("--event-type", "-e", required=True,
                       help="Event type (e.g. measurement/cycle/storage-move/aged/degraded)")
    p_log.add_argument("--note", "-n", help="Event description")
    p_log.add_argument("--update-status", help="Also update sample status")
    p_log.set_defaults(func=cmd_log)

    # export
    p_exp = sub.add_parser("export", help="Export sample records")
    p_exp.add_argument("--format", "-f", choices=["csv", "json", "markdown"], default="markdown", help="Output format")
    p_exp.add_argument("--output", "-o", default="samples-export.md", help="Output file")
    p_exp.set_defaults(func=cmd_export)

    # import
    p_imp = sub.add_parser("import", help="Bulk import from CSV/JSON")
    p_imp.add_argument("file", help="Input CSV or JSON file")
    p_imp.set_defaults(func=cmd_import)

    # dashboard
    p_dash = sub.add_parser("dashboard", help="Generate visual dashboard")
    p_dash.add_argument("--output", "-o", help="Output PNG file")
    p_dash.set_defaults(func=cmd_dashboard)

    # view
    p_view = sub.add_parser("view", help="View detailed sample information")
    p_view.add_argument("sample_id", help="Sample ID")
    p_view.set_defaults(func=cmd_view)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Change to skill dir for DB and config
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(skill_dir)

    args.func(args)


if __name__ == "__main__":
    main()
