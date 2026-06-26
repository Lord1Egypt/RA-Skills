---
name: create-agents-wizard
description: Guided creation of multiple OpenClaw agents and their workspace templates. Use when users ask to create agents in batch, configure new agents, or customize AGENTS/SOUL/IDENTITY/BOOTSTRAP/USER/STYLE files. The workflow confirms scope, collects preferences agent-by-agent, drafts and confirms files, writes to disk, and summarizes results.
---

# Create Agents Wizard

Follow this workflow to create multiple agents with low user effort.

## 1) Confirm scope

1. Ask for total agent count `N`.
2. Ask each agent `id` (lowercase letters/digits/hyphens only).
3. Ask each workspace path (default `~/.openclaw/workspace-<id>`).
4. Ask scaffold mode:
   - **Standard (default):** 6 files
     - `AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `BOOTSTRAP.md`, `USER.md`, `STYLE.md`
   - **Fast mode:** 2 files only
     - `AGENTS.md`, `SOUL.md`
5. If user does not specify, use **Standard** by default.

## 2) Process one agent at a time

For each agent, collect info and draft files in fixed order.

1. Ask focused questions (use `references/question-bank.md` if available).
2. Produce an improved draft from user input.
3. Ask explicit confirmation: `Confirm write / Revise`.
4. Write only after confirmation; otherwise keep iterating.

Rules:
- Do not dump a long questionnaire; ask in small rounds (2–4 key questions each).
- Preserve user intent; do not change direction without consent.
- Respect selected mode (Standard 6 files or Fast 2 files).
- If user requests partial scaffolding, allow writing only the confirmed subset and continue/stop as requested.

## 3) Write files and create agent

After required files for one agent are confirmed:

1. If agent does not exist, create it:
   - `openclaw agents add <id> --workspace <path>`
2. Write approved files into workspace root.
   - Optional batch helper:
   - `scripts/scaffold.sh --agent <id> --workspace <path> --from <approved_dir> --force`
3. Optional identity setup:
   - `openclaw agents set-identity --workspace <path> --from-identity`

If user wants docs only, skip CLI config changes.

## 4) Final summary

When all agents are done, report:

- Created agents (id + workspace)
- Written file list per agent
- `openclaw agents list` output (if CLI available)
- Next-step suggestions (skills, routing, default models)

## 5) Quality bar

- `AGENTS.md`: operation rules, safety boundaries, heartbeat/external-action policy
- `SOUL.md`: values, working principles, boundaries, style
- `IDENTITY.md`: name, type, vibe, emoji, avatar convention
- `BOOTSTRAP.md`: first-conversation script and initialization steps
- `USER.md`: addressing, timezone, preferences, taboos, work/life context
- `STYLE.md`: tone, length preference, banned words, output format preference

## 6) Failure handling

- Conflicting user inputs: point out conflicts and offer 2 concrete revision options.
- Too-short answers: provide a minimal viable template, then request missing details.
- Scope change mid-way: reconfirm scope, then continue serial processing.
- Write failure: report exact path + error and provide retry command.
