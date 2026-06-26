#!/usr/bin/env python3
"""
colab_run.py — Execute Python code on Google Colab runtimes.

Uses the same Colab API as colab-mcp but standalone, for use from OpenClaw skills/tools.

Usage:
    # Execute code
    python3 colab_run.py exec "print('hello')"
    
    # Execute code from file
    python3 colab_run.py exec-file script.py
    
    # Execute with GPU
    python3 colab_run.py exec --gpu "import torch; print(torch.cuda.is_available())"
    
    # List active runtimes
    python3 colab_run.py list
    
    # Stop runtime
    python3 colab_run.py stop <endpoint>
    
    # Check subscription/compute info
    python3 colab_run.py info

Auth: reads ~/.colab-mcp-auth-token.json (same as colab-mcp)
"""

import argparse
import json
import logging
import os
import sys
import uuid
from enum import Enum
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlparse

# Bootstrap venv if needed, then re-exec
VENV_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".colab-venv")
VENV_PYTHON = os.path.join(VENV_DIR, "bin", "python")

if not os.path.exists(VENV_PYTHON):
    import subprocess
    print("Bootstrapping .colab-venv...", file=sys.stderr)
    subprocess.check_call(["uv", "venv", VENV_DIR, "--python", "3.12"], stderr=subprocess.DEVNULL)
    subprocess.check_call([
        "uv", "pip", "install",
        "--python", VENV_PYTHON,
        "google-auth-oauthlib", "google-auth", "jupyter-kernel-client", "requests",
        "google-api-python-client",
    ])
    print("Venv ready.", file=sys.stderr)

if sys.executable != VENV_PYTHON:
    os.execv(VENV_PYTHON, [VENV_PYTHON] + sys.argv)

import requests
from google.auth.transport.requests import Request as GoogleRequest
from google.auth.transport import requests as google_requests
from google.oauth2.credentials import Credentials

# ─── Constants ───────────────────────────────────────────────────────────────

TOKEN_PATH = os.path.expanduser("~/.colab-mcp-auth-token.json")
COLAB_DOMAIN = "https://colab.research.google.com"
COLAB_API = "https://colab.pa.googleapis.com"
TUN_ENDPOINT = "/tun/m"
XSSI_PREFIX = ")]}'\n"
SCOPES = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/colaboratory",
    "openid",
]

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


# ─── Auth ────────────────────────────────────────────────────────────────────

def get_session() -> google_requests.AuthorizedSession:
    """Get an authorized session, refreshing token if needed."""
    if not os.path.exists(TOKEN_PATH):
        print(f"Error: No auth token at {TOKEN_PATH}", file=sys.stderr)
        print("Run: uvx git+https://github.com/googlecolab/colab-mcp -- -r", file=sys.stderr)
        sys.exit(1)

    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(GoogleRequest())
            with open(TOKEN_PATH, "w") as f:
                f.write(creds.to_json())
        else:
            print("Error: Token expired and no refresh token. Re-authenticate.", file=sys.stderr)
            sys.exit(1)

    return google_requests.AuthorizedSession(creds)


# ─── API helpers ─────────────────────────────────────────────────────────────

def strip_xssi(text: str) -> str:
    if text.startswith(XSSI_PREFIX):
        return text[len(XSSI_PREFIX):]
    return text


def colab_get(session, path: str, domain=COLAB_DOMAIN, params=None) -> Any:
    url = urljoin(domain, path)
    if params is None:
        params = {}
    if urlparse(url).hostname in urlparse(COLAB_DOMAIN).hostname:
        params["authuser"] = "0"
    headers = {
        "Accept": "application/json",
        "X-Goog-Colab-Client-Agent": "python-colab-client",
    }
    resp = session.get(url, headers=headers, params=params)
    if not resp.ok:
        log.error(f"GET {resp.url} → {resp.status_code}: {resp.text[:500]}")
        resp.raise_for_status()
    body = strip_xssi(resp.text)
    return json.loads(body) if body.strip() else None


def colab_post(session, path: str, xsrf_token: str, domain=COLAB_DOMAIN, params=None) -> Any:
    url = urljoin(domain, path)
    if params is None:
        params = {}
    if urlparse(url).hostname in urlparse(COLAB_DOMAIN).hostname:
        params["authuser"] = "0"
    headers = {
        "Accept": "application/json",
        "X-Goog-Colab-Client-Agent": "python-colab-client",
        "X-Goog-Colab-Token": xsrf_token,
    }
    resp = session.post(url, headers=headers, params=params)
    resp.raise_for_status()
    body = strip_xssi(resp.text)
    return json.loads(body) if body.strip() else None


def uuid_to_web_safe(u: uuid.UUID) -> str:
    s = str(u).replace("-", "_")
    return s + "." * (44 - len(str(u)))


# ─── Runtime management ─────────────────────────────────────────────────────

STATE_PATH = os.path.expanduser("~/.colab-runtime-state.json")


class ColabRuntime:
    def __init__(self, session, gpu=False):
        self.session = session
        self.gpu = gpu
        self.notebook_id = uuid.uuid4()
        self.endpoint = None
        self.proxy_url = None
        self.proxy_token = None
        self.kernel = None

    @classmethod
    def from_state(cls, session):
        """Restore a runtime from saved state file."""
        if not os.path.exists(STATE_PATH):
            return None
        with open(STATE_PATH) as f:
            state = json.load(f)
        rt = cls(session)
        rt.endpoint = state["endpoint"]
        rt.proxy_url = state["proxy_url"]
        rt.proxy_token = state["proxy_token"]
        rt.notebook_id = uuid.UUID(state["notebook_id"])
        return rt

    def save_state(self):
        """Save runtime state for later resume."""
        state = {
            "endpoint": self.endpoint,
            "proxy_url": self.proxy_url,
            "proxy_token": self.proxy_token,
            "notebook_id": str(self.notebook_id),
        }
        with open(STATE_PATH, "w") as f:
            json.dump(state, f)

    @staticmethod
    def clear_state():
        """Remove saved state file."""
        if os.path.exists(STATE_PATH):
            os.remove(STATE_PATH)

    def assign(self) -> dict:
        """Assign a Colab VM."""
        nbh = uuid_to_web_safe(self.notebook_id)
        get_params = {"nbh": nbh}

        # GET to get XSRF token (no GPU params — Colab rejects them on GET)
        get_resp = colab_get(self.session, f"{TUN_ENDPOINT}/assign", params=get_params)
        xsrf_token = get_resp.get("token")

        # POST with GPU params if requested
        post_params = {"nbh": nbh}
        if self.gpu:
            post_params["variant"] = "GPU"
            post_params["accelerator"] = self.gpu  # "T4", "A100", "L4", etc.

        post_resp = colab_post(self.session, f"{TUN_ENDPOINT}/assign", xsrf_token, params=post_params)

        self.endpoint = post_resp["endpoint"]
        proxy_info = post_resp.get("runtimeProxyInfo", {})
        self.proxy_url = proxy_info.get("url")
        self.proxy_token = proxy_info.get("token")

        return post_resp

    def connect_kernel(self):
        """Connect to the Jupyter kernel via jupyter-kernel-client."""
        from jupyter_kernel_client import KernelClient, JupyterSubprotocol

        self.kernel = KernelClient(
            server_url=self.proxy_url,
            token=self.proxy_token,
            client_kwargs={
                "subprotocol": JupyterSubprotocol.DEFAULT,
                "extra_params": {"colab-runtime-proxy-token": self.proxy_token},
            },
            headers={
                "X-Colab-Client-Agent": "colab-mcp",
                "X-Colab-Runtime-Proxy-Token": self.proxy_token,
            },
        )
        self.kernel.start()
        # Warm up
        self.kernel.execute("_colab_mcp = True")

    def execute(self, code: str) -> dict:
        """Execute code and return outputs."""
        if not self.kernel:
            raise RuntimeError("Kernel not connected. Call connect_kernel() first.")
        reply = self.kernel.execute(code)
        return reply

    def stop(self):
        """Unassign the VM."""
        if self.endpoint:
            try:
                get_resp = colab_get(
                    self.session,
                    f"{TUN_ENDPOINT}/unassign/{self.endpoint}",
                )
                xsrf_token = get_resp.get("token", "")
                colab_post(
                    self.session,
                    f"{TUN_ENDPOINT}/unassign/{self.endpoint}",
                    xsrf_token,
                )
                print(f"Unassigned {self.endpoint}")
            except Exception as e:
                print(f"Warning: unassign failed: {e}", file=sys.stderr)


def list_assignments(session) -> list:
    resp = colab_get(session, f"{TUN_ENDPOINT}/assignments")
    return resp.get("assignments", [])


def get_info(session) -> dict:
    result = {}
    try:
        result["user_info"] = colab_get(session, "v1/user-info", domain=COLAB_API)
    except Exception as e:
        result["user_info_error"] = str(e)
    try:
        result["ccu_info"] = colab_get(session, f"{TUN_ENDPOINT}/ccu-info")
    except Exception as e:
        result["ccu_info_error"] = str(e)
    return result


# ─── Output formatting ──────────────────────────────────────────────────────

def format_outputs(result: dict) -> str:
    """Format kernel execution result into readable text."""
    if not result:
        return "(no output)"
    
    outputs = result.get("outputs", [])
    if not outputs:
        # Check for direct text
        if isinstance(result, str):
            return result
        return "(no output)"
    
    parts = []
    for out in outputs:
        if isinstance(out, dict):
            # text/plain output
            if "text" in out:
                parts.append(out["text"])
            elif "data" in out:
                data = out["data"]
                if "text/plain" in data:
                    parts.append(data["text/plain"])
                if "image/png" in data:
                    parts.append("[image/png output]")
            elif "ename" in out:
                parts.append(f"ERROR: {out['ename']}: {out.get('evalue', '')}")
                if "traceback" in out:
                    for tb in out["traceback"]:
                        parts.append(tb)
        elif isinstance(out, str):
            parts.append(out)
    
    return "\n".join(parts) if parts else "(no output)"


# ─── CLI ─────────────────────────────────────────────────────────────────────

def cmd_exec(args):
    session = get_session()
    rt = ColabRuntime(session, gpu=args.gpu)

    print("Assigning Colab VM...", file=sys.stderr)
    info = rt.assign()
    accel = info.get("accelerator", "NONE")
    print(f"Assigned: {rt.endpoint} (accelerator={accel})", file=sys.stderr)

    print("Connecting to kernel...", file=sys.stderr)
    rt.connect_kernel()
    print("Connected.", file=sys.stderr)

    if args.code:
        code = args.code
    elif args.file:
        with open(args.file) as f:
            code = f.read()
    else:
        print("Error: provide code or --file", file=sys.stderr)
        sys.exit(1)

    print("Executing...", file=sys.stderr)
    result = rt.execute(code)
    print(format_outputs(result))

    if not args.keep:
        rt.stop()
        rt.clear_state()
    else:
        rt.save_state()
        print(f"Runtime kept alive. Resume with: colab_run.py resume \"code\"", file=sys.stderr)


def cmd_resume(args):
    """Execute code on a previously kept-alive runtime."""
    session = get_session()

    # Try to restore from state
    rt = ColabRuntime.from_state(session)
    if not rt:
        print("No saved runtime state. Use 'exec --keep' first.", file=sys.stderr)
        sys.exit(1)

    # Verify the runtime is still alive
    assignments = list_assignments(session)
    alive = any(a.get("endpoint") == rt.endpoint for a in assignments)
    if not alive:
        print(f"Runtime {rt.endpoint} is no longer active. Starting fresh.", file=sys.stderr)
        rt.clear_state()
        sys.exit(1)

    print(f"Resuming runtime: {rt.endpoint}", file=sys.stderr)
    print("Connecting to kernel...", file=sys.stderr)
    rt.connect_kernel()
    print("Connected.", file=sys.stderr)

    if args.code:
        code = args.code
    elif args.file:
        with open(args.file) as f:
            code = f.read()
    else:
        print("Error: provide code or --file", file=sys.stderr)
        sys.exit(1)

    print("Executing...", file=sys.stderr)
    result = rt.execute(code)
    print(format_outputs(result))

    if args.stop:
        rt.stop()
        rt.clear_state()
        print("Runtime stopped.", file=sys.stderr)
    else:
        rt.save_state()
        print(f"Runtime still alive. Resume again or stop with: colab_run.py stop {rt.endpoint}", file=sys.stderr)


def cmd_list(args):
    session = get_session()
    assignments = list_assignments(session)
    if not assignments:
        print("No active runtimes.")
        return
    for a in assignments:
        accel = a.get("accelerator", "NONE")
        endpoint = a.get("endpoint", "?")
        variant = a.get("variant", "?")
        print(f"  {endpoint}  accelerator={accel}  variant={variant}")


def cmd_stop(args):
    session = get_session()
    endpoint = args.endpoint

    # If no endpoint given, try the saved runtime
    if not endpoint:
        rt = ColabRuntime.from_state(session)
        if rt:
            endpoint = rt.endpoint
        else:
            print("No endpoint given and no saved runtime state.", file=sys.stderr)
            sys.exit(1)

    try:
        get_resp = colab_get(session, f"{TUN_ENDPOINT}/unassign/{endpoint}")
        xsrf_token = get_resp.get("token", "")
        colab_post(session, f"{TUN_ENDPOINT}/unassign/{endpoint}", xsrf_token)
        print(f"Unassigned {endpoint}")
        ColabRuntime.clear_state()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)


def cmd_info(args):
    session = get_session()
    info = get_info(session)
    print(json.dumps(info, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Execute code on Google Colab")
    sub = parser.add_subparsers(dest="command")

    p_exec = sub.add_parser("exec", help="Execute code on Colab")
    p_exec.add_argument("code", nargs="?", help="Python code to execute")
    p_exec.add_argument("--file", "-f", help="Execute code from file")
    p_exec.add_argument("--gpu", nargs="?", const="T4", default=None,
                        help="Request GPU runtime (default: T4). Options: T4, L4, A100")
    p_exec.add_argument("--keep", action="store_true", help="Keep runtime alive after execution")
    p_exec.set_defaults(func=cmd_exec)

    p_resume = sub.add_parser("resume", help="Execute code on a kept-alive runtime")
    p_resume.add_argument("code", nargs="?", help="Python code to execute")
    p_resume.add_argument("--file", "-f", help="Execute code from file")
    p_resume.add_argument("--stop", action="store_true", help="Stop runtime after execution")
    p_resume.set_defaults(func=cmd_resume)

    p_list = sub.add_parser("list", help="List active runtimes")
    p_list.set_defaults(func=cmd_list)

    p_stop = sub.add_parser("stop", help="Stop a runtime")
    p_stop.add_argument("endpoint", nargs="?", help="Runtime endpoint (or omit to stop saved runtime)")
    p_stop.set_defaults(func=cmd_stop)

    p_info = sub.add_parser("info", help="Show account/compute info")
    p_info.set_defaults(func=cmd_info)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()
