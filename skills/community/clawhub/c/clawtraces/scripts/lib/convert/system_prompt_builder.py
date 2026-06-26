# FILE_META
# INPUT:  tool names, cwd, model, thinking level
# OUTPUT: reconstructed system prompt string
# POS:    skill lib — fallback for cache_trace.py, called via the openclaw adapter
# MISSION: Reconstruct system prompt from workspace files when cache-trace is unavailable.

"""Extract session metadata from OpenClaw JSONL logs and reconstruct system prompts.

Reconstruction logic is reverse-engineered from OpenClaw's buildAgentSystemPrompt()
in dist/pi-embedded-*.js and related modules. It reads the same workspace files
(AGENTS.md, SOUL.md, etc.) and scans the same skill directories that OpenClaw uses
at runtime, producing a system prompt that closely matches the real one.

The main gap vs. a real cache-trace system prompt:
- Memory section is plugin-injected at runtime (we include MEMORY.md if it exists)
- Some runtime-only params (reactionGuidance, reasoningTagHint, etc.) are unavailable
"""

from __future__ import annotations

import os
import xml.sax.saxutils

# ---------------------------------------------------------------------------
# Complete tool summary map — mirrors OpenClaw coreToolSummaries
# ---------------------------------------------------------------------------

CORE_TOOL_SUMMARIES: dict[str, str] = {
    "read": "Read file contents",
    "write": "Create or overwrite files",
    "edit": "Make precise edits to files",
    "apply_patch": "Apply multi-file patches",
    "grep": "Search file contents for patterns",
    "find": "Find files by glob pattern",
    "ls": "List directory contents",
    "exec": "Run shell commands (pty available for TTY-required CLIs)",
    "process": "Manage background exec sessions",
    "web_search": "Search the web (Brave API)",
    "web_fetch": "Fetch and extract readable content from a URL",
    "browser": "Control web browser",
    "canvas": "Present/eval/snapshot the Canvas",
    "nodes": "List/describe/notify/camera/screen on paired nodes",
    "cron": "Manage cron jobs and wake events",
    "message": "Send messages and channel actions",
    "gateway": "Restart, apply config, or run updates on the running OpenClaw process",
    "agents_list": "List OpenClaw agent ids allowed for sessions_spawn",
    "sessions_list": "List other sessions (incl. sub-agents) with filters/last",
    "sessions_history": "Fetch history for another session/sub-agent",
    "sessions_send": "Send a message to another session/sub-agent",
    "sessions_spawn": "Spawn an isolated sub-agent session",
    "subagents": "List, steer, or kill sub-agent runs for this requester session",
    "session_status": "Show usage/time/model state",
    "image": "Analyze an image with the configured image model",
    "image_generate": "Generate images with the configured image-generation model",
    "pdf": "Analyze PDF documents with a model",
    "sessions_yield": "End your current turn",
    "tts": "Convert text to speech",
}

TOOL_ORDER = [
    "read", "write", "edit", "apply_patch", "grep", "find", "ls",
    "exec", "process", "web_search", "web_fetch", "browser", "canvas",
    "nodes", "cron", "message", "gateway", "agents_list", "sessions_list",
    "sessions_history", "sessions_send", "subagents", "session_status",
    "image", "image_generate",
]

# Context file names loaded by OpenClaw's loadWorkspaceBootstrapFiles()
CONTEXT_FILE_NAMES = [
    "AGENTS.md",
    "SOUL.md",
    "TOOLS.md",
    "IDENTITY.md",
    "USER.md",
    "HEARTBEAT.md",
]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _build_tool_lines(tool_names: list[str]) -> list[str]:
    """Build sorted tool lines matching OpenClaw's ordering logic."""
    available = set(t.lower() for t in tool_names)
    name_map = {t.lower(): t for t in tool_names}

    lines: list[str] = []
    seen: set[str] = set()

    for tool in TOOL_ORDER:
        if tool in available:
            canonical = name_map.get(tool, tool)
            summary = CORE_TOOL_SUMMARIES.get(tool, "")
            lines.append(f"- {canonical}: {summary}" if summary else f"- {canonical}")
            seen.add(tool)

    for tool in sorted(available - seen):
        canonical = name_map.get(tool, tool)
        summary = CORE_TOOL_SUMMARIES.get(tool, "")
        lines.append(f"- {canonical}: {summary}" if summary else f"- {canonical}")

    return lines


def _read_file_safe(path: str, max_chars: int = 20000) -> str | None:
    """Read a text file, return content or None if missing/error."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read(max_chars + 1)
        if len(content) > max_chars:
            content = content[:max_chars]
        return content.strip() if content.strip() else None
    except OSError:
        return None


def _parse_skill_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from a SKILL.md file.

    Extracts name, description, and eligibility/filter metadata from the
    --- delimited frontmatter block. Returns dict with string values for
    simple keys and structured data for complex keys (os, requires, etc.).
    """
    result: dict = {}
    if not content.startswith("---"):
        return result

    end = content.find("\n---", 3)
    if end == -1:
        return result

    frontmatter = content[3:end]

    # Try YAML parsing first for structured fields
    try:
        import yaml
        parsed = yaml.safe_load(frontmatter)
        if isinstance(parsed, dict):
            # Merge openclaw manifest metadata into top level for eligibility checks.
            # OpenClaw stores requires/os/always inside metadata.openclaw:
            #   metadata: { "openclaw": { "requires": { "config": [...] }, "os": [...] } }
            metadata = parsed.get("metadata", {})
            if isinstance(metadata, str):
                # metadata might be a JSON string
                try:
                    import json
                    metadata = json.loads(metadata)
                except (json.JSONDecodeError, ValueError):
                    metadata = {}
            if isinstance(metadata, dict):
                oc = metadata.get("openclaw", {})
                if isinstance(oc, dict):
                    # Merge openclaw manifest keys into parsed (lower priority than top-level)
                    for key in ("requires", "os", "always"):
                        if key in oc and key not in parsed:
                            parsed[key] = oc[key]
            return parsed
    except Exception:
        pass

    # Fallback: line-by-line parsing for simple key: value pairs
    for line in frontmatter.split("\n"):
        line = line.strip()
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip().lower()
        value = value.strip()
        # Strip surrounding quotes
        if len(value) >= 2 and value[0] in ('"', "'") and value[-1] == value[0]:
            value = value[1:-1]
        if value:
            result[key] = value

    return result


def _shorten_home(path: str) -> str:
    """Replace home directory prefix with ~."""
    home = os.path.expanduser("~")
    if path.startswith(home):
        return "~" + path[len(home):]
    return path


def _has_binary(name: str) -> bool:
    """Check if a binary is available on PATH (mirrors OpenClaw's hasBinary)."""
    import shutil
    return shutil.which(name) is not None


def _should_include_skill(fm: dict, source: str) -> bool:
    """Evaluate whether a skill should be included in the prompt.

    Mirrors OpenClaw's shouldIncludeSkill() + evaluateRuntimeEligibility():
    1. disable-model-invocation → exclude from prompt
    2. OS filter → only include if current platform matches
    3. always: true → skip requires checks
    4. requires.bins → all required binaries must exist on PATH
    5. requires.anyBins → at least one must exist
    6. requires.env → all required env vars must be set
    """
    import sys

    # disable-model-invocation: excluded from prompt entirely
    if fm.get("disable-model-invocation") is True:
        return False

    # OS filter
    os_list = fm.get("os", [])
    if isinstance(os_list, str):
        os_list = [os_list]
    if os_list:
        platform = sys.platform  # "darwin", "linux", "win32"
        if platform not in os_list:
            return False

    # always: true skips requires checks
    if fm.get("always") is True:
        return True

    # requires checks
    requires = fm.get("requires", {})
    if not isinstance(requires, dict):
        return True

    # requires.bins — all must exist
    req_bins = requires.get("bins", [])
    if isinstance(req_bins, list) and req_bins:
        for b in req_bins:
            if isinstance(b, str) and not _has_binary(b):
                return False

    # requires.anyBins — at least one must exist
    any_bins = requires.get("anyBins", [])
    if isinstance(any_bins, list) and any_bins:
        if not any(_has_binary(b) for b in any_bins if isinstance(b, str)):
            return False

    # requires.env — all must be set
    req_env = requires.get("env", [])
    if isinstance(req_env, list) and req_env:
        for env_name in req_env:
            if isinstance(env_name, str) and not os.environ.get(env_name):
                return False

    # requires.config — all config paths must be truthy in openclaw.json
    req_config = requires.get("config", [])
    if isinstance(req_config, list) and req_config:
        config = _load_openclaw_config()
        for config_path in req_config:
            if isinstance(config_path, str) and not _is_config_path_truthy(config, config_path):
                return False

    return True


# Cache for openclaw config (loaded once per scan)
_openclaw_config_cache: dict | None = None


def _load_openclaw_config() -> dict:
    """Load full OpenClaw config (cached)."""
    global _openclaw_config_cache
    if _openclaw_config_cache is not None:
        return _openclaw_config_cache
    import json
    state_dir = os.environ.get("OPENCLAW_STATE_DIR", os.path.expanduser("~/.openclaw"))
    config_path = os.path.join(state_dir, "openclaw.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            _openclaw_config_cache = json.load(f)
    except (OSError, json.JSONDecodeError):
        _openclaw_config_cache = {}
    return _openclaw_config_cache


def _is_config_path_truthy(config: dict, path_str: str) -> bool:
    """Check if a dot-separated config path resolves to a truthy value.

    Mirrors OpenClaw's isConfigPathTruthy() with default values.
    """
    defaults = {
        "browser.enabled": True,
        "browser.evaluateEnabled": True,
    }
    current = config
    for part in path_str.split("."):
        if not isinstance(current, dict):
            # Path doesn't exist, check defaults
            return defaults.get(path_str, False)
        current = current.get(part)
    if current is None:
        return defaults.get(path_str, False)
    if isinstance(current, bool):
        return current
    if isinstance(current, (int, float)):
        return current != 0
    if isinstance(current, str):
        return len(current.strip()) > 0
    return bool(current)


# Max chars for skills section (matches OpenClaw DEFAULT_MAX_SKILLS_PROMPT_CHARS)
MAX_SKILLS_PROMPT_CHARS = 30000


def _load_openclaw_skill_config() -> dict:
    """Load OpenClaw config and extract skills.entries for enabled/disabled checks.

    Returns dict mapping skill name → config dict (e.g. {"enabled": False}).
    """
    config = _load_openclaw_config()
    return config.get("skills", {}).get("entries", {})


def _scan_skills(workspace_dir: str) -> list[dict[str, str]]:
    """Scan workspace and OpenClaw extension dirs for skills.

    Returns list of dicts with keys: name, description, filePath.
    Mirrors OpenClaw's loadSkillEntries() + filterSkillEntries() logic.
    """
    skills: list[dict[str, str]] = []
    seen_names: set[str] = set()
    skill_config = _load_openclaw_skill_config()

    # Collect skill root directories to scan
    scan_dirs: list[str] = []

    # 1. Workspace skills dir (workspace/skills/)
    ws_skills = os.path.join(workspace_dir, "skills")
    if os.path.isdir(ws_skills):
        scan_dirs.append(ws_skills)

    # 2. OpenClaw built-in skills (installed package)
    #    Find via `which openclaw` → resolve symlink → package root/skills/
    import shutil
    openclaw_bin = shutil.which("openclaw")
    if openclaw_bin:
        try:
            real_bin = os.path.realpath(openclaw_bin)
            # e.g. /opt/homebrew/lib/node_modules/openclaw/openclaw.mjs → package root
            pkg_root = os.path.dirname(real_bin)
            builtin_skills = os.path.join(pkg_root, "skills")
            if os.path.isdir(builtin_skills):
                scan_dirs.append(builtin_skills)
        except OSError:
            pass

    # 3. OpenClaw extensions (each extension may have a skills/ subdir)
    state_dir = os.environ.get("OPENCLAW_STATE_DIR", os.path.expanduser("~/.openclaw"))
    extensions_dir = os.path.join(state_dir, "extensions")
    if os.path.isdir(extensions_dir):
        try:
            for ext_name in sorted(os.listdir(extensions_dir)):
                ext_skills = os.path.join(extensions_dir, ext_name, "skills")
                if os.path.isdir(ext_skills):
                    scan_dirs.append(ext_skills)
        except OSError:
            pass

    # 4. OpenClaw bundled extension skills (dist/extensions/*/skills/)
    if openclaw_bin:
        try:
            real_bin = os.path.realpath(openclaw_bin)
            pkg_root = os.path.dirname(real_bin)
            dist_ext = os.path.join(pkg_root, "dist", "extensions")
            if os.path.isdir(dist_ext):
                for ext_name in sorted(os.listdir(dist_ext)):
                    ext_skills = os.path.join(dist_ext, ext_name, "skills")
                    if os.path.isdir(ext_skills):
                        scan_dirs.append(ext_skills)
        except OSError:
            pass

    # Scan each root for SKILL.md files
    for root_dir in scan_dirs:
        try:
            entries = sorted(os.listdir(root_dir))
        except OSError:
            continue

        for entry_name in entries:
            if entry_name.startswith("."):
                continue
            skill_dir = os.path.join(root_dir, entry_name)
            if not os.path.isdir(skill_dir):
                continue
            skill_md = os.path.join(skill_dir, "SKILL.md")
            if not os.path.isfile(skill_md):
                continue

            content = _read_file_safe(skill_md, max_chars=5000)
            if not content:
                continue

            fm = _parse_skill_frontmatter(content)
            name = fm.get("name", entry_name)
            description = fm.get("description", "")
            if not description:
                continue

            # Config-level enabled check (skills.entries.<name>.enabled: false)
            sc = skill_config.get(name, {})
            if isinstance(sc, dict) and sc.get("enabled") is False:
                continue

            # Runtime eligibility filter (OS, requires.bins, requires.env, etc.)
            if not _should_include_skill(fm, source=""):
                continue

            if name in seen_names:
                continue
            seen_names.add(name)

            skills.append({
                "name": name,
                "description": description,
                "filePath": _shorten_home(skill_md),
            })

    return skills


def _build_skills_section(workspace_dir: str) -> list[str]:
    """Build the Skills (mandatory) section by scanning installed skills.

    Applies the same prompt char limit as OpenClaw (DEFAULT_MAX_SKILLS_PROMPT_CHARS).
    If the full format exceeds the limit, falls back to compact format (no descriptions).
    """
    skills = _scan_skills(workspace_dir)
    if not skills:
        return []

    preamble = [
        "## Skills (mandatory)",
        "Before replying: scan <available_skills> <description> entries.",
        "- If exactly one skill clearly applies: read its SKILL.md at <location> with `read`, then follow it.",
        "- If multiple could apply: choose the most specific one, then read/follow it.",
        "- If none clearly apply: do not read any SKILL.md.",
        "Constraints: never read more than one skill up front; only read after selecting.",
        "- When a skill drives external API writes, assume rate limits: prefer fewer larger writes, avoid tight one-item loops, serialize bursts when possible, and respect 429/Retry-After.",
    ]

    def _format_full(skill_list: list[dict]) -> list[str]:
        """Full format with descriptions."""
        catalog = [
            "The following skills provide specialized instructions for specific tasks.",
            "Use the read tool to load a skill's file when the task matches its description.",
            "When a skill file references a relative path, resolve it against the skill directory (parent of SKILL.md / dirname of the path) and use that absolute path in tool commands.",
            "",
            "<available_skills>",
        ]
        esc = xml.sax.saxutils.escape
        for skill in skill_list:
            catalog.append("  <skill>")
            catalog.append(f"    <name>{esc(skill['name'])}</name>")
            catalog.append(f"    <description>{esc(skill['description'])}</description>")
            catalog.append(f"    <location>{esc(skill['filePath'])}</location>")
            catalog.append("  </skill>")
        catalog.append("</available_skills>")
        return catalog

    def _format_compact(skill_list: list[dict]) -> list[str]:
        """Compact format (no descriptions) as fallback."""
        catalog = [
            "The following skills provide specialized instructions for specific tasks.",
            "Use the read tool to load a skill's file when the task matches its name.",
            "When a skill file references a relative path, resolve it against the skill directory (parent of SKILL.md / dirname of the path) and use that absolute path in tool commands.",
            "",
            "<available_skills>",
        ]
        esc = xml.sax.saxutils.escape
        for skill in skill_list:
            catalog.append("  <skill>")
            catalog.append(f"    <name>{esc(skill['name'])}</name>")
            catalog.append(f"    <location>{esc(skill['filePath'])}</location>")
            catalog.append("  </skill>")
        catalog.append("</available_skills>")
        return catalog

    # Try full format first
    full_catalog = _format_full(skills)
    full_text = "\n".join(full_catalog)
    if len(full_text) <= MAX_SKILLS_PROMPT_CHARS:
        lines = preamble + full_catalog
        lines.append("")
        return lines

    # Fall back to compact format
    compact_catalog = _format_compact(skills)
    compact_text = "\n".join(compact_catalog)
    if len(compact_text) <= MAX_SKILLS_PROMPT_CHARS:
        lines = preamble + compact_catalog
        lines.append("")
        return lines

    # Truncate: binary search for max skills that fit in compact
    lo, hi = 0, len(skills)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if len("\n".join(_format_compact(skills[:mid]))) <= MAX_SKILLS_PROMPT_CHARS:
            lo = mid
        else:
            hi = mid - 1
    lines = preamble + _format_compact(skills[:lo])
    lines.append("")
    return lines


def _build_context_files_section(workspace_dir: str) -> list[str]:
    """Build the Project Context section by reading workspace bootstrap files.

    Reads AGENTS.md, SOUL.md, TOOLS.md, IDENTITY.md, USER.md, HEARTBEAT.md
    from the workspace directory, matching OpenClaw's loadWorkspaceBootstrapFiles().
    """
    files: list[tuple[str, str]] = []  # (path, content)

    for filename in CONTEXT_FILE_NAMES:
        filepath = os.path.join(workspace_dir, filename)
        content = _read_file_safe(filepath, max_chars=20000)
        if content is not None:
            files.append((filepath, content))

    # Also check MEMORY.md / memory.md
    for mem_name in ("MEMORY.md", "memory.md"):
        mem_path = os.path.join(workspace_dir, mem_name)
        content = _read_file_safe(mem_path, max_chars=20000)
        if content is not None:
            files.append((mem_path, content))
            break

    if not files:
        return []

    has_soul = any(os.path.basename(p).upper() == "SOUL.MD" for p, _ in files)

    lines = [
        "# Project Context",
        "",
        "The following project context files have been loaded:",
    ]
    if has_soul:
        lines.append(
            "If SOUL.md is present, embody its persona and tone. "
            "Avoid stiff, generic replies; follow its guidance unless "
            "higher-priority instructions override it."
        )
    lines.append("")

    for filepath, content in files:
        lines.append(f"## {filepath}")
        lines.append("")
        lines.append(content)
        lines.append("")

    return lines


# ---------------------------------------------------------------------------
# Main builder
# ---------------------------------------------------------------------------

def build_system_prompt(
    tool_names: list[str],
    cwd: str = "",
    model: str = "",
    thinking_level: str = "off",
    timestamp: str = "",
) -> str:
    """Reconstruct a system prompt from session metadata and workspace files.

    This is the fallback for sessions where cache-trace is not available.
    Reproduces all sections from OpenClaw's buildAgentSystemPrompt() by:
    1. Using fixed-text sections verbatim from source code
    2. Reading workspace context files (AGENTS.md, SOUL.md, etc.) from cwd
    3. Scanning installed skills from workspace and extensions directories

    Sections that remain unavailable (runtime-only):
    - Memory plugin injection (we include MEMORY.md as fallback)
    - Model Aliases (runtime config)
    - Reaction guidance (runtime config)
    - Reasoning tag hints (runtime config)
    - Sandbox configuration (runtime config)

    Args:
        tool_names: Tool names observed in the session (deduplicated).
        cwd: Working directory from session node.
        model: Model ID from session.
        thinking_level: Thinking level (off/auto/low/medium/high).
        timestamp: Session start timestamp (ISO-8601).

    Returns:
        Reconstructed system prompt string.
    """
    # Reset config cache for fresh scan
    global _openclaw_config_cache
    _openclaw_config_cache = None

    tool_lines = _build_tool_lines(tool_names)
    available = set(t.lower() for t in tool_names)
    has_gateway = "gateway" in available

    lines: list[str] = [
        "You are a personal assistant running inside OpenClaw.",
        "",
    ]

    # ── 1. Tooling ──────────────────────────────────────────────────────
    lines.extend([
        "## Tooling",
        "Tool availability (filtered by policy):",
        "Tool names are case-sensitive. Call tools exactly as listed.",
    ])
    if tool_lines:
        lines.extend(tool_lines)
    lines.extend([
        "TOOLS.md does not control tool availability; it is user guidance for how to use external tools.",
        "For long waits, avoid rapid poll loops: use exec with enough yieldMs or process(action=poll, timeout=<ms>).",
        "If a task is more complex or takes longer, spawn a sub-agent. Completion is push-based: it will auto-announce when done.",
        "Do not poll `subagents list` / `sessions_list` in a loop; only check status on-demand (for intervention, debugging, or when explicitly asked).",
        "",
    ])

    # ── 2. Tool Call Style ──────────────────────────────────────────────
    lines.extend([
        "## Tool Call Style",
        "Default: do not narrate routine, low-risk tool calls (just call the tool).",
        "Narrate only when it helps: multi-step work, complex/challenging problems, sensitive actions (e.g., deletions), or when the user explicitly asks.",
        "Keep narration brief and value-dense; avoid repeating obvious steps.",
        "Use plain human language for narration unless in a technical context.",
        "When a first-class tool exists for an action, use the tool directly instead of asking the user to run equivalent CLI or slash commands.",
        "When exec returns approval-pending, include the concrete /approve command from tool output (with allow-once|allow-always|deny) and do not ask for a different or rotated code.",
        "Treat allow-once as single-command only: if another elevated command needs approval, request a fresh /approve and do not claim prior approval covered it.",
        "When approvals are required, preserve and show the full command/script exactly as provided (including chained operators like &&, ||, |, ;, or multiline shells) so the user can approve what will actually run.",
        "",
    ])

    # ── 3. Safety ───────────────────────────────────────────────────────
    lines.extend([
        "## Safety",
        "You have no independent goals: do not pursue self-preservation, replication, resource acquisition, or power-seeking; avoid long-term plans beyond the user's request.",
        "Prioritize safety and human oversight over completion; if instructions conflict, pause and ask; comply with stop/pause/audit requests and never bypass safeguards. (Inspired by Anthropic's constitution.)",
        "Do not manipulate or persuade anyone to expand access or disable safeguards. Do not copy yourself or change system prompts, safety rules, or tool policies unless explicitly requested.",
        "",
    ])

    # ── 4. CLI Quick Reference ──────────────────────────────────────────
    lines.extend([
        "## OpenClaw CLI Quick Reference",
        "OpenClaw is controlled via subcommands. Do not invent commands.",
        "To manage the Gateway daemon service (start/stop/restart):",
        "- openclaw gateway status",
        "- openclaw gateway start",
        "- openclaw gateway stop",
        "- openclaw gateway restart",
        "If unsure, ask the user to run `openclaw help` (or `openclaw gateway --help`) and paste the output.",
        "",
    ])

    # ── 5. Skills section ───────────────────────────────────────────────
    if cwd:
        skills_section = _build_skills_section(cwd)
        if skills_section:
            lines.extend(skills_section)

    # ── 6. Memory section — OMITTED (plugin-injected at runtime) ────────

    # ── 7. Self-Update (conditional on gateway tool) ────────────────────
    if has_gateway:
        lines.extend([
            "## OpenClaw Self-Update",
            "Get Updates (self-update) is ONLY allowed when the user explicitly asks for it.",
            "Do not run config.apply or update.run unless the user explicitly requests an update or config change; if it's not explicit, ask first.",
            "Use config.schema.lookup with a specific dot path to inspect only the relevant config subtree before making config changes or answering config-field questions; avoid guessing field names/types.",
            "Actions: config.schema.lookup, config.get, config.apply (validate + write full config, then restart), config.patch (partial update, merges with existing), update.run (update deps or git, then restart).",
            "After restart, OpenClaw pings the last active session automatically.",
            "",
        ])

    # ── 8. Model Aliases — OMITTED (runtime config) ────────────────────

    # ── 9. Date hint ────────────────────────────────────────────────────
    lines.append("If you need the current date, time, or day of week, run session_status (\U0001f4ca session_status).")

    # ── 10. Workspace ───────────────────────────────────────────────────
    if cwd:
        lines.extend([
            "## Workspace",
            f"Your working directory is: {cwd}",
            "Treat this directory as the single global workspace for file operations unless explicitly instructed otherwise.",
            "",
        ])

    # ── 11. Documentation ───────────────────────────────────────────────
    lines.extend([
        "## Documentation",
        "Mirror: https://docs.openclaw.ai",
        "Source: https://github.com/openclaw/openclaw",
        "Community: https://discord.com/invite/clawd",
        "Find new skills: https://clawhub.ai",
        "For OpenClaw behavior, commands, config, or architecture: consult local docs first.",
        "When diagnosing issues, run `openclaw status` yourself when possible; only ask the user if you lack access (e.g., sandboxed).",
        "",
    ])

    # ── 12. Sandbox — OMITTED (runtime config) ─────────────────────────

    # ── 13. Authorized Senders — OMITTED (privacy) ─────────────────────

    # ── 14. Current Date & Time — OMITTED (runtime dynamic) ────────────

    # ── 15. Workspace Files note ────────────────────────────────────────
    lines.extend([
        "## Workspace Files (injected)",
        "These user-editable files are loaded by OpenClaw and included below in Project Context.",
        "",
    ])

    # ── 16. Reply Tags ──────────────────────────────────────────────────
    lines.extend([
        "## Reply Tags",
        "To request a native reply/quote on supported surfaces, include one tag in your reply:",
        "- Reply tags must be the very first token in the message (no leading text/newlines): [[reply_to_current]] your reply.",
        "- [[reply_to_current]] replies to the triggering message.",
        "- Prefer [[reply_to_current]]. Use [[reply_to:<id>]] only when an id was explicitly provided (e.g. by the user or a tool).",
        "Whitespace inside the tag is allowed (e.g. [[ reply_to_current ]] / [[ reply_to: 123 ]]).",
        "Tags are stripped before sending; support depends on the current channel config.",
        "",
    ])

    # ── 17. Messaging ───────────────────────────────────────────────────
    lines.extend([
        "## Messaging",
        "- Reply in current session \u2192 automatically routes to the source channel (Signal, Telegram, etc.)",
        "- Cross-session messaging \u2192 use sessions_send(sessionKey, message)",
        "- Sub-agent orchestration \u2192 use subagents(action=list|steer|kill)",
        "- Runtime-generated completion events may ask for a user update. Rewrite those in your normal assistant voice and send the update.",
        "- Never use exec/curl for provider messaging; OpenClaw handles all routing internally.",
        "",
    ])

    # ── 18. Voice — OMITTED (runtime config) ───────────────────────────

    # ── 19. Project Context (workspace files) ───────────────────────────
    if cwd:
        context_section = _build_context_files_section(cwd)
        if context_section:
            lines.extend(context_section)

    # ── 20. Silent Replies ──────────────────────────────────────────────
    lines.extend([
        "## Silent Replies",
        "When you have nothing to say, respond with ONLY: NO_REPLY",
        "",
        "\u26a0\ufe0f Rules:",
        "- It must be your ENTIRE message \u2014 nothing else",
        '- Never append it to an actual response (never include "NO_REPLY" in real replies)',
        "- Never wrap it in markdown or code blocks",
        "",
        '\u274c Wrong: "Here\'s help... NO_REPLY"',
        '\u274c Wrong: "NO_REPLY"',
        "\u2705 Right: NO_REPLY",
        "",
    ])

    # ── 21. Heartbeats — OMITTED (runtime config) ──────────────────────

    # ── 22. Runtime ─────────────────────────────────────────────────────
    runtime_parts: list[str] = []
    if model:
        runtime_parts.append(f"model={model}")
    reasoning_level = thinking_level if thinking_level != "off" else "off"
    runtime_parts.append(f"thinking={reasoning_level}")
    if runtime_parts:
        lines.extend([
            "## Runtime",
            f"Runtime: {' | '.join(runtime_parts)}",
            f"Reasoning: {reasoning_level} (hidden unless on/stream). Toggle /reasoning; /status shows Reasoning when enabled.",
        ])

    return "\n".join(lines)


def _normalize_provider(model: str) -> str:
    """Map model name to standard provider name."""
    model_lower = model.lower()
    if "claude" in model_lower:
        return "anthropic"
    if "gpt" in model_lower or "o1" in model_lower or "o3" in model_lower:
        return "openai"
    if "gemini" in model_lower:
        return "google"
    if "qwen" in model_lower:
        return "alibaba"
    if "deepseek" in model_lower:
        return "deepseek"
    return "unknown"


def extract_session_metadata(nodes: list[dict]) -> dict:
    """Extract metadata from JSONL nodes for trajectory metadata.

    Returns dict with keys: cwd, model, provider, thinking_level, timestamp, tool_names.
    """
    meta: dict = {
        "cwd": "",
        "model": "",
        "provider": "",
        "thinking_level": "off",
        "timestamp": "",
        "tool_names": [],
    }

    for node in nodes:
        node_type = node.get("type")

        if node_type == "session":
            meta["cwd"] = node.get("cwd", "")
            meta["timestamp"] = node.get("timestamp", "")

        elif node_type == "model_change":
            meta["model"] = node.get("modelId", "")

        elif node_type == "thinking_level_change":
            meta["thinking_level"] = node.get("thinkingLevel", "off")

        elif node_type == "message":
            msg = node.get("message", {})
            if msg.get("role") == "assistant":
                for block in msg.get("content", []):
                    if isinstance(block, dict) and block.get("type") == "toolCall":
                        name = block.get("name", "")
                        if name:
                            meta["tool_names"].append(name)

            if not meta["model"] and msg.get("model"):
                meta["model"] = msg["model"]

    # Deduplicate tool names preserving order
    seen = set()
    unique = []
    for name in meta["tool_names"]:
        if name not in seen:
            seen.add(name)
            unique.append(name)
    meta["tool_names"] = unique

    # Derive provider from model name
    if meta["model"]:
        meta["provider"] = _normalize_provider(meta["model"])

    return meta
