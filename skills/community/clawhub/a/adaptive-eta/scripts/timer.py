#!/usr/bin/env python3
"""adaptive-eta timer: track a promised ETA, flag overruns, learn from history.

Commands:
  start   --eta SEC [--label TEXT] [--task ID]   begin tracking, print calibration hint
  revise  --eta SEC [--reason TEXT] [--task ID]  new *remaining* time; keeps start + initial ETA
  check   [--task ID]                            STATUS line + numbers
  stop    [--outcome done|aborted] [--task ID]   log to history, print time report
  calibrate                                      summarize estimate accuracy

State lives in $ADAPTIVE_ETA_HOME (default ~/.adaptive-eta), never in the skill dir.
Stdlib only, Python 3.8+.
"""
import argparse
import json
import os
import statistics
import sys
import time
from pathlib import Path

HOME = Path(os.environ.get("ADAPTIVE_ETA_HOME", Path.home() / ".adaptive-eta"))
STATE_DIR = HOME / "state"
HISTORY = HOME / "history.jsonl"

THRESHOLD_RATIO = 0.8   # warn when 80% of the current deadline is used
OVERRUN_FACTOR = 3.0    # ask the user when elapsed > 3x the initial ETA
STALE_AFTER = 6 * 3600  # a timer untouched this long is treated as abandoned
AMEND_WINDOW = 60       # a revise this soon after start replaces the initial ETA
CALIBRATION_MIN_N = 3
CALIBRATION_WINDOW = 20


def fmt(sec: float) -> str:
    sec = int(round(max(sec, 0)))
    if sec < 60:
        return f"{sec}s"
    m, s = divmod(sec, 60)
    if m < 60:
        return f"{m}m{s:02d}s" if s else f"{m}m"
    h, m = divmod(m, 60)
    return f"{h}h{m:02d}m"


def state_path(task: str) -> Path:
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in task) or "default"
    return STATE_DIR / f"{safe}.json"


def load(task: str):
    p = state_path(task)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except (OSError, json.JSONDecodeError):
        return None


def save(task: str, state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    p = state_path(task)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(state))
    os.replace(tmp, p)


def is_stale(state: dict, now: float) -> bool:
    return now - state.get("updated_at", state["start_time"]) > STALE_AFTER


def log_history(entry: dict) -> None:
    HOME.mkdir(parents=True, exist_ok=True)
    with HISTORY.open("a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def read_ratios():
    if not HISTORY.exists():
        return []
    ratios = []
    for line in HISTORY.read_text().splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if e.get("outcome") == "done" and e.get("initial_eta", 0) > 0:
            ratios.append(e["actual"] / e["initial_eta"])
    return ratios[-CALIBRATION_WINDOW:]


def calibration_factor():
    ratios = read_ratios()
    if len(ratios) < CALIBRATION_MIN_N:
        return None, len(ratios)
    return statistics.median(ratios), len(ratios)


def close(task: str, state: dict, outcome: str, now: float) -> dict:
    actual = now - state["start_time"]
    entry = {
        "label": state.get("label", ""),
        "initial_eta": state["initial_eta"],
        "final_eta": round(state["deadline"] - state["start_time"], 1),
        "actual": round(actual, 1),
        "revisions": state.get("revisions", 0),
        "outcome": outcome,
        "ended_at": int(now),
    }
    log_history(entry)
    try:
        state_path(task).unlink()
    except OSError:
        pass
    return entry


def cmd_start(a) -> int:
    if a.eta <= 0:
        print("ERROR: --eta must be a positive number of seconds")
        return 1
    now = time.time()
    old = load(a.task)
    if old:
        close(a.task, old, "abandoned", now)
        print(f"WARN: replaced an unfinished timer ({old.get('label') or a.task}); logged as abandoned")
    save(a.task, {
        "label": a.label, "start_time": now, "updated_at": now,
        "initial_eta": a.eta, "deadline": now + a.eta, "revisions": 0,
    })
    print(f"STATUS: STARTED  eta={fmt(a.eta)}")
    factor, n = calibration_factor()
    if factor is not None and not 0.8 <= factor <= 1.25:
        suggested = int(round(a.eta * factor))
        print(f"CALIBRATION: recent tasks took {factor:.1f}x their estimate (n={n}). "
              f"Tell the user ~{fmt(suggested)} and run: revise --eta {suggested}")
    return 0


def cmd_revise(a) -> int:
    if a.eta <= 0:
        print("ERROR: --eta must be a positive number of seconds (time REMAINING)")
        return 1
    now = time.time()
    s = load(a.task)
    if not s:
        print("STATUS: NOT_RUNNING  (use start instead)")
        return 0
    elapsed = now - s["start_time"]
    if s.get("revisions", 0) == 0 and elapsed < AMEND_WINDOW:
        # Correcting the first estimate (e.g. after a CALIBRATION hint), not a revision.
        s.update(initial_eta=a.eta, deadline=now + a.eta, updated_at=now)
        save(a.task, s)
        print(f"STATUS: AMENDED  initial_eta={fmt(a.eta)}")
        return 0
    s["deadline"] = now + a.eta
    s["window_start"] = now
    s["updated_at"] = now
    s["revisions"] = s.get("revisions", 0) + 1
    if a.reason:
        s.setdefault("reasons", []).append(a.reason)
    save(a.task, s)
    print(f"STATUS: REVISED  remaining={fmt(a.eta)}  total_so_far={fmt(elapsed)}  "
          f"initial_eta={fmt(s['initial_eta'])}  revisions={s['revisions']}")
    return 0


def cmd_check(a) -> int:
    now = time.time()
    s = load(a.task)
    if not s:
        print("STATUS: NOT_RUNNING")
        return 0
    if is_stale(s, now):
        close(a.task, s, "abandoned", now)
        print("STATUS: STALE  (timer untouched >6h; discarded. start a new one if still working)")
        return 0
    s["updated_at"] = now
    save(a.task, s)

    elapsed = now - s["start_time"]
    window = s["deadline"] - s.get("window_start", s["start_time"])
    remaining = s["deadline"] - now
    initial = s["initial_eta"]

    if elapsed > initial * OVERRUN_FACTOR:
        status, action = "OVERRUN", f"elapsed > {OVERRUN_FACTOR:g}x initial ETA: pause and ask the user whether to continue"
    elif remaining <= 0:
        status, action = "EXPIRED", "re-estimate remaining time, tell the user, then run revise"
    elif remaining <= window * (1 - THRESHOLD_RATIO):
        status, action = "THRESHOLD_REACHED", "if not nearly done: re-estimate, tell the user, run revise"
    else:
        status, action = "ON_TRACK", "continue silently"

    print(f"STATUS: {status}")
    print(f"ELAPSED: {fmt(elapsed)}  REMAINING: {fmt(remaining) if remaining > 0 else '-' + fmt(-remaining)}  "
          f"INITIAL_ETA: {fmt(initial)}  REVISIONS: {s.get('revisions', 0)}")
    print(f"ACTION: {action}")
    return 0


def cmd_stop(a) -> int:
    now = time.time()
    s = load(a.task)
    if not s:
        print("STATUS: NOT_RUNNING  (nothing to stop)")
        return 0
    e = close(a.task, s, a.outcome, now)
    rev = f" · {e['revisions']} revision(s)" if e["revisions"] else ""
    print(f"STATUS: STOPPED  outcome={a.outcome}")
    print(f"REPORT: estimated {fmt(e['initial_eta'])} · actual {fmt(e['actual'])}{rev}")
    return 0


def cmd_calibrate(_a) -> int:
    ratios = read_ratios()
    if len(ratios) < CALIBRATION_MIN_N:
        print(f"CALIBRATION: not enough data (n={len(ratios)}, need {CALIBRATION_MIN_N})")
        return 0
    med = statistics.median(ratios)
    within = sum(0.67 <= r <= 1.5 for r in ratios) / len(ratios)
    print(f"CALIBRATION: median actual/estimate = {med:.2f}x (n={len(ratios)})")
    print(f"ACCURACY: {within:.0%} of tasks finished within 0.67x-1.5x of the estimate")
    if med > 1.25:
        print(f"ADVICE: you underestimate; multiply first estimates by ~{med:.1f}")
    elif med < 0.8:
        print(f"ADVICE: you overestimate; multiply first estimates by ~{med:.1f}")
    else:
        print("ADVICE: estimates are well calibrated")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="adaptive-eta timer")
    sub = p.add_subparsers(dest="cmd", required=True)

    def with_task(sp):
        sp.add_argument("--task", default="default", help="id for parallel timers (default: default)")
        return sp

    sp = with_task(sub.add_parser("start", help="start tracking with an initial ETA"))
    sp.add_argument("--eta", type=int, required=True, help="estimated total seconds")
    sp.add_argument("--label", default="", help="short task description for history")

    sp = with_task(sub.add_parser("revise", help="set new REMAINING seconds, keep initial ETA"))
    sp.add_argument("--eta", type=int, required=True, help="estimated remaining seconds")
    sp.add_argument("--reason", default="", help="why the estimate changed")

    with_task(sub.add_parser("check", help="report status"))

    sp = with_task(sub.add_parser("stop", help="finish, log history, print report"))
    sp.add_argument("--outcome", choices=["done", "aborted"], default="done")

    sub.add_parser("calibrate", help="summarize past estimate accuracy")

    a = p.parse_args()
    handlers = {"start": cmd_start, "revise": cmd_revise, "check": cmd_check,
                "stop": cmd_stop, "calibrate": cmd_calibrate}
    try:
        return handlers[a.cmd](a)
    except OSError as e:
        print(f"ERROR: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
