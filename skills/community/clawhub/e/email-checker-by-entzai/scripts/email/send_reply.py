#!/usr/bin/env python3
"""
send_reply.py — Send an email reply via Mail.app

Usage:
    python3 send_reply.py --to EMAIL --subject SUBJECT --content "Reply text"
    python3 send_reply.py --to EMAIL --subject SUBJECT --file reply.txt

Examples:
    python3 send_reply.py \
        --to colleague@example.com \
        --subject "Re: Quick question" \
        --content "Hi, thanks for the note! EntzClawBot 🤖"

    python3 send_reply.py \
        --to someone@example.com \
        --subject "Re: Meeting" \
        --file /path/to/draft.txt
"""

import subprocess
import argparse
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR    = Path(__file__).parent.resolve()
WORKSPACE_DIR = SCRIPT_DIR.parent.parent
LOG_FILE      = WORKSPACE_DIR / "logs" / "email_check.log"
TEMP_FILE     = WORKSPACE_DIR / "temp" / "send_reply_content.txt"


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")


def send_reply(to_address, subject, content):
    # Write content to temp file — avoids AppleScript string injection issues
    # with newlines and quotes in the message body.
    TEMP_FILE.parent.mkdir(parents=True, exist_ok=True)
    TEMP_FILE.write_text(content, encoding="utf-8")

    applescript = f'''tell application "Mail"
        set replyContent to do shell script "cat {TEMP_FILE}"
        set newMessage to make new outgoing message with properties {{subject:"{subject}", content:replyContent}}
        tell newMessage
            make new to recipient at end of to recipients with properties {{address:"{to_address}"}}
        end tell
        send newMessage
        return "Sent"
    end tell'''

    try:
        result = subprocess.run(
            ['osascript', '-e', applescript],
            capture_output=True, text=True,
            timeout=30
        )
        if result.returncode != 0:
            log(f"Failed to send to {to_address}: {result.stderr.strip()}")
            return False
        log(f"Reply sent to {to_address} — Subject: {subject}")
        return True
    except subprocess.TimeoutExpired:
        log("send_reply: osascript timed out after 30s")
        return False
    except Exception as e:
        log(f"send_reply: unexpected error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Send an email reply via Mail.app")
    parser.add_argument("--to",      required=True,  help="Recipient email address")
    parser.add_argument("--subject", required=True,  help="Email subject line")

    content_group = parser.add_mutually_exclusive_group(required=True)
    content_group.add_argument("--content", help="Reply text (inline)")
    content_group.add_argument("--file",    help="Path to a text file containing the reply")

    args = parser.parse_args()

    if args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"Error: file not found: {args.file}")
            sys.exit(1)
        content = path.read_text(encoding="utf-8").strip()
    else:
        content = args.content.strip()

    if not content:
        print("Error: reply content is empty")
        sys.exit(1)

    log(f"Sending reply to {args.to}...")
    success = send_reply(args.to, args.subject, content)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
