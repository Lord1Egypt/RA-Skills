# Multi-Agent Shared Layout (~/.agents)

Cross-environment + cross-tool layout policy: **`~/.agents/` is the single source of truth** for `skills/`, `rules/`, and `agents/`. Every AI tool installation (Claude, Codex, Gemini, Antigravity) symlinks into it. **`~/.claude/plugins/` is deliberately NOT shared** to avoid marketplace cache races.

> **Applicability**: This topic targets hosts that share `~/.agents/` between Windows and WSL via NTFS. macOS / Linux-only hosts can skip the Windows-specific subsections below (marked `<details>`); the linking matrix, why-share rationale, and recovery procedure apply identically on any Unix host.

## Source of truth

<details>
<summary>Windows + WSL hosts</summary>

- **Windows-side**: `C:\Users\<user>\.agents\` is the actual on-disk storage.
- **WSL-side**: `~/.agents/` is a symlink to `/mnt/c/Users/<user>/.agents/`. Editing on either side modifies the same files.

</details>

- Other machines (e.g., macOS) keep their own `~/.agents/` and sync via Syncthing at the host-to-host layer — that is **out of this topic's scope**.

## Layout diagram

```
~/.agents/                    ← single source of truth (Windows path; WSL symlinks in)
  ├── skills/   ─────────────────┐
  ├── rules/    ───────────┐     │
  └── agents/   ───┐       │     │
                   │       │     │
                   ▼       ▼     ▼
~/.claude/agents/  ~/.claude/rules/   ~/.claude/skills/
~/.codex/skills/                                  ─┘
~/.gemini/skills/                                 ─┘
~/.gemini/antigravity/skills/                     ─┘
~/.gemini/antigravity/global_workflows/  ←  ~/.agents/agents/
~/.gemini/agents/                        ←  ~/.agents/agents/

~/.claude/plugins/   ← per-environment, NEVER linked or shared
  ├── marketplaces/  (atomic rename target; races on shared FS)
  └── cache/         (per-platform binaries)

~/.claude/projects/  ← per-environment (session JSONL keyed by CWD)
```

## Linking matrix

The bootstrap script `~/.agents/skills/dotfile/scripts/link-shared-ai-configs.{sh,ps1}` creates these symlinks idempotently:

| Source (`~/.agents/`) | Target | Tool |
|-----------------------|--------|------|
| `skills/` | `~/.claude/skills/` | Claude Code |
| `skills/` | `~/.codex/skills/` | Codex |
| `skills/` | `~/.gemini/skills/` | Gemini |
| `skills/` | `~/.gemini/antigravity/skills/` | Antigravity |
| `rules/` | `~/.claude/rules/` | Claude Code |
| `agents/` | `~/.claude/agents/` | Claude Code |
| `agents/` | `~/.gemini/agents/` | Gemini |
| `agents/` | `~/.gemini/antigravity/global_workflows/` | Antigravity (different name on this side) |

When a target already exists, the script moves it to `<parent>/.bak/<name>-<timestamp>` before creating the symlink.

## Why share these directories

| Directory | Reason to share |
|-----------|-----------------|
| `skills/` | Skills are environment-agnostic Markdown + scripts. One source = no drift between Claude, Codex, Gemini, Antigravity installs across both Windows and WSL. |
| `rules/` | Rules describe behavior, not platform-specific paths. Shared so a fix on one side propagates everywhere. |
| `agents/` | Same source feeds Claude's `agents/` and Gemini Antigravity's `global_workflows/`. Different consumer paths, same library. |

## Why NOT share ~/.claude/plugins/

The `~/.claude/plugins/marketplaces/<repo>/` directory is the atomic-rename target during `claude plugin install` and marketplace refresh:

1. Fresh clone goes to `marketplaces/temp_<timestamp>/`
2. `rename(temp_<timestamp>, <repo>)` — atomic swap

When Windows and WSL both run a plugin operation on a shared path, step 2 fails:

```
EACCES: permission denied, rename
'/.../marketplaces/temp_<ts>' -> '/.../marketplaces/<repo>'
```

The losing side leaves a `temp_*` orphan that blocks the next install. Sharing `plugins/` would convert every plugin operation into a coordination problem. Keeping `plugins/` per-environment removes the race entirely.

`~/.claude/projects/` is also per-environment for a different reason: session JSONL files encode the CWD as a project key, and Windows-style vs. WSL-style CWDs translate differently.

## Bootstrap workflow

On a fresh environment (new install or rebuild), invoke the script via its
`~/.agents/` path — the `~/.claude/skills/dotfile/` symlink does not exist yet
on first run, but `~/.agents/skills/dotfile/` is always present:

```bash
# macOS / Linux / WSL (sh)
bash ~/.agents/skills/dotfile/scripts/link-shared-ai-configs.sh
```

<details>
<summary>Windows (PowerShell)</summary>

```powershell
~/.agents/skills/dotfile/scripts/link-shared-ai-configs.ps1
```

</details>

The script:
- Detects WSL via `/proc/version` and rewrites `AGENT_DIR` to `/mnt/c/Users/<WIN_USER>/.agents/`
- Backs up any existing destination to `<parent>/.bak/<name>-<timestamp>` before linking
- Is idempotent — running again on an already-linked tree prints `✓ Already linked` and exits
- PowerShell variant also merges Codex `skills/.system/` into the shared
  `~/.agents/skills/.system/` before linking, so Codex system skills survive
  the junction replacement

## Recovery — plugin marketplace EACCES

When a shared-plugins history left a `temp_*` orphan or rename collision, clean it inside the affected environment only:

```bash
# Inside the environment hitting EACCES (Windows OR WSL — never both)
rm -rf ~/.claude/plugins/marketplaces/<repo>
rm -rf ~/.claude/plugins/marketplaces/temp_*
# Then re-run plugin install / marketplace update
```

Do **not** touch the same path from the other environment during recovery — the fix is per-environment by design.

## Related topics

- `chezmoi.md` — template-managed dotfiles (single-source pattern at the file level)
- `mcp.md` — MCP config sharing via chezmoi templates
- `syncthing.md` — cross-host sync (e.g., Windows ↔ macOS) at a different layer than this topic
