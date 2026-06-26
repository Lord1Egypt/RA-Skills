#!/usr/bin/env python3
"""
agent-interrupt: Kill target agent process and rollback session transcript
to the state before the last triggering user message.

Usage:
    python -X utf8 interrupt.py --agent <agent_id> [--dry-run]

Environment:
    OPENCLAW_HOME  Override default ~/.openclaw location
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path


def find_openclaw_home():
    env = os.environ.get("OPENCLAW_HOME")
    if env:
        return Path(env)
    return Path.home() / ".openclaw"


def get_gateway_config(openclaw_home):
    config_path = openclaw_home / "openclaw.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_agent_id(target, config):
    """
    Resolve agent ID from a target string.
    Supports:
    - Exact ID match: 'my_agent'
    - Exact name match: 'My Agent Name'
    - Fuzzy name match: 'agent', 'my', 'age', '开发1', 'dev'
    Returns (agent_id, agent) or (None, None)
    """
    agents = config["agents"]["list"]
    target_lower = target.lower()

    # 1. Exact ID match
    for a in agents:
        if a["id"].lower() == target_lower:
            return a["id"], a

    # 2. Exact name match
    for a in agents:
        if a.get("name", "").lower() == target_lower:
            return a["id"], a

    # 3. Fuzzy: target is substring of id or name
    matches = []
    for a in agents:
        if (target_lower in a["id"].lower() or
                target_lower in a.get("name", "").lower()):
            matches.append(a)

    if len(matches) == 1:
        return matches[0]["id"], matches[0]
    elif len(matches) > 1:
        print(f"[interrupt] Ambiguous target '{target}', matches:")
        for m in matches:
            print(f"  - {m['id']} ({m.get('name', '')})")
        print("[interrupt] Please be more specific.")
        sys.exit(1)

    return None, None


def find_procs(workspace):
    procs = []
    if not workspace:
        return procs
    if sys.platform == "win32":
        # Use WMIC which is faster than Get-WmiObject for CommandLine queries
        try:
            result = subprocess.run(
                ["wmic", "process", "get", "ProcessId,CommandLine", "/format:csv"],
                capture_output=True, text=True, encoding="utf-8", timeout=10
            )
            for line in result.stdout.splitlines():
                if workspace.lower() in line.lower():
                    parts = line.split(",")
                    if len(parts) >= 2:
                        try:
                            pid = int(parts[-1].strip())
                            procs.append({"pid": pid, "cmd": line[:100]})
                        except ValueError:
                            pass
        except subprocess.TimeoutExpired:
            print("[interrupt] WARNING: Process scan timed out, skipping")
        except Exception:
            pass
    else:
        try:
            result = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=10)
            for line in result.stdout.splitlines():
                if workspace in line:
                    parts = line.split()
                    if parts:
                        try:
                            procs.append({"pid": int(parts[1]), "cmd": line[:100]})
                        except ValueError:
                            pass
        except subprocess.TimeoutExpired:
            print("[interrupt] WARNING: Process scan timed out, skipping")
    return procs


def get_marker_path(openclaw_home, agent_id):
    return openclaw_home / "agents" / agent_id / "running.json"


def read_marker(openclaw_home, agent_id):
    """Read running.json marker if exists."""
    marker_path = get_marker_path(openclaw_home, agent_id)
    if marker_path.exists():
        try:
            with open(marker_path, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return None


def kill_pid_tree(pid, dry_run=False):
    """Kill a PID and all its children recursively."""
    # Get all descendant PIDs
    result = subprocess.run(
        ["powershell", "-Command",
         f"$pids = @({pid}); $queue = @({pid}); while ($queue.Count -gt 0) {{ $p = $queue[0]; $queue = $queue[1..($queue.Count-1)]; $children = Get-WmiObject Win32_Process | Where-Object {{ $_.ParentProcessId -eq $p }} | Select-Object -ExpandProperty ProcessId; foreach ($c in $children) {{ $pids += $c; $queue += $c }}; }}; $pids -join ','" ],
        capture_output=True, text=True, encoding="utf-8"
    )
    all_pids = [int(p.strip()) for p in result.stdout.strip().split(',') if p.strip().isdigit()]
    print(f"[interrupt] PID tree to kill: {all_pids}")
    if dry_run:
        print("[interrupt] DRY-RUN: skipping kill")
        return True
    for p in all_pids:
        subprocess.run(
            ["powershell", "-Command", f"Stop-Process -Id {p} -Force -ErrorAction SilentlyContinue"],
            capture_output=True
        )
        print(f"[interrupt] Killed PID {p}")
    return True


def kill_agent_processes(agent_id, workspace, dry_run=False, openclaw_home=None):
    # Priority 1: Use running.json marker for precise kill
    if openclaw_home:
        marker = read_marker(openclaw_home, agent_id)
        if marker:
            pid = marker.get("pid")
            session_id = marker.get("session_id", "")
            print(f"[interrupt] Found marker: PID={pid} session={session_id}")
            if not dry_run:
                kill_pid_tree(pid, dry_run=False)
                # Clear marker after kill
                get_marker_path(openclaw_home, agent_id).unlink(missing_ok=True)
                time.sleep(0.5)
                # Verify dead
                still = find_procs(workspace or "")
                if still:
                    print(f"[interrupt] ERROR: Processes still alive after kill: {[p['pid'] for p in still]}")
                    print("[interrupt] ABORTING — transcript not modified.")
                    sys.exit(1)
                print("[interrupt] All processes confirmed dead.")
            else:
                print("[interrupt] DRY-RUN: would kill PID tree")
            return

    # Priority 2: Fallback — match by workspace path
    if not workspace:
        print(f"[interrupt] No workspace configured for {agent_id}, skipping process kill")
        return

    procs = find_procs(workspace)

    if not procs:
        print(f"[interrupt] No running processes found for {agent_id}")
        return

    print(f"[interrupt] Found {len(procs)} process(es) for {agent_id}:")
    for p in procs:
        print(f"  PID={p['pid']} {p['cmd']}")

    if dry_run:
        print("[interrupt] DRY-RUN: skipping kill")
        return

    for p in procs:
        if sys.platform == "win32":
            subprocess.run(
                ["powershell", "-Command", f"Stop-Process -Id {p['pid']} -Force -ErrorAction SilentlyContinue"],
                capture_output=True
            )
        else:
            subprocess.run(["kill", "-9", str(p["pid"])], capture_output=True)
        print(f"[interrupt] Killed PID {p['pid']}")

    # Verify all processes are dead
    time.sleep(0.5)
    still_alive = find_procs(workspace)
    if still_alive:
        pids = [str(p['pid']) for p in still_alive]
        print(f"[interrupt] ERROR: Processes still alive after kill: {', '.join(pids)}")
        print("[interrupt] ABORTING — transcript not modified to avoid data loss.")
        sys.exit(1)
    else:
        print(f"[interrupt] All processes confirmed dead.")


def find_latest_session(openclaw_home, agent_id):
    session_dir = openclaw_home / "agents" / agent_id / "sessions"
    if not session_dir.exists():
        return None
    files = list(session_dir.glob("*.jsonl"))
    if not files:
        return None
    return max(files, key=lambda f: f.stat().st_mtime)


def rollback_transcript(transcript_path, dry_run=False):
    lines = transcript_path.read_text(encoding="utf-8").splitlines()
    messages = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            messages.append(json.loads(line))
        except Exception:
            continue

    if not messages:
        print("[interrupt] Transcript is empty, nothing to rollback")
        return

    def get_role(entry):
        if entry.get("type") == "message" and "message" in entry:
            return entry["message"].get("role")
        return entry.get("role")

    last_user_idx = None
    for i in range(len(messages) - 1, -1, -1):
        if get_role(messages[i]) == "user":
            last_user_idx = i
            break

    if last_user_idx is None:
        print("[interrupt] No user message found in transcript, nothing to rollback")
        return

    last_user_msg = messages[last_user_idx]
    msg_body = last_user_msg.get("message", last_user_msg) if last_user_msg.get("type") == "message" else last_user_msg
    content = msg_body.get("content", "")
    if isinstance(content, list):
        preview = " ".join(c.get("text", "") for c in content if c.get("type") == "text")[:120]
    else:
        preview = str(content)[:120]

    removed = messages[last_user_idx:]
    print(f"[interrupt] Rolling back from message [{last_user_idx}]: {preview}")
    print(f"[interrupt] Removing {len(removed)} message(s) from transcript")

    if dry_run:
        print("[interrupt] DRY-RUN: skipping transcript modification")
        return

    # Backup removed messages to a log file for recovery
    import datetime
    log_dir = transcript_path.parent.parent / "interrupt-logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_path = log_dir / f"rollback-{ts}.jsonl"
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(json.dumps({
            "rollback_time": ts,
            "transcript": str(transcript_path),
            "removed_from_idx": last_user_idx,
            "removed_count": len(removed)
        }, ensure_ascii=False) + "\n")
        for msg in removed:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")
    print(f"[interrupt] Backup saved to: {log_path}")

    kept = messages[:last_user_idx]
    with open(transcript_path, "w", encoding="utf-8") as f:
        for msg in kept:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")

    print(f"[interrupt] Transcript rolled back. Kept {len(kept)} message(s).")


def interrupt_agent(agent_id, config, openclaw_home, dry_run=False):
    """Interrupt a single agent."""
    print(f"\n[interrupt] Target: {agent_id}")
    agent = next((a for a in config["agents"]["list"] if a["id"] == agent_id), None)
    workspace = agent.get("workspace") if agent else None
    if workspace is None:
        print(f"[interrupt] SKIP: Unknown agent '{agent_id}'")
        return

    kill_agent_processes(agent_id, workspace, dry_run, openclaw_home=openclaw_home)

    transcript = find_latest_session(openclaw_home, agent_id)
    if not transcript:
        print(f"[interrupt] No session transcript found for {agent_id}")
        return

    print(f"[interrupt] Transcript: {transcript}")
    rollback_transcript(transcript, dry_run)
    print(f"[interrupt] Done. {agent_id} is now in standby state.")


def main():
    parser = argparse.ArgumentParser(
        description="Interrupt agent task and rollback session",
        usage="interrupt.py <agent_name_or_id | all> [--dry-run]"
    )
    parser.add_argument("target", nargs="?", help="Agent name, ID, or 'all'")
    parser.add_argument("--agent", help="Agent ID or name (alternative to positional)")
    parser.add_argument("--all", action="store_true", help="Interrupt all agents except main")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no changes")
    args = parser.parse_args()

    # Resolve target: positional > --agent > --all
    target = args.target or args.agent
    if target and target.lower() == "all":
        args.all = True
        target = None

    if not target and not args.all:
        parser.error("Must specify an agent name/ID or 'all'")

    if args.dry_run:
        print("[interrupt] DRY-RUN mode")

    openclaw_home = find_openclaw_home()
    print(f"[interrupt] OpenClaw home: {openclaw_home}")
    config = get_gateway_config(openclaw_home)

    if args.all:
        all_agents = [a["id"] for a in config["agents"]["list"] if a["id"] != "main"]
        print(f"[interrupt] ALL mode: targeting {len(all_agents)} agents: {', '.join(all_agents)}")
        for agent_id in all_agents:
            interrupt_agent(agent_id, config, openclaw_home, args.dry_run)
        print(f"\n[interrupt] All agents interrupted.")
    else:
        agent_id, agent = resolve_agent_id(target, config)
        if agent_id is None:
            known = [(a["id"], a.get("name", "")) for a in config["agents"]["list"]]
            print(f"[interrupt] ERROR: No agent matching '{target}'")
            print("[interrupt] Known agents:")
            for aid, aname in known:
                print(f"  - {aid} ({aname})")
            sys.exit(1)
        if agent_id != target:
            print(f"[interrupt] Resolved '{target}' → {agent_id} ({agent.get('name', '')})")
        interrupt_agent(agent_id, config, openclaw_home, args.dry_run)


if __name__ == "__main__":
    main()
