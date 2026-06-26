#!/usr/bin/env python3
"""CLI interface for amarin-memory — used by the OpenClaw skill."""

import argparse
import asyncio
import json
import os
import sys


def get_engine():
    """Get or create the MemoryEngine."""
    try:
        from amarin_memory import MemoryEngine
    except ImportError:
        print("ERROR: amarin-memory not installed. Run: pip install amarin-memory")
        sys.exit(1)

    db_dir = os.path.expanduser("~/.amarin")
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, "agent.db")
    embedding_url = os.environ.get("OLLAMA_URL", "http://localhost:11434")

    engine = MemoryEngine(db_path=db_path, embedding_url=embedding_url)
    engine.init_db()
    return engine


def cmd_store(args):
    engine = get_engine()
    content = args.content
    if content is None:
        content = sys.stdin.read().strip()
    if not content:
        print("ERROR: No content provided. Pass as argument or via stdin.")
        sys.exit(1)
    result = asyncio.run(engine.store(
        content=content,
        tags=args.tags or "",
        member_id=args.member or None,
        importance=args.importance,
        emotion_tags=args.emotion or None,
    ))
    action = result.get("action", "unknown")
    mem_id = result.get("memory_id", "?")
    reason = result.get("reason", "")
    if action == "skipped":
        print(f"Skipped — duplicate of memory #{result.get('existing_id', '?')} ({reason})")
    elif action == "merged":
        print(f"Merged into memory #{result.get('existing_id', '?')} ({reason})")
    else:
        print(f"Stored as memory #{mem_id} (action: {action}, {reason})")


def cmd_search(args):
    engine = get_engine()
    results = asyncio.run(engine.search(
        query=args.query,
        limit=args.limit,
        member_id=args.member or None,
    ))
    if not results:
        print("No results found.")
        return
    for r in results:
        score = r.get("score", 0)
        content = r.get("content", "")[:200]
        mem_id = r.get("id", "?")
        importance = r.get("importance", 0)
        print(f"  [{mem_id}] (score: {score:.3f}, importance: {importance:.2f}) {content}")


def cmd_blocks(args):
    engine = get_engine()
    blocks = engine.get_blocks()
    if not blocks:
        print("No core memory blocks set.")
        return
    for b in blocks:
        print(f"  [{b['label']}] {b['value']}")


def cmd_set_block(args):
    engine = get_engine()
    engine.set_block(args.label, args.value)
    print(f"Core block '{args.label}' set.")


def cmd_decay(args):
    engine = get_engine()
    engine.apply_decay(
        decay_rate=args.rate,
        min_importance=args.floor,
    )
    print(f"Temporal decay applied (rate: {args.rate}, floor: {args.floor}).")


def cmd_list(args):
    from amarin_memory.memory import list_archival
    engine = get_engine()
    db = engine.get_session()
    try:
        results = list_archival(db, limit=args.limit)
        if not results:
            print("No memories stored.")
            return
        for r in results:
            content = r["content"][:150]
            print(f"  [{r['id']}] (imp: {r.get('importance', 0):.2f}) {content}")
    finally:
        db.close()


def cmd_protect(args):
    from amarin_memory.memory import protect_archival
    engine = get_engine()
    db = engine.get_session()
    try:
        result = protect_archival(db, args.memory_id)
        if result.get("protected"):
            print(f"Memory #{args.memory_id} is now protected from decay.")
        else:
            print(f"Could not protect memory #{args.memory_id}: {result}")
    finally:
        db.close()


def cmd_revise(args):
    from amarin_memory.memory import revise_archival
    engine = get_engine()
    db = engine.get_session()
    try:
        result = revise_archival(db, args.memory_id, args.content, reason=args.reason)
        if result.get("revised"):
            print(f"Memory #{args.memory_id} revised.")
        else:
            print(f"Could not revise memory #{args.memory_id}: {result}")
    finally:
        db.close()


def cmd_forget(args):
    from amarin_memory.memory import deactivate_archival
    engine = get_engine()
    db = engine.get_session()
    try:
        result = deactivate_archival(db, args.memory_id, reason=args.reason)
        if result.get("forgotten"):
            print(f"Memory #{args.memory_id} soft-deleted. Can be restored.")
        else:
            print(f"Could not forget memory #{args.memory_id}: {result}")
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="Amarin Memory CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    # store
    p = sub.add_parser("store", help="Store a new memory")
    p.add_argument("content", nargs="?", default=None, help="Memory content (or pass via stdin with --stdin)")
    p.add_argument("--tags", default="", help="Comma-separated tags")
    p.add_argument("--importance", type=float, default=0.5, help="0.0-1.0")
    p.add_argument("--emotion", default=None, help="Emotion tags")
    p.add_argument("--member", default=None, help="Member ID for multi-agent isolation")

    # search
    p = sub.add_parser("search", help="Semantic search")
    p.add_argument("query", help="Search query")
    p.add_argument("--limit", type=int, default=5)
    p.add_argument("--member", default=None, help="Filter by member ID")

    # blocks
    sub.add_parser("blocks", help="List core memory blocks")

    # set-block
    p = sub.add_parser("set-block", help="Set a core memory block")
    p.add_argument("label", help="Block label (e.g., persona, human)")
    p.add_argument("value", help="Block content")

    # decay
    p = sub.add_parser("decay", help="Apply temporal decay")
    p.add_argument("--rate", type=float, default=0.01, help="Decay rate per day")
    p.add_argument("--floor", type=float, default=0.1, help="Minimum importance")

    # list
    p = sub.add_parser("list", help="List memories")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--offset", type=int, default=0)

    # protect
    p = sub.add_parser("protect", help="Protect a memory from decay")
    p.add_argument("memory_id", type=int)

    # revise
    p = sub.add_parser("revise", help="Revise a memory's content")
    p.add_argument("memory_id", type=int)
    p.add_argument("content", help="New content")
    p.add_argument("--reason", default="revised", help="Reason for revision")

    # forget
    p = sub.add_parser("forget", help="Soft-delete a memory")
    p.add_argument("memory_id", type=int)
    p.add_argument("--reason", default="no longer relevant", help="Reason")

    args = parser.parse_args()
    cmd_map = {
        "store": cmd_store,
        "search": cmd_search,
        "blocks": cmd_blocks,
        "set-block": cmd_set_block,
        "decay": cmd_decay,
        "list": cmd_list,
        "protect": cmd_protect,
        "revise": cmd_revise,
        "forget": cmd_forget,
    }
    cmd_map[args.command](args)


if __name__ == "__main__":
    main()
