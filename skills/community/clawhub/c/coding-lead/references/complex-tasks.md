# Complex Tasks — Roles, QA Isolation, Parallel Strategies

> **Only read this file for Complex-level tasks.** Simple and Medium tasks don't need any of this.

## Complex Task Flow

```
RESEARCH → PLAN → EXECUTE → REVIEW → QA → FIX → RECORD
```

Skip steps that don't apply. Not every complex task needs all steps.

## Coding Roles

**Don't micromanage Claude Code's internal roles.** If Claude Code has its own agent system (e.g., oh-my-claudecode, project-level `.claude/agents/`), it handles role routing internally — architect, reviewer, QA, etc. Just give it the task.

OpenClaw's job for complex tasks:

```
1. RESEARCH (OpenClaw agent reads code, searches memory + qmd)
2. PLAN (agent designs approach, gets confirmation if needed)
3. EXECUTE (spawn ACP — one prompt, Claude Code handles internal delegation)
4. VERIFY (check acceptance criteria after completion)
5. RECORD (log to memory)
```

### When to spawn multiple ACP sessions (max 2)

Only when tasks are **truly independent** (different projects or zero file overlap):
```
Session 1: "Build favorites backend API..." (cwd: project-a)
Session 2: "Fix CSS layout bug..." (cwd: project-b)
```

For complex tasks within ONE project, prefer a single ACP session — Claude Code's internal agents parallelize better than multiple external spawns.

## QA Isolation

If Claude Code has internal QA agents (e.g., OMC test-engineer, qa-tester), it handles test isolation internally.

If you need to ensure isolation explicitly, mention it in the ACP prompt:
> "Write tests based on requirements and interfaces only, not implementation. Use a separate agent/session for tests."

The principle: tests should verify the contract, not mirror the code.

## RESEARCH Phase (No Changes)

Spawn in session mode, investigation only:

```
Investigate <project-dir> for <task description>.

DO NOT make any changes. Only report:
1. Files that need changes
2. Dependencies and call chains
3. Reusable existing code
4. Risks and edge cases
5. Test coverage status

Use qmd/grep/find to explore. Read .openclaw/context-xxx.md for project context.
```

## Agent Routing

Route via `agentId` in `sessions_spawn`. Fallback: preferred → alternate → direct execution.
Claude Code handles its own internal agent selection (OMC, project agents, etc.) — don't duplicate.

## Verification

Verification is mandatory before declaring success. Validate against the stated task, acceptance criteria, explicit constraints, and obvious regressions. If any of these remain unclear, report the gap instead of claiming completion.


| Level | What OpenClaw checks |
|-------|---------------------|
| Simple | No formal review |
| Medium | Success reported? Tests pass? |
| Complex | Acceptance criteria met? Tests pass? No unrelated changes? |

Code review itself is Claude Code's job (it has reviewers internally).

## Definition of Done

### Medium Tasks
- [ ] ACP reported success (or fallback completed)
- [ ] Linter passed (if available)
- [ ] Existing tests pass
- [ ] No unrelated file changes
- [ ] Logged in memory

### Complex Tasks
- [ ] All acceptance criteria met
- [ ] Linter + tests pass
- [ ] Code review passed
- [ ] QA tests written and passing (if applicable)
- [ ] UI changes: screenshots/descriptions included
- [ ] No debug logs, unused imports, temp files
- [ ] Logged in memory with decisions and lessons

## Task Registry

Track active tasks in `<project>/.openclaw/active-tasks.json`:

```json
{
  "id": "feat-favorites",
  "task": "Add favorites feature",
  "status": "running",
  "sessionKey": "acp:run:abc123",
  "startedAt": 1740268800000,
  "complexity": "complex"
}
```

Update on completion/failure. Clean up entries older than 7 days.
Add `.openclaw/` to `.gitignore`.

## Claude Code Tools

Claude Code has its own tools (LSP, Grep, MCP plugins, etc.). Don't list them in ACP prompts — it knows what it has. Only mention a specific tool if the task requires it (e.g., "use Playwright MCP to test the page").

## Prompt Pattern Library

After successful tasks, record what worked:

```bash
# [memory] Record lesson (skip if smart-agent-memory not installed)
node ~/.openclaw/skills/smart-agent-memory/scripts/memory-cli.js learn \
  --action "Built favorites feature" \
  --context "Laravel+React, medium complexity" \
  --outcome positive \
  --insight "Including full DB schema context in prompt upfront made ACP get it right first try" \
  2>/dev/null || echo "memory skip: smart-agent-memory not found"
```

Before spawning, search for similar past tasks (if smart-agent-memory installed): `node ~/.openclaw/skills/smart-agent-memory/scripts/memory-cli.js lessons --context "<similar task type>"`
