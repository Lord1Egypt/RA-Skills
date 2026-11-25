"""Narrow codecs for configuration formats that can be safely preserved."""
from __future__ import annotations
import json
import re
import tomllib
from agent_clients import McpServerSpec


class UnsupportedConfigFormat(ValueError):
    pass


def render_codex_toml(source: str, spec: McpServerSpec) -> str:
    """Append a new Codex MCP table only after parse validation.

    `tomllib` provides no round-trip writer, so this deliberately never rewrites
    existing tables. An existing target table or malformed TOML is manual-only.
    """
    try:
        parsed = tomllib.loads(source)
    except tomllib.TOMLDecodeError as exc:
        raise UnsupportedConfigFormat("invalid TOML; refusing lossy rewrite") from exc
    key = spec.name.replace("-", "_")
    if not re.fullmatch(r"[a-z][a-z0-9_]{0,62}", key):
        raise UnsupportedConfigFormat("server name cannot become a safe TOML key")
    header = f"[mcp_servers.{key}]"
    servers = parsed.get("mcp_servers", {})
    if not isinstance(servers, dict) or key in servers:
        raise UnsupportedConfigFormat("target MCP table already exists")
    args = ", ".join(json.dumps(arg) for arg in spec.args)
    suffix = "" if not source or source.endswith("\n") else "\n"
    return source + suffix + f"\n{header}\ncommand = {json.dumps(spec.command)}\nargs = [{args}]\ncwd = {json.dumps(str(spec.cwd))}\n"


def patch_jsonc(source: str, spec: McpServerSpec) -> str:
    """Fail closed until a reviewed comment-preserving writer is bundled."""
    del source, spec
    raise UnsupportedConfigFormat("JSONC is manual-export-only because comment preservation is not proven")
