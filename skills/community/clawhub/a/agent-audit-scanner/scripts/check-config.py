#!/usr/bin/env python3
"""Audit OpenClaw configuration files for security risks.

Checks ~/.openclaw/openclaw.json and .mcp.json files for dangerous settings.
Uses BLOCK/WARN/INFO tiers consistent with Agent Audit output.

Usage: python3 check-config.py
Exit codes: 0=CLEAN, 1=WARNINGS, 2=CRITICAL
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


# ─── Constants (aligned with Agent Audit's MCPConfigScanner) ─────────────────

OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"
MCP_SEARCH_PATHS = [
    Path.home() / ".openclaw" / "workspace" / ".mcp.json",
    Path.home() / ".openclaw" / ".mcp.json",
    Path.home() / ".openclaw" / "workspace" / "mcp.json",
]

SENSITIVE_ENV_PATTERN = re.compile(
    r"(?i)(key|secret|token|password|credential|auth|private)"
)

SAFE_ENV_KEYS = {
    "PATH", "NODE_ENV", "LOG_LEVEL", "DEBUG", "VERBOSE",
    "HOME", "USER", "SHELL", "TERM", "LANG", "LC_ALL",
    "TZ", "EDITOR", "DISPLAY", "XDG_RUNTIME_DIR",
    "TMPDIR", "TEMP", "TMP", "COLORTERM", "FORCE_COLOR",
    "NO_COLOR", "CI", "NODE_OPTIONS", "UV_THREADPOOL_SIZE",
}

DANGEROUS_PATHS = {"/", "/home", "/etc", "/usr", "/var", "/root",
                   "~", "$HOME", "%USERPROFILE%", "%HOMEPATH%",
                   "C:\\", "C:/", "D:\\", "D:/"}

CHANNEL_TOKEN_KEYS = {"botToken", "appToken", "token", "webhookSecret",
                      "password", "apiKey", "signingSecret"}

ALL_CHANNEL_NAMES = {"whatsapp", "telegram", "slack", "discord", "signal",
                     "bluebubbles", "imessage", "msteams", "googlechat",
                     "matrix", "zalo", "zalouser", "webchat"}


# ─── JSONC Preprocessing ─────────────────────────────────────────────────────

def strip_jsonc(text: str) -> str:
    """Remove // comments and trailing commas for JSON5/JSONC parsing."""
    lines = []
    for line in text.splitlines():
        stripped = line.lstrip()
        # Skip full-line comments
        if stripped.startswith("//"):
            lines.append("")
            continue
        # Remove inline comments (not inside strings — naive but sufficient)
        # Only strip if // appears outside of a quoted URL context
        in_string = False
        result_chars = []
        i = 0
        while i < len(line):
            c = line[i]
            if c == '"' and (i == 0 or line[i - 1] != '\\'):
                in_string = not in_string
            elif c == '/' and i + 1 < len(line) and line[i + 1] == '/' and not in_string:
                break
            result_chars.append(c)
            i += 1
        lines.append("".join(result_chars))

    text = "\n".join(lines)
    # Remove trailing commas before } or ]
    text = re.sub(r",\s*([}\]])", r"\1", text)
    return text


def load_jsonc(path: Path) -> Optional[dict]:
    """Load a JSONC file, return None on failure."""
    try:
        raw = path.read_text(encoding="utf-8")
        cleaned = strip_jsonc(raw)
        return json.loads(cleaned)
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as e:
        print(f"  \u26a0\ufe0f  Could not parse {path}: {e}")
        return None


# ─── Finding Container ────────────────────────────────────────────────────────

class Finding:
    __slots__ = ("tier", "code", "message", "location", "remediation")

    def __init__(self, tier: str, code: str, message: str,
                 location: str = "", remediation: str = ""):
        self.tier = tier
        self.code = code
        self.message = message
        self.location = location
        self.remediation = remediation

    def __str__(self) -> str:
        icon = {
            "BLOCK": "\ud83d\udeab",
            "WARN": "\u26a0\ufe0f ",
            "INFO": "\u2139\ufe0f ",
        }.get(self.tier, "?")
        parts = [f"  {icon} [{self.tier}] {self.code}: {self.message}"]
        if self.location:
            parts.append(f"      at {self.location}")
        if self.remediation:
            parts.append(f"      \u2192 {self.remediation}")
        return "\n".join(parts)


findings: List[Finding] = []


# ─── OpenClaw Config Checks ──────────────────────────────────────────────────

def check_gateway_bind(config: dict) -> None:
    gateway = config.get("gateway", {})
    if not isinstance(gateway, dict):
        return
    bind = gateway.get("bind", "loopback")
    safe_binds = {"loopback", "127.0.0.1", "localhost", "::1"}
    if isinstance(bind, str) and bind not in safe_binds:
        findings.append(Finding(
            "BLOCK", "CONFIG-BIND",
            f"Gateway bound to '{bind}' — exposed to network",
            "gateway.bind",
            "Set gateway.bind to 'loopback' unless using Tailscale Serve/Funnel",
        ))


def check_dm_policies(config: dict) -> None:
    # Global dmPolicy
    if config.get("dmPolicy") == "open":
        findings.append(Finding(
            "WARN", "CONFIG-DM-OPEN",
            "Global dmPolicy='open' — anyone can message the bot",
            "dmPolicy",
            "Set dmPolicy='pairing' and use explicit allowFrom",
        ))
    allow_from = config.get("allowFrom")
    if isinstance(allow_from, list) and "*" in allow_from:
        findings.append(Finding(
            "WARN", "CONFIG-ALLOW-WILDCARD",
            "Global allowFrom=['*'] — wildcard allows all senders",
            "allowFrom",
            "Replace with explicit list of trusted sender IDs",
        ))

    # Per-channel
    channels = config.get("channels", {})
    if not isinstance(channels, dict):
        return
    for ch_name, ch_cfg in channels.items():
        if not isinstance(ch_cfg, dict):
            continue
        dm_policy = ch_cfg.get("dmPolicy")
        if dm_policy is None:
            dm_cfg = ch_cfg.get("dm", {})
            if isinstance(dm_cfg, dict):
                dm_policy = dm_cfg.get("policy")
        if dm_policy == "open":
            findings.append(Finding(
                "WARN", "CONFIG-DM-OPEN",
                f"Channel '{ch_name}' has dmPolicy='open'",
                f"channels.{ch_name}.dmPolicy",
                "Set dmPolicy='pairing' for this channel",
            ))
        ch_allow = ch_cfg.get("allowFrom")
        if ch_allow is None:
            dm_cfg = ch_cfg.get("dm", {})
            if isinstance(dm_cfg, dict):
                ch_allow = dm_cfg.get("allowFrom")
        if isinstance(ch_allow, list) and "*" in ch_allow:
            findings.append(Finding(
                "WARN", "CONFIG-ALLOW-WILDCARD",
                f"Channel '{ch_name}' has allowFrom=['*']",
                f"channels.{ch_name}.allowFrom",
                "Replace with explicit sender allowlist",
            ))


def check_sandbox(config: dict) -> None:
    agents = config.get("agents", {})
    if not isinstance(agents, dict):
        return
    defaults = agents.get("defaults", {})
    if not isinstance(defaults, dict):
        return
    sandbox = defaults.get("sandbox", {})
    if not sandbox or not isinstance(sandbox, dict):
        findings.append(Finding(
            "INFO", "CONFIG-NO-SANDBOX",
            "No sandbox configuration — main session has full host access by default",
            "agents.defaults.sandbox",
            "Consider sandbox.mode='non-main' to isolate group/channel sessions",
        ))
        return
    mode = sandbox.get("mode", "")
    if mode == "off":
        findings.append(Finding(
            "WARN", "CONFIG-SANDBOX-OFF",
            "Sandbox explicitly disabled — all sessions run with full host access",
            "agents.defaults.sandbox.mode",
            "Set sandbox.mode='non-main' to isolate non-main sessions",
        ))


def check_hardcoded_tokens(config: dict) -> None:
    channels = config.get("channels", {})
    if not isinstance(channels, dict):
        return
    for ch_name, ch_cfg in channels.items():
        if not isinstance(ch_cfg, dict):
            continue
        for key in CHANNEL_TOKEN_KEYS:
            value = ch_cfg.get(key)
            if (isinstance(value, str)
                    and len(value) > 10
                    and not value.startswith("${")
                    and not value.startswith("$")):
                # Mask the value for display
                masked = value[:4] + "..." + value[-4:] if len(value) > 12 else "***"
                findings.append(Finding(
                    "WARN", "CONFIG-HARDCODED-TOKEN",
                    f"Channel '{ch_name}' has hardcoded {key} ({masked})",
                    f"channels.{ch_name}.{key}",
                    f"Use environment variable: {key.upper()} or ${{ENV_VAR}} reference",
                ))


def check_skill_entries(config: dict) -> None:
    skills = config.get("skills", {})
    if not isinstance(skills, dict):
        return
    entries = skills.get("entries", {})
    if not isinstance(entries, dict):
        return
    for skill_name, entry in entries.items():
        if not isinstance(entry, dict):
            continue
        env = entry.get("env", {})
        if not isinstance(env, dict):
            continue
        for key, value in env.items():
            if (SENSITIVE_ENV_PATTERN.search(key)
                    and isinstance(value, str)
                    and len(value) > 8
                    and not value.startswith("${")):
                findings.append(Finding(
                    "WARN", "CONFIG-SKILL-SECRET",
                    f"Skill '{skill_name}' has hardcoded sensitive env: {key}",
                    f"skills.entries.{skill_name}.env.{key}",
                    "Use environment variable references instead of hardcoded values",
                ))


# ─── MCP Config Checks ───────────────────────────────────────────────────────

def check_mcp_servers(mcp_data: dict, source: str) -> None:
    servers = mcp_data.get("mcpServers", {})
    if not isinstance(servers, dict):
        return

    for name, server in servers.items():
        if not isinstance(server, dict):
            continue

        # Sensitive env vars (AGENT-031)
        env = server.get("env", {})
        if isinstance(env, dict):
            for key in env:
                if key not in SAFE_ENV_KEYS and SENSITIVE_ENV_PATTERN.search(key):
                    findings.append(Finding(
                        "WARN", "MCP-SENSITIVE-ENV",
                        f"MCP server '{name}' exposes sensitive env: {key}",
                        f"{source} → mcpServers.{name}.env.{key}",
                        "Only pass necessary env vars; use least-privilege",
                    ))

        # Broad filesystem access (AGENT-029)
        args = server.get("args", [])
        if isinstance(args, list):
            for arg in args:
                if isinstance(arg, str) and arg in DANGEROUS_PATHS:
                    findings.append(Finding(
                        "WARN", "MCP-BROAD-FS",
                        f"MCP server '{name}' has broad filesystem access: {arg}",
                        f"{source} → mcpServers.{name}.args",
                        "Restrict to specific subdirectories",
                    ))

        # SSE/HTTP without auth (AGENT-033)
        transport = server.get("type", server.get("transport", "stdio"))
        if transport in ("sse", "http"):
            headers = server.get("headers", {})
            has_auth = (isinstance(headers, dict)
                        and any("auth" in k.lower() for k in headers))
            if not has_auth:
                findings.append(Finding(
                    "INFO", "MCP-NO-AUTH",
                    f"MCP server '{name}' uses {transport} without auth headers",
                    f"{source} → mcpServers.{name}",
                    "Add Authorization header for authenticated access",
                ))

    # Excessive servers (AGENT-042)
    if len(servers) > 10:
        findings.append(Finding(
            "INFO", "MCP-EXCESSIVE",
            f"{len(servers)} MCP servers configured — large attack surface",
            source,
            "Each server expands what the agent can access",
        ))


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    print()
    print("\ud83d\udee1 Agent Audit \u2014 OpenClaw Configuration Audit")
    print("\u2501" * 50)
    print()

    scanned_any = False

    # 1. Main config
    if OPENCLAW_CONFIG.exists():
        print(f"  Scanning: {OPENCLAW_CONFIG}")
        config = load_jsonc(OPENCLAW_CONFIG)
        if config is not None:
            scanned_any = True
            check_gateway_bind(config)
            check_dm_policies(config)
            check_sandbox(config)
            check_hardcoded_tokens(config)
            check_skill_entries(config)
            # openclaw.json can also contain mcpServers
            if "mcpServers" in config:
                check_mcp_servers(config, str(OPENCLAW_CONFIG))
    else:
        print(f"  Config not found: {OPENCLAW_CONFIG}")

    # 2. MCP configs
    for mcp_path in MCP_SEARCH_PATHS:
        if mcp_path.exists():
            print(f"  Scanning: {mcp_path}")
            mcp_data = load_jsonc(mcp_path)
            if mcp_data is not None:
                scanned_any = True
                check_mcp_servers(mcp_data, str(mcp_path))

    print()

    if not scanned_any:
        print("  No configuration files found to audit.")
        return 0

    if not findings:
        print("  \u2705 No configuration issues found.")
        print()
        return 0

    # Count by tier
    blocks = [f for f in findings if f.tier == "BLOCK"]
    warns = [f for f in findings if f.tier == "WARN"]
    infos = [f for f in findings if f.tier == "INFO"]

    print(f"  Found {len(findings)} issue(s):")
    if blocks:
        print(f"    \ud83d\udeab BLOCK: {len(blocks)}")
    if warns:
        print(f"    \u26a0\ufe0f  WARN:  {len(warns)}")
    if infos:
        print(f"    \u2139\ufe0f  INFO:  {len(infos)}")
    print()

    for f in findings:
        print(str(f))
    print()

    if blocks:
        print("  Verdict: \u274c CRITICAL — fix before exposing OpenClaw to network")
        return 2
    elif warns:
        print("  Verdict: \u26a0\ufe0f  REVIEW NEEDED — address warnings to harden setup")
        return 1
    else:
        print("  Verdict: \u2705 CONFIG OK (informational notes only)")
        return 0


if __name__ == "__main__":
    sys.exit(main())
