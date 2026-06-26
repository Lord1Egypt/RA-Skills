#!/usr/bin/env python3
"""
queue_processor.py — Part of the comfyui-bridge OpenClaw skill.

Faceswap Queue Processor — runs on the same machine as OpenClaw.

When the bridge is down, comfyui_generate.py saves requests to a local queue
directory (~/.openclaw/faceswap-queue/). This script processes them when the
bridge comes back up and delivers results via iMessage using the imsg CLI.

Repository: https://github.com/Bortlesboat/comfyui-bridge (see repo for full source)

Usage:
    python3 queue_processor.py --process    # Process all queued requests
    python3 queue_processor.py --status     # Show queue status
    python3 queue_processor.py --daemon     # Run as background daemon (check every 5 min)

Queue dir: ~/.openclaw/faceswap-queue/
Each request is a JSON file + associated image files.

Environment variables:
    COMFYUI_BRIDGE_URL  URL of the ComfyUI Bridge server (default: http://localhost:8100)
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

QUEUE_DIR = Path.home() / ".openclaw" / "faceswap-queue"
DEAD_LETTER_DIR = QUEUE_DIR / "dead-letter"
OUTBOUND_DIR = Path.home() / ".openclaw" / "media" / "outbound"
MAX_RETRIES = 3
BRIDGE_URL = os.environ.get("COMFYUI_BRIDGE_URL", "http://localhost:8100")

# Resolve comfyui_generate.py relative to this script so the package works
# regardless of where it is installed.
GENERATE_SCRIPT = Path(__file__).resolve().parent / "comfyui_generate.py"

LOG_FILE = QUEUE_DIR / "processor.log"

# Default delivery target — iMessage chat ROWID (override via --chat-id or
# the chat_target field in the queued request JSON).
DEFAULT_CHAT_ID = "7"
IMSG_CLI = "/opt/homebrew/bin/imsg"


def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} {msg}"
    print(line)
    try:
        QUEUE_DIR.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def check_bridge():
    """Check if bridge is reachable."""
    try:
        import urllib.request
        req = urllib.request.Request(f"{BRIDGE_URL}/health")
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read())
        return data.get("status") == "ok" and data.get("comfyui") == "reachable"
    except Exception:
        return False


def get_queued_requests():
    """Get all queued request files, sorted by creation time."""
    if not QUEUE_DIR.exists():
        return []
    requests = sorted(QUEUE_DIR.glob("request_*.json"), key=lambda p: p.stat().st_mtime)
    return requests


def send_imessage(chat_id, text, image_path=None):
    """Send a message (and optionally an image) to an iMessage chat via imsg CLI.

    chat_id is the chat ROWID (e.g. "7").
    Uses /opt/homebrew/bin/imsg which is the same tool OpenClaw uses.
    """
    if not chat_id or chat_id == "":
        chat_id = DEFAULT_CHAT_ID
    try:
        cmd = [IMSG_CLI, "send", "--chat-id", str(chat_id)]
        if text:
            cmd.extend(["--text", text])
        if image_path and Path(image_path).exists():
            cmd.extend(["--file", str(image_path)])
        if not text and not (image_path and Path(image_path).exists()):
            log("Nothing to send (no text, no valid image)")
            return False
        # Pass HOME explicitly so imsg finds ~/Library/Messages/chat.db
        # even when running as a LaunchAgent with restricted environment
        send_env = {**os.environ, "HOME": str(Path.home())}
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30, env=send_env)
        if r.returncode == 0:
            log(f"Delivered to chat {chat_id}")
            return True
        log(f"imsg send failed (exit {r.returncode}): {r.stderr[:200] or '(no stderr)' }")
        # Shell fallback for LaunchAgent TCC context
        shell_cmd = " ".join([IMSG_CLI, "send", "--chat-id", str(chat_id)])
        if text:
            shell_cmd += " --text " + subprocess.list2cmdline([text])
        if image_path and Path(image_path).exists():
            shell_cmd += " --file " + subprocess.list2cmdline([str(image_path)])
        r2 = subprocess.run(shell_cmd, shell=True, capture_output=True, text=True, timeout=30, env=send_env)
        if r2.returncode == 0:
            log(f"Delivered to chat {chat_id} (shell fallback)")
            return True
        log(f"imsg shell fallback failed (exit {r2.returncode}): {r2.stderr[:200] or '(no stderr)' }")
        return False
    except Exception as e:
        log(f"iMessage send error: {e}")
        return False


def _cleanup_queue_images(req_file, req):
    """Delete queue-dir copies of input images after successful processing.
    Only removes files that live inside QUEUE_DIR (i.e., copies made at queue time),
    never the originals in faces/ or elsewhere.
    """
    for img_key in ["source_face", "input_image", "style_ref"]:
        img_path = req.get(img_key)
        if img_path:
            img_p = Path(img_path)
            if img_p.exists() and img_p.parent == QUEUE_DIR:
                try:
                    img_p.unlink()
                except Exception as exc:
                    log(f"Cleanup warning: could not delete {img_p.name}: {exc}")


def _move_to_dead_letter(req_file, req):
    """Move a request file (and its associated images) to the dead-letter directory."""
    DEAD_LETTER_DIR.mkdir(parents=True, exist_ok=True)
    dst = DEAD_LETTER_DIR / req_file.name
    shutil.move(str(req_file), str(dst))
    # Also move associated image files
    for img_key in ["source_face", "input_image", "style_ref"]:
        img_path = req.get(img_key)
        if img_path:
            img_p = Path(img_path)
            if img_p.exists() and img_p.parent == QUEUE_DIR:
                shutil.move(str(img_p), str(DEAD_LETTER_DIR / img_p.name))
    log(f"Moved {req_file.name} to dead-letter after {MAX_RETRIES} failures")


def _increment_retry(req_file, req):
    """Increment retry_count in the request file. Returns new count."""
    retry_count = req.get("retry_count", 0) + 1
    req["retry_count"] = retry_count
    tmp = req_file.with_suffix(".tmp")
    tmp.write_text(json.dumps(req, indent=2))
    tmp.rename(req_file)
    return retry_count


def process_request(req_file):
    """Process a single queued request."""
    try:
        req = json.loads(req_file.read_text())
    except Exception as e:
        log(f"Invalid request file {req_file.name}: {e}")
        req_file.unlink(missing_ok=True)
        return False

    # Check retry count — move to dead letter if exceeded
    retry_count = req.get("retry_count", 0)
    if retry_count >= MAX_RETRIES:
        _move_to_dead_letter(req_file, req)
        return False

    args = req.get("args", [])
    chat_target = req.get("chat_target", "") or DEFAULT_CHAT_ID
    requester = req.get("requester", "someone")
    description = req.get("description", "a faceswap")
    queued_at = req.get("queued_at", "unknown time")
    output_file = req.get("output_file", "")

    # Verify image files still exist
    for img_key in ["source_face", "input_image", "style_ref"]:
        img_path = req.get(img_key)
        if img_path and not Path(img_path).exists():
            log(f"Image missing for {req_file.name}: {img_path}")
            req_file.unlink(missing_ok=True)
            return False

    log(f"Processing queued request: {description} (from {requester} at {queued_at}, attempt {retry_count + 1}/{MAX_RETRIES})")

    # Build command — add --no-media only if not already present (prevents accumulation on retries)
    extra = [] if "--no-media" in args else ["--no-media"]
    cmd = ["uv", "run", str(GENERATE_SCRIPT)] + args + extra
    if output_file and "-f" not in args and "--filename" not in args:
        cmd.extend(["-f", output_file])

    # Ensure uv and homebrew binaries are in PATH (launchd has minimal PATH)
    proc_env = {**os.environ, "COMFYUI_BRIDGE_URL": BRIDGE_URL}
    extra_path = str(Path.home() / ".local" / "bin") + ":/opt/homebrew/bin:/usr/local/bin"
    proc_env["PATH"] = extra_path + ":" + proc_env.get("PATH", "/usr/bin:/bin")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, timeout=600,
            env=proc_env
        )

        if result.returncode == 0:
            # Find the output file path from stdout
            out_path = output_file
            for line in result.stdout.splitlines():
                if line.startswith("Image saved:"):
                    out_path = line.split("Image saved:")[1].strip().split(" (")[0]
                    break

            if out_path and Path(out_path).exists():
                log(f"Success: {out_path}")
                # Deliver via iMessage if we have a chat target
                if chat_target:
                    caption = f"Here's that {description} from earlier (was queued while the system was down)"
                    if send_imessage(chat_target, caption, out_path):
                        log(f"Delivered to {chat_target}")
                    else:
                        log(f"WARNING: iMessage delivery failed for {chat_target}")
                # Cleanup: remove queue-dir copies of input images (prevent disk bloat)
                _cleanup_queue_images(req_file, req)
                req_file.unlink(missing_ok=True)
                return True
            else:
                log(f"Command succeeded but no output file found (stdout: {result.stdout[-300:]!r})")
                # Treat as a soft failure — retry rather than silently discard
                _increment_retry(req_file, req)
                return False
        else:
            log(f"Command failed (exit {result.returncode}): {result.stderr[:200]}")
            # Increment retry count — will dead-letter after MAX_RETRIES
            _increment_retry(req_file, req)
            return False
    except subprocess.TimeoutExpired:
        log(f"Command timed out (600s)")
        _increment_retry(req_file, req)
        return False
    except Exception as e:
        log(f"Process error: {e}")
        _increment_retry(req_file, req)
        return False


def process_all():
    """Process all queued requests."""
    requests = get_queued_requests()
    if not requests:
        print("No queued requests")
        return

    if not check_bridge():
        print("Bridge still down — skipping queue processing")
        return

    print(f"Processing {len(requests)} queued request(s)...")
    success = 0
    for req_file in requests:
        if process_request(req_file):
            success += 1
        time.sleep(2)  # Brief pause between requests

    print(f"Processed: {success}/{len(requests)} succeeded")


def show_status():
    """Show queue status."""
    requests = get_queued_requests()
    dead_letters = sorted(DEAD_LETTER_DIR.glob("request_*.json")) if DEAD_LETTER_DIR.exists() else []
    bridge_up = check_bridge()
    print(f"Bridge: {'UP' if bridge_up else 'DOWN'}")
    print(f"Queued requests: {len(requests)}")
    for req_file in requests:
        try:
            req = json.loads(req_file.read_text())
            retries = req.get("retry_count", 0)
            retry_info = f" (retries: {retries})" if retries else ""
            print(f"  - {req.get('description', '?')} from {req.get('requester', '?')} at {req.get('queued_at', '?')}{retry_info}")
        except Exception:
            print(f"  - {req_file.name} (corrupt)")
    if dead_letters:
        print(f"Dead-letter requests: {len(dead_letters)}")
        for dl in dead_letters:
            try:
                req = json.loads(dl.read_text())
                print(f"  - {req.get('description', '?')} at {req.get('queued_at', '?')} (failed {req.get('retry_count', '?')}x)")
            except Exception:
                print(f"  - {dl.name} (corrupt)")


def daemon_loop():
    """Run as daemon, checking every 5 minutes."""
    log("Queue processor daemon started")
    while True:
        try:
            requests = get_queued_requests()
            if requests and check_bridge():
                log(f"Bridge up, {len(requests)} queued — processing")
                process_all()
        except Exception as e:
            log(f"Daemon error: {e}")
        time.sleep(300)  # 5 minutes


def main():
    parser = argparse.ArgumentParser(description="Faceswap Queue Processor")
    parser.add_argument("--process", action="store_true", help="Process all queued requests now")
    parser.add_argument("--status", action="store_true", help="Show queue status")
    parser.add_argument("--daemon", action="store_true", help="Run as background daemon")
    args = parser.parse_args()

    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    DEAD_LETTER_DIR.mkdir(parents=True, exist_ok=True)
    OUTBOUND_DIR.mkdir(parents=True, exist_ok=True)

    if args.daemon:
        daemon_loop()
    elif args.status:
        show_status()
    elif args.process:
        process_all()
    else:
        show_status()


if __name__ == "__main__":
    main()
