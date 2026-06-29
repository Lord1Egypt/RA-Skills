---
name: auto-skill-installer
description: "Understand a user or agent capability need, discover relevant Codex/agent skills, choose the best candidate, install it, and verify the installation. Use when a user asks what skill to install, asks to automatically find/install skills, describes a task that may require a missing specialized skill, or when an agent notices it lacks a reusable capability during a task."
---

# Auto Skill Installer

## Overview

Act as a skill acquisition router: translate the need into search terms, check already installed skills, search trusted skill sources, inspect candidates before installation, install the best fit when confidence is high, and tell the user what changed.

Prefer installing one high-quality skill that directly unlocks the request over installing many adjacent skills.

## Workflow

### 1. Understand the Need

Extract:

- Domain: product, design, QA, deployment, data, documents, browser automation, etc.
- Task: what the user or agent needs to do repeatedly.
- Environment: Codex, Claude/agent skills ecosystem, local repo, private GitHub, or known plugin/tool.
- Urgency: whether the user asked for automatic install or only recommendations.

If the user explicitly names a skill, skip broad discovery and verify/install that skill.

### 2. Check Existing Skills First

Do not install duplicates. Check the current skill metadata in context, then inspect likely local skill roots when available:

```bash
find "${CODEX_HOME:-$HOME/.codex}/skills" "$HOME/.agents/skills" .agents/skills -maxdepth 2 -name SKILL.md 2>/dev/null
```

If a suitable skill is already installed, tell the user which one to use. If it was installed during the current session, remind them to restart Codex before relying on auto-triggering.

### 3. Search Skill Sources

Search from most trusted/specific to broadest:

1. Current local skills and system skills.
2. Platform-native registries: OpenClaw ClawHub via `openclaw skills search`, Hermes registries via `hermes skills search`, OpenAI curated/experimental via the installed `skill-installer` skill scripts.
3. The broader open agent skills ecosystem via `npx skills find <query>` when available.
4. GitHub repo/path or local skill directory provided by the user.

Try 2-3 focused searches before concluding there is no good candidate. Use concrete terms from the task, then synonyms:

```bash
npx skills find "react performance"
openclaw skills search "qa browser testing"
hermes skills search "qa browser testing"
```

OpenClaw-specific discovery:

```bash
openclaw skills list --json
openclaw skills check --json
openclaw skills info <name> --json
```

Hermes-specific discovery:

```bash
hermes skills list
hermes skills inspect <identifier>
```

Networked commands require normal Codex approval when sandboxed. OpenClaw commands may also need permission to update `~/.openclaw/state`.

### 4. Inspect and Rank Candidates

Before installing an external skill, inspect its metadata and source when possible. Prefer candidates with:

- Direct match to the requested task, not just the broad domain.
- Clear `SKILL.md` frontmatter and concise workflow.
- Trusted source: platform bundled/curated skills, OpenClaw ClawHub verified skills, user's own repos, known vendor/org, or active public repo.
- Minimal dependencies and no surprising install-time side effects.
- No requests for secrets, credentials, or broad filesystem/network access unrelated to the skill.

Avoid installing:

- Skills that mainly duplicate an installed one.
- Skills with vague descriptions or no visible instructions.
- Bundles that execute opaque setup scripts during install unless the user explicitly accepts the risk.
- Plugins/connectors when the user asked for a skill; use plugin installation tools only when the user explicitly asks for a plugin/connector.

### 5. Decide Whether to Install Automatically

Install without asking an extra question only when all are true:

- The user asked to automatically install, or the agent needs the skill to complete the current task.
- One candidate is clearly best.
- The source is trusted enough for the task.
- The installation command will not perform surprising writes outside the normal skills directory.

Otherwise present a short ranked list with a recommendation and wait for the user's choice.

### 6. Install

Use the installer that matches the source:

```bash
# OpenClaw: ClawHub slug into active workspace
openclaw skills install <slug>

# OpenClaw: local skill directory into active workspace
openclaw skills install /path/to/skill --as <slug>

# OpenClaw: shared managed install visible to all local agents
openclaw skills install /path/to/skill --as <slug> --global

# OpenClaw: git source
openclaw skills install git:<owner>/<repo>@<ref> --as <slug>

# Hermes: registry/GitHub/URL skill
hermes skills install <identifier> --yes

# skills.sh / agent skills package
npx skills find "react performance"
npx skills add <owner/repo@skill> -g -y

# OpenAI curated or experimental skill paths
python3 /path/to/skill-installer/scripts/install-skill-from-github.py --repo openai/skills --path skills/.curated/<skill-name>
```

OpenClaw notes:

- `openclaw skills install` expects a skill directory root containing `SKILL.md` for local installs.
- Without `--global`, OpenClaw installs into the active agent workspace `skills/` directory.
- With `--global`, OpenClaw installs into the shared managed directory, usually `~/.openclaw/skills`.
- `--agent <id>` targets one configured OpenClaw agent workspace.
- OpenClaw installation is not the same as model visibility. Run `openclaw skills check --json`; if `blockedByAgentFilter` is true, update the target agent skill allowlist/config before expecting automatic model injection.
- Changes may require a new OpenClaw session or a skill watcher refresh before the agent sees them.

Hermes notes:

- `hermes skills install` accepts registry identifiers and direct HTTP(S) URLs to `SKILL.md`.
- For local development, a category folder under `~/.hermes/skills/<category>/<skill-name>` is the observed local layout.

When `skill-installer` is available, read its `SKILL.md` for exact helper script paths and current options. If an install command fails because of sandboxed network access, rerun it with the required Codex escalation flow rather than inventing a workaround.

### 7. Verify and Report

After installation:

1. Confirm the destination skill directory exists.
2. Check `SKILL.md` has valid `name` and `description` frontmatter.
3. If the skill came from a GitHub path, confirm the installed folder name matches the skill name or explain the alias.
4. Tell the user: `Restart Codex to pick up new skills.`
5. Continue the original task with the best available capability if a restart is required before the new skill can auto-trigger.

## Response Pattern

Use concise, action-oriented updates:

- "I found an existing installed skill: ..."
- "Best match: ... because ..."
- "Installed: ... Restart Codex to pick up new skills."
- "I did not find a trustworthy skill for this; I can solve the task directly or help create one."

## Failure Modes

If no skill is found, do not force an install. Offer to complete the task directly and, if the task is recurring, create a new custom skill.

If multiple skills are close, recommend one and explain the tradeoff in one sentence.

If installation is blocked by network, permissions, auth, or sandbox approval, explain the exact blocker and provide the command that would complete the install.
