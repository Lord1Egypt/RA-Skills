---
name: "claude_md_initializer"
description: "Use when onboarding a repository into Claude Code by creating or improving CLAUDE.md, and optionally identifying useful skills, hooks, and verifier setup."
---


# CLAUDE MD Initializer

Use this skill when a repo needs onboarding documentation for future agent sessions.

## Workflow
1. Read the repository structure, README, existing instructions, and tooling config.
2. Identify key build, test, and run commands.
3. Summarize the high-level architecture and important conventions.
4. Create or improve `CLAUDE.md` without stuffing it with generic advice.
5. Suggest follow-on skills, hooks, or verifier setup if they materially help.

## Guardrails
- Do not invent commands or conventions.
- Focus on repo-specific knowledge, not generic coding advice.
- Keep the file practical for future agent sessions.

## Example Requests
- Analyze this repo and produce a strong CLAUDE.md for future agent sessions.
- Upgrade the existing CLAUDE.md so future coding agents onboard faster.

## Inputs
- Repository structure
- Existing docs and config
- Important commands and conventions

## Outputs
- New or improved CLAUDE.md
- Optional follow-up recommendations

## Success Criteria
- Repo-specific commands are captured correctly.
- Architecture notes are practical, not generic.
- The file helps future agents move faster.

## Non-Goals
- Generic engineering advice
- Invented commands or undocumented workflows

## Source Provenance
Derived from `src/commands/init.ts`.
