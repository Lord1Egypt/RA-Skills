#!/usr/bin/env python3
"""Configure Codex App agentmemory hooks on Windows."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


EVENTS = {
    "PreToolUse": ("pre_tool_use", "pre-tool-use.mjs"),
    "PostToolUse": ("post_tool_use", "post-tool-use.mjs"),
    "SessionStart": ("session_start", "session-start.mjs"),
    "UserPromptSubmit": ("user_prompt_submit", "prompt-submit.mjs"),
    "Stop": ("stop", "stop.mjs"),
    "PreCompact": ("pre_compact", "pre-compact.mjs"),
}

HOOK_SCRIPT_REPLACEMENTS = {
    "session-start.mjs": r"""#!/usr/bin/env node
function isSdkChildContext(payload) {
  if (process.env["AGENTMEMORY_SDK_CHILD"] === "1") return true;
  if (!payload || typeof payload !== "object") return false;
  return payload.entrypoint === "sdk-ts";
}

const INJECT_CONTEXT = process.env["AGENTMEMORY_INJECT_CONTEXT"] === "true";
const REST_URL = process.env["AGENTMEMORY_URL"] || "http://localhost:3111";
const SECRET = process.env["AGENTMEMORY_SECRET"] || "";
const INJECT_TIMEOUT_MS = 1500;
const REGISTER_TIMEOUT_MS = 800;

function authHeaders() {
  const h = { "Content-Type": "application/json" };
  if (SECRET) h["Authorization"] = `Bearer ${SECRET}`;
  return h;
}

function writeCodexContext(context) {
  if (!context) return;
  process.stdout.write(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: "SessionStart",
      additionalContext: context,
    },
    suppressOutput: true,
  }));
}

async function main() {
  let input = "";
  for await (const chunk of process.stdin) input += chunk;
  let data;
  try {
    data = JSON.parse(input);
  } catch {
    return;
  }
  if (isSdkChildContext(data)) return;

  const sessionId = data.session_id || `ses_${Date.now().toString(36)}`;
  const project = data.cwd || process.cwd();
  const url = `${REST_URL}/agentmemory/session/start`;
  const init = {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ sessionId, project, cwd: project }),
  };

  if (!INJECT_CONTEXT) {
    fetch(url, { ...init, signal: AbortSignal.timeout(REGISTER_TIMEOUT_MS) }).catch(() => {});
    return;
  }

  try {
    const res = await fetch(url, { ...init, signal: AbortSignal.timeout(INJECT_TIMEOUT_MS) });
    if (res.ok) {
      const result = await res.json();
      if (result.context) writeCodexContext(result.context);
    }
  } catch {}
}

main();
""",
    "prompt-submit.mjs": r"""#!/usr/bin/env node
function isSdkChildContext(payload) {
  if (process.env["AGENTMEMORY_SDK_CHILD"] === "1") return true;
  if (!payload || typeof payload !== "object") return false;
  return payload.entrypoint === "sdk-ts";
}

const REST_URL = process.env["AGENTMEMORY_URL"] || "http://localhost:3111";
const SECRET = process.env["AGENTMEMORY_SECRET"] || "";
const INJECT_CONTEXT = process.env["AGENTMEMORY_INJECT_CONTEXT"] === "true";
const INJECT_TIMEOUT_MS = 1600;
const OBSERVE_TIMEOUT_MS = 1600;

function authHeaders() {
  const h = { "Content-Type": "application/json" };
  if (SECRET) h["Authorization"] = `Bearer ${SECRET}`;
  return h;
}

function writeCodexContext(context) {
  if (!context) return;
  process.stdout.write(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: "UserPromptSubmit",
      additionalContext: context,
    },
    suppressOutput: true,
  }));
}

async function fetchProjectContext(sessionId, project) {
  try {
    const res = await fetch(`${REST_URL}/agentmemory/context`, {
      method: "POST",
      headers: authHeaders(),
      body: JSON.stringify({ sessionId, project, budget: 1200 }),
      signal: AbortSignal.timeout(INJECT_TIMEOUT_MS),
    });
    if (!res.ok) return "";
    const result = await res.json();
    return typeof result.context === "string" ? result.context.trim() : "";
  } catch {
    return "";
  }
}

async function fetchPromptRecall(prompt, project) {
  const query = typeof prompt === "string" ? prompt.trim() : "";
  if (query.length < 4) return "";
  try {
    const res = await fetch(`${REST_URL}/agentmemory/search`, {
      method: "POST",
      headers: authHeaders(),
      body: JSON.stringify({
        query: query.slice(0, 500),
        limit: 5,
        project,
        format: "narrative",
        token_budget: 900,
      }),
      signal: AbortSignal.timeout(INJECT_TIMEOUT_MS),
    });
    if (!res.ok) return "";
    const result = await res.json();
    const text = typeof result.text === "string" ? result.text.trim() : "";
    if (!text) return "";
    return `<agentmemory-prompt-recall>\n## Relevant Past Context\n${text}\n</agentmemory-prompt-recall>`;
  } catch {
    return "";
  }
}

async function observePrompt(sessionId, project, prompt) {
  try {
    await fetch(`${REST_URL}/agentmemory/observe`, {
      method: "POST",
      headers: authHeaders(),
      body: JSON.stringify({
        hookType: "prompt_submit",
        sessionId,
        project,
        cwd: project,
        timestamp: new Date().toISOString(),
        data: { prompt },
      }),
      signal: AbortSignal.timeout(OBSERVE_TIMEOUT_MS),
    });
  } catch {}
}

async function main() {
  let input = "";
  for await (const chunk of process.stdin) input += chunk;
  let data;
  try {
    data = JSON.parse(input);
  } catch {
    return;
  }
  if (isSdkChildContext(data)) return;

  const sessionId = data.session_id || "unknown";
  const project = data.cwd || process.cwd();
  if (!INJECT_CONTEXT) {
    await observePrompt(sessionId, project, data.prompt);
    return;
  }

  const [projectContext, promptRecall] = await Promise.all([
    fetchProjectContext(sessionId, project),
    fetchPromptRecall(data.prompt, project),
    observePrompt(sessionId, project, data.prompt),
  ]);
  const context = [projectContext, promptRecall].filter(Boolean).join("\n\n");
  if (context) writeCodexContext(context);
}

main();
""",
    "pre-tool-use.mjs": r"""#!/usr/bin/env node
function isSdkChildContext(payload) {
  if (process.env["AGENTMEMORY_SDK_CHILD"] === "1") return true;
  if (!payload || typeof payload !== "object") return false;
  return payload.entrypoint === "sdk-ts";
}

const INJECT_CONTEXT = process.env["AGENTMEMORY_INJECT_CONTEXT"] === "true";
const REST_URL = process.env["AGENTMEMORY_URL"] || "http://localhost:3111";
const SECRET = process.env["AGENTMEMORY_SECRET"] || "";

function authHeaders() {
  const h = { "Content-Type": "application/json" };
  if (SECRET) h["Authorization"] = `Bearer ${SECRET}`;
  return h;
}

function writeCodexContext(context) {
  if (!context) return;
  process.stdout.write(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      additionalContext: context,
    },
    suppressOutput: true,
  }));
}

async function main() {
  if (!INJECT_CONTEXT) return;
  let input = "";
  for await (const chunk of process.stdin) input += chunk;
  let data;
  try {
    data = JSON.parse(input);
  } catch {
    return;
  }
  if (isSdkChildContext(data)) return;

  const toolName = data.tool_name;
  if (!["Edit", "Write", "Read", "Glob", "Grep"].includes(toolName)) return;

  const toolInput = data.tool_input || {};
  const files = [];
  const fileKeys = toolName === "Grep" ? ["path", "file"] : ["file_path", "path", "file", "pattern"];
  for (const key of fileKeys) {
    const val = toolInput[key];
    if (typeof val === "string" && val.length > 0) files.push(val);
  }
  if (files.length === 0) return;

  const terms = [];
  if (toolName === "Grep" || toolName === "Glob") {
    const pattern = toolInput["pattern"];
    if (typeof pattern === "string" && pattern.length > 0) terms.push(pattern);
  }

  try {
    const res = await fetch(`${REST_URL}/agentmemory/enrich`, {
      method: "POST",
      headers: authHeaders(),
      body: JSON.stringify({
        sessionId: data.session_id || "unknown",
        files,
        terms,
        toolName,
      }),
      signal: AbortSignal.timeout(2000),
    });
    if (res.ok) {
      const result = await res.json();
      if (result.context) writeCodexContext(result.context);
    }
  } catch {}
}

main();
""",
}

CONTEXT_HELPERS = r"""function normalizeProjectPath(project) {
	return String(project || "").replace(/\\/g, "/").replace(/\/+$/g, "").toLowerCase();
}
function codexScratchRoot(project) {
	const normalized = normalizeProjectPath(project);
	const match = normalized.match(/^(.*\/documents\/codex\/\d{4}-\d{2}-\d{2})\/[^/]+$/);
	return match ? match[1] : "";
}
function isContextProjectMatch(sessionProject, currentProject) {
	if (sessionProject === currentProject) return true;
	const sessionNorm = normalizeProjectPath(sessionProject);
	const currentNorm = normalizeProjectPath(currentProject);
	if (sessionNorm === currentNorm) return true;
	const currentRoot = codexScratchRoot(currentProject);
	return !!currentRoot && codexScratchRoot(sessionProject) === currentRoot;
}
function semanticMatchesProject(memory, currentProject) {
	const leaf = normalizeProjectPath(currentProject).split("/").filter(Boolean).pop() || "";
	const compactLeaf = leaf.replace(/[^a-z0-9]+/g, "");
	const hints = [leaf, compactLeaf].filter((hint) => hint.length >= 4);
	if (hints.length === 0) return false;
	const fact = String(memory?.fact || "").toLowerCase();
	const compactFact = fact.replace(/[^a-z0-9]+/g, "");
	return hints.some((hint) => fact.includes(hint) || compactFact.includes(hint));
}
"""

BACKGROUND_IMPORTS = 'import { readFileSync, writeFileSync } from "node:fs";\nimport { join } from "node:path";\nimport { tmpdir } from "node:os";\n'
BACKGROUND_READONLY_IMPORTS = 'import { readFileSync } from "node:fs";\nimport { join } from "node:path";\nimport { tmpdir } from "node:os";\n'
BACKGROUND_FILE_CONST = 'const IGNORED_SESSIONS_FILE = join(tmpdir(), "agentmemory-codex-ignored-sessions.json");\n'
BACKGROUND_READER = r"""function isIgnoredSession(sessionId) {
	try {
		const parsed = JSON.parse(readFileSync(IGNORED_SESSIONS_FILE, "utf8"));
		return Array.isArray(parsed) && parsed.includes(sessionId);
	} catch {
		return false;
	}
}
"""
BACKGROUND_PROMPT_HELPERS = r"""function readIgnoredSessions() {
	try {
		const parsed = JSON.parse(readFileSync(IGNORED_SESSIONS_FILE, "utf8"));
		return new Set(Array.isArray(parsed) ? parsed : []);
	} catch {
		return new Set();
	}
}
function isIgnoredSession(sessionId) {
	return !!sessionId && readIgnoredSessions().has(sessionId);
}
function rememberIgnoredSession(sessionId) {
	if (!sessionId || sessionId === "unknown") return;
	const ignored = readIgnoredSessions();
	ignored.add(sessionId);
	writeFileSync(IGNORED_SESSIONS_FILE, JSON.stringify([...ignored].slice(-200)), "utf8");
}
function isCodexBackgroundSuggestionPrompt(prompt) {
	const text = typeof prompt === "string" ? prompt.trim() : "";
	return text.startsWith("# Overview Generate 0 to 3 hyperpersonalized suggestions for what this user can do with Codex in this local project:");
}
async function forgetSession(sessionId) {
	if (!sessionId || sessionId === "unknown") return;
	try {
		await fetch(`${REST_URL}/agentmemory/forget`, {
			method: "POST",
			headers: authHeaders(),
			body: JSON.stringify({ sessionId }),
			signal: AbortSignal.timeout(OBSERVE_TIMEOUT_MS)
		});
	} catch {}
}
"""

SERVICE_BACKGROUND_HELPERS = r"""const CODEX_BACKGROUND_SUGGESTION_SESSIONS = new Set();
function getCodexPromptTextFromPayload(payload) {
	const data = payload?.data;
	if (typeof data === "object" && data !== null) return String(data.prompt ?? data.userPrompt ?? data.message ?? data.text ?? "");
	if (typeof data === "string") return data;
	return "";
}
function isCodexBackgroundSuggestionText(text) {
	const normalized = String(text || "").replace(/\s+/g, " ").trim();
	return normalized.includes("Generate 0 to 3 hyperpersonalized suggestions for what this user can do with Codex in this local project");
}
async function deleteCodexBackgroundSession(kv, sessionId) {
	try {
		const observations = await kv.list(KV.observations(sessionId));
		for (const obs of observations) await kv.delete(KV.observations(sessionId), obs.id);
	} catch {}
	try { await kv.delete(KV.sessions, sessionId); } catch {}
	try { await kv.delete(KV.summaries, sessionId); } catch {}
}
"""


def parse_args() -> argparse.Namespace:
    default_codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", type=Path, default=default_codex_home)
    parser.add_argument("--url", default=None, help="agentmemory REST URL")
    parser.add_argument("--secret", default=None, help="agentmemory bearer secret")
    parser.add_argument("--plugin-root", type=Path, default=None)
    parser.add_argument("--node-exe", type=Path, default=None)
    parser.add_argument("--inject-context", choices=["true", "false"], default="true")
    parser.add_argument("--preserve-other-hooks", action="store_true")
    parser.add_argument("--skip-mcp-config", action="store_true")
    parser.add_argument("--skip-injection-patch", action="store_true", help="Do not rewrite hook scripts for Codex additionalContext JSON output.")
    parser.add_argument("--patch-codex-scratch-context", action="store_true", help="Patch agentmemory service bundles to share context across Codex daily scratch folders.")
    parser.add_argument("--agentmemory-package-root", type=Path, action="append", default=[], help="Path to an @agentmemory/agentmemory package root to patch.")
    parser.add_argument("--absolute-data-dir", type=Path, default=None, help="Patch iii-config.yaml to use this absolute data directory.")
    parser.add_argument("--skip-hook-validation", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def backup(path: Path) -> Path | None:
    if not path.exists():
        return None
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out = path.with_name(f"{path.name}.bak-agentmemory-windows-{stamp}")
    shutil.copy2(path, out)
    return out


def write_with_backup(path: Path, text: str, dry_run: bool) -> bool:
    current = read_text(path)
    if current == text:
        return False
    if dry_run:
        print(f"would update: {path}")
        return True
    backup(path)
    path.write_text(text, encoding="utf-8", newline="\n")
    return True


def extract_config_value(config: str, key: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(key)}\s*=\s*['\"]([^'\"]*)['\"]", config)
    return match.group(1) if match else None


def find_plugin_root(codex_home: Path, explicit: Path | None) -> Path:
    candidates: list[Path] = []
    if explicit:
        candidates.append(explicit)
    cache_root = codex_home / "plugins" / "cache" / "agentmemory" / "agentmemory"
    if cache_root.exists():
        candidates.extend(sorted((p for p in cache_root.iterdir() if p.is_dir()), reverse=True))
    for candidate in candidates:
        if (candidate / "scripts" / "session-start.mjs").exists():
            return candidate
    raise SystemExit("Could not find agentmemory plugin root. Pass --plugin-root.")


def find_node(explicit: Path | None) -> Path:
    candidates: list[Path] = []
    if explicit:
        candidates.append(explicit)
    which = shutil.which("node.exe") or shutil.which("node")
    if which:
        candidates.append(Path(which))
    candidates.append(Path(r"C:\Program Files\nodejs\node.exe"))
    local = os.environ.get("LOCALAPPDATA")
    if local:
        candidates.extend(Path(local).glob(r"OpenAI\Codex\bin\*\node.exe"))
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise SystemExit("Could not find node.exe. Install Node.js or pass --node-exe.")


def cmd_quote(path: Path) -> str:
    return str(path)


def hook_command(wrapper: Path, script: str) -> str:
    return f'cmd.exe /d /s /c ""{cmd_quote(wrapper)}" {script}"'


def build_agentmemory_hooks(wrapper: Path) -> tuple[dict, dict[str, str]]:
    hooks = {}
    hashes = {}
    for event, (key, script) in EVENTS.items():
        command = hook_command(wrapper, script)
        entry = {"hooks": [{"type": "command", "command": command}]}
        if event == "PreToolUse":
            entry["matcher"] = "Edit|Write|Read|Glob|Grep"
        if event == "SessionStart":
            entry["hooks"][0]["statusMessage"] = "agentmemory: loading session context"
        if event == "UserPromptSubmit":
            entry["hooks"][0]["statusMessage"] = "agentmemory: recalling relevant memories"
        hooks[event] = [entry]
        hashes[key] = "sha256:" + hashlib.sha256(command.encode("utf-8")).hexdigest()
    return {"hooks": hooks}, hashes


def is_agentmemory_entry(entry: dict) -> bool:
    text = json.dumps(entry, ensure_ascii=False).lower()
    return "agentmemory" in text or "pre-tool-use.mjs" in text or "post-tool-use.mjs" in text


def merge_hooks(existing: dict, agent_hooks: dict) -> dict:
    out = {"hooks": dict(existing.get("hooks", {}))}
    for event, entries in agent_hooks["hooks"].items():
        preserved = [e for e in out["hooks"].get(event, []) if not is_agentmemory_entry(e)]
        out["hooks"][event] = entries + preserved
    return out


def make_wrapper(wrapper: Path, node_exe: Path, plugin_root: Path, url: str, secret: str, inject: str) -> str:
    if '"' in secret or '"' in url:
        raise SystemExit('AGENTMEMORY_SECRET and AGENTMEMORY_URL must not contain double quotes for .cmd wrapper safety.')
    return "\n".join(
        [
            "@echo off",
            f'set "AGENTMEMORY_URL={url}"',
            f'set "AGENTMEMORY_SECRET={secret}"',
            f'set "AGENTMEMORY_INJECT_CONTEXT={inject}"',
            'if "%~1"=="" exit /b 2',
            f'"{node_exe}" "{plugin_root}\\scripts\\%~1"',
            "exit /b %ERRORLEVEL%",
            "",
        ]
    )


def remove_section(text: str, header: str) -> str:
    pattern = rf"(?ms)^\[{re.escape(header)}\]\s*.*?(?=^\[|\Z)"
    return re.sub(pattern, "", text).rstrip() + "\n"


def upsert_section_key(config: str, section: str, key: str, value: str) -> str:
    header = f"[{section}]"
    quoted = json.dumps(value)
    if header not in config:
        return config.rstrip() + f"\n\n{header}\n{key} = {quoted}\n"
    pattern = rf"(?ms)(^\[{re.escape(section)}\]\s*.*?)(?=^\[|\Z)"
    match = re.search(pattern, config)
    if not match:
        return config
    block = match.group(1).rstrip()
    key_pattern = rf"(?m)^({re.escape(key)}\s*=\s*).*$"
    if re.search(key_pattern, block):
        block = re.sub(key_pattern, rf"\1{quoted}", block)
    else:
        block += f"\n{key} = {quoted}"
    return config[: match.start(1)] + block + "\n\n" + config[match.end(1) :]


def upsert_trust_state(config: str, hooks_path: Path, hashes: dict[str, str]) -> str:
    for key, digest in hashes.items():
        section = f"hooks.state.'{hooks_path}:{key}:0:0'"
        config = upsert_section_key(config, section, "enabled", "true")
        config = re.sub(
            rf"(?ms)(^\[{re.escape(section)}\]\s*.*?^enabled\s*=\s*)\"true\"",
            r"\1true",
            config,
        )
        config = upsert_section_key(config, section, "trusted_hash", digest)
    return config


def configure_mcp(config: str, url: str, secret: str) -> str:
    config = remove_section(config, "mcp_servers.agentmemory")
    config = remove_section(config, "mcp_servers.agentmemory.env")
    block = f"""
[mcp_servers.agentmemory]
command = "npx"
args = ["-y", "@agentmemory/mcp"]

[mcp_servers.agentmemory.env]
AGENTMEMORY_URL = "{url}"
AGENTMEMORY_SECRET = "{secret}"
"""
    return config.rstrip() + "\n" + block


def disable_plugin_hooks(config: str) -> str:
    for key in EVENTS.values():
        section = f'hooks.state."agentmemory@agentmemory:hooks/hooks.codex.json:{key[0]}:0:0"'
        if f"[{section}]" in config:
            config = upsert_section_key(config, section, "enabled", "false")
            config = re.sub(
                rf"(?ms)(^\[{re.escape(section)}\]\s*.*?^enabled\s*=\s*)\"false\"",
                r"\1false",
                config,
            )
    return config


def patch_injection_scripts(plugin_root: Path, dry_run: bool) -> list[Path]:
    changed: list[Path] = []
    scripts_dir = plugin_root / "scripts"
    for name, text in HOOK_SCRIPT_REPLACEMENTS.items():
        path = scripts_dir / name
        if not path.exists():
            raise SystemExit(f"Missing hook script: {path}")
        final_text = text
        if name == "prompt-submit.mjs":
            final_text = patch_prompt_background_filter(final_text)
        elif name == "pre-tool-use.mjs":
            final_text = patch_readonly_background_filter(final_text, name)
        if write_with_backup(path, final_text, dry_run):
            changed.append(path)
    return changed


def add_imports_after_shebang(text: str, imports: str) -> str:
    if imports.strip() in text:
        return text
    if text.startswith("#!/usr/bin/env node\n"):
        return text.replace("#!/usr/bin/env node\n", "#!/usr/bin/env node\n" + imports, 1)
    return imports + text


def patch_prompt_background_filter(text: str) -> str:
    if "agentmemory-codex-ignored-sessions.json" in text:
        return text
    text = add_imports_after_shebang(text, BACKGROUND_IMPORTS)
    text = text.replace("const OBSERVE_TIMEOUT_MS = 1600;\n", "const OBSERVE_TIMEOUT_MS = 1600;\n" + BACKGROUND_FILE_CONST, 1)
    text = text.replace("function writeCodexContext(context) {", BACKGROUND_PROMPT_HELPERS + "function writeCodexContext(context) {", 1)
    marker = "const project = data.cwd || process.cwd();\n"
    guard = (
        marker
        + "\tif (isCodexBackgroundSuggestionPrompt(data.prompt)) {\n"
        + "\t\trememberIgnoredSession(sessionId);\n"
        + "\t\tawait forgetSession(sessionId);\n"
        + "\t\treturn;\n"
        + "\t}\n"
        + "\tif (isIgnoredSession(sessionId)) return;\n"
    )
    return text.replace(marker, guard, 1)


def patch_readonly_background_filter(text: str, script_name: str) -> str:
    if "agentmemory-codex-ignored-sessions.json" in text:
        return text
    text = add_imports_after_shebang(text, BACKGROUND_READONLY_IMPORTS)
    text = text.replace('const SECRET = process.env["AGENTMEMORY_SECRET"] || "";\n', 'const SECRET = process.env["AGENTMEMORY_SECRET"] || "";\n' + BACKGROUND_FILE_CONST, 1)
    text = text.replace("async function main() {", BACKGROUND_READER + "async function main() {", 1)
    if script_name == "pre-tool-use.mjs":
        marker = "const toolInput = data.tool_input || {};\n"
        guard = 'const sessionId = data.session_id || "unknown";\n\tif (isIgnoredSession(sessionId)) return;\n\t'
        text = text.replace(marker, guard + marker, 1)
        text = text.replace('sessionId: data.session_id || "unknown",', "sessionId,", 1)
        return text
    marker = 'const sessionId = data.session_id || "unknown";\n'
    return text.replace(marker, marker + "\tif (isIgnoredSession(sessionId)) return;\n", 1)


def patch_background_suggestion_filter(plugin_root: Path, dry_run: bool) -> list[Path]:
    changed: list[Path] = []
    scripts_dir = plugin_root / "scripts"
    for script_name in ["prompt-submit.mjs", "pre-tool-use.mjs", "post-tool-use.mjs", "stop.mjs", "pre-compact.mjs"]:
        path = scripts_dir / script_name
        if not path.exists():
            continue
        original = read_text(path)
        if script_name == "prompt-submit.mjs":
            final = patch_prompt_background_filter(original)
        else:
            final = patch_readonly_background_filter(original, script_name)
        if final != original and write_with_backup(path, final, dry_run):
            changed.append(path)
    return changed


def npm_global_root() -> Path | None:
    try:
        proc = subprocess.run(
            ["npm.cmd", "root", "-g"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None
    root = Path(proc.stdout.strip())
    return root if root.exists() else None


def find_agentmemory_package_roots(explicit: list[Path]) -> list[Path]:
    candidates: list[Path] = [p.expanduser() for p in explicit]
    appdata = os.environ.get("APPDATA")
    if appdata:
        candidates.append(Path(appdata) / "npm" / "node_modules" / "@agentmemory" / "agentmemory")
    global_root = npm_global_root()
    if global_root:
        candidates.append(global_root / "@agentmemory" / "agentmemory")
    localappdata = os.environ.get("LOCALAPPDATA")
    if localappdata:
        candidates.extend(Path(localappdata).glob(r"npm-cache\_npx\*\node_modules\@agentmemory\agentmemory"))

    roots: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        try:
            key = str(candidate.resolve()).lower()
        except OSError:
            continue
        if key in seen:
            continue
        seen.add(key)
        if (candidate / "dist").exists():
            roots.append(candidate)
    return roots


def patch_absolute_data_paths(package_roots: list[Path], data_dir: Path, dry_run: bool) -> list[Path]:
    changed: list[Path] = []
    state_file = (data_dir.expanduser() / "state_store.db").as_posix()
    stream_dir = (data_dir.expanduser() / "stream_store").as_posix()
    for root in package_roots:
        config_path = root / "dist" / "iii-config.yaml"
        if not config_path.exists():
            continue
        lines = read_text(config_path).splitlines()
        out = []
        for line in lines:
            if "file_path:" in line and "state_store.db" in line:
                out.append(re.sub(r"file_path:\s*.*$", f"file_path: {state_file}", line))
            elif "file_path:" in line and "stream_store" in line:
                out.append(re.sub(r"file_path:\s*.*$", f"file_path: {stream_dir}", line))
            else:
                out.append(line)
        final = "\n".join(out) + "\n"
        if write_with_backup(config_path, final, dry_run):
            changed.append(config_path)
    return changed


def patch_context_bundle(path: Path, dry_run: bool) -> bool:
    text = read_text(path)
    if "function isContextProjectMatch(sessionProject, currentProject)" in text:
        return False

    escape_block = (
        'function escapeXmlAttr(s) {\n'
        '\treturn s.replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;").replace(/>/g, "&gt;");\n'
        '}\n'
    )
    promise_old = (
        "\t\tconst [pinnedSlots, profile, lessons] = await Promise.all([\n"
        "\t\t\tisSlotsEnabled() ? listPinnedSlots(kv).catch(() => []) : Promise.resolve([]),\n"
        "\t\t\tkv.get(KV.profiles, data.project).catch(() => null),\n"
        "\t\t\tkv.list(KV.lessons).catch(() => [])\n"
        "\t\t]);\n"
    )
    promise_new = (
        "\t\tconst [pinnedSlots, profile, lessons, allSessions, semanticMemories] = await Promise.all([\n"
        "\t\t\tisSlotsEnabled() ? listPinnedSlots(kv).catch(() => []) : Promise.resolve([]),\n"
        "\t\t\tkv.get(KV.profiles, data.project).catch(() => null),\n"
        "\t\t\tkv.list(KV.lessons).catch(() => []),\n"
        "\t\t\tkv.list(KV.sessions),\n"
        "\t\t\tkv.list(KV.semantic).catch(() => [])\n"
        "\t\t]);\n"
        "\t\tconst relatedSessionIds = new Set(allSessions.filter((s) => isContextProjectMatch(s.project, data.project) && s.id !== data.sessionId).map((s) => s.id));\n"
    )
    sessions_old = (
        "\t\tconst sessions = (await kv.list(KV.sessions)).filter((s) => s.project === data.project && s.id !== data.sessionId).sort((a, b) => new Date(b.startedAt).getTime() - new Date(a.startedAt).getTime()).slice(0, 10);\n"
    )
    semantic_block = (
        "\t\tconst relevantSemantic = semanticMemories.filter((m) => semanticMatchesProject(m, data.project) && Array.isArray(m.sourceSessionIds) && m.sourceSessionIds.some((id) => relatedSessionIds.has(id))).sort((a, b) => {\n"
        "\t\t\tconst scoreA = (a.strength ?? a.confidence ?? 0) + new Date(a.updatedAt || a.createdAt || 0).getTime() / 1e15;\n"
        "\t\t\tconst scoreB = (b.strength ?? b.confidence ?? 0) + new Date(b.updatedAt || b.createdAt || 0).getTime() / 1e15;\n"
        "\t\t\treturn scoreB - scoreA;\n"
        "\t\t}).slice(0, 8);\n"
        "\t\tif (relevantSemantic.length > 0) {\n"
        "\t\t\tconst semanticContent = `## Long-Term Semantic Memories\\n${relevantSemantic.map((m) => `- ${m.fact}`).join(\"\\n\")}`;\n"
        "\t\t\tblocks.push({\n"
        "\t\t\t\ttype: \"memory\",\n"
        "\t\t\t\tcontent: semanticContent,\n"
        "\t\t\t\ttokens: estimateTokens$1(semanticContent),\n"
        "\t\t\t\trecency: relevantSemantic.reduce((acc, m) => Math.max(acc, new Date(m.updatedAt || m.createdAt || 0).getTime()), 0),\n"
        "\t\t\t\tsourceIds: relevantSemantic.map((m) => m.id)\n"
        "\t\t\t});\n"
        "\t\t}\n"
    )
    sessions_new = (
        semantic_block
        + "\t\tconst sessions = allSessions.filter((s) => isContextProjectMatch(s.project, data.project) && s.id !== data.sessionId).sort((a, b) => new Date(b.startedAt).getTime() - new Date(a.startedAt).getTime()).slice(0, 10);\n"
    )

    if escape_block not in text or promise_old not in text or sessions_old not in text:
        print(f"skip context patch, unrecognized bundle shape: {path}")
        return False

    text = text.replace(escape_block, escape_block + CONTEXT_HELPERS, 1)
    text = text.replace(promise_old, promise_new, 1)
    text = text.replace(sessions_old, sessions_new, 1)
    return write_with_backup(path, text, dry_run)


def patch_codex_scratch_context(package_roots: list[Path], dry_run: bool) -> list[Path]:
    changed: list[Path] = []
    for root in package_roots:
        dist = root / "dist"
        bundle_paths = [dist / "index.mjs"]
        bundle_paths.extend(sorted(dist.glob("src-*.mjs")))
        for path in bundle_paths:
            if path.exists() and patch_context_bundle(path, dry_run):
                changed.append(path)
    return changed


def patch_service_background_filter_bundle(path: Path, dry_run: bool) -> bool:
    text = read_text(path)
    original = text
    if "CODEX_BACKGROUND_SUGGESTION_SESSIONS" not in text:
        marker = 'function registerObserveFunction(sdk, kv, dedupMap, maxObservationsPerSession) {'
        if marker not in text:
            print(f"skip background service filter, no observe marker: {path}")
            return False
        text = text.replace(marker, SERVICE_BACKGROUND_HELPERS + marker, 1)

    validation = (
        '\t\tif (!payload?.sessionId || typeof payload.sessionId !== "string" || !payload.hookType || typeof payload.hookType !== "string" || !payload.timestamp || typeof payload.timestamp !== "string") return {\n'
        '\t\t\tsuccess: false,\n'
        '\t\t\terror: "Invalid payload: sessionId, hookType, and timestamp are required"\n'
        '\t\t};\n'
    )
    observe_guard = validation + (
        '\t\tif (CODEX_BACKGROUND_SUGGESTION_SESSIONS.has(payload.sessionId)) return {\n'
        '\t\t\tignored: true,\n'
        '\t\t\tsessionId: payload.sessionId\n'
        '\t\t};\n'
        '\t\tif (isCodexBackgroundSuggestionText(getCodexPromptTextFromPayload(payload))) {\n'
        '\t\t\tCODEX_BACKGROUND_SUGGESTION_SESSIONS.add(payload.sessionId);\n'
        '\t\t\tawait deleteCodexBackgroundSession(kv, payload.sessionId);\n'
        '\t\t\treturn {\n'
        '\t\t\t\tignored: true,\n'
        '\t\t\t\tsessionId: payload.sessionId\n'
        '\t\t\t};\n'
        '\t\t}\n'
    )
    if observe_guard not in text:
        if validation not in text:
            print(f"skip background service filter, no validation marker: {path}")
            return False
        text = text.replace(validation, observe_guard, 1)

    title_line = '\t\tconst title = typeof body.title === "string" ? body.title.trim() : void 0;\n'
    title_guard = title_line + (
        '\t\tif (isCodexBackgroundSuggestionText(title)) return {\n'
        '\t\t\tstatus_code: 200,\n'
        '\t\t\tbody: { ignored: true, context: "" }\n'
        '\t\t};\n'
    )
    if title_guard not in text and title_line in text:
        text = text.replace(title_line, title_guard, 1)

    return text != original and write_with_backup(path, text, dry_run)


def patch_service_background_filter(package_roots: list[Path], dry_run: bool) -> list[Path]:
    changed: list[Path] = []
    for root in package_roots:
        dist = root / "dist"
        bundle_paths = [dist / "index.mjs"]
        bundle_paths.extend(sorted(dist.glob("src-*.mjs")))
        for path in bundle_paths:
            if path.exists() and patch_service_background_filter_bundle(path, dry_run):
                changed.append(path)
    return changed


def validate_hooks(agent_hooks: dict) -> list[tuple[str, int]]:
    payload = '{"session_id":"agentmemory-windows-test","cwd":"C:\\\\Temp","prompt":"test"}'
    results = []
    for event, entries in agent_hooks["hooks"].items():
        command = entries[0]["hooks"][0]["command"]
        proc = subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command", command],
            input=payload,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=15,
        )
        results.append((event, proc.returncode))
        if proc.returncode != 0:
            sys.stderr.write(f"{event} stderr:\n{proc.stderr}\n")
    return results


def main() -> None:
    args = parse_args()
    codex_home = args.codex_home.expanduser()
    hooks_path = codex_home / "hooks.json"
    config_path = codex_home / "config.toml"
    wrapper = codex_home / "agentmemory-hook.cmd"

    config = read_text(config_path)
    url = args.url or os.environ.get("AGENTMEMORY_URL") or extract_config_value(config, "AGENTMEMORY_URL") or "http://localhost:3111"
    secret = args.secret or os.environ.get("AGENTMEMORY_SECRET") or extract_config_value(config, "AGENTMEMORY_SECRET")
    if not secret:
        raise SystemExit("Missing AGENTMEMORY_SECRET. Pass --secret or add it to Codex config/environment.")

    plugin_root = find_plugin_root(codex_home, args.plugin_root)
    node_exe = find_node(args.node_exe)
    agent_hooks, hashes = build_agentmemory_hooks(wrapper)
    package_roots = find_agentmemory_package_roots(args.agentmemory_package_root)

    existing_hooks = json.loads(read_text(hooks_path) or "{}")
    final_hooks = merge_hooks(existing_hooks, agent_hooks) if args.preserve_other_hooks else agent_hooks

    final_config = config
    final_config = upsert_trust_state(final_config, hooks_path, hashes)
    final_config = disable_plugin_hooks(final_config)
    final_config = upsert_section_key(final_config, "shell_environment_policy.set", "AGENTMEMORY_INJECT_CONTEXT", args.inject_context)
    final_config = upsert_section_key(final_config, "shell_environment_policy.set", "AGENTMEMORY_URL", url)
    final_config = upsert_section_key(final_config, "shell_environment_policy.set", "AGENTMEMORY_SECRET", secret)
    if not args.skip_mcp_config:
        final_config = configure_mcp(final_config, url, secret)

    wrapper_text = make_wrapper(wrapper, node_exe, plugin_root, url, secret, args.inject_context)

    print(f"Codex home: {codex_home}")
    print(f"Plugin root: {plugin_root}")
    print(f"Node: {node_exe}")
    print(f"Hooks path: {hooks_path}")
    print(f"Config path: {config_path}")
    if package_roots:
        print("agentmemory package roots:")
        for root in package_roots:
            print(f"  {root}")
    if args.dry_run:
        print("Dry run: no files written.")
        if not args.skip_injection_patch:
            patch_injection_scripts(plugin_root, dry_run=True)
            patch_background_suggestion_filter(plugin_root, dry_run=True)
            patch_service_background_filter(package_roots, dry_run=True)
        if args.absolute_data_dir:
            patch_absolute_data_paths(package_roots, args.absolute_data_dir, dry_run=True)
        if args.patch_codex_scratch_context:
            patch_codex_scratch_context(package_roots, dry_run=True)
        return

    codex_home.mkdir(parents=True, exist_ok=True)
    hooks_backup = backup(hooks_path)
    config_backup = backup(config_path)
    if hooks_backup:
        print(f"hooks backup: {hooks_backup}")
    if config_backup:
        print(f"config backup: {config_backup}")

    wrapper.write_text(wrapper_text, encoding="utf-8")
    hooks_path.write_text(json.dumps(final_hooks, indent=2) + "\n", encoding="utf-8")
    config_path.write_text(final_config, encoding="utf-8")

    if not args.skip_injection_patch:
        changed_scripts = patch_injection_scripts(plugin_root, dry_run=False)
        for path in changed_scripts:
            print(f"patched injection script: {path}")
        changed_filter_scripts = patch_background_suggestion_filter(plugin_root, dry_run=False)
        for path in changed_filter_scripts:
            print(f"patched background suggestion filter: {path}")
        changed_service_filters = patch_service_background_filter(package_roots, dry_run=False)
        for path in changed_service_filters:
            print(f"patched service background suggestion filter: {path}")
        if changed_service_filters:
            print("Restart agentmemory so the patched service filter is loaded.")
    if args.absolute_data_dir:
        changed_configs = patch_absolute_data_paths(package_roots, args.absolute_data_dir, dry_run=False)
        for path in changed_configs:
            print(f"patched absolute data path: {path}")
    if args.patch_codex_scratch_context:
        changed_bundles = patch_codex_scratch_context(package_roots, dry_run=False)
        for path in changed_bundles:
            print(f"patched Codex scratch context matching: {path}")
        if changed_bundles:
            print("Restart agentmemory so the patched service bundle is loaded.")

    if not args.skip_hook_validation:
        results = validate_hooks(agent_hooks)
        for event, code in results:
            print(f"{event}: exit={code}")
        if any(code != 0 for _, code in results):
            raise SystemExit("One or more hook commands failed validation.")
    print("agentmemory Windows hook configuration completed.")


if __name__ == "__main__":
    main()
