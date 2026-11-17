"""mcp2skill — Extract MCP server tools and generate equivalent Agent Skills.

Connects to an MCP server, sends initialize + tools/list, extracts tool
schemas, and generates a skill that teaches the agent to achieve the same
results without the MCP server running.

Usage:
    cli2skill mcp <command> [args...] --name <skill-name>
    cli2skill mcp --config <settings.json> --server <name> --name <skill-name>
"""
from __future__ import annotations

import json
import subprocess
import sys
import os
from dataclasses import dataclass


@dataclass
class McpTool:
    name: str
    description: str
    parameters: dict  # JSON Schema


def connect_and_extract(
    command: list[str],
    env: dict[str, str] | None = None,
    timeout: int = 30,
) -> list[McpTool]:
    """Spawn an MCP server, handshake, extract tools, kill it."""
    merged_env = {**os.environ, **(env or {})}

    # Build the JSON-RPC messages
    init_req = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "mcp2skill", "version": "0.1.0"},
        },
    })
    init_notif = json.dumps({
        "jsonrpc": "2.0",
        "method": "notifications/initialized",
    })
    list_req = json.dumps({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {},
    })

    stdin_data = f"{init_req}\n{init_notif}\n{list_req}\n"

    # On Windows, commands like npx/node need shell=True or .cmd suffix
    use_shell = sys.platform == "win32"
    proc = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=merged_env,
        shell=use_shell,
    )

    try:
        stdout, stderr = proc.communicate(
            input=stdin_data.encode(), timeout=timeout
        )
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
        raise RuntimeError(f"MCP server timed out after {timeout}s")

    # Parse responses (one JSON per line)
    tools = []
    for line in stdout.decode("utf-8", errors="replace").strip().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            resp = json.loads(line)
        except json.JSONDecodeError:
            continue

        # Look for tools/list response (id=2)
        if resp.get("id") == 2 and "result" in resp:
            raw_tools = resp["result"].get("tools", [])
            for t in raw_tools:
                tools.append(McpTool(
                    name=t.get("name", "unknown"),
                    description=t.get("description", ""),
                    parameters=t.get("inputSchema", {}),
                ))
    return tools


def extract_from_config(
    settings_path: str, server_name: str
) -> tuple[list[str], dict[str, str]]:
    """Read MCP server config from Claude Code settings.json."""
    with open(settings_path, encoding="utf-8") as f:
        settings = json.load(f)

    servers = settings.get("mcpServers", {})
    if server_name not in servers:
        available = list(servers.keys())
        raise ValueError(
            f"Server '{server_name}' not found. Available: {available}"
        )

    cfg = servers[server_name]
    command = [cfg["command"]] + cfg.get("args", [])
    env = {}
    for k, v in cfg.get("env", {}).items():
        # Expand ${VAR} references
        if v.startswith("${") and v.endswith("}"):
            env_name = v[2:-1]
            env[k] = os.environ.get(env_name, v)
        else:
            env[k] = v
    return command, env


def generate_mcp_skill(
    tools: list[McpTool],
    name: str,
    description: str | None = None,
    hint: str | None = None,
) -> str:
    """Generate a SKILL.md from extracted MCP tools."""
    desc = description or f"Extracted from MCP server — {len(tools)} tools"
    lines: list[str] = []

    # Frontmatter
    lines.append("---")
    lines.append(f"name: {name}")
    lines.append(f"description: {desc[:100]}")
    lines.append("user-invocable: false")
    lines.append("allowed-tools: Bash(*)")
    lines.append("---")
    lines.append("")
    lines.append(f"# {name}")
    lines.append("")
    lines.append(f"{desc}")
    lines.append("")

    if hint:
        lines.append(f"> **Implementation hint**: {hint}")
        lines.append("")

    lines.append(f"## Tools ({len(tools)})")
    lines.append("")

    for tool in tools:
        lines.append(f"### {tool.name}")
        if tool.description:
            lines.append(tool.description)
        lines.append("")

        # Parameters
        props = tool.parameters.get("properties", {})
        required = tool.parameters.get("required", [])
        if props:
            lines.append("**Parameters:**")
            for pname, pschema in props.items():
                ptype = pschema.get("type", "any")
                pdesc = pschema.get("description", "")
                req = " **(required)**" if pname in required else ""
                default = ""
                if "default" in pschema:
                    default = f" (default: {pschema['default']})"
                if "enum" in pschema:
                    default += f" enum: {pschema['enum']}"
                lines.append(f"- `{pname}` ({ptype}{req}): {pdesc}{default}")
            lines.append("")

    # When to use
    lines.append("## When to use")
    lines.append(f"- {desc}")
    tool_names = ", ".join(f"`{t.name}`" for t in tools[:8])
    lines.append(f"- Available operations: {tool_names}")
    if len(tools) > 8:
        lines.append(f"- ... and {len(tools) - 8} more")
    lines.append("")

    return "\n".join(lines)
