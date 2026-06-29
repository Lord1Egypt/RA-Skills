---
name: copy-my-profile
description: >
  Extract a standardized cross-tool user profile from any AI agent's long-term memory
  (USER.md, MEMORY.md, AGENTS.md, CLAUDE.md, .cursorrules, etc.) so you can
  re-use it in another AI tool without retraining. Output is a portable
  Markdown document with five categories — instructions, identity, profession,
  projects, preferences. Works with Claude Code, OpenClaw, Codex CLI, Cursor,
  Cline, Continue, Aider, or any LLM agent. 适用场景:生成我的画像/导出 profile/
  拷贝到其他 AI 工具/跨工具同步偏好/换 agent 不丢记忆。
---

# Copy My Profile

- **Version**: 1.0.0
- **License**: MIT
- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/better-agent-skills

Generate a portable Markdown profile from one AI tool's long-term memory and
re-use it in another. Solves the "I just trained Tool A to know me, now I want
to use Tool B" problem without retraining.

## Why this skill

Modern developers use multiple AI tools: Claude Code at home, Cursor at work,
ChatGPT for brainstorming, OpenClaw for backend automation, etc. Each tool
accumulates its own memory of who you are — but **none of them talk to each
other**. This skill defines a portable Markdown format (like vCard for
contacts, or ICS for calendars) so your "AI profile" can move with you.

- Zero infrastructure: no cloud, no account, no sync server
- Privacy-controlled: you see the full output before copying anywhere
- Standard format: 5 categories that any LLM can parse reliably

## Output categories (5 in order)

Detailed format examples and filtering rules live in
`references/profile-template.md` (read it during step 2-3).

1. **Instructions** — Explicit rules the user wants followed (tone, format,
   behavior corrections, ⚠️-marked rules in memory files)
2. **Identity** — Name, education, interests, non-sensitive personal info
3. **Profession** — Role, company, skill domains
4. **Projects** — Projects the user actually built or invested effort in
5. **Preferences** — Broadly-applicable work style and taste preferences

## Execution steps

### Step 1 — Pick execution path

Choose based on the current runtime environment.

**Path A — Memory-search-capable environment** (Claude Code, OpenClaw, Codex
CLI, or any agent that exposes a `memory_search` / file-read tool):

1. Run `memory_search` for topics like "instructions", "preferences",
   "projects"
2. Read key files based on the host tool:
   - **Claude Code**: `~/.claude/CLAUDE.md`, project `CLAUDE.md`
   - **OpenClaw**: `USER.md`, `MEMORY.md`, `AGENTS.md`, `memory/*.md`
   - **Codex CLI**: `AGENTS.md`, `~/.codex/instructions.md`
   - **Cursor**: project `.cursorrules`, `.cursor/rules/*.md`
   - **Cline**: project `.clinerules`
   - **Continue**: `~/.continue/config.json` (system message), workspace
     `.continue/*.md`
   - **Aider**: `CONVENTIONS.md`, `.aider.conf.yml`
   - See `references/tools-memory-map.md` for the full table.
3. Read the most recent N daily memory logs (if the tool keeps them) to
   capture recent context

**Path B — No memory-search tool** (Cline without filesystem, web ChatGPT,
fresh Cursor session, etc.):

1. Ask the user to provide files or paste relevant content (see
   `references/tools-memory-map.md` for what to ask for)
2. If the user only supplies an old profile, normalize the format and note at
   the end: "Based on existing profile, not re-extracted from raw memory"

**Degradation strategy (both paths):**

- If a key file is missing, continue with what's available and list "missing
  sources" at the bottom
- If a category has zero data, output `(no data)` — don't skip the category
- If `memory_search` returns empty, fall back to Path B

### Step 2 — Filter

- **Instructions**: Only items clearly identifiable as rules in memory files;
  don't fabricate. Distinction rules in `profile-template.md`
- **Identity**: Only non-sensitive info the user has actively shared. Privacy
  filter rules in `profile-template.md`
- **Projects**: One line per project — function, status, key decisions
- Preserve the user's original phrasing as much as possible

### Step 3 — Output format

Write the profile to `./my-profile.md` (current directory) and also reply to
the user inline. Format:

- Each line: `[YYYY-MM-DD] - entry content`
- Use `[unknown]` if the date is unclear
- Within each category, sort by date ascending
- Wrap the entire profile in a single fenced Markdown code block (so the user
  can copy-paste in one click)

### Step 4 — Closing notes

After the code block, add a brief note covering:

- Whether all relevant info from current memory was included
- Any categories that had no data or used degradation
- Any dimensions or uncertain entries excluded (so the user can decide whether
  to add them)
- **Import hint**: which file to paste this into for the target tool — see
  `references/import-prompts.md` for ready-to-use prompts

## Tips for cross-tool transfer

- **Pull** (export): Run this skill in your source tool → copy `my-profile.md`
- **Push** (import): In the target tool, paste the profile with a prompt from
  `references/import-prompts.md`
- The Markdown is plain text — works through clipboard, email, Notion, GitHub
  gist, file transfer, anything

## See also

- `references/profile-template.md` — full output format example + filtering
  rules + privacy rules
- `references/tools-memory-map.md` — where each AI tool stores its memory
  (where to read FROM and where to write TO)
- `references/import-prompts.md` — copy-paste prompts for importing the
  profile into each target tool
