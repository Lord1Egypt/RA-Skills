# LINLAN AI Development Assistant Reference

[中文](./README.md)

Version: `v1.0.2-linlan` | Release: 2026-09

This reference package supports LINLAN's AI pilot projects, compatible with **Trae**, **CodeBuddy**, **Claude Code**, and **opencode**. Its goal is to reduce the context preparation cost for AI-assisted development tasks, helping users document requirements, design, testing, review, and evaluation materials without altering existing development workflows.

---

## File Index

### Root Directory

| File | Description |
|---|---|
| [AGENTS.md](./AGENTS.md) | Project-level AI assistant reference (opencode native, includes LINLAN pilot project references) |
| [CLAUDE.md](./CLAUDE.md) | Claude Code bridge file (includes company tech stack) |
| [VERSION.md](./VERSION.md) | Version, compatibility, and distribution notes |
| [deploy.cmd](./deploy.cmd) | Shortest entry for Windows — **double-click to deploy** (auto-locates `scripts/deploy.ps1`) |
| [deploy.sh](./deploy.sh) | Shortest entry for macOS / Linux (forwards to `scripts/deploy.sh`) |
| [scripts/deploy.ps1](./scripts/deploy.ps1) | One-click deploy script for Windows (full copy + rule placement) |
| [scripts/deploy.sh](./scripts/deploy.sh) | One-click deploy script for macOS / Linux |

### Tool Rule Entries

Rule files ship under `rules/` (non-hidden), and are copied/renamed into the project's dot-directories during deployment:

| Tool | Packaged File | Target Project Path | Description |
|---|---|---|---|
| Trae | [rules/trae-poc-rule.md](./rules/trae-poc-rule.md) | `.trae/rules/poc-rule.md` | Auto-load after copy + rename |
| CodeBuddy | [rules/codebuddy-poc-rule.md](./rules/codebuddy-poc-rule.md) | `.codebuddy/rules/poc-rule.md` | Auto-load after copy + rename |

### AI Pilot Main

| File | Description |
|---|---|
| [ai-pilot/README.md](./ai-pilot/README.md) | Reference package overview and directory guide |

### Standard Templates (`ai-pilot/standards/`)

| File | Purpose |
|---|---|
| [00-ai-usage-rule.md](./ai-pilot/standards/00-ai-usage-rule.md) | AI usage rules overview |
| [01-requirement-spec-template.md](./ai-pilot/standards/01-requirement-spec-template.md) | Requirement specification template |
| [02-design-template.md](./ai-pilot/standards/02-design-template.md) | Technical design template |
| [03-api-design-template.md](./ai-pilot/standards/03-api-design-template.md) | API design template |
| [04-db-design-template.md](./ai-pilot/standards/04-db-design-template.md) | Database design template |
| [05-test-case-template.md](./ai-pilot/standards/05-test-case-template.md) | Test case template |
| [06-code-review-template.md](./ai-pilot/standards/06-code-review-template.md) | Code review template |
| [07-release-note-template.md](./ai-pilot/standards/07-release-note-template.md) | Release note template |
| [08-ai-usage-record-template.md](./ai-pilot/standards/08-ai-usage-record-template.md) | AI usage record template |
| [09-poc-evaluation-template.md](./ai-pilot/standards/09-poc-evaluation-template.md) | POC evaluation template |
| [10-prompt-guide.md](./ai-pilot/standards/10-prompt-guide.md) | Prompt writing guide |
| [11-context-1week-template.md](./ai-pilot/standards/11-context-1week-template.md) | 1WEEK task context template |
| [12-context-3day-template.md](./ai-pilot/standards/12-context-3day-template.md) | 3DAY task context template |
| [13-context-1day-template.md](./ai-pilot/standards/13-context-1day-template.md) | 1DAY task context template |
| [14-test-execution-log-template.md](./ai-pilot/standards/14-test-execution-log-template.md) | Test execution log template |

### Quick Command Workflows (`ai-pilot/reference/workflows/`)

| Command | File | Description |
|---|---|---|
| Init Project | [00-init-project.md](./ai-pilot/reference/workflows/00-init-project.md) | Scan config and prefill project info |
| Start Task | [01-start-task.md](./ai-pilot/reference/workflows/01-start-task.md) | Create task directory and base artifacts |
| Clarify Requirements | [02-prepare-requirement.md](./ai-pilot/reference/workflows/02-prepare-requirement.md) | Generate or update requirement docs |
| Start Design | [03-prepare-design.md](./ai-pilot/reference/workflows/03-prepare-design.md) | Generate or update technical design |
| Write Test Cases | [04-prepare-test-cases.md](./ai-pilot/reference/workflows/04-prepare-test-cases.md) | Generate or update test cases |
| Start Coding | [05-start-coding.md](./ai-pilot/reference/workflows/05-start-coding.md) | Implement code based on task context |
| Run Tests | [06-run-tests.md](./ai-pilot/reference/workflows/06-run-tests.md) | Run minimal necessary test suite |
| Code Review | [07-code-review.md](./ai-pilot/reference/workflows/07-code-review.md) | Risk review based on diff |
| Finish Task | [08-finish-task.md](./ai-pilot/reference/workflows/08-finish-task.md) | Supplement AI usage record and completeness check |
| Generate Summary | [09-generate-summary.md](./ai-pilot/reference/workflows/09-generate-summary.md) | Generate pilot summary from task artifacts |

### Reference Materials (`ai-pilot/reference/`)

| File | Description |
|---|---|
| [quick-commands.md](./ai-pilot/reference/quick-commands.md) | Quick command reference card |
| [metrics-definition.md](./ai-pilot/reference/metrics-definition.md) | Evaluation metrics definitions |
| [summary-template.md](./ai-pilot/reference/summary-template.md) | Phase review template |
| [gitignore.template](./ai-pilot/reference/gitignore.template) | Security gitignore reference |
| [pre-commit-config.yaml](./ai-pilot/reference/pre-commit-config.yaml) | Gitleaks pre-commit reference |

---

## Task Artifacts Directory

Real task artifacts should be placed in:

```
ai-pilot/poc/{task_id}/
```

Standard task artifacts:

| File | Purpose |
|---|---|
| `context.md` | Task context index |
| `requirement.md` | Requirement background, scope, acceptance criteria |
| `design.md` | Technical solution, impact scope, key flows |
| `api-design.md` | API definitions, request/response, error codes |
| `db-design.md` | Table structure, fields, indexes, migration strategy |
| `test-cases.md` | Functional, exception, boundary, regression tests |
| `test-execution-log.md` | Test execution log |
| `review-summary.md` | Code review summary |
| `release-note.md` | Release content, impact, rollback plan |
| `ai-usage-record.md` | AI usage process, adoption rate, efficiency metrics |

---

## Task Complexity Levels

| Level | Use Case | Recommended Artifacts |
|---|---|---|
| **1WEEK** (>3 days) | New features, architecture changes, cross-system refactoring | Full context + 8 core files |
| **3DAY** (1-3 days) | Medium requirements, API development | Simplified context + 5 core files |
| **1DAY** (<1 day) | Bug fixes, config changes | review-summary + ai-usage-record |

---

## Quick Start

### One-Click Deploy (Recommended)

Pick whichever is easiest for you — from most foolproof to most explicit:

| Option | What to do | Best for |
|---|---|---|
| **Just ask the AI** | In the project, say "deploy assist-skills into this project" | Everyone (recommended) |
| **Double-click** | When the package is vendored inside the project, double-click `deploy.cmd` — zero input; otherwise it prompts for the target directory | People who avoid terminals |
| **Send to** | Run `deploy.cmd -Shortcuts` once, then right-click any project folder → Send to → 部署AI开发助手(assist-skills) | People who never want to type |
| **One command line** | See the code blocks below | Terminal users |

```cmd
:: Windows: deploy.cmd in the package root auto-locates scripts\deploy.ps1
"%USERPROFILE%\.openclaw\workspace\skills\assist-skills\deploy.cmd" D:\your-project
```

```bash
# macOS / Linux
bash ~/.openclaw/workspace/skills/assist-skills/deploy.sh --target ~/my-project
```

You can also set up an alias once (`function ai-deploy { & "$HOME\.openclaw\workspace\skills\assist-skills\deploy.cmd" @args }` / `alias ai-deploy="bash ~/.openclaw/workspace/skills/assist-skills/deploy.sh"`), then just run `ai-deploy D:\your-project`.

### Team Distribution: Make the Project Self-Contained

The project owner runs this once:

```cmd
:: Deploy + vendor the package into <project>\tools\assist-skills
deploy.cmd -Target "D:\your-project" -Vendor
```

After committing, **teammates simply double-click `tools\assist-skills\deploy.cmd`** (zero input) to finish setup — no ClawHub install, no commands, no aliases. Use `-VendorDir` to change the location (default `tools\assist-skills`).

The script copies the entire package into the target project root and renames `rules/*.md` into `.trae/rules/poc-rule.md` and `.codebuddy/rules/poc-rule.md`. Existing files are skipped by default; use `-DryRun` / `--dry-run` to preview first.

### Manual Deploy

1. Copy the package contents into the project root (`AGENTS.md`, `CLAUDE.md`, `VERSION.md`, `ai-pilot/`, `rules/`)
2. For Trae / CodeBuddy, copy and rename `rules/trae-poc-rule.md` and `rules/codebuddy-poc-rule.md` to `.trae/rules/poc-rule.md` and `.codebuddy/rules/poc-rule.md`
3. In the AI chat, enter `Initialize Project` to let AI scan and prefill `AGENTS.md` sections 1-4
4. Add business context, confirm AI inferences, then start using AI tools

---

## Usage Boundaries

- Do not place production keys, tokens, connection strings, or sensitive data in this package
- Not all tasks need all 8 files; tailor to task complexity
- AI output should go through review, build checks, and test verification before delivery