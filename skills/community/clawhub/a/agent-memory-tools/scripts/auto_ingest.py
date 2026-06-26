#!/usr/bin/env python3
"""
auto_ingest — Watch workspace for .md changes, extract facts, store to agentMemory, update embed cache.

Modes:
    auto_ingest.py --watch          # fswatch daemon (continuous)
    auto_ingest.py --scan           # One-shot: scan recently modified files
    auto_ingest.py --file path.md   # Ingest a single file
    auto_ingest.py --post-compaction "LCM summary text"  # Extract from compaction output

Designed to run as a LaunchAgent or cron job.
"""
from __future__ import annotations
import os, sys
# Cross-platform PATH setup
if sys.platform == "darwin":
    os.environ["PATH"] = "/opt/homebrew/bin:" + os.environ.get("HOME", "") + "/.bun/bin:" + os.environ.get("PATH", "")

import argparse, json, hashlib, subprocess, time
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from llm_client import load_config, embed
from extract_facts import extract as extract_facts, store_to_convex
from knowledge_graph import update_graph_incremental

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
WATCH_DIRS = ["memory", "agents", "projects", "docs", "notes"]  # customize for your workspace
IGNORE_PATTERNS = [".cache", "__pycache__", "node_modules", ".git", "brain/references"]
MIN_FILE_SIZE = 50  # bytes — skip near-empty files
MAX_FILE_SIZE = 50_000  # bytes — skip huge files (process in chunks later)
DEBOUNCE_SECONDS = 5  # Wait before processing (batch rapid saves)
COOLDOWN_FILE_SECONDS = 300  # Don't re-process same file within 5 min


def load_state(state_path: str) -> dict:
    """Load ingestion state (last processed times per file)."""
    if os.path.exists(state_path):
        try:
            with open(state_path) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"processed": {}, "stats": {"total_files": 0, "total_facts": 0, "last_run": None}}


def save_state(state: dict, state_path: str):
    os.makedirs(os.path.dirname(state_path), exist_ok=True)
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2, default=str)


def content_hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()[:12]


def should_process(filepath: str, state: dict) -> bool:
    """Check if file needs processing (modified since last ingestion)."""
    if not os.path.isfile(filepath):
        return False
    
    size = os.path.getsize(filepath)
    if size < MIN_FILE_SIZE or size > MAX_FILE_SIZE:
        return False
    
    for pat in IGNORE_PATTERNS:
        if pat in filepath:
            return False
    
    if not filepath.endswith(".md"):
        return False
    
    mtime = os.path.getmtime(filepath)
    prev = state.get("processed", {}).get(filepath)
    
    if prev:
        # Skip if processed recently and content unchanged
        if time.time() - prev.get("at", 0) < COOLDOWN_FILE_SECONDS:
            return False
        # Check content hash
        try:
            with open(filepath) as f:
                current_hash = content_hash(f.read())
            if current_hash == prev.get("hash"):
                return False
        except IOError:
            return False
    
    return True


def ingest_file(filepath: str, cfg: dict, state: dict, agent: str = "default",
                debug: bool = False) -> int:
    """Process a single file: extract facts → store to agentMemory."""
    try:
        with open(filepath) as f:
            text = f.read()
    except IOError as e:
        if debug:
            print(f"  ⚠ Cannot read {filepath}: {e}", file=sys.stderr)
        return 0
    
    if len(text.strip()) < 30:
        return 0
    
    # Extract facts — truncate to ~4000 chars to stay within context window
    filename = os.path.basename(filepath)
    if len(text) > 4000:
        text = text[:4000] + "\n\n[... truncated ...]"
    context = f"[Source: {filepath}]\n\n{text}"
    
    if debug:
        print(f"  📄 Extracting from {filepath} ({len(text)} chars)...", file=sys.stderr)
    
    facts = extract_facts(context, cfg, debug)
    
    if not facts:
        if debug:
            print(f"  → 0 facts", file=sys.stderr)
        # Still update state to avoid reprocessing
        state.setdefault("processed", {})[filepath] = {
            "at": time.time(),
            "hash": content_hash(text),
            "facts": 0,
        }
        return 0
    
    # Store to agentMemory
    stored = store_to_convex(facts, agent=agent, debug=debug)
    
    if debug:
        print(f"  → {stored}/{len(facts)} facts stored", file=sys.stderr)
    
    # Update state
    state.setdefault("processed", {})[filepath] = {
        "at": time.time(),
        "hash": content_hash(text),
        "facts": stored,
    }
    state.setdefault("stats", {})["total_files"] = state["stats"].get("total_files", 0) + 1
    state["stats"]["total_facts"] = state["stats"].get("total_facts", 0) + stored
    state["stats"]["last_run"] = datetime.now().isoformat()
    
    return stored


def update_embed_cache(changed_files: list[str], cfg: dict, debug: bool = False):
    """Update embedding cache for changed files (incremental)."""
    ws = cfg.get("paths", {}).get("workspace", ".")
    cache_path = os.path.join(ws, ".cache", "embed-chunks.json")
    
    if not os.path.exists(cache_path):
        if debug:
            print("  📦 No embed cache — skip incremental update", file=sys.stderr)
        return
    
    try:
        with open(cache_path) as f:
            cache = json.load(f)
    except (json.JSONDecodeError, IOError):
        return
    
    chunks = cache.get("chunks", [])
    
    # Remove old chunks from changed files
    changed_set = set(os.path.abspath(f) for f in changed_files)
    chunks = [c for c in chunks if os.path.abspath(c.get("filepath", "")) not in changed_set]
    
    # Re-chunk changed files
    new_chunks = []
    chunk_size = cfg.get("embeddings", {}).get("chunkTokens", 400)
    overlap = cfg.get("embeddings", {}).get("overlap", 50)
    chars_per_chunk = chunk_size * 4  # rough chars-to-tokens
    overlap_chars = overlap * 4
    
    for fp in changed_files:
        try:
            with open(fp) as f:
                text = f.read()
        except IOError:
            continue
        
        # Simple chunking
        pos = 0
        chunk_idx = 0
        while pos < len(text):
            end = pos + chars_per_chunk
            chunk_text = text[pos:end]
            if len(chunk_text.strip()) > 20:
                new_chunks.append({
                    "filepath": os.path.abspath(fp),
                    "text": chunk_text,
                    "chunk_index": chunk_idx,
                })
            pos = end - overlap_chars if end < len(text) else end
            chunk_idx += 1
    
    if not new_chunks:
        return
    
    # Embed new chunks
    texts = [c["text"] for c in new_chunks]
    vectors = embed(texts, cfg, debug)
    
    if vectors and len(vectors) == len(new_chunks):
        for c, v in zip(new_chunks, vectors):
            c["embedding"] = v
        chunks.extend(new_chunks)
        cache["chunks"] = chunks
        cache["updated_at"] = datetime.now().isoformat()
        
        with open(cache_path, "w") as f:
            json.dump(cache, f)
        
        if debug:
            print(f"  📦 Embed cache updated: +{len(new_chunks)} chunks ({len(chunks)} total)", file=sys.stderr)


def scan_workspace(cfg: dict, state: dict, agent: str = "default",
                   debug: bool = False, max_files: int = 10) -> dict:
    """Scan workspace for recently modified .md files and ingest them."""
    ws = cfg.get("paths", {}).get("workspace", ".")
    
    candidates = []
    for watch_dir in WATCH_DIRS:
        dir_path = os.path.join(ws, watch_dir)
        if not os.path.isdir(dir_path):
            continue
        for root, dirs, files in os.walk(dir_path):
            # Skip ignored dirs
            dirs[:] = [d for d in dirs if d not in [".cache", "__pycache__", "node_modules", ".git"]]
            for fname in files:
                if fname.endswith(".md"):
                    fpath = os.path.join(root, fname)
                    if should_process(fpath, state):
                        candidates.append((os.path.getmtime(fpath), fpath))
    
    # Also check root-level important files
    for root_file in ["MEMORY.md", "USER.md", "COMPANY.md", "TOOLS.md"]:
        fpath = os.path.join(ws, root_file)
        if os.path.isfile(fpath) and should_process(fpath, state):
            candidates.append((os.path.getmtime(fpath), fpath))
    
    # Process most recently modified first
    candidates.sort(reverse=True)
    candidates = candidates[:max_files]
    
    total_stored = 0
    processed_files = []
    
    if debug and candidates:
        print(f"📂 Found {len(candidates)} files to ingest", file=sys.stderr)
    
    for mtime, fpath in candidates:
        stored = ingest_file(fpath, cfg, state, agent, debug)
        total_stored += stored
        processed_files.append(fpath)
    
    # Update embed cache + knowledge graph for changed files
    if processed_files:
        update_embed_cache(processed_files, cfg, debug)
        try:
            graph_stats = update_graph_incremental(processed_files, cfg, debug)
            if graph_stats and debug:
                print(f"🔗 Graph updated: {graph_stats.get('total_entities', 0)} entities", file=sys.stderr)
        except Exception as e:
            if debug:
                print(f"⚠ Graph update skipped: {e}", file=sys.stderr)
    
    return {"files_processed": len(processed_files), "facts_stored": total_stored}


def watch_loop(cfg: dict, state: dict, state_path: str, agent: str = "default",
               debug: bool = False):
    """Continuous file watcher. Uses fswatch on macOS, polling fallback everywhere else."""
    ws = cfg.get("paths", {}).get("workspace", ".")
    watch_paths = [os.path.join(ws, d) for d in WATCH_DIRS if os.path.isdir(os.path.join(ws, d))]
    
    if not watch_paths:
        print("❌ No watch directories found", file=sys.stderr)
        return
    
    print(f"👁 Watching {len(watch_paths)} dirs for .md changes...", file=sys.stderr)
    
    # Try fswatch (macOS), fall back to polling
    use_fswatch = False
    if sys.platform == "darwin":
        try:
            subprocess.run(["which", "fswatch"], capture_output=True, check=True)
            use_fswatch = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
    
    if use_fswatch:
        _watch_fswatch(watch_paths, cfg, state, state_path, agent, debug)
    else:
        _watch_polling(watch_paths, cfg, state, state_path, agent, debug)


def _watch_fswatch(watch_paths, cfg, state, state_path, agent, debug):
    """macOS fswatch watcher."""
    cmd = ["fswatch", "-r", "--event", "Updated", "--event", "Created",
           "-e", r"\.cache", "-e", r"__pycache__", "-e", r"\.git",
           "-i", r"\.md$"] + watch_paths
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
    pending = {}
    
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        filepath = line.strip()
        if not filepath.endswith(".md"):
            continue
        now = time.time()
        if filepath not in pending:
            pending[filepath] = now
        ready = [fp for fp, t in pending.items() if now - t >= DEBOUNCE_SECONDS]
        for fp in ready:
            del pending[fp]
            if should_process(fp, state):
                print(f"\n🔔 Change: {os.path.basename(fp)}", file=sys.stderr)
                stored = ingest_file(fp, cfg, state, agent, debug)
                if stored > 0:
                    print(f"   💾 {stored} facts → agentMemory", file=sys.stderr)
                update_embed_cache([fp], cfg, debug)
                try:
                    update_graph_incremental([fp], cfg, debug)
                except Exception:
                    pass
                save_state(state, state_path)


def _watch_polling(watch_paths, cfg, state, state_path, agent, debug, interval=30):
    """Cross-platform polling watcher (works on Windows/Linux/macOS)."""
    print(f"  Using polling mode (every {interval}s)", file=sys.stderr)
    known_mtimes = {}
    
    # Initial snapshot
    for wp in watch_paths:
        for root, dirs, files in os.walk(wp):
            dirs[:] = [d for d in dirs if d not in [".cache", "__pycache__", ".git"]]
            for f in files:
                if f.endswith(".md"):
                    fp = os.path.join(root, f)
                    try:
                        known_mtimes[fp] = os.path.getmtime(fp)
                    except OSError:
                        pass
    
    while True:
        time.sleep(interval)
        changed = []
        for wp in watch_paths:
            for root, dirs, files in os.walk(wp):
                dirs[:] = [d for d in dirs if d not in [".cache", "__pycache__", ".git"]]
                for f in files:
                    if not f.endswith(".md"):
                        continue
                    fp = os.path.join(root, f)
                    try:
                        mtime = os.path.getmtime(fp)
                    except OSError:
                        continue
                    if fp not in known_mtimes or mtime > known_mtimes[fp]:
                        known_mtimes[fp] = mtime
                        if should_process(fp, state):
                            changed.append(fp)
        
        for fp in changed:
            print(f"\n🔔 Change: {os.path.basename(fp)}", file=sys.stderr)
            stored = ingest_file(fp, cfg, state, agent, debug)
            if stored > 0:
                print(f"   💾 {stored} facts → agentMemory", file=sys.stderr)
            update_embed_cache([fp], cfg, debug)
        
        if changed:
            try:
                update_graph_incremental(changed, cfg, debug)
            except Exception:
                pass
            save_state(state, state_path)


def ingest_post_compaction(text: str, cfg: dict, agent: str = "default",
                           debug: bool = False) -> int:
    """Extract facts from LCM compaction summary text."""
    if debug:
        print(f"📋 Processing compaction output ({len(text)} chars)...", file=sys.stderr)
    
    facts = extract_facts(text, cfg, debug)
    if not facts:
        return 0
    
    stored = store_to_convex(facts, agent=agent, debug=debug)
    if debug:
        print(f"  → {stored}/{len(facts)} facts from compaction", file=sys.stderr)
    return stored


def main():
    parser = argparse.ArgumentParser(description="Auto-ingest workspace changes into agent memory")
    parser.add_argument("--watch", action="store_true", help="Continuous fswatch daemon")
    parser.add_argument("--scan", action="store_true", help="One-shot scan of recent changes")
    parser.add_argument("--file", help="Ingest a single file")
    parser.add_argument("--post-compaction", help="Extract from LCM compaction text (use - for stdin)")
    parser.add_argument("--max-files", type=int, default=10, help="Max files per scan (default 10)")
    parser.add_argument("--agent", default="default", help="Agent name")
    parser.add_argument("--preset", help="Config preset")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    
    cfg = load_config(preset=args.preset, script="extract")
    ws = cfg.get("paths", {}).get("workspace", ".")
    state_path = os.path.join(ws, ".cache", "ingest-state.json")
    state = load_state(state_path)
    
    if args.file:
        stored = ingest_file(args.file, cfg, state, args.agent, args.debug)
        save_state(state, state_path)
        print(f"💾 {stored} facts from {args.file}")
    
    elif args.post_compaction:
        text = sys.stdin.read() if args.post_compaction == "-" else args.post_compaction
        stored = ingest_post_compaction(text, cfg, args.agent, args.debug)
        print(f"💾 {stored} facts from compaction")
    
    elif args.scan:
        result = scan_workspace(cfg, state, args.agent, args.debug, args.max_files)
        save_state(state, state_path)
        print(f"📊 Scan: {result['files_processed']} files, {result['facts_stored']} facts stored")
        print(f"   Cumul: {state['stats'].get('total_files', 0)} files, {state['stats'].get('total_facts', 0)} facts total")
    
    elif args.watch:
        try:
            watch_loop(cfg, state, state_path, args.agent, args.debug)
        except KeyboardInterrupt:
            save_state(state, state_path)
            print("\n👁 Watcher stopped.", file=sys.stderr)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
