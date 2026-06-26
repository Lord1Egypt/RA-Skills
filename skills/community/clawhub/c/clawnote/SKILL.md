---
name: clawnote
description: Review-first Xiaohongshu/Rednote content ops for OpenClaw. Use when creating a repeatable workflow for topic research, draft generation, Feishu review, exact-title approval, structured publish packages, and optional approved publishing after explicit confirmation.
---

# Clawnote

Use this skill when the goal is to build or run a Xiaohongshu content workflow inside OpenClaw.

This skill is for:

- daily AI news + OpenClaw practice drafts
- Feishu-first review flow
- Xiaohongshu-style rewriting
- exact-title approval before publish
- memory + cron driven content ops

## What To Read

Start with:

- `workspace-template/AGENTS.md`
- `workspace-template/SOUL.md`
- `workspace-template/TOOLS.md`

Read these when needed:

- `workspace-template/PUBLISH_ASSIST.md` for publish rules
- `workspace-template/FEISHU_COMMANDS.md` for user command patterns
- `docs/SAFETY.md` for risk boundaries

## Workflow

Follow this order:

1. `xhs-research`
2. `xhs-draft`
3. `xhs-publish-assist`

Default mode is review-first, not auto-publish.

## Bundled Scripts

Use these scripts instead of rewriting them:

- `workspace-template/scripts/save_publish_package.py`
- `workspace-template/scripts/build_publish_package.py`
- `workspace-template/scripts/publish_approved_note.py`
- `workspace-template/scripts/write_memory_entry.py`

## Important Safety Rules

- Do not publish without explicit user approval.
- Treat deletion as a separate high-risk action.
- Do not assume archive-to-draft works unless it has been re-verified for the current Xiaohongshu UI.
- Prefer exact-match title confirmation over fuzzy matching.
