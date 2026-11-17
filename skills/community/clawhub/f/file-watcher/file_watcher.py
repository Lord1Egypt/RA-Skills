#!/usr/bin/env python3
"""
File System Watcher — watch, monitor, and diff file system changes.

Commands: watch, once, diff
Zero dependencies (Python stdlib only). Polling-based.
"""

import sys
import os
import time
import json
import hashlib
import fnmatch


# ── core ─────────────────────────────────────────────────────────────────

def snapshot_state(root, glob_filter=None, ignore_patterns=None):
    """
    Walk `root` and return a dict: {rel_path: {"mtime": ..., "size": ..., "hash": ...}}
    respecting glob/ignore patterns.
    """
    ignore_patterns = ignore_patterns or []
    glob_filter = glob_filter or []
    state = {}
    root = os.path.abspath(root)

    if os.path.isfile(root):
        # Single file mode
        rel = os.path.basename(root)
        if not _is_ignored(rel, ignore_patterns):
            if not glob_filter or any(fnmatch.fnmatch(rel, g) for g in glob_filter):
                state[rel] = _file_info(root)
        return state

    for dirpath, dirnames, filenames in os.walk(root):
        # Prune ignored directories (modify dirnames in-place)
        rel_dir = os.path.relpath(dirpath, root)
        if rel_dir == ".":
            rel_dir = ""
        dirnames[:] = [d for d in dirnames if not _is_ignored(
            os.path.join(rel_dir, d) if rel_dir else d, ignore_patterns
        )]

        for fname in filenames:
            rel_path = os.path.join(rel_dir, fname) if rel_dir else fname
            if _is_ignored(rel_path, ignore_patterns):
                continue
            if glob_filter and not any(fnmatch.fnmatch(rel_path, g) for g in glob_filter):
                continue
            full = os.path.join(dirpath, fname)
            state[rel_path] = _file_info(full)

    return state


def _file_info(path):
    """Return metadata dict for a single file."""
    try:
        st = os.stat(path)
        return {
            "mtime": st.st_mtime,
            "size": st.st_size,
            "hash": _quick_hash(path, st.st_size) if st.st_size < 10 * 1024 * 1024 else None,
        }
    except FileNotFoundError:
        return None


def _quick_hash(path, size):
    """MD5 hash (first 8KB + last 8KB for large files; full for small)."""
    h = hashlib.md5()
    with open(path, "rb") as f:
        if size <= 65536:
            h.update(f.read())
        else:
            h.update(f.read(8192))
            f.seek(-8192, os.SEEK_END)
            h.update(f.read(8192))
    return h.hexdigest()


def _is_ignored(rel_path, patterns):
    """Check if rel_path matches any ignore pattern."""
    for pat in patterns:
        # Strip leading **/
        p = pat.lstrip("*").lstrip("/")
        if fnmatch.fnmatch(rel_path, p) or fnmatch.fnmatch(os.path.basename(rel_path), p):
            return True
        # Dir match
        parts = rel_path.replace("\\", "/").split("/")
        for part in parts:
            if fnmatch.fnmatch(part, p):
                return True
    return False


def diff_states(before, after):
    """Compare two state dicts and return events list."""
    events = []
    all_paths = set(before.keys()) | set(after.keys())

    for path in sorted(all_paths):
        b = before.get(path)
        a = after.get(path)

        if b is None and a is not None:
            events.append({"type": "created", "path": path, "new": a})
        elif b is not None and a is None:
            events.append({"type": "deleted", "path": path, "old": b})
        elif b and a:
            changed = []
            if b["mtime"] != a["mtime"]:
                changed.append("mtime")
            if b["size"] != a["size"]:
                changed.append("size")
            if b["hash"] and a["hash"] and b["hash"] != a["hash"]:
                changed.append("hash")
            if changed:
                events.append({"type": "modified", "path": path, "changes": changed, "old": b, "new": a})

    return events


def format_event(event):
    """Format an event dict as a human-readable string."""
    t = event["type"]
    p = event["path"]
    if t == "created":
        return f"\033[92m[CREATED]\033[0m  {p}"
    elif t == "deleted":
        return f"\033[91m[DELETED]\033[0m  {p}"
    elif t == "modified":
        details = ", ".join(event.get("changes", []))
        return f"\033[93m[MODIFIED]\033[0m {p} ({details})"
    return f"[{t.upper()}] {p}"


# ── commands ─────────────────────────────────────────────────────────────

def cmd_watch(args):
    """Continuously watch a path for changes."""
    path = os.path.abspath(args.path)
    if not os.path.exists(path):
        print(f"\u274c {path}: does not exist", file=sys.stderr)
        sys.exit(1)

    ignore = args.ignore or []
    glob_filter = args.glob or []
    poll_interval = args.poll_interval or 1.0
    max_events = args.max_events or 0
    quiet = args.quiet

    if not quiet:
        print(f"Watching \033[1m{path}\033[0m (poll every {poll_interval}s)")
        if ignore:
            print(f"  Ignoring: {', '.join(ignore)}")
        if glob_filter:
            print(f"  Filter: {', '.join(glob_filter)}")

    prev_state = snapshot_state(path, glob_filter, ignore)
    event_count = 0

    try:
        while True:
            time.sleep(poll_interval)
            curr_state = snapshot_state(path, glob_filter, ignore)
            events = diff_states(prev_state, curr_state)
            prev_state = curr_state

            for ev in events:
                print(format_event(ev))
                event_count += 1
                if max_events and event_count >= max_events:
                    print(f"\nReached max events ({max_events}). Exiting.")
                    return
    except KeyboardInterrupt:
        if not quiet:
            print(f"\nStopped. {event_count} event(s) recorded.")


def cmd_once(args):
    """Take a one-time snapshot of a path."""
    path = os.path.abspath(args.path)
    if not os.path.exists(path):
        print(f"\u274c {path}: does not exist", file=sys.stderr)
        sys.exit(1)

    ignore = args.ignore or []
    glob_filter = args.glob or []
    state = snapshot_state(path, glob_filter, ignore)

    output = {
        "path": path,
        "timestamp": time.time(),
        "files": list(state.keys()),
        "file_count": len(state),
        "state": state,
    }

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)
        print(f"\u2705 Snapshot saved to {args.output} ({len(state)} files)")
    else:
        print(json.dumps(output, indent=2, ensure_ascii=False))


def cmd_diff(args):
    """Compare two snapshots and show changes."""
    with open(args.snapshot_a, "r", encoding="utf-8") as f:
        sa = json.load(f)
    with open(args.snapshot_b, "r", encoding="utf-8") as f:
        sb = json.load(f)

    before_state = sa.get("state", {})
    after_state = sb.get("state", {})

    events = diff_states(before_state, after_state)

    if not events:
        print("\u2705 No changes between snapshots")
        return

    print(f"Changes between {args.snapshot_a} and {args.snapshot_b}:")
    for ev in events:
        print(format_event(ev))

    # Summary
    counts = {"created": 0, "modified": 0, "deleted": 0}
    for ev in events:
        counts[ev["type"]] = counts.get(ev["type"], 0) + 1
    print(f"\nSummary: {counts['created']} created, {counts['modified']} modified, {counts['deleted']} deleted")


# ── argparse ─────────────────────────────────────────────────────────────

def build_parser():
    import argparse
    parser = argparse.ArgumentParser(
        description="File System Watcher \u2014 watch, snapshot, and diff file changes (polling-based)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("watch", help="Continuously watch for file changes")
    p.add_argument("path", help="File or directory to watch")
    p.add_argument("--poll-interval", "-i", type=float, default=1.0, help="Poll interval in seconds")
    p.add_argument("--ignore", action="append", default=[], help="Ignore pattern (can specify multiple)")
    p.add_argument("--glob", "-g", action="append", default=[], help="Only watch glob-matched files")
    p.add_argument("--max-events", "-n", type=int, default=0, help="Exit after N events")
    p.add_argument("--quiet", "-q", action="store_true", help="Suppress banner output")

    p = sub.add_parser("once", help="Take a one-time snapshot")
    p.add_argument("path", help="File or directory to snapshot")
    p.add_argument("--output", "-o", help="Output JSON file (default: stdout)")
    p.add_argument("--ignore", action="append", default=[], help="Ignore pattern")
    p.add_argument("--glob", "-g", action="append", default=[], help="Only snapshot glob-matched files")

    p = sub.add_parser("diff", help="Compare two snapshot JSON files")
    p.add_argument("snapshot_a", metavar="SNAPSHOT_A", help="First snapshot JSON")
    p.add_argument("snapshot_b", metavar="SNAPSHOT_B", help="Second snapshot JSON")

    sub.add_parser("self-test", help="Run built-in self tests")

    return parser


def _self_test():
    """Real test of snapshot + diff + format_event core. Returns 0/1."""
    import tempfile, os, time
    d = tempfile.mkdtemp(prefix="fw_selftest_")
    try:
        f1 = os.path.join(d, "a.txt")
        with open(f1, "w", encoding="utf-8") as fh:
            fh.write("v1")
        before = snapshot_state(d)
        if "a.txt" not in before or before["a.txt"] is None:
            print("self-test: FAIL (snapshot missing file)")
            return 1

        # create + modify a file
        with open(os.path.join(d, "b.txt"), "w", encoding="utf-8") as fh:
            fh.write("new")
        time.sleep(0.01)
        with open(f1, "w", encoding="utf-8") as fh:
            fh.write("v2-longer")

        after = snapshot_state(d)
        events = diff_states(before, after)
        types = {e["type"] for e in events}
        if "created" not in types:
            print("self-test: FAIL (created event not detected)")
            return 1
        if "modified" not in types:
            print("self-test: FAIL (modified event not detected)")
            return 1
        # format_event must render a string for each
        for ev in events:
            if not format_event(ev):
                print("self-test: FAIL (format_event empty)")
                return 1
        print("self-test: PASS")
        return 0
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)


def main():
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "self-test":
        sys.exit(_self_test())
    cmds = {
        "watch": cmd_watch,
        "once": cmd_once,
        "diff": cmd_diff,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
