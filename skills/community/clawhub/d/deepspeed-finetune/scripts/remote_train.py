#!/usr/bin/env python3
"""
Remote training manager: execute training asynchronously on remote GPU servers and monitor progress via log files.

Security design:
1. Passwords are passed via environment variables only, never written to any file
2. After the first connection, an SSH ControlMaster socket is established and reused for subsequent operations
3. Supports automatic SSH key authentication (no passphrase) to eliminate password transmission entirely
4. Session file stores only non-sensitive info (host, port, log path, socket, etc.)

Environment variables:
    REMOTE_SSH_PASSWORD — SSH login password (only needed on first connection or without key)
    REMOTE_TRAIN_SSH_KEY — Private key path (default ~/.ssh/deepspeed_remote)

Usage (run on local machine):

    # 1. First connection + launch training (password via env var)
    REMOTE_SSH_PASSWORD=xxx python3 scripts/remote_train.py launch \
        --host user@your-server.com \
        --port 22 \
        --script train_qwen25_0.5b.py \
        --log train_log.txt

    # 2. Check training progress (reuses ControlMaster, no password needed)
    python3 scripts/remote_train.py status [--tail-lines 30]

    # 3. Get full logs
    python3 scripts/remote_train.py logs [--tail-lines 100]

    # 4. Stop training
    python3 scripts/remote_train.py stop

    # 5. Setup SSH key authentication (optionally with password)
    # With password: auto-uploads public key
    # Without password: generates key pair and displays public key for manual addition
    REMOTE_SSH_PASSWORD=xxx python3 scripts/remote_train.py setup-keys \
        --host user@your-server.com \
        --port 22

    # 6. Check connection status (verify ControlMaster or key availability)
    python3 scripts/remote_train.py check-connection
"""

import argparse
import subprocess
import re
import sys
import json
import os
import time
import base64


SESSION_FILE = ".remote_train_session.json"
SOCKET_DIR = "/tmp/deepspeed_remote_ssh"
DEFAULT_KEY_PATH = os.path.expanduser("~/.ssh/deepspeed_remote")
TMUX_SESSION_NAME = "ds-train"
def _shell_safe(s):
    """Shell-escape a string to prevent command injection."""
    return subprocess.list2cmdline([s])


def _safe_int(s):
    """Ensure value is a positive integer to prevent numeric injection."""
    try:
        v = int(s)
        if v > 0:
            return str(v)
    except (ValueError, TypeError):
        pass
    raise ValueError(f"Expected positive integer, got: {s}")


def _socket_path(host, port):
    """Generate SSH ControlMaster socket path."""
    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', f"{host}_{port}")
    return os.path.join(SOCKET_DIR, f"ctrl_{safe_name}")


def _get_session():
    """Read local session file, return None if it doesn't exist."""
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE) as f:
            return json.load(f)
    return None


def _save_session(session):
    """Save session file (without passwords or other sensitive info)."""
    sensitive_keys = {"password", "passphrase", "key_passphrase", "REMOTE_SSH_PASSWORD", "REMOTE_SSH_KEY_PASSPHRASE"}
    for key in sensitive_keys:
        if key in session:
            del session[key]
    with open(SESSION_FILE, "w") as f:
        json.dump(session, f, indent=2, ensure_ascii=False)
    os.chmod(SESSION_FILE, 0o600)


def _get_password():
    """Get SSH password from environment variable."""
    return os.environ.get("REMOTE_SSH_PASSWORD", "")


def _build_ssh_base(host, port, use_key=True):
    """Build base SSH argument list (without password)."""
    cmd = [
        "ssh",
        "-o", "StrictHostKeyChecking=no",
        "-o", "ServerAliveInterval=30",
        "-o", "ConnectTimeout=10",
        "-p", str(port),
    ]

    socket = _socket_path(host, port)
    if os.path.exists(socket):
        cmd.extend(["-S", socket])
    elif use_key and os.path.exists(DEFAULT_KEY_PATH):
        cmd.extend(["-i", DEFAULT_KEY_PATH])

    cmd.append(host)
    return cmd


def _ssh_exec(host, port, cmd, timeout=15):
    """Execute command on remote server. Tries ControlMaster first, then key, then password."""
    ssh_cmd = _build_ssh_base(host, port, use_key=True)
    ssh_cmd.append(cmd)
    try:
        result = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=timeout)
        if result.returncode == 0:
            return result.stdout, result.stderr, 0
    except subprocess.TimeoutExpired:
        return "", "SSH timeout", 1

    # Fallback: use password (read from env var only)
    password = _get_password()
    if not password:
        return "", "Authentication failed: no usable key and REMOTE_SSH_PASSWORD not set", 1

    ssh_cmd = [
        "sshpass", "-p", password,
        "ssh", "-o", "StrictHostKeyChecking=no",
        "-o", "ServerAliveInterval=30",
        "-o", "ConnectTimeout=10",
        "-p", str(port), host, cmd
    ]
    try:
        result = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=timeout)
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "SSH timeout", 1


def _ensure_control_master(host, port):
    """Establish SSH ControlMaster connection (persistent background, reuses authenticated channel)."""
    socket = _socket_path(host, port)
    if os.path.exists(socket):
        test_cmd = _build_ssh_base(host, port, use_key=True)
        test_cmd.append("-O", "check")
        result = subprocess.run(test_cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return True
        else:
            try:
                os.unlink(socket)
            except OSError:
                pass

    os.makedirs(SOCKET_DIR, exist_ok=True)
    os.chmod(SOCKET_DIR, 0o700)

    # Try to establish with key (no passphrase)
    if os.path.exists(DEFAULT_KEY_PATH):
        ssh_cmd = [
            "ssh", "-o", "StrictHostKeyChecking=no",
            "-o", "ServerAliveInterval=30",
            "-o", "ConnectTimeout=10",
            "-M", "-S", socket,
            "-i", DEFAULT_KEY_PATH,
            "-p", str(port), host,
            "-N", "-f"
        ]
        result = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=15)
        if result.returncode == 0 and os.path.exists(socket):
            return True

    # Fallback: establish ControlMaster with password
    password = _get_password()
    if password:
        ssh_cmd = [
            "sshpass", "-p", password,
            "ssh", "-o", "StrictHostKeyChecking=no",
            "-o", "ServerAliveInterval=30",
            "-o", "ConnectTimeout=10",
            "-M", "-S", socket,
            "-p", str(port), host,
            "-N", "-f"
        ]
        result = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=15)
        if result.returncode == 0 and os.path.exists(socket):
            return True

    return False


def _check_tmux_available(host, port):
    """Check if tmux is available on the remote server."""
    stdout, _, code = _ssh_exec(host, port, "which tmux 2>/dev/null")
    return code == 0 and stdout.strip()


def launch(args):
    """Launch a training task on the remote server (asynchronous, using tmux for session persistence)."""
    host, port = args.host, args.port

    # 1. Establish ControlMaster
    print(f"Connecting to {host}:{port}...")
    if not _ensure_control_master(host, port):
        print("Failed to establish connection. Set password via REMOTE_SSH_PASSWORD env var, or run setup-keys first.")
        sys.exit(1)
    print(f"Connected successfully")

    # 2. Check tmux availability
    if not _check_tmux_available(host, port):
        print("tmux is not installed on the remote server. It is required for session persistence.")
        print("Install it with: apt-get install tmux (Debian/Ubuntu) or yum install tmux (RHEL/CentOS)")
        sys.exit(1)

    # 3. Upload training script
    remote_path = f"{args.remote_dir}/{os.path.basename(args.script)}"
    print(f"Uploading training script {args.script} -> {remote_path}")

    socket = _socket_path(host, port)
    scp_cmd = [
        "scp", "-o", "StrictHostKeyChecking=no",
        "-S", socket,
        args.script, f"{host}:{remote_path}"
    ]
    result = subprocess.run(scp_cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        # Fallback: scp with password
        password = _get_password()
        if password:
            scp_cmd = [
                "sshpass", "-p", password,
                "scp", "-o", "StrictHostKeyChecking=no",
                "-P", str(port), args.script, f"{host}:{remote_path}"
            ]
            result = subprocess.run(scp_cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            print(f"Upload failed: {result.stderr}")
            sys.exit(1)

    # 4. Kill existing tmux session if it exists (idempotent)
    safe_session = _shell_safe(TMUX_SESSION_NAME)
    kill_cmd = f"tmux kill-session -t {safe_session} 2>/dev/null; true"
    _ssh_exec(host, port, kill_cmd, timeout=10)

    # 5. Launch remote training via tmux
    log_path = f"{args.remote_dir}/{args.log}"
    safe_dir = _shell_safe(args.remote_dir)
    safe_python = _shell_safe(args.remote_python)
    safe_script = _shell_safe(os.path.basename(args.script))
    safe_log = _shell_safe(log_path)
    safe_session = _shell_safe(TMUX_SESSION_NAME)
    remote_cmd = (
        f"tmux new-session -d -s {safe_session} "
        f"\"cd {safe_dir} && exec {safe_python} -u {safe_script} > {safe_log} 2>&1\""
    )
    print(f"Launching training on {host}...")
    stdout, stderr, code = _ssh_exec(host, port, remote_cmd, timeout=30)

    if code != 0:
        print(f"Launch failed: {stderr}")
        sys.exit(1)

    # Get PID from tmux pane
    pid_cmd = f"tmux list-panes -t {safe_session} -F '{{{{pane_pid}}}}' 2>/dev/null"
    stdout, _, code = _ssh_exec(host, port, pid_cmd, timeout=10)
    pid = stdout.strip() if code == 0 else "unknown"

    print(f"Training started, tmux session: {TMUX_SESSION_NAME}, PID: {pid}")
    print(f"Log file: {host}:{log_path}")
    print(f"Use 'status' command to check progress")

    # Save connection info (without password)
    session = {
        "host": host,
        "port": port,
        "pid": pid,
        "tmux_session": TMUX_SESSION_NAME,
        "log": log_path,
        "remote_dir": args.remote_dir,
        "script": args.script,
        "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    _save_session(session)
    print(f"Session info saved to {SESSION_FILE} (no password included)")


def get_status(args):
    """Query remote training status and progress."""
    session = _get_session()
    if not session:
        print("No session file found. Run launch first.")
        sys.exit(1)

    host = session["host"]
    port = session["port"]
    tmux_session = session.get("tmux_session")
    pid = session.get("pid")
    log_path = session.get("log")

    tail_lines = args.tail_lines if hasattr(args, 'tail_lines') and args.tail_lines else 30

    # Check tmux session
    if tmux_session:
        safe_session = _shell_safe(tmux_session)
        check_cmd = f"tmux has-session -t {safe_session} 2>/dev/null && tmux list-panes -t {safe_session} -F '{{{{pane_pid}}}}' || echo TMUX_ENDED"
        stdout, _, code = _ssh_exec(host, port, check_cmd)
        pane_output = stdout.strip()
        if pane_output and pane_output != "TMUX_ENDED":
            print(f"Training tmux session running ({tmux_session})")
            if pane_output:
                actual_pid = pane_output.split('\n')[-1].strip()
                ps_cmd = f"ps -p {_safe_int(actual_pid)} -o pid,pcpu,pmem,etime,args --no-headers 2>/dev/null"
                ps_out, _, _ = _ssh_exec(host, port, ps_cmd)
                if ps_out.strip():
                    print(f"   {ps_out.strip()}")
        else:
            print(f"Training tmux session ended ({tmux_session})")
    elif pid and pid != "unknown":
        # Legacy: check by PID (no tmux session stored)
        safe_pid = _safe_int(pid)
        check_cmd = f"ps -p {safe_pid} -o pid,pcpu,pmem,etime,args --no-headers 2>/dev/null"
        stdout, _, code = _ssh_exec(host, port, check_cmd)
        if code == 0 and stdout.strip():
            print(f"Training process running:")
            print(f"   {stdout.strip()}")
        else:
            print(f"Training process ended (PID {pid})")

    # GPU status
    gpu_cmd = "nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv,noheader 2>/dev/null"
    stdout, _, _ = _ssh_exec(host, port, gpu_cmd)
    if stdout.strip():
        parts = stdout.strip().split(", ")
        if len(parts) >= 4:
            print(f"GPU: {parts[0]} / {parts[1]}, utilization: {parts[2]}, temperature: {parts[3]}")

    # Logs
    if log_path:
        safe_log = _shell_safe(log_path)
        safe_tail = _safe_int(tail_lines)
        log_cmd = f"tail -{safe_tail} {safe_log} 2>/dev/null"
        stdout, _, _ = _ssh_exec(host, port, log_cmd)
        if stdout.strip():
            print(f"\nLatest logs ({log_path}):")
            print("-" * 60)

            lines = stdout.strip().split('\n')
            progress_info = []
            for line in lines:
                loss_match = re.search(r"'loss':\s*'?([\d.]+)'?", line)
                eval_match = re.search(r"'eval_loss':\s*'?([\d.]+)'?", line)
                lr_match = re.search(r"'learning_rate':\s*'?([\d.e+-]+)'?", line)
                epoch_match = re.search(r"'epoch':\s*'?([\d.]+)'?", line)

                if loss_match:
                    progress_info.append(f"  Train Loss: {loss_match.group(1)}")
                    if lr_match:
                        progress_info.append(f"  LR: {lr_match.group(1)}")
                    if epoch_match:
                        progress_info.append(f"  Epoch: {epoch_match.group(1)}")
                if eval_match:
                    progress_info.append(f"  Eval Loss: {eval_match.group(1)}")

            for line in lines:
                print(line)

            if progress_info:
                print("\nTraining metrics summary:")
                for info in progress_info:
                    print(info)
        else:
            print("Log file is empty or does not exist")

        # Log file size
        safe_size_log = _shell_safe(log_path)
        size_cmd = f"stat --format=%s {safe_size_log} 2>/dev/null"
        stdout, _, _ = _ssh_exec(host, port, size_cmd)
        if stdout.strip():
            size_kb = int(stdout.strip()) / 1024
            print(f"\nLog file size: {size_kb:.1f} KB")


def get_logs(args):
    """Get full or tail logs."""
    session = _get_session()
    if not session:
        print("No session file found. Run launch first.")
        sys.exit(1)

    host = session["host"]
    port = session["port"]
    log_path = session.get("log", f"{session.get('remote_dir', '/root')}/{args.log}")

    lines = _safe_int(args.tail_lines if args.tail_lines else 100)
    safe_log = _shell_safe(log_path)
    log_cmd = f"tail -{lines} {safe_log} 2>/dev/null"
    stdout, _, _ = _ssh_exec(host, port, log_cmd, timeout=30)
    print(stdout if stdout.strip() else "No log output")


def remote_exec(args):
    """Execute arbitrary command on remote server and return output. For quick checks."""
    host = args.host
    port = args.port
    timeout = args.timeout if hasattr(args, 'timeout') and args.timeout else 30

    if not host:
        session = _get_session()
        if session:
            host = session["host"]
            port = session["port"]
        else:
            print("No --host specified and no active session")
            sys.exit(1)

    stdout, stderr, code = _ssh_exec(host, port, args.command, timeout=timeout)
    if stdout.strip():
        print(stdout.strip())
    if stderr.strip():
        print(f"[stderr] {stderr.strip()}")
    sys.exit(code)


def stop(args):
    """Terminate remote training process."""
    session = _get_session()
    if not session:
        print("No session file found")
        sys.exit(1)

    host, port = session["host"], session["port"]
    tmux_session = session.get("tmux_session")

    if tmux_session:
        safe_session = _shell_safe(tmux_session)
        kill_cmd = f"tmux kill-session -t {safe_session} 2>/dev/null; echo done"
        stdout, _, _ = _ssh_exec(host, port, kill_cmd)
        print(f"Killed tmux session: {tmux_session}")
    else:
        # Legacy: kill by PID
        pid = session.get("pid")
        if not pid or pid == "unknown":
            print("No PID or tmux session found")
            sys.exit(1)
        safe_pid = _safe_int(pid)
        kill_cmd = f"kill {safe_pid} 2>/dev/null; sleep 1; ps -p {safe_pid} 2>/dev/null || echo 'Process terminated'"
        stdout, _, _ = _ssh_exec(host, port, kill_cmd)
        print(f"Terminating process PID {pid}")
        print(stdout.strip())


def setup_keys(args):
    """Configure SSH key authentication (no passphrase).

    If REMOTE_SSH_PASSWORD is provided, the public key is uploaded automatically.
    If no password is available (e.g., RunPod), the public key is displayed for
    manual addition to the remote machine's management interface.
    """
    host, port = args.host, args.port
    password = _get_password()

    # 1. Generate key pair (no passphrase)
    if os.path.exists(DEFAULT_KEY_PATH):
        print(f"Key already exists: {DEFAULT_KEY_PATH}")
        overwrite = input("Overwrite? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("Cancelled")
            sys.exit(1)

    print(f"Generating key pair...")
    keygen_cmd = ["ssh-keygen", "-t", "ed25519", "-f", DEFAULT_KEY_PATH, "-N", "", "-C", "deepspeed-remote"]
    result = subprocess.run(keygen_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Key generation failed: {result.stderr}")
        sys.exit(1)
    os.chmod(DEFAULT_KEY_PATH, 0o600)
    os.chmod(f"{DEFAULT_KEY_PATH}.pub", 0o644)
    ssh_dir = os.path.dirname(DEFAULT_KEY_PATH)
    if os.path.isdir(ssh_dir):
        os.chmod(ssh_dir, 0o700)
    print(f"Key generated: {DEFAULT_KEY_PATH}")

    # 2. Read public key
    pub_key_path = f"{DEFAULT_KEY_PATH}.pub"
    with open(pub_key_path) as f:
        pub_key = f.read().strip()

    if not password:
        # No password available: display public key for manual addition
        print(f"NO_PASSWORD_MODE")
        print(f"PUBLIC_KEY_START")
        print(pub_key)
        print(f"PUBLIC_KEY_END")
        print(f"KEY_PATH={DEFAULT_KEY_PATH}")
        return

    # 3. Auto-upload public key via SSH (password available)
    pub_key_b64 = base64.b64encode(pub_key.encode()).decode()
    remote_setup = (
        f"mkdir -p ~/.ssh && "
        f"chmod 700 ~/.ssh && "
        f"touch ~/.ssh/authorized_keys && "
        f"chmod 600 ~/.ssh/authorized_keys && "
        f"grep -qF '{pub_key_b64}' ~/.ssh/.deepspeed_setup_marker 2>/dev/null || "
        f"(echo '{pub_key_b64}' >> ~/.ssh/.deepspeed_setup_marker && "
        f"echo '{pub_key_b64}' | base64 -d >> ~/.ssh/authorized_keys)"
    )
    print(f"Uploading public key to {host}...")
    stdout, stderr, code = sshpass_exec(host, port, password, remote_setup, timeout=15)
    if code != 0:
        print(f"Public key upload failed: {stderr}")
        print(f"\nYou can add the key manually instead. Here is the public key:")
        print(f"\n--- PUBLIC KEY ---")
        print(pub_key)
        print(f"--- END ---")
        print(f"\nAfter adding, run: python3 scripts/remote_train.py check-connection")
        return
    print(f"Public key configured on remote machine")

    # 4. Verify key login
    print(f"Verifying key login...")
    verify_cmd = [
        "ssh", "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        "-i", DEFAULT_KEY_PATH,
        "-p", str(port), host, "echo ok"
    ]
    result = subprocess.run(verify_cmd, capture_output=True, text=True, timeout=10)

    if result.returncode == 0 and "ok" in result.stdout:
        print(f"Key authentication verified! No password needed for future connections.")
        _ensure_control_master(host, port)
    else:
        print(f"Key verification failed. authorized_keys may need time to take effect. Password can still be used as fallback.")


def check_connection(args):
    """Check current connection status."""
    session = _get_session()
    if not session:
        print("No session file found")

        if os.path.exists(DEFAULT_KEY_PATH):
            print(f"Key found: {DEFAULT_KEY_PATH}")
            print("Ready to use (no passphrase)")
        else:
            print("No key found. Set up via password or setup-keys")
        return

    host, port = session["host"], session["port"]
    socket = _socket_path(host, port)

    if os.path.exists(socket):
        test_cmd = _build_ssh_base(host, port, use_key=True)
        test_cmd.append("-O")
        test_cmd.append("check")
        result = subprocess.run(test_cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"ControlMaster connection active ({socket})")
            return

    if os.path.exists(DEFAULT_KEY_PATH):
        print("Key found, attempting connection...")
        stdout, stderr, code = _ssh_exec(host, port, "echo ok", timeout=10)
        if code == 0:
            print(f"Key authentication available, establishing ControlMaster...")
            if _ensure_control_master(host, port):
                print(f"ControlMaster established")
            return

    print(f"No active connection. Set REMOTE_SSH_PASSWORD env var or run setup-keys")


def sshpass_exec(host, port, password, cmd, timeout=15):
    """Execute SSH command using sshpass + password (only used in setup-keys and other init scenarios)."""
    ssh_cmd = [
        "sshpass", "-p", password,
        "ssh", "-o", "StrictHostKeyChecking=no",
        "-o", "ServerAliveInterval=30",
        "-o", "ConnectTimeout=10",
        "-p", str(port), host, cmd
    ]
    try:
        result = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=timeout)
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "SSH timeout", 1


def main():
    parser = argparse.ArgumentParser(description="Remote training manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # launch command
    launch_parser = subparsers.add_parser("launch", help="Launch training on remote server")
    launch_parser.add_argument("--host", required=True, help="SSH address (user@host)")
    launch_parser.add_argument("--port", type=int, default=22, help="SSH port")
    launch_parser.add_argument("--script", required=True, help="Training script filename (local path)")
    launch_parser.add_argument("--log", default="train_log.txt", help="Remote log filename")
    launch_parser.add_argument("--remote-dir", default="/root", help="Remote working directory")
    launch_parser.add_argument("--remote-python", default="python3", help="Remote Python path")

    # status command (no extra args, reads from session)
    status_parser = subparsers.add_parser("status", help="Check training status")
    status_parser.add_argument("--tail-lines", type=int, default=30, help="Show last N lines of log")

    # logs command
    logs_parser = subparsers.add_parser("logs", help="Get logs")
    logs_parser.add_argument("--tail-lines", type=int, default=100, help="Show last N lines of log")

    # remote-exec command
    re_parser = subparsers.add_parser("remote-exec", help="Execute command on remote and return output")
    re_parser.add_argument("--host", help="SSH address (uses session if not specified)")
    re_parser.add_argument("--port", type=int, default=22, help="SSH port")
    re_parser.add_argument("command", help="Remote command to execute")
    re_parser.add_argument("--timeout", type=int, default=30, help="Timeout in seconds")

    # stop command
    subparsers.add_parser("stop", help="Stop training")

    # setup-keys command
    keys_parser = subparsers.add_parser("setup-keys", help="Setup SSH key authentication (no passphrase)")
    keys_parser.add_argument("--host", required=True, help="SSH address (user@host)")
    keys_parser.add_argument("--port", type=int, default=22, help="SSH port")

    # check-connection command
    subparsers.add_parser("check-connection", help="Check current connection status")

    args = parser.parse_args()

    if args.command == "launch":
        launch(args)
    elif args.command == "remote-exec":
        remote_exec(args)
    elif args.command == "status":
        get_status(args)
    elif args.command == "logs":
        get_logs(args)
    elif args.command == "stop":
        stop(args)
    elif args.command == "setup-keys":
        setup_keys(args)
    elif args.command == "check-connection":
        check_connection(args)


if __name__ == "__main__":
    main()
