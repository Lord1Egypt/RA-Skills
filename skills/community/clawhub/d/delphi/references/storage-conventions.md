# Storage Conventions

How to reason about workspace layout, file placement, and path decisions — generically, for any OpenClaw deployment.

---

## The Mental Model

Think of storage in three zones:

```
ZONE 1: Workspace (agent's home)
  └── Where you read and write files by default
  └── Auto-injected bootstrap files live here
  └── Path: configured in `agents.defaults.workspace` (default: ~/.openclaw/workspace)

ZONE 2: State dir (platform's home)
  └── Where OpenClaw stores its own operational data
  └── Session transcripts, cron jobs, skill installs, logs
  └── Path: ~/.openclaw/ (or OPENCLAW_STATE_DIR)

ZONE 3: Host filesystem (everything else)
  └── Accessible via absolute paths unless sandboxed
  └── Where persistent volumes live on cloud deployments
  └── Treat with care — changes here survive redeployments
```

---

## Workspace Layout (Recommended)

A well-organized workspace follows this convention:

```
<workspace>/
├── AGENTS.md           ← primary operating instructions
├── SOUL.md             ← personality/tone
├── IDENTITY.md         ← agent identity
├── USER.md             ← user profile
├── TOOLS.md            ← environment-specific notes
├── HEARTBEAT.md        ← periodic task checklist
├── MEMORY.md           ← long-term curated memory (main session only)
├── PLATFORM.md         ← optional: platform reference (if created)
│
├── memory/             ← all memory files
│   ├── YYYY-MM-DD.md   ← daily notes (auto-loaded: today + yesterday)
│   ├── drift-log.md    ← self-awareness drift log
│   ├── lessons.md      ← append-only lessons learned
│   └── *.md            ← topic files, loaded on demand
│
├── skills/             ← workspace-level skills (highest precedence)
│   └── <skill-name>/
│       ├── SKILL.md
│       └── references/
│
├── scripts/            ← utility scripts
├── agents/             ← per-agent bootstrap files (if multi-agent)
└── <project-dirs>/     ← project-specific working directories
```

---

## Storage Decision Rules

### Where does a new file go?

| File type | Location |
|---|---|
| Long-term knowledge the agent should always have | `MEMORY.md` (as a distilled entry) |
| Raw session notes, logs, daily events | `memory/YYYY-MM-DD.md` |
| Lessons learned (append-only) | `memory/lessons.md` |
| Topic-specific knowledge (loaded on demand) | `memory/<topic>.md` |
| Self-check drift events | `memory/drift-log.md` |
| Scripts | `scripts/<name>.<ext>` |
| Skill instructions | `skills/<skill-name>/SKILL.md` |
| Skill reference material | `skills/<skill-name>/references/<file>.md` |
| Persistent data that survives redeployments | A persistent volume path (e.g. `/data/` on Railway) |
| Temporary working files | `<workspace>/tmp/` or in-memory — clean up after use |

### What NOT to put in MEMORY.md

- Raw logs or transcripts — those go in daily files
- Temporary state — will be stale immediately
- Very large reference documents — create a topic file instead
- Secrets or API keys — those go in a secure location (`memory/keys.env` or env config), never in MEMORY.md

### What NOT to put in daily files

- Curated knowledge — distill important stuff into MEMORY.md
- Lessons that should persist — those go in `memory/lessons.md`

---

## Path Conventions

### Always verify before using a path

Don't assume a path exists. Check with `read` or `exec ls` before operating on it.

```
# Check workspace
read: <workspace>/

# Check a specific file
read: <workspace>/memory/YYYY-MM-DD.md

# List a directory
exec: ls <workspace>/memory/
```

### Absolute vs relative paths

- **Within workspace tools**: relative paths resolve from workspace root — safe to use
- **In exec commands**: use absolute paths unless you've confirmed cwd
- **In cron/subagent contexts**: always use absolute paths — they run in fresh sessions with potentially different cwd

### Persistent vs ephemeral storage

| Storage type | Survives restart? | Survives redeploy? |
|---|---|---|
| Workspace files | ✅ (if on persistent volume) | Depends on deployment |
| State dir (`~/.openclaw/`) | ✅ | ❌ usually (unless volume-mounted) |
| In-memory / session state | ❌ | ❌ |
| Persistent volume (e.g. `/data/`) | ✅ | ✅ |

**Key question to ask on any deployment:** Is the workspace on a persistent volume? If not, files written there will be lost on redeploy.

---

## First-Load Storage Discovery

On first load in a new deployment, do this to understand what you're working with:

```
1. Run session_status → note the workspace path
2. exec: ls <workspace>/
3. exec: ls <workspace>/memory/ (if it exists)
4. Read MEMORY.md to understand what's been established
5. Check if drift-log.md exists — create it if not
```

This gives you a complete picture in under a minute.

---

## Storage Hygiene Rules

1. **Name files clearly** — a file named `notes.md` from 6 months ago is useless. Use dated names or descriptive names: `memory/integrations.md`, `memory/2026-04-24.md`.
2. **Clean up tmp files** — if you create a working file, delete it when done.
3. **Don't duplicate** — if something belongs in MEMORY.md, don't also put it in a daily file. Pick one.
4. **Append-only for logs** — `drift-log.md`, `lessons.md` — never edit past entries, only append.
5. **Reference over copy** — if a topic needs detail, create `memory/<topic>.md` and add a pointer in MEMORY.md rather than bloating MEMORY.md itself.
