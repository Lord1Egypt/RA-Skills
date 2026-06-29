"""
system_health.py — 中央健康状态接口

所有维护脚本通过 task_report() 写入统一状态文件。
不依赖 OpenClaw 内部模块，纯 Python + JSON。

用法:
    from system_health import task_report, load_health, compute_health_score
    task_report("vault_guardian", status="ok", duration_ms=3200)
"""

import json
import os
import time
from pathlib import Path
from datetime import datetime, timezone


# ── Paths ──────────────────────────────────────────────────────────
WORKSPACE = Path(__file__).resolve().parent.parent
HEALTH_FILE = WORKSPACE / "data" / "system_health.json"

# ── Default health template ────────────────────────────────────────
DEFAULT_HEALTH = {
    "updated_at": "",
    "cycle": "",
    "orchestrator_version": "1.0",
    "tasks": {},
    "system_health_score": 100,
    "previous_health_score": 100,
}


def _atomic_write(path: Path, data: dict):
    """Atomic write via temp file + rename, with retry on Windows lock contention."""
    import random, uuid
    path.parent.mkdir(parents=True, exist_ok=True)
    # 用 uuid 避免并行时 PID 不够唯一
    tmp = path.with_suffix(f".tmp.{os.getpid()}.{uuid.uuid4().hex[:6]}")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    for attempt in range(10):  # 更多重试
        try:
            tmp.replace(path)
            return
        except (OSError, PermissionError) as e:
            if attempt < 9:
                time.sleep(random.uniform(0.1, 0.5))
                # 如果 tmp 被删了，重新写
                if not tmp.exists():
                    with open(tmp, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
            else:
                # 最后尝试直接覆盖
                try:
                    with open(path, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    return
                except:
                    raise e


def load_health() -> dict:
    """Load system_health.json, return default if missing or corrupt."""
    if not HEALTH_FILE.exists():
        return dict(DEFAULT_HEALTH)
    try:
        with open(HEALTH_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Ensure all default keys exist
        for k, v in DEFAULT_HEALTH.items():
            data.setdefault(k, v)
        return data
    except (json.JSONDecodeError, UnicodeDecodeError, OSError):
        return dict(DEFAULT_HEALTH)


def save_health(data: dict):
    """Save to system_health.json atomically."""
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    _atomic_write(HEALTH_FILE, data)


def task_report(name: str, status: str = "ok", duration_ms: int = 0,
                error: str = None, warnings: list = None,
                metrics: dict = None):
    """
    Report a task execution result. Called at the end of each script.

    Args:
        name: Task identifier (e.g. "vault_guardian")
        status: "ok", "warning", or "error"
        duration_ms: Execution time in milliseconds
        error: Error message if status is "error"
        warnings: List of warning strings
        metrics: Arbitrary key-value metrics (e.g. {"points_synced": 72})
    """
    data = load_health()
    tasks = data.setdefault("tasks", {})

    now_iso = datetime.now(timezone.utc).isoformat()
    prev = tasks.get(name, {})

    # Track consecutive failures/warnings
    consec_fail = prev.get("consecutive_failures", 0)
    consec_warn = prev.get("consecutive_warnings", 0)

    if status == "error":
        consec_fail += 1
        consec_warn = 0
    elif status == "warning":
        consec_fail = 0
        consec_warn += 1
    else:  # ok
        consec_fail = 0
        consec_warn = 0

    entry = {
        "last_run": now_iso,
        "last_status": status,
        "last_duration_ms": duration_ms,
        "last_error": error,
        "last_warnings": warnings or [],
        "last_metrics": metrics or {},
        "consecutive_failures": consec_fail,
        "consecutive_warnings": consec_warn,
        "total_runs": prev.get("total_runs", 0) + 1,
        "total_failures": prev.get("total_failures", 0) + (1 if status == "error" else 0),
        "total_warnings": prev.get("total_warnings", 0) + (1 if status == "warning" else 0),
    }
    tasks[name] = entry

    # Recompute health score
    data["system_health_score"] = compute_health_score(data)

    save_health(data)


def compute_health_score(data: dict) -> int:
    """
    Compute overall health score 0-100.

    Deductions:
      - Each task in error state: -15
      - Each task in warning state: -5
      - Each task with consecutive_failures >= 3: -10
      - Each task not run in > 2h (stale): -5
    """
    tasks = data.get("tasks", {})
    if not tasks:
        return 100

    score = 100
    now = time.time()
    stale_threshold = 8 * 3600  # 8 hours (reasonable for cron-scheduled tasks)

    for name, t in tasks.items():
        status = t.get("last_status", "ok")
        if status == "error":
            score -= 15
        elif status == "warning":
            score -= 5

        if t.get("consecutive_failures", 0) >= 3:
            score -= 10

        # Staleness check
        last_run_str = t.get("last_run", "")
        if last_run_str:
            try:
                last_dt = datetime.fromisoformat(last_run_str)
                age_sec = (now - last_dt.replace(tzinfo=None).timestamp())
                if age_sec > stale_threshold:
                    score -= 5
            except (ValueError, OSError):
                pass

    return max(0, min(100, score))


def get_task_status(name: str) -> dict | None:
    """Get a single task's status entry."""
    data = load_health()
    return data.get("tasks", {}).get(name)


def get_alert_summary() -> str:
    """Return a 1-line summary of current health state."""
    data = load_health()
    tasks = data.get("tasks", {})
    errors = [n for n, t in tasks.items() if t.get("last_status") == "error"]
    warnings = [n for n, t in tasks.items() if t.get("last_status") == "warning"]
    stale = []
    now = time.time()
    for n, t in tasks.items():
        last_run_str = t.get("last_run", "")
        if last_run_str:
            try:
                last_dt = datetime.fromisoformat(last_run_str)
                age = (now - last_dt.replace(tzinfo=None).timestamp()) / 3600
                if age > 2:
                    stale.append(f"{n}({age:.0f}h)")
            except (ValueError, OSError):
                pass

    parts = [f"Health: {data.get('system_health_score', '?')}/100"]
    if errors:
        parts.append(f"ERRORS: {', '.join(errors)}")
    if warnings:
        parts.append(f"WARNINGS: {', '.join(warnings)}")
    if stale:
        parts.append(f"STALE: {', '.join(stale)}")
    if not errors and not warnings and not stale:
        parts.append("All OK")

    return " | ".join(parts)


# ── Self-test ──────────────────────────────────────────────────────
if __name__ == "__main__":
    print("system_health.py self-test")
    print(f"  Health file: {HEALTH_FILE}")

    # Test: report a task
    task_report("test_script", status="ok", duration_ms=1234,
                metrics={"items": 42})
    print(f"  Wrote test entry to {HEALTH_FILE}")

    # Test: read back
    data = load_health()
    t = data["tasks"].get("test_script", {})
    print(f"  Read back: status={t.get('last_status')}, "
          f"runs={t.get('total_runs')}, score={data['system_health_score']}")

    # Test: summary
    print(f"  Summary: {get_alert_summary()}")

    # Clean up test entry
    data["tasks"].pop("test_script", None)
    save_health(data)
    print("  Cleaned up test entry. OK.")
