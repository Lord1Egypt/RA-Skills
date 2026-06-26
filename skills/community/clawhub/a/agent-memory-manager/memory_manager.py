#!/usr/bin/env python3
"""
memory_manager.py — Agent Memory Manager
Veritas Corporate / OpenClaw Agent

Persistent structured memory across sessions.
Organizes memory by domain: clients, projects, trades, knowledge.

Operations:
  remember  → store new record
  recall    → retrieve record by id
  update    → update a field in existing record
  search    → full-text search across all memory
  list      → list all records in a domain
  archive   → move record to archived/
  init      → initialize memory directory structure
  stats     → show memory statistics

Usage:
  python3 memory_manager.py --init
  python3 memory_manager.py remember --domain clients --id "jean-dupont" --data '{...}'
  python3 memory_manager.py recall --domain clients --id "jean-dupont"
  python3 memory_manager.py update --domain clients --id "jean-dupont" --field "status" --value "client"
  python3 memory_manager.py search --query "cold email B2B"
  python3 memory_manager.py list --domain clients
  python3 memory_manager.py list --domain clients --filter "status=hot_lead"
  python3 memory_manager.py archive --domain clients --id "jean-dupont"
  python3 memory_manager.py stats
  python3 memory_manager.py due-today
"""

import json
import os
import sys
import argparse
import shutil
from datetime import datetime, date
from pathlib import Path
from typing import Optional, Any


# ─── CONFIG ────────────────────────────────────────────────────────────────
MEMORY_ROOT  = Path("/workspace/memory")
AUDIT_LOG    = Path("/workspace/AUDIT.md")
ERRORS_LOG   = Path("/workspace/.learnings/ERRORS.md")
DOMAINS      = ["clients", "projects", "trades", "knowledge"]
MAX_FILE_SIZE = 1_000_000  # 1MB — trigger compaction above this


# ─── HELPERS ───────────────────────────────────────────────────────────────
def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

def today_str() -> str:
    return date.today().isoformat()

def domain_path(domain: str, archived: bool = False) -> Path:
    p = MEMORY_ROOT / domain
    if archived:
        p = p / "archived"
    return p

def record_path(domain: str, record_id: str, archived: bool = False) -> Path:
    ext = ".md" if domain == "knowledge" else ".json"
    return domain_path(domain, archived) / f"{record_id}{ext}"

def slugify(text: str) -> str:
    import re
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text

def audit(msg: str):
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(f"\n[{now_iso()}] MEMORY: {msg}")

def log_error(msg: str):
    ERRORS_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(ERRORS_LOG, "a", encoding="utf-8") as f:
        f.write(f"\n[{now_iso()}] MEMORY ERROR: {msg}")

def load_json(path: Path) -> Optional[dict]:
    if not path.exists():
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        log_error(f"JSONDecodeError reading {path}: {e}")
        return None

def save_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_index() -> dict:
    idx_path = MEMORY_ROOT / "index.json"
    data = load_json(idx_path)
    if data is None:
        data = {
            "last_updated": now_iso(),
            "counts": {d: 0 for d in DOMAINS},
            "recent": [],
            "hot_leads": [],
            "active_trades": [],
            "active_projects": []
        }
    return data

def save_index(index: dict):
    index["last_updated"] = now_iso()
    save_json(MEMORY_ROOT / "index.json", index)

def update_index(domain: str, record_id: str, record: dict):
    idx = load_index()

    # Update counts
    count = len(list(domain_path(domain).glob("*.json")))
    idx["counts"][domain] = count

    # Update recent (keep last 10)
    entry = {"domain": domain, "id": record_id, "updated": today_str()}
    idx["recent"] = [r for r in idx["recent"] if r["id"] != record_id]
    idx["recent"].insert(0, entry)
    idx["recent"] = idx["recent"][:10]

    # Update hot_leads list
    if domain == "clients":
        status = record.get("status", "")
        is_hot = status in ("hot_lead", "client")
        if is_hot and record_id not in idx["hot_leads"]:
            idx["hot_leads"].append(record_id)
        elif not is_hot and record_id in idx["hot_leads"]:
            idx["hot_leads"].remove(record_id)

    # Update active_trades
    if domain == "trades":
        status = record.get("status", "")
        is_active = status == "open"
        if is_active and record_id not in idx["active_trades"]:
            idx["active_trades"].append(record_id)
        elif not is_active and record_id in idx["active_trades"]:
            idx["active_trades"].remove(record_id)

    # Update active_projects
    if domain == "projects":
        status = record.get("status", "")
        is_active = status == "active"
        if is_active and record_id not in idx["active_projects"]:
            idx["active_projects"].append(record_id)
        elif not is_active and record_id in idx["active_projects"]:
            idx["active_projects"].remove(record_id)

    save_index(idx)


# ─── OPERATIONS ────────────────────────────────────────────────────────────

def op_init():
    """Initialize memory directory structure."""
    for domain in DOMAINS:
        domain_path(domain).mkdir(parents=True, exist_ok=True)
        domain_path(domain, archived=True).mkdir(parents=True, exist_ok=True)

    (MEMORY_ROOT / "scripts").mkdir(parents=True, exist_ok=True)

    # Init knowledge files if they don't exist
    knowledge_files = ["acquisition", "trading", "content", "market_signals", "product"]
    for kf in knowledge_files:
        kpath = MEMORY_ROOT / "knowledge" / f"{kf}.md"
        if not kpath.exists():
            kpath.write_text(
                f"# knowledge/{kf}.md\n\n"
                f"_Initialized {today_str()} — Agent will enrich this file over time._\n",
                encoding="utf-8"
            )

    # Init index
    idx = load_index()
    save_index(idx)

    audit("Memory structure initialized")
    print("✅ Memory initialized:")
    print(f"   Root: {MEMORY_ROOT}")
    for domain in DOMAINS:
        print(f"   ✓ {domain}/")
    print(f"   ✓ index.json")
    print(f"   ✓ knowledge/ ({len(knowledge_files)} files)")


def op_remember(domain: str, record_id: str, data_str: str):
    """Store a new memory record."""
    if domain not in DOMAINS:
        print(f"❌ Unknown domain: {domain}. Valid: {DOMAINS}")
        sys.exit(1)

    record_id = slugify(record_id)
    path = record_path(domain, record_id)

    # Check for duplicate
    if path.exists():
        existing = load_json(path)
        print(f"⚠️  Record '{record_id}' already exists in {domain}/")
        print(f"   Auto-switching to UPDATE operation...")
        # Merge new data into existing
        try:
            new_data = json.loads(data_str)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in --data: {e}")
            log_error(f"remember: invalid JSON for {domain}/{record_id}: {e}")
            sys.exit(1)
        existing.update(new_data)
        existing["updated_at"] = today_str()
        save_json(path, existing)
        update_index(domain, record_id, existing)
        audit(f"Memory merged (auto-update): {domain}/{record_id}")
        print(f"✅ Merged: {domain}/{record_id}")
        return

    try:
        data = json.loads(data_str)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in --data: {e}")
        log_error(f"remember: invalid JSON for {domain}/{record_id}: {e}")
        sys.exit(1)

    # Add metadata
    data.setdefault("id", record_id)
    data.setdefault("slug", record_id)
    data.setdefault("domain", domain)
    data.setdefault("created_at", today_str())
    data["updated_at"] = today_str()

    save_json(path, data)
    update_index(domain, record_id, data)

    # Check file size
    if path.stat().st_size > MAX_FILE_SIZE:
        log_error(f"remember: {domain}/{record_id} exceeds 1MB — compaction needed")

    audit(f"Memory stored: {domain}/{record_id}")
    print(f"✅ Stored: {domain}/{record_id}")


def op_recall(domain: str, record_id: str, fmt: str = "pretty"):
    """Retrieve a memory record."""
    record_id = slugify(record_id)
    path = record_path(domain, record_id)

    if not path.exists():
        # Check archived
        archived = record_path(domain, record_id, archived=True)
        if archived.exists():
            print(f"ℹ️  Record '{record_id}' is archived.")
            path = archived
        else:
            print(f"❌ Not found: {domain}/{record_id}")
            print(f"   (Creating new record — use 'remember' to store data)")
            return None

    if domain == "knowledge":
        content = path.read_text(encoding="utf-8")
        print(content)
        return content

    data = load_json(path)
    if data is None:
        print(f"❌ Could not read {domain}/{record_id} — file may be corrupted")
        log_error(f"recall: read failure {domain}/{record_id}")
        return None

    if fmt == "json":
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        _pretty_print(domain, record_id, data)

    return data


def _pretty_print(domain: str, record_id: str, data: dict):
    print(f"\n{'─'*50}")
    print(f"  🧠 MEMORY: {domain.upper()} / {record_id}")
    print(f"{'─'*50}")

    if domain == "clients":
        p = data.get("profile", {})
        print(f"  Name:     {p.get('name', '—')}")
        print(f"  Company:  {p.get('company', '—')}  ({p.get('role', '—')})")
        print(f"  Email:    {p.get('email', '—')}")
        print(f"  Status:   {data.get('status', '—')}")
        print(f"  Channel:  {data.get('preferences', {}).get('preferred_channel', '—')}")
        interactions = data.get("interactions", [])
        print(f"  Interactions: {len(interactions)}")
        if interactions:
            last = interactions[-1]
            print(f"  Last:     {last.get('date')} via {last.get('channel')} → {last.get('outcome')}")
        print(f"  Next:     {data.get('next_action', '—')} ({data.get('next_action_date', '—')})")
        print(f"  Notes:    {data.get('notes', '—')}")

    elif domain == "trades":
        print(f"  Asset:    {data.get('asset', '—')}  {data.get('direction', '').upper()}")
        print(f"  Status:   {data.get('status', '—')}")
        print(f"  Entry:    {data.get('entry_price', '—')}")
        print(f"  Exit:     {data.get('exit_price', '—')}")
        pnl = data.get('pnl_usdt', 0)
        pct = data.get('pnl_pct', 0)
        sign = "+" if pnl >= 0 else ""
        print(f"  PnL:      {sign}{pnl} USDT ({sign}{pct}%)")
        print(f"  Strategy: {data.get('strategy', '—')}")
        print(f"  Lessons:  {data.get('lessons', '—')}")

    elif domain == "projects":
        print(f"  Name:     {data.get('name', '—')}")
        print(f"  Status:   {data.get('status', '—')}  Phase {data.get('phase', '—')}")
        print(f"  Goal:     {data.get('objective', '—')}")
        ms = data.get("milestones", [])
        done = sum(1 for m in ms if m.get("status") == "done")
        print(f"  Progress: {done}/{len(ms)} milestones done")
        print(f"  Next:     {data.get('next_action', '—')}")

    print(f"{'─'*50}")
    print(f"  Updated: {data.get('updated_at', '—')}")


def op_update(domain: str, record_id: str, field: str, value: str):
    """Update a specific field in an existing record."""
    record_id = slugify(record_id)
    path = record_path(domain, record_id)

    if not path.exists():
        print(f"❌ Not found: {domain}/{record_id} — use 'remember' to create first")
        sys.exit(1)

    data = load_json(path)
    if data is None:
        print(f"❌ Could not read {domain}/{record_id}")
        log_error(f"update: read failure {domain}/{record_id}")
        sys.exit(1)

    # Try to parse value as JSON (handles lists, dicts, booleans)
    try:
        parsed_value = json.loads(value)
    except (json.JSONDecodeError, ValueError):
        parsed_value = value

    # Support dot notation: interactions[-1].outcome
    if "." in field:
        parts = field.split(".", 1)
        if parts[0] in data and isinstance(data[parts[0]], dict):
            data[parts[0]][parts[1]] = parsed_value
        else:
            data[field] = parsed_value
    else:
        data[field] = parsed_value

    data["updated_at"] = today_str()
    save_json(path, data)
    update_index(domain, record_id, data)
    audit(f"Memory updated: {domain}/{record_id} → {field}={value}")
    print(f"✅ Updated: {domain}/{record_id}.{field} = {parsed_value}")


def op_search(query: str, domain: Optional[str] = None):
    """Full-text search across memory files."""
    query_lower = query.lower()
    results = []

    search_domains = [domain] if domain else DOMAINS
    for d in search_domains:
        dpath = domain_path(d)
        if not dpath.exists():
            continue
        pattern = "*.md" if d == "knowledge" else "*.json"
        for fpath in dpath.glob(pattern):
            try:
                content = fpath.read_text(encoding="utf-8").lower()
                if query_lower in content:
                    results.append({
                        "domain": d,
                        "id": fpath.stem,
                        "path": str(fpath),
                        "matches": content.count(query_lower)
                    })
            except Exception:
                continue

    results.sort(key=lambda x: x["matches"], reverse=True)

    if not results:
        print(f"🔍 No results for '{query}'")
        return []

    print(f"\n🔍 Search: '{query}' — {len(results)} result(s)")
    print(f"{'─'*50}")
    for r in results:
        print(f"  [{r['domain'].upper()}] {r['id']}  ({r['matches']} match{'es' if r['matches'] > 1 else ''})")
    print(f"{'─'*50}")
    print(f"  To recall: python3 memory_manager.py recall --domain [domain] --id [id]")

    return results


def op_list(domain: str, filter_str: Optional[str] = None):
    """List all records in a domain."""
    if domain not in DOMAINS:
        print(f"❌ Unknown domain: {domain}")
        sys.exit(1)

    dpath = domain_path(domain)
    if not dpath.exists():
        print(f"  No records in {domain}/")
        return

    pattern = "*.md" if domain == "knowledge" else "*.json"
    files = list(dpath.glob(pattern))

    if not files:
        print(f"  No records in {domain}/")
        return

    # Apply filter
    if filter_str and "=" in filter_str:
        filter_key, filter_val = filter_str.split("=", 1)
    else:
        filter_key = filter_val = None

    print(f"\n{'─'*50}")
    print(f"  🧠 {domain.upper()} — {len(files)} record(s)")
    print(f"{'─'*50}")

    count = 0
    for fpath in sorted(files):
        if domain == "knowledge":
            print(f"  📄 {fpath.stem}")
            count += 1
            continue

        data = load_json(fpath)
        if data is None:
            continue

        # Apply filter
        if filter_key:
            actual = str(data.get(filter_key, ""))
            if actual != filter_val:
                continue

        # Display summary line based on domain
        if domain == "clients":
            p = data.get("profile", {})
            name    = p.get("name", fpath.stem)
            company = p.get("company", "—")
            status  = data.get("status", "—")
            next_d  = data.get("next_action_date", "—")
            print(f"  {fpath.stem:<30} {status:<15} {company:<20} next: {next_d}")
        elif domain == "trades":
            asset   = data.get("asset", "—")
            status  = data.get("status", "—")
            pnl     = data.get("pnl_usdt", 0)
            sign    = "+" if pnl >= 0 else ""
            print(f"  {fpath.stem:<35} {status:<10} PnL: {sign}{pnl} USDT")
        elif domain == "projects":
            name    = data.get("name", fpath.stem)
            status  = data.get("status", "—")
            phase   = data.get("phase", "—")
            print(f"  {fpath.stem:<35} {status:<10} Phase {phase}  {name}")

        count += 1

    print(f"{'─'*50}")
    print(f"  Total shown: {count}")


def op_archive(domain: str, record_id: str):
    """Archive a record (move to archived/)."""
    record_id = slugify(record_id)
    src  = record_path(domain, record_id)
    dest = record_path(domain, record_id, archived=True)

    if not src.exists():
        print(f"❌ Not found: {domain}/{record_id}")
        sys.exit(1)

    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dest))

    # Update index
    idx = load_index()
    idx["counts"][domain] = len(list(domain_path(domain).glob("*.json")))
    for lst_key in ["hot_leads", "active_trades", "active_projects"]:
        if record_id in idx.get(lst_key, []):
            idx[lst_key].remove(record_id)
    save_index(idx)

    audit(f"Memory archived: {domain}/{record_id}")
    print(f"✅ Archived: {domain}/{record_id} → {domain}/archived/")


def op_stats():
    """Show memory statistics."""
    idx = load_index()

    print(f"\n{'='*50}")
    print(f"  🧠 MEMORY STATS")
    print(f"  Updated: {idx.get('last_updated', '—')}")
    print(f"{'='*50}")
    for domain in DOMAINS:
        count = idx["counts"].get(domain, 0)
        dpath = domain_path(domain)
        archived = len(list(domain_path(domain, True).glob("*.json"))) if domain != "knowledge" else 0
        print(f"  {domain:<15} {count:>4} active  {archived:>4} archived")
    print(f"{'─'*50}")
    hot = idx.get("hot_leads", [])
    active_t = idx.get("active_trades", [])
    active_p = idx.get("active_projects", [])
    print(f"  Hot leads:       {len(hot)}")
    if hot:
        print(f"    → {', '.join(hot[:5])}")
    print(f"  Active trades:   {len(active_t)}")
    print(f"  Active projects: {len(active_p)}")
    if active_p:
        print(f"    → {', '.join(active_p)}")
    print(f"{'='*50}")


def op_due_today():
    """Show all follow-ups and actions due today."""
    today = today_str()
    due = []

    dpath = domain_path("clients")
    if dpath.exists():
        for fpath in dpath.glob("*.json"):
            data = load_json(fpath)
            if data is None:
                continue
            next_date = data.get("next_action_date", "")
            if next_date and next_date <= today:
                due.append({
                    "domain": "clients",
                    "id": fpath.stem,
                    "action": data.get("next_action", "follow up"),
                    "date": next_date,
                    "name": data.get("profile", {}).get("name", fpath.stem),
                    "channel": data.get("preferences", {}).get("preferred_channel", "—"),
                })

    if not due:
        print(f"✅ No follow-ups due today ({today})")
        return

    print(f"\n{'─'*50}")
    print(f"  📅 DUE TODAY — {today} — {len(due)} action(s)")
    print(f"{'─'*50}")
    for item in sorted(due, key=lambda x: x["date"]):
        overdue = " ⚠️ OVERDUE" if item["date"] < today else ""
        print(f"  [{item['domain'].upper()}] {item['name']:<25} via {item['channel']:<10}")
        print(f"    Action: {item['action']}{overdue}")
    print(f"{'─'*50}")


# ─── MAIN ──────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Agent Memory Manager — Veritas Corporate"
    )
    subparsers = parser.add_subparsers(dest="operation")

    # init
    subparsers.add_parser("init", help="Initialize memory directory structure")

    # remember
    p_rem = subparsers.add_parser("remember", help="Store a new memory record")
    p_rem.add_argument("--domain", required=True, choices=DOMAINS)
    p_rem.add_argument("--id",     required=True)
    p_rem.add_argument("--data",   required=True, help="JSON string with record data")

    # recall
    p_rec = subparsers.add_parser("recall", help="Retrieve a memory record")
    p_rec.add_argument("--domain", required=True, choices=DOMAINS)
    p_rec.add_argument("--id",     required=True)
    p_rec.add_argument("--format", choices=["pretty", "json"], default="pretty")

    # update
    p_upd = subparsers.add_parser("update", help="Update a field in a record")
    p_upd.add_argument("--domain", required=True, choices=DOMAINS)
    p_upd.add_argument("--id",     required=True)
    p_upd.add_argument("--field",  required=True)
    p_upd.add_argument("--value",  required=True)

    # search
    p_srch = subparsers.add_parser("search", help="Full-text search across memory")
    p_srch.add_argument("--query",  required=True)
    p_srch.add_argument("--domain", choices=DOMAINS, default=None)

    # list
    p_list = subparsers.add_parser("list", help="List all records in a domain")
    p_list.add_argument("--domain", required=True, choices=DOMAINS)
    p_list.add_argument("--filter", dest="filter_str", default=None,
                        help="Filter by field value, e.g. status=hot_lead")

    # archive
    p_arch = subparsers.add_parser("archive", help="Archive a record")
    p_arch.add_argument("--domain", required=True, choices=DOMAINS)
    p_arch.add_argument("--id",     required=True)

    # stats
    subparsers.add_parser("stats", help="Show memory statistics")

    # due-today
    subparsers.add_parser("due-today", help="Show follow-ups due today")

    args = parser.parse_args()

    if args.operation is None:
        parser.print_help()
        sys.exit(0)

    if   args.operation == "init":
        op_init()
    elif args.operation == "remember":
        op_remember(args.domain, args.id, args.data)
    elif args.operation == "recall":
        op_recall(args.domain, args.id, args.format)
    elif args.operation == "update":
        op_update(args.domain, args.id, args.field, args.value)
    elif args.operation == "search":
        op_search(args.query, args.domain)
    elif args.operation == "list":
        op_list(args.domain, args.filter_str)
    elif args.operation == "archive":
        op_archive(args.domain, args.id)
    elif args.operation == "stats":
        op_stats()
    elif args.operation == "due-today":
        op_due_today()


if __name__ == "__main__":
    main()
