"""
maintenance_orchestrator.py — 统一维护编排器

按 DAG 拓扑顺序执行所有维护脚本。
替代 heartbeat.py 的碎片化 subprocess 调用。

Phase 1: topological_sort() → cycle_filter() → subprocess x N
Phase 2: aggregate results → task_report() into system_health.json
Phase 3: compute_health_score() + detect anomalies
Phase 4: write alerts if anomalies detected

用法:
    python scripts/maintenance_orchestrator.py --cycle light
    python scripts/maintenance_orchestrator.py --cycle heavy
    python scripts/maintenance_orchestrator.py --cycle weekly
    python scripts/maintenance_orchestrator.py --dry-run
    python scripts/maintenance_orchestrator.py --cycle light --timeout 120
"""

import argparse
import json
import subprocess
import sys
import time
import platform
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

# Windows: suppress console popups from subprocess
_WIN_HIDE = {}
if platform.system() == "Windows":
    _WIN_HIDE = {"creationflags": subprocess.CREATE_NO_WINDOW}

# ── Paths ──────────────────────────────────────────────────────────
SCRIPTS_DIR = Path(__file__).resolve().parent
WORKSPACE   = SCRIPTS_DIR.parent
HEALTH_FILE = WORKSPACE / "data" / "system_health.json"
ALERTS_FILE = WORKSPACE / "data" / "alerts.json"

# ── System health import ───────────────────────────────────────────
sys.path.insert(0, str(SCRIPTS_DIR))
from system_health import task_report, load_health, save_health, compute_health_score


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  TASK DAG                                                         ║
# ╚═════════════════════════════════════════════════════════════════════╝

TASK_DAG = {
    "vault_guardian": {
        "requires": [],
        "cycle": "light",
        "timeout": 30,
    },
    "vault_maintainer": {
        "requires": [],
        "cycle": "light",
        "timeout": 15,
    },
        "vault_to_qdrant_sync": {
        "requires": [],
        "cycle": "light",
        "script": "vault_to_qdrant.py",
        "timeout": 120,
    },
    "sync_vault_memory": {
        "requires": ["vault_guardian"],
        "cycle": "light",
        "timeout": 10,
    },
    "process_inbox": {
        "requires": [],
        "cycle": "light",
        "timeout": 60,
    },
    "auto_link_vault": {
        "requires": [],
        "cycle": "light",
        "timeout": 15,
    },
    "context_snapshot": {
        "requires": [],
        "cycle": "light",
        "timeout": 30,
    },
    "lmstudio_guardian": {
        "requires": [],
        "cycle": "light",
        "timeout": 30,
    },
    "system_snapshot": {
        "requires": [],
        "cycle": "light",
        "timeout": 15,
    },
    "memory_health": {
        "requires": [],
        "cycle": "light",
        "timeout": 30,
    },
    "extract_memories": {
        "requires": [],
        "cycle": "light",
        "timeout": 120,
    },
    "smoke_test": {
        "requires": [],
        "cycle": "light",
        "timeout": 30,
    },
    "heartbeat_alert": {
        "requires": [],
        "cycle": "light",
        "timeout": 30,
    },
    "health_scoreboard": {
        "requires": [],
        "cycle": "light",
        "timeout": 15,
    },
    "health_check_v2": {
        "requires": [],
        "cycle": "light",
        "timeout": 60,
    },
    # ── Heavy ──
    "build_project_profile": {
        "requires": [],
        "cycle": "heavy",
        "timeout": 60,
    },
    "sync_skills": {
        "requires": [],
        "cycle": "heavy",
        "script": "sync_skills_to_memory.py",
        "timeout": 30,
    },
    "vault_to_qdrant": {
        "requires": [],
        "cycle": "heavy",
        "timeout": 300,
    },
    "elevate_frequent": {
        "requires": ["vault_to_qdrant"],
        "cycle": "heavy",
        "timeout": 120,
    },
    "extract_memories_full": {
        "requires": [],
        "cycle": "heavy",
        "script": "extract_memories.py",
        "args": ["--full"],
        "timeout": 300,
    },
    "build_project_profile": {
        "requires": ["vault_to_qdrant"],
        "cycle": "heavy",
        "timeout": 30,
    },
    "session_cleaner_heavy": {
        "requires": [],
        "cycle": "heavy",
        "script": "session_cleaner.py",
        "args": ["--keep", "14", "--execute"],
        "timeout": 120,
    },
    # ── Compress pipeline → moved to standalone cron (compress-pipeline) ──
    # ── Weekly ──
    "session_cleanup": {
        "requires": [],
        "cycle": "weekly",
        "script": "session_cleaner.py",
        "timeout": 60,
    },
}


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  TOPOLOGICAL SORT (Kahn's algorithm)                              ║
# ╚═════════════════════════════════════════════════════════════════════╝

def topological_sort(dag: dict, cycle: str) -> list:
    """Return ordered list of task names for the given cycle."""
    cycle_tasks = {name: info for name, info in dag.items()
                   if info["cycle"] == cycle}

    # Build dependency graph (only within this cycle)
    in_degree = {name: 0 for name in cycle_tasks}
    adj = defaultdict(list)

    for name, info in cycle_tasks.items():
        for dep in info.get("requires", []):
            if dep in cycle_tasks:
                adj[dep].append(name)
                in_degree[name] += 1

    # Kahn's algorithm
    queue = deque([n for n, d in in_degree.items() if d == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Any leftover tasks have circular deps — add them at end
    leftover = [n for n in cycle_tasks if n not in result]
    result.extend(leftover)

    return result


def topological_levels(dag: dict, cycle: str) -> list:
    """Return list of lists: tasks at the same level have no mutual
    dependencies and can execute in parallel."""
    cycle_tasks = {name: info for name, info in dag.items()
                   if info["cycle"] == cycle}

    in_degree = {}
    for name, info in cycle_tasks.items():
        deps = [d for d in info.get("requires", []) if d in cycle_tasks]
        in_degree[name] = len(deps)

    levels = []
    remaining = dict(in_degree)

    while remaining:
        current = [n for n, d in remaining.items() if d == 0]
        if not current:
            # Circular dependency — add leftovers and break
            levels.append(list(remaining.keys()))
            break
        levels.append(current)
        for name in current:
            del remaining[name]
        # Decrement in-degree for tasks that depend on completed tasks
        for name in list(remaining.keys()):
            info = cycle_tasks[name]
            done_deps = [d for d in info.get("requires", []) if d not in remaining]
            remaining[name] = max(0, len([d for d in info.get("requires", []) if d in cycle_tasks]) - len(done_deps))

    return levels


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  EXECUTION                                                        ║
# ╚═════════════════════════════════════════════════════════════════════╝

def run_task(name: str, info: dict, default_timeout: int,
             dry_run: bool = False) -> dict:
    """Execute a single task. Returns result dict."""
    script_name = info.get("script", f"{name}.py")
    script_path = SCRIPTS_DIR / script_name
    timeout = info.get("timeout", default_timeout)
    args = info.get("args", [])

    cmd = ["python", str(script_path)] + args

    if dry_run:
        print(f"  [DRY] {name}: {' '.join(cmd)}")
        return {
            "name": name,
            "status": "ok",
            "duration_ms": 0,
            "exit_code": 0,
            "dry": True,
        }

    print(f"  [{name}] ", end="", flush=True)
    t0 = time.time()

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=timeout,
            cwd=str(SCRIPTS_DIR),
            **_WIN_HIDE,
        )
        duration_ms = int((time.time() - t0) * 1000)
        exit_code = result.returncode

        if exit_code == 0:
            # Check for silent success: exit 0 but stderr has content
            stderr_text = result.stderr.decode("utf-8", errors="replace").strip()
            stdout_text = result.stdout.decode("utf-8", errors="replace").strip()

            warnings = []
            if stderr_text and any(
                w in stderr_text.lower()
                for w in ["warning", "error", "fail", "traceback", "except"]
            ):
                warnings.append(f"stderr: {stderr_text[:100]}")
                status = "warning"
            elif not stdout_text and name not in {"session_cleanup"}:
                # Silent: no output at all (may not have done work)
                warnings.append("no output (possible silent skip)")
                status = "warning"
            else:
                status = "ok"

            print(f"OK ({duration_ms}ms)")
        else:
            err = result.stderr.decode("utf-8", errors="replace")[-150:]
            print(f"FAIL (exit {exit_code}): {err[:80]}")
            status = "error"

        task_report(
            name,
            status=status,
            duration_ms=duration_ms,
            error=(result.stderr.decode("utf-8", errors="replace")[-200:]
                    if exit_code != 0 else None),
            warnings=warnings if exit_code == 0 else [],
            metrics={"exit_code": exit_code},
        )

        return {
            "name": name,
            "status": status,
            "duration_ms": duration_ms,
            "exit_code": exit_code,
            "warnings": warnings if exit_code == 0 else [],
            "error": (result.stderr.decode("utf-8", errors="replace")[-200:]
                      if exit_code != 0 else None),
        }

    except subprocess.TimeoutExpired:
        duration_ms = int((time.time() - t0) * 1000)
        print(f"TIMEOUT ({timeout}s)")
        task_report(name, status="error", duration_ms=duration_ms,
                     error=f"Timeout after {timeout}s")
        return {
            "name": name,
            "status": "error",
            "duration_ms": duration_ms,
            "exit_code": -1,
            "error": f"Timeout after {timeout}s",
        }

    except Exception as e:
        duration_ms = int((time.time() - t0) * 1000)
        print(f"ERROR: {e}")
        task_report(name, status="error", duration_ms=duration_ms,
                     error=str(e))
        return {
            "name": name,
            "status": "error",
            "duration_ms": duration_ms,
            "exit_code": -2,
            "error": str(e),
        }


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  ANOMALY DETECTION + ALERTS                                        ║
# ╚═════════════════════════════════════════════════════════════════════╝

def detect_anomalies(results: list) -> list:
    """Detect anomalies from execution results."""
    alerts = []

    for r in results:
        name = r["name"]

        # Consecutive failures (check from health)
        from system_health import get_task_status
        task = get_task_status(name)
        if task and task.get("consecutive_failures", 0) >= 3:
            alerts.append({
                "id": f"consec-fail-{name}-{datetime.now().strftime('%Y%m%d')}",
                "level": "critical",
                "title": f"{name} failed {task['consecutive_failures']} times in a row",
                "component": name,
                "detected_at": datetime.now(timezone.utc).isoformat(),
                "status": "active",
                "resolved_at": None,
            })

        # Silent script: exit 0 but warnings or empty output
        if r.get("warnings"):
            alerts.append({
                "id": f"silent-{name}-{datetime.now().strftime('%Y%m%d%H%M')}",
                "level": "warning",
                "title": f"{name}: silent issue detected",
                "component": name,
                "detail": "; ".join(r["warnings"]),
                "detected_at": datetime.now(timezone.utc).isoformat(),
                "status": "active",
                "resolved_at": None,
            })

    return alerts


def write_alerts(alerts: list):
    """Write alerts to data/alerts.json."""
    existing = []
    if ALERTS_FILE.exists():
        try:
            with open(ALERTS_FILE, "r", encoding="utf-8") as f:
                existing = json.load(f).get("active", [])
        except (json.JSONDecodeError, UnicodeDecodeError):
            existing = []

    # Merge: keep existing alerts not superseded by new ones
    new_ids = {a["id"] for a in alerts}
    merged = [a for a in existing if a["id"] not in new_ids] + alerts

    # Limit to 20 active alerts
    merged = merged[-20:]

    has_critical = any(a.get("level") == "critical" for a in merged)

    payload = {
        "active": merged,
        "has_active_critical": has_critical,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    ALERTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = ALERTS_FILE.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    tmp.replace(ALERTS_FILE)


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  MAIN                                                             ║
# ╚═════════════════════════════════════════════════════════════════════╝

def main():
    parser = argparse.ArgumentParser(
        description="maintenance_orchestrator.py — unified task scheduler"
    )
    parser.add_argument("--cycle", choices=["light", "heavy", "weekly"],
                        default="light", help="Maintenance cycle")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview without executing")
    parser.add_argument("--timeout", type=int, default=60,
                        help="Default per-task timeout in seconds")
    parser.add_argument("--no-topological", action="store_true",
                        help="Skip topological sort, run in DAG order")
    parser.add_argument("--parallel", action="store_true",
                        help="Run independent tasks (same DAG level) in parallel")
    opts = parser.parse_args()

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
          f"orchestrator --cycle={opts.cycle}")

    # Get ordered task list
    if opts.no_topological:
        ordered = [n for n, i in TASK_DAG.items() if i["cycle"] == opts.cycle]
    else:
        ordered = topological_sort(TASK_DAG, opts.cycle)

    print(f"  Cycle: {opts.cycle}, Tasks: {len(ordered)}")
    if ordered:
        mode = "parallel" if opts.parallel else "sequential"
        print(f"  Mode: {mode}")
        print(f"  Order: {' → '.join(ordered)}")

    # Execute
    results = []
    ok = fail = warn = 0

    if opts.parallel:
        levels = topological_levels(TASK_DAG, opts.cycle)
        for li, level in enumerate(levels):
            if len(level) > 1:
                print(f"  Level {li}: {' | '.join(level)} (parallel)")
            with ThreadPoolExecutor(max_workers=len(level)) as executor:
                futures = {
                    executor.submit(
                        run_task, name, TASK_DAG[name], opts.timeout, opts.dry_run
                    ): name
                    for name in level
                }
                for future in as_completed(futures):
                    result = future.result()
                    results.append(result)
                    status = result["status"]
                    if status == "ok":
                        ok += 1
                    elif status == "warning":
                        warn += 1
                    else:
                        fail += 1
    else:
        for name in ordered:
            info = TASK_DAG[name]
            result = run_task(name, info, opts.timeout, dry_run=opts.dry_run)

            if result.get("dry"):
                results.append(result)
                continue

            results.append(result)
            status = result["status"]
            if status == "ok":
                ok += 1
            elif status == "warning":
                warn += 1
            else:
                fail += 1
                # AI Harness: fault isolation — don't block subsequent tasks

    # Summary
    print(f"\n  Results: {ok} OK, {warn} WARN, {fail} FAIL")

    # Phase 3: Detect anomalies
    if not opts.dry_run:
        alerts = detect_anomalies(results)
        if alerts:
            print(f"  Alerts: {len(alerts)} new")
            for a in alerts:
                print(f"    [{a['level'].upper()}] {a['title']}")
            write_alerts(alerts)

    # Phase 4: Update health score
    if not opts.dry_run:
        health_data = load_health()
        health_data["cycle"] = opts.cycle
        health_data["previous_health_score"] = health_data.get(
            "system_health_score", 100
        )
        health_data["system_health_score"] = compute_health_score(health_data)
        save_health(health_data)

    # Return summary line (for LLM consumption via cron)
    from system_health import get_alert_summary
    summary = get_alert_summary()
    print(f"\n  {summary}")

    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
