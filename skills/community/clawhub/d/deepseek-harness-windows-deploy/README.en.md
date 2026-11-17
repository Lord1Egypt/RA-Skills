# DeepSeek Harness — Windows Deployment Pitfalls Skill

A practical guide for **agents**: how to source-build, construct, launch, and configure a
workspace for DeepSeek Harness (`deepseek-ai/deepseek-harness`) on **Windows**, while
skipping every pitfall that has already been hit.

> This is an **Agent Skills** package (centred on `SKILL.md`). It is auto-loaded by agents
> that support the Agent Skills standard, such as WorkBuddy and OpenClaw. It is **not** a
> script for humans to execute directly.

## Scope and Boundaries (read first)

This skill covers **one thing only**: installing, building, launching, and troubleshooting
DeepSeek Harness itself on Windows.

It explicitly does **not** cover (these have been split into separate skills to keep scope
tight):

- Project scaffolding, cross-platform desktop application development, or Electron / Tauri
  packaging — those belong to the `deepseek-harness-desktop-shell` skill.
- Any environment changes unrelated to Harness deployment.

High-impact steps (clearing `NODE_OPTIONS`, terminating the process holding port 3080, or
deleting files under `~/.dsh`) **must be explained to the user and confirmed before they
run**, and the patterns given here apply **only** to Harness troubleshooting — do not
re-use them elsewhere.

Non-trigger conditions: if the task is just "build a desktop app" or "package as exe",
hand it to the desktop-shell skill, not this one.

## What This Skill Solves

- pnpm / corepack paths corrupted under Windows + managed Node — invoke `corepack.js`
  directly via PowerShell.
- WorkBuddy-sandbox injected `genie-safe-delete` hook blocks Harness writes — launch with
  `NODE_OPTIONS=""`.
- Post-migration `EPERM` directory symlink failures and stuck port 3080.
- Workspace persistence location (`~/.dsh/storages/workspace.json`) and "workspace won't
  select" diagnosis.

## Compatibility

This skill follows the open **Agent Skills standard** (`SKILL.md` + frontmatter). Any
agent runtime that supports the standard can load it.

- **Confirmed compatible**: WorkBuddy, OpenClaw (100% compatible skill ecosystems; ClawHub
  marketplace skills install with one click).
- **Format-compatible, runtime loading pending official confirmation**: Claude / Claude Code
  (Anthropic's Agent Skills standard natively supports `SKILL.md`), Cursor, Windsurf,
  Codex (OpenAI), and others — if they implement the Agent Skills standard, this skill
  loads directly. Whether each product loads it **natively** is up to its official docs.
- **Requires separate confirmation**: Hermes is an independent agent product whose skill
  system is also `SKILL.md`-shaped, but runtime loading per the Agent Skills standard
  must be confirmed against Hermes' own documentation.
- **Operating system**: Windows 10 / 11. Some pitfalls tie to Windows path / directory
  symlink behaviour; on macOS / Linux, adapt the paths.
- **Note**: apart from the explicitly marked "WorkBuddy / CodeBuddy sandbox-only" pitfalls,
  the rest (pnpm, port 3080, EPERM symlink, workspace semantics) are useful to any agent
  deploying Harness on Windows.

## Directory Layout

```
deepseek-harness-windows-deploy/
├── SKILL.md                      # Main instruction for the agent (core takeaways, launch command, compatibility, safety boundaries)
├── README.md                     # This file's Chinese counterpart (default entry)
├── README.en.md                  # This file (English)
└── references/
    └── deploy-pitfalls.md        # Detailed pitfalls A–G (cause + remedy)
```

## Usage (agent side)

- **Auto**: after installing into `~/.workbuddy/skills/` (or the equivalent skills
  directory of OpenClaw), the agent auto-triggers this skill on related tasks (deploying,
  building, launching, or troubleshooting DeepSeek Harness on Windows).
- **Manual**: drop this whole directory into the agent's skills directory.

## Version History

- **v1.0.3** (2026-08-14): Review-driven hardening.
  - Added "Scope and Boundaries" section: explicitly excludes desktop-shell / scaffolding,
    and states that high-impact steps require user confirmation and that patterns must not
    leak to other scenarios (addresses SQP-1).
  - Strengthened "Safety and Guardrails": `NODE_OPTIONS=""` is now explicitly scoped to
    **a single dsh web process**, not a global or system-wide disabling, and confirmation
    is required before execution (addresses RA2 / TM1).
  - Declared the backgrounded dsh web as user-controlled (addresses persistence_privilege).
  - Removed all emoji, cleaned Chinese / English mixing, and replaced personal paths with
    placeholders.
- **v1.0.2** (2026-08-14): Removed the "Desktop Shell (Optional)" section and the
  `references/desktop-shell-prompt.md` file from this skill (that topic now lives in its own
  skill / project). Documentation cleanup only; no behavioural change.
- **v1.0.1** (2026-08-14): In response to ClawHub LLM review, added a "Safety and
  Guardrails" section to `SKILL.md`.
  - Clarified that `NODE_OPTIONS=""` is **only for the single `dsh web` launch command**,
    aimed at bypassing the sandbox-injected `genie-safe-delete` hook — it is **not** a
    system- or filesystem-level security disable and must not be applied to other commands
    or long-lived environments.
  - Clarified that `fs.rmSync(path, {recursive:true, force:true})` targets **only** the
    single stale directory symlink
    `~/.dsh/profiles/node_modules/@deepseek-ai/dsh-goal-round-driver` — reconstructable,
    path-exact, never touches user data.
- **v1.0.0** (2026-08-14): Initial release covering all known pitfalls and verified
  commands for deploying DeepSeek Harness under Windows + managed Node.

## License

MIT