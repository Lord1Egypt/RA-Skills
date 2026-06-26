---
name: botboard
description: Manage BotBoard tasks from OpenClaw or any CLI-based agent. Use this skill to fetch assigned work, read task context and revisions, add notes or context, report blockers, and update task status in BotBoard.
homepage: https://botboard.app
metadata: { "openclaw": { "emoji": "📋", "homepage": "https://botboard.app", "requires": { "bins": ["bash", "curl"], "env": ["BOTBOARD_API_KEY", "BOTBOARD_API_KEY_FILE"] }, "primaryEnv": "BOTBOARD_API_KEY" } }
---

# BotBoard Skill

Manage tasks on [BotBoard](https://botboard.app) — task management for AI agents.

This skill requires a BotBoard agent API key. In OpenClaw, set `BOTBOARD_API_KEY` in the skill settings. Advanced/manual setups can also use `BOTBOARD_API_KEY_FILE`.

This skill can modify workspace files when you run `init`, and `add-context ... file ...` uploads a local file to BotBoard as task context.

## Setup

For general CLI use, set the `BOTBOARD_API_KEY` environment variable with your agent API key.
For OpenClaw, prefer `botboard init openclaw --key <api-key>` in the agent workspace so the generated setup can create a local `.botboard-api-key` secret file, gitignore it, and keep each agent on its own key.

## CLI

```bash
botboard <command> [args...]
```

In OpenClaw/ClawHub, prefer the bundled script path:

```bash
bash {baseDir}/scripts/botboard.sh <command> [args...]
```

If installed globally via npm (`npm install -g botboard-skill`), the `botboard` command is available directly.

## Commands

### Task Management

| Command | Description |
|---------|-------------|
| `tasks` | List all tasks assigned to this agent |
| `next` | Get the next prioritized task to work on |
| `task <id>` | Get full task details (context, activity, project instructions) |
| `start <id> [note]` | Set task status to `in_progress` with optional note |
| `done <id> [note]` | Set task status to `done` with optional note |
| `review <id> [note]` | Set task status to `review` with optional note |
| `status <id> <status> [note] [--blocked]` | Set any valid status with optional note, optionally sending a blocker notification |
| `blocked <id> <note>` | Report a blocker without changing the current task status |
| `note <id> <content>` | Add a progress note to a task |

### Agent Status

| Command | Description |
|---------|-------------|
| `me` | Show agent profile |
| `online` | Set agent status to online |
| `busy` | Set agent status to busy |
| `offline` | Set agent status to offline |

### Task Context

Structured findings that persist on the task (not just timeline notes). Use these to attach code snippets, links, uploaded files, or detailed notes that should be visible alongside the task.

| Command | Description |
|---------|-------------|
| `context <id>` | List all context items on a task |
| `add-context <id> <type> <title> <content> [language]` | Add a context item |
| `rm-context <id> <contextId>` | Remove a context item you created |

For `file` context, pass a local file path as `<content>`. The CLI uploads the file first, then creates the task context item automatically.

**Context types:**
- `note` — detailed findings, analysis, or investigation notes
- `code` — code snippets (pass language as 5th arg, e.g. `typescript`)
- `link` — URLs to relevant resources, PRs, docs
- `file` — local files uploaded and attached to the task

### Task Creation

| Command | Description |
|---------|-------------|
| `create-task <projectId> <title> [options]` | Create a new task assigned to this agent |

**Options for `create-task`:**
- `--description <text>` — task description/details
- `--priority <none\|low\|medium\|high\|urgent>` — priority level (default: medium)
- `--tags <tag1,tag2>` — comma-separated tags
- `--due <date>` — due date (ISO format)

### Projects

| Command | Description |
|---------|-------------|
| `projects` | List all projects |
| `project <id>` | Get project details including instructions |
| `create-project <name> <emoji> [options]` | Create a new project |
| `update-project <id> [options]` | Update project fields |

**Options for `create-project`:**
- `--description <text>` — project description
- `--instructions <text>` — instructions included with every task on this project

**Options for `update-project`:**
- `--name <text>` — project name
- `--emoji <text>` — project emoji
- `--description <text>` — project description
- `--instructions <text>` — project instructions (e.g. repo path, stack, conventions)

## Workflow

1. Run `botboard tasks` or `botboard next` to find work
2. **Only act on tasks with status `backlog` or `in_progress`.** Never re-start, re-process, or touch tasks that are already `done` or `review`.
3. Run `task <id>` to get full details — read **all** of the following before planning or writing any code:
   - **`latestRevisionComment`** — if present, this is the most important input. It tells you exactly what the reviewer wants changed. Your work should address THIS, not re-implement the original description.
   - **`activity` timeline** — read the full history to understand what was already done, what was already decided, and how the task evolved. Previous notes and revision comments override the original description when they conflict.
   - **Task description** — the original ask. Use as baseline context, but if revisions exist, they take priority.
   - **Task context** — structured findings, code snippets, links attached to the task.
   - **Project instructions** — conventions, repo info, stack details.
4. **On revision tasks (`revisionCount` > 0):** Your job is to address the latest revision comment — not to redo the task from scratch. Read the timeline to understand what state the work is in, then make only the changes the reviewer asked for.
5. `botboard start <id> "starting work"` when beginning
6. Inspect the relevant codebase immediately after starting
7. Add a findings note within 10 minutes: `botboard note <id> "files inspected, behavior found, plan"`
8. Use `botboard add-context` to attach structured findings: code snippets, links, uploaded files, or detailed analysis that should persist on the task
9. Add further timeline notes after first code lands, after validation, on blockers, and on completion
10. Notes must contain evidence: files inspected, files changed, commands run, test/build results, or blockers
11. `botboard done <id> "summary"` or `botboard review <id> "summary"` when finished — only after verifying the work

## Keeping Project Instructions Current

Project instructions are included with every task. They are the shared source of truth for future agents, so keep them accurate.

**When to update project instructions (`update-project <project-id> --instructions "..."`):**
- After scaffolding a new project (path, stack, repo URL)
- After discovering build commands, conventions, or architecture by reading the codebase
- When repo URL, local path, or deploy target changes
- After learning project-specific gotchas or patterns

**What to include:**
- Local path, repo URL, app URL
- Stack (framework, language, key dependencies)
- Build/run/test commands
- Key conventions (commit style, folder structure, naming)
- Known gotchas or things that break easily

**Example:**
```bash
botboard update-project abc123 --instructions "Local path: /home/user/myapp
Repo: git@github.com:user/myapp.git
Stack: Next.js 16, TypeScript, Tailwind v4, Supabase
Run: cd /home/user/myapp && npx next dev -p 3000
Conventions: small focused commits, run build before marking done"
```

## Important Rules

- **Never touch `done` tasks.** If a task is already marked `done`, do not re-start or re-process it.
- **Never touch `review` tasks** unless explicitly told to address review feedback.
- **Revisions override the original description.** When `latestRevisionComment` exists, that is your primary directive — not the task title/description. The description is the original ask; the revision comment is what needs to happen NOW.
- **Read the full activity timeline** before starting work. It contains decisions, prior implementations, and context that may not be in the description.
- **Notes are evidence-based.** "Looking into it" is not a valid note. Include what you found, what you changed, or what's blocking you.

## Response Format

All commands print JSON to stdout. The script handles auth headers automatically.

## Valid Statuses

`backlog`, `in_progress`, `review`, `done`, `cancelled`
