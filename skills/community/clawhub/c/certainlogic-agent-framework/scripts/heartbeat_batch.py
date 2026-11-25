#!/usr/bin/env python3
"""
Heartbeat Batch — run all critical health checks in one exec call.

Outputs JSON with alerts for every check. Exit 0 if all clear, 1 if alerts.

Usage:
    python3 heartbeat_batch.py
"""
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

NOW = datetime.now(timezone.utc).isoformat()
SCRIPTS = Path(__file__).resolve().parent
WORKSPACE = SCRIPTS.parent.parent  # workspace root


def run(cmd, timeout=10):
    """Run a shell command and return (rc, stdout, stderr)."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", f"Timed out after {timeout}s"
    except Exception as e:
        return -1, "", str(e)


def check_brain():
    """Check Brain API /health endpoint."""
    url = os.environ.get("BRAIN_URL", "http://127.0.0.1:8000")
    rc, out, err = run(["curl", "-s", f"{url}/health"], timeout=5)
    if rc != 0:
        return {"ok": False, "facts_loaded": 0, "error": f"curl failed: {err}"}
    try:
        data = json.loads(out)
        ok = data.get("status") == "ok"
        return {
            "ok": ok,
            "facts_loaded": data.get("facts_loaded", 0),
            "error": None if ok else f"status={data.get('status')}",
        }
    except Exception as e:
        return {"ok": False, "facts_loaded": 0, "error": f"parse failed: {e}"}


def check_git():
    """Check git status for uncommitted files."""
    rc, out, err = run(["git", "status", "--short"], timeout=5)
    if rc != 0:
        return {"uncommitted_files": -1, "alert": True, "error": f"git failed: {err}"}
    count = len([l for l in out.split("\n") if l.strip()])
    return {
        "uncommitted_files": count,
        "alert": count > 20,
        "error": None if count <= 20 else f"{count} uncommitted files",
    }


def check_clawhub_skills():
    """Count installed ClawHub skills."""
    rc, out, err = run(["clawhub", "list"], timeout=10)
    if rc != 0:
        return {"count": -1, "error": f"clawhub failed: {err}"}
    count = len([l for l in out.split("\n") if l.strip()])
    return {"count": count, "error": None}


def check_benchmark_health():
    """Run benchmark health check script if available."""
    path = WORKSPACE / "scripts" / "benchmark_health_check.py"
    if not path.exists():
        return {"ok": True, "error": None, "note": "benchmark_health_check.py not found, skipping"}
    rc, out, err = run(["python3", str(path)], timeout=15)
    return {"ok": rc == 0, "error": None if rc == 0 else out or err}


def check_cron_health():
    """Run cron health check if available."""
    path = WORKSPACE / "scripts" / "cron_health_fixed.py"
    if not path.exists():
        return {"ok": True, "error": None, "note": "cron_health_fixed.py not found, skipping"}
    rc, out, err = run(["python3", str(path)], timeout=10)
    return {"ok": rc == 0, "error": None if rc == 0 else out or err}


def main():
    results = {}

    results["brain"] = check_brain()
    results["git"] = check_git()
    results["clawhub_skills"] = check_clawhub_skills()
    results["benchmark_health"] = check_benchmark_health()
    results["cron_health"] = check_cron_health()

    alerts = []
    critical = False

    if not results["brain"]["ok"]:
        alerts.append(f"Brain: {results['brain']['error']}")
        critical = True

    if results["git"]["alert"]:
        alerts.append(f"Git: {results['git']['error']}")

    if not results["benchmark_health"]["ok"]:
        alerts.append(f"Benchmark: {results['benchmark_health']['error']}")
        critical = True

    if not results["cron_health"]["ok"]:
        alerts.append(f"Cron: {results['cron_health']['error']}")

    if results["clawhub_skills"]["count"] == -1:
        alerts.append(f"ClawHub: {results['clawhub_skills']['error']}")

    output = {
        "timestamp": NOW,
        "brain": results["brain"],
        "git": {"uncommitted_files": results["git"]["uncommitted_files"], "alert": results["git"]["alert"]},
        "clawhub_skills": {"count": results["clawhub_skills"]["count"]},
        "benchmark_health": results["benchmark_health"]["ok"],
        "cron_health": results["cron_health"]["ok"],
        "alerts": alerts,
        "critical": critical,
    }

    print(json.dumps(output, indent=2))
    sys.exit(1 if alerts else 0)


if __name__ == "__main__":
    main()