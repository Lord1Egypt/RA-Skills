# Spawning on each harness

The pipeline is the same on every harness; only the spawn call differs. Two ways to spawn:

- **In-process sub-agent** (Claude Code's Agent tool): no CLI, the report comes back as the tool
  result, follow-ups go through `SendMessage`. Cheapest to wire up when the orchestrator is Claude Code.
- **Headless CLI** (`claude -p`, `codex exec`, `opencode run`) through `scripts/spawn.mjs`: any
  orchestrator, any mix of vendors, and every run leaves a run directory (`command.txt`,
  `events.jsonl`, `stderr.log`, `final.md`, `result.json`) plus an optional ledger row.

Rules for every harness:
- Write the brief to a file first (`.agent-briefs/<feature>-<role>-r<round>.md`, git-ignored) and send
  it on stdin, or as "Read and follow <path> exactly" for the Agent tool. The file is the audit trail
  and the base for the next fix brief.
- One worktree per writing executor. Readers (reviewers, scouts) may share a checkout.
- Record the session id of every run (`result.json` -> `sessionId`). Re-reviews and blocked-question
  answers resume THAT id, never "the last session".
- Fix rounds start a FRESH session; resuming a builder multiplies cost with its transcript.
- Run every CLI as a tracked background job and judge it by its exit code and `result.json`.

## Claude Code — in-process (Agent tool)

| Need | How |
|---|---|
| Executor | `Agent({ subagent_type: "maestro-executor", isolation: "worktree", run_in_background: true, description, prompt: "Read and follow .agent-briefs/F12-build-r1.md exactly. Your final message is the report block." })` |
| Model / effort / tools | Fixed per agent definition: copy `templates/claude-agent-executor.md` to `.claude/agents/` (or `~/.claude/agents/`) and set `model`, `effort` and `tools` there; keep one definition per risk class (for example `maestro-executor` on Sonnet, `maestro-executor-strong` on Opus). The call's `model` parameter can override the model for one run. |
| Read-only reviewer or scout | A definition whose `tools` has no Edit/Write (or `subagent_type: "Explore"` for search). |
| Blocked question | `SendMessage({ to: <agent id>, message: "<answer>" })`: same agent, context still warm. |
| Fix round | A NEW Agent call with the fix brief, never `SendMessage` to the builder. |
| Parallel lanes | Several Agent calls in one message, each with `isolation: "worktree"`. |

Notes: the worktree an isolated agent works in is reported back with its result; commit there, or
fetch its branch. A background agent's result arrives as a notification; do not poll.

## Claude Code — headless CLI

```bash
node scripts/spawn.mjs --harness claude --model sonnet --effort high \
  --brief .agent-briefs/F12-build-r1.md --dir ../wt-F12 --out .agent-runs/F12-build-r1
```

- Runs `claude -p --output-format json --permission-mode <auto> [--model] [--effort] [--resume <id>]`.
- `--mode write` uses `--permission-mode auto` by default; where auto mode is not available, pass
  `--permission acceptEdits` plus an allow-list after `--`, for example
  `-- --allowedTools 'Bash(pnpm test:*)' 'Bash(pnpm typecheck:*)'`, or the gates will be denied.
  `--mode read-only` uses `plan`.
- Effort levels: `low`, `medium`, `high`, `xhigh`, `max`. Session id, cost and tokens come from the
  JSON result.
- **Lean by default.** A headless run otherwise loads every user MCP server, skill and plugin. Measured
  on a one-line reply (Haiku): full setup 61K input tokens, $0.15, 29 s; with spawn.mjs's default
  `--strict-mcp-config --disable-slash-commands --exclude-dynamic-system-prompt-sections`, $0.06, 7 s.
  The executor needs no tools beyond the built-ins: its context is the brief. `--no-lean` restores the
  full setup (an executor that needs an MCP server: pass `-- --mcp-config <file>` instead).
- `--setting-sources project,local` also drops user plugins (fewer tokens) but also drops user-level
  permission rules; `--bare` is leanest but needs an API key instead of the usual login.

## Codex

```bash
node scripts/spawn.mjs --harness codex --effort high \
  --brief .agent-briefs/F12-build-r1.md --dir ../wt-F12 --out .agent-runs/F12-build-r1
# reviewer (read-only), then a re-review in the SAME session:
node scripts/spawn.mjs --harness codex --mode read-only --brief review.md --dir . --out .agent-runs/F12-review-r1
node scripts/spawn.mjs --harness codex --mode read-only --resume <sessionId> --brief rereview.md --dir . --out .agent-runs/F12-review-r2
```

- Runs `codex exec --json -C <dir> --sandbox workspace-write|read-only -o final.md [-m] [-c model_reasoning_effort="<e>"] -`
  with the brief on stdin (stdin is closed after the brief, so it never waits for input).
- Resume: `codex exec resume <id> ...` takes neither `-C` nor `--sandbox`, so spawn.mjs runs it in
  `--dir` and passes the sandbox as `-c sandbox_mode=...`.
- Effort: `minimal`, `low`, `medium`, `high` (some models also take `xhigh`). Session id is the
  `thread_id` of the first event; tokens come from `turn.completed`.
- Some Codex sandboxes cannot write `.git` inside a linked worktree: the executor does not commit, the
  orchestrator does (see operations.md).
- Built-in alternative for reviews: `codex exec review` reviews the current repository's changes.

## OpenCode

```bash
node scripts/spawn.mjs --harness opencode --model opencode/deepseek-v4.1-flash-free \
  --brief .agent-briefs/F12-build-r1.md --dir ../wt-F12 --out .agent-runs/F12-build-r1
```

spawn.mjs reads `opencode --version` and builds the command for the installed major version:

| | v2 (current) | v1 |
|---|---|---|
| Command | `opencode run --standalone --format json --agent build --auto -m provider/model[#effort] [--session <id>]` | `opencode run --format json --dir <dir> --agent build --auto -m provider/model [--variant <effort>] [--session <id>]` |
| Working directory | the process cwd, with `PWD` set to it (v2 takes its project from `$PWD`; an inherited `PWD` points it at the wrong checkout) | `--dir` |
| Effort | inside the model id: `provider/model#high` (pass `--model` with `--effort`) | `--variant` |
| Server | `--standalone`: a private server per run, so parallel lanes never share a service rooted elsewhere | a local server per run |

- `--model provider/model` is REQUIRED on a fresh run (`opencode models` lists what your providers
  can route; a model can be listed and still refuse with `provider.no-route` when its provider is not
  logged in). A resumed run keeps its session's model.
- `--mode write` passes `--auto` so a headless run never hangs on a permission prompt. OpenCode has
  no OS sandbox: only run it in a disposable worktree, and deny anything sensitive in the agent's
  permission config. `--mode read-only` uses the `plan` agent without `--auto`; if a plan run needs a
  permission it can block until `--timeout`, so give the plan agent `allow`/`deny`, not `ask`.
- Lean by default: `OPENCODE_DISABLE_CLAUDE_CODE=1` keeps `~/.claude` prompts and skills out of the
  executor's context; `--no-lean` keeps them.
- Session id is the `sessionID` of the events (`ses_…`); the report is the concatenated `text`
  events. v2 emits no token or cost events, so those ledger columns stay empty.
- Several installs on one machine (an installer script, npm globals, Homebrew) can shadow each other on
  PATH, and an old binary cannot read a database migrated by v2. Keep one install, or pin it with
  `--bin /opt/homebrew/bin/opencode`.

## Any other harness

The brief is plain text and the report block is plain text, so any agent that can read stdin or a
file works. What spawn.mjs needs from a new harness: a headless command that takes the prompt on stdin,
a way to pin the model and effort, a write vs read-only switch, a session id to resume, and a final
message. Add it as one more branch in `scripts/spawn.mjs` and one section here.

## Choosing a harness per role

| Role | Typical choice | Why |
|---|---|---|
| Orchestrator | Strongest model you have (Claude Code Opus, Codex top model) | Holds the context; every ruling comes from here |
| Plumbing executor (schemas, CRUD, UI, refactors) | Cheapest capable model on any harness | The brief carries the judgement |
| High-risk executor (security, untrusted parsers, money, determinism, cross-system e2e) | Strong model from the start | Rounds of fixes cost more than the stronger model |
| Reviewer | A different vendor or model family from the executor | Independent errors; same-model review misses the same things |
| Scout (find a pattern, list callers) | Cheapest model, read-only | Returns facts and paths, not file dumps |
