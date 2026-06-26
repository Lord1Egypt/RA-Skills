---
name: cline
description: Delegate coding tasks to Cline CLI (open-source autonomous coding agent). Model-agnostic, supports all major providers. Use for one-shot tasks, CI/CD automation, and parallel workstreams. Requires Node.js 20+.
version: 2.0.0
author: AndreasThinks
license: MIT
metadata:
  hermes:
    tags: [Coding-Agent, Cline, OpenSource, Automation, CI-CD]
    related_skills: [claude-code, codex, hermes-agent]
---

# Cline CLI

Delegate coding tasks to [Cline CLI](https://cline.bot/cli) — an open-source, model-agnostic coding agent that runs directly in the terminal.

## Installation

Install Cline CLI globally:

```bash
npm install -g cline
# or
npx cline auth  # Follow prompts to configure your provider
```

This installs the `cline` command globally. No PATH configuration needed for standard npm installs.

**Default model:** Configure during `cline auth` — recommended: `anthropic/claude-haiku-4-5` (cheap, fast) or `xiaomi/mimo-v2-pro` (good for large tasks when credits are tight).

Config stored in `~/.cline/data/`.

## Authentication

Run `cline auth` interactively (needs a TTY/PTY), or use flags:

```bash
cline auth -p <provider> -k <api_key> -m <model_id>
```

**v2.8.0 quirk:** Even with flags, auth launches a TUI. Run in the background with a long timeout (20-25s) — it writes config before exiting on SIGTERM. Config is saved to `~/.cline/data/globalState.json` and `~/.cline/data/secrets.json`.

## One-Shot Tasks (Headless)

```bash
cd /path/to/project
cline -y "Add error handling to all API calls in src/"
```

`-y` / `--yolo` = auto-approve all file changes, forces headless mode.

## With Timeout (CI/CD)

```bash
cline -y --timeout 300 "Run tests and fix any failures"
```

## Piped Input

```bash
git diff origin/main | cline -y "Review these changes for bugs and security issues"
npm test 2>&1 | cline -y "Fix failing tests"
```

## JSON Output (for scripting)

```bash
cline --json "List all TODO comments" | jq '.text'
```

## Custom Model

```bash
cline -y -m anthropic/claude-sonnet-4-5 "Refactor auth module to use JWT"
```

## Parallel Workstreams

```bash
(cd /tmp/branch-a && cline -y "Fix login bug") &
(cd /tmp/branch-b && cline -y "Add unit tests for auth") &
wait
```

## Planning Subagent + Cline Pattern

For complex multi-task implementations, don't send vague instructions to Cline. Use a two-step pattern:

1. **Plan first** — dispatch a `delegate_task` subagent with full codebase context to read the relevant files, understand the structure, and write a detailed plan doc (exact file paths, line numbers, complete code snippets) to e.g. `docs/plans/YYYY-MM-DD-feature.md`.

2. **Implement with Cline** — hand the plan file to Cline:
   ```bash
   cline -y --timeout 600 -m anthropic/claude-sonnet-4-5 \
     "Implement the plan in docs/plans/2026-04-03-feature.md exactly as written. Read the plan first, then read each source file before editing it."
   ```
   Optionally add `--double-check-completion` to force Cline to re-verify its work before marking done. Adds time, reduces the need for a first-pass audit.

This pattern works because:
- The subagent reads the actual code and generates grounded, correct code snippets
- Cline gets precise instructions and doesn't have to infer structure
- The plan doc is a reviewable artefact before a line of code is written

**When to use:** Any implementation involving 3+ files, or where field names / API shapes need to be verified before writing code.

## Opus Review + Cline Fix Cycle

For features spanning many files, Cline first passes routinely miss steps — even with a detailed plan. Observed: 5 of 13 planned steps skipped on a leaderboard feature (UI, tests, runner loop all absent). The reliable pattern is:

1. **Cline implements** — fire with a detailed prompt, set a cron review job for 15-20 min
2. **Opus reviews** — spawn `delegate_task` with `max_iterations=40`, ask it to read every changed file against the plan and produce a prioritised list: bugs, missing steps, integration gaps, test gaps. Specify exact files and what to check.
3. **Targeted second Cline pass** — write a new prompt referencing specific findings by file:function:line. Include exact replacement code for bugs, not just descriptions. This pass is faster and cleaner than the first because the problem space is fully defined.
4. **Repeat if needed** — a second opus review after the fix pass usually comes back clean.

Key differences from the first pass prompt:
- List each fix as a numbered section with file path in the heading
- For bugs: include the exact broken code and the exact replacement
- For missing implementations: paste in the complete code, not a description of it
- End with "Run tests and commit if they pass"

**Observed outcome:** Two-pass cycle (Cline → Opus review → Cline) consistently produces cleaner results than one long prompt, because the review grounds the second prompt in reality rather than the plan.

## File Conflict Rule

**If all tasks in a phase touch the same file — use ONE Cline agent for the whole phase.**

The parallel workstream pattern only works when tasks are on different files. When a code review or plan surfaces N tasks that all modify `dashboard.html` (or any single file), combine them into one agent prompt rather than trying to parallelize. Sequential tasks in a single session preserve the file state correctly.

Quick decision:
- Tasks on different files → parallel agents, one per file group
- Tasks on same file → one agent, all tasks in one prompt

**Exception: Kanban.** When using `cline kanban`, each task runs in its own git worktree. Parallel agents can't clobber each other because they're working in separate checkpoints. The one-agent-per-file constraint does not apply when using Kanban.

## Single-File Rule

**One agent per file, always** — unless using Kanban (worktrees handle isolation natively). If multiple tasks touch the same file and you're using raw CLI, combine them into one agent prompt. Two agents editing the same file concurrently will clobber each other — the second write overwrites the first, silently. Group tasks by file before dispatching.

## Parallel Bug-Fix Pattern (Multi-Agent from Code Review)

When a code review surfaces N independent issues, dispatch one Cline agent per issue
as background processes. **Critical rule: split work so no two agents touch the same file.
If two agents edit the same file concurrently, the second write overwrites the first.**

Workflow:
1. Group issues by the files they require editing
2. Combine any issues that share files into a single agent task
3. Dispatch agents in sequence (small stagger), redirect each to its own log
4. Schedule a cron job to review all results after a fixed delay

```bash
cd /path/to/your/project

# Agent 1: touches only dice.py
cline -y --timeout 300 "Fix scatter logic in app/game/dice.py: ..." \
  > /tmp/fix_scatter.log 2>&1 &
echo "Agent 1 pid $!"

# Agent 2: touches only combat.py
cline -y --timeout 300 "Implement assists in app/game/combat.py: ..." \
  > /tmp/fix_assists.log 2>&1 &
echo "Agent 2 pid $!"

# Agent 3: touches only action_executor.py
cline -y --timeout 300 "Implement push in app/state/action_executor.py: ..." \
  > /tmp/fix_push.log 2>&1 &
echo "Agent 3 pid $!"
```

Then schedule a single cron job (deliver: origin) to fire after enough time for all agents
to finish. The cron task reads each log, runs the full test suite, and reports pass/fail
per agent plus any issues needing manual attention.

```python
# In the cron prompt, check each log and run tests:
# - cat /tmp/fix_scatter.log | tail -30
# - cd /path/to/your/project && uv run pytest tests/ -q | tail -20
```

## Multi-Pass Implementation with Opus Audit

For larger features (5+ files), a single Cline pass frequently skips steps or times out silently. Realistically expect **three passes** for anything complex:

1. **Plan** — delegate_task subagent reads codebase, writes `docs/plans/YYYY-MM-DD-feature.md` with exact file paths, line numbers, and complete code snippets.

2. **First Cline pass** — implement the plan with a tight, specific prompt.

3. **Opus audit** — run as a direct `delegate_task` (not a cron) when actively working — faster feedback. Use a cron (deliver: origin) if you're stepping away. The subagent reads every new/modified file and produces a prioritised findings report: bugs, missing steps, integration gaps, test coverage. Give it the plan file path and the specific integration points to check.

4. **Second Cline pass** — targeted fix prompt. **Provide exact code for each fix**, not just descriptions. Cline is significantly more accurate when the prompt says "add this exact block after line X" vs "fix the timeout handling". List each issue as a numbered heading with the precise code to insert.

5. **Second Opus audit + third Cline pass if needed** — for a feature with multiple review cycles, the second audit is usually much cleaner. If only a handful of issues remain (missing tests, minor edge cases), fix them directly rather than firing another Cline pass.

**Observed failure modes on first pass:**
- Steps silently skipped (5 of 13 in one case) with no error in the log
- `--timeout 600` hit mid-task, leaving the last file untouched (0-byte test file)
- Frontend JS wiring (calling new function from existing function) frequently missed
- Pydantic v2 issues: `@property` not serialized (needs `@computed_field`), `datetime.utcnow()` deprecated
- Score/state fields not cleared in reset methods, causing data bleed across sessions
- In-memory guard (`set.add()`) placed before the disk write it protects — silent data loss on failure

**Audit prompt shape that works well:**
```
goal: "Thorough code review of <feature> in <project>. Read the plan at <path>, then read every new/modified file. Produce prioritised: (1) bugs, (2) missing edge cases, (3) integration gaps, (4) test coverage gaps. File + line + fix for each. Also flag what's correct."
context: "New files: <list>. Modified files: <list>. Pay specific attention to: <list of integration points from the plan's gotchas section>."
toolsets: ["terminal", "file"]
max_iterations: 40
```

**When to run audit as cron vs direct delegate_task:**
- Actively working and waiting → `delegate_task` directly (blocks, returns findings immediately)
- Stepping away / Cline running in background → cron with `deliver: origin` so findings arrive when you're back

## Multi-Pass Implementation Pattern (plan → implement → review → fix)

For features spanning 8+ files, a single Cline pass will often miss steps or time out on the last task (typically tests). Use a structured multi-pass loop:

1. **Subagent plans** — `delegate_task` with opus reads the full codebase and writes a detailed plan to `docs/plans/YYYY-MM-DD-feature.md` with exact file paths, line numbers, and code snippets.

2. **Cline implements** — hand it the plan file. Set `--timeout 600`. It will implement 70-80% correctly.

3. **Cron review** — schedule a cron (15-20 min) to check: `git diff --stat`, syntax checks on new files, `pytest -q`. Report back.

4. **Opus code review** — `delegate_task` with opus reads every touched file and produces a prioritised bug list. Findings will typically include: missing steps Cline skipped, bugs in wiring between components, Pydantic v2 gotchas (`@property` vs `@computed_field`), and 0-byte test files from timeout.

5. **Second Cline pass** — tight prompt with exact fixes, explicit code for each change. Much smaller scope = fewer timeouts.

6. **Write remaining tests manually** — if Cline timed out on tests (common), write them directly. Faster and more reliable than re-running Cline.

**Observed Cline failure modes on large implementations:**
- Tests are almost always the last step and get cut off by timeout — write them yourself
- Cline generates files but doesn't verify them — always syntax-check new Python files
- On multi-file features, Cline may skip steps silently (no error) — Opus review catches these
- `@computed_field` (Pydantic v2) vs `@property` — Cline often writes `@property` which doesn't serialize; Opus catches it
- Premature guard updates before dependent operations succeed (e.g. adding to a set before the disk write) — logic bug Cline introduces, Opus catches

**Cron review prompt pattern:**
```
1. pgrep -fl cline (is it still running?)
2. tail -50 /tmp/impl.log
3. git diff --stat
4. wc -l on all new files (catch 0-byte files)
5. grep specific fix markers to verify they landed
6. pytest -q | tail -20
Report: what was fixed, what failed, what needs manual attention.
```

## Multi-Round Implementation + Review Cycle

For large features (10+ files, multi-step plans), a single Cline run often misses steps or times out. The pattern that works:

**Round 1 — Cline implements from plan doc**
Point Cline at the plan file. It will implement the backend correctly but often skip frontend, tests, and runner changes (these come last and hit timeout).

**Round 2 — Opus subagent reviews**
Use `delegate_task` with `claude-opus-4-6` (not sonnet — opus catches subtler wiring issues). Give it the plan doc path and specific things to check. It will find: missing files, wrong ordering of operations, Pydantic v2 gotchas, exception isolation gaps.

**Round 3 — Cline fix pass with tight prompt**
Do NOT re-run the original prompt. Write a new prompt listing ONLY the specific issues found in the review, with exact code for each fix. This is the critical lesson: vague "finish what you missed" prompts cause Cline to re-attempt the whole plan and timeout again. Specific "fix these 7 things, here is the exact code" prompts land clean in one pass.

**Round 4 — Manual cleanup**
Tests and small correctness fixes are faster to write directly than to re-run Cline. If tests were skipped or are 0 bytes, just write them. A Cline run costs more time and credits than writing 100 lines of pytest.

**When to skip Round 3 entirely:** If the Opus review finds only 2-3 small, well-understood bugs (e.g. a missing `break` removal, a filter condition that needs one line added), fix them directly with `mcp_patch` or a short Python script. The overhead of another Cline pass (context reloading, 10+ min runtime, potential timeout) is not worth it for changes that are faster to write than to describe. Rule of thumb: if you can write the fix in under 5 minutes, do it yourself.

**What to put in a tight fix prompt:**
- One section per issue, labelled by file
- Exact replacement code, not descriptions
- "Read the file before editing" at the top
- "Run tests and report result" at the bottom
- Do NOT include issues already fixed — Cline will re-edit them

**Timing:**
- Set review cron for ~15min after Cline fires (not 10 — mimo/sonnet needs time)
- Set a second review cron 5min after the fix pass
- Both deliver: origin so findings come back to chat

## Two-cron review pattern

For long Cline jobs, fire two review crons at different delays — one for a quick status check (test results, what changed), one for a deeper quality review (Opus subagent):

```python
# Fire Cline in background
cline -y --timeout 600 -m anthropic/claude-sonnet-4-5 "..." > /tmp/task.log 2>&1 &

# Quick status cron (fires when Cline should be done)
mcp_cronjob(action='create', schedule='20m', repeat=1, deliver='origin',
  prompt='tail -30 /tmp/task.log; cd ~/project && git diff --stat; pytest -q | tail -10')

# Opus quality review cron (fires slightly later or at same time)
mcp_cronjob(action='create', schedule='25m', repeat=1, deliver='origin',
  prompt='Use delegate_task with claude-opus-4-6 to review what was just implemented...')
```

The status cron catches "Cline timed out and did nothing" fast. The Opus review catches correctness issues. Both deliver to origin so findings come back to the current conversation.

**Cline timeout behaviour:** When Cline times out mid-task, it often leaves the working tree clean (no changes committed). Always check `git status` and `git diff --stat` in the review cron — if the tree is clean, the task didn't complete and needs a retry or manual fix.

## Full Autonomous Review Cycle (cron pattern)

For a complete fire-and-forget workflow — agents run in background, cron reviews,
commits, deploys, then audits with a code review subagent:

```python
# Cron prompt (deliver: origin, schedule: Nm for N minutes after agents start):
"""
1. Check agent logs: cat /tmp/agent_a.log | tail -40, /tmp/agent_b.log | tail -40
2. Review diffs: cd ~/projects/X && git diff --stat && git diff <files>
3. Syntax check: python3 -c "import ast; ast.parse(open('file.py').read()); print('OK')"
4. If clean: git add <files> && git commit -m "..." && git push
5. Deploy via subprocess with RAILWAY_API_TOKEN (see use-railway skill)
6. Code review via delegate_task: spawn a subagent to read changed files and produce
   a prioritised bug report (what broke, what's risky, silent failures)
7. Report everything back — what agents did, what committed, what deployed, review findings
"""
```

Key points:
- Set schedule to fire after agents realistically finish (e.g. 12-15min for 3 Cline agents)
- `deliver: origin` means the report comes back to the current chat
- The code review subagent should focus on new bugs introduced, not style
- If an agent log shows 402 credit errors, note which file was not modified so you can patch manually

**Pitfall:** Cline with `--timeout 300` backgrounded via `&` detaches from the shell
but still writes to the log. The log may appear empty mid-run (buffering). Check the
target files directly rather than tailing the log in real time.

## Key Flags

| Flag | Effect |
|------|--------|
| `-y, --yolo` | Auto-approve all actions, forces headless mode |
| `--auto-approve-all` | Auto-approve but stay interactive (shows output) |
| `-p, --plan` | Plan mode: agent presents execution plan before writing code |
| `-a, --act` | Act mode: skip plan, execute immediately |
| `-m, --model <id>` | Override model (OpenRouter: `anthropic/claude-haiku-4-5`, etc.) |
| `--timeout <seconds>` | Max execution time |
| `--json` | Output as JSON (one object per line) |
| `-c, --cwd <path>` | Set working directory |
| `--config <path>` | Override configuration directory |
| `--continue` | Resume most recent task in current directory |
| `-T, --taskId <id>` | Resume a specific task by ID (use `cline history` to list IDs) |
| `--thinking [tokens]` | Enable extended thinking (default: 1024 token budget) |
| `--reasoning-effort <effort>` | none / low / medium / high / xhigh |
| `--double-check-completion` | Reject first completion attempt to force re-verification |
| `--auto-condense` | AI-powered context compaction instead of mechanical truncation |
| `--max-consecutive-mistakes <N>` | Halt in yolo mode after N consecutive mistakes |
| `--hooks-dir <path>` | Inject additional runtime hooks |
| `--acp` | ACP mode for editor integration (Zed, Neovim, JetBrains) |
| `--kanban` | Launch the Kanban board UI |
| `--tui` | Open the legacy terminal UI |
| `-v, --verbose` | Verbose output |

## Subcommands

| Subcommand | Effect |
|------------|--------|
| `cline task <prompt>` | Alias for running a task (same as positional prompt) |
| `cline history` | List past tasks with IDs — use with `-T` to resume |
| `cline config` | Show current configuration |
| `cline auth` | Authenticate a provider (needs PTY — run in background or with timeout) |
| `cline mcp` | Manage MCP servers |
| `cline kanban` | Launch the Kanban board UI |
| `cline update` | Check for and install updates |

## Supported Providers (for re-auth)

`anthropic`, `openrouter`, `openai-native`, `openai`, `gemini`, `deepseek`, `ollama`, `bedrock`, `xai`, `cerebras`, `groq`, and more.

## Rules

1. **Always export PATH** — the binary is not in the default PATH
2. **Use `-y` for automation** — without it, Cline prompts for approval of each action
3. **Use `--timeout`** for long tasks to avoid hanging processes
4. **Use `-c` (cwd)** to keep the agent focused on the right directory
5. **Report results** — after completion, check what changed and summarize

## Invoking Hermes as a non-interactive subprocess

`hermes --task` does not exist. The correct invocation:

```bash
hermes chat -q "your prompt here" -m model/id --provider openrouter -s skill-name -Q
```

- `-q` / `--query` — single query, non-interactive mode
- `-Q` / `--quiet` — suppress banner/spinner, output final response only
- `--provider openrouter` — required when using OpenRouter models (otherwise routes to Anthropic)
- `-s skill-name` — preload a skill (can repeat or comma-separate)

Without `--provider openrouter`, a model like `qwen/qwen3.6-plus:free` will be sent to Anthropic and get a 404.

## Cline Kanban

Kanban is built into the CLI (v2.13.0+). Launch from the root of any git repo:

```bash
cd /path/to/your/project
cline kanban
# or: cline --kanban
```

Opens a browser UI at `http://127.0.0.1:3484/<project-name>`.

### How it works

Each task card gets its own ephemeral git worktree with its own terminal. Multiple agents run in parallel without merge conflicts. When a card is trashed, the worktree is deleted automatically.

### Key features

- **Dependency chains**: link cards with Cmd+click. When a task completes, dependent tasks auto-start.
- **Sidebar chat**: natural language board management — ask it to break down a goal into linked task cards.
- **Diff viewer**: click a card to see changes. Click any line to leave inline feedback sent back to the agent.
- **Resume by ID**: tasks have a resume ID even after worktree cleanup. `cline history` lists IDs; resume with `cline -T <id>`.
- **Auto-commit / Auto-PR**: agents commit incrementally and can open PRs on completion.
- **Agent-agnostic**: works with Cline, Claude Code, Codex, OpenCode.

### Config

```
~/.cline/kanban/config.json       # agent selection, autonomous mode toggle
~/.cline/kanban/workspaces/<project>/boards.json  # task state
```

Autonomous mode (no approval prompts) is on by default. Disable in config or UI if you need oversight of every shell command.

### Remote access (network binding)

By default Kanban binds to `127.0.0.1` — localhost only. To access from another machine on your network:

```bash
cline kanban --host 0.0.0.0 --port 3484 --no-open
```

Then access from any machine at `http://<pi-ip>:3484/<project-name>`. The Pi's firewall typically allows local network traffic on arbitrary ports.

**Verified working** (Apr 2026): bound to `0.0.0.0:3484`, accessed from remote machine on same network. Task created and completed end-to-end.

### CLI task management

Kanban has a full CLI — **separate from `cline task`** — for creating and managing tasks without the UI. The `kanban` command is installed globally alongside `cline`.

```bash
# List all tasks (kanban server must be running)
kanban task list --project-path /path/to/project

# Create a task in backlog
kanban task create --prompt "Do X, Y, Z" --project-path /path/to/project

# Link tasks (create dependency chain)
# Task A waits on Task B: A won't start until B completes and moves to trash
kanban task link --task-id <A> --linked-task-id <B> --project-path /path/to/project

# Unlink tasks
kanban task unlink --task-id <A> --linked-task-id <B> --project-path /path/to/project

# Start a task manually (spawns agent in isolated worktree)
kanban task start --task-id <id> --project-path /path/to/project

# Move task to trash (cleans up worktree)
kanban task trash --task-id <id> --project-path /path/to/project

# Update a task (e.g., change prompt, column, settings)
kanban task update --task-id <id> --prompt "New prompt" --project-path /path/to/project
```

**Important:** The `kanban task` CLI requires the Kanban server to be running. Start it first:

```bash
kanban --no-open  # binds to 127.0.0.1:3484 by default
```

Or bind to all interfaces for remote access:

```bash
kanban --host 0.0.0.0 --port 3484 --no-open
```

### Dependency chains (CLI)

The `kanban task link` command creates dependency chains. Direction matters:

- `--task-id` = the **dependent** task (waits)
- `--linked-task-id` = the **prerequisite** task (runs first)

When the prerequisite completes and moves to trash, the dependent task auto-starts.

```bash
# Task B depends on Task A (A runs first, then B)
kanban task link --task-id B --linked-task-id A

# Stored in board.json as:
# { "fromTaskId": "B", "toTaskId": "A" }
```

**Board JSON format** (`~/.cline/kanban/workspaces/<project>/board.json`):

```json
{
  "columns": [...],
  "dependencies": [
    {
      "id": "297d513c",
      "fromTaskId": "a2dd3",      // dependent (waits)
      "toTaskId": "be008",        // prerequisite (runs first)
      "createdAt": 1775494077112
    }
  ]
}
```

**Autonomous workflow pattern:**

1. Create tasks via CLI or sidebar chat
2. Link them into a chain (or DAG — multiple dependencies supported)
3. Start the first task (or let the sidebar agent start it)
4. When each task completes → auto-commits → moves to trash → next task auto-starts

**Sidebar chat shortcut:** Instead of manual linking, ask the Kanban sidebar agent:

> "Break this into 5 tasks and link them so they run in order"

The agent has board-management instructions injected and can create/link tasks directly.

### Autonomous prompt patterns (sidebar chat)

The Kanban sidebar agent can decompose complex work into linked task chains. Patterns from the Cline team:

**Greenfield scaffolding** — set up foundation, then fan out parallel tasks:

```
Build a production-ready Express API. Tasks:
1) Set up Express with TypeScript, tsconfig, nodemon dev script
2) Add health check at GET /health returning { status: "ok", timestamp }
3) Add structured JSON logging with pino
4) Add global error handling middleware
5) Add CORS and helmet security middleware
Link them sequentially – each builds on the last. Start task 1.
```

**Parallel branches** — after foundation, run independent tasks in parallel:

```
Set up full-stack app with Express + SQLite. Tasks:
1) Initialize Express with TypeScript, install better-sqlite3
2) Create database module (src/db.ts) with users table (id, name, email, created_at)
3) Add CRUD routes: GET /users, GET /users/:id, POST /users, PUT /users/:id, DELETE /users/:id
4) Add input validation middleware using zod for POST/PUT
5) Add seed script with 10 sample users
Link 1 → 2 → 3 → 4, and 2 → 5 so seeding runs in parallel with routes. Start task 1.
```

**Migration/refactoring** — audit first, then fan out:

```
Migrate this JavaScript project to TypeScript. Tasks:
1) Add tsconfig.json (strict mode), install typescript + ts-node, rename entry to .ts
2) Rename all .js files in src/ to .ts, fix immediate type errors
3) Add explicit types to all function signatures
4) Enable strict mode and fix remaining errors
Link 1 → 2 → 3 → 4. Start task 1.
```

**Key pattern:** The agent intelligently parallelizes where possible and links sequentially where there are dependencies. One prompt → autonomous chain → committed code.

**Full workflow example** (verified Apr 2026):

```bash
# 1. Create task
cd ~/projects/your-project
cline task create --prompt "Test the kanban workflow. Create test-kanban.md, commit it, move to trash."
# → returns task ID (e.g. 49547)

# 2. Start task (agent runs autonomously in worktree)
cline task start --task-id 49547
# → task moves to "in_progress", agent starts in isolated worktree

# 3. Wait for completion (task auto-moves to "review" column when done)
cline task list
# → check column: "review" means ready for merge

# 4. Merge the work
cd ~/.cline/worktrees/<task-id>/<project-name>
git log --oneline -1  # get commit hash
cd ~/projects/your-project
git cherry-pick <commit-hash>

# 5. Clean up
cline task trash --task-id 49547
# → worktree deleted, task archived
```

### How worktrees work

Each task runs in an isolated git worktree at:
```
~/.cline/worktrees/<task-id>/<project-name>/
```

The agent commits to the worktree, not your main repo. When a task completes, it moves to the **Review** column automatically.

**Worktree structure** (verified Apr 2026):
- Base: `~/.cline/worktrees/<task-id>/<project-name>/`
- Agent has full write access, commits to worktree branch
- Symlinks to `node_modules` and other gitignored dirs (fast, no duplication)
- Worktree deleted on `task trash`

**To merge the work:**

```bash
# Find the commit in the worktree
cd ~/.cline/worktrees/<task-id>/<project-name>
git log --oneline -1

# Cherry-pick to your main repo
cd /path/to/your/project
git cherry-pick <commit-hash>

# Then trash the task to clean up
cline task trash --task-id 49547
```

**Task lifecycle:**
1. **Backlog** — created, not started
2. **In Progress** — agent running in worktree
3. **Review** — agent finished, awaiting human approval (auto-moves here)
4. **Trash** — worktree deleted, task archived (resume later via ID if needed)

### Task lifecycle

1. **Backlog** — task created, not started
2. **In Progress** — agent session running in worktree
3. **Review** — agent finished, awaiting human approval (auto-moves here on completion)
4. **Trash** — worktree deleted, task archived (can resume later via task ID)

### Caveat

Kanban is a research preview. It's browser-based — no headless/programmatic API. Hermes can read `boards.json` for task state but cannot drive the UI from a cron job. Use raw CLI patterns for fully automated pipelines; use Kanban when you're at the keyboard and want visual oversight of parallel agents.

**State files:**
- `~/.cline/kanban/workspaces/<project>/boards.json` — task state, column assignments
- `~/.cline/kanban/workspaces/<project>/index.json` — workspace registry
- `~/.cline/kanban/config.json` — agent selection

Hermes can read these directly to monitor task progress without the UI.

## Known Pitfalls

- **`git checkout --theirs` during rebase can break cross-file imports silently.** When resolving merge conflicts by taking the upstream version of a file, that file may no longer match the import expectations of other files in the same stash/local branch. Classic example: taking upstream `llm.py` while the local `model_picker.py` imports `validate_model` from it — the function only exists in the local version. Always check what each conflicted file exports and what the other conflicted files import from it before resolving. When in doubt, don't resolve conflicts with `--theirs`/`--ours` blindly — read the diffs first. If a cascade of import errors follows a rebase, this is the likely cause. Fix: `git reset --hard <last_clean_commit>` and force-push to recover.



- **claude-sonnet-4-5 requests 64k max_tokens by default** — if OpenRouter credits are tight this causes immediate 402 before the task even starts (\"You requested up to 64000 tokens, but can only afford N\"). Switch to `anthropic/claude-haiku-4-5` which uses a much smaller token budget and is far cheaper. Haiku is the safe fallback for all Cline tasks when credits are a concern. Alternative when Anthropic credits are exhausted: `xiaomi/mimo-v2-pro` (OpenRouter) — confirmed working for large frontend implementation tasks.
- **xiaomi/mimo-v2-pro is a reliable fallback for large frontend tasks**: Confirmed working for dashboard.html implementation (1000+ line file). Use when Sonnet/Haiku are hitting 402s or credits are tight. Specify as `-m xiaomi/mimo-v2-pro`.
- **OpenRouter credit limits — Cline requests 64000 max_tokens by default, 402 fires if key balance is below that threshold**: Both `claude-sonnet-4-5` and `claude-haiku-4-5` will 402 if instantaneous credit balance is too low. When running multiple concurrent agents they each request 64k simultaneously and collectively drain the key fast. Check balance before firing parallel agents. If hitting 402s, top up or switch to a smaller-context model. Original pitfall note:
- **OpenRouter credit limits with large AND small models**: Both `claude-sonnet-4-5` and `claude-haiku-4-5` can hit 402 credit errors mid-task when generating long files (>600 lines). Error: `"This request requires more credits, or fewer max_tokens. You requested up to 64000 tokens, but can only afford N."` Cline writes whatever it completed before the error — always check `wc -l` and `python3 -c "import ast; ast.parse(open('file.py').read())"` to verify the output file is syntactically complete and covers all requested functionality. If truncated, patch the missing sections manually rather than re-running Cline (re-running burns more credits on re-reading context).
- **Cline timeout on long-running scrapes**: Cline may time out waiting on its own background monitoring commands (e.g. `sleep 180 && ...`) before the actual task finishes. The script will still be running. Check with `pgrep -fl <script_name>` and inspect output files directly rather than waiting for Cline to report completion.
- **300s timeout may not be enough for scraping tasks** — if the task involves network I/O (API calls, GH Archive downloads), set `--timeout 600` or higher.
- **Log redirect swallows Cline output**: Running `cline ... > /tmp/log.log 2>&1` causes the log file to appear empty while Cline is running — it buffers internally and flushes late. Poll the file with `tail` or check the output file the task was supposed to create rather than watching the log in real time.
- **Cline generates but does not verify**: Cline will write a script and mark the task complete without running it. Use `--double-check-completion` to force a re-verification pass before Cline marks the task done. Still always run a syntax check and smoke test after, especially for complex tasks. A credit-limit mid-run produces syntactically valid but functionally incomplete code.
- **`cline history` launches TUI**: Like `cline auth`, calling `cline history` without a PTY hangs. Run with a timeout or in background to get the output, or use PTY mode.
