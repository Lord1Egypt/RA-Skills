#!/usr/bin/env python3
"""
server_monitor.py — Feature 8: SSH/SLURM Experiment Monitoring
Connect to your GPU server, watch jobs, auto-pull results when done.
Usage:
  python3 server_monitor.py setup                        — configure server
  python3 server_monitor.py jobs                         — list running SLURM jobs
  python3 server_monitor.py watch <job_id>               — watch job log live
  python3 server_monitor.py status                       — show all jobs + GPU usage
  python3 server_monitor.py pull <job_id> <remote_path>  — pull results when done
  python3 server_monitor.py gpu                          — check GPU usage
  python3 server_monitor.py run <script.sh>             — submit SLURM job
"""

import sys
import os
import json
import subprocess
import time
import datetime

CONFIG_FILE = os.path.expanduser(
    "~/.openclaw/workspace/research-supervisor-pro/memory/server_config.json"
)


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE) as f:
        return json.load(f)


def save_config(data):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Server config saved → {CONFIG_FILE}")


def ssh_cmd(config, remote_cmd, timeout=30):
    """Run a command on the remote server via SSH."""
    host = config.get("host", "")
    user = config.get("user", "")
    port = config.get("port", 22)
    key  = config.get("ssh_key", "")

    if not host or not user:
        print("❌ Server not configured. Run: python3 server_monitor.py setup")
        return None, "Not configured"

    cmd = ["ssh", "-o", "StrictHostKeyChecking=no",
           "-o", f"ConnectTimeout={timeout}",
           "-p", str(port)]
    if key:
        cmd += ["-i", os.path.expanduser(key)]
    cmd += [f"{user}@{host}", remote_cmd]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout+5)
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return None, "SSH timeout"
    except Exception as e:
        return None, str(e)


def setup_server():
    print("\n🖥️  SERVER SETUP")
    print("━" * 50)
    print("Configure your GPU server for experiment monitoring.\n")

    cfg = load_config()

    fields = [
        ("host",     "Server hostname or IP (e.g. 10.26.xx.xx or login.hpc.edu):"),
        ("user",     "Username:"),
        ("port",     "SSH port (default 22):"),
        ("ssh_key",  "SSH key path (e.g. ~/.ssh/id_rsa, or Enter for password):"),
        ("workdir",  "Remote working directory (e.g. /home/user/research):"),
        ("scheduler","Job scheduler (slurm / pbs / none):"),
    ]

    for key, prompt in fields:
        current = cfg.get(key, "")
        val = input(f"{prompt}\n  [{current or 'not set'}] → ").strip()
        if val:
            cfg[key] = val
        elif not current and key == "port":
            cfg[key] = "22"
        elif not current and key == "scheduler":
            cfg[key] = "slurm"

    save_config(cfg)

    # Test connection
    print("\n🔍 Testing connection...")
    out, err = ssh_cmd(cfg, "echo 'EVE_CONNECTED' && hostname")
    if out and "EVE_CONNECTED" in out:
        print(f"✅ Connected to: {out.split(chr(10))[-1]}")
    else:
        print(f"❌ Connection failed: {err}")
        print("   Check your hostname, username, and SSH key.")


def list_jobs():
    cfg = load_config()
    scheduler = cfg.get("scheduler", "slurm")

    if scheduler == "slurm":
        cmd = "squeue --me --format='%.10i %.20j %.8T %.10M %.6D %R' 2>/dev/null"
    elif scheduler == "pbs":
        cmd = "qstat -u $USER 2>/dev/null"
    else:
        cmd = "ps aux | grep python | grep -v grep"

    out, err = ssh_cmd(cfg, cmd)
    if out:
        print(f"\n📋 RUNNING JOBS on {cfg.get('host','?')}:")
        print("━" * 60)
        print(out)
        print("━" * 60)
    else:
        print(f"❌ Could not list jobs: {err}")


def watch_job(job_id):
    cfg = load_config()
    workdir = cfg.get("workdir", "~")

    # Find log file
    log_patterns = [
        f"{workdir}/logs/*{job_id}*.out",
        f"{workdir}/slurm-{job_id}.out",
        f"{workdir}/*{job_id}*.log",
    ]

    log_file = None
    for pattern in log_patterns:
        out, _ = ssh_cmd(cfg, f"ls {pattern} 2>/dev/null | head -1")
        if out:
            log_file = out.strip()
            break

    if not log_file:
        # Try finding by job name
        out, _ = ssh_cmd(cfg, f"scontrol show job {job_id} 2>/dev/null | grep StdOut | awk -F= '{{print $2}}'")
        if out:
            log_file = out.strip()

    if not log_file:
        print(f"❌ Log file not found for job {job_id}")
        print("   Looking in:", workdir)
        return

    print(f"👁️  Watching job {job_id} → {log_file}")
    print("   (Ctrl+C to stop)\n")
    print("━" * 60)

    seen_lines = 0
    try:
        while True:
            out, err = ssh_cmd(cfg, f"tail -n +{seen_lines+1} {log_file} 2>/dev/null")
            if out:
                lines = out.split("\n")
                for line in lines:
                    print(line)
                    # Detect completion
                    if any(kw in line.lower() for kw in ["completed", "finished", "done", "error", "failed", "epoch"]):
                        if "error" in line.lower() or "failed" in line.lower():
                            print(f"\n🚨 ALERT: Job may have failed!")
                seen_lines += len(lines)

            # Check if job is still running
            status_out, _ = ssh_cmd(cfg, f"squeue -j {job_id} --noheader 2>/dev/null")
            if not status_out:
                print(f"\n✅ Job {job_id} appears to have finished!")
                break

            time.sleep(10)
    except KeyboardInterrupt:
        print("\n\nStopped watching.")


def check_gpu():
    cfg = load_config()
    out, err = ssh_cmd(cfg, "nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv,noheader,nounits 2>/dev/null")

    if out:
        print(f"\n🖥️  GPU STATUS on {cfg.get('host','?')}:")
        print("━" * 60)
        lines = out.strip().split("\n")
        for i, line in enumerate(lines):
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 5:
                name, mem_used, mem_total, util, temp = parts[:5]
                mem_pct = int(mem_used) / int(mem_total) * 100 if mem_total.isdigit() and int(mem_total) > 0 else 0
                bar = "█" * int(mem_pct / 10) + "░" * (10 - int(mem_pct / 10))
                print(f"  GPU {i}: {name}")
                print(f"    Memory:  [{bar}] {mem_used}/{mem_total} MB ({mem_pct:.0f}%)")
                print(f"    Util:    {util}% | Temp: {temp}°C")
        print("━" * 60)
    else:
        print(f"❌ Could not get GPU info: {err}")


def pull_results(job_id, remote_path, local_path=None):
    cfg = load_config()
    host = cfg.get("host", "")
    user = cfg.get("user", "")
    port = cfg.get("port", 22)
    key  = cfg.get("ssh_key", "")

    if not local_path:
        local_path = f"./results_{job_id}/"
    os.makedirs(local_path, exist_ok=True)

    print(f"📥 Pulling results from {remote_path} → {local_path}")

    cmd = ["scp", "-r", "-P", str(port), "-o", "StrictHostKeyChecking=no"]
    if key:
        cmd += ["-i", os.path.expanduser(key)]
    cmd += [f"{user}@{host}:{remote_path}", local_path]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(f"✅ Results pulled to: {local_path}")
            # List pulled files
            for f in os.listdir(local_path):
                print(f"   📄 {f}")
        else:
            print(f"❌ SCP failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Error: {e}")


def server_status():
    cfg = load_config()
    if not cfg.get("host"):
        print("❌ Server not configured. Run: python3 server_monitor.py setup")
        return

    print(f"\n🖥️  SERVER: {cfg.get('user')}@{cfg.get('host')}")
    print("━" * 60)

    # CPU/Memory
    out, _ = ssh_cmd(cfg, "top -bn1 | grep 'Cpu\\|Mem' | head -2")
    if out:
        print("System:", out[:100])

    # Disk
    out, _ = ssh_cmd(cfg, f"df -h {cfg.get('workdir','~')} 2>/dev/null | tail -1")
    if out:
        print("Disk:  ", out)

    print()
    check_gpu()
    print()
    list_jobs()


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "setup":
        setup_server()
    elif sys.argv[1] == "jobs":
        list_jobs()
    elif sys.argv[1] == "watch" and len(sys.argv) >= 3:
        watch_job(sys.argv[2])
    elif sys.argv[1] == "status":
        server_status()
    elif sys.argv[1] == "gpu":
        check_gpu()
    elif sys.argv[1] == "pull" and len(sys.argv) >= 4:
        local = sys.argv[4] if len(sys.argv) > 4 else None
        pull_results(sys.argv[2], sys.argv[3], local)
    elif sys.argv[1] == "run" and len(sys.argv) >= 3:
        cfg = load_config()
        out, err = ssh_cmd(cfg, f"cd {cfg.get('workdir','~')} && sbatch {sys.argv[2]}")
        print(out or err)
    else:
        print(__doc__)
