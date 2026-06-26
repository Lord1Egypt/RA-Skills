#!/usr/bin/env python3
"""
Clawdos CLI - Standalone Windows Automation Client

Usage:
    python clawdos.py health
    python clawdos.py window_list
    python clawdos.py click --args '{"x": 100, "y": 200}'
    ...
"""

import os
import sys
import json
import base64
import argparse
import requests
from pathlib import Path

# Standard OpenClaw injected environment variables via SKILL.md metadata
BASE_URL = os.getenv("CLAWDOS_BASE_URL", "http://127.0.0.1:17171")
API_KEY = os.getenv("CLAWDOS_API_KEY", "")
TIMEOUT = int(os.getenv("CLAWDOS_TIMEOUT", "30"))
FS_ROOT_ID = int(os.getenv("CLAWDOS_FS_ROOT_ID", "0"))

def get_headers(auth=True):
    if auth:
        if not API_KEY:
            print(json.dumps({"error": "CLAWDOS_API_KEY environment variable is not set. Please configure the skill in OpenClaw."}), file=sys.stderr)
            sys.exit(1)
        return {"X-Api-Key": API_KEY}
    return {}

def api_get(path, params=None, auth=True):
    url = f"{BASE_URL}{path}"
    resp = requests.get(url, params=params, headers=get_headers(auth), timeout=TIMEOUT)
    resp.raise_for_status()
    return resp

def api_post(path, payload):
    url = f"{BASE_URL}{path}"
    resp = requests.post(url, json=payload, headers=get_headers(True), timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()

def main():
    parser = argparse.ArgumentParser(description="Clawdos REST API CLI")
    parser.add_argument("action", help="Action to perform (e.g., health, get_env, window_list, window_focus, screen_capture, click, move, type_text, fs_list, shell_exec, etc.)")
    parser.add_argument("--args", type=str, default="{}", help="JSON dictionary of arguments for the action")
    parser.add_argument("--out", type=str, help="Output file path (for saving images or binary data)")
    parser.add_argument("--file", type=str, help="Input file path (e.g. for reading local file to fs_write)")

    args = parser.parse_args()
    action = args.action
    
    try:
        kwargs = json.loads(args.args)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON in --args: {e}"}), file=sys.stderr)
        sys.exit(1)

    try:
        if action == "health":
            res = api_get("/v1/health", auth=False).json()
        elif action == "get_env":
            res = api_get("/v1/env").json()
        elif action == "window_list":
            res = api_get("/v1/window/list").json()
        elif action == "window_focus":
            res = api_post("/v1/window/focus", kwargs)
        elif action == "screen_capture":
            resp = api_get("/v1/screen/capture", params=kwargs)
            res_bytes = resp.content
            ct = resp.headers.get("Content-Type", "image/png")
            if args.out:
                with open(args.out, "wb") as f:
                    f.write(res_bytes)
                res = {"success": True, "saved_to": args.out, "content_type": ct}
            else:
                b64 = base64.b64encode(res_bytes).decode("ascii")
                # For stdout, return full base64 so agents can read it
                print(json.dumps({"success": True, "content_type": ct, "image_base64": b64}))
                return
        elif action == "click":
            res = api_post("/v1/input/click", kwargs)
        elif action == "move":
            res = api_post("/v1/input/move", kwargs)
        elif action == "drag":
            res = api_post("/v1/input/drag", kwargs)
        elif action == "keys":
            res = api_post("/v1/input/keys", kwargs)
        elif action == "type_text":
            res = api_post("/v1/input/type", kwargs)
        elif action == "scroll":
            res = api_post("/v1/input/scroll", kwargs)
        elif action == "batch":
            res = api_post("/v1/input/batch", kwargs)
        elif action == "fs_list":
            if "rootId" not in kwargs: kwargs["rootId"] = FS_ROOT_ID
            res = api_get("/v1/fs/list", params=kwargs).json()
        elif action == "fs_read":
            if "rootId" not in kwargs: kwargs["rootId"] = FS_ROOT_ID
            raw = api_get("/v1/fs/read", params=kwargs).json()
            b_data = base64.b64decode(raw["data"])
            if args.out:
                with open(args.out, "wb") as f:
                    f.write(b_data)
                res = {"success": True, "saved_to": args.out}
            else:
                try:
                    res = b_data.decode("utf-8")
                    print(res)
                    return
                except UnicodeDecodeError:
                    print(json.dumps({"error": "File is binary, use --out to save it"}), file=sys.stderr)
                    sys.exit(1)
        elif action == "fs_write":
            if "rootId" not in kwargs: kwargs["rootId"] = FS_ROOT_ID
            if args.file:
                with open(args.file, "rb") as f:
                    b_data = f.read()
                kwargs["data"] = base64.b64encode(b_data).decode("ascii")
                kwargs["encoding"] = "base64"
            elif "content" in kwargs:
                content = kwargs.pop("content")
                kwargs["data"] = base64.b64encode(content.encode("utf-8")).decode("ascii")
                kwargs["encoding"] = "base64"
            res = api_post("/v1/fs/write", kwargs)
        elif action == "fs_mkdir":
            if "rootId" not in kwargs: kwargs["rootId"] = FS_ROOT_ID
            res = api_post("/v1/fs/mkdir", kwargs)
        elif action == "fs_delete":
            if "rootId" not in kwargs: kwargs["rootId"] = FS_ROOT_ID
            res = api_post("/v1/fs/delete", kwargs)
        elif action == "fs_move":
            if "rootId" not in kwargs: kwargs["rootId"] = FS_ROOT_ID
            res = api_post("/v1/fs/move", kwargs)
        elif action == "shell_exec":
            res = api_post("/v1/shell/exec", kwargs)
        else:
            print(json.dumps({"error": f"Unknown action: {action}"}), file=sys.stderr)
            sys.exit(1)
            
        print(json.dumps(res, indent=2))
        
    except requests.exceptions.RequestException as e:
        details = str(e)
        if hasattr(e, "response") and e.response is not None:
            try:
                details += " | Response: " + e.response.text
            except Exception:
                pass
        print(json.dumps({"error": "Request failed", "details": details}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
