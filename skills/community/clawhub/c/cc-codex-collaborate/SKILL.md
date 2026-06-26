---
name: cc-codex-collaborate
version: 0.1.13
description: Coordinate Claude Code and Codex in a milestone-based collaboration loop. Claude Code discovers the project, plans, implements, and fixes; Codex performs adversarial planning review and read-only milestone review. Working documents are stored under docs/cccc.
argument-hint: "[task description]"
---

# cc-codex-collaborate

You are Claude Code acting as the primary orchestrator and implementer.

Use this skill when the user wants Claude Code and Codex to collaborate on a coding task through project discovery, adversarial planning review, milestone implementation, Codex review, and iterative fixes.

The working document root is always:

```text
docs/cccc
```

Do not use `.agent-loop` for this skill.

## First-run setup

The first user-facing action after installation should be:

```text
/cc-codex-collaborate setup
```

Setup is an **interactive configuration wizard** conducted by Claude Code (you). It does NOT start any task, does NOT enable hooks, and does NOT modify `.claude/settings.json`.

### Setup wizard flow

When invoked with `setup`, you must conduct the interactive wizard in the user's primary language. Follow this flow:

#### 1. Detect user language

Detect the user's primary language from:
1. Explicit user preference
2. The language of the current message
3. If unclear, default to the language of the most recent user message

#### 2. Opening message

Display in the user's language:

> I will initialize cc-codex-collaborate for this project. This generates `.claude/commands` and `docs/cccc`, but does not enable hooks or start any task.

#### 3. Handle existing config first

If `docs/cccc/config.json` already exists, ask the user before proceeding:

> A. Keep existing config, only fill missing files
> B. Interactively update parts of the config
> C. Backup and rebuild config
> D. Exit

If C is chosen, backup to `docs/cccc/backups/config.<timestamp>.json` before proceeding.

If A is chosen, run `cccc-setup.sh keep [language]` and skip the preset selection.

#### 4. Ask configuration mode (only if no existing config, or user chose B/C)

Present choices using `AskUserQuestion`:

> A. Quick setup: recommended defaults for most projects (recommended)
> B. Strict setup: stronger review, smaller milestones, easier to pause
> C. Custom setup: configure thresholds and behavior step by step
> D. Import config: from existing `docs/cccc/config.json` or template
> E. Exit setup

Default: A.

#### 5. Preset details

**A. Quick / recommended preset:**
- mode: supervised-auto
- max_plan_review_rounds: 3
- max_milestones_per_run: 5, max_diff_lines: 1200, max_changed_files: 20
- max_review_rounds_per_milestone: 3, max_fix_attempts: 3
- block_on_p0: true, block_on_p1: true, allow_continue_with_p2: true
- stop_hook_loop_enabled: false

**B. Strict preset:**
- mode: supervised-auto
- max_plan_review_rounds: 4
- max_milestones_per_run: 3, max_diff_lines: 600, max_changed_files: 10
- max_review_rounds_per_milestone: 4, max_fix_attempts: 2
- block_on_p0: true, block_on_p1: true, allow_continue_with_p2: false
- stop_hook_loop_enabled: false

**C. Custom setup — ask these questions one at a time:**

1. **User language**: A. Auto detect (recommended) B. 简体中文 C. English D. Other
2. **Collaboration mode**: A. manual B. supervised-auto (recommended) C. full-auto-safe D. Custom
3. **Planning review strength**: A. Standard (recommended) B. Strict (4 rounds) C. Very strict (5 rounds, ask on any uncertainty) D. Custom
4. **Milestone granularity**: A. Small steps (600 diff, 10 files) B. Standard (1200 diff, 20 files) (recommended) C. Large steps (2500 diff, 40 files) D. Custom
5. **Review thresholds**: max review rounds (default 3), max fix attempts (default 3), block P1 (default yes), allow P2 (default yes)
6. **Auto loop**: A. Not enabled (recommended) B. Decide later C. Enable now (warning: changes Claude Code stop behavior)

If the user chooses "Enable now" for auto loop, warn that stop-hook will change Claude Code's stop behavior, and ask for explicit confirmation before modifying `.claude/settings.json`. Default recommendation: don't enable now, use `/cc-codex-collaborate-loop-start` later.

**D. Import**: Use existing `docs/cccc/config.json` as-is, or use recommended defaults if no config found.

#### 6. Execute setup script

After gathering the user's choices, build the config and run:

```bash
# For quick/strict presets:
.claude/skills/cc-codex-collaborate/scripts/cccc-setup.sh recommended [language]
.claude/skills/cc-codex-collaborate/scripts/cccc-setup.sh strict [language]

# For custom config, write JSON to a temp file and pipe it:
cat /tmp/cccc-custom-config.json | .claude/skills/cc-codex-collaborate/scripts/cccc-setup.sh custom [language]

# For import/keep:
.claude/skills/cc-codex-collaborate/scripts/cccc-setup.sh import [language]
.claude/skills/cc-codex-collaborate/scripts/cccc-setup.sh keep [language]
```

#### 7. Setup summary

After the script completes, output a summary in the user's language:

- List generated files
- List preserved files (not overwritten)
- List what was NOT enabled (hooks, settings.json)
- Show current configuration (mode, language, review rounds, diff lines, file limit, sensitive ops policy)
- Show next steps:
  - Start a task: `/cc-codex-collaborate "your free-form task description"`
  - Check loop status: `/cc-codex-collaborate-loop-status`
  - Enable auto-continuation: `/cc-codex-collaborate-loop-start`

Setup should explain:

- generated command files
- generated `docs/cccc` files (including config.json and state.json)
- that hooks were not enabled
- that loop automation can be enabled later with `/cc-codex-collaborate-loop-start`
- current configuration summary (mode, language, thresholds)

## Configuration presets

Setup offers three configuration presets:

### A. Recommended (default)

Standard settings for most projects: `supervised-auto` mode, 3 review rounds, 1200 diff lines, 20 files per milestone, P1 blocks, P2 allowed.

### B. Strict

For high-risk projects: 4 review rounds, 600 diff lines, 10 files, 4 review rounds per milestone, 2 fix attempts, P2 also blocks.

### C. Custom

Step-by-step configuration of: language, mode, planning review strength, milestone granularity, review thresholds, and auto-loop behavior.

## Config vs State

`docs/cccc/config.json` is the project-level configuration. It stores:

- language settings
- collaboration mode
- planning thresholds
- milestone granularity
- review thresholds
- automation settings
- safety policies
- codex behavior

`docs/cccc/state.json` is runtime state only:

- current milestone
- current status
- review round counts
- pause reason
- completed/blocked milestones
- last context update
- loop continuation count

All planning, review, and milestone thresholds must read from `config.json`. If `config.json` does not exist, prompt the user to run setup first.

## Command bootstrap model

The release zip should not require users to copy `.claude/commands/`, `.claude/hooks/`, or `docs/cccc/` manually.

The zip includes only the skill, scripts, prompts, schemas, hooks templates, and command templates.

Runtime generation rules:

- `/cc-codex-collaborate setup` generates `.claude/commands/` and `docs/cccc/` (including config.json and state.json). It does NOT generate `.claude/hooks/` or modify `.claude/settings.json`.
- `/cc-codex-collaborate-loop-start` generates `.claude/hooks/`, updates `.claude/settings.json`, sets `config.json` `automation.stop_hook_loop_enabled` to `true`, and sets `state.json` mode to `full-auto-safe`.
- `/cc-codex-collaborate-loop-stop` removes only this skill's hook registrations from `.claude/settings.json`, sets `config.json` `automation.stop_hook_loop_enabled` to `false`, and reverts `state.json` mode to `supervised-auto`.

## Loop control commands

After setup, this package provides three explicit slash-command wrappers for loop automation:

- `/cc-codex-collaborate-loop-status`: inspect `docs/cccc/config.json`, `docs/cccc/state.json`, hook files, and `.claude/settings.json` hook registrations.
- `/cc-codex-collaborate-loop-start`: enable full-auto-safe loop continuation by installing cccc hook scripts into `.claude/hooks`, registering them in `.claude/settings.json`, and updating `config.json` automation settings. If an active workflow exists, immediately continue the state machine. If no workflow exists, prompt the user to start a task. If the workflow is paused, suggest `/cc-codex-collaborate resume`.
- `/cc-codex-collaborate-loop-stop`: disable loop automation by removing only cccc hook registrations from `.claude/settings.json` and updating `config.json` to disable the loop.

Do not enable Stop-hook automation implicitly. The user must explicitly run `/cc-codex-collaborate-loop-start`.

`docs/cccc` is a runtime workspace. It must be generated on first use by setup and should not be required as a pre-copied project directory.

## Subcommand handling

Interpret the first argument after `/cc-codex-collaborate` as a subcommand when it matches one of these values:

- `setup`: run `scripts/cccc-setup.sh`, the interactive configuration wizard. Do not start planning or implementation.
- `update`: run `scripts/cccc-update.sh`, safe workspace migration after skill upgrade. Sync config/state fields, commands, and enabled hooks. Does NOT start any task, does NOT enable hooks, does NOT run Codex review.
- `resume`: resume a paused workflow. See "Resume command" section below.
- `status`: run `scripts/cccc-status.sh` and summarize.
- `loop-status`: run `scripts/cccc-loop-status.sh` and summarize.
- `loop-start`: run `scripts/cccc-loop-start.sh` and summarize.
- `loop-stop`: run `scripts/cccc-loop-stop.sh` and summarize.

If no known subcommand is provided, treat the arguments as the user's coding task. Before doing project discovery or planning, ensure setup has been performed. If `docs/cccc/config.json` is missing, prompt the user to run `/cc-codex-collaborate setup` first.

## Public commands summary

| Command | Purpose |
| --- | --- |
| `/cc-codex-collaborate setup` | First-time setup. Interactive configuration wizard. Generates docs/cccc and .claude/commands. Does NOT enable hooks. |
| `/cc-codex-collaborate update` | Safe migration after skill upgrade. Syncs config/state fields, commands, enabled hooks. Does NOT overwrite user planning/review history. Does NOT enable hooks if not already enabled. |
| `/cc-codex-collaborate force-update` | Force sync regardless of version number. Same as update but ignores version check. |
| `/cc-codex-collaborate resume` | Resume a paused workflow. Does NOT bypass Codex gates, safety pauses, or secret requirements. |
| `/cc-codex-collaborate reset` / `reset state` | Reset state machine runtime state and rehydrate from docs. Does NOT delete planning docs, reviews, or logs. |
| `/cc-codex-collaborate doctor` | Diagnose installation, config, hooks, Codex, gates, and context. Does NOT modify files. |
| `/cc-codex-collaborate rebuild-context` | Rebuild context-bundle.md for Codex. Does NOT modify milestone status. |
| `/cc-codex-collaborate gates` | Show plan/milestone/final/safety gate status. Does NOT modify files. |
| `/cc-codex-collaborate repair` | Auto-fix safe inconsistencies. Backs up before modifying. Does NOT bypass Codex gates or safety pauses. |
| `/cc-codex-collaborate trace` | Show recent state machine events. Does NOT modify files. |
| `/cc-codex-collaborate dev-smoke` | Developer self-test for skill installation. Does NOT modify user files. |
| `/cc-codex-collaborate codex-check` | Check Codex CLI availability. |
| `/cc-codex-collaborate "task"` | Start user's free-form task description. Full collaboration loop. |
| `/cc-codex-collaborate-loop-status` | Show loop/hooks/Codex gates/version status. Includes resume guidance. |
| `/cc-codex-collaborate-loop-start` | Enable stop-hook auto-continuation. If active workflow exists, immediately continue state machine. |
| `/cc-codex-collaborate-loop-stop` | Disable stop-hook auto-continuation. |

## Update command

When invoked with `update`, run:

```bash
.claude/skills/cc-codex-collaborate/scripts/cccc-update.sh
```

When invoked with `force-update`, run:

```bash
.claude/skills/cc-codex-collaborate/scripts/cccc-update.sh --force
```

## Maintenance commands

### reset / reset state

Reset state machine runtime state. Run `cccc-reset.sh`. Uses `cccc-rehydrate-state.py` to infer current milestone from planning docs, reviews, and git history. Does NOT delete planning docs, reviews, or logs. Always creates backup.

### doctor

Diagnose installation, config, hooks, Codex, gates, and context. Run `cccc-doctor.py`. Outputs PASS/WARN/FAIL with fix suggestions. Does NOT modify files.

### rebuild-context

Rebuild context-bundle.md. Run `cccc-build-context.sh`. Does NOT modify milestone status or run Codex.

### gates

Show plan/milestone/final/safety/testing gate status. Run `cccc-gates.py`. Does NOT modify files.

### repair

Auto-fix safe inconsistencies: deprecated state fields, missing hooks, missing commands, recoverable milestone ID, missing context. Run `cccc-repair.sh`. Backs up before modifying. Does NOT bypass Codex gates, safety pauses, NEEDS_SECRET, SENSITIVE_OPERATION, or UNSAFE.

### trace

Show recent state machine events from logs, reviews, and decision log. Run `cccc-trace.py`. Does NOT modify files.

### dev-smoke

Developer self-test: JSON validation, shell syntax, Python compile, core file existence, script executability. Run `cccc-dev-smoke.sh`. Does NOT modify user files.

### codex-check

Check Codex CLI availability. Run `cccc-codex-check.sh`.

## Resume command

When invoked with `resume`, Claude Code must recover a paused workflow without bypassing safety rules.

### Resume flow

1. Read `docs/cccc/config.json` and `docs/cccc/state.json`.
2. Explain why the workflow is paused (status + pause_reason).
3. If the status allows automatic resume (e.g. `READY_TO_CONTINUE`), call `cccc-resume.sh` and continue the state machine.
4. If the status requires user confirmation or answers, use the user's primary language with brainstorm-style options.
5. After user confirms:
   - Write to `docs/cccc/decision-log.md`
   - Update `docs/cccc/open-questions.md` if applicable
   - Update `docs/cccc/state.json`:
     - `previous_status` = old status
     - `status` = `READY_TO_CONTINUE`
     - `resume_reason` = reason for resuming
     - `resume_strategy` = selected strategy
     - `last_resumed_at` = UTC timestamp
     - `stop_hook_continuations` = 0
     - `pause_reason` = null
   - Do NOT mark any milestone as passed.
   - Do NOT mark the task as DONE.
   - Do NOT mark any Codex gate as pass.
6. If `config.mode = full-auto-safe` and `automation.stop_hook_loop_enabled = true`:
   - Resume must immediately continue executing the state machine.
   - Do not just output "resumed" and stop.
7. If `mode != full-auto-safe`:
   - After resume, output next-step suggestions. Do not force auto-continue.

### Safe resume rules by status

**PAUSED_FOR_HUMAN / NEEDS_HUMAN:**
- If `pause_reason` or `open-questions.md` has unanswered questions, ask the user first.
- Brainstorm-style options: A. recommended approach, B. conservative approach, C. skip milestone, D. continue with risk recorded, E. free input.
- After answer: write decision-log, update open-questions, set status to `READY_TO_CONTINUE`.
- Do NOT mark milestone as passed. Must re-enter the appropriate gate (e.g. Codex review).

**PAUSED_FOR_CODEX:**
- Run `cccc-codex-check.sh` first.
- If Codex is still unavailable: remain `PAUSED_FOR_CODEX`, output reason.
- If Codex is available: clear `codex_unavailable_reason`, set status to `READY_TO_CONTINUE`.
- Must re-run the missing Codex gate (plan/milestone/final review). Resume does NOT skip Codex.

**PAUSED_FOR_SYSTEM:**
- Remind user that a system/API error caused the pause.
- Options: A. checked logs, continue, B. view StopFailure logs, C. exit, D. free input.
- User must explicitly confirm. If no confirmation, do not continue.
- On continue: record in decision-log, reset `stop_hook_continuations = 0`, set `READY_TO_CONTINUE`.

**NEEDS_SECRET:**
- Default: cannot resume.
- Remind user: do NOT send real secrets, API keys, wallet private keys, or seed phrases to Claude.
- Options: A. configured locally, continue, B. use mock/dummy/test fixture, C. skip milestone, D. exit.
- If A or B: record decision-log (NO secret values), set `READY_TO_CONTINUE`.
- If C: mark milestone as blocked/skipped, record risk.

**SENSITIVE_OPERATION / UNSAFE:**
- Default: do not auto-resume.
- Options: A. remain paused, B. switch to safe alternative, C. confirm safe local test, D. skip milestone, E. free input.
- Prohibited resume: real money, mainnet transactions, real wallet keys, production deployments, destructive irreversible operations.
- Unless user provides a safe alternative, remain paused.

**FAIL_UNCLEAR / REVIEW_THRESHOLD_EXCEEDED:**
- Options: A. pause for manual intervention, B. extend review budget +1 round, C. record risk and proceed, D. skip milestone, E. free input.
- If B: increase review budget, record decision-log, set `READY_TO_CONTINUE`.
- If C or D: must record known risk. Cannot skip P0/P1 security issues.

### Non-interactive resume

The resume script supports non-interactive arguments:
- `--confirm`: confirm the resume action
- `--strategy recommended`: use recommended approach
- `--strategy mock`: use mock/dummy secrets
- `--strategy skip`: skip current milestone
- `--strategy extend-review`: extend review budget +1

### Resume script

Run:
```bash
.claude/skills/cc-codex-collaborate/scripts/cccc-resume.sh [--confirm] [--strategy <strategy>]
```

The script only updates state and outputs guidance. It does NOT execute Codex review or implement code. The actual continuation is driven by the SKILL.md state machine.

## Role separation

- Claude Code: project discovery, language detection, planning, self-review, implementation, tests, fixes, state management, human-facing communication.
- Codex: independent read-only reviewer, adversarial planning challenger, milestone reviewer, next-milestone critic, final reviewer.
- Human: ambiguous requirements, product decisions, security decisions, secrets, production operations, real money, irreversible actions.

Codex must not directly modify files. Codex reviews using context and returns structured JSON.

## Mandatory Codex Gates

**This is a P0 invariant. Codex review is NEVER optional.**

Rules:

1. Claude Code MUST NOT begin implementation until Codex adversarial plan review has passed.
2. Claude Code MUST NOT mark a milestone as passed until Codex milestone review has passed.
3. Claude Code MUST NOT mark the whole task as completed until Codex final review has passed.
4. If Codex is unavailable, misconfigured, fails to run, or returns invalid JSON, Claude Code MUST pause with status `PAUSED_FOR_CODEX`.
5. Claude Code MUST NOT silently skip Codex review, even for trivial tasks.
6. For trivial tasks, Claude may use a lightweight plan and milestone, but Codex review is still required.
7. Self-checks such as cat, tests, lint, or build are NOT a substitute for Codex review.
8. A milestone can only be marked passed if there is a valid Codex review artifact with `status = pass` for that milestone and review round.
9. If no Codex review artifact exists, the only valid next action is to run Codex review or pause if Codex is unavailable.
10. Any final summary must mention the Codex review file used to approve the milestone.

**Invariants (memorize these):**

```text
No Codex plan review, no implementation.
No Codex milestone review, no milestone pass.
No Codex final review, no task completion.
Codex unavailable means pause, not skip.
```

**Before implementation:**

- Run `.claude/skills/cc-codex-collaborate/scripts/cccc-codex-check.sh` to verify Codex availability.
- Run `.claude/skills/cc-codex-collaborate/scripts/cccc-assert-codex-gates.py assert-plan-approved` to verify plan approval.
- If assertion fails, you MUST pause with `status = PAUSED_FOR_CODEX`.

**Before marking milestone passed:**

- Run `cccc-assert-codex-gates.py assert-milestone-approved`.
- If assertion fails, run `cccc-codex-milestone-review.sh` and wait for result.
- If review fails, fix and re-review. Do NOT skip.

**Before marking task DONE:**

- Run `cccc-assert-codex-gates.py assert-final-approved`.
- If assertion fails, run `cccc-codex-final-review.sh`.
- Only proceed to DONE if final review passes.

## User language rule

Before planning or asking any question, detect the user's primary language.

Detection priority:

1. `config.json` `language.user_language` if not `"auto"`.
2. Explicit user preference.
3. Latest user instruction language.
4. Main task language if the message is mixed.
5. If still unclear, default to the language of the most recent user message.

Store it in `docs/cccc/config.json` as `language.user_language`.

All human-facing output must use `user_language`. Codex may reason in English, but Claude Code must summarize and ask questions in the user's language.

## State machine

```text
SETUP_OR_BOOTSTRAP
  ↓
INIT
  ↓
DETECT_USER_LANGUAGE
  ↓
DISCOVER_EXISTING_PROJECT
  ↓
BUILD_PROJECT_CONTEXT
  ↓
CLAUDE_PLANNING_REVIEW
  ├─ READ_MORE_PROJECT → DISCOVER_EXISTING_PROJECT
  ├─ ASK_HUMAN → PAUSE_FOR_HUMAN
  └─ OK
      ↓
CODEX_ADVERSARIAL_PLAN_REVIEW
  ├─ INSUFFICIENT_CONTEXT → DISCOVER_EXISTING_PROJECT
  ├─ REJECTED_FIXABLE → CLAUDE_REVISE_PLAN
  ├─ NEEDS_HUMAN → PAUSE_FOR_HUMAN
  ├─ UNSAFE → PAUSE_FOR_HUMAN
  └─ APPROVED
      ↓
IMPLEMENT_MILESTONE
      ↓
CLAUDE_SELF_REVIEW
      ↓
CODEX_MILESTONE_REVIEW
  ├─ PASS → RECORD_ACCEPTANCE → PLAN_NEXT_MILESTONE
  ├─ FAIL_FIXABLE → CLAUDE_FIX → CLAUDE_SELF_REVIEW
  ├─ FAIL_UNCLEAR → PAUSE_FOR_HUMAN
  ├─ NEEDS_HUMAN → PAUSE_FOR_HUMAN
  ├─ SENSITIVE_OPERATION → PAUSE_FOR_HUMAN
  └─ MAX_REVIEW_EXCEEDED → THRESHOLD_POLICY

PAUSED_FOR_HUMAN / NEEDS_HUMAN / PAUSED_FOR_SYSTEM
PAUSED_FOR_CODEX / NEEDS_SECRET / SENSITIVE_OPERATION
UNSAFE / FAIL_UNCLEAR / REVIEW_THRESHOLD_EXCEEDED
  ↓ (resume with /cc-codex-collaborate resume)
READY_TO_CONTINUE
  ↓ (re-enter appropriate gate)
  └─→ CODEX_ADVERSARIAL_PLAN_REVIEW / CODEX_MILESTONE_REVIEW / IMPLEMENT_MILESTONE
```

No implementation may start until project discovery is complete and the initial roadmap has passed Claude self-review plus Codex adversarial plan review, unless the human explicitly chooses to override after a pause.

## Thresholds

Thresholds are stored in `docs/cccc/config.json`. Read them from there, not from state.json.

Default thresholds (recommended preset):

```json
{
  "planning": {
    "max_plan_review_rounds": 3
  },
  "milestones": {
    "max_milestones_per_run": 5,
    "max_diff_lines_per_milestone": 1200,
    "max_changed_files_per_milestone": 20
  },
  "review": {
    "max_review_rounds_per_milestone": 3,
    "max_fix_attempts_per_milestone": 3,
    "block_on_p0": true,
    "block_on_p1": true,
    "allow_continue_with_p2": true
  },
  "automation": {
    "stop_hook_loop_enabled": false,
    "max_stop_hook_continuations": 10
  }
}
```

Supported modes:

- `manual`: pause after each major phase.
- `supervised-auto`: default. Planning is strictly reviewed; implementation can loop automatically until risk or threshold.
- `full-auto-safe`: optional Stop hook can continue safe unfinished work, but never bypass hard pause conditions.

## Hard pause conditions

Immediately pause and ask the human if any of these occur:

1. Real wallet private keys, seed phrases, keystores, signing keys, or production API keys are needed.
2. Real production API keys, database passwords, OAuth secrets, SSH private keys, cookies, tokens, or sessions are needed.
3. Real money movement, blockchain transactions, withdrawals, purchases, deployments, or irreversible external actions are needed.
4. Production database, production infrastructure, DNS, IAM, billing, or permission changes are required.
5. Destructive operations are required, including force push, history rewrite, mass delete, dropping databases, or removing important directories.
6. Codex returns `needs_human: true`.
7. Codex cannot determine a safe next step.
8. Requirements are ambiguous and continuing would create product, security, financial, architecture, or data-loss risk.
9. The same milestone exceeds `max_review_rounds_per_milestone` from config.
10. Claude Code and Codex disagree on whether the result is safe.
11. Real user data or credentials would be exposed to a model, log, test, or third-party service.
12. Project context is missing or stale and cannot be reconstructed by reading the repository.

Never ask the user to paste real secrets into chat. Ask them to configure secrets locally in a sandboxed environment.

## Brainstorming and human-question gate

When clarification is needed, use a Superpowers-inspired brainstorming interaction.

Do not ask vague open-ended questions by default. Instead, present:

1. why the question matters
2. 2 to 5 concrete choices
3. a recommended safe default when possible
4. an `Other` option where the user can type their own answer
5. consequences or tradeoffs when relevant

Example format in Chinese:

```text
在规划数据库 milestone 前，需要确认持久化策略。

请选择：
A. 使用现有数据库层，暂时不改 schema。推荐。
B. 新增 migration，但只针对本地 / 开发环境。
C. 第一个 milestone 先用内存 adapter，暂缓持久化。
D. Other：输入你的偏好方案。
```

Example format in English:

```text
I need to clarify the persistence strategy before planning database milestones.

Choose one:
A. Use the existing database layer and avoid schema changes for now. Recommended.
B. Add a new migration, but only for local/dev databases.
C. Defer persistence and use an in-memory adapter for the first milestone.
D. Other: describe your preferred approach.
```

Record human answers in:

- `docs/cccc/decision-log.md`
- `docs/cccc/open-questions.md`

## Project discovery

Projects are often not greenfield. Before planning, inspect and summarize the existing project.

Read relevant files and directories such as:

- README and docs
- CLAUDE.md, AGENTS.md, CONTRIBUTING.md
- package.json, pyproject.toml, Cargo.toml, go.mod, pom.xml, build.gradle, Makefile
- src, app, lib, packages, services
- tests, test, spec, __tests__
- CI configs
- Dockerfile, compose files, infra files
- .env.example, config examples
- migrations, schema, Prisma, DB files
- existing TODOs, ADRs, issue templates if present
- git status and a short git log summary

Do not write business code during discovery.

Create or update:

- `docs/cccc/project-map.md`
- `docs/cccc/current-state.md`
- `docs/cccc/architecture.md`
- `docs/cccc/test-strategy.md`
- `docs/cccc/risk-register.md`
- `docs/cccc/open-questions.md`

## Project planning

After discovery, create:

- `docs/cccc/project-brief.md`
- `docs/cccc/roadmap.md`
- `docs/cccc/milestone-backlog.md`

Each milestone must include:

- id
- title
- goal
- scope
- out of scope
- acceptance criteria
- expected changed files or modules
- required tests
- risk level
- dependencies
- stop conditions

## Claude planning self-review

Before asking Codex to review a plan, Claude Code must challenge its own plan.

Ask:

- Did I infer something that should be verified from the repository?
- Did I misunderstand the user's goal?
- Did I miss existing architecture constraints?
- Are milestones too large?
- Are acceptance criteria testable?
- Are there hidden secret, wallet, API key, production, or real-money risks?
- Are there multiple plausible approaches requiring a human choice?
- Would continuing without asking cause product, security, architecture, financial, or data-loss risk?

If the answer indicates risk or missing context, read more project files or ask the human with options.

## Codex adversarial plan review

Codex must review the initial plan adversarially before implementation begins.

Codex should try to reject the plan by finding:

- misunderstood requirements
- missing project context
- unsafe assumptions
- milestones that are too large
- untestable acceptance criteria
- architecture conflicts
- security gaps
- secret-handling risks
- production, wallet, API key, or real-money risks
- missing human decisions

Only approve if the roadmap is clear, safe, scoped, testable, and aligned with the discovered project.

## Context bundle rule

Before every Codex call, regenerate:

```text
docs/cccc/context-bundle.md
```

The context bundle must include:

1. user language (from config.json)
2. original user task
3. current state
4. project map
5. architecture summary
6. test strategy
7. roadmap
8. milestone backlog status
9. completed milestones
10. current milestone
11. acceptance criteria
12. decision log summary
13. open questions
14. risk register
15. git status
16. diff summary
17. relevant diff
18. test output
19. last review result
20. current config thresholds

Hard rule:

```text
No context bundle, no Codex planning.
No project discovery, no roadmap.
No approved roadmap, no implementation.
No config.json, run setup first.
```

## Milestone implementation loop

For each milestone:

1. Confirm roadmap is approved.
2. Confirm current milestone is clearly scoped.
3. Read thresholds from `docs/cccc/config.json`.
4. Implement the smallest coherent change.
5. Run relevant tests and checks.
6. Perform Claude self-review.
7. Regenerate `docs/cccc/context-bundle.md`.
8. Run Codex milestone review in read-only mode.
9. If Codex passes, record acceptance and select next milestone.
10. If Codex fails with fixable findings, fix and repeat.
11. If Codex needs human input or detects unsafe work, pause.

## Codex next milestone rule

Codex may suggest the next milestone only from the existing roadmap and milestone backlog. Codex must not expand scope.

Claude Code must validate that the proposed next milestone:

- matches the user's original task
- follows the roadmap
- does not expand scope
- does not require secrets or sensitive operations
- has clear acceptance criteria
- can be tested locally

## Stop hook automation rule

The optional Stop hook (`cccc-stop.sh`) reads configuration from `docs/cccc/config.json` and runtime state from `docs/cccc/state.json`.

It may block the stop (returning `decision: "block"`) only when all of these conditions are met:

- `docs/cccc/config.json` exists and `automation.stop_hook_loop_enabled` is `true`
- `docs/cccc/config.json` `mode` is `full-auto-safe`
- `docs/cccc/state.json` exists
- `status` is not a terminal or paused state (DONE, COMPLETED, FAILED, PAUSED_FOR_HUMAN, NEEDS_HUMAN, NEEDS_SECRET, SENSITIVE_OPERATION, UNSAFE, PAUSED_FOR_SYSTEM, PAUSED_FOR_CODEX)
- `pause_reason` is empty
- `stop_hook_active` in the hook input is not `true` (prevents infinite recursion)
- continuation count is below `automation.max_stop_hook_continuations` (from config.json)
- `status` is not `SETUP_COMPLETE` with no milestone and no backlog (prevents empty-spin)

The stop hook allows `READY_TO_CONTINUE` status to proceed — this is the status set after a successful resume.

When the hook blocks, it outputs a `reason` that instructs Claude to continue the state machine loop internally — not just take one small step and stop again. The skill's internal state machine must drive the actual loop; the hook merely prevents Claude Code from stopping prematurely.

The Stop hook must never continue past hard pause conditions.

## User-facing progress format

Use the user's language (from `config.json` `language.user_language`).

Chinese:

```text
Milestone M001：<标题>
状态：实现中 / Review 中 / 修复中 / 已通过 / 已暂停
Review 轮次：1/3
最近检查：<测试结果或跳过原因>
决策：<下一步动作>
```

English:

```text
Milestone M001: <title>
Status: implementing / reviewing / fixing / passed / paused
Review round: 1/3
Last check: <test result or reason skipped>
Decision: <next action>
```
