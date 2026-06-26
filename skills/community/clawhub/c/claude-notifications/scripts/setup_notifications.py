#!/usr/bin/env python3
"""Claude Code Notification Setup.

Sets up native macOS notifications for local and devpod environments.
Usage: ./setup_notifications.py [--devpod <ssh-host>] [--devpod <ssh-host>] ...
"""

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path


def require_macos():
    """Exit with a clear message if not running on macOS."""
    if platform.system() != "Darwin":
        print(
            "Error: claude-notifications setup requires macOS (uses brew, launchctl, terminal-notifier).\n"
            "Run this on your Mac, not on a devpod/Linux machine.\n"
            "The setup script SSHs into devpods to configure them remotely.",
            file=sys.stderr,
        )
        sys.exit(1)


# Constants
NOTIFY_PORT = 19876
CLAUDE_DIR = Path.home() / ".claude"
SCRIPTS_DIR = CLAUDE_DIR / "scripts"
LOGS_DIR = CLAUDE_DIR / "logs"
PLIST_LABEL = "com.claude.notify-listener"
PLIST_PATH = Path.home() / "Library/LaunchAgents" / f"{PLIST_LABEL}.plist"

HOOK_MATCHERS = [
    {
        "matcher": "permission_prompt",
        "hooks": [{
            "type": "command",
            "command": '~/.claude/scripts/notify.py "Claude Code needs your permission to proceed" --title "Claude Code - Action Required" --sound "Ping"',
            "timeout": 5
        }]
    },
    {
        "matcher": "idle_prompt",
        "hooks": [{
            "type": "command",
            "command": '~/.claude/scripts/notify.py "Claude has been waiting for your input (60+ seconds)" --title "Claude Code - Idle" --sound "Glass"',
            "timeout": 5
        }]
    },
    {
        "matcher": "elicitation_dialog",
        "hooks": [{
            "type": "command",
            "command": '~/.claude/scripts/notify.py "Additional input required for MCP tool" --title "Claude Code" --sound "Submarine"',
            "timeout": 5
        }]
    }
]


def info(msg: str) -> None:
    """Print info message."""
    print(f"✅ {msg}")


def warn(msg: str) -> None:
    """Print warning message."""
    print(f"⚠️  {msg}")


def error(msg: str) -> None:
    """Print error message and exit."""
    print(f"❌ {msg}", file=sys.stderr)
    sys.exit(1)


def create_launchd_plist(python3_path: str, scripts_dir: Path, logs_dir: Path) -> str:
    """Create launchd plist XML content.

    Args:
        python3_path: Path to python3 executable
        scripts_dir: Path to scripts directory
        logs_dir: Path to logs directory

    Returns:
        XML plist content as string
    """
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{PLIST_LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python3_path}</string>
        <string>{scripts_dir}/notify-listener.py</string>
    </array>
    <key>KeepAlive</key>
    <true/>
    <key>RunAtLoad</key>
    <true/>
    <key>ProcessType</key>
    <string>Interactive</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>
    <key>StandardOutPath</key>
    <string>{logs_dir}/notify-listener.log</string>
    <key>StandardErrorPath</key>
    <string>{logs_dir}/notify-listener.log</string>
</dict>
</plist>
"""


def setup_hooks(settings_path: Path) -> None:
    """Configure Claude Code hooks in settings.json.

    Args:
        settings_path: Path to settings.json file
    """
    # Create file if it doesn't exist
    if not settings_path.exists():
        settings_path.write_text("{}")

    # Validate settings.json is valid JSON
    try:
        with open(settings_path) as f:
            data = json.load(f)
    except json.JSONDecodeError:
        warn(f"{settings_path} is corrupt. Backing up and recreating.")
        backup = Path(str(settings_path) + ".bak")
        shutil.copy(settings_path, backup)
        data = {}
        settings_path.write_text("{}")

    # Check if hooks already configured
    if "hooks" in data and "Notification" in data.get("hooks", {}):
        info("Claude Code notification hooks already configured")
        return

    # Add notification hooks
    data.setdefault("hooks", {})["Notification"] = HOOK_MATCHERS

    # Write back
    with open(settings_path, "w") as f:
        json.dump(data, f, indent=2)

    info("Configured Claude Code notification hooks")


def setup_local(script_dir: Path, claude_dir: Path) -> None:
    """Set up local macOS notifications.

    Args:
        script_dir: Path to skill's scripts directory
        claude_dir: Path to ~/.claude directory
    """
    print("── Setting up local notifications ──")

    # Create directories
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # Check terminal-notifier
    notifier_path = shutil.which("terminal-notifier")
    if notifier_path is None:
        print("Installing terminal-notifier...")
        result = subprocess.run(
            ["brew", "install", "terminal-notifier"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            error("Failed to install terminal-notifier. Run: brew install terminal-notifier")
        notifier_path = shutil.which("terminal-notifier")

    info(f"terminal-notifier found at {notifier_path}")

    # Copy notify.py
    src_notify = script_dir / "notify.py"
    dst_notify = SCRIPTS_DIR / "notify.py"
    shutil.copy(src_notify, dst_notify)
    dst_notify.chmod(0o755)
    info("Installed notify.py")

    # Copy and configure notify-listener.py
    src_listener = script_dir / "notify-listener.py"
    listener_content = src_listener.read_text()
    listener_content = listener_content.replace("__TERMINAL_NOTIFIER_PATH__", notifier_path)
    dst_listener = SCRIPTS_DIR / "notify-listener.py"
    dst_listener.write_text(listener_content)
    dst_listener.chmod(0o755)
    info("Installed notify-listener.py")

    # Get python3 path
    python3_path = shutil.which("python3")
    if python3_path is None:
        error("python3 is required but not found. Install via: brew install python3")

    # Create launchd plist
    plist_content = create_launchd_plist(python3_path, SCRIPTS_DIR, LOGS_DIR)
    PLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    PLIST_PATH.write_text(plist_content)
    info("Created launchd plist")

    # Stop existing listener if running
    subprocess.run(
        ["launchctl", "unload", str(PLIST_PATH)],
        capture_output=True,
        text=True
    )

    # Kill any stale process on the port and wait for it to be free
    result = subprocess.run(
        ["lsof", "-ti", f":{NOTIFY_PORT}"],
        capture_output=True,
        text=True
    )
    if result.stdout.strip():
        stale_pids = result.stdout.strip().split()
        for pid in stale_pids:
            subprocess.run(["kill", pid], capture_output=True)

        # Wait for port to be free
        for _ in range(10):
            result = subprocess.run(
                ["lsof", "-ti", f":{NOTIFY_PORT}"],
                capture_output=True,
                text=True
            )
            if not result.stdout.strip():
                break
            time.sleep(0.5)

    # Start listener
    subprocess.run(["launchctl", "load", str(PLIST_PATH)])
    time.sleep(1)

    # Verify
    result = subprocess.run(
        ["lsof", "-i", f":{NOTIFY_PORT}"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0 and result.stdout.strip():
        info(f"Notify listener running on port {NOTIFY_PORT}")
    else:
        warn(f"Listener may not have started. Check: cat {LOGS_DIR}/notify-listener.log")

    # Configure Claude Code hooks in settings.json
    setup_hooks(claude_dir / "settings.json")

    # Test
    print("")
    print("── Testing local notification ──")
    subprocess.run([
        str(SCRIPTS_DIR / "notify.py"),
        "Notifications setup complete!",
        "--title", "Claude Code",
        "--sound", "Glass"
    ])
    info("Test notification sent. You should see a native macOS notification.")

    print("")
    print("── Manual steps required ──")
    print("1. Enable notifications for your terminal app:")
    print("   System Settings > Notifications > [Warp / iTerm / Terminal]")
    print("   → Set 'Allow Notifications' to ON, alert style to 'Banners' or 'Alerts'")
    print("")
    print("2. Enable notifications for Script Editor:")
    print("   System Settings > Notifications > Script Editor")
    print("   → Set 'Allow Notifications' to ON")
    print("   (terminal-notifier routes through Script Editor)")
    print("")
    print("3. If using Focus/Do Not Disturb:")
    print("   Add 'Script Editor' and your terminal app to Focus exceptions")
    print("   OR turn off Do Not Disturb")


def setup_devpod_hooks(host: str) -> None:
    """Configure Claude Code hooks on devpod.

    Args:
        host: SSH hostname
    """
    python_script = """
import json, os

settings_path = os.path.expanduser("~/.claude/settings.json")
os.makedirs(os.path.dirname(settings_path), exist_ok=True)

data = {}
if os.path.exists(settings_path):
    with open(settings_path) as f:
        data = json.load(f)

if "hooks" in data and "Notification" in data.get("hooks", {}):
    print("hooks already configured")
else:
    data.setdefault("hooks", {})["Notification"] = [
        {"matcher": "permission_prompt", "hooks": [{"type": "command", "command": "~/.claude/scripts/notify.py \\"Claude Code needs your permission to proceed\\" --title \\"Claude Code - Action Required\\" --sound \\"Ping\\"", "timeout": 5}]},
        {"matcher": "idle_prompt", "hooks": [{"type": "command", "command": "~/.claude/scripts/notify.py \\"Claude has been waiting for your input (60+ seconds)\\" --title \\"Claude Code - Idle\\" --sound \\"Glass\\"", "timeout": 5}]},
        {"matcher": "elicitation_dialog", "hooks": [{"type": "command", "command": "~/.claude/scripts/notify.py \\"Additional input required for MCP tool\\" --title \\"Claude Code\\" --sound \\"Submarine\\"", "timeout": 5}]}
    ]
    with open(settings_path, "w") as f:
        json.dump(data, f, indent=2)
    print("hooks configured")
"""

    result = subprocess.run(
        ["ssh", host, f"python3 -c '{python_script}'"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        error(f"Failed to configure hooks on {host}: {result.stderr}")

    info(f"Configured Claude Code hooks on {host}")


def add_ssh_forward(host: str, port: int = NOTIFY_PORT) -> None:
    """Add RemoteForward to SSH config for host.

    Args:
        host: SSH hostname
        port: Port number for RemoteForward
    """
    ssh_config_path = Path.home() / ".ssh/config"
    forward_line = f"    RemoteForward {port} 127.0.0.1:{port}"

    # Create .ssh directory and config if needed
    ssh_config_path.parent.mkdir(parents=True, exist_ok=True)
    ssh_config_path.touch(mode=0o600)

    # Check if RemoteForward already configured for this host using resolved SSH config
    result = subprocess.run(
        ["ssh", "-G", host],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        for line in result.stdout.split("\n"):
            if line.lower().startswith("remoteforward") and str(port) in line:
                info(f"SSH RemoteForward already configured for {host}")
                return

    # Read SSH config
    content = ssh_config_path.read_text() if ssh_config_path.exists() else ""
    lines = content.split("\n")

    result_lines = []
    found_host = False
    inserted = False
    host_re = re.compile(r'^Host\s+.*\b' + re.escape(host) + r'\b')

    for i, line in enumerate(lines):
        # If we found the host block and hit the next block or blank line, insert before it
        if found_host and not inserted:
            is_new_block = line.startswith("Host ")
            is_blank = not line.strip()
            if is_new_block or is_blank:
                result_lines.append(forward_line)
                inserted = True
        result_lines.append(line)
        if not found_host and host_re.match(line):
            found_host = True

    # Host block was last in file, append at end
    if found_host and not inserted:
        result_lines.append(forward_line)

    if not found_host:
        # Add new Host block
        result_lines.append("")
        result_lines.append(f"Host {host}")
        result_lines.append(forward_line)

    # Write back
    ssh_config_path.write_text("\n".join(result_lines))

    info(f"SSH RemoteForward configured for {host}")


def setup_devpod(host: str, script_dir: Path) -> None:
    """Set up devpod notifications.

    Args:
        host: SSH hostname
        script_dir: Path to skill's scripts directory
    """
    print("")
    print(f"── Setting up devpod: {host} ──")

    # Verify SSH connectivity
    result = subprocess.run(
        ["ssh", "-o", "ConnectTimeout=10", host, "echo ok"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        error(f"Cannot SSH to {host}. Ensure the devpod is running.")
    info(f"SSH connection to {host} verified")

    # Create dirs and copy notify.py
    subprocess.run(["ssh", host, "mkdir -p ~/.claude/scripts"], check=True)

    src_notify = SCRIPTS_DIR / "notify.py"
    subprocess.run(
        ["scp", str(src_notify), f"{host}:~/.claude/scripts/notify.py"],
        check=True
    )

    subprocess.run(
        ["ssh", host, "chmod +x ~/.claude/scripts/notify.py"],
        check=True
    )
    info(f"Installed notify.py on {host}")

    # Configure tmux passthrough
    tmux_check = subprocess.run(
        ["ssh", host, 'grep -q "allow-passthrough" ~/.tmux.conf 2>/dev/null && echo "already set" || (echo "" >> ~/.tmux.conf && echo "# Allow OSC escape sequences to pass through for notifications" >> ~/.tmux.conf && echo "set -g allow-passthrough on" >> ~/.tmux.conf && echo "added")'],
        capture_output=True,
        text=True
    )
    info(f"Configured tmux passthrough on {host}")

    # Reload tmux config if tmux is running
    subprocess.run(
        ["ssh", host, "tmux source-file ~/.tmux.conf 2>/dev/null || true"],
        capture_output=True
    )

    # Configure Claude Code hooks on devpod
    setup_devpod_hooks(host)

    # Add RemoteForward to SSH config
    add_ssh_forward(host)

    info(f"Devpod {host} setup complete")
    print(f"   ⮑ Start a NEW SSH session to {host} for the reverse tunnel to activate.")


def main() -> None:
    """Main entry point."""
    require_macos()

    parser = argparse.ArgumentParser(
        description="Set up Claude Code notifications for local and devpod environments",
        epilog="""
Examples:
  %(prog)s                                    # Local only
  %(prog)s --devpod myuser.devpod-ind         # Local + one devpod
  %(prog)s --devpod host1 --devpod host2      # Local + multiple devpods
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--devpod",
        action="append",
        dest="devpods",
        metavar="SSH_HOST",
        help="SSH hostname of devpod to configure (can be specified multiple times)"
    )

    args = parser.parse_args()

    # Get script directory (where this script lives)
    script_dir = Path(__file__).parent

    # Always set up local first
    setup_local(script_dir, CLAUDE_DIR)

    # Set up devpods if specified
    devpods = args.devpods or []
    for host in devpods:
        setup_devpod(host, script_dir)

    print("")
    print("── Setup complete ──")
    print("Local notifications: ✅")
    if devpods:
        for host in devpods:
            print(f"Devpod {host}:     ✅ (reconnect SSH for tunnel)")


if __name__ == "__main__":
    main()
