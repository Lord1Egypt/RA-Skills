---
name: dev-workflow
description: Orchestrate coding agents (Claude Code, Codex, etc.) to implement coding tasks through a structured workflow. Use when the user gives a coding requirement, feature request, bug fix, or GitHub issue to implement. Includes requirement analysis, document generation (requirement doc + verification doc), agent dispatch, monitoring, verification, and delivery. NOT for simple one-line fixes or reading code. Triggers on coding tasks, feature requests, bug reports, GitHub issues, or "implement/build/fix this".
---

# Dev Workflow — Orchestrated Coding Agent Dispatch

Structured 6-phase gated workflow for driving coding agents to implement requirements with quality control.

## Prerequisites

- Claude Code (`claude` CLI) installed with `--permission-mode bypassPermissions --print`
- [cc-plugin](https://github.com/TokenRollAI/cc-plugin) installed in Claude Code (provides llmdoc read/write, investigator/scout/recorder sub-agents)
- Global `~/.claude/CLAUDE.md` configured with cc-plugin settings

## Workflow Overview

```
Phase 1: Environment Check
    ↓
Phase 2: Spec  ← spec-writer skill
    ↓ [user confirms]
Phase 3: Task Planning
    ↓ [user confirms]
Phase 4: Agent Dispatch
    ↓
Phase 5: Verification
    ↓
Phase 6: Delivery
```

Each phase must complete before moving to the next. Phase 2 and Phase 3 have explicit user confirmation gates.

---

### Phase 1: Environment Check

Before any work, check the target project:

1. **`llmdoc/` exists?**
   - Yes → read `llmdoc/index.md` + overview files to understand project
   - No → dispatch Claude Code with `/tr:initDoc` to generate it first
2. **`CLAUDE.md` in project root?** — verify cc-plugin config is present; fix if missing
3. **`git status`** — ensure working tree is clean enough to work on

### Phase 2: Spec

Generate a structured implementation spec using the **spec-writer** skill.

1. Activate `spec-writer` skill — read its SKILL.md and follow its workflow
2. It will gather project context, draft a spec using its template, and present to the user
3. The spec covers: objectives, user stories, technical plan, boundaries, verification criteria, and a preliminary task breakdown
4. **🚫 Gate: Do not proceed until the user confirms the spec.**

The confirmed spec replaces the old requirement-doc + verification-doc pair — everything is in one document now.

> **Fallback:** If spec-writer skill is not installed, use the templates in `references/` (requirement-template.md + verification-template.md) as before.

### Phase 3: Task Planning

Refine the spec's preliminary task breakdown into a precise, executable task list. This is the bridge between "what to build" and "how to tell the agent."

#### 3.1 Extract Tasks from Spec

Start from Section 10 (Task Breakdown) of the confirmed spec. For each task, expand it into a **Task Card**:

```markdown
### Task [#]: [Title]

**Objective:** What this task accomplishes (one sentence)
**Input:** What must exist before this task starts (files, tables, APIs from prior tasks)
**Output:** What this task produces (new/modified files, passing tests, working endpoint)
**Affected files:**
- `src/xxx.py` — create / modify
- `tests/test_xxx.py` — create

**Agent instructions:**
- [Specific, actionable instruction 1]
- [Specific, actionable instruction 2]
- Reference: [relevant spec section, e.g., "See Spec §4.2 for design decision"]

**Verification:**
- [ ] [How to confirm this task is done — a command, a test, an observable result]

**Depends on:** Task #X, #Y (or "none")
**Complexity:** Low / Medium / High
**Parallel:** Can run in parallel with Task #Z (or "no")
```

#### 3.2 Scoping Rules

Each task should be:

- **Independently implementable** — an agent can complete it without context from other incomplete tasks
- **Independently verifiable** — there is a concrete way to check it worked (test passes, endpoint responds, file exists)
- **Small enough to review** — aim for changes reviewable in one pass (rough guide: <300 lines changed)
- **Large enough to be meaningful** — don't split a 20-line function into 3 tasks

**Splitting heuristics:**
- If a task touches >3 unrelated modules → split by module
- If a task has both "create infrastructure" and "implement logic" → split
- If a task requires multiple design decisions → split by decision boundary
- If you can describe two independent verification criteria → likely two tasks

#### 3.3 Dependency Graph

After expanding all tasks, produce a dependency summary:

```
Task 1 (Low)  ─┐
Task 3 (Low)  ─┤─→ Task 5 (Medium) ─→ Task 7 (Medium)
Task 2 (Medium) ─→ Task 4 (Medium) ─┤
Task 6 (High) ────────────────────────┘─→ Task 8 (Medium)
```

Identify:
- **Critical path** — longest chain of dependent tasks
- **Parallel groups** — tasks that can run simultaneously
- **Execution order** — the sequence to dispatch agents

#### 3.4 Context Budgeting

For each task, determine what context the agent needs:

- **Spec sections to include** — only the relevant parts, not the full spec (avoid context overload)
- **Existing code to reference** — specific files, not "the whole src/"
- **Boundaries to emphasize** — the ✅/⚠️/🚫 rules most relevant to this task

Principle: feed the agent only what it needs for the current task. A well-fed agent is like a well-fed function — give it only the inputs for the job at hand.

#### 3.5 User Confirmation

Present the task list to the user with:
- All task cards (or a summary table + full cards on request)
- Dependency graph
- Estimated execution order (serial vs parallel)
- Highlight the critical path

**🚫 Gate: Do not dispatch any agents until the user confirms the task plan.**

Common discussion points:
- Is the granularity right? (too fine → overhead; too coarse → risky)
- Are dependencies correct? Can anything be parallelized further?
- Any task missing from the spec's intent?

### Phase 4: Agent Dispatch

Execute the confirmed task plan by dispatching coding agents.

#### 4.1 Prompt Construction

For each task, construct the agent prompt from the task card:

```bash
claude --permission-mode bypassPermissions --print '<task prompt>' 2>&1
```

**Task prompt structure:**

```
## Task: [Title]

### Objective
[From task card]

### Context
[Relevant spec sections — copy only what's needed]
[Relevant existing code snippets or file references]

### Instructions
[Agent instructions from task card]

### Constraints
- 不要 git commit
- 完成后执行 /update-doc 更新 llmdoc
- [Relevant boundaries from spec §7]

### Verification
When done, confirm:
- [Verification criteria from task card]
```

**Use `workdir`** to scope the agent to the project directory.
**Use `background: true`** for long-running tasks, monitor with `process` tool.

#### 4.2 Execution Strategy

- **Serial tasks** (has dependencies): wait for dependency to complete and verify before dispatching
- **Parallel tasks** (independent): dispatch simultaneously, use git worktrees if touching overlapping files
- **After each task completes:**
  1. Check agent output for errors
  2. Run the task's verification criteria
  3. If verification fails → re-prompt the agent with the failure details (up to 2 retries)
  4. If still fails → stop and report to user

#### 4.3 Error Handling

| Situation | Action |
|-----------|--------|
| Small error (syntax, typo, missing import) | Re-prompt agent to fix, no user interruption |
| Test failure on the current task | Re-prompt with test output, up to 2 retries |
| Design-level issue or ambiguity | **Stop and ask the user** |
| Agent produces output that contradicts spec | Stop, quote the spec conflict, ask user |
| Downstream task blocked by upstream failure | Pause dependent tasks, attempt to fix upstream first |

### Phase 5: Verification

After all tasks complete, verify the whole against the spec's verification criteria (Section 9):

1. **Automated checks (§9.1)** — run tests, build, lint, type check
2. **Functional verification (§9.2)** — execute each test scenario step by step
3. **Edge cases & error handling (§9.3)** — verify each edge case
4. **Regression (§9.4)** — confirm existing functionality unaffected
5. **Code quality** — style consistency, no stray files, no hardcoded secrets

If any verification fails:
- Identify which task(s) caused the issue
- Re-dispatch agent to fix, providing the failure context
- Re-verify after fix

### Phase 6: Delivery

Present results to the user with:

1. **All changed files** — every file touched, including llmdoc updates, config changes, everything
2. **Suggested commit message** — conventional commits format
3. **Task completion summary** — which tasks passed, any retries needed
4. **Verification results** — what passed, any caveats
5. **Items for human review** — what needs the user's attention

**Never commit.** The user handles all git commits.

## Agent Selection

Default: **Claude Code** (`claude --permission-mode bypassPermissions --print`)

| Agent | Use when |
|-------|----------|
| Claude Code | Default for all tasks; complex reasoning, architecture |
| Codex | User explicitly requests; batch/parallel tasks (`pty:true`, `--full-auto`) |
| OpenCode/Pi | User explicitly requests |

## Key Constraints

- **Never commit** — code changes only, user commits
- **Never run agents in `~/.openclaw/`** — agents will read soul/identity files
- **Always update llmdoc** — every agent run should end with doc update
- **Always list all changed files** on delivery
- **Always provide commit message** on delivery
- **Interrupt on design issues** — don't let agents drift on wrong assumptions
- **Feed minimal context** — each agent gets only spec sections and files relevant to its task
