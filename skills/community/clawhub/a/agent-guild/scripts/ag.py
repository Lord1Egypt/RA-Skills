#!/usr/bin/env python3
"""ag — Agent Guild CLI (zero-dependency, stdlib only).

Bootstraps and maintains the shared cross-agent directory at ~/.agent-guild/.
Writes are atomic + audited so multiple agents can share state without
corrupting it. Reads stay plain file reads (zero cost).

Runs on Windows / macOS / Linux (and POSIX-ish mobile shells) with Python 3.8+.
No third-party packages.

Commands:
  init [agent]            Bootstrap ~/.agent-guild/ (idempotent, safe to re-run)
  find-root [agent]       Locate your user-extensible skills dir — instant,
                          never asks the user, READONLY fallback if not found
  link-root [agent]       Consolidate to ONE directory link <skills_root> ->
                          ~/.agent-guild/skills (replaces per-skill links,
                          DRY-RUN report by default)
  link-root --apply       Execute the consolidation: foreign links move into
                          the guild, guild links go to trash, real skills
                          abort with a pointer to `adopt --apply` first
  adopt [agent]           Scan agent home for adoptable assets (DRY-RUN report)
  adopt --apply [agent]   Move assets into the guild + link back
  bootstrap [agent]      Print identity/routine/rules only (no task context)
                          --no-maintenance skips grooming and upgrade checks
  recall <kw> [...]       Search shared memory (identity/rules/projects/memory/
                          handoff/logs/learnings) — AND by default; --all = OR,
                          --limit N caps output (default 20); exit 1 if no hit
  finish [agent]          Close a session: summary (stdin) -> today's daily log,
                          last-seen refresh, inbox report
                          opt: --archive-inbox  mv this agent's inbox -> archive/
  doctor                  Health check: broken links, stale paths, version drift
  platform                Identify THIS device: os / arch / host-id / link support
  tool <name>             Resolve a tool's executable for this platform (prints
                          the path; exit 3 + install hint when unavailable)
  tools                   List declared tools x availability on this device
  port                    Portability audit for multi-device guilds (DRY-RUN)
  port --apply            Move host-scoped state under hosts/<host-id>/,
                          fold registry paths per device, declare tool platforms
  upgrade                 Check 3 platforms for a newer skill version (dry-run)
  upgrade --apply         Download + install the latest version, keep user data
                          (bootstrap also self-checks once per UPGRADE.md
                          interval; mode=apply there auto-installs)
  status                  List registered agents + last_seen
  register <agent> <home> <tier> [skills_root] [caps...]
  last-seen <agent>       Refresh an agent's presence
  send <dst> <topic>      Write an inbox message from stdin
  log <agent> <title>     Append a daily log entry from stdin
  task <action>           Create/list/resume/checkpoint/attach/release/close/reopen
  history <action>        History status/plan and explicitly confirmed maintenance
  inbox [agent]           Explicitly list this agent's message filenames
  migrate [--dry-run]     Preview legacy message locations (never auto-migrates)
  focus                   Retired; use task checkpoints
  learn <agent> <kind> "<summary>"   Learning-ledger entry (details from stdin)
                          kind: learning | error | featreq
                          opts: --area A --priority P --category C --pattern-key K
  review                  Ledger stats: pending items + promotion candidates
  resolve <ID> [note ...] Mark a ledger entry resolved (+ resolution note)
  groom [--dry-run]       Data hygiene: archive expired logs/focus/ledgers,
                          rotate audit trail, report degradation (never deletes)
  audit [n]               Show last n audit lines (default 20)
  prune [days]            List agents idle > N days (default 30) — never deletes

Env:
  AGENT_GUILD_DIR   override central dir (default ~/.agent-guild)
  AG_AGENT          your agent name (used by `send`, and as default for
                    init/adopt when no agent argument is given)
  AG_HOST_ID        override this device's id (default <os>-<arch>-<hostname>)
  AG_PLATFORM       override platform detection as <os>-<arch> (e.g. linux-x64)

Exit codes: 0 ok, 1 error, 2 usage.
"""

from __future__ import annotations

import io
import json
import os
import platform
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from contextlib import contextmanager, nullcontext
from datetime import datetime, timezone
from fnmatch import fnmatch
from pathlib import Path
from typing import Tuple

CENTRAL = Path(os.environ.get("AGENT_GUILD_DIR", "~/.agent-guild")).expanduser()
REGISTRY = CENTRAL / "registry.json"
AUDIT = CENTRAL / "log" / "audit.jsonl"
DAILY = CENTRAL / "log" / "daily"
INBOX = CENTRAL / "messages" / "inbox"
FOCUS = CENTRAL / "handoff" / "shared-state" / "current-focus.md"
VERSION = CENTRAL / "VERSION"
LEARNINGS = CENTRAL / "learnings"
HOSTS = CENTRAL / "hosts"
TOOLS = CENTRAL / "tools"

PROTOCOL_VERSION = "4.0"

# ------------------------------------------------------------ portability ---

# A guild directory is frequently placed on a file-level carrier shared by
# several devices (any folder-sync tool, cloud drive, or VCS checkout): a
# laptop, a desktop running another OS, a phone. Protocol 3.3 therefore gives
# every stored fact a SCOPE, so a second device can tell "not mine" apart from
# "missing":
#
#   shared    true on every device       -> stays exactly where it always was
#   platform  true for one OS+arch pair  -> declared per platform tag
#   host      true for this device only  -> namespaced under hosts/<host-id>/
#
# Rule of thumb for any agent: "would this still be true on another device?"
# Yes -> shared. Only on the same OS -> platform. Only here -> host.
#
# Link-direction invariant: the guild OWNS its payloads. Links pointing from
# the guild to an external path break on every other device, so they are a
# violation; links pointing INTO the guild (runtime skills dirs, project
# checkouts) are the normal, portable direction.

TOOL_MANIFEST = "tool.json"
HOST_NOTES = "host-notes.md"

# Root-level protocol docs seeded into the central dir by `ag init`.
PROTOCOL_DOCS = ("ONBOARDING.md", "CONVENTIONS.md", "SPEC.md", "PORTABILITY.md")

# Where those docs may sit inside a skill package. Registries differ on the
# sanctioned layout: some take `references/`, others only allow references/ scripts/
# templates/. Both are accepted so one package works everywhere.
DOC_DIRS = ("references", "docs")  # docs = legacy layouts pre-3.10

# Canonical OS tags. Anything unrecognised degrades to a sanitized
# platform.system() value instead of being guessed into the wrong family.
OS_TAGS = ("macos", "windows", "linux", "android", "ios")

_ARCH_ALIASES = {
    "x86_64": "x64", "amd64": "x64", "x64": "x64",
    "aarch64": "arm64", "arm64": "arm64", "armv8l": "arm64",
    "i386": "x86", "i686": "x86", "x86": "x86",
    "armv7l": "arm",
}

# Host-scoped state files: written under hosts/<host-id>/, with the pre-3.3
# root location kept as a read-only fallback until `ag port --apply` moves it.
_LEGACY_STATE = {"VERSION": "VERSION", "groom.json": ".groom.json"}

# Registry fields whose value is a property of the DEVICE, not of the agent.
HOST_SCOPED_FIELDS = ("home", "skills_root", "install_tier",
                      "install_verified", "last_seen")


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")


def _platform_override() -> Tuple[str, str]:
    """`AG_PLATFORM=<os>-<arch>` overrides detection.

    Two honest uses: a runtime whose probes are wrong (exotic shell, emulated
    arch), and dry-running another device's resolution before carrying the
    guild there.
    """
    raw = _slug(os.environ.get("AG_PLATFORM", ""))
    if not raw:
        return ("", "")
    parts = raw.split("-")
    return (parts[0], "-".join(parts[1:]) if len(parts) > 1 else "")


def detect_os() -> str:
    """Canonical OS tag for this device — probes only, never guesses."""
    forced = _platform_override()[0]
    if forced:
        return forced
    if os.name == "nt" or sys.platform.startswith("win"):
        return "windows"
    if sys.platform == "ios" or platform.system() == "iOS":
        return "ios"
    if sys.platform == "android" or platform.system() == "Android":
        return "android"
    if sys.platform == "darwin":
        if (platform.machine().startswith(("iPhone", "iPad", "iPod"))
                or Path("/var/mobile").is_dir()):
            return "ios"
        return "macos"
    if sys.platform.startswith("linux"):
        # Termux / Android userland looks like Linux to sys.platform
        if ("com.termux" in os.environ.get("PREFIX", "")
                or os.environ.get("ANDROID_ROOT")
                or Path("/system/build.prop").is_file()):
            return "android"
        return "linux"
    return _slug(platform.system()) or "unknown"


def detect_arch() -> str:
    forced = _platform_override()[1]
    if forced:
        return forced
    m = platform.machine().lower()
    return _ARCH_ALIASES.get(m, _slug(m) or "unknown")


def platform_tag() -> str:
    """`<os>-<arch>` — the unit of "the same prebuilt binary runs here"."""
    return f"{detect_os()}-{detect_arch()}"


def host_id() -> str:
    """Stable id of THIS device: `<os>-<arch>-<hostname>`.

    Computed at runtime and never read back from a stored file — a synced copy
    of the guild landing on a second device must not inherit the first
    device's identity. `AG_HOST_ID` overrides it (hostname changed, or two
    devices deliberately sharing one id).
    """
    override = os.environ.get("AG_HOST_ID", "").strip()
    if override:
        return _slug(override)
    node = _slug(platform.node().split(".")[0]) or "host"
    return f"{platform_tag()}-{node}"


def host_dir(create: bool = False) -> Path:
    d = HOSTS / host_id()
    if create:
        d.mkdir(parents=True, exist_ok=True)
    return d


def known_hosts() -> list:
    """Device ids that have ever written state into this guild."""
    if not HOSTS.is_dir():
        return []
    try:
        return sorted(p.name for p in HOSTS.iterdir() if p.is_dir())
    except OSError:
        return []


def host_state(name: str) -> Path:
    """Read path of a host-scoped state file: new location first, pre-3.3 root
    location as fallback so an un-migrated guild keeps working."""
    new = host_dir() / name
    if new.exists():
        return new
    legacy = CENTRAL / _LEGACY_STATE.get(name, name)
    return legacy if legacy.exists() else new


def link_capability() -> str:
    """What kind of link this device can actually create — probed, not
    assumed (Windows without developer mode, some Android/iOS shells and
    exFAT/FAT volumes cannot symlink at all)."""
    probe = None
    try:
        probe = Path(tempfile.mkdtemp(prefix="ag-probe-"))
        target = probe / "t"
        target.mkdir()
        ok, how = make_link(probe / "l", target)
        return how if ok else "copy-only"
    except OSError:
        return "copy-only"
    finally:
        if probe:
            shutil.rmtree(probe, ignore_errors=True)


def platform_facts() -> dict:
    return {
        "host_id": host_id(),
        "platform": platform_tag(),
        "os": detect_os(),
        "arch": detect_arch(),
        "python": sys.executable or "python3",
        "python_version": platform.python_version(),
        "links": link_capability(),
        "central": str(CENTRAL),
        "known_hosts": known_hosts(),
    }


# Learning ledger: kind -> (file, ID prefix). Protocol 3.1+.
LEDGERS = {
    "learning": ("learnings/LEARNINGS.md", "LRN"),
    "error": ("learnings/ERRORS.md", "ERR"),
    "featreq": ("learnings/FEATURE_REQUESTS.md", "FEAT"),
}
LEDGER_ALIASES = {
    "learn": "learning", "insight": "learning",
    "err": "error", "bug": "error",
    "feat": "featreq", "feature": "featreq", "fr": "featreq",
}

# Remote version sources, queried WITHOUT any auth (any ordinary user can
# self-check). Order is the reporting priority; the newest wins.
VERSION_SOURCES = [
    ("skillhub", "https://api.skillhub.cn/api/v1/search?q=agent-guild"),
    ("github", "https://github.com/dqsjqian/agent-guild/releases/latest"),
    ("clawhub", "https://clawhub.ai/api/v1/skills/agent-guild/versions"),
]

# ------------------------------------------------------------------ groom ---

# Data-hygiene defaults (protocol 3.2+). User-editable in RETENTION.md;
# re-read on every run. Core invariant: groom NEVER hard-deletes — expired
# data moves to archive dirs or the recoverable trash.
RETENTION = CENTRAL / "RETENTION.md"
GROOM_STATE = CENTRAL / ".groom.json"  # pre-3.3 location, read-only fallback


def groom_state_read() -> Path:
    """Groom bookkeeping is per device: one machine's grooming says nothing
    about another's."""
    return host_state("groom.json")


def groom_state_write() -> Path:
    return host_dir(create=True) / "groom.json"

RETENTION_DEFAULTS = {
    "daily_log_days": 90,
    "focus_days": 30,
    "focus_blocks": 20,
    "inbox_archive_days": 60,
    "audit_max_lines": 2000,
    "audit_keep_lines": 1000,
    "ledger_resolved_days": 120,
    "trash_days": 30,
    "groom_interval_hours": 24,
}

# Download source for upgrades — our own GitHub release zip (most stable).
GITHUB_RELEASE_ZIP = (
    "https://github.com/dqsjqian/agent-guild/releases/download/"
    "v{ver}/agent-guild-v{ver}.zip"
)

# ---------------------------------------------------------------- skeleton ---

SKELETON = [
    "identity", "rules", "toolchain", "projects",
    "handoff/active", "handoff/archive", "messages/inbox", "messages/archive",
    "log/daily", "log/decisions", "log/archive", "learnings", "learnings/archive",
    "skills", "skills_data", "mcp", "plugins", "tools", "memory", "connectors",
    "hosts",
]

PLACEHOLDERS = {
    "identity/profile.md": "# Who the user is\n\n_Fill this in — every joined agent reads it._\n",
    "identity/ROUTINE.md": "# Daily routine\n\n_Schedule, habits, commute, working hours._\n",
    "rules/universal.md": "# Universal rules (highest priority)\n\n_Mandatory commandments every agent obeys._\n",
    "projects/active.md": "# Active projects\n\n_What the user is working on right now._\n",
    "memory/README.md": (
        "# memory/\n\n"
        "Cross-agent memory. Agent-private memory files adopted from each\n"
        "runtime live under `memory/<agent>/`; facts worth sharing across all\n"
        "agents go in `memory/shared/`.\n"
    ),
    "learnings/LEARNINGS.md": (
        "# Learnings\n\n"
        "Cross-agent ledger: corrections, knowledge gaps, best practices.\n"
        "Entries are append-only; only Status/Resolution may be edited later.\n"
        "Never log secrets — redacted summaries only.\n\n"
        "**Categories**: correction | insight | knowledge_gap | best_practice\n"
        "**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill\n\n"
        "---\n"
    ),
    "learnings/ERRORS.md": (
        "# Errors\n\n"
        "Cross-agent ledger: command failures, integration errors, unexpected\n"
        "behavior. Redacted excerpts only — no secrets, no raw transcripts.\n\n"
        "---\n"
    ),
    "learnings/FEATURE_REQUESTS.md": (
        "# Feature Requests\n\n"
        "Cross-agent ledger: capabilities the user wanted but nothing provides.\n\n"
        "---\n"
    ),
    "RETENTION.md": (
        "# Data Retention Policy\n\n"
        "> `ag groom` (auto-run after bootstrap, at most once per interval)\n"
        "> reads this file. Edit freely — values apply on the next run.\n"
        "> Nothing is ever hard-deleted: expired data moves to archive dirs\n"
        "> or the recoverable trash (`~/.agent-guild/.trash/`).\n\n"
        "```\n"
        "daily_log_days = 90        # log/daily/ files older -> log/archive/\n"
        "focus_days = 30            # current-focus blocks older -> shared-state/archive/\n"
        "focus_blocks = 20          # ...and beyond this many live blocks\n"
        "inbox_archive_days = 60    # processed messages: review candidates\n"
        "audit_max_lines = 2000     # audit.jsonl beyond this rotates\n"
        "audit_keep_lines = 1000    # newest lines kept after rotation\n"
        "ledger_resolved_days = 120 # resolved ledger entries older -> learnings/archive/\n"
        "trash_days = 30            # .trash/ items older -> reported for manual emptying\n"
        "groom_interval_hours = 24  # auto-groom cooldown\n"
        "history_max_bytes = 1073741824      # one shared 1 GiB history budget\n"
        "history_target_bytes = 838860800    # 800 MiB low watermark\n"
        "history_full_days = 30              # review old full archives\n"
        "history_retention_days = 180        # retirement candidates, not auto-delete\n"
        "history_max_tasks = 2000            # review archive count\n"
        "history_check_interval_hours = 24   # check on use, no daemon\n"
        "```\n"
    ),
    "UPGRADE.md": (
        "# Upgrade Policy\n\n"
        "> `ag bootstrap` self-checks the published version once per interval\n"
        "> (3.9.0+). Edit freely — applies on the next bootstrap. The check\n"
        "> only reaches the public version endpoints; `apply` downloads from\n"
        "> this project's GitHub releases and never touches user data.\n\n"
        "```\n"
        "mode = check              # check | apply | off\n"
        "                          #   check: report an available update, do nothing\n"
        "                          #   apply: download and install it automatically\n"
        "                          #   off:   no self-check on bootstrap\n"
        "interval_hours = 24       # self-check cooldown\n"
        "```\n"
    ),
}

# --------------------------------------------------------------- adoption ---

# Where each asset class lands inside the guild.
# Note: `connectors` (credential store) is deliberately NOT adoptable — it is a
# manually-placed directory. Adopt must never auto-move credentials into a
# directory the user backs up.
ADOPT_DESTS = {
    "skills": "skills",
    "skills_data": "skills_data",
    "mcp": "mcp",
    "tools": "tools",
    "memory": "memory",
}

# Never adopt: rebuildable caches, credential stores, VCS/OS noise,
# runtime-internal bookkeeping, and the protocol's own skill.
EXCLUDE_NAMES = {
    ".venv", "venv", "node_modules", "__pycache__", ".git", ".DS_Store",
    ".env", "secrets", "cache", ".cache", "tmp", ".tmp", "dist", "build",
    "browsers",  # Playwright / Puppeteer browser binaries — rebuildable
    "agent-guild", "agent-commons",
    # runtime-internal metadata: owned by the host, not portable skills
    "agent-created-skills.json", "_bm_skillid_migration.json",
    "settings.json", "config.json", "mcp.json", ".skill-lock.json",
}

# Rebuildable binaries and runtime artifacts: adopt nothing with these suffixes.
EXCLUDE_SUFFIXES = (".app", ".pid", ".log", ".pyc", ".tmp")

# Platform-managed / vendor-wired packages: moving them breaks the host.
EXCLUDE_SUBSTRINGS = ("__skillhub", "connector-", "-connector", "marketplace",
                      "_migration", "-lock")

# Markers that identify a skill as host-wired rather than portable: its
# capability comes from a connector / MCP server the runtime manages, so moving
# the files detaches it from that wiring. Detected by content, not by a
# hardcoded vendor list — that keeps this portable across ecosystems.
HOST_WIRED_MARKERS = (
    "connector to access",
    "via connector",
    "connector config",
    "mcp connector",
    "official mcp",
    "(connector)",
)

# Users can add their own glob-ish patterns, one per line, in
# ~/.agent-guild/.adoptignore (blank lines and #comments ignored).
ADOPTIGNORE = ".adoptignore"

# Candidate locations per agent home, by asset class.
# `connectors` is intentionally absent: credentials are manually placed, never
# auto-adopted (see ADOPT_DESTS note above).
CANDIDATE_LAYOUT = {
    "skills": ["skills"],
    "skills_data": ["skills_data", "skill_data"],
    "mcp": ["mcp", "mcp_servers"],
    "tools": ["tools", "bin"],
    "memory": ["memory", "memories"],
}

# Agent-private memory files worth adopting (relative to agent home).
MEMORY_FILES = ["MEMORY.md", "SOUL.md", "USER.md", "IDENTITY.md"]


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def audit(action: str, detail: dict) -> None:
    line = json.dumps({"ts": now_iso(), "action": action, **detail}, ensure_ascii=False)
    import ag_history
    with _append_lock(AUDIT):
        with ag_history.budget_lock(sys.modules[__name__]):
            ag_history.ensure_capacity(sys.modules[__name__], len((line + "\n").encode("utf-8")))
            with AUDIT.open("a", encoding="utf-8") as f:
                f.write(line + "\n")


def atomic_write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".ag-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def _session_path(path, write: bool = False) -> Path:
    """Resolve a guild state path for the session protocol. Relative paths
    land under the central dir (session data is guild-owned); `write`
    pre-creates the parent directories."""
    p = Path(path)
    if not p.is_absolute():
        p = CENTRAL / p
    if write:
        p.parent.mkdir(parents=True, exist_ok=True)
    return p


@contextmanager
def _append_lock(path: Path):
    """Lock a sidecar file, not the inode that os.replace swaps out from
    under us — keeps concurrent appends from losing each other."""
    lock = path.with_name(f".{path.name}.ag-lock")
    _session_path(lock, write=True)
    with lock.open("a+b") as stream:
        if os.name == "nt":
            import msvcrt
            stream.seek(0, os.SEEK_END)
            if not stream.tell():
                stream.write(b"0")
                stream.flush()
            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            if os.name == "nt":
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def atomic_append(path: Path, content: str) -> None:
    import ag_history
    # Existing legacy writers may already hold another file's lock. Always
    # acquire their destination lock before the shared budget lock; never
    # call an API that acquires a file lock while holding the budget lock.
    with _append_lock(path):
        with ag_history.budget_lock(sys.modules[__name__]):
            old_bytes = path.stat().st_size if path.exists() else 0
            ag_history.ensure_capacity(sys.modules[__name__], old_bytes + len(content.encode("utf-8")) + 2)
            _append_unlocked(path, content)


def _append_unlocked(path: Path, content: str) -> None:
    """Append while the caller holds `_append_lock(path)`. This lets ledger
    ID allocation and the resulting write share one critical section."""
    body = path.read_text(encoding="utf-8") if path.exists() else ""
    existing = body.rstrip("\n")
    fresh = content.rstrip("\n")
    # A brand-new target must not start with a stray blank line.
    body = (existing + "\n" + fresh if existing else fresh) + "\n"
    _atomic_write_text(path, body)


def load_registry() -> dict:
    if not REGISTRY.exists():
        return {
            "protocol_version": PROTOCOL_VERSION,
            "central_dir": "~/.agent-guild/",
            "agents": {},
        }
    # Windows PowerShell 5.1's UTF8 writer adds a BOM to legacy registries.
    return json.loads(REGISTRY.read_text(encoding="utf-8-sig"))


def save_registry(data: dict, agent: str, action: str) -> None:
    atomic_write_json(REGISTRY, data)
    audit(action, {"agent": agent, "file": "registry.json"})


# -- registry, per device (protocol 3.3+) ------------------------------------
# An agent entry mixes two scopes: what the agent IS (name, capabilities, the
# protocol version it joined under) is shared, while where it lives (home,
# skills_root, install tier, last_seen) is a fact about one device. The device
# facts live in `agents.<name>.hosts.<host-id>`; the flat fields are kept as a
# compat mirror so a pre-3.3 client on the same machine still reads them.

def host_block(entry: dict, hid: str = "") -> dict:
    hosts = entry.get("hosts")
    if isinstance(hosts, dict):
        block = hosts.get(hid or host_id())
        if isinstance(block, dict):
            return block
    return {}


def entry_view(entry: dict) -> dict:
    """Effective agent fields for THIS device.

    A pre-3.3 entry has flat fields only; those describe the machine they were
    written on, so treating them as this device's data is the correct reading
    until `ag port --apply` folds them into a host block.
    """
    view = {k: v for k, v in entry.items() if k != "hosts"}
    view.update({k: v for k, v in host_block(entry).items() if v})
    return view


def registered_here(entry: dict) -> bool:
    """False only when the entry has host blocks and none of them is ours —
    i.e. the agent is installed on other devices, not on this one."""
    hosts = entry.get("hosts")
    if not isinstance(hosts, dict) or not hosts:
        return True
    return host_id() in hosts


def other_hosts(entry: dict) -> list:
    hosts = entry.get("hosts")
    if not isinstance(hosts, dict):
        return []
    return sorted(h for h in hosts if h != host_id())


def fold_entry_to_host(entry: dict, hid: str) -> bool:
    """Move an entry's flat device fields into hosts[hid]. Returns True when
    something was folded. Never drops the flat fields — they stay as the
    compat mirror."""
    if host_block(entry, hid):
        return False
    block = {k: entry[k] for k in HOST_SCOPED_FIELDS
             if entry.get(k) not in (None, "")}
    if not block:
        return False
    entry.setdefault("hosts", {})[hid] = block
    entry["mirror_host"] = hid
    return True


def read_stdin() -> str:
    return sys.stdin.read().strip()


def default_agent(args: list) -> str:
    """Agent name from argv, else $AG_AGENT, else 'unknown'."""
    for a in args:
        if not a.startswith("-"):
            return a
    return os.environ.get("AG_AGENT") or "unknown"


# Candidate user-extensible skills roots, checked in order. Full-disk probing
# is deliberately avoided — it is slow (30s+) and rarely needed.
def _candidate_roots(name: str) -> list:
    home = Path.home()
    roots = [
        home / f".{name}" / "skills",
        home / f".{name}",
        home / ".config" / name / "skills",
        home / ".config" / name,
    ]
    if sys.platform == "darwin":
        roots += [
            home / "Library" / "Application Support" / name / "skills",
            home / "Library" / "Application Support" / name,
        ]
    elif os.name == "nt":
        appdata = os.environ.get("APPDATA")
        if appdata:
            roots += [Path(appdata) / name / "skills", Path(appdata) / name]
    return roots


def cmd_find_root(args: list) -> int:
    """Locate a user-extensible skills dir by checking well-known paths.

    Order: registry entry → common paths. Never full-disk probes. If nothing
    is found, print a READONLY verdict and exit 0 — joining read-only is the
    correct fallback, not a failure. An agent's own install path is something
    it can look up; the user usually cannot.
    """
    agent = default_agent(args)
    entry = load_registry().get("agents", {}).get(agent, {})

    sr = entry.get("skills_root")
    if sr and sr != "platform-managed":
        p = Path(sr).expanduser()
        if p.is_dir():
            print(f"SKILLS_ROOT={p}\nTIER=dir-symlink-if-supported  (from registry)")
            print(f"NEXT=ag link-root {agent} --apply  (one link for ALL guild skills)")
            return 0

    for p in _candidate_roots(agent):
        if p.is_dir():
            print(f"SKILLS_ROOT={p}\nTIER=dir-symlink-if-supported")
            print(f"NEXT=ag link-root {agent} --apply  (one link for ALL guild skills)")
            return 0

    print("SKILLS_ROOT=not-found")
    print("TIER=readonly")
    print("VERDICT=no user-extensible skills dir found — skip installation and "
          "join read-only (read central files each session).")
    return 0


# ------------------------------------------------------------- link-root ---

def _locate_linkable_root(agent: str) -> Path | None:
    """The agent's skills dir to consolidate: registry skills_root first,
    then candidate roots. Only ever targets a DEDICATED skills directory —
    an agent home itself (~/.<me>, ~/.config/<me>, ...) holds more than
    skills and must never be replaced by a link."""
    entry = load_registry().get("agents", {}).get(agent, {})
    sr = entry.get("skills_root")
    if sr and sr != "platform-managed":
        return Path(sr).expanduser()
    roots = _candidate_roots(agent)
    agent_dirs = [p for p in roots if p.name != "skills" and p.is_dir()]
    if not agent_dirs:
        return None
    # existing dedicated skills dir wins; else a creatable <agent-dir>/skills
    for p in roots:
        if p.name == "skills" and p.is_dir():
            return p
    for p in roots:
        if p.name == "skills" and p.parent in agent_dirs:
            return p
    return None


def cmd_link_root(args: list) -> int:
    """Point the agent's whole skills dir at the guild with ONE directory link.

    Replaces the per-skill link pattern (one symlink per guild skill) with a
    single link <skills_root> -> ~/.agent-guild/skills, so every new guild
    skill is instantly visible to the runtime — zero per-skill maintenance.

    Safety model (never loses data):
      - links matching guild names/targets -> removed (dir link replaces them)
      - links without a guild counterpart  -> recreated with the same target
      - links conflicting with guild names -> abort: resolve the conflict first
      - real adoptable skills         -> abort: run `ag adopt --apply` first
      - host-wired / platform items   -> abort: keep the per-skill tier
    """
    apply_ = "--apply" in args
    rest = [a for a in args if not a.startswith("-")]
    agent = default_agent(rest)
    if not CENTRAL.is_dir():
        print(f"{CENTRAL} missing — run `ag init` first", file=sys.stderr)
        return 1
    guild = CENTRAL / "skills"
    if not guild.is_dir():
        print(f"{guild} missing — run `ag init` first", file=sys.stderr)
        return 1

    root = _locate_linkable_root(agent)
    if root is None:
        print("SKILLS_ROOT=not-found — nothing to link; join read-only instead")
        return 1

    # Case 0: already a link to the guild (symlink OR Windows junction)
    if is_link(root):
        try:
            consolidated = root.resolve() == guild.resolve()
        except OSError:
            consolidated = False
        if consolidated:
            print(f"already consolidated: {root} -> {guild}")
            print(f"register (if not yet): ag register {agent} <home> dir-symlink {root}")
            return 0
        print(f"{root} is already a link elsewhere ({link_target(root)}) — "
              "refusing to hijack it")
        return 1

    # Case 1: no skills dir yet — just create the directory link
    if not root.exists():
        if not root.parent.is_dir():
            print(f"cannot create {root}: parent {root.parent} does not exist "
                  "(never fabricate an agent home)")
            return 1
        if not apply_:
            print(f"DRY-RUN — would link {root} -> {guild}")
            print("re-run with --apply to execute")
            return 0
        ok, how = make_link(root, guild)
        if not ok or not (root / "agent-guild" / "SKILL.md").is_file():
            print(f"FAILED: {how}")
            return 1
        audit("link-root", {"agent": agent, "root": str(root), "mode": how})
        print(f"linked {root} -> {guild} ({how})")
        print("next: trigger-test the skill in your runtime, then "
              f"`ag register {agent} <home> dir-symlink {root}`")
        return 0

    # Case 2: existing real directory — classify every child
    trash_items, move_items, adopt_items, block_items = [], [], [], []
    link_conflicts, link_targets = [], {}
    try:
        children = sorted(root.iterdir())
    except OSError as e:
        print(f"cannot read {root}: {e}", file=sys.stderr)
        return 1
    for child in children:
        if is_link(child):
            # The directory link replaces a child only when the SAME name
            # resolves to the SAME target. A differently named guild alias
            # still needs preserving; an unrelated same-name item conflicts.
            dest = guild / child.name
            try:
                try:
                    target = child.resolve(strict=True)
                except FileNotFoundError:
                    # Preserve dangling links too, but do not accept loops
                    # (non-strict resolve ignores ELOOP on recent Python).
                    target = child.resolve()
                if dest.exists() or is_link(dest):
                    (trash_items if target == dest.resolve()
                     else link_conflicts).append(child)
                else:
                    move_items.append(child)
                    link_targets[child] = target
            except (OSError, RuntimeError):
                link_conflicts.append(child)
        elif child.name == ".DS_Store":
            trash_items.append(child)
        elif (child.is_dir() and (child / "SKILL.md").is_file()
                and not _is_host_wired_skill(child)
                and not _is_excluded(child.name, "skills")):
            adopt_items.append(child)
        else:
            block_items.append(child)

    print(f"{'CONSOLIDATING' if apply_ else 'DRY-RUN'} — "
          f"one directory link {root} -> {guild}")
    print(f"{'kind':<28} item")
    print("-" * 78)
    for c in trash_items:
        print(f"{'trash (guild already has it)':<28} {c.name}")
    for c in move_items:
        print(f"{'move into guild':<28} {c.name} -> {link_target(c)}")
    for c in adopt_items:
        print(f"{'ADOPT FIRST (blocks)':<28} {c.name}")
    for c in block_items:
        print(f"{'CANNOT MOVE (blocks)':<28} {c.name}")
    for c in link_conflicts:
        print(f"{'LINK CONFLICT (blocks)':<28} {c.name} -> {link_target(c)}")
    print("-" * 78)

    if link_conflicts:
        print("Resolve conflicting or unresolvable links before consolidating; "
              "no items were changed.")
        return 1
    if adopt_items:
        print(f"{len(adopt_items)} real skill(s) still live outside the guild.")
        print("Run `ag adopt " + agent + " --apply` first, then retry link-root.")
        return 1
    if block_items:
        print(f"{len(block_items)} host-wired / platform-managed item(s) must stay "
              "in a real directory — per-skill tier is the correct mode for "
              "this runtime.")
        return 1
    if not apply_:
        print("re-run with --apply to execute")
        return 0

    # Execute
    for c in trash_items:
        if not to_trash(c):
            print(f"FAILED to trash {c} — aborted, nothing else touched")
            return 1
    for c in move_items:
        dest = guild / c.name
        if dest.exists() or is_link(dest):
            print(f"FAILED: {dest} appeared after planning — aborted")
            return 1
        # Moving a relative symlink verbatim changes its meaning. Create a
        # replacement using the target resolved at the original location,
        # then remove only the original link (also safe for junctions).
        ok, how = make_link(dest, link_targets[c])
        if not ok:
            print(f"FAILED to link {dest}: {how} — original link kept")
            return 1
        if not drop_link(c):
            drop_link(dest)
            print(f"FAILED to remove {c} — original link kept")
            return 1
    leftover = list(root.iterdir())
    if leftover:
        print(f"refusing to link: {root} is not empty after planning "
              f"({', '.join(c.name for c in leftover)})")
        return 1
    try:
        os.rmdir(root)
    except OSError as e:
        print(f"FAILED to remove emptied dir {root}: {e}")
        return 1
    ok, how = make_link(root, guild)
    if not ok or not (root / "agent-guild" / "SKILL.md").is_file():
        print(f"FAILED: {how} (original dir contents are in trash)")
        return 1
    audit("link-root", {"agent": agent, "root": str(root), "mode": how,
                        "trashed": len(trash_items), "moved": len(move_items)})
    print(f"linked {root} -> {guild} ({how})")
    print(f"consolidated: trashed={len(trash_items)} moved_into_guild={len(move_items)}")
    print("next: trigger-test the skill in your runtime, then "
          f"`ag register {agent} <home> dir-symlink {root}`")
    return 0


def agent_home(name: str) -> Path | None:
    """Resolve an agent's home dir on THIS device: registry first (host block,
    then the legacy flat field), finally the ~/.<name>/ convention."""
    entry = load_registry().get("agents", {}).get(name, {})
    home = entry_view(entry).get("home")
    if home and home != "platform-managed":
        p = Path(home).expanduser()
        if p.is_dir():
            return p
    p = Path(f"~/.{name}").expanduser()
    return p if p.is_dir() else None


def to_trash(path: Path) -> bool:
    """Recoverable delete, cross-platform.

    Tries the OS trash helper first (`trash` on macOS, `gio trash` / `trash-put`
    on Linux, Recycle Bin via PowerShell on Windows); otherwise moves the path
    into the guild's own .trash/<timestamp>/ so nothing is ever unrecoverable.

    Links are unlinked, never trashed: a trash helper (or a cross-device
    `shutil.move`) can follow a symlink/junction and take the TARGET with it.
    Dropping a link loses no data — the target stays exactly where it is.
    """
    if is_link(path):
        return drop_link(path)
    for cmd in (["trash"], ["trash-put"], ["gio", "trash"]):
        exe = shutil.which(cmd[0])
        if exe:
            try:
                if subprocess.run(cmd + [str(path)],
                                  capture_output=True).returncode == 0:
                    return True
            except OSError:
                pass
    if os.name == "nt" and shutil.which("powershell"):
        ps = (
            "Add-Type -AssemblyName Microsoft.VisualBasic; "
            "[Microsoft.VisualBasic.FileIO.FileSystem]::"
            f"{{0}}('{path}','OnlyErrorDialogs','SendToRecycleBin')"
        ).format("DeleteDirectory" if path.is_dir() else "DeleteFile")
        try:
            if subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                              capture_output=True).returncode == 0:
                return True
        except OSError:
            pass
    graveyard = CENTRAL / ".trash" / datetime.now().strftime("%Y%m%d-%H%M%S")
    graveyard.mkdir(parents=True, exist_ok=True)
    try:
        shutil.move(str(path), str(graveyard / path.name))
        return True
    except OSError:
        return False


def make_link(link: Path, target: Path) -> Tuple[bool, str]:
    """Create link -> target. Symlink first; on Windows fall back to a
    directory junction / hard link, which need no special privileges."""
    try:
        link.symlink_to(target, target_is_directory=target.is_dir())
        return True, "symlink"
    except (OSError, NotImplementedError) as e:
        first = e
    if os.name == "nt":
        if target.is_dir():
            r = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)],
                               capture_output=True)
            if r.returncode == 0:
                return True, "junction"
        else:
            try:
                os.link(str(target), str(link))
                return True, "hardlink"
            except OSError:
                pass
    return False, f"link failed: {first}"


# Windows reparse tags. Defined in `stat` only on Windows (3.8+), so the
# literals are the fallback when the attribute is missing.
_TAG_MOUNT_POINT = getattr(stat, "IO_REPARSE_TAG_MOUNT_POINT", 0xA0000003)
_TAG_SYMLINK = getattr(stat, "IO_REPARSE_TAG_SYMLINK", 0xA000000C)


def is_link(p: Path) -> bool:
    """True for symlinks AND Windows directory junctions.

    `Path.is_symlink()` is False for a junction (IO_REPARSE_TAG_MOUNT_POINT)
    even though `make_link` creates junctions on Windows as the
    no-privilege fallback. Without this, a junctioned skills dir looks like
    an ordinary directory, and adopt / link-root would try to move the
    guild's own files back into the guild.
    """
    try:
        if p.is_symlink():
            return True
    except OSError:
        return False
    if os.name != "nt":
        return False
    try:
        tag = os.lstat(p).st_reparse_tag  # Windows-only attribute
    except (OSError, ValueError, AttributeError):
        return False
    return tag in (_TAG_MOUNT_POINT, _TAG_SYMLINK)


def link_target(p: Path) -> str:
    """Readable link target. os.readlink handles junctions on 3.8+; fall
    back to the resolved path when it does not."""
    try:
        return os.readlink(p)
    except OSError:
        try:
            return str(p.resolve())
        except OSError:
            return "?"


def drop_link(p: Path) -> bool:
    """Remove a link itself, never its target. A junction needs rmdir."""
    try:
        p.unlink()
        return True
    except OSError:
        try:
            os.rmdir(p)
            return True
        except OSError:
            return False


# ------------------------------------------------------------------- init ---

def read_runtime_version() -> dict:
    """Read the installed runtime version anchor. Host-scoped: each device
    installs its own copy of the skill package, so the version is a property
    of the device, not of the shared guild."""
    path = host_state("VERSION")
    if not path.is_file():
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, _, v = line.partition("=")
            out[k.strip()] = v.strip()
    return out


def write_runtime_version(proto: str, skill: str) -> None:
    """Persist the applied protocol/skill version for THIS device."""
    (host_dir(create=True) / "VERSION").write_text(
        "# Agent Guild runtime version — managed by `ag init` / `ag upgrade`.\n"
        "# Records the version last applied on THIS device. Do not edit.\n"
        f"host_id={host_id()}\n"
        f"protocol_version={proto}\n"
        f"skill_version={skill}\n",
        encoding="utf-8",
    )


def current_versions(skill_src: Path) -> Tuple[str, str]:
    """(protocol_version, skill_version) declared by a skill package."""
    m = skill_src / "manifest.json"
    if m.is_file():
        try:
            d = json.loads(m.read_text(encoding="utf-8"))
            return (d.get("protocol_version", PROTOCOL_VERSION),
                    d.get("skill_version", "0"))
        except (OSError, ValueError):
            pass
    return (PROTOCOL_VERSION, "0")


def _version_gt(a: str, b: str) -> bool:
    """True if semantic version a > b (e.g. '3.4.0' > '3.3.1')."""

    def parts(v: str) -> list:
        out = []
        for seg in str(v).replace("-", ".").split("."):
            out.append(int(re.sub(r"\D", "", seg) or "0"))
        return out

    pa, pb = parts(a), parts(b)
    for x, y in zip(pa, pb):
        if x != y:
            return x > y
    return len(pa) > len(pb)


def cmd_init(args: list) -> int:
    """Bootstrap the central dir. Idempotent: never clobbers existing data."""
    agent = default_agent(args)
    fresh = not CENTRAL.exists()

    created_dirs, created_files = [], []
    for rel in SKELETON:
        p = CENTRAL / rel
        if not p.exists():
            p.mkdir(parents=True, exist_ok=True)
            created_dirs.append(rel)

    for rel, body in PLACEHOLDERS.items():
        p = CENTRAL / rel
        with _append_lock(p):
            if not p.exists():
                _atomic_write_text(p, body)
                created_files.append(rel)

    with _append_lock(REGISTRY):
        if not REGISTRY.exists():
            atomic_write_json(REGISTRY, {
                "protocol_version": PROTOCOL_VERSION,
                "central_dir": "~/.agent-guild/",
                "agents": {},
            })
            created_files.append("registry.json")

    # Claim this device (protocol 3.3+). host.json is the device's own record;
    # host-notes.md is where the user keeps facts that are true HERE only.
    hd = host_dir(create=True)
    facts = platform_facts()
    host_json = hd / "host.json"
    first_seen = now_iso()
    if host_json.is_file():
        try:
            first_seen = json.loads(host_json.read_text(encoding="utf-8")) \
                .get("first_seen") or first_seen
        except (OSError, ValueError):
            pass
    atomic_write_json(host_json, {
        "host_id": facts["host_id"],
        "platform": facts["platform"],
        "os": facts["os"],
        "arch": facts["arch"],
        "links": facts["links"],
        "python": facts["python"],
        "first_seen": first_seen,
        "last_init": now_iso(),
    })
    notes = hd / HOST_NOTES
    if not notes.exists():
        notes.write_text(
            f"# Host notes — {facts['host_id']}\n\n"
            "> Facts that are true on THIS device only: local tool paths,\n"
            "> project checkout locations, quirks of this OS install.\n"
            "> Shared truths belong in identity/ rules/ projects/ instead.\n"
            f"\n- platform: {facts['platform']}\n"
            f"- links: {facts['links']}\n",
            encoding="utf-8")
        created_files.append(f"hosts/{facts['host_id']}/{HOST_NOTES}")

    # Make sure the protocol's own skill is present AND current in the bus.
    # Compare against the installed package itself: an older runtime copy may
    # run init after another agent upgraded the guild, and its anchor can lag.
    # Refresh protocol-owned files only forwards, leaving all user data alone.
    own_skill = CENTRAL / "skills" / "agent-guild"
    skill_src = Path(__file__).resolve().parent.parent  # .../skills/agent-guild
    cur_proto, cur_skill = current_versions(skill_src)
    anchor = read_runtime_version()
    skill_missing = not (own_skill / "SKILL.md").exists()
    inst_proto = anchor.get("protocol_version", "") if not skill_missing else ""
    inst_skill = anchor.get("skill_version", "") if not skill_missing else ""
    if not skill_missing:
        package_proto, package_skill = current_versions(own_skill)
        if package_skill != "0":
            inst_proto, inst_skill = package_proto, package_skill

    source_older = ((bool(inst_skill) and _version_gt(inst_skill, cur_skill))
                    or (bool(inst_proto) and _version_gt(inst_proto, cur_proto)))
    skill_outdated = bool(inst_skill) and _version_gt(cur_skill, inst_skill)
    proto_outdated = bool(inst_proto) and _version_gt(cur_proto, inst_proto)
    upgrading = not source_older and (skill_outdated or proto_outdated)
    applied_proto, applied_skill = inst_proto or cur_proto, inst_skill or cur_skill
    refresh_docs = False

    skill_status = "already current"
    if skill_missing:
        if (skill_src / "SKILL.md").is_file() and skill_src.resolve() != own_skill.resolve():
            own_skill.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(skill_src, own_skill, dirs_exist_ok=True)
            skill_status = "installed"
            applied_proto, applied_skill = cur_proto, cur_skill
            refresh_docs = True
        else:
            skill_status = "MISSING — copy the agent-guild skill package into skills/agent-guild/"
    elif upgrading:
        if skill_src.resolve() != own_skill.resolve() and (skill_src / "SKILL.md").is_file():
            # Same restricted swap path as `upgrade --apply`: source init must
            # not bypass the link/protocol/downgrade checks and the backup.
            _upgrade_replace_tree(skill_src, own_skill)
            skill_status = f"upgraded {inst_skill or '?'} → {cur_skill}"
            applied_proto, applied_skill = cur_proto, cur_skill
            refresh_docs = True
        else:
            skill_status = "kept installed package — upgrade source unavailable"
    elif source_older:
        skill_status = f"kept newer installed version {inst_skill}"
    elif (anchor.get("skill_version") != applied_skill
          or anchor.get("protocol_version") != applied_proto):
        skill_status = "anchor repaired"

    # An in-place package update can already be newer than its anchor. Repair
    # the anchor and docs from that installed package, never from an old copy.
    refresh_docs = refresh_docs or any(
        old and _version_gt(new, old) for new, old in (
            (applied_skill, anchor.get("skill_version", "")),
            (applied_proto, anchor.get("protocol_version", "")),
        )
    )
    write_runtime_version(applied_proto, applied_skill)

    # Seed / refresh the root protocol docs. First run seeds them; an upgrade
    # follows the version; when already current they are left alone.
    # Docs are looked up in both layouts a registry may require: `references/` as in
    # the repository, and `references/` as used by hosts that only sanction
    # references/ scripts/ templates/ inside a skill package.
    for doc in PROTOCOL_DOCS:
        target = CENTRAL / doc
        src = None
        for base in ((own_skill,) if source_older else (own_skill, skill_src)):
            for sub in DOC_DIRS:
                cand = base / sub / doc
                if cand.is_file():
                    src = cand
                    break
            if src is not None:
                break
        if src is None:
            continue
        body = src.read_text(encoding="utf-8")
        if not target.exists():
            target.write_text(body, encoding="utf-8")
            created_files.append(doc)
        elif refresh_docs and target.read_text(encoding="utf-8") != body:
            target.write_text(body, encoding="utf-8")
            created_files.append(doc)

    audit("init", {"agent": agent, "fresh": fresh, "dirs": len(created_dirs)})

    print(f"{'initialized' if fresh else 'verified'} {CENTRAL}")
    print(f"  protocol_version : {applied_proto}")
    print(f"  skill_version    : {applied_skill}")
    print(f"  this device      : {facts['host_id']} "
          f"({facts['platform']}, links={facts['links']})")
    print(f"  dirs created     : {len(created_dirs)}" + (f" ({', '.join(created_dirs)})" if created_dirs else ""))
    print(f"  files created    : {len(created_files)}" + (f" ({', '.join(created_files)})" if created_files else ""))
    print(f"  own skill        : {skill_status}")
    print()
    print("Next: `ag bootstrap <agent>` to read context; close with `ag finish <agent>` "
          "(summary via stdin). Use `ag recall <keyword>` to find it later.")
    print("Optional: see ONBOARDING.md to register an agent or share skills and tools.")
    return 0


# ---------------------------------------------------------------- upgrade ---

def _verkey(v: str) -> Tuple[int, ...]:
    """Semantic-version tuple for comparison."""
    return tuple(int(re.sub(r"\D", "", seg) or "0")
                 for seg in str(v).replace("-", ".").split("."))


def _http_bytes(url: str, timeout: int = 6) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "agent-guild"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _http_json(url: str, timeout: int = 12):
    return json.loads(_http_bytes(url, timeout).decode("utf-8"))


def fetch_skillhub_version() -> str:
    d = _http_json("https://api.skillhub.cn/api/v1/search?q=agent-guild")
    for x in d.get("results", []):
        ns = (x.get("namespace") or {}).get("canonicalName", "")
        if x.get("slug") == "agent-guild" or "agent-guild" in str(ns):
            v = x.get("version")
            if v:
                return str(v)
    raise LookupError("agent-guild not found on skillhub")


def fetch_github_version() -> str:
    """Get the latest release tag via the releases/latest redirect (no API,
    no rate limit)."""

    class _NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, hdrs, newurl):
            return None

    opener = urllib.request.build_opener(_NoRedirect)
    req = urllib.request.Request(
        "https://github.com/dqsjqian/agent-guild/releases/latest",
        headers={"User-Agent": "agent-guild"})
    try:
        opener.open(req, timeout=6)
        raise LookupError("no redirect from releases/latest")
    except urllib.error.HTTPError as e:
        if e.code not in (301, 302, 303, 307, 308):
            raise
        loc = e.headers.get("Location", "")
        tag = loc.rstrip("/").rsplit("/", 1)[-1]
        if not tag or not tag.startswith("v"):
            raise LookupError(f"unexpected redirect target: {loc}")
        return tag[1:]


def fetch_clawhub_version() -> str:
    d = _http_json("https://clawhub.ai/api/v1/skills/agent-guild/versions")
    items = d.get("items", [])
    if not items or not items[0].get("version"):
        raise LookupError("no versions on clawhub")
    return str(items[0]["version"])


def cmd_upgrade(args: list) -> int:
    """Check the three platforms for a newer version; --apply downloads and
    installs it (user data preserved)."""
    apply_ = "--apply" in args

    versions, errors = {}, []
    for name, fetcher in (("skillhub", fetch_skillhub_version),
                          ("github", fetch_github_version),
                          ("clawhub", fetch_clawhub_version)):
        try:
            versions[name] = fetcher()
        except Exception as e:  # network / parse — skip this source
            errors.append(f"{name}: {e}")

    if not versions:
        print("could not reach any version source")
        for e in errors:
            print(f"  - {e}")
        return 1

    local = read_runtime_version().get("skill_version", "0")
    latest_name, latest = max(versions.items(), key=lambda kv: _verkey(kv[1]))

    print("version check:")
    for name, v in versions.items():
        mark = "  ← latest" if name == latest_name else ""
        print(f"  {name:<9} {v}{mark}")
    print(f"  {'local':<9} {local}")
    for e in errors:
        print(f"  (unreachable: {e})")

    if not _version_gt(latest, local):
        print(f"\nalready up to date ({local}).")
        return 0

    print(f"\nupdate available: {local} → {latest} (from {latest_name})")
    if not apply_:
        print("run `ag upgrade --apply` to download and install.")
        return 0

    print("downloading ...")
    ok, msg = _download_and_apply(latest)
    print(f"  {msg}")
    if not ok:
        return 1
    print("user data (identity/rules/log/handoff/skills_data/connectors/memory) untouched.")
    return 0


# 安装和更新共用此校验链；HTTPS 元数据提供完整性，不等同独立签名信任。
_UPGRADE_MAX_BYTES = 64 * 1024 * 1024
_UPGRADE_MAX_ENTRIES = 2048


def _release_bytes(url: str, limit: int, timeout: int = 120) -> bytes:
    """有界 HTTPS 下载；重定向也不得降级或离开 GitHub 的资产主机。"""
    from urllib.parse import urlsplit

    def check_url(value):
        parsed = urlsplit(value)
        if (parsed.scheme != "https" or parsed.username or parsed.password
                or parsed.port not in (None, 443)
                or parsed.hostname not in ("api.github.com", "github.com",
                                           "release-assets.githubusercontent.com",
                                           "objects.githubusercontent.com")):
            raise ValueError("拒绝非授权 HTTPS release URL")

    class SafeRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            check_url(newurl)
            return super().redirect_request(req, fp, code, msg, headers, newurl)

    check_url(url)
    req = urllib.request.Request(url, headers={"User-Agent": "agent-guild",
                                               "Accept": "application/vnd.github+json"})
    with urllib.request.build_opener(SafeRedirect).open(req, timeout=timeout) as response:
        check_url(response.geturl())
        data = response.read(limit + 1)
    if len(data) > limit:
        raise ValueError("release 下载超过大小上限")
    return data


def _release_digest(asset: dict):
    value = asset.get("digest")
    if value is None or value == "":
        return None
    if not isinstance(value, str) or not re.fullmatch(r"sha256:[0-9a-fA-F]{64}", value):
        raise ValueError("release asset digest 必须是完整 SHA-256")
    return value[7:].lower()


def _verified_release_zip(version: str) -> bytes:
    """绑定同一 tag、资产名称及 HTTPS API digest，缺少校验依据则拒绝安装。"""
    import hashlib
    if not isinstance(version, str) or not re.fullmatch(r"[0-9]{1,6}\.[0-9]{1,6}\.[0-9]{1,6}", version):
        raise ValueError("release version 必须为 x.y.z")
    api = "https://api.github.com/repos/dqsjqian/agent-guild/releases/tags/v" + version
    release = json.loads(_release_bytes(api, 2 * 1024 * 1024, timeout=30))
    if (not isinstance(release, dict) or release.get("tag_name") != "v" + version
            or release.get("draft") or release.get("prerelease")):
        raise ValueError("release tag 不匹配或不是正式发布")
    assets = release.get("assets")
    if not isinstance(assets, list):
        raise ValueError("release 缺少资产列表")
    name = f"agent-guild-v{version}.zip"
    url = GITHUB_RELEASE_ZIP.format(ver=version)

    def asset_named(asset_name, asset_url, limit):
        matches = [a for a in assets if isinstance(a, dict) and a.get("name") == asset_name]
        if len(matches) != 1:
            raise ValueError(f"release 必须包含唯一资产 {asset_name}")
        asset = matches[0]
        size = asset.get("size")
        if (asset.get("browser_download_url") != asset_url
                or asset.get("state") != "uploaded"
                or type(size) is not int or not 0 < size <= limit):
            raise ValueError(f"release 资产 URL、状态或大小无效: {asset_name}")
        return asset

    asset = asset_named(name, url, _UPGRADE_MAX_BYTES)
    expected = _release_digest(asset)
    if expected is None:
        sidecar = asset_named(name + ".sha256", url + ".sha256", 4096)
        checksum = _release_bytes(url + ".sha256", 4096)
        if len(checksum) != sidecar["size"]:
            raise ValueError("SHA-256 sidecar 大小不匹配")
        sidecar_digest = _release_digest(sidecar)
        if sidecar_digest and hashlib.sha256(checksum).hexdigest() != sidecar_digest:
            raise ValueError("SHA-256 sidecar digest 不匹配")
        match = re.fullmatch(r"([0-9a-fA-F]{64}) [ *]" + re.escape(name) + r"\r?\n?",
                             checksum.decode("ascii"))
        if not match:
            raise ValueError("SHA-256 sidecar 必须仅包含目标资产 basename 和完整 hash")
        expected = match.group(1).lower()
    data = _release_bytes(url, _UPGRADE_MAX_BYTES)
    if len(data) != asset["size"] or hashlib.sha256(data).hexdigest() != expected:
        raise ValueError("release ZIP SHA-256 或大小不匹配；未安装")
    return data


def _extract_verified_release(data: bytes, stage: Path, version: str) -> Tuple[Path, str]:
    """先验证整个 ZIP 索引，再解包；拒绝路径别名、链接和压缩炸弹。"""
    import unicodedata
    paths, explicit, total = {}, set(), 0
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        entries = archive.infolist()
        if not entries or len(entries) > _UPGRADE_MAX_ENTRIES:
            raise ValueError("ZIP 条目数超限")
        for entry in entries:
            raw = entry.filename
            parts = (raw[:-1] if raw.endswith("/") else raw).split("/")
            if (raw != entry.orig_filename or "\\" in raw or not raw
                    or parts[0] != "agent-guild" or len(parts) > 3
                    or (len(parts) == 1 and not entry.is_dir())):
                raise ValueError("ZIP 路径或包布局无效")
            for part in parts:
                device = part.split(".", 1)[0].upper()
                if (part in ("", ".", "..") or part.endswith((".", " "))
                        or any(ord(c) < 32 or ord(c) == 127 or c in ':<>"|?*' for c in part)
                        or device in ("CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$")
                        or re.fullmatch(r"(?:COM|LPT)[1-9¹²³]", device)):
                    raise ValueError("ZIP 包含不安全路径")
            key = unicodedata.normalize("NFC", "/".join(parts)).casefold()
            if key in explicit:
                raise ValueError("ZIP 包含重复或大小写冲突路径")
            explicit.add(key)
            for i in range(1, len(parts) + 1):
                path = "/".join(parts[:i])
                folded = unicodedata.normalize("NFC", path).casefold()
                kind = "dir" if i < len(parts) or entry.is_dir() else "file"
                if folded in paths and paths[folded] != (path, kind):
                    raise ValueError("ZIP 包含路径别名或文件目录冲突")
                paths[folded] = (path, kind)
            mode = stat.S_IFMT(entry.external_attr >> 16)
            if (mode not in (0, stat.S_IFDIR if entry.is_dir() else stat.S_IFREG)
                    or entry.flag_bits & 1
                    or entry.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED)
                    or (entry.is_dir() and entry.file_size)):
                raise ValueError("ZIP 包含链接、特殊文件或不支持的压缩条目")
            total += entry.file_size
            if (total > _UPGRADE_MAX_BYTES
                    or entry.file_size > max(1, entry.compress_size) * 200):
                raise ValueError("ZIP 解压大小或压缩比超限")
        written = 0
        for entry in entries:
            target = stage.joinpath(*entry.filename.rstrip("/").split("/"))
            if entry.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            count = 0
            with archive.open(entry) as source, target.open("xb") as dest:
                while True:
                    chunk = source.read(1024 * 1024)
                    if not chunk:
                        break
                    count += len(chunk)
                    written += len(chunk)
                    if written > _UPGRADE_MAX_BYTES or count > entry.file_size:
                        raise ValueError("ZIP 实际解压大小超限")
                    dest.write(chunk)
            if count != entry.file_size:
                raise ValueError("ZIP 实际文件大小不匹配")
            target.chmod(0o755 if target.name in ("ag.py", "install.sh") else 0o644)
    pkg = stage / "agent-guild"

    def reject(message: str):
        # 校验失败时不留下半解包的 payload，stage 由调用方处置。
        shutil.rmtree(pkg, ignore_errors=True)
        raise ValueError(message)

    if not (pkg / "manifest.json").is_file() or not (pkg / "SKILL.md").is_file():
        reject("release ZIP 缺少必要协议文件或运行模块")
    manifest = json.loads((pkg / "manifest.json").read_text(encoding="utf-8"))
    proto = manifest.get("protocol_version") if isinstance(manifest, dict) else None
    if (not isinstance(manifest, dict) or manifest.get("name") != "agent-guild"
            or manifest.get("skill_version") != version
            or not isinstance(proto, str) or not re.fullmatch(r"[0-9]+\.[0-9]+", proto)):
        reject("release manifest 名称、版本或协议不匹配")
    # 必需运行模块由 payload 自身声明：CLI 本体 + manifest.scripts 声明的
    # .py + ag.py/ag_history.py 静态 import 的 ag_* 兄弟模块。旧版合法三
    # 模块 4.0.0 包（无 ag_retention.py）因此可安装；缺自身必需模块才拒绝。
    required = {"scripts/ag.py"}
    required.update("references/" + doc for doc in PROTOCOL_DOCS)
    declared = manifest.get("scripts")
    if isinstance(declared, dict):
        for entry in declared.values():
            if (isinstance(entry, str)
                    and re.fullmatch(r"scripts/[A-Za-z0-9][A-Za-z0-9._-]*\.py", entry)):
                required.add(entry)
    for module in ("ag.py", "ag_history.py"):
        path = pkg / "scripts" / module
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            required.update("scripts/" + name + ".py" for name in
                            re.findall(r"(?m)^[ \t]*(?:import|from)[ \t]+(ag_[a-z0-9_]+)\b", text))
    missing = sorted(name for name in required if not (pkg / name).is_file())
    if missing:
        reject("release ZIP 缺少必要协议文件或运行模块: " + ", ".join(missing))
    return pkg, proto


def _upgrade_check_code_tree(root: Path) -> None:
    """仅接受有界的普通协议代码目录；不跟随 symlink/junction。"""
    if is_link(root) or not root.is_dir():
        raise ValueError(f"不是普通代码目录: {root}")
    count = size = 0
    for parent, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            path = Path(parent) / name
            count += 1
            info = path.lstat()
            if is_link(path) or not (stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode)):
                raise ValueError(f"代码目录包含链接或特殊文件: {path}")
            size += info.st_size if stat.S_ISREG(info.st_mode) else 0
            if count > _UPGRADE_MAX_ENTRIES or size > _UPGRADE_MAX_BYTES:
                raise ValueError("协议代码目录超过大小或条目上限")
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or manifest.get("name") != "agent-guild":
        raise ValueError("拒绝替换或清理非 Agent Guild 协议目录")


def _upgrade_replace_tree(src: Path, dst: Path, after_swap=None) -> None:
    """同父目录 stage → 单份代码备份 → rename；失败恢复旧包，非用户数据备份。"""
    if is_link(dst.parent) or is_link(dst):
        raise ValueError("拒绝通过链接替换协议代码")
    dst.parent.mkdir(parents=True, exist_ok=True)
    backup = dst.with_name("." + dst.name + ".previous-code")
    marker = "Agent Guild protocol code backup v1\n"
    with _append_lock(dst):
        if backup.exists() or is_link(backup):
            if (is_link(backup) or not backup.is_dir()
                    or {p.name for p in backup.iterdir()} != {"OWNER", "package"}
                    or is_link(backup / "OWNER")
                    or (backup / "OWNER").read_text(encoding="utf-8") != marker):
                raise ValueError(f"拒绝清理无法识别的代码备份: {backup}")
            _upgrade_check_code_tree(backup / "package")
            if not dst.exists():
                os.replace(backup / "package", dst)
                shutil.rmtree(backup)
        if dst.exists():
            _upgrade_check_code_tree(dst)
            old_proto, old_version = current_versions(dst)
            new_proto, new_version = current_versions(src)
            if _version_gt(old_version, new_version) or _version_gt(old_proto, new_proto):
                raise ValueError("拒绝将已安装协议降级")
        _upgrade_check_code_tree(src)
        with tempfile.TemporaryDirectory(prefix=".ag-release-stage-", dir=dst.parent) as temp:
            candidate = Path(temp) / "package"
            shutil.copytree(src, candidate)
            _upgrade_check_code_tree(candidate)
            if backup.exists():
                shutil.rmtree(backup)
            had_old = dst.exists()
            if had_old:
                backup.mkdir()
                (backup / "OWNER").write_text(marker, encoding="utf-8")
                try:
                    os.replace(dst, backup / "package")
                except BaseException:
                    shutil.rmtree(backup)
                    raise
            try:
                os.replace(candidate, dst)
                if after_swap:
                    after_swap()
            except BaseException:
                # 新包移回临时位置后再恢复旧包，不先删除可恢复的旧安装。
                if dst.exists():
                    os.replace(dst, Path(temp) / "failed-package")
                if had_old:
                    os.replace(backup / "package", dst)
                    shutil.rmtree(backup)
                raise


def _apply_verified_release(pkg: Path, proto: str, version: str) -> None:
    """仅更新协议代码、入口文档与本机版本锚；文档失败也回滚。"""
    own = CENTRAL / "skills" / "agent-guild"
    if is_link(CENTRAL) or is_link(own.parent):
        raise ValueError("拒绝通过链接写入中央协议目录")
    anchor = host_dir() / "VERSION"
    updates = {CENTRAL / doc: (pkg / "references" / doc).read_text(encoding="utf-8")
               for doc in PROTOCOL_DOCS}
    updates[anchor] = (
        "# Agent Guild runtime version — managed by `ag init` / `ag upgrade`.\n"
        "# Records the version last applied on THIS device. Do not edit.\n"
        f"host_id={host_id()}\nprotocol_version={proto}\nskill_version={version}\n")
    for path in updates:
        if is_link(path) or any(is_link(p) for p in path.parents if p != CENTRAL.parent and CENTRAL in p.parents):
            raise ValueError(f"协议状态路径不能是链接: {path}")
        if path.exists() and not path.is_file():
            raise ValueError(f"协议状态目标不是文件: {path}")

    def refresh_state():
        previous = {path: path.read_bytes() if path.exists() else None for path in updates}
        changed = []
        try:
            for path, text in updates.items():
                _atomic_write_text(path, text)
                changed.append(path)
        except BaseException:
            for path in reversed(changed):
                if previous[path] is None:
                    path.unlink()
                else:
                    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".ag-restore-")
                    try:
                        with os.fdopen(fd, "wb") as stream:
                            stream.write(previous[path])
                        os.replace(tmp, path)
                    finally:
                        if os.path.exists(tmp):
                            os.unlink(tmp)
            raise

    _upgrade_replace_tree(pkg, own, refresh_state)


def _download_and_apply(latest: str) -> Tuple[bool, str]:
    """安装器、手动升级和自动升级共用的 fail-closed release 安装路径。"""
    try:
        data = _verified_release_zip(latest)
        with tempfile.TemporaryDirectory(prefix="ag-upgrade-") as temp:
            pkg, proto = _extract_verified_release(data, Path(temp), latest)
            _apply_verified_release(pkg, proto, latest)
        return True, f"upgraded → {latest} (protocol {proto}; SHA-256 verified)"
    except Exception as error:
        return False, f"release 校验或安装失败: {error}"


def _install_release(version: str) -> int:
    """薄安装器入口；审查后的本地 CLI 先校验，最后才执行已核验的包。"""
    ok, message = _download_and_apply(version)
    if not ok:
        print(message, file=sys.stderr)
        return 1
    script = CENTRAL / "skills" / "agent-guild" / "scripts" / "ag.py"
    result = subprocess.run([sys.executable, str(script), "init"], check=False)
    return result.returncode


# ------------------------------------------------------------------ adopt ---

def _user_ignores() -> list:
    """User-defined ignore patterns from ~/.agent-guild/.adoptignore."""
    p = CENTRAL / ADOPTIGNORE
    if not p.is_file():
        return []
    out = []
    for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out


def _is_host_wired_skill(skill_dir: Path) -> bool:
    """True if this skill's capability comes from host-managed connector/MCP
    wiring, so its files are not portable on their own."""
    md = skill_dir / "SKILL.md"
    if not md.is_file():
        return False
    try:
        head = md.read_text(encoding="utf-8", errors="ignore")[:1500].lower()
    except OSError:
        return False
    return any(m in head for m in HOST_WIRED_MARKERS)


def _is_excluded(name: str, kind: str = "") -> bool:
    if name in EXCLUDE_NAMES:
        return True
    if any(s in name for s in EXCLUDE_SUBSTRINGS):
        return True
    if name.endswith(EXCLUDE_SUFFIXES):
        return True
    for pat in _user_ignores():
        if fnmatch(name, pat):
            return True
    return False


def _scan_dir(src_dir: Path, dest_root: str) -> list[dict]:
    """Adoptable children of src_dir (real dirs/files, not symlinks)."""
    found = []
    if not src_dir.is_dir():
        return found
    for child in sorted(src_dir.iterdir()):
        if is_link(child):
            continue  # already linked somewhere — nothing to adopt
        if _is_excluded(child.name, dest_root):
            continue
        if child.name.startswith("."):
            continue
        # A skill is a directory with a SKILL.md; loose files under skills/ are
        # host bookkeeping, not skills.
        if dest_root == "skills":
            if (child.is_dir() and (child / "SKILL.md").is_file()
                    and not _is_host_wired_skill(child)):
                found.append({"src": child, "dest": CENTRAL / dest_root / child.name, "kind": dest_root})
            continue
        if child.is_dir() or child.suffix in (".md", ".json", ".yaml", ".yml", ".toml"):
            found.append({
                "src": child,
                "dest": CENTRAL / dest_root / child.name,
                "kind": dest_root,
            })
    return found


def _scan_agent(home: Path, agent: str) -> list[dict]:
    items, seen_src, used_dest = [], set(), set()

    def add(src: Path, dest: Path, kind: str) -> None:
        key = src.resolve() if src.exists() else src
        if key in seen_src:
            return
        seen_src.add(key)
        # Two distinct sources can map to the same name (e.g. ~/.x/MEMORY.md and
        # ~/.x/memory/MEMORY.md). Disambiguate instead of silently overwriting.
        if dest in used_dest:
            try:
                rel = src.parent.relative_to(home).as_posix()
            except ValueError:
                rel = src.parent.name
            tag = rel.strip("./").replace("/", "-") or "home"
            dest = dest.with_name(f"{dest.stem}__{tag}{dest.suffix}")
        used_dest.add(dest)
        items.append({"src": src, "dest": dest, "kind": kind})

    for cls, subdirs in CANDIDATE_LAYOUT.items():
        dest_root = ADOPT_DESTS[cls]
        for sub in subdirs:
            src_dir = home / sub
            for it in _scan_dir(src_dir, dest_root):
                dest = it["dest"]
                if cls == "memory":
                    # keep each agent's memory namespaced: memory/<agent>/
                    dest = CENTRAL / dest_root / agent / it["src"].name
                add(it["src"], dest, it["kind"])

    # agent-private memory files sitting at the home root
    for fname in MEMORY_FILES:
        f = home / fname
        if f.is_file() and not is_link(f):
            add(f, CENTRAL / "memory" / agent / fname, "memory")
    return items


def _link_back(src: Path, dest: Path) -> Tuple[bool, str]:
    """Move src -> dest, then link src -> dest. Verify; roll back on any failure.

    The verification step matters most for memory files: some runtimes recreate
    or refuse to follow links, and a silent failure would lose user data.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        shutil.move(str(src), str(dest))
    except OSError as e:
        return False, f"move failed: {e}"

    linked, how = make_link(src, dest)
    if not linked:
        shutil.move(str(dest), str(src))  # rollback
        return False, f"{how} (rolled back)"

    # Verify the link resolves to the new location and is still readable.
    ok, why = True, ""
    try:
        if not src.exists() or src.resolve() != dest.resolve():
            ok, why = False, "link does not resolve to target"
        elif dest.is_file():
            dest.read_bytes()
    except OSError as e:
        ok, why = False, f"unreadable after link: {e}"

    if not ok:
        try:
            src.unlink()
        except OSError:
            try:
                shutil.rmtree(src)  # Windows junction
            except OSError:
                pass
        shutil.move(str(dest), str(src))  # rollback
        return False, f"verification failed: {why} (rolled back)"
    return True, how


def cmd_adopt(args: list) -> int:
    apply = "--apply" in args
    rest = [a for a in args if not a.startswith("-")]
    agent = default_agent(rest)
    home = agent_home(agent)
    if home is None:
        print(f"cannot resolve home for agent '{agent}' — "
              f"pass a registered name or set AG_AGENT", file=sys.stderr)
        return 1
    if not CENTRAL.exists():
        print(f"{CENTRAL} missing — run `ag init` first", file=sys.stderr)
        return 1

    items = _scan_agent(home, agent)
    if not items:
        print(f"nothing to adopt from {home}")
        return 0

    print(f"{'ADOPTING' if apply else 'DRY-RUN'} — agent={agent} home={home}")
    print(f"{'kind':<12} {'name':<34} action")
    print("-" * 78)

    moved = skipped = failed = 0
    for it in items:
        src, dest, kind = it["src"], it["dest"], it["kind"]
        if dest.exists() or is_link(dest):
            print(f"{kind:<12} {src.name:<34} skip (already in guild)")
            skipped += 1
            continue
        if not apply:
            print(f"{kind:<12} {src.name:<34} would move -> {dest.relative_to(CENTRAL)}")
            continue
        ok, msg = _link_back(src, dest)
        if ok:
            print(f"{kind:<12} {src.name:<34} moved + symlinked")
            audit("adopt", {"agent": agent, "kind": kind, "name": src.name})
            moved += 1
        else:
            print(f"{kind:<12} {src.name:<34} FAILED: {msg}")
            failed += 1

    print("-" * 78)
    if apply:
        print(f"moved={moved} skipped={skipped} failed={failed}")
    else:
        print(f"{len(items) - skipped} candidate(s). Re-run with --apply to execute.")
        print("Excluded by policy: caches (.venv/node_modules), credentials, "
              "platform-managed packages (__skillhub/connector-*).")
    return 0 if failed == 0 else 1


# -------------------------------------------------------------- bootstrap ---

BOOTSTRAP_FILES = [
    ("identity/profile.md", "WHO THE USER IS"),
    ("identity/ROUTINE.md", "ROUTINE"),
    ("rules/universal.md", "SHARED RULES (user-authored)"),
]


def _inbox_messages(agent: str) -> list:
    """List message files, leaving persistent lock sidecars in place."""
    if not INBOX.is_dir():
        return []
    return [f for f in sorted(INBOX.iterdir())
            if f.is_file() and f.suffix == ".md" and not f.name.startswith(".")
            and f"-to-{agent}-" in f.name]


def cmd_bootstrap(args: list) -> int:
    """Read shared context, with policy-controlled maintenance by default."""
    if not CENTRAL.exists():
        print(f"{CENTRAL} missing — run `ag init` first", file=sys.stderr)
        return 1
    agent = default_agent(args)
    shown = 0

    # Which device am I on? Everything platform- or host-scoped hangs off this.
    hid = host_id()
    print(f"\n{'=' * 78}\n== THIS DEVICE\n{'=' * 78}")
    print(f"host-id  : {hid}   platform: {platform_tag()}   links: {link_capability()}")
    others = [h for h in known_hosts() if h != hid]
    print(f"others   : {', '.join(others) if others else '(none seen yet)'}")
    print(f"host data: hosts/{hid}/   (paths, install state, device-only facts)")
    print("platform assets: resolve with `ag tool <name>` — never hardcode a path")
    # Host notes can contain task details. Resolve them only after an explicit
    # task selection; a new conversation must not inherit another task.

    for rel, title in BOOTSTRAP_FILES:
        p = CENTRAL / rel
        print(f"\n{'=' * 78}\n== {title}  ({rel})\n{'=' * 78}")
        if p.exists():
            print(p.read_text(encoding="utf-8").rstrip())
            shown += 1
        else:
            print(f"[missing: {rel}]")

    # Do not inject message topics or task metadata into an unrelated session.
    print("\nTask context: not loaded. Ask for todos, then select a task.")
    print("Use `ag task list --session <session-id> --agent <agent>` only on request.")
    print("Messages are separate: `ag inbox <agent>` (explicit request only).")

    # Other rules files, listed not dumped (read on demand)
    extra = sorted(p.name for p in (CENTRAL / "rules").glob("*.md")
                   if p.name != "universal.md") if (CENTRAL / "rules").is_dir() else []
    if extra:
        print(f"\nOther rules (read on demand): {', '.join(extra)}")

    # Learning-ledger pending summary (protocol 3.1+)
    led = []
    for path in _ledger_files():
        if not path.exists():
            continue
        entries = _parse_entries(path.read_text(encoding="utf-8"))
        n_open = sum(1 for e in entries
                     if _field(e, "Status") in ("", "pending", "in_progress"))
        if n_open:
            led.append(f"{path.stem} {n_open} open")
    if led:
        print(f"\nLearning ledger (learnings/): {' | '.join(led)}")
        print("  fix what you touch (ag resolve), promote what recurs (ag review).")

    print(f"\n{shown}/{len(BOOTSTRAP_FILES)} context files loaded.")
    print("Mid-session: `ag recall <keyword>` searches shared memory; "
          "close out with `ag finish` (summary via stdin).")

    # Data hygiene (protocol 3.2+): rate-limited auto-groom so the guild never
    # slowly rots. Prints only when something was found; never fails.
    if "--no-maintenance" not in args:
        maybe_auto_groom(agent)

    if "--no-maintenance" not in args:
        _history_maintenance()

    # Upgrade self-check (3.9.0+): once per interval_hours, compare against
    # the published version; mode=apply installs it. Policy: UPGRADE.md.
    if "--no-maintenance" not in args:
        maybe_auto_upgrade(agent)
    return 0


# ------------------------------------------------------------------ recall ---

# Shared-memory roots a recall query walks (read-only, *.md, recursive).
# Host- and platform-scoped state, skills/, tools/ and registry internals
# stay out: a memory query must not surface another device's install noise.
RECALL_ROOTS = (
    "identity", "rules", "projects", "memory",
    "messages/inbox", "messages/archive",
    "log/daily", "log/archive", "learnings",
)


def cmd_recall(args: list) -> int:
    """Full-text search across shared memory (grep-style, read-only)."""
    if not CENTRAL.exists():
        print(f"{CENTRAL} missing — run `ag init` first", file=sys.stderr)
        return 1
    limit_raw = _opt(args, "--limit", "20")
    try:
        limit = max(1, int(limit_raw))
    except ValueError:
        print("--limit needs an integer", file=sys.stderr)
        return 2
    or_mode = "--all" in args
    if or_mode:
        args.remove("--all")
    keywords = [a.lower() for a in args if a and not a.startswith("-")]
    if not keywords:
        print("usage: ag recall <keyword> [...] [--limit N] [--all]",
              file=sys.stderr)
        return 2

    hits, done = 0, False
    for root in RECALL_ROOTS:
        if done:
            break
        d = _session_path(root)
        if not d.is_dir():
            continue
        for p in sorted(d.rglob("*.md")):
            if done:
                break
            try:
                lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
            except OSError:
                continue
            for no, line in enumerate(lines, 1):
                low = line.lower()
                hit = any(k in low for k in keywords) if or_mode \
                    else all(k in low for k in keywords)
                if hit:
                    print(f"{p.relative_to(CENTRAL)}:{no}: {line.strip()}")
                    hits += 1
                    if hits >= limit:
                        done = True
                        break
    if not hits:
        print(f"no matches for: {' '.join(keywords)}")
        return 1
    print(f"\n{hits} match(es) in shared memory (limit {limit})")
    return 0


# ------------------------------------------------------------------ finish ---

def _daily_log_path(agent: str) -> Path:
    """Today's daily-log file for agent. One device: the historical name.
    Several devices: suffix with the host-id, so two machines appending on
    the same day cannot collide when the guild is carried between them."""
    day = datetime.now().strftime("%Y-%m-%d")
    path = DAILY / f"{day}-{agent}.md"
    if len(known_hosts()) > 1 and not path.exists():
        path = DAILY / f"{day}-{agent}.{host_id()}.md"
    return path


def _touch_last_seen(name: str) -> bool:
    """Refresh an agent's presence stamps (shared + this device's block).
    Returns False when the agent is not registered — caller decides whether
    that is fatal."""
    with _append_lock(REGISTRY):
        data = load_registry()
        agents = data.setdefault("agents", {})
        if name not in agents:
            return False
        hid, stamp = host_id(), now_iso()
        entry = agents[name]
        fold_entry_to_host(entry, hid)
        entry.setdefault("hosts", {}).setdefault(hid, {})["last_seen"] = stamp
        entry["last_seen"] = stamp
        entry["mirror_host"] = hid
        save_registry(data, name, "last_seen")
    return True


def cmd_finish(args: list) -> int:
    """Close a session: summary (stdin) -> daily log, presence refresh,
    inbox report / archive."""
    archive_inbox = "--archive-inbox" in args
    if archive_inbox:
        args.remove("--archive-inbox")
    agent = default_agent(args)
    body = read_stdin()
    if not body:
        print("usage: ag finish [agent] [--archive-inbox]  (summary from stdin)",
              file=sys.stderr)
        return 2
    if not CENTRAL.exists():
        print(f"{CENTRAL} missing — run `ag init` first", file=sys.stderr)
        return 1

    # 1) session summary -> today's daily log (lock-protected atomic append)
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", agent):
        print("invalid agent identifier", file=sys.stderr)
        return 2
    path = _daily_log_path(agent)
    atomic_append(path, f"\n## Session summary — {now_iso()} by {agent}\n\n{body}\n")

    # 2) presence: the same refresh `ag last-seen` does, never fatal here
    if not _touch_last_seen(agent):
        print(f"note: agent '{agent}' not registered — last_seen not refreshed")

    # 3) inbox: report pending, or archive what this agent has now processed
    #    (SPEC 3.6: recipient moves a handled message to handoff/archive/)
    mine = _inbox_messages(agent)
    archived = 0
    if mine and archive_inbox:
        archive_dir = _session_path("messages/archive", write=True)
        for f in mine:
            # Match send's lock so a pending append cannot land in a file
            # being moved. Keep its sidecar stable for later senders.
            with _append_lock(f):
                if not f.is_file():
                    continue  # another finish already archived this message
                with _append_lock(archive_dir):
                    archive_dir.mkdir(parents=True, exist_ok=True)
                    dest = archive_dir / f.name
                    suffix = 1
                    while dest.exists() or dest.is_symlink():
                        dest = archive_dir / f"{f.stem}-{suffix}{f.suffix}"
                        suffix += 1
                    import ag_history
                    with ag_history.budget_lock(sys.modules[__name__]):
                        ag_history.ensure_capacity(sys.modules[__name__], f.stat().st_size)
                        shutil.move(str(f), str(dest))
                archived += 1
        print(f"archived {archived} inbox message(s) -> messages/archive/")
    elif mine:
        print(f"{len(mine)} inbox message(s) still pending — process them, "
              f"then re-run with --archive-inbox")

    audit("finish", {"agent": agent, "log": f"log/daily/{path.name}",
                     "archived_inbox": archived})
    print(f"session closed for {agent} — summary in log/daily/{path.name}")
    _history_maintenance()
    return 0


# ----------------------------------------------------------------- doctor ---

def cmd_doctor(args: list) -> int:
    """Health check: broken links, missing files, registry / version drift."""
    if not CENTRAL.exists():
        print(f"{CENTRAL} missing — run `ag init` first", file=sys.stderr)
        return 1

    problems = 0
    print("== broken links in the guild ==")
    dangling = []
    for root, dirs, files in os.walk(CENTRAL, followlinks=False):
        for name in list(dirs) + files:
            p = Path(root) / name
            if is_link(p) and not p.exists():
                dangling.append(p)
    if dangling:
        for p in dangling:
            print(f"  ✗ {p} -> {link_target(p)}")
        problems += len(dangling)
    else:
        print("  ok — none")

    print("\n== broken links in registered agent homes ==")
    reg = load_registry()
    local_agents = {n: e for n, e in reg.get("agents", {}).items()
                    if registered_here(e)}
    remote_agents = {n: e for n, e in reg.get("agents", {}).items()
                     if not registered_here(e)}
    agent_dangling = []
    for name, entry in local_agents.items():
        sr = entry_view(entry).get("skills_root")
        if not sr or sr == "platform-managed":
            continue
        d = Path(sr).expanduser()
        if not d.is_dir():
            continue
        try:
            children = list(d.iterdir())
        except OSError:
            continue
        for child in children:
            if is_link(child) and not child.exists():
                agent_dangling.append((name, child))
    if agent_dangling:
        for name, p in agent_dangling:
            print(f"  ✗ [{name}] {p} -> {link_target(p)}")
        problems += len(agent_dangling)
    else:
        print("  ok — none")

    print("\n== link direction (the guild owns its payloads) ==")
    outbound = _outbound_links()
    if outbound:
        for p, t in outbound:
            print(f"  ✗ {p.relative_to(CENTRAL)} -> {t}")
        print("  the guild must not link OUT: every other device sees a dead "
              "link. Fix: `ag port --apply` (moves the payload in, links the "
              "old path back into the guild).")
        problems += len(outbound)
    else:
        print("  ok — no links pointing outside the guild")

    print("\n== skills dir consolidation (advisory, not an error) ==")
    guild_resolved = (CENTRAL / "skills").resolve()
    consolidated = per_skill = 0
    for name, entry in local_agents.items():
        sr = entry_view(entry).get("skills_root")
        if not sr or sr == "platform-managed":
            continue
        d = Path(sr).expanduser()
        if is_link(d):
            try:
                if d.resolve() == guild_resolved:
                    consolidated += 1
                    continue
            except OSError:
                pass
        n = 0
        if d.is_dir():
            try:
                for child in d.iterdir():
                    if is_link(child):
                        try:
                            if child.resolve().parent == guild_resolved:
                                n += 1
                        except OSError:
                            pass
            except OSError:
                pass
        if n:
            per_skill += 1
            print(f"  ℹ [{name}] {n} per-skill link(s) into the guild — "
                  f"consolidate: `ag link-root {name} --apply`")
    if not per_skill:
        print("  ok — no per-skill link sprawl detected")
    print(f"  (dir-linked agents: {consolidated}, per-skill agents: {per_skill})")

    print("\n== core protocol files ==")
    required = [
        "registry.json", "ONBOARDING.md",
        "skills/agent-guild/SKILL.md", "skills/agent-guild/manifest.json",
        "identity/profile.md", "rules/universal.md",
    ]
    missing = [r for r in required if not (CENTRAL / r).is_file()]
    if missing:
        for r in missing:
            print(f"  ✗ missing: {r}")
        problems += len(missing)
    else:
        print("  ok — all present")

    bad_json = []
    for rel in ("registry.json", "skills/agent-guild/manifest.json"):
        p = CENTRAL / rel
        if p.is_file():
            try:
                json.loads(p.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError) as e:
                bad_json.append((rel, str(e)))
    if bad_json:
        for rel, e in bad_json:
            print(f"  ✗ unparseable JSON: {rel} ({e})")
        problems += len(bad_json)

    print(f"\n== registry drift (this device: {host_id()}) ==")
    drift = 0
    for name, entry in local_agents.items():
        v = entry_view(entry)
        home = v.get("home", "")
        # "platform-managed" is a sentinel (no real home dir), not a path
        if home and home != "platform-managed" and not Path(home).expanduser().exists():
            print(f"  ✗ [{name}] home does not exist: {home}")
            drift += 1
        sr = v.get("skills_root")
        if sr and sr != "platform-managed" and not Path(sr).expanduser().exists():
            print(f"  ✗ [{name}] skills_root does not exist: {sr}")
            drift += 1
    if not drift:
        print("  ok — none")
    problems += drift
    if remote_agents:
        print("  other devices (not checked here): " + ", ".join(
            f"{n} @ {', '.join(other_hosts(e))}" for n, e in remote_agents.items()))
    legacy_flat = [n for n, e in reg.get("agents", {}).items()
                   if not isinstance(e.get("hosts"), dict) or not e["hosts"]]
    if legacy_flat:
        print(f"  ℹ {len(legacy_flat)} entry(ies) still store device paths flat "
              f"— run `ag port --apply` to scope them per device")

    print(f"\n== protocol version drift (central={PROTOCOL_VERSION}) ==")
    stale_proto = []
    central_major = PROTOCOL_VERSION.split(".")[0]
    for name, entry in reg.get("agents", {}).items():
        pv = str(entry.get("protocol_version", "0"))
        if pv.split(".")[0] != central_major:
            stale_proto.append((name, pv))
    if stale_proto:
        for name, pv in stale_proto:
            print(f"  ✗ [{name}] joined under {pv} — MAJOR bump, must re-run ONBOARDING.md")
        problems += len(stale_proto)
    else:
        print("  ok — all agents on the current major version")

    print("\n== portability (multi-device readiness) ==")
    port_findings = _portability_findings()
    if port_findings:
        for f in port_findings:
            print(f"  ! {f}")
        print("  detail + mechanical fixes: `ag port` / `ag port --apply`")
    else:
        print("  ok — nothing device-specific leaking into shared files")

    print(f"\n{'=' * 60}")
    if problems:
        print(f"{problems} problem(s) found. Suggested fixes:")
        print("  broken links      → delete the link (never the target)")
        print("  outbound links    → `ag port --apply` (payload moves into the guild)")
        print("  missing files     → `ag init` refills gaps without touching data")
        print("  registry drift    → `ag register <agent> <home> <tier> <skills_root>`")
        print("  version drift     → re-run ONBOARDING.md, then re-register")
        return 1
    print("All checks passed.")
    return 0


# ------------------------------------------------------- portability audit ---

_SKIP_WALK = {".git", ".trash", "__pycache__", "node_modules", ".venv"}

# Paths that only exist on one machine: a home dir with a specific user name,
# or a Windows drive-rooted user profile.
_MACHINE_PATH_RE = re.compile(
    r"(?:/Users/|/home/|/root/)[A-Za-z0-9._-]+/"
    r"|[A-Za-z]:\\Users\\[A-Za-z0-9._-]+"
)

# Shared, user-owned text: statements here are supposed to hold on every
# device, so a machine path in them is a portability bug.
SHARED_LINT_DIRS = ("identity", "rules", "toolchain", "projects", "memory/shared")
SHARED_LINT_FILES = ("handoff/shared-state/current-focus.md",)

_WIN_EXT = {".ps1", ".bat", ".cmd"}
_POSIX_EXT = {".sh", ".command", ".zsh", ".bash"}


def _resolve_link(p: Path, raw: str) -> Path:
    try:
        base = Path(raw) if os.path.isabs(raw) else (p.parent / raw)
        return base.resolve()
    except OSError:
        return Path(raw)


def _inside_guild(path: Path) -> bool:
    try:
        central = CENTRAL.resolve()
    except OSError:
        return False
    return path == central or central in path.parents


def _walk_links():
    """Every link inside the guild, without descending through links."""
    for root, dirs, files in os.walk(CENTRAL, followlinks=False):
        rootp = Path(root)
        for name in list(dirs) + list(files):
            p = rootp / name
            if is_link(p):
                yield p, link_target(p)
        dirs[:] = [d for d in dirs
                   if d not in _SKIP_WALK and not is_link(rootp / d)]


def _outbound_links() -> list:
    """Links from the guild to an external path — the payload then exists on
    exactly one device and every other device sees a dead link."""
    return [(p, raw) for p, raw in _walk_links()
            if not _inside_guild(_resolve_link(p, raw))]


def _absolute_internal_links() -> list:
    """Links that stay inside the guild but store an absolute path: they break
    as soon as the user name, home dir, or drive letter differs."""
    return [(p, raw) for p, raw in _walk_links()
            if os.path.isabs(raw) and _inside_guild(_resolve_link(p, raw))]


def _machine_paths_in_shared(limit: int = 40) -> list:
    """(relpath, lineno, snippet) for machine paths written into shared text."""
    hits = []
    targets = []
    for rel in SHARED_LINT_DIRS:
        d = CENTRAL / rel
        if d.is_dir():
            targets += [p for p in sorted(d.rglob("*.md")) if p.is_file()]
    for rel in SHARED_LINT_FILES:
        p = CENTRAL / rel
        if p.is_file():
            targets.append(p)
    for p in targets:
        if "archive" in p.parts:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            m = _MACHINE_PATH_RE.search(line)
            if m:
                hits.append((str(p.relative_to(CENTRAL)), i, m.group(0)))
                if len(hits) >= limit:
                    return hits
    return hits


def _declared_platforms(skill_dir: Path) -> list:
    """`platforms` as declared by a skill (manifest.json or SKILL.md
    frontmatter). Empty list means "undeclared" = portable by default."""
    mf = skill_dir / "manifest.json"
    if mf.is_file():
        try:
            d = json.loads(mf.read_text(encoding="utf-8"))
            p = d.get("platforms")
            if isinstance(p, list) and p:
                return [str(x) for x in p]
        except (OSError, ValueError):
            pass
    sk = skill_dir / "SKILL.md"
    if sk.is_file():
        try:
            head = sk.read_text(encoding="utf-8", errors="ignore")[:2000]
        except OSError:
            return []
        m = re.search(r"^platforms:\s*\[?([^\]\n]+)\]?\s*$", head, re.M)
        if m:
            return [x.strip().strip("\"'") for x in m.group(1).split(",") if x.strip()]
    return []


def _skill_platform_hints() -> list:
    """Skills whose payload is clearly single-platform yet declare nothing."""
    out = []
    root = CENTRAL / "skills"
    if not root.is_dir():
        return out
    for d in sorted(root.iterdir()):
        if not d.is_dir() or d.name.startswith("."):
            continue
        if _declared_platforms(d):
            continue
        exts = set()
        for p in d.rglob("*"):
            if p.is_file() and not set(p.parts) & _SKIP_WALK:
                exts.add(p.suffix.lower())
        win, posix = exts & _WIN_EXT, exts & _POSIX_EXT
        if win and not posix:
            out.append((d.name, "windows"))
        elif posix and not win and (exts & {".command"}):
            out.append((d.name, "macos"))
    return out


def _legacy_host_state() -> list:
    """Pre-3.3 host state still sitting at the guild root."""
    out = []
    for new_name, legacy_name in _LEGACY_STATE.items():
        legacy = CENTRAL / legacy_name
        if legacy.exists() and not (host_dir() / new_name).exists():
            out.append((legacy, new_name))
    return out


def _portability_findings() -> list:
    """Short one-line findings, used by `ag doctor`."""
    out = []
    n = len(_outbound_links())
    if n:
        out.append(f"{n} link(s) point outside the guild (dead on other devices)")
    n = len(_absolute_internal_links())
    if n:
        out.append(f"{n} internal link(s) store an absolute path (not portable)")
    n = len(_legacy_host_state())
    if n:
        out.append(f"{n} host-scoped state file(s) still at the guild root")
    hits = _machine_paths_in_shared(limit=6)
    if hits:
        out.append("machine paths inside shared text: " + ", ".join(
            f"{f}:{i}" for f, i, _ in hits[:3])
            + (" ..." if len(hits) > 3 else ""))
    undeclared = [d for d in (CENTRAL / "tools").iterdir()
                  if d.is_dir() and not (d / TOOL_MANIFEST).is_file()
                  and not d.name.startswith(".")] if TOOLS.is_dir() else []
    if undeclared:
        out.append(f"{len(undeclared)} tool(s) without {TOOL_MANIFEST} "
                   f"(other devices cannot tell 'not for me' from 'missing')")
    return out


# ----------------------------------------------------------- platform tools ---

def _tool_index() -> dict:
    """slug -> {dir, manifest, declared} for everything under tools/."""
    idx = {}
    if not TOOLS.is_dir():
        return idx
    try:
        entries = sorted(TOOLS.iterdir())
    except OSError:
        return idx
    for d in entries:
        if not d.is_dir() or d.name.startswith("."):
            continue
        mf = d / TOOL_MANIFEST
        man = {}
        if mf.is_file():
            try:
                man = json.loads(mf.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                man = {}
        keys = {_slug(d.name)}
        if man.get("name"):
            keys.add(_slug(str(man["name"])))
        # `doxygen-1.18.0-official` should also answer to `doxygen`
        keys.add(_slug(d.name).split("-")[0])
        for k in keys:
            if k:
                idx.setdefault(k, {"dir": d, "manifest": man,
                                   "declared": mf.is_file()})
    return idx


def _discover_exec(d: Path) -> Path | None:
    """Best-guess executable inside a tool dir (used to seed a manifest)."""
    want = _slug(d.name).split("-")[0]
    cands = []
    for root, dirs, files in os.walk(d):
        dirs[:] = [x for x in dirs if x not in _SKIP_WALK and not x.startswith(".")]
        for f in files:
            p = Path(root) / f
            if p.suffix.lower() in (".json", ".md", ".txt", ".cfg", ".yml",
                                    ".yaml", ".plist", ".dylib", ".so"):
                continue
            if p.is_symlink():
                continue
            if os.name == "nt":
                ok = p.suffix.lower() in (".exe", ".bat", ".cmd", ".ps1")
            else:
                ok = os.access(p, os.X_OK)
            if ok:
                cands.append(p)
    if not cands:
        return None
    cands.sort(key=lambda p: (0 if _slug(p.stem) == want else 1,
                              len(p.parts), len(p.name)))
    return cands[0]


def resolve_tool(name: str) -> dict:
    """Where is `name` runnable on THIS device?

    Order: manifest entry for <os>-<arch> -> manifest entry for <os> ->
    manifest `any` -> PATH. An honest "unavailable + how to install here" beats
    a path that only exists on one machine.
    """
    tag, osx = platform_tag(), detect_os()
    out = {"name": name, "status": "unavailable", "path": "", "how": "",
           "hint": "", "install": "", "declared": []}
    entry = _tool_index().get(_slug(name))
    if entry is None:
        w = shutil.which(name)
        if w:
            out.update(status="ok", path=w, how="PATH (undeclared tool)")
        else:
            out["hint"] = (f"no tools/*/{TOOL_MANIFEST} declares '{name}' and it "
                           f"is not on PATH")
        return out

    d, man = entry["dir"], entry["manifest"]
    plats = man.get("platforms") or {}
    out["declared"] = sorted(plats)
    for key in (tag, osx):
        spec = plats.get(key)
        if not isinstance(spec, dict):
            continue
        rel = spec.get("exec")
        if rel:
            p = d / rel
            if p.exists():
                out.update(status="ok", path=str(p), how=f"declared:{key}")
                return out
            out["hint"] = f"declared for {key} but the file is missing: {p}"
        on_path = spec.get("exec_on_path")
        if on_path:
            w = shutil.which(on_path)
            if w:
                out.update(status="ok", path=w, how=f"PATH:{key}")
                return out
    anyspec = man.get("any") if isinstance(man.get("any"), dict) else {}
    on_path = anyspec.get("exec_on_path") or man.get("exec_on_path")
    if on_path:
        w = shutil.which(on_path)
        if w:
            out.update(status="ok", path=w, how="PATH:any")
            return out
    w = shutil.which(str(man.get("name") or name))
    if w:
        out.update(status="ok", path=w, how="PATH")
        return out

    for key in (tag, osx):
        spec = plats.get(key)
        if isinstance(spec, dict) and spec.get("install"):
            out["install"] = str(spec["install"])
            break
    out["install"] = out["install"] or str(anyspec.get("install") or man.get("install") or "")
    if not out["hint"]:
        declared = ", ".join(out["declared"]) or "none"
        out["hint"] = (f"not available on {tag} (declared platforms: {declared})")
    return out


def cmd_tool(args: list) -> int:
    """Print the executable path for this device. Exit 3 when unavailable, so
    a caller can branch instead of running a path that does not exist."""
    rest = [a for a in args if not a.startswith("-")]
    if not rest:
        print("usage: ag tool <name> [--json]", file=sys.stderr)
        return 2
    info = resolve_tool(rest[0])
    if "--json" in args:
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return 0 if info["status"] == "ok" else 3
    if info["status"] == "ok":
        print(info["path"])
        return 0
    print(f"{info['name']}: {info['hint']}", file=sys.stderr)
    if info["install"]:
        print(f"install on {platform_tag()}: {info['install']}", file=sys.stderr)
    return 3


def cmd_tools(args: list) -> int:
    idx = _tool_index()
    if not idx:
        print(f"no tools under {TOOLS}")
        return 0
    seen, rows = set(), []
    for key, e in sorted(idx.items()):
        d = e["dir"]
        if d in seen:
            continue
        seen.add(d)
        info = resolve_tool(key)
        rows.append((d.name, info, e["declared"]))
    print(f"platform: {platform_tag()}   (tools/ declared for this device)")
    print(f"{'tool':<32} {'status':<12} resolved / hint")
    print("-" * 78)
    for name, info, declared in rows:
        status = "ok" if info["status"] == "ok" else "unavailable"
        detail = info["path"] if info["status"] == "ok" else info["hint"]
        if not declared:
            status = status + "*"
        print(f"{name:<32} {status:<12} {detail}")
    if any(not d for _, _, d in rows):
        print(f"\n* no {TOOL_MANIFEST} — run `ag port --apply` to declare this "
              f"device's platform for it")
    print("\nusage in scripts:  BIN=$(ag tool <name>) || handle-unavailable")
    return 0


# ------------------------------------------------------------ ag platform ---

def cmd_platform(args: list) -> int:
    facts = platform_facts()
    if "--json" in args:
        print(json.dumps(facts, ensure_ascii=False, indent=2))
        return 0
    print(f"host-id   : {facts['host_id']}")
    print(f"platform  : {facts['platform']}  (os={facts['os']}, arch={facts['arch']})")
    print(f"links     : {facts['links']}")
    print(f"python    : {facts['python']} ({facts['python_version']})")
    print(f"guild     : {facts['central']}")
    print(f"host state: hosts/{facts['host_id']}/")
    others = [h for h in facts["known_hosts"] if h != facts["host_id"]]
    print(f"other devices: {', '.join(others) if others else '(none seen yet)'}")
    print("\nscope rules:")
    print("  shared   — true everywhere            -> normal guild paths")
    print("  platform — one os+arch                -> tools/<t>/tool.json, ag tool <t>")
    print(f"  host     — this device only           -> hosts/{facts['host_id']}/")
    return 0


# ---------------------------------------------------------------- ag port ---

def _internalize(link: Path, raw: str) -> str:
    """Turn an outbound link into guild-owned payload.

    The guild owns its payloads; other devices must find the real files here.
    So: drop the link, move the external target in, then link the old external
    path back INTO the guild (inbound links are the portable direction).
    """
    target = _resolve_link(link, raw)
    if not target.exists():
        return (f"dangling outbound link left untouched: "
                f"{link.relative_to(CENTRAL)} -> {raw} (target missing)")
    if not drop_link(link):
        return f"could not drop link {link} — skipped"
    try:
        shutil.move(str(target), str(link))
    except OSError as e:
        make_link(link, target)  # restore, never leave the guild worse off
        return f"move failed for {link.name}: {e}"
    ok, how = make_link(target, link)
    back = f", old path linked back ({how})" if ok else \
           f", old path NOT recreated ({how}) — payload now lives only in the guild"
    audit("port_internalize", {"path": str(link), "from": str(target)})
    return f"internalized {link.relative_to(CENTRAL)} <- {target}{back}"


def _relativize(link: Path, raw: str) -> str:
    """Rewrite an absolute intra-guild link as a relative one.

    The relative path is computed against the guild's own (unresolved) layout,
    so it stays short and inside the guild even when the guild itself sits
    behind a symlinked mount point.
    """
    target = _resolve_link(link, raw)
    try:
        inside = CENTRAL / target.relative_to(CENTRAL.resolve())
    except ValueError:
        inside = target
    try:
        rel = os.path.relpath(str(inside), str(link.parent))
    except ValueError as e:
        return f"cannot relativize {link.name}: {e}"
    if not drop_link(link):
        return f"could not drop link {link} — skipped"
    ok, how = make_link(link, Path(rel))
    if not ok:
        make_link(link, target)
        return f"relativize failed for {link.name} ({how}) — absolute link restored"
    audit("port_relativize", {"path": str(link), "target": rel})
    return f"{link.relative_to(CENTRAL)} -> {rel} (relative, portable)"


def _seed_tool_manifest(d: Path) -> str:
    """Declare the CURRENT device's platform for an undeclared tool.

    Nothing is moved: a tool's internals often depend on their own layout.
    Declaring is enough — another device then gets an honest "not available
    here" plus an install hint instead of a broken path.
    """
    exe = _discover_exec(d)
    tag = platform_tag()
    name = _slug(d.name).split("-")[0] or _slug(d.name)
    man = {
        "name": name,
        "description": f"{name} — declared per platform; resolve with `ag tool {name}`",
        "platforms": {},
        "any": {"exec_on_path": name},
    }
    if exe:
        man["platforms"][tag] = {"exec": str(exe.relative_to(d))}
    (d / TOOL_MANIFEST).write_text(
        json.dumps(man, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    audit("port_declare_tool", {"tool": d.name, "platform": tag})
    return (f"{d.name}/{TOOL_MANIFEST} created "
            + (f"({tag} -> {exe.relative_to(d)})" if exe
               else f"(no executable found; only PATH fallback declared)"))


def cmd_port(args: list) -> int:
    """Portability audit for a guild shared by several devices.

    Default is a DRY-RUN report. `--apply` performs only the mechanical,
    reversible fixes; user-written text is never rewritten automatically.
    """
    if not CENTRAL.exists():
        print(f"{CENTRAL} missing — run `ag init` first", file=sys.stderr)
        return 1
    apply_ = "--apply" in args
    hid = host_id()
    did, todo = [], []

    print(f"== this device ==")
    print(f"  host-id  : {hid}")
    print(f"  platform : {platform_tag()}   links: {link_capability()}")
    others = [h for h in known_hosts() if h != hid]
    print(f"  others   : {', '.join(others) if others else '(none seen yet)'}")

    print("\n== host-scoped state ==")
    legacy = _legacy_host_state()
    if not legacy:
        print(f"  ok — already under hosts/{hid}/")
    for src, new_name in legacy:
        if apply_:
            dest = host_dir(create=True) / new_name
            try:
                shutil.move(str(src), str(dest))
                did.append(f"moved {src.name} -> hosts/{hid}/{new_name}")
            except OSError as e:
                todo.append(f"could not move {src.name}: {e}")
        else:
            todo.append(f"move {src.name} -> hosts/{hid}/{new_name}")

    print("\n== registry scoping ==")
    changed = []
    with _append_lock(REGISTRY) if apply_ else nullcontext():
        reg = load_registry()
        for name, entry in reg.get("agents", {}).items():
            hosts = entry.get("hosts")
            if isinstance(hosts, dict) and hosts:
                continue
            if apply_:
                if fold_entry_to_host(entry, hid):
                    changed.append(name)
            else:
                todo.append(f"fold device paths of '{name}' into hosts.{hid}")
        if apply_ and changed:
            reg["protocol_version"] = PROTOCOL_VERSION
            save_registry(reg, "port", "port_registry")
            did.append(f"scoped {len(changed)} registry entry(ies) to {hid}: "
                       + ", ".join(changed))
    if not changed and not any(t.startswith("fold ") for t in todo):
        print("  ok — every entry is already device-scoped")

    print("\n== link direction (guild owns payloads, links point inward) ==")
    outbound = _outbound_links()
    if not outbound:
        print("  ok — no outbound links")
    for p, raw in outbound:
        if apply_:
            did.append(_internalize(p, raw))
        else:
            todo.append(f"internalize {p.relative_to(CENTRAL)} -> {raw} "
                        f"(move payload in, link the old path back)")
    absolute = _absolute_internal_links()
    if not absolute:
        print("  ok — no absolute intra-guild links")
    for p, raw in absolute:
        if apply_:
            did.append(_relativize(p, raw))
        else:
            todo.append(f"relativize {p.relative_to(CENTRAL)} -> {raw}")

    print("\n== platform tools ==")
    undeclared = []
    if TOOLS.is_dir():
        for d in sorted(TOOLS.iterdir()):
            if d.is_dir() and not d.name.startswith(".") \
                    and not (d / TOOL_MANIFEST).is_file():
                undeclared.append(d)
    if not undeclared:
        print(f"  ok — every tool declares its platforms ({TOOL_MANIFEST})")
    for d in undeclared:
        if apply_:
            did.append(_seed_tool_manifest(d))
        else:
            todo.append(f"declare platforms for tools/{d.name} "
                        f"({TOOL_MANIFEST})")
    print(f"  recommended layout for multi-platform payloads: "
          f"tools/<name>/bin/<os>-<arch>/…")

    print("\n== shared text vs machine paths (report only) ==")
    hits = _machine_paths_in_shared()
    if not hits:
        print("  ok — no machine paths in shared files")
    for f, i, snippet in hits:
        print(f"  ! {f}:{i}  {snippet}")
    if hits:
        print(f"  fix by hand: use ~ / a placeholder, or move the fact to "
              f"hosts/{hid}/{HOST_NOTES}")

    print("\n== single-platform skills without a declaration (report only) ==")
    hints = _skill_platform_hints()
    if not hints:
        print("  ok — nothing obviously platform-locked is undeclared")
    for name, guess in hints:
        print(f"  ! skills/{name}: payload looks {guess}-only — add "
              f"\"platforms\": [\"{guess}\"] to its manifest")

    print(f"\n{'=' * 60}")
    if apply_:
        for d in did:
            print(f"  ✓ {d}")
        for t in todo:
            print(f"  ! {t}")
        print(f"\napplied {len(did)} fix(es)."
              + (f" {len(todo)} need a human." if todo else ""))
    else:
        for t in todo:
            print(f"  → {t}")
        print(f"\n{len(todo)} mechanical fix(es) available — run "
              f"`ag port --apply`." if todo else
              "\nnothing mechanical to fix.")
    return 0


# ------------------------------------------------------- existing commands ---

def cmd_status(args=None) -> int:
    data = load_registry()
    agents = data.get("agents", {})
    if not agents:
        print("No agents registered.")
        return 0
    show_all = bool(args) and "--all" in args
    hid = host_id()
    print(f"this device: {hid}")
    print(f"{'agent':<12} {'tier':<14} {'last_seen'}")
    print("-" * 60)
    elsewhere = []
    for name, e in sorted(agents.items()):
        if not show_all and not registered_here(e):
            elsewhere.append((name, other_hosts(e)))
            continue
        v = entry_view(e)
        here = registered_here(e)
        tier = v.get("install_tier", "?") if here else "(other device)"
        print(f"{name:<12} {tier:<14} {v.get('last_seen','?') if here else ''}")
        if show_all:
            for h in other_hosts(e):
                b = host_block(e, h)
                print(f"  └ on {h}: tier={b.get('install_tier','?')} "
                      f"last_seen={b.get('last_seen','?')}")
    for name, hosts in elsewhere:
        print(f"{name:<12} {'(other device)':<14} {', '.join(hosts)}")
    if elsewhere and not show_all:
        print("\n(entries marked (other device) are installed on another "
              "machine — `ag status --all` for details)")
    return 0


def cmd_register(args: list) -> int:
    if len(args) < 3:
        print("usage: ag register <agent> <home> <tier> [skills_root] [capabilities...]", file=sys.stderr)
        return 2
    name, home, tier = args[0], args[1], args[2]
    skills_root = args[3] if len(args) > 3 else None
    caps = args[4:] or ["read_files", "write_files"]
    hid = host_id()
    stamp = now_iso()
    with _append_lock(REGISTRY):
        data = load_registry()
        data.setdefault("agents", {})
        entry = data["agents"].get(name, {})
        entry.update(
            joined_at=entry.get("joined_at", stamp),
            protocol_version=PROTOCOL_VERSION,
            capabilities=caps,
        )
        # device-scoped facts
        block = dict(host_block(entry, hid))
        block.update(home=home, skills_root=skills_root,
                     install_tier=tier, last_seen=stamp)
        entry.setdefault("hosts", {})[hid] = block
        # compat mirror for pre-3.3 readers on this same device
        entry.update(home=home, skills_root=skills_root, install_tier=tier,
                     last_seen=stamp, mirror_host=hid)
        data["agents"][name] = entry
        save_registry(data, name, "register")
    print(f"registered {name} (tier={tier}, protocol={PROTOCOL_VERSION}, host={hid})")
    return 0


def cmd_last_seen(args: list) -> int:
    if len(args) < 1:
        print("usage: ag last-seen <agent>", file=sys.stderr)
        return 2
    name = args[0]
    if not _touch_last_seen(name):
        print(f"agent '{name}' not registered — run: ag register {name} <home> <tier>", file=sys.stderr)
        return 1
    print(f"{name} last_seen updated (host={host_id()})")
    return 0


def cmd_send(args: list) -> int:
    if len(args) < 2:
        print("usage: ag send <dst> <topic>  (message body from stdin)", file=sys.stderr)
        return 2
    dst, topic = args[0], args[1]
    body = read_stdin()
    if not body:
        print("empty message body", file=sys.stderr)
        return 2
    src = os.environ.get("AG_AGENT") or "unknown"
    if not all(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value) for value in (src, dst)):
        print("sender and recipient must be lowercase agent identifiers", file=sys.stderr)
        return 2
    safe_topic = re.sub(r"[^A-Za-z0-9._-]", "-", topic)[:100]
    fname = f"from-{src}-to-{dst}-{safe_topic}.md"
    atomic_append(INBOX / fname, body)
    audit("send", {"from": src, "to": dst, "file": f"messages/inbox/{fname}"})
    print(f"sent to {dst}: {fname}")
    return 0


def cmd_log(args: list) -> int:
    if len(args) < 2:
        print("usage: ag log <agent> <title>  (body from stdin)", file=sys.stderr)
        return 2
    agent, title = args[0], args[1]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", agent):
        print("invalid agent identifier", file=sys.stderr)
        return 2
    body = read_stdin()
    if not body:
        print("empty log body", file=sys.stderr)
        return 2
    path = _daily_log_path(agent)
    atomic_append(path, f"\n## {title}\n\n{body}")
    print(f"appended to log/daily/{path.name}")
    return 0


def cmd_focus(args: list) -> int:
    print("Global focus writes are retired. Use `ag task create` or "
          "`ag task checkpoint` for the selected task; legacy data is untouched.",
          file=sys.stderr)
    return 2


def cmd_task(args: list) -> int:
    import ag_tasks
    return ag_tasks.run(args, sys.modules[__name__])


def cmd_history(args: list) -> int:
    import ag_history
    return ag_history.run(args, sys.modules[__name__])


def _history_maintenance() -> None:
    import ag_history
    try:
        result = ag_history.maintenance(sys.modules[__name__])
        if result.get("checked"):
            print("History maintenance checked; request `ag history status` "
                  "or `ag history plan` for details. No task context loaded.")
    except (OSError, ValueError, RuntimeError):
        # Paths and task metadata in an exception may belong to other work.
        print("History maintenance blocked; request `ag history status` for details.",
              file=sys.stderr)


def cmd_inbox(args: list) -> int:
    agent = default_agent(args)
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", agent):
        print("invalid agent name", file=sys.stderr)
        return 2
    print(json.dumps({"agent": agent, "messages": [
        str(p.relative_to(CENTRAL)) for p in _inbox_messages(agent)
    ]}, ensure_ascii=False, indent=2))
    return 0


def cmd_migrate(args: list) -> int:
    """Read-only, explicit v3 inventory. Never guesses tasks from old logs."""
    if args not in ([], ["--dry-run"]):
        print("Migration is preview-only. Review and back up the listed files "
              "before authorizing a separate migration.", file=sys.stderr)
        return 2
    rows = []
    for old, new in (("handoff/inbox", "messages/inbox"),
                     ("handoff/archive", "messages/archive")):
        base = CENTRAL / old
        if base.is_symlink():
            print(f"refusing linked legacy directory: {old}", file=sys.stderr)
            return 1
        if not base.is_dir():
            continue
        for p in sorted(base.iterdir()):
            # Task directories in the new archive are never legacy messages.
            if p.suffix != ".md" or p.name.startswith("."):
                continue
            if p.is_symlink() or not p.is_file():
                print(f"refusing non-regular legacy file: {p.name}", file=sys.stderr)
                return 1
            rows.append({"source": str(p.relative_to(CENTRAL)),
                         "destination": f"{new}/{p.name}", "bytes": p.stat().st_size,
                         "destination_exists": (CENTRAL / new / p.name).exists()})
    focus = CENTRAL / "handoff/shared-state"
    print(json.dumps({"mode": "preview", "files": rows,
                      "legacy_focus_present": focus.exists(),
                      "focus_policy": "retain as historical evidence; never infer active tasks",
                      "mutated": False}, ensure_ascii=False, indent=2))
    return 0


# --------------------------------------------------------------- learnings ---

# Entry header pattern: "## [LRN-20260818-003] category"
_ENTRY_RE = re.compile(r"^## \[((?:LRN|ERR|FEAT)-\d{8}-[A-Za-z0-9]{3})\]\s*(.*)$", re.M)


def _ledger_files() -> list:
    return [CENTRAL / rel for rel, _ in LEDGERS.values()]


def _parse_entries(text: str) -> list:
    """Split a ledger file into structured entries (id, category, block)."""
    out = []
    matches = list(_ENTRY_RE.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[m.start():end]
        out.append({"id": m.group(1), "category": m.group(2).strip(), "block": block})
    return out


def _field(entry: dict, name: str) -> str:
    m = re.search(rf"^\*\*{re.escape(name)}\*\*:\s*(.+)$", entry["block"], re.M)
    return m.group(1).strip() if m else ""


def _summary_of(entry: dict) -> str:
    m = re.search(r"^### Summary\s*\n+\s*(.+)$", entry["block"], re.M)
    return m.group(1).strip() if m else "(no summary)"


def _next_id(path: Path, prefix: str) -> str:
    day = datetime.now().strftime("%Y%m%d")
    used = set()
    if path.exists():
        for e in _parse_entries(path.read_text(encoding="utf-8")):
            if e["id"].startswith(f"{prefix}-{day}-"):
                used.add(e["id"].rsplit("-", 1)[-1])
    n = 1
    while f"{n:03d}" in used:
        n += 1
    return f"{prefix}-{day}-{n:03d}"


def _opt(args: list, name: str, default: str = "") -> str:
    """Extract --name VALUE from args (and remove both from the list)."""
    if name in args:
        i = args.index(name)
        if i + 1 < len(args):
            val = args[i + 1]
            del args[i:i + 2]
            return val
        args.remove(name)
    return default


def cmd_learn(args: list) -> int:
    """Append a structured entry to a learning ledger (details from stdin)."""
    area = _opt(args, "--area", "")
    priority = _opt(args, "--priority", "medium")
    category = _opt(args, "--category", "")
    pattern_key = _opt(args, "--pattern-key", "")
    rest = [a for a in args if not a.startswith("-")]
    if len(rest) < 3:
        print('usage: ag learn <agent> <learning|error|featreq> "<summary>" '
              "[--area A] [--priority low|medium|high|critical] "
              "[--category C] [--pattern-key K]  (details from stdin)",
              file=sys.stderr)
        return 2
    agent, kind, summary = rest[0], rest[1].lower(), rest[2]
    kind = LEDGER_ALIASES.get(kind, kind)
    if kind not in LEDGERS:
        print(f"unknown kind '{kind}' — use learning | error | featreq", file=sys.stderr)
        return 2
    if not CENTRAL.exists():
        print(f"{CENTRAL} missing — run `ag init` first", file=sys.stderr)
        return 1

    body = read_stdin() or "(no details provided)"
    if kind == "error":
        detail = f"### Error\n```\n{body}\n```"
    elif kind == "featreq":
        detail = f"### Requested Capability\n{summary}\n\n### User Context\n{body}"
    else:
        detail = f"### Details\n{body}"
        if not category:
            category = "insight"

    if kind == "learning":
        heading_cat = category or "insight"
    elif kind == "error":
        heading_cat = category or "error"
    else:
        heading_cat = category or "request"
    rel, prefix = LEDGERS[kind]
    path = CENTRAL / rel
    with _append_lock(path):
        if not path.exists():  # older central dir — back-fill header
            _atomic_write_text(path, PLACEHOLDERS.get(rel, "# ledger\n\n---\n"))

        # Allocate the ID from the same snapshot that this append updates.
        # Locking only the final append allows concurrent callers to reuse it.
        entry_id = _next_id(path, prefix)
        see_also = ""
        if pattern_key:
            prior = [e["id"] for e in _parse_entries(path.read_text(encoding="utf-8"))
                     if re.search(rf"Pattern-Key:\s*{re.escape(pattern_key)}\s*$",
                                  e["block"], re.M)]
            if prior:
                see_also = ", ".join(prior)
                print(f"recurrence: Pattern-Key '{pattern_key}' seen in {see_also} "
                      f"— linking via See Also; promotion threshold may now be met (ag review).")

        meta = ["- Source: conversation", "- Related Files: ", "- Tags: "]
        if see_also:
            meta.append(f"- See Also: {see_also}")
        if pattern_key:
            meta.append(f"- Pattern-Key: {pattern_key}")
        entry = (
            f"\n## [{entry_id}] {heading_cat}\n\n"
            f"**Logged**: {now_iso()}\n"
            f"**By**: {agent}\n"
            f"**Host**: {host_id()}\n"
            f"**Priority**: {priority}\n"
            f"**Status**: pending\n"
            f"**Area**: {area or 'unspecified'}\n\n"
            f"### Summary\n{summary}\n\n"
            f"{detail}\n\n"
            f"### Suggested Action\n(none yet)\n\n"
            f"### Metadata\n" + "\n".join(meta) + "\n\n---\n"
        )
        _append_unlocked(path, entry)
    audit("learn", {"agent": agent, "id": entry_id, "kind": kind,
                    "pattern_key": pattern_key or None})
    print(f"logged {entry_id} -> {rel} (by {agent}, priority={priority})")
    print("next: fix it later with `ag resolve " + entry_id + "`, "
          "or distill recurring ones via `ag review`.")
    return 0


def cmd_resolve(args: list) -> int:
    """Set an entry's Status to resolved + append a Resolution block."""
    if not args:
        print("usage: ag resolve <ENTRY-ID> [note ...]", file=sys.stderr)
        return 2
    entry_id = args[0].strip("[]")
    note = " ".join(args[1:]).strip() or "resolved"
    agent = os.environ.get("AG_AGENT") or "unknown"

    for path in _ledger_files():
        with _append_lock(path):
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            entries = _parse_entries(text)
            for e in entries:
                if e["id"] != entry_id:
                    continue
                block = e["block"]
                if "**Status**: resolved" in block:
                    print(f"{entry_id} is already resolved")
                    return 0
                new_block, n = re.subn(r"^\*\*Status\*\*:\s*\S+",
                                       "**Status**: resolved", block, count=1, flags=re.M)
                if n == 0:
                    new_block = block.replace("### Summary",
                                              "**Status**: resolved\n\n### Summary", 1)
                new_block = new_block.rstrip("\n") + (
                    f"\n\n### Resolution\n- **Resolved**: {now_iso()}\n"
                    f"- **By**: {agent}\n- **Notes**: {note}\n\n---\n")
                new_text = text.replace(block, new_block, 1)
                _atomic_write_text(path, new_text)
                audit("resolve", {"agent": agent, "id": entry_id})
                print(f"resolved {entry_id} in {path.relative_to(CENTRAL)}")
                return 0
    print(f"entry '{entry_id}' not found in any ledger "
          f"(searched learnings/*.md)", file=sys.stderr)
    return 1


def cmd_review(args: list) -> int:
    """Ledger overview: pending stats, high-priority items, promotion candidates."""
    any_file = False
    for path in _ledger_files():
        if not path.exists():
            continue
        any_file = True
        entries = _parse_entries(path.read_text(encoding="utf-8"))
        if not entries:
            continue
        open_items = [e for e in entries
                      if _field(e, "Status") in ("", "pending", "in_progress")]
        print(f"== {path.relative_to(CENTRAL)} — {len(entries)} entries, "
              f"{len(open_items)} open ==")
        hot = [e for e in open_items if _field(e, "Priority") in ("high", "critical")]
        for e in hot:
            print(f"  [{_field(e, 'Priority'):<8}] {e['id']}  {_summary_of(e)}"
                  f"  (by {_field(e, 'By') or '?'})")
        if not hot and open_items:
            print(f"  ({len(open_items)} open, none high/critical)")
        if not open_items:
            print("  (all resolved/promoted)")

        # Pattern-Key recurrence groups -> promotion candidates
        groups = {}
        for e in entries:
            m = re.search(r"^- Pattern-Key:\s*(\S+)\s*$", e["block"], re.M)
            if m:
                groups.setdefault(m.group(1), []).append(e)
        for key, es in sorted(groups.items()):
            hits, agents = len(es), {_field(e, "By") for e in es}
            if hits >= 3 or (hits >= 2 and len(agents) >= 2):
                print(f"  PROMOTION CANDIDATE: Pattern-Key '{key}' — "
                      f"{hits} hits by {len(agents)} agents "
                      f"({', '.join(sorted(a or '?' for a in agents))})")
                print(f"    -> distill into rules/ / toolchain/ / memory/shared/, "
                      f"or extract a skill onto skills/ (references/LEARNINGS.md)")
        print()

    if not any_file:
        print("no ledgers found — run `ag init` to create learnings/")
        return 1
    return 0


# ------------------------------------------------------------------ groom ---

def _parse_iso(s: str):
    """Lenient ISO-8601 parser -> aware datetime (or None)."""
    try:
        t = datetime.fromisoformat(str(s).strip().replace("Z", "+00:00"))
        if t.tzinfo is None:
            t = t.replace(tzinfo=timezone.utc)
        return t
    except (ValueError, TypeError):
        return None


def load_retention() -> dict:
    """RETENTION.md `key = value` lines override the defaults. Missing keys,
    a missing file, or unparseable values fall back silently."""
    out = dict(RETENTION_DEFAULTS)
    if not RETENTION.is_file():
        return out
    for line in RETENTION.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k, v = k.strip(), v.strip().split("#", 1)[0].strip()
        if k in out:
            try:
                out[k] = int(v)
            except ValueError:
                pass
    return out


# current-focus blocks are opened by an `ag focus`-style marker line.
# The timestamp is captured leniently up to " by <agent>": agents have been
# observed writing "2026-08-03 11:47" (space, no tz) instead of strict ISO.
_FOCUS_TS_RE = re.compile(r"^> Last updated: (.+?) by \S+(?:\s+@\S+)?\s*$", re.M)
_FOCUS_SEP = "\n---\n"


def _split_focus(text: str):
    """Split current-focus.md into (header, blocks). Each block carries a
    'Last updated:' marker (ag focus style) plus any hand-written fragment
    that trails it before the next marker. Fragments without their own
    marker are never rotated — they always stay in the live file."""
    matches = list(_FOCUS_TS_RE.finditer(text))
    if not matches:
        return text, []
    header = text[:matches[0].start()]
    blocks = []
    for i, m in enumerate(matches):
        seg_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        seg = text[m.start():seg_end]
        sep = seg.find(_FOCUS_SEP)
        if sep != -1:
            end = sep + len(_FOCUS_SEP)
            blocks.append({"ts": _parse_iso(m.group(1)), "text": seg[:end], "tail": seg[end:]})
        else:
            blocks.append({"ts": _parse_iso(m.group(1)), "text": seg, "tail": ""})
    return header, blocks


def _atomic_write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".ag-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(body)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def _groom(cfg: dict, dry_run: bool = False):
    """Detect + fix data degradation. Returns (actions, notes).
    Actions mutate (archive / trash — never delete); notes are report-only."""
    now = datetime.now(timezone.utc)
    acts, notes = [], []

    # -- 1. rotate old daily logs -> log/archive/ --------------------------
    log_archive = CENTRAL / "log" / "archive"
    rotated = []
    if DAILY.is_dir():
        for f in sorted(DAILY.iterdir()):
            m = re.match(r"^(\d{4}-\d{2}-\d{2})-", f.name)
            if not f.is_file() or not m:
                continue
            d = _parse_iso(m.group(1))
            if d and (now - d).days > cfg["daily_log_days"]:
                rotated.append(f)
    if rotated:
        span = f"({rotated[0].name[:10]} .. {rotated[-1].name[:10]})"
        if dry_run:
            acts.append(f"would rotate {len(rotated)} daily log(s) -> log/archive/ {span}")
        else:
            log_archive.mkdir(parents=True, exist_ok=True)
            for f in rotated:
                dest = log_archive / f.name
                if dest.exists():
                    dest = log_archive / f"{f.stem}-{now:%Y%m%d%H%M%S}{f.suffix}"
                shutil.move(str(f), str(dest))
            acts.append(f"rotated {len(rotated)} daily log(s) -> log/archive/ {span}")

    # -- 2. rotate stale current-focus blocks -> shared-state/archive/ -----
    if FOCUS.is_file():
        with _append_lock(FOCUS) if not dry_run else nullcontext():
            text = FOCUS.read_text(encoding="utf-8")
            header, blocks = _split_focus(text)
            cutoff = now.timestamp() - cfg["focus_days"] * 86400
            keep_idx, drop_idx = [], []
            for i, b in enumerate(blocks):
                if b["ts"] and b["ts"].timestamp() < cutoff:
                    drop_idx.append(i)
                else:
                    keep_idx.append(i)
            # count cap: beyond focus_blocks live blocks, rotate the OLDEST
            # timestamped ones (tail of the list); timestamp-less blocks never move
            if len(keep_idx) > cfg["focus_blocks"]:
                excess = len(keep_idx) - cfg["focus_blocks"]
                moved = []
                for i in reversed(keep_idx):
                    if excess <= 0:
                        break
                    if blocks[i]["ts"]:
                        moved.append(i)
                        excess -= 1
                if moved:
                    drop_idx += moved
                    drop_idx.sort()
                    moved_set = set(moved)
                    keep_idx = [i for i in keep_idx if i not in moved_set]
            if drop_idx:
                bucket = (CENTRAL / "handoff" / "shared-state" / "archive"
                          / f"current-focus-{now:%Y-%m}.md")
                drop_set = set(drop_idx)
                arch_body = "".join(blocks[i]["text"] for i in drop_idx)
                kept_text = header
                for i, b in enumerate(blocks):
                    if i in drop_set:
                        kept_text += b.get("tail", "")  # hand-written tail stays live
                    else:
                        kept_text += b["text"] + b.get("tail", "")
                span = f"({len(keep_idx)} kept)"
                if dry_run:
                    acts.append(f"would archive {len(drop_idx)} focus block(s) -> "
                                f"shared-state/archive/ {span}")
                else:
                    atomic_append(bucket, arch_body)
                    _atomic_write_text(FOCUS, kept_text)
                    acts.append(f"archived {len(drop_idx)} focus block(s) -> "
                                f"handoff/shared-state/archive/current-focus-{now:%Y-%m}.md {span}")

    # -- 3. compact resolved ledger entries -> learnings/archive/ ----------
    for path in _ledger_files():
        with _append_lock(path) if not dry_run else nullcontext():
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            entries = _parse_entries(text)
            if not entries:
                continue
            keep_e, drop_e = [], []
            for e in entries:
                st = _field(e, "Status")
                logged = _parse_iso(_field(e, "Logged"))
                if (st in ("resolved", "wont_fix", "promoted", "promoted_to_skill")
                        and logged and (now - logged).days > cfg["ledger_resolved_days"]):
                    drop_e.append(e)
                else:
                    keep_e.append(e)
            if drop_e:
                if dry_run:
                    acts.append(f"would compact {len(drop_e)} resolved entrie(s) "
                                f"from {path.name} -> learnings/archive/")
                else:
                    arcdir = LEARNINGS / "archive"
                    arcdir.mkdir(parents=True, exist_ok=True)
                    atomic_append(arcdir / path.name,
                                  "\n".join(e["block"].rstrip("\n") for e in drop_e) + "\n")
                    first = _ENTRY_RE.search(text)
                    prefix = text[:first.start()] if first else text
                    _atomic_write_text(path, prefix + "".join(e["block"] for e in keep_e))
                    acts.append(f"compacted {len(drop_e)} resolved entrie(s) from "
                                f"{path.name} -> learnings/archive/{path.name} "
                                f"({len(keep_e)} live)")

    # -- 4. rotate the audit trail ------------------------------------------
    if AUDIT.exists():
        with _append_lock(AUDIT) if not dry_run else nullcontext():
            lines = [l for l in AUDIT.read_text(encoding="utf-8").splitlines() if l.strip()]
            if len(lines) > cfg["audit_max_lines"]:
                keep_n = min(cfg["audit_keep_lines"], len(lines) - 1)
                head, tail = lines[:-keep_n] if keep_n else lines, lines[-keep_n:] if keep_n else []
                if head:
                    if dry_run:
                        acts.append(f"would rotate audit.jsonl: {len(head)} old line(s) -> log/archive/")
                    else:
                        log_archive.mkdir(parents=True, exist_ok=True)
                        stem = f"audit-{now:%Y%m%d-%H%M%S}"
                        dest = log_archive / f"{stem}.jsonl"
                        collision = 1
                        while dest.exists():
                            dest = log_archive / f"{stem}-{collision}.jsonl"
                            collision += 1
                        _atomic_write_text(dest, "\n".join(head) + "\n")
                        _atomic_write_text(AUDIT, "\n".join(tail) + "\n")
                        acts.append(f"rotated audit.jsonl: {len(head)} old line(s) -> "
                                    f"log/archive/, {len(tail)} kept")

    # -- 5. report old messages; retirement needs an explicit reviewed plan --
    h_archive = CENTRAL / "messages" / "archive"
    expired = []
    if h_archive.is_dir() and not h_archive.is_symlink():
        for f in sorted(h_archive.iterdir()):
            if (not f.is_symlink() and f.is_file() and f.suffix == ".md"
                    and not f.name.startswith(".")
                    and (now.timestamp() - f.stat().st_mtime) > cfg["inbox_archive_days"] * 86400):
                expired.append(f)
    if expired:
        notes.append(f"{len(expired)} processed message(s) need retention review; "
                     "use `ag history plan` (no automatic removal)")

    # -- 6. report-only findings (never auto-fixed) --------------------------
    if INBOX.is_dir():
        try:
            stale_unread = [f for f in INBOX.iterdir()
                            if f.is_file() and f.suffix == ".md" and not f.name.startswith(".")
                            and (now.timestamp() - f.stat().st_mtime) > cfg["inbox_archive_days"] * 86400]
        except OSError:
            stale_unread = []
        if stale_unread:
            notes.append(f"{len(stale_unread)} unread inbox message(s) older than "
                         f"{cfg['inbox_archive_days']}d — never auto-moved (unprocessed)")
    trash_dir = CENTRAL / ".trash"
    if trash_dir.is_dir():
        try:
            old_trash = [d for d in trash_dir.iterdir()
                         if (now.timestamp() - d.stat().st_mtime) > cfg["trash_days"] * 86400]
        except OSError:
            old_trash = []
        if old_trash:
            notes.append(f".trash/ holds {len(old_trash)} item(s) older than "
                         f"{cfg['trash_days']}d — safe to empty by hand")
    cache_hits = []
    for root_name in ("skills", "skills_data", "mcp", "plugins", "tools"):
        base = CENTRAL / root_name
        if not base.is_dir():
            continue
        for cur, dirs, _files in os.walk(base):
            for d in list(dirs):
                if d in ("node_modules", ".venv", "venv", "__pycache__", ".cache"):
                    cache_hits.append(Path(cur) / d)
                    dirs.remove(d)
    if cache_hits:
        notes.append(f"{len(cache_hits)} rebuildable cache dir(s) inside the guild "
                     f"(node_modules/.venv/__pycache__) — bloat backups; clean or rebuild outside")
    return acts, notes


def _record_groom(acts: list, notes: list) -> None:
    atomic_write_json(groom_state_write(), {
        "host_id": host_id(),
        "last_run": now_iso(),
        "last_actions": acts,
        "last_notes": notes,
    })


def _groom_due(cfg: dict) -> bool:
    state = groom_state_read()
    if not state.is_file():
        return True
    try:
        last = json.loads(state.read_text(encoding="utf-8")).get("last_run", "")
    except (json.JSONDecodeError, OSError):
        return True
    t = _parse_iso(last)
    if not t:
        return True
    return (_now_epoch() - t.timestamp()) >= cfg["groom_interval_hours"] * 3600


def _now_epoch() -> float:
    return datetime.now(timezone.utc).timestamp()


def maybe_auto_groom(agent: str) -> None:
    """Rate-limited auto-groom after bootstrap — keeps the guild from slowly
    rotating. At most once per groom_interval_hours; NEVER fails bootstrap."""
    try:
        cfg = load_retention()
        if not _groom_due(cfg):
            return
        # Automatic maintenance is a read-only plan. Applying file moves
        # requires the user's reviewed, explicit maintenance action.
        acts, notes = _groom(cfg, dry_run=True)
        _record_groom(acts, notes)
        audit("groom", {"agent": agent, "auto": True,
                        "actions": len(acts), "notes": len(notes)})
        if acts or notes:
            print(f"\n== AUTO-GROOM (data hygiene — policy: RETENTION.md) ==")
            print(f"  {len(acts)} maintenance action(s), {len(notes)} note(s). "
                  "Details withheld from unrelated sessions; request a maintenance plan.")
    except Exception as e:  # hygiene must never break the session contract
        print(f"  (auto-groom skipped: {e})")


# ------------------------------------------------- upgrade self-check (3.9) ---

UPGRADE = CENTRAL / "UPGRADE.md"

UPGRADE_DEFAULTS = {
    "mode": "check",        # check | apply | off
    "interval_hours": 24,
}


def load_upgrade_config() -> dict:
    """UPGRADE.md `key = value` lines override the defaults — same parsing
    convention as RETENTION.md. mode is a string, interval_hours an int;
    anything unparseable falls back silently."""
    out = dict(UPGRADE_DEFAULTS)
    if not UPGRADE.is_file():
        return out
    for line in UPGRADE.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k, v = k.strip(), v.strip().split("#", 1)[0].strip().lower()
        if k == "mode" and v in ("check", "apply", "off"):
            out["mode"] = v
        elif k == "interval_hours":
            try:
                out["interval_hours"] = max(1, int(v))
            except ValueError:
                pass
    return out


def _upgrade_state(read_only: bool = False) -> Path:
    """Upgrade bookkeeping is per device, exactly like groom state."""
    return host_state("upgrade.json") if read_only \
        else host_dir(create=True) / "upgrade.json"


def _upgrade_due(cfg: dict) -> bool:
    state = _upgrade_state(read_only=True)
    if not state.is_file():
        return True
    try:
        last = json.loads(state.read_text(encoding="utf-8")).get("last_check", "")
    except (json.JSONDecodeError, OSError):
        return True
    t = _parse_iso(last)
    if not t:
        return True
    return (_now_epoch() - t.timestamp()) >= cfg["interval_hours"] * 3600


def maybe_auto_upgrade(agent: str) -> None:
    """Rate-limited upgrade self-check after bootstrap (3.9.0+). Compares the
    installed version against the public registries once per interval_hours;
    mode=apply installs the update automatically. NEVER fails bootstrap."""
    try:
        cfg = load_upgrade_config()
        if cfg["mode"] == "off" or not _upgrade_due(cfg):
            return
        # Stamp BEFORE any network call: an offline machine must not retry
        # the check on every bootstrap for a whole day.
        atomic_write_json(_upgrade_state(), {
            "host_id": host_id(),
            "last_check": now_iso(),
            "mode": cfg["mode"],
        })
        versions = {}
        for _name, fetcher in (("skillhub", fetch_skillhub_version),
                               ("github", fetch_github_version),
                               ("clawhub", fetch_clawhub_version)):
            try:
                versions[_name] = fetcher()
            except Exception:
                pass  # one unreachable registry is not an error here
        if not versions:
            return  # offline / all registries unreachable — retried next interval
        local = read_runtime_version().get("skill_version", "0")
        latest = max(versions.values(), key=_verkey)
        if not _version_gt(latest, local):
            return
        if cfg["mode"] == "apply":
            ok, msg = _download_and_apply(latest)
            audit("upgrade", {"agent": agent, "auto": True,
                              "result": "ok" if ok else "failed", "version": latest})
            print(f"\n== AUTO-UPGRADE ({local} → {latest}) ==")
            print(f"  {'✓' if ok else '✗'} {msg}")
            if ok:
                print("  user data (identity/rules/log/handoff/skills_data/"
                      "connectors/memory) untouched.")
        else:
            print(f"\nupdate available: {local} → {latest} "
                  f"(bootstrap self-check, mode=check — set `mode = apply` in "
                  f"UPGRADE.md to install automatically, or run `ag upgrade --apply`)")
    except Exception as e:  # the self-check must never break bootstrap
        print(f"  (auto-upgrade check skipped: {e})")


def cmd_groom(args: list) -> int:
    """Explicit legacy rotations; --dry-run reports only. No hard deletion.
    Task archive retirement is handled by reviewed `history` plans."""
    if not CENTRAL.exists():
        print(f"{CENTRAL} missing — run `ag init` first", file=sys.stderr)
        return 1
    dry = "--dry-run" in args
    agent = os.environ.get("AG_AGENT") or "unknown"
    acts, notes = _groom(load_retention(), dry)
    print(f"== groom {'(DRY-RUN) ' if dry else ''}— {CENTRAL} ==")
    for a in acts:
        print(f"  {'→' if dry else '✓'} {a}")
    if not acts:
        print("  ok — nothing past retention (policy: RETENTION.md)")
    for n in notes:
        print(f"  ! {n}")
    if not dry:
        _record_groom(acts, notes)
        audit("groom", {"agent": agent, "actions": len(acts), "notes": len(notes)})
    return 0


def cmd_audit(args: list) -> int:
    n = int(args[0]) if args and args[0].isdigit() else 20
    if not AUDIT.exists():
        print("no audit trail yet")
        return 0
    lines = [l for l in AUDIT.read_text(encoding="utf-8").splitlines() if l.strip()][-n:]
    for line in lines:
        try:
            e = json.loads(line)
            print(f"{e.get('ts','?')}  {e.get('action','?'):<10} "
                  f"{e.get('agent',''):<12} {e.get('file', e.get('name', e.get('title','')))}")
        except json.JSONDecodeError:
            print(line)
    return 0


def cmd_prune(args: list) -> int:
    days = int(args[0]) if args and args[0].isdigit() else 30
    data = load_registry()
    now = datetime.now(timezone.utc)
    stale = []
    for name, e in data.get("agents", {}).items():
        if not registered_here(e):
            continue  # another device's install — not ours to judge
        ls = entry_view(e).get("last_seen")
        if not ls:
            continue
        try:
            t = datetime.fromisoformat(ls.replace("Z", "+00:00"))
            if t.tzinfo is None:
                t = t.replace(tzinfo=timezone.utc)
            age = (now - t.astimezone(timezone.utc)).days
        except ValueError:
            continue
        if age > days:
            stale.append((name, ls, age))
    if not stale:
        print(f"no agents idle > {days} days")
        return 0
    print(f"agents idle > {days} days (candidates for manual removal):")
    for name, ls, age in stale:
        print(f"  {name:<12} last_seen={ls}  idle={age}d")
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    cmd, args = sys.argv[1], sys.argv[2:]
    table = {
        "init": cmd_init,
        "find-root": cmd_find_root,
        "link-root": cmd_link_root,
        "adopt": cmd_adopt,
        "bootstrap": cmd_bootstrap,
        "recall": cmd_recall,
        "finish": cmd_finish,
        "task": cmd_task,
        "history": cmd_history,
        "inbox": cmd_inbox,
        "migrate": cmd_migrate,
        "doctor": cmd_doctor,
        "platform": cmd_platform,
        "tool": cmd_tool,
        "tools": cmd_tools,
        "port": cmd_port,
        "upgrade": cmd_upgrade,
        "status": cmd_status,
        "register": cmd_register,
        "last-seen": cmd_last_seen,
        "send": cmd_send,
        "log": cmd_log,
        "focus": cmd_focus,
        "learn": cmd_learn,
        "review": cmd_review,
        "resolve": cmd_resolve,
        "groom": cmd_groom,
        "audit": cmd_audit,
        "prune": cmd_prune,
    }
    fn = table.get(cmd)
    if fn is None:
        print(f"unknown command: {cmd}\n\n{__doc__}", file=sys.stderr)
        return 2
    try:
        return fn(args)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"{cmd} failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
