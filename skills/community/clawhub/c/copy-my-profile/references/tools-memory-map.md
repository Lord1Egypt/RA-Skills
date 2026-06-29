# AI Tools — Long-Term Memory File Map

Where each AI tool stores its long-term memory of you. Use this to decide
**where to READ FROM** (when extracting your profile) and **where to WRITE TO**
(when importing your profile into a new tool).

## Quick reference table

| Tool | Memory file(s) | Format | Auto-loaded? |
|------|----------------|--------|--------------|
| **Claude Code** (Anthropic) | `~/.claude/CLAUDE.md`, project `CLAUDE.md`, project `.claude/skills/` | Markdown | ✅ |
| **OpenClaw** | `<workspace>/USER.md`, `MEMORY.md`, `AGENTS.md`, `memory/*.md` | Markdown | ✅ |
| **Codex CLI** (OpenAI) | `AGENTS.md`, `~/.codex/instructions.md` | Markdown | ✅ |
| **Cursor** | project `.cursorrules`, `.cursor/rules/*.md`, global Settings → Rules for AI | Markdown / inline text | ✅ |
| **Cline** (VSCode ext) | project `.clinerules`, global Settings → Custom Instructions | Markdown | ✅ |
| **Continue** (VSCode/JetBrains ext) | `~/.continue/config.json` `systemMessage` field, workspace `.continue/*.md` | JSON + Markdown | ✅ |
| **Aider** | `CONVENTIONS.md`, `.aider.conf.yml` `read` field | Markdown / YAML | ✅ via `--read` |
| **ChatGPT (web)** | OpenAI's hosted "Memory" feature | proprietary | ✅ but **vendor-locked** |
| **Claude.ai (web)** | Project knowledge files, custom instructions | text upload | ✅ |
| **Anthropic Apps (skills)** | `~/.claude/skills/<skill-name>/SKILL.md` | Markdown frontmatter + body | ✅ |

## Detailed notes per tool

### Claude Code (CLI)

- **Global**: `~/.claude/CLAUDE.md` — loaded for every session
- **Project**: any `CLAUDE.md` walked upward from CWD — loaded automatically
- Best place to paste profile: append to global `~/.claude/CLAUDE.md`

### OpenClaw

- **Identity & user**: `<workspace>/USER.md` (about the user), `IDENTITY.md`
  (about the agent)
- **Long-term memory**: `<workspace>/MEMORY.md` + `<workspace>/memory/*.md`
- Best place to paste profile: update `USER.md` (about-the-user section)

### Codex CLI

- **Project**: `AGENTS.md` in working directory
- **Global**: `~/.codex/instructions.md` (or `~/.config/codex/instructions.md`)
- Best place to paste profile: append to `~/.codex/instructions.md`

### Cursor

- **Project rules**: `.cursorrules` in project root (legacy single-file format)
  or `.cursor/rules/*.md` (newer multi-file format)
- **Global "Rules for AI"**: Settings → General → Rules for AI (plain text box)
- Best place to paste profile: Global "Rules for AI" for cross-project use

### Cline (VSCode extension)

- **Project**: `.clinerules` file
- **Global**: Settings → Custom Instructions
- Best place to paste profile: Custom Instructions (global)

### Continue (VSCode/JetBrains extension)

- **Config**: `~/.continue/config.json` → `systemMessage` field
- **Context**: `.continue/*.md` files in workspace
- Best place to paste profile: edit `~/.continue/config.json` `systemMessage`

### Aider

- **Conventions**: `CONVENTIONS.md` in project, loaded via
  `--read CONVENTIONS.md` or `read:` in `.aider.conf.yml`
- Best place to paste profile: `CONVENTIONS.md` + add to `.aider.conf.yml`
  `read:` list

### ChatGPT (web) & Claude.ai (web)

- ChatGPT: Settings → Personalization → Memory (vendor-managed, can't
  bulk-import a profile, must dribble it in via chat)
- Claude.ai: Project → Knowledge → upload `my-profile.md` as a file
- Note: web tools are **vendor-locked** — profile imported here doesn't sync
  back out

## Path A vs Path B selection rule

| You're running in | Use path |
|-------------------|----------|
| Claude Code / OpenClaw / Codex CLI / any agent with file-read & memory tools | **A** (auto-extract) |
| Cursor / Cline / Continue / Aider (have file access but no memory_search) | **A** (read files directly) |
| ChatGPT web / Claude.ai web / any sandboxed chat with no file access | **B** (user pastes content) |
