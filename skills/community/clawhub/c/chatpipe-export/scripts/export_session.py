#!/usr/bin/env python3
"""
ChatPipe Export — One-click session export via ChatPipe.

Usage:
    python3 export_session.py                          # export current session as markdown
    python3 export_session.py --session agent:main:main  # specific session
    python3 export_session.py --format chatgpt-json    # output as JSON
    python3 export_session.py --markdown                # shortcut

The script saves session data to a temp JSON, runs ChatPipe on it,
and saves the result to workspace with a readable filename.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
CHATPIPE = os.path.join(WORKSPACE, "products/chatpipe/chatpipe.py")

def export_session(session_key: str, output_format: str = "markdown", title: str = None):
    """Export a session transcript and convert via ChatPipe."""

    # Build a mock session JSON that ChatPipe can parse
    # The caller (OpenClaw agent) should provide the actual session data.
    # This script reads from stdin if piped, or creates a sample.

    if not os.path.exists(CHATPIPE):
        print(f"❌ ChatPipe not found at {CHATPIPE}")
        return None

    # If stdin has data, use it directly
    if not sys.stdin.isatty():
        raw_input = sys.stdin.read().strip()
        if raw_input:
            temp_path = os.path.join(WORKSPACE, "temp_session_export.json")
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(raw_input)
        else:
            print("❌ No data received on stdin")
            return None
    else:
        print("❌ No session data provided. Pipe session JSON to this script.")
        print("   Usage: cat session.json | python3 export_session.py")
        return None

    # Run chatpipe
    out_dir = WORKSPACE
    cmd = [
        sys.executable, CHATPIPE,
        temp_path,
        "-o", output_format,
        "-d", out_dir,
    ]
    if title:
        cmd.extend(["--title", title])

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        return None

    # Find the output file
    import_name = os.path.basename(temp_path).replace(".json", "")
    ext = {"markdown": ".md", "chatgpt-json": ".json", "chatbox-json": ".json", "plain-text": ".txt"}[output_format]
    out_name = f"{import_name}_export{ext}"
    out_path = os.path.join(out_dir, out_name)

    # Rename to something nicer
    date_str = datetime.now().strftime("%Y-%m-%d")
    nice_name = f"session-{session_key.replace(':','-')}-{date_str}{ext}"
    nice_path = os.path.join(out_dir, nice_name)
    if os.path.exists(out_path):
        os.rename(out_path, nice_path)

    # Clean temp
    os.remove(temp_path)

    return nice_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ChatPipe Session Export")
    parser.add_argument("--session", type=str, default="current", help="Session key")
    parser.add_argument("--format", type=str, default="markdown",
                       choices=["markdown", "chatgpt-json", "chatbox-json", "plain-text"])
    parser.add_argument("--markdown", action="store_true", help="Shortcut for --format markdown")
    parser.add_argument("--title", type=str, help="Export title")
    args = parser.parse_args()

    fmt = "markdown" if args.markdown else args.format
    path = export_session(args.session, fmt, args.title)
    if path:
        print(f"\n✅ Exported: {path}")
        sys.exit(0)
    else:
        sys.exit(1)
