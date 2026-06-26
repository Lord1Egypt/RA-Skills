#!/usr/bin/env python3
"""
AI Session Tool Analysis — Deep dive into tool usage patterns.
Reads Claude Code project transcripts, Codex events, and Kimi wire protocol.

Usage: python3 tool_analysis.py
"""

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from shared import classify_shell_cmd, strip_home_prefix  # noqa: E402

HOME = Path.home()

# ── Claude Code ──────────────────────────────────────────────

def analyze_claude():
    print("=" * 60)
    print("CLAUDE CODE — Tool Deep Dive")
    print("=" * 60)

    projects_dir = HOME / ".claude" / "projects"
    jsonl_files = list(projects_dir.rglob("*.jsonl"))

    tool_counts = Counter()
    shell_cmds = []
    read_files = []
    write_files = []
    edit_files = []
    project_tools = defaultdict(Counter)
    parse_errors = 0

    for jf in jsonl_files:
        proj = strip_home_prefix(str(jf.relative_to(projects_dir).parts[0]))
        try:
            for line in jf.read_text().strip().splitlines():
                if not line.strip(): continue
                d = json.loads(line)
                if d.get("type") != "assistant": continue
                content = d.get("message", {}).get("content", [])
                if not isinstance(content, list): continue
                for block in content:
                    if not isinstance(block, dict) or block.get("type") != "tool_use":
                        continue
                    tn = block.get("name", "?")
                    tool_counts[tn] += 1
                    project_tools[proj][tn] += 1
                    inp = block.get("input", {})
                    if tn == "Bash" and isinstance(inp, dict):
                        cmd = inp.get("command", "")
                        if cmd: shell_cmds.append(cmd)
                    elif tn == "Read" and isinstance(inp, dict):
                        read_files.append(inp.get("file_path", ""))
                    elif tn == "Write" and isinstance(inp, dict):
                        write_files.append(inp.get("file_path", ""))
                    elif tn == "Edit" and isinstance(inp, dict):
                        edit_files.append(inp.get("file_path", ""))
        except Exception:
            parse_errors += 1

    # Shell commands
    print(f"\n── Shell Commands ({len(shell_cmds):,} total) ──")
    cats = Counter()
    for cmd in shell_cmds:
        cats[classify_shell_cmd(cmd)] += 1
    for cat, cnt in cats.most_common():
        bar = "█" * max(1, cnt // 50)
        print(f"  {cat:<20} {cnt:>6} {bar}")

    print(f"\n  Sample commands:")
    for cmd in shell_cmds[:5]:
        print(f"    $ {cmd[:150]}")

    # File operations
    print(f"\n── File Operations ──")
    print(f"  Read:  {len(read_files):,} calls")
    print(f"  Write: {len(write_files):,} calls")
    print(f"  Edit:  {len(edit_files):,} calls")

    # File types
    if read_files:
        exts = Counter()
        for fp in read_files:
            ext = Path(fp).suffix if fp else "?"
            exts[ext or "(none)"] += 1
        print(f"\n  Top file types read:")
        for ext, cnt in exts.most_common(10):
            print(f"    {ext:<15} {cnt:>5}")

    # Projects
    print(f"\n── Top projects by tool calls ──")
    for proj, tools in sorted(project_tools.items(), key=lambda x: sum(x[1].values()), reverse=True)[:10]:
        total = sum(tools.values())
        top3 = ", ".join(f"{t}({c})" for t, c in tools.most_common(3))
        print(f"  {proj:<50} {total:>6} — {top3}")

    if parse_errors:
        print(f"\nParse errors: {parse_errors}")

# ── Codex ────────────────────────────────────────────────────

def analyze_codex():
    print("\n" + "=" * 60)
    print("CODEX — Tool Deep Dive")
    print("=" * 60)

    sessions_dir = HOME / ".codex" / "sessions"
    jsonl_files = list(sessions_dir.rglob("*.jsonl"))

    shell_cmds = []
    searches = []
    patches_ok = 0
    patches_total = 0
    errors_list = []
    token_in = 0; token_out = 0; token_cache = 0
    parse_errors = 0

    for sf in jsonl_files:
        try:
            for line in sf.read_text().strip().splitlines():
                if not line.strip(): continue
                d = json.loads(line)
                if d.get("type") != "event_msg": continue
                p = d.get("payload", {})
                et = p.get("type", "")
                if et == "exec_command_end":
                    cmd_arr = p.get("command", [])
                    cmd = " ".join(cmd_arr) if isinstance(cmd_arr, list) else str(cmd_arr)
                    shell_cmds.append(cmd)
                elif et == "patch_apply_end":
                    patches_total += 1
                    if p.get("success"): patches_ok += 1
                elif et == "web_search_end":
                    searches.append(p.get("query", "")[:120])
                elif et == "token_count":
                    token_in += p.get("input_tokens", 0) or 0
                    token_out += p.get("output_tokens", 0) or 0
                    token_cache += p.get("cache_hit_tokens", 0) or 0
                elif et == "error":
                    errors_list.append(str(p.get("message", ""))[:120])
        except Exception:
            parse_errors += 1

    print(f"\n── Shell ({len(shell_cmds):,}) ──")
    cats = Counter()
    for cmd in shell_cmds:
        cats[classify_shell_cmd(cmd)] += 1
    for cat, cnt in cats.most_common():
        print(f"  {cat:<20} {cnt:>5} {'█' * max(1, cnt//5)}")

    print(f"\n── Patches: {patches_total} ({patches_ok} ok)")
    print(f"── Web searches: {len(searches)}")
    if searches:
        for q in searches[:3]: print(f"  \"{q}\"")

    if token_in > 0:
        print(f"\n── Tokens: in={token_in:,} out={token_out:,} cache={token_cache:,} ({token_cache/token_in*100:.1f}% hit)")

    if errors_list:
        print(f"\n── Errors ({len(errors_list)}):")
        for err, cnt in Counter(e[:80] for e in errors_list).most_common(3):
            print(f"  [{cnt}x] {err}")

    if parse_errors:
        print(f"\nParse errors: {parse_errors}")

# ── Kimi Code ────────────────────────────────────────────────

def analyze_kimi():
    print("\n" + "=" * 60)
    print("KIMI CODE — Tool Deep Dive")
    print("=" * 60)

    wire_files = list((HOME / ".kimi" / "sessions").rglob("wire.jsonl"))

    tool_counts = Counter()
    shell_cmds = []
    parse_errors = 0

    for wf in wire_files:
        try:
            for line in wf.read_text().strip().splitlines():
                if not line.strip(): continue
                d = json.loads(line)
                msg = d.get("message", {})
                if not isinstance(msg, dict): continue
                if msg.get("type") != "ToolCall": continue
                func = msg.get("payload", {}).get("function", msg.get("function", {}))
                tn = func.get("name", "?")
                tool_counts[tn] += 1
                args_str = func.get("arguments", "{}")
                try:
                    args = json.loads(args_str) if isinstance(args_str, str) else args_str
                    cmd = args.get("command", "")
                    if cmd: shell_cmds.append(cmd)
                except Exception: pass
        except Exception:
            parse_errors += 1

    domain_tools = Counter()
    for tn, cnt in tool_counts.items():
        if tn not in ("Shell", "ReadFile", "WriteFile", "StrReplaceFile", "Glob", "Grep"):
            domain_tools[tn] = cnt

    print(f"\n── Core tools ──")
    for tn in ["Shell", "ReadFile", "Glob", "WriteFile", "StrReplaceFile", "Grep"]:
        if tn in tool_counts:
            print(f"  {tn:<25} {tool_counts[tn]:>6}")

    if domain_tools:
        print(f"\n── Domain tools ({len(domain_tools)} types) ──")
        for tn, cnt in domain_tools.most_common(15):
            print(f"  {tn:<35} {cnt:>5}")

    print(f"\n── Shell ({len(shell_cmds):,}) ──")
    cats = Counter()
    for cmd in shell_cmds:
        cats[classify_shell_cmd(cmd)] += 1
    for cat, cnt in cats.most_common():
        print(f"  {cat:<20} {cnt:>5} {'█' * max(1, cnt//10)}")

    if shell_cmds:
        print(f"\n  Sample:")
        for cmd in shell_cmds[:5]:
            print(f"    $ {cmd[:150]}")

    if parse_errors:
        print(f"\nParse errors: {parse_errors}")

if __name__ == "__main__":
    analyze_claude()
    analyze_codex()
    analyze_kimi()
    print("\nDone.")
