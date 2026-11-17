#!/usr/bin/env python3
"""Manage the cross-agent runtime for dlazy-ppt.

The runtime lives outside any specific agent installation so Codex, Claude Code,
OpenClaw, Hermes Agent, and other local agents can share one virtual
environment and one dLazy API configuration.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import Dict, Iterable, Optional
import urllib.error
import urllib.request
import venv


DEFAULT_RUNTIME_HOME = "~/.dlazy-ppt"
DEFAULT_MODEL = "gpt-image-2"
DEFAULT_BASE_URL = "https://dlazy.com"
ENV_FIELDS = ("DLAZY_API_KEY", "DLAZY_BASE_URL", "DLAZY_PPT_IMAGE_MODEL")

# Must match dlazy_client.CLI_VERSION: the tool API answers 426 without it.
CLI_VERSION = "1.2.3"
API_KEY_URL = "https://dlazy.com/dashboard/organization/api-key"


def _runtime_home() -> Path:
    return Path(os.getenv("DLAZY_PPT_HOME", DEFAULT_RUNTIME_HOME)).expanduser()


def _skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _venv_python(home: Path) -> Path:
    if os.name == "nt":
        return home / ".venv" / "Scripts" / "python.exe"
    return home / ".venv" / "bin" / "python"


def _env_path(home: Path) -> Path:
    return home / ".env"


def _requirements_path() -> Path:
    return _skill_root() / "requirements.txt"


def _die(message: str, code: int = 1) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(code)


def _mask_secret(value: str) -> str:
    if not value:
        return ""
    if len(value) <= 8:
        return "****"
    return f"{value[:4]}...{value[-4:]}"


def _parse_env_file(path: Path) -> Dict[str, str]:
    if not path.exists():
        return {}
    values: Dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            values[key] = value
    return values


def _quote_env_value(value: str) -> str:
    if not value:
        return ""
    if any(ch.isspace() for ch in value) or "#" in value or '"' in value:
        return json.dumps(value)
    return value


def _write_env_file(path: Path, values: Dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# dlazy-ppt shared runtime configuration",
        "# Used by Codex, Claude Code, OpenClaw, Hermes Agent, and other local agents.",
    ]
    for key in ENV_FIELDS:
        value = values.get(key, "")
        if value:
            lines.append(f"{key}={_quote_env_value(value)}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    try:
        path.chmod(stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass


def _load_env_values(home: Path) -> Dict[str, str]:
    values = _parse_env_file(_env_path(home))
    for key in ENV_FIELDS:
        if os.getenv(key):
            values[key] = os.environ[key]
    return values


def _ensure_dirs(home: Path) -> None:
    for child in (home, home / "cache", home / "logs"):
        child.mkdir(parents=True, exist_ok=True)


def _bootstrap(args: argparse.Namespace) -> int:
    home = _runtime_home()
    _ensure_dirs(home)
    python = _venv_python(home)
    if not python.exists():
        print(f"Creating virtual environment: {home / '.venv'}")
        venv.EnvBuilder(with_pip=True, clear=False).create(home / ".venv")
    else:
        print(f"Virtual environment already exists: {home / '.venv'}")

    requirements = _requirements_path()
    if not requirements.exists():
        _die(f"requirements.txt not found: {requirements}")

    cmd = [str(python), "-m", "pip", "install", "-r", str(requirements)]
    if args.upgrade:
        cmd.insert(4, "-U")
    print(f"Installing dependencies from: {requirements}")
    subprocess.run(cmd, check=True)
    print(f"Runtime ready: {home}")
    return 0


def _config(args: argparse.Namespace) -> int:
    home = _runtime_home()
    _ensure_dirs(home)
    env_file = _env_path(home)
    values = _parse_env_file(env_file)

    if args.api_key:
        values["DLAZY_API_KEY"] = args.api_key.strip()

    if args.base_url is not None:
        values["DLAZY_BASE_URL"] = args.base_url.strip()
    if args.model is not None:
        values["DLAZY_PPT_IMAGE_MODEL"] = args.model.strip()

    if args.clear_base_url:
        values.pop("DLAZY_BASE_URL", None)

    _write_env_file(env_file, values)
    print(f"Wrote {env_file}")
    for key in ENV_FIELDS:
        value = values.get(key, "")
        if key == "DLAZY_API_KEY":
            value = _mask_secret(value)
        print(f"{key}={value or '<unset>'}")
    return 0


def _check_python_imports(python: Path) -> bool:
    if not python.exists():
        print(f"venv: missing ({python})")
        return False
    code = "import requests, PIL, pptx; print('imports ok')"
    proc = subprocess.run(
        [str(python), "-c", code],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if proc.returncode != 0:
        print("dependencies: missing or broken")
        if proc.stderr.strip():
            print(proc.stderr.strip())
        return False
    print("dependencies: ok")
    return True


def _manifest_request(base_url: str, api_key: str, timeout: int) -> Optional[dict]:
    """Fetch the tool manifest - the cheapest call that proves the key works."""
    endpoint = base_url.rstrip("/") + "/api/cli/tool/manifest"
    req = urllib.request.Request(
        endpoint,
        headers={
            "Authorization": f"Bearer {api_key}",
            "X-CLI-Version": CLI_VERSION,
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            print(f"tool manifest: HTTP {resp.status}")
            return json.loads(resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as exc:
        body = exc.read(800).decode("utf-8", "replace")
        print(f"tool manifest: HTTP {exc.code}")
        if exc.code == 401:
            print(f"The API key was rejected. Get a valid key from {API_KEY_URL}.")
        if body:
            print(body)
        return None
    except Exception as exc:
        print(f"tool manifest: {exc.__class__.__name__}: {exc}")
        return None


def _doctor(args: argparse.Namespace) -> int:
    home = _runtime_home()
    env_file = _env_path(home)
    print(f"runtime home: {home}")
    print(f"env file: {env_file} ({'exists' if env_file.exists() else 'missing'})")
    print(f"venv python: {_venv_python(home)}")

    ok = True
    ok = _check_python_imports(_venv_python(home)) and ok

    values = _load_env_values(home)
    api_key = values.get("DLAZY_API_KEY", "")
    base_url = values.get("DLAZY_BASE_URL", DEFAULT_BASE_URL)
    model = values.get("DLAZY_PPT_IMAGE_MODEL", DEFAULT_MODEL)

    print(f"DLAZY_API_KEY={'set (' + _mask_secret(api_key) + ')' if api_key else '<unset>'}")
    print(f"DLAZY_BASE_URL={base_url}")
    print(f"DLAZY_PPT_IMAGE_MODEL={model}")

    if not api_key:
        print(f"api key: missing, get one from {API_KEY_URL}")
        ok = False

    if args.check_api:
        if not api_key:
            print("api check: skipped, DLAZY_API_KEY is unset")
        else:
            manifest = _manifest_request(base_url, api_key, args.timeout)
            if manifest is None:
                ok = False
            else:
                # The manifest is the authority on which tools this account can
                # run, so a mistyped or unavailable model is caught here rather
                # than as a 400 halfway through a deck.
                names = {t.get("cli_name") or t.get("id") for t in manifest.get("tools", [])}
                if model in names:
                    print(f"model check: ok, {model} is available on this account")
                else:
                    print(f"model check: {model} is not in this account's tool manifest")
                    ok = False

    return 0 if ok else 1


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage the dlazy-ppt shared runtime")
    subparsers = parser.add_subparsers(dest="command", required=True)

    bootstrap = subparsers.add_parser("bootstrap", help="Create shared venv and install deps")
    bootstrap.add_argument("--upgrade", action="store_true")
    bootstrap.set_defaults(func=_bootstrap)

    config = subparsers.add_parser("config", help="Write or update the shared .env")
    config.add_argument("--api-key", help=f"dLazy API key from {API_KEY_URL}")
    config.add_argument("--base-url", help="Override the dLazy base URL (self-hosted deployments)")
    config.add_argument("--clear-base-url", action="store_true")
    config.add_argument("--model", help="dLazy image tool to use (default: gpt-image-2)")
    config.set_defaults(func=_config)

    doctor = subparsers.add_parser("doctor", help="Check runtime and optional API access")
    doctor.add_argument("--check-api", action="store_true")
    doctor.add_argument("--timeout", type=int, default=30)
    doctor.set_defaults(func=_doctor)

    return parser


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
