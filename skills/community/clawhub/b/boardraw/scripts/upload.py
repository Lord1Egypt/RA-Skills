#!/usr/bin/env python3
"""
Upload an Excalidraw whiteboard to boardraw.com via API.

Usage:
    python upload.py <whiteboard.json>
    cat whiteboard.json | python upload.py -

Environment:
    BOARDRAW_API_KEY  — your boardraw.com API key (or set in .env)
"""

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path


API_URL = "https://www.boardraw.com/api/keys/auth"


def load_api_key() -> str:
    key = os.environ.get("BOARDRAW_API_KEY", "")
    if not key:
        # Walk up from CWD looking for a .env file
        for directory in [Path.cwd(), *Path.cwd().parents]:
            env_file = directory / ".env"
            if env_file.is_file():
                for line in env_file.read_text().splitlines():
                    line = line.strip()
                    if line.startswith("BOARDRAW_API_KEY=") and not line.startswith("#"):
                        key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        break
            if key:
                break
    return key


def load_whiteboard(source: str) -> dict:
    if source == "-":
        raw = sys.stdin.read()
    else:
        raw = Path(source).read_text()
    return json.loads(raw)


def upload(whiteboard: dict, api_key: str) -> dict:
    payload = json.dumps({"whiteboard": whiteboard}).encode()
    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode()
        try:
            return {"_status": exc.code, **json.loads(body)}
        except json.JSONDecodeError:
            return {"_status": exc.code, "error": body}


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    api_key = load_api_key()
    if not api_key:
        print(
            "Error: BOARDRAW_API_KEY not found.\n"
            "Set it in your environment or add it to a .env file:\n"
            "  BOARDRAW_API_KEY=br_your_api_key_here",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        whiteboard = load_whiteboard(sys.argv[1])
    except FileNotFoundError:
        print(f"Error: file not found — {sys.argv[1]}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON — {exc}", file=sys.stderr)
        sys.exit(1)

    result = upload(whiteboard, api_key)
    status = result.pop("_status", 201)

    if status == 201 and result.get("success"):
        file_info = result["file"]
        user_info = result["user"]
        uuid = file_info["uuid"]
        print(f"✅ Uploaded successfully!")
        print(f"🔗 View online: https://www.boardraw.com/workspace/{uuid}")
        print(f"📁 File name:   {file_info['fileName']}")
        print(f"👤 Account:     {user_info['name']} ({user_info['email']})")
    elif status == 401:
        print(f"Error 401: {result.get('error', 'Unauthorized')}", file=sys.stderr)
        print("Check that your BOARDRAW_API_KEY is valid and not revoked.", file=sys.stderr)
        sys.exit(1)
    elif status == 403:
        print(f"Error 403: {result.get('error', 'Forbidden')}", file=sys.stderr)
        print("Upgrade to a Pro or Team plan at boardraw.com.", file=sys.stderr)
        sys.exit(1)
    elif status == 400:
        print(f"Error 400: {result.get('error', 'Bad Request')}", file=sys.stderr)
        print("The whiteboard JSON is invalid or missing required fields.", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"Unexpected response (HTTP {status}):", file=sys.stderr)
        print(json.dumps(result, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
