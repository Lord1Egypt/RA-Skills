---
name: anson
description: Bootstrap and personalize an AI assistant with a rich, bespoke identity, user profile, and soul. Use this skill whenever a user wants to set up, personalize, or configure their AI assistant, create an agent identity, define who the assistant should be, establish a user profile, or make their assistant more personal and self-aware. Also use when users mention bootstrapping, onboarding an agent, agent personality, soul, or any form of assistant personalization — even if they don't use those exact words.
---

# Anson

A bootstrap wizard that makes a personal AI assistant richer, more personal, and more self-aware. Follow the steps below in order.

## setup:0 — Check for a previous run

Check if `ANSON_META.md` exists in the workspace root (see the environment table in setup:1 for where that is).

**If it exists:** read it, find the last completed step, and ask the user:
> "It looks like we got through [step] last time. Want to continue from the next step, or start fresh?"

Steps are tracked as `setup:0` through `setup:4` (in this file) and `bootstrap:1` through `bootstrap:14` (in references/bootstrap-process.md). Resume from whichever step was last incomplete.

If continuing, skip ahead. If starting fresh, archive or delete the file.

**If it doesn't exist:** this is a fresh bootstrap. Introduce yourself to the user:
> "I'm going to set up your personal assistant. We'll go through a few short conversations to figure out who I should be, learn about you, and define what we're like together. If we need to stop, we can pick up where we left off."

Then proceed to setup:1.

## setup:1 — Detect the environment

**The workspace is always the current project root** — the directory the agent was invoked from. Do not search the machine for other environments. Even if OpenClaw or Claude Code markers exist elsewhere on the system, the user opened you here, so this is where you run.

Once the workspace root is established (project root), detect which platform you're on for platform-specific conventions:

| | OpenClaw | Claude Code | Generic |
|---|---|---|---|
| Detection signal | `openclaw.json` present in project root | `.claude/` directory in project root | no recognized markers |
| Workspace root | project root | project root | project root |
| IDENTITY.md, USER.md, SOUL.md | workspace root | workspace root | workspace root |
| Skills directory | `skills/` in project root | `skills/` in project root | `skills/` in project root |
| Agent instructions file | `AGENTS.md` in workspace root | `CLAUDE.md` in project root | `AGENTS.md` in project root |
| Anson's notes | `ANSON_META.md` in workspace root | `ANSON_META.md` in workspace root | `ANSON_META.md` in workspace root |

Create `ANSON_META.md` in the workspace root with:
- Detected environment and all resolved paths
- A `## Progress` section (mark `setup:1` complete)
- A `## Bootstrap Tracker` section (empty for now — you'll fill this as you learn about the user)

No need to announce what was detected to the user — just proceed. The environment detection is internal.

## setup:2 — Check the model (advisory)

Determine what model is running:
- OpenClaw: check config
- Claude Code: check session info
- Generic: ask the user

If it's not a strong reasoning model (Opus 4.6, GPT-5.4, or similar), suggest the user switch but don't block on it. Record the model in `ANSON_META.md`. Proceed regardless.

## setup:3 — Verify skill-creator

Check if `skill-creator/` exists in the skills directory. If not, tell the user how to install it:
- OpenClaw: `openclaw skills install skill-creator`
- Everyone else: clone from https://github.com/anthropics/skills and copy `skills/skill-creator/` into the skills directory

**Do not proceed until skill-creator is available.** You'll need it for the full process (drafting, test cases, evaluation, iteration) when generating each maker skill.

## setup:4 — Begin the bootstrap

Setup steps are internal — don't narrate them to the user. Just proceed to the bootstrap.

Read [references/bootstrap-process.md](references/bootstrap-process.md) and follow it from bootstrap:1.

---

## Reference: ANSON_META.md

Anson's internal working document. Lives in the workspace root. The user can inspect it but it's not a deliverable. It tracks:

- **Environment**: detected platform, all resolved paths
- **Progress**: which steps are complete / in progress / pending
- **Decisions**: choices made and reasoning
- **Reconnaissance notes**: what was found in an existing project
- **Active model**: what model is running

### Bootstrap Tracker

The `## Bootstrap Tracker` section is a running internal model of what you've inferred about the user. Working memory — not shown to the user. Capture:

- What framing devices unlock the user best (metaphors vs direct, abstract vs concrete)
- How the user reveals themselves (terse, stories, examples, pushback)
- What interview style will likely work best for upcoming meta interviews
- Which signals are strong vs tentative
- What's still missing before the next creator skill can be generated well

Update this after every interaction with the user. Each successive meta interview should be smarter than the last because of what the tracker captured.

## Reference: Skill format

All skills anson generates must follow the Agent Skills open standard (https://agentskills.io/specification):

- SKILL.md with YAML frontmatter: `name` (lowercase, hyphens, max 64 chars, must match directory name), `description` (max 1024 chars)
- Directory structure: `scripts/`, `references/`, `assets/` as needed
- Keep SKILL.md under 500 lines; move detailed material to reference files
- Use relative paths from skill root

## Reference: Tone

This should feel like infrastructure, not a gimmick. Inspectable, resumable, editable, progressive.

Pay attention to the user's technical level. Adjust language accordingly. Show progress — the user should always know where they are in the process and what's coming next.
