# OpenClaw Local Playbook

Use this playbook when the skill is running inside the current local OpenClaw setup.

The repository also supports an `agents` registry so work can dispatch to custom agents beyond the five shown here. Define each agent’s `id`, `description`, and capability metadata in the routing config, then map `task_types`/`domains` to those ids; the local profile below is just a runnable example that matches the workspace constraints.

## Local Constraints

- Allowed sub-agents: `codex`, `invest`, `content`, `knowledge`, `community`
- ACP dispatch is enabled
- Default ACP agent: `codex`
- Maximum concurrent sub-agents: `2`

If a request does not clearly fit one of those agent ids, do not invent a new one. Keep it in `main`.

## Fast Routing Table

| User Request Pattern | Task Type + Domain | Route To | Keep Local? |
|---|---|---|---|
| "这个报错怎么来的" | `explore + code` | `codex` | No |
| "修这个 bug" | `implement + code` | `codex` | No |
| "帮我 review 这个改动" | `verify + code` | `main` first | Usually yes |
| "把这篇内容入库" | `operate + knowledge` | `knowledge` | No |
| "我之前记过这个吗" | `explore + knowledge` | `knowledge` | No |
| "给我写 3 个标题" | `implement + content` | `content` | Sometimes |
| "去社区发个帖" | `operate + community` | `community` | No |
| "分析一下这个股票" | `explore + invest` | `invest` | No |
| "配置一下本地环境" | ambiguous / coupled | `main` | Yes |
| "你直接做" | explicit no-spawn | `main` | Yes |

## OpenClaw-Safe Dispatch Rules

### Keep It In `main`

Use `main` when:

- the answer is short and direct
- the next step is blocked on the result immediately
- the task mixes multiple domains without clear boundaries
- the user explicitly wants the current agent to do it
- you cannot write a bounded task contract in one pass

### Dispatch To `codex`

Use `codex` when:

- the task needs code reading, code changes, test execution, or repo analysis
- you can name the owned files or owned modules
- the main agent can still verify the result afterward

### Dispatch To `knowledge`

Use `knowledge` when:

- the task is archiving, note organization, retrieval, linking, tagging, or summarization into the knowledge base
- the success condition is a final note path, archive path, or structured knowledge output

### Dispatch To `content`

Use `content` when:

- the task is drafting, rewriting, outlining, packaging, or title generation
- the deliverable is text, not code

### Dispatch To `community`

Use `community` when:

- the task is posting, replying, engaging, or operating on community channels
- the side effect is external communication

### Dispatch To `invest`

Use `invest` when:

- the task is investment analysis, market scanning, watchlist work, or finance-specific workflows
- timeliness and domain judgment matter more than generic writing

## Task Contract Template For OpenClaw

Before dispatch, write a contract with these fields:

```text
Goal: What the sub-agent must accomplish
Expected output: Exact artifact or response shape
Owned scope: Files, notes, channels, or symbols it may touch
Forbidden scope: What it must not edit or operate on
Blocking status: blocking | sidecar
Verification method: How main will verify the result
```

Example:

```text
Goal: Investigate why the retry flow times out under repeated network failures.
Expected output: Root-cause summary plus likely fix scope and inspected files.
Owned scope: Read-only inspection of src/retry/* and tests/retry/*.
Forbidden scope: Do not edit files or inspect unrelated modules.
Blocking status: blocking
Verification method: Main agent checks whether findings cite inspected files and observed failure points.
```

## Parallel Dispatch In OpenClaw

Parallelize only if all of these are true:

- total active sub-agents stays at `2` or less
- write scopes do not overlap
- each task can be explained independently
- the main agent can cheaply integrate the outputs

Safe example:

```text
Task A -> codex: inspect backend retry path (read-only)
Task B -> knowledge: retrieve prior notes about retry incidents
Main -> compare findings and decide next step
```

Unsafe example:

```text
Task A -> codex: refactor auth/
Task B -> codex: fix tests in auth/
```

Those collide on the same area and should stay sequential.

## Acceptance Checklist For `main`

Before returning to the user, `main` should verify:

1. The sub-agent stayed inside owned scope.
2. The expected output actually exists.
3. The result is materially complete.
4. Any claimed verification was really run.
5. No other agent output conflicts with it.
6. The final answer is synthesized instead of forwarded as raw fragments.

## Resume and Recovery Reminder

Long-lived supplies and bundles persist their `dispatch_id` and `bundle_dir`. When an execution is interrupted, call `scripts/resume-orchestration.py` with the saved state to pick up where you left off, reusing the existing dispatch metadata and adapter outputs. Use `scripts/state-store.py update-resume` to inspect or repair the resume metadata before rerunning.

## Local Verification Checklist

Before relying on this skill in day-to-day local orchestration, run:

```bash
./scripts/verify-openclaw-local.sh
```

This confirms:

- the CLI version currently on `PATH`
- the installed directory skill still reports `Ready`
- the local `main` agent runtime can read the workspace orchestration rules and answer with the expected allowed agent ids plus resume-first behavior

If the local turn prints a warning about a newer config version than the current runtime, verify the actual binary path with `which -a openclaw` and compare it with `openclaw update status`. Treat that warning as a path/service mismatch to investigate before concluding the upgrade failed.
