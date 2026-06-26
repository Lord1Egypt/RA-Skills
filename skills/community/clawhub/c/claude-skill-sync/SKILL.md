---
name: claude-skill-sync
description: |
  This skill should be used when the user wants to sync, synchronize, or compare
  skills between Claude Code and OpenClaw. Use it for requests like
  "sync my skills", "sync claude code skills to openclaw",
  "check which skills are out of sync", "bidirectional skill sync",
  "which skills are missing from openclaw", "which skills are missing from claude code",
  or "claude-skill-sync".
  Scans both Claude Code and OpenClaw skill directories, compares their full content,
  and performs bidirectional sync with user confirmation for conflicts.
version: 1.0.0
---

# Claude Code ↔ OpenClaw Skill Sync

## Goal

Scan skill directories for both Claude Code and OpenClaw, compare their contents,
and perform a bidirectional sync — asking the user for confirmation before making
any changes, and asking the user to resolve conflicts when the same skill exists
in both tools with different content.

Both sides store full SKILL.md content. There are no wrapper stubs.

## Steps

### 1. Scan Claude Code Skills

List all immediate subdirectories (one level deep, not recursive) under `~/.claude/skills/` that contain a `SKILL.md` file.
Record the name (directory name) and read the full content of each `SKILL.md`.

### 2. Scan OpenClaw Skills

List all immediate subdirectories (one level deep, not recursive) under `~/.openclaw/workspace/skills/` that contain a `SKILL.md` file.
Record the name (directory name) and read the full content of each `SKILL.md`.

### 3. Compare and Categorize

Build four categories by matching skill names across both directories:

**A. Claude Code only** — exists in Claude Code, no entry in OpenClaw at all.

**B. OpenClaw only** — exists in OpenClaw, no entry in Claude Code at all.

**C. In sync** — exists in both, content is textually identical after stripping
leading/trailing whitespace from each line and ignoring line-ending differences (LF vs CRLF).
No action needed.

**D. Conflict** — exists in both, but content differs after the normalization above.

### 4. Present the Report

Output a summary before taking any action:

```
## Skill Sync Report

### In Sync ✅
{count} skills are already in sync.
{list skill names, one per line}

### Claude Code Only — missing from OpenClaw (A)
- {skill-name}

### OpenClaw Only — missing from Claude Code (B)
- {skill-name}

### Conflicts — same name, different content (D)
- {skill-name}
```

If all skills are in sync, output "✅ All skills are in sync. Nothing to do." and stop.

### 5. Handle Category A — Copy to OpenClaw

For each skill in category A, ask the user:

> "{skill-name}" exists in Claude Code but is missing from OpenClaw.
> Copy it to OpenClaw? [y/n/all/skip-all]

- `y` → copy this skill
- `n` → skip this skill
- `all` → copy all remaining category A skills without asking again
- `skip-all` → skip all remaining category A skills (applies to this category only — you will still be prompted for categories B and D)

**To copy a Claude Code skill to OpenClaw:**

1. Read the `version` field from the `SKILL.md` frontmatter. If absent, use `1.0.0`.
2. Create directory `~/.openclaw/workspace/skills/{name}/`
3. Write the full `SKILL.md` content to `~/.openclaw/workspace/skills/{name}/SKILL.md` as-is.
4. Write `~/.openclaw/workspace/skills/{name}/_meta.json`:

```json
{
  "slug": "{name}",
  "version": "{version}"
}
```

### 6. Handle Category B — Copy to Claude Code

For each skill in category B, ask the user:

> "{skill-name}" exists in OpenClaw but is missing from Claude Code.
> Copy it to Claude Code? [y/n/all/skip-all]

- `y` → copy this skill
- `n` → skip
- `all` → copy all remaining category B skills without asking
- `skip-all` → skip all remaining category B skills (applies to this category only — you will still be prompted for category D)

**To copy an OpenClaw skill to Claude Code:**

1. Create directory `~/.claude/skills/{name}/`
2. Write the full `SKILL.md` content to `~/.claude/skills/{name}/SKILL.md` as-is.
   Do not copy `_meta.json` — it is OpenClaw-specific.

### 7. Handle Category D — Resolve Conflicts

For each conflict, show the user:

```
Conflict: {skill-name}

Claude Code version (first 5 lines of body, i.e. content after the closing --- of frontmatter):
{lines}

OpenClaw version (first 5 lines of body, i.e. content after the closing --- of frontmatter):
{lines}

Which version should be kept?
[1] Keep Claude Code version → overwrites OpenClaw
[2] Keep OpenClaw version → overwrites Claude Code
[3] Skip — leave both as-is
```

Apply the user's choice:

- **Choice 1** → overwrite `~/.openclaw/workspace/skills/{name}/SKILL.md` with the Claude Code content.
  Update `~/.openclaw/workspace/skills/{name}/_meta.json` version to match the frontmatter of the winning file. If `_meta.json` does not exist, create it.
- **Choice 2** → overwrite `~/.claude/skills/{name}/SKILL.md` with the OpenClaw content.
  No changes to `_meta.json` — it is OpenClaw-specific and remains as-is.
- **Choice 3** → do nothing for this skill.

### 8. Summary

After all actions are complete, output:

```
## Sync Complete

- Copied to OpenClaw: {count}
- Copied to Claude Code: {count}
- Conflicts resolved: {count}
- Skipped: {count}
```

## Security Rules

- When presenting conflict previews, show at most the first 5 lines of the body to the user.
  You may read complete file contents internally in order to copy or write files.
- Never output token values, API keys, or credentials that may appear in skill files.
- Always use `~/.claude/` and `~/.openclaw/` path notation. Never expand `~` to an absolute path.
- If a `version` field is absent from a SKILL.md frontmatter, use `1.0.0` as the default.
