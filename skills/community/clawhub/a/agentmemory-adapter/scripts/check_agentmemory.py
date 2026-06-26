#!/usr/bin/env python3
"""Check a local AgentMemory integration without printing secrets."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


HOME = Path.home()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        return {"__error__": f"invalid JSON: {exc}"}


def is_loopback_http(url: str) -> bool:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    return parsed.scheme == "http" and host in {"localhost", "127.0.0.1", "::1"}


def can_send_secret(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" or is_loopback_http(url)


def probe(url: str, path: str, timeout: float, send_secret: bool) -> tuple[bool, str]:
    target = f"{url.rstrip('/')}{path}"
    req = urllib.request.Request(target, headers={})
    secret = os.environ.get("AGENTMEMORY_SECRET") if send_secret else None
    if secret:
        req.add_header("Authorization", f"Bearer {secret}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as res:
            body = res.read(4096).decode("utf-8", errors="replace")
            return 200 <= res.status < 300, f"HTTP {res.status}: {body[:240]}"
    except urllib.error.HTTPError as exc:
        body = exc.read(512).decode("utf-8", errors="replace")
        return False, f"HTTP {exc.code}: {body[:160]}"
    except Exception as exc:  # noqa: BLE001 - diagnostic script reports all failures.
        return False, f"{type(exc).__name__}: {exc}"


def check_codex(results: list[dict[str, str]]) -> None:
    config = read_text(HOME / ".codex" / "config.toml")
    hooks = read_json(HOME / ".codex" / "hooks.json")
    plugin_cache = HOME / ".codex" / "plugins" / "cache"

    if "[mcp_servers.agentmemory]" in config:
        in_block = False
        command_line = ""
        for line in config.splitlines():
            stripped = line.strip()
            if stripped == "[mcp_servers.agentmemory]":
                in_block = True
                continue
            if in_block and stripped.startswith("["):
                break
            if in_block and stripped.startswith("command ="):
                command_line = stripped
                break
        status = "ok" if "agentmemory" in command_line else "warn"
        results.append({"area": "codex", "status": status, "message": f"MCP configured ({command_line or 'command unknown'})"})
    else:
        results.append({"area": "codex", "status": "warn", "message": "missing [mcp_servers.agentmemory] in ~/.codex/config.toml"})

    if isinstance(hooks, dict) and "agentmemory" in json.dumps(hooks):
        results.append({"area": "codex", "status": "ok", "message": "~/.codex/hooks.json includes AgentMemory hook commands"})
    elif isinstance(hooks, dict) and "__error__" in hooks:
        results.append({"area": "codex", "status": "warn", "message": f"invalid ~/.codex/hooks.json: {hooks['__error__']}"})
    elif hooks:
        results.append({"area": "codex", "status": "warn", "message": "~/.codex/hooks.json exists but no AgentMemory hooks were found"})
    else:
        results.append({"area": "codex", "status": "warn", "message": "no ~/.codex/hooks.json hook fallback found"})

    cache_hits = list(plugin_cache.glob("*/agentmemory/*/.mcp.json")) if plugin_cache.exists() else []
    results.append({"area": "codex", "status": "ok" if cache_hits else "info", "message": f"Codex plugin cache entries: {len(cache_hits)}"})


def check_openclaw(results: list[dict[str, str]]) -> None:
    cfg = read_json(HOME / ".openclaw" / "openclaw.json")
    if isinstance(cfg, dict) and "__error__" in cfg:
        results.append({"area": "openclaw", "status": "warn", "message": f"invalid ~/.openclaw/openclaw.json: {cfg['__error__']}"})
        return
    if not isinstance(cfg, dict):
        results.append({"area": "openclaw", "status": "info", "message": "no readable ~/.openclaw/openclaw.json"})
        return

    server = (((cfg.get("mcp") or {}).get("servers") or {}).get("agentmemory") or {})
    if server:
        cmd = server.get("command", "")
        results.append({"area": "openclaw", "status": "ok", "message": f"MCP configured ({cmd})"})
    else:
        results.append({"area": "openclaw", "status": "warn", "message": "missing mcp.servers.agentmemory"})

    plugins = cfg.get("plugins") or {}
    slot = (plugins.get("slots") or {}).get("memory")
    entry = (plugins.get("entries") or {}).get("agentmemory") or {}
    paths = (plugins.get("load") or {}).get("paths") or []
    durable_paths = [p for p in paths if "tmp" not in str(p)]
    if slot == "agentmemory" and entry.get("enabled") is True:
        results.append({"area": "openclaw", "status": "ok", "message": "memory slot points at enabled agentmemory plugin"})
    else:
        results.append({"area": "openclaw", "status": "warn", "message": f"memory slot={slot!r}, enabled={entry.get('enabled')!r}"})
    if durable_paths:
        results.append({"area": "openclaw", "status": "ok", "message": f"durable plugin paths: {len(durable_paths)}"})
    elif paths:
        results.append({"area": "openclaw", "status": "warn", "message": "plugin paths exist but appear temporary"})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=os.environ.get("AGENTMEMORY_URL", "http://localhost:3111"))
    parser.add_argument("--timeout", type=float, default=1.5)
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args()

    results: list[dict[str, str]] = []
    found = shutil.which("agentmemory")
    fallback = HOME / ".local" / "bin" / "agentmemory"
    if found or fallback.exists():
        results.append({"area": "binary", "status": "ok", "message": f"agentmemory command: {found or fallback}"})
    else:
        results.append({"area": "binary", "status": "warn", "message": "agentmemory command not found"})

    check_codex(results)
    check_openclaw(results)

    send_secret = bool(os.environ.get("AGENTMEMORY_SECRET")) and can_send_secret(args.url)
    if os.environ.get("AGENTMEMORY_SECRET") and not send_secret:
        results.append({"area": "security", "status": "warn", "message": "AGENTMEMORY_SECRET is set for non-loopback HTTP; refusing to send it without HTTPS"})

    for endpoint in ("/agentmemory/livez", "/agentmemory/health"):
        ok, message = probe(args.url, endpoint, args.timeout, send_secret)
        results.append({"area": "server", "status": "ok" if ok else "warn", "message": f"{endpoint}: {message}"})

    if args.json_output:
        print(json.dumps(results, indent=2))
    else:
        for item in results:
            print(f"[{item['status'].upper()}] {item['area']}: {item['message']}")
    return 1 if any(item["status"] == "warn" for item in results) else 0


if __name__ == "__main__":
    sys.exit(main())
