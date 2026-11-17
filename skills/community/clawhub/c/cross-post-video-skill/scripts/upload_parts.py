#!/usr/bin/env python3
"""Upload one file to a WoopSocial media upload session (standard library only).

WoopSocial uploads work in three steps:
  1. The agent calls `media_uploads_create_session` with the projectId and the file size in bytes.
  2. This script PUTs the file's bytes to each presigned part URL from that response.
  3. The agent calls `media_uploads_complete_session`. When the status is READY it includes the
     mediaId; otherwise poll `media_uploads_get_session` until it is READY (or report FAILED).

Usage:
    python3 scripts/upload_parts.py session.json clips/launch.mp4

session.json is the JSON returned by `media_uploads_create_session`, saved as it came back. It
must contain `partSizeInBytes` and `parts` (each with `partNumber` and `uploadUrl`). The second
argument is the video or the cover to upload. Both paths are relative to the folder you run from.

A part that fails on the network is tried three times. If the PUT is blocked by a network
allowlist, allow `*.r2.cloudflarestorage.com`.
"""
import http.client
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xplib import die, guard, read_json, reading  # noqa: E402

USAGE = "usage: upload_parts.py session.json <video or cover file>"
NOT_A_SESSION = ("is not the reply of media_uploads_create_session: it needs partSizeInBytes and parts, each "
                 "with partNumber and uploadUrl. Save that reply as it came back and run this again")


def put_with_curl(url, chunk):
    """Fallback for Python builds without system certificates (common on macOS)."""
    result = subprocess.run(
        ["curl", "-fsS", "-X", "PUT", "-H", "Content-Type: application/octet-stream",
         "--data-binary", "@-", "-o", os.devnull, "-w", "%{http_code}", url],
        input=chunk, capture_output=True, timeout=300)
    if result.returncode != 0:
        raise RuntimeError((result.stderr.decode(errors="replace").strip().splitlines() or ["curl failed"])[-1])
    try:
        return int(result.stdout.decode() or 0)
    except ValueError:
        return 0


def plain(err):
    """A network error in a few plain words: 'Connection refused', not '[Errno 61] ...'."""
    text = getattr(err, "strerror", None) or str(err) or "no answer"
    text = re.sub(r"\[[^\]]*\]\s*", "", text).strip() or "no answer"
    return text.splitlines()[0][:120]


def put(url, chunk):
    request = urllib.request.Request(url, data=chunk, method="PUT",
                                     headers={"Content-Type": "application/octet-stream"})
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return response.status
    except urllib.error.HTTPError:
        raise
    except urllib.error.URLError as err:
        if "CERTIFICATE_VERIFY_FAILED" in str(err.reason):
            return put_with_curl(url, chunk)
        raise


def load_session(session_path):
    """The parts to upload, in order, and the size of each. Dies with one line when the file is
    anything other than the saved reply of media_uploads_create_session."""
    session = read_json(session_path)
    for wrap in ("result", "data", "session", "structuredContent"):   # the whole tool reply was saved
        if isinstance(session, dict) and "parts" not in session and isinstance(session.get(wrap), dict):
            session = session[wrap]
    if not isinstance(session, dict):
        die(f"{session_path} {NOT_A_SESSION}")
    size, parts = session.get("partSizeInBytes"), session.get("parts")
    if isinstance(size, bool) or not isinstance(size, int) or size <= 0 or not isinstance(parts, list) or not parts:
        die(f"{session_path} {NOT_A_SESSION}")
    for p in parts:
        number = p.get("partNumber") if isinstance(p, dict) else None
        if isinstance(number, bool) or not isinstance(number, int) or not isinstance(p.get("uploadUrl"), str):
            die(f"{session_path} {NOT_A_SESSION}")
        if not p["uploadUrl"].startswith("https://"):
            die(f"{session_path}: the uploadUrl of part {number} is not an https:// link. Create a new "
                "session (media_uploads_create_session) and save its reply as it came back")
    count = session.get("partCount", len(parts))
    if isinstance(count, bool) or not isinstance(count, int) or count != len(parts):
        die(f"{session_path} says {count} part(s) but lists {len(parts)}. Create a new session "
            "(media_uploads_create_session) and save its reply as it came back")
    return size, sorted(parts, key=lambda p: p["partNumber"])


def main():
    if len(sys.argv) != 3:
        die(USAGE)
    session_path, file_path = sys.argv[1], sys.argv[2]
    if not os.path.exists(session_path):
        die(f"{session_path} not found. Save the reply of media_uploads_create_session as that file first. {USAGE}")
    if os.path.isdir(file_path):
        die(f"{file_path} is a folder; give the one video or cover file to upload")
    if not os.path.isfile(file_path):
        die(f"{file_path} not found (the video or cover to upload is the second argument)")
    if not session_path.lower().endswith(".json") and file_path.lower().endswith(".json"):
        die(f"the two arguments are the wrong way round. {USAGE}")
    part_size, parts = load_session(session_path)
    reading(file_path)
    size = os.path.getsize(file_path)
    if not size:
        die(f"{file_path} is an empty file (0 bytes); there is nothing to upload")
    needed = -(-size // part_size)
    if needed != len(parts):
        die(f"the session expects {len(parts)} part(s) but {file_path} ({size} bytes) needs {needed}. Create "
            "the session again with this file's exact size in bytes (fileSizeInBytes)")

    with open(file_path, "rb") as f:
        for part in parts:
            chunk = f.read(part_size)
            number = part["partNumber"]
            status, why = None, ""
            for attempt in range(3):
                if attempt:
                    time.sleep(attempt * 2 - 1)   # 1 s, then 3 s
                try:
                    status = put(part["uploadUrl"], chunk)
                    if 200 <= status < 300:
                        break
                    why, status = f"HTTP {status}", None
                except urllib.error.HTTPError as err:
                    if err.code in (400, 401, 403, 404, 410):
                        die(f"part {number} was refused (HTTP {err.code}): the upload link has expired or was "
                            "already used. Create a new session (media_uploads_create_session) and run this again")
                    why = f"HTTP {err.code}"
                except (urllib.error.URLError, OSError, http.client.HTTPException, RuntimeError,
                        subprocess.SubprocessError) as err:
                    why = plain(getattr(err, "reason", None) or err)
            if status is None:
                die(f"part {number} could not be uploaded after 3 tries ({why}). Check the internet connection "
                    "and run the same command again; if a network allowlist is on, allow *.r2.cloudflarestorage.com")
            print(f"part {number}/{len(parts)} uploaded (HTTP {status})")
    print("All parts uploaded. Now call media_uploads_complete_session.")


if __name__ == "__main__":
    guard(main)
