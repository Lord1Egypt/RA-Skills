#!/usr/bin/env python3
"""
CodeGraph Assistant — 一键包装器 for npm codegraph.
Usage:
    python codegraph_assist.py setup [path]
    python codegraph_assist.py ask "<question>"
    python codegraph_assist.py query "<symbol>"
    python codegraph_assist.py affected <file>
    python codegraph_assist.py inject [path]
    python codegraph_assist.py status [path]
"""

import argparse, json, os, subprocess, sys
from pathlib import Path

CODEGRAPH_BIN = str(Path.home() / "AppData" / "Roaming" / "npm" / "codegraph.cmd")
MEMORY_FILE = "MEMORY.md"


def run_cg(args, cwd=None, timeout=120):
    """Run codegraph command, return (stdout, stderr, returncode)."""
    r = subprocess.run(
        [CODEGRAPH_BIN] + args, cwd=cwd,
        capture_output=True, text=True, timeout=timeout
    )
    return r.stdout, r.stderr, r.returncode


def cmd_setup(path=None):
    cwd = path or os.getcwd()
    print(f"Setting up CodeGraph in {cwd}")
    out, err, rc = run_cg(["init"], cwd=cwd)
    print(out)
    if "already initialized" not in out:
        out2, err2, rc2 = run_cg(["index"], cwd=cwd, timeout=300)
        print(out2)
    print("Done. Ready to use.")


def cmd_ask(question, path=None):
    cwd = path or os.getcwd()
    # Sanitize question to single word slug for codegraph
    slug = question.strip().replace(" ", "-").replace('"', '')[:50]
    out, err, rc = run_cg(["context", slug, "-n", "15"], cwd=cwd)
    print(out if out else f"No context found for '{slug}'")


def cmd_query(symbol, path=None, json_out=False):
    cwd = path or os.getcwd()
    args = ["query", symbol, "--limit", "10"]
    if json_out:
        args.append("-j")
    out, err, rc = run_cg(args, cwd=cwd)
    print(out)


def cmd_affected(filepath, path=None):
    cwd = path or os.getcwd()
    out, err, rc = run_cg(["affected", filepath, "-q"], cwd=cwd)
    if out.strip():
        print(f"Affected files:\n{out}")
    else:
        print("No test files affected (or no test files found).")


def cmd_inject(path=None):
    cwd = Path(path or os.getcwd()).resolve()
    out, err, rc = run_cg(["status"], cwd=str(cwd))
    out2, err2, rc2 = run_cg(["files", "--max-depth", "2"], cwd=str(cwd))

    summary = f"\n## CodeGraph: {cwd.name}\n"
    summary += f"_Auto-generated via codegraph-assistant_\n\n"
    summary += out + "\n### File Structure\n" + out2

    memory_path = cwd / MEMORY_FILE
    existing = memory_path.read_text(encoding="utf-8", errors="replace") if memory_path.exists() else ""
    marker = "## CodeGraph:"
    if marker in existing:
        lines = existing.splitlines()
        new_lines, skip = [], False
        for line in lines:
            if line.startswith(marker): skip = True; continue
            if skip and line.startswith("## "): skip = False; new_lines.append(line); continue
            if not skip: new_lines.append(line)
        existing = "\n".join(new_lines).rstrip() + "\n"
    memory_path.write_text(existing.rstrip() + "\n" + summary, encoding="utf-8")
    print(f"Injected summary into {memory_path}")


def cmd_status(path=None):
    cwd = path or os.getcwd()
    out, err, rc = run_cg(["status"], cwd=cwd)
    print(out)


def main():
    parser = argparse.ArgumentParser(description="CodeGraph Assistant")
    sub = parser.add_subparsers(dest="cmd")

    p_setup = sub.add_parser("setup", help="init + index project")
    p_setup.add_argument("path", nargs="?", help="Project path")

    p_ask = sub.add_parser("ask", help="Generate task context")
    p_ask.add_argument("question", help="Task description")
    p_ask.add_argument("path", nargs="?", help="Project path")

    p_query = sub.add_parser("query", help="Search symbols")
    p_query.add_argument("symbol", help="Symbol name")
    p_query.add_argument("-j", "--json", action="store_true", help="JSON output")
    p_query.add_argument("path", nargs="?", help="Project path")

    p_aff = sub.add_parser("affected", help="Impact analysis")
    p_aff.add_argument("file", help="File path")
    p_aff.add_argument("path", nargs="?", help="Project path")

    p_inj = sub.add_parser("inject", help="Inject summary into MEMORY.md")
    p_inj.add_argument("path", nargs="?", help="Project path")

    p_stat = sub.add_parser("status", help="Index statistics")
    p_stat.add_argument("path", nargs="?", help="Project path")

    args = parser.parse_args()

    if args.cmd == "setup":
        cmd_setup(getattr(args, 'path', None))
    elif args.cmd == "ask":
        cmd_ask(args.question, getattr(args, 'path', None))
    elif args.cmd == "query":
        cmd_query(args.symbol, getattr(args, 'path', None), getattr(args, 'json', False))
    elif args.cmd == "affected":
        cmd_affected(args.file, getattr(args, 'path', None))
    elif args.cmd == "inject":
        cmd_inject(getattr(args, 'path', None))
    elif args.cmd == "status":
        cmd_status(getattr(args, 'path', None))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
