#!/usr/bin/env python3
"""Claude Code notification script.

On macOS: uses terminal-notifier for native notifications.
On devpod/remote: sends via SSH reverse tunnel to local listener,
falls back to OSC 9 escape sequence.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.request
import urllib.error


def debug(msg: str) -> None:
    """Print debug message to stderr if DEBUG=1."""
    if os.environ.get("DEBUG") == "1":
        print(f"[DEBUG] {msg}", file=sys.stderr)


def send_remote(message: str, title: str, sound: str, port: int = 19876) -> bool:
    """Send notification via SSH reverse tunnel to local listener.

    Args:
        message: Notification message
        title: Notification title
        sound: Sound name
        port: Local port for reverse tunnel

    Returns:
        True if successfully sent, False otherwise
    """
    payload = json.dumps({
        "message": message,
        "title": title,
        "sound": sound
    })

    debug(f"Sending via reverse tunnel on port {port}")

    try:
        req = urllib.request.Request(
            f"http://127.0.0.1:{port}",
            data=payload.encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=3) as response:
            if response.status == 200:
                debug("Notification sent via tunnel")
                return True
    except (urllib.error.URLError, OSError) as e:
        debug(f"Tunnel not available: {e}, falling back to OSC 9")
        return False

    return False


def send_osc9(message: str, title: str) -> None:
    """Send OSC 9 escape sequence for in-app terminal notification.

    Args:
        message: Notification message
        title: Notification title
    """
    msg = f"{title}: {message}"

    if os.environ.get("TMUX"):
        debug("Inside tmux, using DCS passthrough for OSC 9")
        # DCS passthrough: \ePtmux;\e\e]9;...\a\e\\
        print(f"\033Ptmux;\033\033]9;{msg}\007\033\\", end="", flush=True)
    else:
        debug("Sending OSC 9 directly")
        # Direct OSC 9: \e]9;...\a
        print(f"\033]9;{msg}\007", end="", flush=True)


def detect_bundle_id() -> str | None:
    """Detect macOS terminal app bundle ID from TERM_PROGRAM env var.

    Returns:
        Bundle ID string or None if not recognized
    """
    term_program = os.environ.get("TERM_PROGRAM", "")

    bundle_map = {
        "WarpTerminal": "dev.warp.Warp-Stable",
        "iTerm.app": "com.googlecode.iterm2",
        "Apple_Terminal": "com.apple.Terminal",
        "vscode": "com.microsoft.VSCode",
        "Hyper": "co.zeit.hyper",
        "Alacritty": "org.alacritty",
        "kitty": "net.kovidgoyal.kitty"
    }

    return bundle_map.get(term_program)


def send_local(message: str, title: str, sound: str) -> None:
    """Send notification using terminal-notifier on local macOS.

    Args:
        message: Notification message
        title: Notification title
        sound: Sound name
    """
    bundle_id = detect_bundle_id()

    cmd = [
        "terminal-notifier",
        "-message", message,
        "-title", title,
        "-sound", sound
    ]

    if bundle_id:
        cmd.extend(["-activate", bundle_id])

    subprocess.run(cmd, check=True)


def notify(message: str, title: str = "Claude Code", sound: str = "Glass") -> None:
    """Main notification dispatcher.

    Args:
        message: Notification message
        title: Notification title (default: "Claude Code")
        sound: Sound name (default: "Glass")
    """
    debug(f"Message: {message}")
    debug(f"Title: {title}")
    debug(f"Sound: {sound}")

    # Check if terminal-notifier is available
    if shutil.which("terminal-notifier") is None:
        debug("terminal-notifier not found, trying reverse tunnel")
        if not send_remote(message, title, sound):
            send_osc9(message, title)
    else:
        send_local(message, title, sound)


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Send notifications from Claude Code"
    )
    parser.add_argument(
        "message",
        help="Notification message"
    )
    parser.add_argument(
        "--title",
        default="Claude Code",
        help="Notification title (default: Claude Code)"
    )
    parser.add_argument(
        "--sound",
        default="Glass",
        help="Notification sound (default: Glass)"
    )

    args = parser.parse_args()

    try:
        notify(args.message, args.title, args.sound)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
