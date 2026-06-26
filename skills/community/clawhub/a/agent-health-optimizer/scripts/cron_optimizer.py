#!/usr/bin/env python3
"""Cron Optimizer — analyze and selectively fix cron job issues.

Usage:
  python3 cron_optimizer.py [workspace_path]          # Read-only analysis
  python3 cron_optimizer.py --fix [workspace_path]    # Safe auto-repair

The fixer is intentionally conservative:
- It does NOT enable delivery on jobs that intentionally use delivery=none.
- It does NOT add stagger to exact-time jobs.
- It only auto-adds stagger to recurring top-of-hour stampede-prone jobs.
"""

import subprocess, sys, json
from datetime import datetime
from pathlib import Path

FIX_MODE = "--fix" in sys.argv
ws = Path(sys.argv[-1]) if len(sys.argv) > 1 and not sys.argv[-1].startswith("-") else Path.home() / ".openclaw" / "workspace"


def run_cmd(args, timeout=15):
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip(), r.returncode, r.stderr.strip()
    except Exception as e:
        return "", 1, str(e)


def get_all_jobs():
    out, code, err = run_cmd(["openclaw", "cron", "list", "--json"])
    if code != 0:
        return {}, err
    try:
        data = json.loads(out)
        return {j["id"]: j for j in data.get("jobs", [])}, ""
    except Exception as e:
        return {}, str(e)


def backup_cron_state(jobs_detail):
    backup_path = ws / "memory" / "cron-backup.json"
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    backup = {"timestamp": datetime.now().isoformat(), "jobs": jobs_detail}
    backup_path.write_text(json.dumps(backup, indent=2, ensure_ascii=False))
    print(f"💾 Cron state backed up to: {backup_path}")
    return backup_path


def schedule_label(job):
    schedule = job.get("schedule", {})
    kind = schedule.get("kind", "")
    if kind == "cron":
        return f"cron:{schedule.get('expr', '')} @ {schedule.get('tz', '') or 'local'}"
    if kind == "every":
        return f"every:{schedule.get('everyMs', '')}ms"
    if kind == "at":
        return f"at:{schedule.get('at', '')}"
    return "unknown"


def is_top_of_hour_cron(job):
    schedule = job.get("schedule", {})
    if schedule.get("kind") != "cron":
        return False
    expr = (schedule.get("expr") or "").strip()
    parts = expr.split()
    if len(parts) not in (5, 6):
        return False
    minute = parts[-5] if len(parts) == 5 else parts[-5]
    hour = parts[-4] if len(parts) == 5 else parts[-4]
    return minute == "0" and hour in {"*", "*/2", "*/3", "*/4", "*/6", "*/8", "*/12"}


def is_precise_job(job):
    schedule = job.get("schedule", {})
    if schedule.get("kind") != "cron":
        return schedule.get("kind") == "at"
    expr = (schedule.get("expr") or "").strip()
    parts = expr.split()
    if len(parts) not in (5, 6):
        return False
    minute = parts[-5]
    hour = parts[-4]
    return minute.isdigit() and hour.isdigit()


def main():
    print("\n⏰ Cron Optimizer")
    print("=" * 60)
    print("🔧 FIX MODE — safe, conservative repairs only" if FIX_MODE else "👀 READ-ONLY MODE — analysis only")

    jobs, err = get_all_jobs()
    if not jobs:
        print(f"No cron jobs found or could not fetch details. {err}".strip())
        return

    print(f"Found {len(jobs)} cron jobs.\n")

    issues = []
    fixes = []
    fix_candidates = []
    has_stagger = []
    no_stagger = []

    # Error states
    for jid, job in jobs.items():
        state = job.get("state", {})
        name = job.get("name", jid[:8])
        if state.get("lastStatus") == "error" or state.get("lastRunStatus") == "error":
            err = state.get("lastError", "unknown")
            consecutive = state.get("consecutiveErrors", 0)
            issues.append(f"🚨 [{name}] ERROR state (consecutive: {consecutive}): {err[:120]}")

    # Stagger analysis: warn generally, but only auto-fix risky recurring top-of-hour jobs.
    for jid, job in jobs.items():
        schedule = job.get("schedule", {})
        stagger_ms = schedule.get("staggerMs", 0) or 0
        name = job.get("name", jid[:8])
        if stagger_ms > 0:
            has_stagger.append(name)
            continue
        no_stagger.append((jid, name))
        if is_top_of_hour_cron(job):
            issues.append(f"⚠️ [{name}] has no stagger on {schedule_label(job)} — possible top-of-hour stampede risk")
            fix_candidates.append((jid, name))
        elif is_precise_job(job):
            issues.append(f"ℹ️ [{name}] has no stagger on {schedule_label(job)} — likely intentional exact timing")
        else:
            issues.append(f"💡 [{name}] has no stagger on {schedule_label(job)} — consider only if this job contributes to API bursts")

    if has_stagger:
        print(f"  ✅ {len(has_stagger)} jobs have stagger configured")

    # Time collisions
    schedules = {}
    for jid, job in jobs.items():
        key = schedule_label(job)
        schedules.setdefault(key, []).append(job.get("name", jid[:8]))

    for sched, names in schedules.items():
        if len(names) > 1:
            issues.append(f"⚠️ Time collision on '{sched}': {', '.join(names)}")

    # Delivery analysis: delivery=none is valid; only flag suspicious announce setups.
    for jid, job in jobs.items():
        delivery = job.get("delivery", {}) or {}
        mode = delivery.get("mode", "none")
        name = job.get("name", jid[:8])
        if mode in ("none", None):
            issues.append(f"ℹ️ [{name}] has delivery=none — valid for internal/background jobs")

        if mode == "announce" and not delivery.get("to") and delivery.get("channel") not in (None, "", "last"):
            issues.append(f"🚨 [{name}] has announce enabled but missing 'to' for explicit channel delivery — may fail")

    # Session target advice
    for jid, job in jobs.items():
        target = job.get("sessionTarget", "")
        name = job.get("name", jid[:8])
        payload = job.get("payload", {})
        kind = payload.get("kind", "")
        if target == "main" and kind == "agentTurn":
            issues.append(f"💡 [{name}] uses main session for agentTurn — consider isolated for autonomous/background tasks")

    # Timeout heuristics
    for jid, job in jobs.items():
        payload = job.get("payload", {})
        timeout = payload.get("timeoutSeconds", 30)
        msg = payload.get("message", "") or ""
        name = job.get("name", jid[:8])
        step_count = msg.lower().count("step") + msg.lower().count("```") + msg.lower().count("curl")
        if step_count > 3 and timeout < 180:
            issues.append(f"💡 [{name}] has {step_count} step-like markers but only {timeout}s timeout — consider increasing")

    if FIX_MODE and fix_candidates:
        backup_cron_state(jobs)
        for jid, name in fix_candidates:
            out, code, err = run_cmd(["openclaw", "cron", "edit", jid, "--stagger", "2m"])
            if code == 0:
                fixes.append(f"✅ Added 2m stagger to [{name}]")
            else:
                fixes.append(f"❌ Failed to add stagger to [{name}]: {err or out}")

    print("\n📋 Analysis Results:")
    print("-" * 40)
    if not issues:
        print("  ✅ No issues found — cron setup looks good!")
    else:
        for i in issues:
            print(f"  {i}")

    if fixes:
        print(f"\n🔧 Fixes Applied ({len(fixes)}):")
        for f in fixes:
            print(f"  {f}")
    elif fix_candidates and not FIX_MODE:
        print("\n💡 Run with --fix to auto-add stagger only to recurring top-of-hour jobs")

    report = {
        "total_jobs": len(jobs),
        "with_stagger": len(has_stagger),
        "without_stagger": len(no_stagger),
        "fix_candidates": [name for _, name in fix_candidates],
        "issues": issues,
        "fixes": fixes,
        "fix_mode": FIX_MODE,
        "timestamp": datetime.now().isoformat()
    }

    report_path = ws / "memory" / "cron-optimizer.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\n📊 Report saved: {report_path}")


if __name__ == "__main__":
    main()
