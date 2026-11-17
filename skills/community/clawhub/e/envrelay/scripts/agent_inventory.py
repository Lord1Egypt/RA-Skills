#!/usr/bin/env python3
"""One-shot inventory of the AI coding agents installed on this machine.

agent_inventory.py [--agents a,b] [--no-sizes] [--recent-days N] [--diff MANIFEST]

Agent state splits five ways — the agent binary, its configuration, its
extensions, its working state (sessions and memory), and its credentials —
and the five want different decisions. This script finds which of them exist,
how big each one is, what extensions and MCP servers are configured, and
hands the lot over as JSON:

  agents            one record per agent found, paths grouped by plane
  absent_agents     agents this machine does not have — not errors
  errors            something that was present but could not be read
  diff              manifest `agents` vs this machine (with --diff)

Two things it will not do, because doing them would put in your context
exactly what must not be there:

  * It never reads a session transcript. Sessions are counted and sized.
  * It never reports a secret value. MCP `env` blocks and HTTP headers are
    reported as key *names*; URLs as their host; arguments that look like
    they carry a token are redacted.

It installs nothing, launches no agent, and writes no file. What to carry,
what to leave and what to replay is the skill's decision — see
references/ai-agents.md.
"""

import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

HOME = os.path.expanduser("~")
MAC = sys.platform == "darwin"
VERSION_TIMEOUT = 20
# A size walk is stat-only, but an agent directory can hold a million session
# files. Past this many entries the total is reported as a floor, not a fact.
MAX_ENTRIES = 300_000

# Planes, in the order references/ai-agents.md discusses them. The script
# classifies; it does not decide what a plane means for this backup.
PLANES = (
    "config",          # hand-written, small, carry
    "extensions",      # hand-written skills/commands/subagents, carry
    "installed",       # marketplace checkouts — replay from a list instead
    "memory",          # curated agent memory, carry even when sessions do not
    "sessions",        # transcripts and per-project state — the gigabytes
    "working-state",   # generated output, large, judgement
    "credential",      # tokens on disk
    "cache",           # leave
)


def p(path):
    """`~/.claude` -> `/Users/x/.claude`."""
    return os.path.expanduser(path)


def tilde(path):
    """The inverse, so every path we print is machine-independent."""
    if path == HOME:
        return "~"
    if path.startswith(HOME + os.sep):
        return "~" + path[len(HOME):]
    return path


def entry(path, plane, note=None, **extra):
    item = {"path": path, "plane": plane}
    if note:
        item["note"] = note
    item.update(extra)
    return item


# --- the layouts ------------------------------------------------------------
#
# Paths may contain shell globs. `list` enumerates names inside a directory
# ("dirs" or "files"); `mcp` names the shape of an MCP block to parse.

AGENTS = [
    {
        "id": "claude-code",
        "name": "Claude Code",
        "binaries": ["claude"],
        "roots": ["~/.claude"],
        "entries": [
            entry("~/.claude/settings.json", "config"),
            entry("~/.claude/settings.local.json", "config"),
            entry("~/.claude/CLAUDE.md", "config", "global instructions"),
            entry("~/.claude.json", "config", "holds mcpServers and per-project history",
                  mcp="json:mcpServers"),
            entry("~/.claude/statusline-command.sh", "config", "executable"),
            entry("~/.claude/skills", "extensions", list="dirs"),
            entry("~/.claude/agents", "extensions", list="files"),
            entry("~/.claude/commands", "extensions", list="files"),
            entry("~/.claude/hooks", "extensions", "executable — runs on session events",
                  list="files"),
            entry("~/.claude/memory", "memory"),
            entry("~/.claude/plugins/installed_plugins.json", "extensions",
                  "the replayable plugin list"),
            entry("~/.claude/plugins/known_marketplaces.json", "extensions"),
            entry("~/.claude/plugins/cache", "installed", "git clones; claude plugin install"),
            entry("~/.claude/plugins/marketplaces", "installed"),
            entry("~/.claude/projects/*/memory", "memory", "file-based memory, per project"),
            entry("~/.claude/projects", "sessions", "path-keyed — see references/ai-agents.md"),
            entry("~/.claude/history.jsonl", "sessions"),
            entry("~/.claude/sessions", "sessions"),
            entry("~/.claude/tasks", "sessions"),
            entry("~/.claude/file-history", "sessions"),
            entry("~/.claude/shell-snapshots", "cache"),
            entry("~/.claude/backups", "cache"),
            entry("~/.claude/cache", "cache"),
            entry("~/.claude/downloads", "cache"),
            entry("~/.claude/debug", "cache"),
            entry("~/.claude/telemetry", "cache"),
            entry("~/.claude/paste-cache", "cache"),
            entry("~/.claude/.credentials.json", "credential", "Linux only; macOS uses the Keychain"),
        ],
        "machine_bound": ["macOS login Keychain: the OAuth token is not in a file"] if MAC else [],
    },
    {
        "id": "codex",
        "name": "Codex CLI",
        "binaries": ["codex"],
        "roots": ["~/.codex"],
        "entries": [
            entry("~/.codex/config.toml", "config", "holds [mcp_servers] with env",
                  mcp="toml:mcp_servers"),
            entry("~/.codex/AGENTS.md", "config", "global instructions"),
            entry("~/.codex/hooks.json", "config", "executable — runs on session events"),
            entry("~/.codex/hooks", "config", list="files"),
            entry("~/.codex/skills", "extensions", list="dirs"),
            entry("~/.codex/prompts", "extensions", list="files"),
            entry("~/.codex/rules", "extensions", list="files"),
            entry("~/.codex/plugins", "installed", "installed plugins; the list is in config.toml"),
            entry("~/.codex/local-marketplaces", "installed"),
            entry("~/.codex/memories", "memory"),
            entry("~/.codex/memories_*.sqlite*", "memory", "live database — carry with its -wal"),
            entry("~/.codex/sessions", "sessions"),
            entry("~/.codex/archived_sessions", "sessions"),
            entry("~/.codex/thread_history_*.sqlite*", "sessions",
                  "live database — carry with its -wal"),
            entry("~/.codex/history.jsonl", "sessions"),
            entry("~/.codex/generated_images", "working-state", "output, often large"),
            entry("~/.codex/creative-production", "working-state"),
            entry("~/.codex/computer-use", "working-state"),
            entry("~/.codex/auth.json", "credential"),
            entry("~/.codex/cache", "cache"),
            entry("~/.codex/log", "cache"),
            entry("~/.codex/logs_*.sqlite*", "cache"),
            entry("~/.codex/tmp", "cache"),
            entry("~/.codex/ipc", "cache"),
        ],
    },
    {
        "id": "gemini-cli",
        "name": "Gemini CLI",
        "binaries": ["gemini"],
        "roots": ["~/.gemini"],
        "entries": [
            entry("~/.gemini/settings.json", "config", mcp="json:mcpServers"),
            entry("~/.gemini/GEMINI.md", "config", "global instructions"),
            entry("~/.gemini/config/mcp_config.json", "config", mcp="json:mcpServers"),
            entry("~/.gemini/config/skills", "extensions", list="dirs"),
            entry("~/.gemini/extensions", "extensions", list="dirs"),
            entry("~/.gemini/commands", "extensions", list="files"),
            entry("~/.gemini/config/projects", "sessions"),
            entry("~/.gemini/oauth_creds.json", "credential"),
            entry("~/.gemini/google_accounts.json", "credential"),
            entry("~/.gemini/tmp", "cache"),
            entry("~/.gemini/antigravity*", "cache", "a downloaded IDE, not configuration"),
        ],
    },
    {
        "id": "cursor",
        "name": "Cursor",
        "binaries": ["cursor", "cursor-agent"],
        "roots": ["~/.cursor"],
        "entries": [
            entry("~/.cursor/mcp.json", "config", mcp="json:mcpServers"),
            entry("~/.cursor/argv.json", "config"),
            entry("~/.cursor/rules", "extensions", list="files"),
            entry("~/.cursor/skills-cursor", "extensions", list="dirs"),
            entry("~/.cursor/extensions", "installed",
                  "replay as a list: cursor --list-extensions"),
            entry("~/Library/Application Support/Cursor/User/settings.json", "config"),
            entry("~/Library/Application Support/Cursor/User/keybindings.json", "config"),
            entry("~/Library/Application Support/Cursor/User/snippets", "config"),
            entry("~/.cursor/projects", "sessions"),
            entry("~/.cursor/ai-tracking", "sessions"),
            entry("~/Library/Application Support/Cursor/User/globalStorage", "sessions",
                  "chat history and per-workspace state"),
            entry("~/Library/Application Support/Cursor/User/workspaceStorage", "sessions",
                  "path-keyed"),
            entry("~/Library/Application Support/Cursor/Cache", "cache"),
            entry("~/Library/Application Support/Cursor/CachedData", "cache"),
        ],
    },
    {
        "id": "copilot-cli",
        "name": "GitHub Copilot CLI",
        "binaries": ["copilot"],
        "roots": ["~/.copilot"],
        "entries": [
            entry("~/.copilot/config.json", "config", mcp="json:mcpServers"),
            entry("~/.copilot/mcp-config.json", "config", mcp="json:mcpServers"),
            entry("~/.copilot/history", "sessions"),
            entry("~/.copilot/history-session-state", "sessions"),
            entry("~/.copilot/logs", "cache"),
        ],
    },
    {
        "id": "opencode",
        "name": "opencode",
        "binaries": ["opencode"],
        "roots": ["~/.config/opencode", "~/.local/share/opencode"],
        "entries": [
            entry("~/.config/opencode/opencode.json", "config", mcp="json:mcp"),
            entry("~/.config/opencode/opencode.jsonc", "config", mcp="json:mcp"),
            entry("~/.config/opencode/AGENTS.md", "config"),
            entry("~/.config/opencode/agent", "extensions", list="files"),
            entry("~/.config/opencode/command", "extensions", list="files"),
            entry("~/.config/opencode/plugin", "extensions", list="files"),
            entry("~/.config/opencode/node_modules", "cache", "reinstalled from package.json"),
            entry("~/.local/share/opencode/storage", "sessions"),
            entry("~/.local/share/opencode/snapshot", "sessions"),
            entry("~/.local/share/opencode/tool-output", "sessions"),
            entry("~/.local/share/opencode/auth.json", "credential"),
            entry("~/.local/share/opencode/log", "cache"),
            entry("~/.local/share/opencode/bin", "cache"),
        ],
    },
    {
        "id": "windsurf",
        "name": "Windsurf",
        "binaries": ["windsurf"],
        "roots": ["~/.codeium"],
        "entries": [
            entry("~/.codeium/windsurf/mcp_config.json", "config", mcp="json:mcpServers"),
            entry("~/.codeium/windsurf/memories", "memory"),
            entry("~/Library/Application Support/Windsurf/User/settings.json", "config"),
            entry("~/Library/Application Support/Windsurf/User/globalStorage", "sessions"),
            entry("~/Library/Application Support/Windsurf/User/workspaceStorage", "sessions"),
            entry("~/.codeium/windsurf/cascade", "sessions"),
        ],
    },
    {
        "id": "continue",
        "name": "Continue",
        "binaries": ["cn"],
        "roots": ["~/.continue"],
        "entries": [
            entry("~/.continue/config.yaml", "config", "may hold API keys inline"),
            entry("~/.continue/config.json", "config", mcp="json:mcpServers"),
            entry("~/.continue/assistants", "extensions", list="files"),
            entry("~/.continue/rules", "extensions", list="files"),
            entry("~/.continue/mcpServers", "extensions", list="files"),
            entry("~/.continue/sessions", "sessions"),
            entry("~/.continue/index", "cache", "rebuilt by indexing"),
        ],
    },
    {
        "id": "aider",
        "name": "Aider",
        "binaries": ["aider"],
        "roots": ["~/.aider"],
        "entries": [
            entry("~/.aider.conf.yml", "config", "may hold API keys inline"),
            entry("~/.aider.model.settings.yml", "config"),
            entry("~/.aider/caches", "cache"),
        ],
    },
    {
        "id": "goose",
        "name": "Goose",
        "binaries": ["goose"],
        "roots": ["~/.config/goose", "~/.local/share/goose"],
        "entries": [
            entry("~/.config/goose/config.yaml", "config", mcp="yaml:extensions"),
            entry("~/.config/goose/recipes", "extensions", list="files"),
            entry("~/.local/share/goose/sessions", "sessions"),
            entry("~/.local/share/goose/logs", "cache"),
        ],
    },
    {
        "id": "zed",
        "name": "Zed",
        "binaries": ["zed"],
        "roots": ["~/.config/zed"],
        "entries": [
            entry("~/.config/zed/settings.json", "config", mcp="json:context_servers"),
            entry("~/.config/zed/keymap.json", "config"),
            entry("~/.config/zed/prompts", "extensions", list="files"),
            entry("~/.config/zed/extensions", "installed"),
            entry("~/Library/Application Support/Zed/conversations", "sessions"),
            entry("~/Library/Application Support/Zed/db", "sessions"),
            entry("~/.local/share/zed/conversations", "sessions"),
        ],
    },
    {
        "id": "qwen-code",
        "name": "Qwen Code",
        "binaries": ["qwen"],
        "roots": ["~/.qwen"],
        "entries": [
            entry("~/.qwen/settings.json", "config", mcp="json:mcpServers"),
            entry("~/.qwen/QWEN.md", "config"),
            entry("~/.qwen/commands", "extensions", list="files"),
            entry("~/.qwen/oauth_creds.json", "credential"),
            entry("~/.qwen/tmp", "cache"),
        ],
    },
    {
        "id": "ollama",
        "name": "Ollama",
        "binaries": ["ollama"],
        "roots": ["~/.ollama"],
        "entries": [
            entry("~/.ollama/models", "cache", "weights — re-pull, record `ollama list`"),
            entry("~/.ollama/id_ed25519", "credential", "the machine's own key"),
        ],
    },
    {
        "id": "vscode-copilot",
        "name": "VS Code (Copilot and chat extensions)",
        "binaries": ["code"],
        "roots": [],
        "entries": [
            entry("~/Library/Application Support/Code/User/settings.json", "config"),
            entry("~/Library/Application Support/Code/User/keybindings.json", "config"),
            entry("~/Library/Application Support/Code/User/mcp.json", "config",
                  mcp="json:servers"),
            entry("~/Library/Application Support/Code/User/prompts", "extensions", list="files"),
            entry("~/.config/Code/User/settings.json", "config"),
            entry("~/.config/Code/User/mcp.json", "config", mcp="json:servers"),
            entry("~/Library/Application Support/Code/User/globalStorage", "sessions",
                  "Cline, Roo and chat history live in here, per extension id"),
            entry("~/Library/Application Support/Code/User/workspaceStorage", "sessions",
                  "path-keyed"),
        ],
    },
]


# --- redaction --------------------------------------------------------------

# `pat` is bounded: PATH is a path, GITHUB_PAT is a token.
SECRETISH = re.compile(
    r"key|token|secret|password|passwd|credential|auth|cookie|session"
    r"|(?:^|[_\-.])pat(?:$|[_\-.])",
    re.I,
)
TOKEN_SHAPED = re.compile(
    r"^(sk-|pk-|ghp_|gho_|ghu_|ghs_|github_pat_|xox[baprs]-|AKIA|ASIA|glpat-|"
    r"AIza|dop_v1_|hf_|ya29\.)|^[A-Za-z0-9+/_-]{40,}={0,2}$"
)


def redact_arg(arg):
    """Arguments are values too: `--api-key=sk-live-…` is a secret on a
    command line. Keep the shape, drop anything that looks like the key."""
    if not isinstance(arg, str):
        return str(arg)
    name, sep, value = arg.partition("=")
    if sep and SECRETISH.search(name):
        return f"{name}=<redacted>"
    if TOKEN_SHAPED.search(arg):
        return "<redacted>"
    return arg


def safe_url(url):
    """Host and scheme survive; userinfo, path and query do not — a token can
    be in any of the three."""
    if not isinstance(url, str):
        return None, False, False
    match = re.match(r"^(?P<scheme>[a-z][a-z0-9+.-]*)://(?P<rest>.*)$", url, re.I)
    if not match:
        return None, False, False
    rest = match.group("rest")
    authority = rest.split("/", 1)[0].split("?", 1)[0]
    host = authority.rsplit("@", 1)[-1]
    tail = rest[len(authority):]
    return f"{match.group('scheme')}://{host}", "?" in tail, tail.strip("/") != ""


def mcp_record(name, spec, source):
    """One MCP server, with every value that could be a secret removed."""
    item = {"name": name, "source": tilde(source)}
    if not isinstance(spec, dict):
        item["note"] = "unrecognised shape"
        return item

    command = spec.get("command")
    if isinstance(command, str):
        item["command"] = command
    args = spec.get("args")
    if isinstance(args, list):
        item["args"] = [redact_arg(a) for a in args]

    url = spec.get("url") or spec.get("httpUrl") or spec.get("serverUrl")
    if url:
        host, has_query, has_path = safe_url(url)
        item["url_host"] = host or "<unparseable>"
        item["url_has_query"] = has_query
        item["url_has_path"] = has_path

    transport = spec.get("type") or spec.get("transport")
    item["transport"] = transport if isinstance(transport, str) else (
        "http" if url else "stdio" if command else None
    )

    # Key names only. An inline env block is where an API key hides in a file
    # that otherwise looks like ordinary config, and the name is enough to
    # know a value has to be re-provisioned on the new machine.
    for field, label in (("env", "env_keys"), ("environment", "env_keys"),
                         ("headers", "header_keys"), ("env_http_headers", "header_keys")):
        block = spec.get(field)
        if isinstance(block, dict) and block:
            item[label] = sorted(set(item.get(label, [])) | {str(k) for k in block})
    secretish = sorted(
        key for key in item.get("env_keys", []) + item.get("header_keys", [])
        if SECRETISH.search(key)
    )
    if secretish:
        item["likely_secret_keys"] = secretish
    if spec.get("enabled") is False or spec.get("disabled") is True:
        item["enabled"] = False
    return item


# --- config parsing ---------------------------------------------------------

def read_json(path):
    with open(path, encoding="utf-8", errors="replace") as handle:
        text = handle.read()
    if not text.strip():
        return {}
    try:
        return json.loads(text)
    except ValueError:
        # .jsonc and hand-edited config files: strip whole-line comments and
        # retry once. A second failure is a real parse error.
        stripped = "\n".join(
            line for line in text.splitlines() if not line.lstrip().startswith("//")
        )
        return json.loads(stripped)


def split_toml_key(header):
    """`mcp_servers.'my server'.env` -> ['mcp_servers', 'my server', 'env']."""
    parts, buf, quote = [], "", None
    for char in header:
        if quote:
            if char == quote:
                quote = None
            else:
                buf += char
        elif char in "\"'":
            quote = char
        elif char == ".":
            parts.append(buf.strip())
            buf = ""
        else:
            buf += char
    parts.append(buf.strip())
    return [part for part in parts if part != ""]


def toml_value(raw):
    raw = raw.strip()
    if raw[:1] in "\"'" and raw[-1:] == raw[:1] and len(raw) >= 2:
        return raw[1:-1]
    if raw.startswith("["):
        inner = raw[1:raw.rfind("]")] if "]" in raw else raw[1:]
        out, buf, quote = [], "", None
        for char in inner:
            if quote:
                if char == quote:
                    quote = None
                else:
                    buf += char
            elif char in "\"'":
                quote = char
            elif char == ",":
                if buf.strip():
                    out.append(buf.strip())
                buf = ""
            else:
                buf += char
        if buf.strip():
            out.append(buf.strip())
        return out
    if raw in ("true", "false"):
        return raw == "true"
    return raw


def toml_tables(path, wanted):
    """Every `[wanted.NAME…]` table in a TOML file, as nested dicts.

    tomllib when the interpreter has it (3.11+), otherwise a scanner that
    understands the subset these config files use: string, boolean and
    single-line array values under `[a.b.c]` headers. The subset is enough
    for MCP servers and plugin lists, and the caller is told which parser ran.
    """
    try:
        import tomllib  # noqa: PLC0415 — optional, 3.11+
        with open(path, "rb") as handle:
            return tomllib.load(handle).get(wanted, {}) or {}, "tomllib"
    except ImportError:
        pass
    except (OSError, ValueError) as error:
        raise RuntimeError(f"cannot parse {tilde(path)}: {error}")

    tables = {}
    current = None
    with open(path, encoding="utf-8", errors="replace") as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("["):
                end = line.find("]")
                header = line[1:end] if end > 0 else line[1:]
                parts = split_toml_key(header.strip("["))
                current = None
                if len(parts) >= 2 and parts[0] == wanted:
                    table = tables.setdefault(parts[1], {})
                    for key in parts[2:]:
                        table = table.setdefault(key, {})
                    current = table
                continue
            if current is None or "=" not in line:
                continue
            key, _, value = line.partition("=")
            current[key.strip().strip("\"'")] = toml_value(value)
    return tables, "minimal"


def yaml_top_keys(path, wanted):
    """Goose-style `extensions:` blocks: the names of the two-space-indented
    keys under one top-level key. Not a YAML parser — it reports names, and
    names are all this script ever reports from a config it cannot parse."""
    names, inside = [], False
    with open(path, encoding="utf-8", errors="replace") as handle:
        for raw in handle:
            if not raw.strip() or raw.lstrip().startswith("#"):
                continue
            if not raw[:1].isspace():
                inside = raw.split(":", 1)[0].strip() == wanted
                continue
            if inside and re.match(r"^ {2}\S[^:]*:", raw):
                names.append(raw.strip().split(":", 1)[0].strip("\"'"))
    return names


def mcp_from(path, spec, errors):
    kind, _, key = spec.partition(":")
    try:
        if kind == "json":
            data = read_json(path)
            block = data.get(key) if isinstance(data, dict) else None
            if not isinstance(block, dict):
                return []
            return [mcp_record(name, value, path) for name, value in sorted(block.items())]
        if kind == "toml":
            tables, parser = toml_tables(path, key)
            out = [mcp_record(name, value, path) for name, value in sorted(tables.items())]
            if parser == "minimal":
                for item in out:
                    item["parsed_by"] = "minimal-toml"
            return out
        if kind == "yaml":
            return [
                {"name": name, "source": tilde(path), "parsed_by": "names-only"}
                for name in yaml_top_keys(path, key)
            ]
    except (OSError, ValueError, RuntimeError) as error:
        errors.append({"path": tilde(path), "reason": f"cannot read MCP block: {error}"})
    return []


# --- extension lists --------------------------------------------------------

def claude_plugins(errors):
    """The replayable list: what is installed, from which marketplace."""
    out = {}
    installed = p("~/.claude/plugins/installed_plugins.json")
    if os.path.exists(installed):
        try:
            data = read_json(installed)
            plugins = []
            for full_name, records in sorted((data.get("plugins") or {}).items()):
                name, _, marketplace = full_name.partition("@")
                record = (records or [{}])[0] if isinstance(records, list) else {}
                item = {"name": name, "marketplace": marketplace or None}
                if isinstance(record, dict) and record.get("version"):
                    item["version"] = record["version"]
                plugins.append(item)
            out["plugins"] = plugins
        except (OSError, ValueError) as error:
            errors.append({"path": tilde(installed), "reason": str(error)})

    known = p("~/.claude/plugins/known_marketplaces.json")
    if os.path.exists(known):
        try:
            data = read_json(known)
            markets = data if isinstance(data, dict) else {}
            listed = []
            for name, value in sorted(markets.items()):
                source = value.get("source") if isinstance(value, dict) else None
                if isinstance(source, dict):
                    source = source.get("source") or source.get("url") or source.get("repo")
                item = {"name": name}
                if isinstance(source, str):
                    host, _, _ = safe_url(source)
                    item["source"] = host or source
                listed.append(item)
            out["marketplaces"] = listed
        except (OSError, ValueError) as error:
            errors.append({"path": tilde(known), "reason": str(error)})
    return out


def codex_plugins(errors):
    config = p("~/.codex/config.toml")
    if not os.path.exists(config):
        return {}
    out = {}
    try:
        for key, label in (("plugins", "plugins"), ("marketplaces", "marketplaces")):
            tables, _parser = toml_tables(config, key)
            items = []
            for name, value in sorted(tables.items()):
                plugin, _, marketplace = name.partition("@")
                item = {"name": plugin}
                if marketplace:
                    item["marketplace"] = marketplace
                if isinstance(value, dict) and isinstance(value.get("version"), str):
                    item["version"] = value["version"]
                if isinstance(value, dict) and isinstance(value.get("url"), str):
                    host, _, _ = safe_url(value["url"])
                    item["source"] = host or value["url"]
                items.append(item)
            if items:
                out[label] = items
    except (OSError, ValueError, RuntimeError) as error:
        errors.append({"path": tilde(config), "reason": str(error)})
    return out


EXTENSION_EXTRAS = {"claude-code": claude_plugins, "codex": codex_plugins}


# --- the filesystem side ----------------------------------------------------

def walk_size(path, recent_cutoff=None):
    """Recursive size by stat, never following a symlink out of the tree."""
    total = files = recent_files = recent_bytes = 0
    newest = None
    truncated = False
    stack = [path]
    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as scan:
                for item in scan:
                    if files >= MAX_ENTRIES:
                        truncated = True
                        stack = []
                        break
                    try:
                        if item.is_symlink():
                            files += 1
                            continue
                        if item.is_dir(follow_symlinks=False):
                            stack.append(item.path)
                            continue
                        stat = item.stat(follow_symlinks=False)
                    except OSError:
                        continue
                    files += 1
                    total += stat.st_size
                    if newest is None or stat.st_mtime > newest:
                        newest = stat.st_mtime
                    if recent_cutoff is not None and stat.st_mtime >= recent_cutoff:
                        recent_files += 1
                        recent_bytes += stat.st_size
        except OSError:
            continue
    return {
        "bytes": total,
        "files": files,
        "newest": stamp(newest),
        "recent_files": recent_files,
        "recent_bytes": recent_bytes,
        "size_truncated": truncated,
    }


def stamp(mtime):
    if mtime is None:
        return None
    return datetime.fromtimestamp(mtime, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def names_in(path, which):
    try:
        with os.scandir(path) as scan:
            out = []
            for item in scan:
                if item.name.startswith("."):
                    continue
                is_dir = item.is_dir(follow_symlinks=False) or (
                    item.is_symlink() and os.path.isdir(item.path)
                )
                if (which == "dirs") == bool(is_dir):
                    out.append(item.name)
            return sorted(out)
    except OSError:
        return []


def describe(path, spec, sizes, recent_cutoff, errors):
    """One declared path that exists, as a record."""
    record = {
        "path": tilde(path),
        "plane": spec["plane"],
        "kind": "dir" if os.path.isdir(path) else "file",
    }
    if spec.get("note"):
        record["note"] = spec["note"]
    try:
        if record["kind"] == "dir":
            if sizes:
                record.update(walk_size(path, recent_cutoff))
        else:
            stat = os.lstat(path)
            record["bytes"] = stat.st_size
            record["files"] = 1
            record["newest"] = stamp(stat.st_mtime)
            if recent_cutoff is not None and stat.st_mtime >= recent_cutoff:
                record["recent_files"], record["recent_bytes"] = 1, stat.st_size
    except OSError as error:
        errors.append({"path": tilde(path), "reason": str(error)})
    if spec.get("list"):
        record["names"] = names_in(path, spec["list"])
    return record


def declared_paths(spec_entries):
    """Every literal path and glob an agent declares, expanded."""
    for spec in spec_entries:
        pattern = p(spec["path"])
        if any(char in pattern for char in "*?["):
            for match in sorted(glob.glob(pattern)):
                yield match, spec
        elif os.path.lexists(pattern):
            yield pattern, spec


def unclassified_in(roots, claimed, sizes, errors, depth=3):
    """Children of an agent root that no rule mentions.

    Agent layouts change with every release, so this is not an edge case: a
    directory nobody classified is a decision for the skill, and reporting it
    is the difference between a considered omission and a silent one. A
    directory that only *contains* classified paths is descended into rather
    than reported, so `plugins/` does not hide a new `plugins/whatever/`.
    """
    out = []
    claimed_set = set(claimed)

    def record_for(child):
        record = {"path": tilde(child), "kind": "dir" if os.path.isdir(child) else "file"}
        try:
            if record["kind"] == "dir":
                if sizes:
                    size = walk_size(child)
                    record["bytes"], record["files"] = size["bytes"], size["files"]
            else:
                record["bytes"] = os.lstat(child).st_size
        except OSError as error:
            errors.append({"path": tilde(child), "reason": str(error)})
        return record

    def sweep(base, level):
        try:
            names = sorted(os.listdir(base))
        except OSError as error:
            errors.append({"path": tilde(base), "reason": str(error)})
            return
        for name in names:
            child = os.path.join(base, name)
            if child in claimed_set or any(
                child.startswith(item + os.sep) for item in claimed_set
            ):
                continue
            holds_claims = any(item.startswith(child + os.sep) for item in claimed_set)
            if holds_claims and os.path.isdir(child) and not os.path.islink(child):
                if level < depth:
                    sweep(child, level + 1)
                else:
                    out.append({**record_for(child), "note": "contains classified paths"})
                continue
            out.append(record_for(child))

    for root in roots:
        base = p(root)
        if os.path.isdir(base):
            sweep(base, 1)
    return out


def cli_of(binaries):
    for binary in binaries:
        found = shutil.which(binary)
        if not found:
            continue
        info = {"binary": binary, "path": tilde(found)}
        try:
            done = subprocess.run(
                [found, "--version"],
                capture_output=True, text=True, timeout=VERSION_TIMEOUT,
                stdin=subprocess.DEVNULL, env={**os.environ, "LC_ALL": "C"},
            )
            for line in done.stdout.splitlines():
                line = re.sub(r"\x1b\[[0-9;]*m", "", line).strip()
                if line:
                    info["version"] = line
                    break
        except (OSError, subprocess.SubprocessError):
            pass
        return info
    return None


def inspect(agent, sizes, recent_cutoff, errors):
    paths, claimed, mcp_servers = [], [], []
    for path, spec in declared_paths(agent["entries"]):
        claimed.append(path)
        paths.append(describe(path, spec, sizes, recent_cutoff, errors))
        if spec.get("mcp"):
            mcp_servers.extend(mcp_from(path, spec["mcp"], errors))

    record = {
        "id": agent["id"],
        "name": agent["name"],
        "cli": cli_of(agent["binaries"]),
        "paths": paths,
        "unclassified": unclassified_in(agent.get("roots", []), claimed, sizes, errors),
    }
    if mcp_servers:
        record["mcp_servers"] = mcp_servers
    if agent.get("machine_bound"):
        record["machine_bound"] = agent["machine_bound"]

    extensions = {}
    for item in paths:
        if item["plane"] == "extensions" and item.get("names"):
            extensions[os.path.basename(item["path"])] = item["names"]
    extra = EXTENSION_EXTRAS.get(agent["id"])
    if extra:
        extensions.update(extra(errors))
    if extensions:
        record["extensions"] = extensions

    if sizes:
        # A declared path can sit inside another — claude-code keeps memory/
        # inside the sessions directory — and the enclosing walk already
        # counted those bytes. The inner path keeps its own plane and the same
        # bytes come off every plane that encloses it, so the planes add up to
        # the total instead of counting the overlap twice.
        by_plane = {}
        for item in paths:
            by_plane[item["plane"]] = by_plane.get(item["plane"], 0) + item.get("bytes", 0)
        for item in paths:
            enclosing = [
                other for other in paths
                if other is not item and item["path"].startswith(other["path"] + "/")
            ]
            if not enclosing:
                continue
            item["counted_under"] = max(enclosing, key=lambda o: len(o["path"]))["path"]
            for other in enclosing:
                by_plane[other["plane"]] -= item.get("bytes", 0)
        # A truncated walk can leave a plane short of what its children claim.
        by_plane = {plane: max(0, total) for plane, total in by_plane.items()}
        record["bytes_by_plane"] = by_plane
        record["bytes_total"] = sum(by_plane.values()) + sum(
            item.get("bytes", 0) for item in record["unclassified"]
        )
    return record


# --- the diff ---------------------------------------------------------------

def flatten(extensions):
    """{'skills': ['a'], 'plugins': [{'name': 'b'}]} -> {'skills': {'a'}, …}"""
    out = {}
    for label, items in (extensions or {}).items():
        names = set()
        for item in items or []:
            if isinstance(item, str):
                names.add(item)
            elif isinstance(item, dict) and item.get("name"):
                names.add(item["name"])
        out[label] = names
    return out


def diff_against(manifest, found):
    here = {record["id"]: record for record in found}
    out = []
    for wanted in manifest.get("agents", []):
        agent_id = wanted.get("id") or wanted.get("name", "?")
        mine = here.get(agent_id)
        row = {"id": agent_id, "installed": bool(mine and mine.get("cli"))}
        if mine is None:
            row["state"] = "absent"
            out.append(row)
            continue
        row["state"] = "present"
        if mine.get("cli", {}).get("version"):
            row["current_version"] = mine["cli"]["version"]
        if wanted.get("version"):
            row["manifest_version"] = wanted["version"]

        mine_ext = flatten(mine.get("extensions"))
        missing = {}
        for label, names in flatten(wanted.get("extensions")).items():
            gap = sorted(names - mine_ext.get(label, set()))
            if gap:
                missing[label] = gap
        if missing:
            row["extensions_missing"] = missing

        mine_mcp = {server["name"] for server in mine.get("mcp_servers", [])}
        gap = sorted(
            server.get("name")
            for server in wanted.get("mcp_servers", [])
            if server.get("name") and server["name"] not in mine_mcp
        )
        if gap:
            row["mcp_servers_missing"] = gap
        out.append(row)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--agents", metavar="A,B", help="only these agent ids")
    parser.add_argument(
        "--no-sizes", action="store_true",
        help="skip the size walk (faster; a 50 GB session directory then looks like any other)",
    )
    parser.add_argument(
        "--recent-days", type=int, metavar="N",
        help="also count files modified in the last N days — sizes the `recent` session tier",
    )
    parser.add_argument("--diff", metavar="MANIFEST", help="compare a manifest's agents array")
    args = parser.parse_args()

    known = {agent["id"] for agent in AGENTS}
    wanted = set(args.agents.split(",")) if args.agents else known
    unknown = wanted - known
    if unknown:
        parser.error(f"unknown agent ids: {', '.join(sorted(unknown))}")

    recent_cutoff = None
    if args.recent_days is not None:
        if args.recent_days < 0:
            parser.error("--recent-days cannot be negative")
        recent_cutoff = datetime.now(timezone.utc).timestamp() - args.recent_days * 86400

    manifest = None
    if args.diff:
        try:
            with open(args.diff, encoding="utf-8") as handle:
                manifest = json.load(handle)
        except (OSError, ValueError) as error:
            print(f"agent_inventory: cannot read manifest {args.diff}: {error}", file=sys.stderr)
            sys.exit(1)

    errors, found, absent = [], [], []
    for agent in AGENTS:
        if agent["id"] not in wanted:
            continue
        record = inspect(agent, not args.no_sizes, recent_cutoff, errors)
        # An agent is "here" if it left state behind or its CLI is installed:
        # a binary with no config is a fresh install, config with no binary is
        # what a half-finished restore looks like. Both are worth reporting.
        if record["paths"] or record["cli"] or record["unclassified"]:
            found.append(record)
        else:
            absent.append(agent["id"])

    result = {
        "platform": "macos" if MAC else "linux",
        "home": tilde(HOME),
        "agents": found,
        "absent_agents": absent,
        "errors": errors,
    }
    if manifest is not None:
        result["diff"] = diff_against(manifest, found)

    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    print()


if __name__ == "__main__":
    main()
