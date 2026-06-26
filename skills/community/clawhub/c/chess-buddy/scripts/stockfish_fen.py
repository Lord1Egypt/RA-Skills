#!/usr/bin/env python3
"""Small MIT-0 Stockfish UCI helper for FEN analysis.

This helper intentionally avoids chess libraries. It asks Stockfish to validate
and analyze a FEN via the UCI protocol, then returns JSON with best lines in UCI
notation. The assistant should translate the lines into human explanation.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from typing import Any

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def locate_engine(explicit: str | None = None) -> str | None:
    candidates = [explicit, os.environ.get("STOCKFISH_PATH"), "stockfish"]
    for candidate in candidates:
        if not candidate:
            continue
        path = shutil.which(candidate) if os.path.basename(candidate) == candidate else candidate
        if path and os.path.exists(path):
            return path
    return None


def run_stockfish(engine: str, commands: list[str], timeout: float = 20.0) -> list[str]:
    proc = subprocess.Popen(
        [engine],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )
    assert proc.stdin is not None and proc.stdout is not None
    out: list[str] = []
    for command in commands:
        proc.stdin.write(command + "\n")
        proc.stdin.flush()
        if command.startswith("go "):
            for line in proc.stdout:
                line = line.rstrip("\n")
                out.append(line)
                if line.startswith("bestmove "):
                    break
    proc.stdin.write("quit\n")
    proc.stdin.flush()
    try:
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        raise
    return out


def parse_score(tokens: list[str]) -> dict[str, Any] | None:
    if "score" not in tokens:
        return None
    i = tokens.index("score")
    if i + 2 >= len(tokens):
        return None
    kind, value = tokens[i + 1], tokens[i + 2]
    if kind == "cp":
        cp = int(value)
        return {"type": "cp", "cp_side_to_move": cp, "pawns_side_to_move": round(cp / 100, 2)}
    if kind == "mate":
        return {"type": "mate", "mate_in": int(value)}
    return {"type": kind, "value": value}


def parse_analysis(lines: list[str]) -> list[dict[str, Any]]:
    latest: dict[int, dict[str, Any]] = {}
    for line in lines:
        if not line.startswith("info "):
            continue
        tokens = line.split()
        if "pv" not in tokens:
            continue
        multipv = 1
        if "multipv" in tokens:
            try:
                multipv = int(tokens[tokens.index("multipv") + 1])
            except Exception:
                multipv = 1
        pv_idx = tokens.index("pv")
        pv = tokens[pv_idx + 1 :]
        depth = None
        if "depth" in tokens:
            try:
                depth = int(tokens[tokens.index("depth") + 1])
            except Exception:
                pass
        latest[multipv] = {
            "multipv": multipv,
            "depth": depth,
            "score": parse_score(tokens),
            "move_uci": pv[0] if pv else None,
            "pv_uci": pv,
        }
    return [latest[k] for k in sorted(latest)]


def cmd_engine_check(args: argparse.Namespace) -> int:
    engine = locate_engine(args.engine)
    if not engine:
        print(json.dumps({"ok": False, "error": "stockfish not found", "install": "Install stockfish or set STOCKFISH_PATH."}, indent=2))
        return 3
    lines = run_stockfish(engine, ["uci", "isready", f"position fen {STARTING_FEN}", "go depth 1"])
    print(json.dumps({"ok": True, "engine": engine, "name": os.path.basename(engine), "lines": parse_analysis(lines)}, indent=2))
    return 0


def cmd_analyze(args: argparse.Namespace) -> int:
    engine = locate_engine(args.engine)
    if not engine:
        print(json.dumps({"ok": False, "error": "stockfish not found", "install": "Install stockfish or set STOCKFISH_PATH."}, indent=2))
        return 3
    commands = [
        "uci",
        "isready",
        f"setoption name MultiPV value {args.multipv}",
        f"position fen {args.fen}",
    ]
    commands.append(f"go depth {args.depth}" if args.depth else f"go movetime {int(args.limit * 1000)}")
    lines = run_stockfish(engine, commands, timeout=max(20.0, args.limit + 10.0))
    analysis = parse_analysis(lines)
    print(json.dumps({"ok": True, "engine": engine, "fen": args.fen, "lines": analysis}, indent=2))
    return 0 if analysis else 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("engine-check")
    p.add_argument("--engine")
    p.set_defaults(func=cmd_engine_check)
    p = sub.add_parser("analyze")
    p.add_argument("--fen", required=True)
    p.add_argument("--engine")
    p.add_argument("--multipv", type=int, default=3)
    p.add_argument("--limit", type=float, default=1.0)
    p.add_argument("--depth", type=int)
    p.set_defaults(func=cmd_analyze)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
