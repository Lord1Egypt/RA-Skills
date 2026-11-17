#!/usr/bin/env python3
"""Synthetic, reproducible onboarding workflow; does not call an AI engine."""
import argparse
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from _contract import load, minimal_env, write
from _sql import compile_single


def run(script, *args):
    command = [sys.executable, str(SCRIPTS / script), *map(str, args)]
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8",
                            env=minimal_env())
    if result.returncode:
        raise RuntimeError(f"{script}: {result.stdout}\n{result.stderr}")
    print("PASS " + script)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = Path(args.out).resolve()
    if out.exists() and any(out.iterdir()):
        ap.error("output must be new or empty")
    out.mkdir(parents=True, exist_ok=True)
    db = out / "source.db"
    conn = sqlite3.connect(db)
    conn.executescript((HERE / "source.sql").read_text(encoding="utf-8"))
    conn.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?,?)", [
        ("t1", 1, 10, 100, "paid", "2026-08-01", "2026-08-03"),
        ("t1", 2, 20, 200, "paid", "2026-08-02", "2026-08-04")])
    conn.executemany("INSERT INTO customers VALUES (?,?,?)", [("t1", 10, "east"), ("t1", 20, "west")])
    conn.executemany("INSERT INTO items VALUES (?,?,?)", [(1, "t1", 1), (2, "t1", 1), (3, "t1", 2)])
    conn.commit()
    session = out / "session.json"
    run("guide_model.py", "init", "--model", HERE / "partial.yaml", "--scope", HERE / "scope.yaml", "--session", session)
    state, examples = load(session), load(HERE / "decisions.yaml")
    answers = {"session_revision": state["revision"], "decisions": []}
    for gap in state["gaps"]:
        supplied = examples[gap["object"] + "/" + gap["property"]]
        answers["decisions"].append({"gap_id": gap["id"], "state": "confirmed", **supplied})
    write(out / "answers.json", answers)
    run("guide_model.py", "propose", "--session", session, "--answers", out / "answers.json", "--patch", out / "review-patch.json")
    run("guide_model.py", "apply", "--session", session, "--patch", out / "review-patch.json")
    run("guide_model.py", "export", "--session", session, "--out", out / "draft")
    model_path = out / "draft" / "semantic.yaml"
    model = load(model_path)
    run("check_model.py", "-f", model_path)
    run("check_join_graph.py", "--model", model_path, "--db", db, "--out", out / "joins.json")
    run("check_constraints.py", "--model", model_path, "--db", db, "--out", out / "constraints.json")
    metric = model["metrics"][0]
    sql, error = compile_single(metric, model["datasets"][0])
    if error:
        raise ValueError(error)
    value = conn.execute(sql).fetchone()[0]
    conn.close()
    write(out / "actual.json", [{"id": "D01", "value": value}, {"id": "D02", "refused": True}])
    run("run_eval.py", "--gold", HERE / "cases.json", "--actual", out / "actual.json", "--model", model_path,
        "--db", db, "--mode", "mock", "--report", out / "evaluation.json")
    run("release_gate.py", "--model", model_path, "--cases", HERE / "cases.json", "--db", db,
        "--session", session, "--eval-report", out / "evaluation.json", "--profile", "validated",
        "--log", out / "release-log.yaml", "--out", out / "gate.json")
    run("visualize_model.py", "--model", model_path, "--session", session, "--report", out / "joins.json",
        "--report", out / "constraints.json", "--report", out / "gate.json", "--out", out / "model.html")
    run("export_exchange.py", "--model", model_path, "--cases", HERE / "cases.json", "--session", session,
        "--report", out / "gate.json", "--visualization", out / "model.html", "--out", out / "exchange")
    print(f"Synthetic workflow complete: {out}\nMode=mock; refusal is simulated; no production engine tested.")


if __name__ == "__main__":
    main()
