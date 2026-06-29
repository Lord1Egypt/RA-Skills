#!/usr/bin/env python3
"""Build, upload, and deploy a FastEdge Rust Wasm app.

Requires the `requests` package and (for upload/deploy) GCORE_API_KEY.
"""
import glob
import os
import shutil
import subprocess
import sys

API_BASE = "https://api.gcore.com/fastedge/v1"


def _toolchain():
    """Resolve cargo + rustc, preferring rustup's toolchain.

    A Homebrew/distro `cargo` first on PATH may lack the wasm32-wasip1 target
    even when `rustup target add` reports it installed (the target lives in the
    rustup toolchain). Resolving via `rustup which` avoids that shadowing.
    Honors explicit CARGO / RUSTC env overrides.
    """
    cargo = os.environ.get("CARGO") or "cargo"
    rustc = os.environ.get("RUSTC")
    if (not os.environ.get("CARGO") or not rustc) and shutil.which("rustup"):
        try:
            if not os.environ.get("CARGO"):
                cargo = subprocess.check_output(
                    ["rustup", "which", "cargo"], text=True).strip() or cargo
            if not rustc:
                rustc = subprocess.check_output(
                    ["rustup", "which", "rustc"], text=True).strip() or None
        except subprocess.CalledProcessError:
            pass
    return cargo, rustc


def _requests():
    """Import requests lazily so `build` works without it installed."""
    try:
        import requests
    except ImportError:
        sys.exit("Error: the 'requests' package is required for upload/deploy "
                 "(uv pip install requests)")
    return requests


def _api_key():
    key = os.environ.get("GCORE_API_KEY")
    if not key:
        sys.exit("Error: GCORE_API_KEY environment variable not set")
    return key


def _json_headers():
    return {
        "Authorization": f"APIKey {_api_key()}",
        "Content-Type": "application/json",
        "accept": "application/json",
    }


def build():
    """Build the release Wasm binary and return its path."""
    cargo, rustc = _toolchain()
    subprocess.run(["rustup", "target", "add", "wasm32-wasip1"],
                   capture_output=True, text=True)

    env = dict(os.environ)
    if rustc:
        env["RUSTC"] = rustc
    result = subprocess.run([cargo, "build", "--release"],
                            capture_output=True, text=True, env=env)
    if result.returncode != 0:
        sys.exit(f"Build failed:\n{result.stderr}")

    name = os.path.basename(os.getcwd()).replace("-", "_")
    wasm_path = f"target/wasm32-wasip1/release/{name}.wasm"
    if not os.path.exists(wasm_path):
        matches = glob.glob("target/wasm32-wasip1/release/*.wasm")
        if not matches:
            sys.exit("No .wasm file found in target/wasm32-wasip1/release/")
        wasm_path = matches[0]

    print(f"✓ Built: {wasm_path} ({os.path.getsize(wasm_path):,} bytes)")
    return wasm_path


def upload(wasm_path):
    """Upload a Wasm binary and return its binary id."""
    if not os.path.exists(wasm_path):
        sys.exit(f"Error: {wasm_path} not found")
    requests = _requests()
    with open(wasm_path, "rb") as f:
        resp = requests.post(
            f"{API_BASE}/binaries/raw",
            headers={"Authorization": f"APIKey {_api_key()}",
                     "Content-Type": "application/octet-stream",
                     "accept": "application/json"},
            data=f.read(),
        )
    if resp.status_code not in (200, 201):
        sys.exit(f"Upload error: {resp.status_code} - {resp.text}")
    binary_id = resp.json().get("id")
    print(f"✓ Uploaded binary id: {binary_id}")
    return binary_id


def deploy(binary_id, app_name=None, app_id=None):
    """Create a new app, or update an existing one when app_id is given."""
    requests = _requests()
    if app_id:
        resp = requests.put(
            f"{API_BASE}/apps/{app_id}",
            headers=_json_headers(),
            json={"binary": binary_id, "status": 1, "name": app_name},
        )
    else:
        resp = requests.post(
            f"{API_BASE}/apps",
            headers={**_json_headers(), "client_id": "0"},
            json={"name": app_name, "binary": binary_id, "status": 1},
        )

    if resp.status_code not in (200, 201):
        sys.exit(f"Error: {resp.status_code} - {resp.text}")
    data = resp.json()
    print(f"✓ Deployed: {data.get('url')}")
    print(f"  App ID: {data.get('id')}")


def _parse_opts(argv):
    opts = {}
    i = 0
    while i < len(argv):
        if argv[i].startswith("--") and i + 1 < len(argv):
            opts[argv[i][2:].replace("-", "_")] = argv[i + 1]
            i += 2
        else:
            i += 1
    return opts


USAGE = """Usage: build_rust.py COMMAND [OPTIONS]

  build                                 Build the Wasm binary
  upload [--wasm PATH]                  Upload a binary, print its id
  deploy --binary-id ID --app-name N    Create a new app
  deploy --binary-id ID --app-id ID --app-name N   Update an existing app
  release --app-name N [--app-id ID]    Build + upload + deploy in one step
"""


def main():
    if len(sys.argv) < 2:
        sys.exit(USAGE)

    cmd, opts = sys.argv[1], _parse_opts(sys.argv[2:])

    if cmd == "build":
        build()
    elif cmd == "upload":
        upload(opts.get("wasm") or build())
    elif cmd == "deploy":
        if "binary_id" not in opts:
            sys.exit("Error: --binary-id required for deploy")
        deploy(int(opts["binary_id"]), opts.get("app_name"),
               int(opts["app_id"]) if "app_id" in opts else None)
    elif cmd == "release":
        if "app_name" not in opts:
            sys.exit("Error: --app-name required for release")
        binary_id = upload(build())
        deploy(binary_id, opts["app_name"],
               int(opts["app_id"]) if "app_id" in opts else None)
    else:
        sys.exit(f"Unknown command: {cmd}\n\n{USAGE}")


if __name__ == "__main__":
    main()
