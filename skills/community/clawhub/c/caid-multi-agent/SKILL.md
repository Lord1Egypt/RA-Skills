---
name: caid-multi-agent
description: Coordinate multiple sub-agents to collaboratively complete long-horizon software engineering tasks using the CAID (Centralized Asynchronous Isolated Delegation) paradigm. Use when tasks require complex multi-file edits, interdependent subtasks, parallelizable work, or when a single agent would take too long. This skill implements branch-and-merge coordination with git worktree isolation, dependency-aware task delegation, and structured integration. CRITICAL: Never use CAID as a fallback after single-agent failure; use from the outset. Max 2-4 engineers (8 absolute max). Physical git worktree isolation is mandatory; soft isolation degrades performance.
---

# CAID Multi-Agent Coordination

This skill implements the **Centralized Asynchronous Isolated Delegation (CAID)** paradigm for coordinating multiple agents working on shared artifacts.

> ⚠️ **CRITICAL WARNINGS FROM PAPER:**
> - **Use CAID from the outset** — Don't run single-agent first as fallback. Sequential strategy costs nearly 2x with minimal gain.
> - **Physical worktree isolation is mandatory** — Soft isolation (instruction-only) degrades performance on complex tasks.
> - **Engineer limits are strict** — 2 for PaperBench-style, 4 for Commit0-style, never exceed 8.
> - **Higher cost/runtime trade-off** — CAID improves accuracy, not speed. Integration is sequential/test-gated.

## Core Principles

1. **Centralized Task Delegation** — A manager agent decomposes tasks into dependency-aware units
2. **Asynchronous Execution** — Multiple engineer agents work concurrently
3. **Isolated Workspaces** — Each agent works in its own isolated branch/worktree
4. **Structured Integration** — Progress is merged via git commit/merge with test verification

## When to Use This Skill

**Use CAID from the outset for:**
- Long-horizon tasks with multiple interdependent files
- Clear dependency structure (imports, test mappings)
- Parallelizable work exists
- Integration can be verified by executable tests

**Don't use as fallback:** Running single-agent first then CAID is inefficient (cost/runtime nearly additive, minimal performance gain).

**Use single-agent for:**
- Isolated, single-file changes
- No clear parallelization opportunities
- Exploratory/research-oriented tasks

## Coordination Workflow

### 0. Manager Pre-Setup (CRITICAL)

**Before ANY delegation, the manager must:**

1. **Prepare runtime environment**
   - Ensure dependencies installed
   - Set up virtual environment

2. **Organize entry points**
   - Create main entry files
   - Ensure import paths work

3. **Add minimal function stubs**
   - Empty function definitions so imports don't fail
   - Type signatures if available

4. **Commit to main branch**
   - All engineer branches created from consistent base
   - Without this, engineers start from divergent states

```bash
# Pre-setup commit
git add .
git commit -m "setup: initial stubs and entry points"
git push origin main
```

### 1. Task Analysis & Dependency Graph Creation

**Manager's role:** Before delegating, analyze the task structure:

- Identify atomic units of work (files, functions, modules)
- Build a dependency graph: G=(V,E) where edges indicate dependencies
- Define Ready(v) ⇔ all dependencies of v are completed
- Only delegate tasks that are Ready (all dependencies satisfied)

**Commit0-style tasks (clear file structure):**
1. Check import statements to identify file-level dependencies
2. Collect executable test cases from repository
3. Examine which files tests exercise
4. Identify components to implement earlier (upstream dependencies)
5. **Delegate at file level first** — only split to function level if file has many unimplemented functions

**PaperBench-style tasks (inferred structure):**
1. Read paper to identify main contribution
2. Infer implementation order from contribution
3. **Use max 2 engineers** — manager task is harder, more agents destabilize

**Dependency graph construction:**
```
Ready_t(v_j) ⇔ ∀(v_i, v_j) ∈ E, v_i ∈ Completed_t

Only delegate tasks from {v ∈ V | Ready_t(v)}
```

### 2. Workspace Isolation Setup

**Create PHYSICALLY isolated worktrees (not soft isolation):**

```bash
# Main branch is the single source of truth
git worktree add ../workspace-engineer-1 <branch-name-1>
git worktree add ../workspace-engineer-2 <branch-name-2>
# etc.
```

> ⚠️ **WARNING:** Soft isolation (same workspace, instruction-level constraints) degrades performance to below single-agent on PaperBench. Physical `git worktree` isolation is **mandatory**.

**Key isolation principles:**
- Each engineer operates in its own git worktree (physical filesystem isolation)
- All worktrees are derived from the main branch
- Engineers modify files only within their assigned workspace
- **Restricted files** (shared across engineers): `__init__.py`, config files, global constants — engineers must NOT commit changes to these

### 3. Dependency-Aware Task Delegation

**STRICT Engineer Limits:**
| Task Type | Max Engineers | Why |
|-----------|--------------|-----|
| PaperBench-style | 2 | Inferred dependencies; more destabilizes |
| Commit0-style | 4 | Clear file structure; test-guided |
| General SWE | 2-4 | Balance parallelism vs integration overhead |
| Absolute max | 8 | Beyond this, coordination tax exceeds gains |

> ⚠️ **Critical:** Increasing engineers beyond optimal degrades performance due to integration overhead and conflict resolution costs.

**Task prioritization heuristics:**
Manager should prioritize tasks that:
1. **Enable earlier test execution** (expose evaluation signals sooner)
2. **Lie closer to upstream** of dependency chain
3. **Are simpler functions** before complex ones

**Round definition:**
> One round = complete cycle of **delegation → implementation → dependency update**

**Recommended iteration limits (from paper experiments):**
| Role | Max Iterations |
|------|---------------|
| Manager | 50 |
| Each Engineer | 80 |
| Total Rounds | ~22 (varies by task) |

**Delegation algorithm:**

```
At round t:
1. Ready_Set = {v ∈ V | Ready_t(v)}  // all dependencies satisfied
2. Select up to N tasks from Ready_Set (N = max parallel engineers above)
3. Apply prioritization heuristics
4. Delegate to available engineers
5. Wait for completion signals
6. Update dependency state after each successful integration
```

**Task assignment JSON format (structured communication — NO free-form dialog):**

```json
{
  "task_id": "string",
  "task_description": "string",
  "target_files": ["path/to/file.py"],
  "target_functions": ["function_name"],
  "dependencies": ["task_id_1", "task_id_2"],
  "expected_outcome": "description of success criteria",
  "verification_command": "pytest tests/test_file.py -v",
  "restricted_files": ["src/__init__.py", "src/config.py"],
  "priority": "high|medium|low"
}
```

> **Key:** All communication uses structured JSON, not free-form dialog. This prevents inter-agent misalignment (primary failure mode in multi-agent systems).

### 4. Asynchronous Execution Loop

**Event loop pattern:**

1. **Delegate** → Manager assigns tasks to available engineers
2. **Execute** → Engineers work concurrently in isolated worktrees
3. **Self-Verify** → Engineer runs tests, fixes failures
4. **Complete** → Engineer submits commit when ALL tests pass
5. **Integrate** → Manager attempts merge to main
6. **Conflict Resolution** (if needed) → Responsible engineer resolves
7. **Update** → Manager updates dependency graph
8. **Repeat** → Continue until all tasks complete or limits reached

**Engineer self-verification (MANDATORY before submission):**
- Run relevant tests that import/reference modified files
- If no explicit mapping, run repository's default test command
- Any failed test or runtime exception MUST be resolved
- Use concrete error logs and tracebacks for iterative refinement
- **Only submit commit after ALL tests pass**

### 5. Integration via Merge

**Merge workflow:**

```bash
# Manager attempts merge
git checkout main
git merge <engineer-branch>

# If conflict:
# 1. Engineer who produced conflicting commit is RESPONSIBLE for resolution
# 2. Engineer pulls latest main: git pull origin main
# 3. Resolves conflicts locally
# 4. Re-runs tests to ensure resolution didn't break anything
# 5. Resubmits commit
# 6. Manager retries merge
```

**Main branch is single source of truth** throughout execution.

### 6. Context Management for Manager

To prevent context explosion, manager uses **LLMSummarizingCondenser** pattern:

```
Periodically:
1. Summarize prior interaction rounds
2. Preserve structured artifacts:
   - Dependency graph (current state)
   - Completed tasks (with commit hashes)
   - Unresolved errors (with traceback summaries)
3. Discard detailed conversation history
4. Maintain execution traceability without bloat
```

**Compressed execution history format:**
```json
{
  "round": 5,
  "completed": ["task-1", "task-2", "task-3"],
  "ready": ["task-4", "task-5"],
  "blocked": ["task-6: waiting for task-5"],
  "active_engineers": 2,
  "main_branch_commits": ["abc123", "def456"],
  "unresolved_errors": []
}
```

### 7. Worktree Synchronization & Cleanup

**State synchronization when main advances:**

```bash
# Engineer syncs to latest integrated state
cd ../workspace-engineer-1
git fetch origin
git reset --hard origin/main  # Sync worktree to latest main
```

**Worktree cleanup (after completion or limit reached):**

```bash
# Remove worktree when engineer finishes or hits iteration limit
git worktree remove ../workspace-engineer-1
rm -rf ../workspace-engineer-1  # Clean up directory
```

> Worktrees are deleted after all assigned tasks are completed or when the engineer reaches the predefined iteration limit.

### 8. Termination Conditions

- **Success:** All units completed and integrated into main
- **Failure:** Maximum rounds/iterations reached with unresolved tasks
- **Incomplete:** Task considered incomplete if any units remain unresolved

**Manager iteration limits (from paper):**
- Manager: `max_iterations=50`
- Each engineer: `max_iterations=80`
- Total rounds: ~22 (varies by task)

### 9. Manager Final Review

> **After the asynchronous loop completes, the manager does a final review before submitting the final product.**

**Final review checklist:**
1. Verify all tasks from dependency graph are completed
2. Run full test suite: `pytest tests/ -v`
3. Check integration completeness (all commits merged)
4. Review any unresolved errors or warnings
5. Validate final state matches expected outcome
6. Submit final product only after verification

```bash
# Manager final verification
git checkout main
pytest tests/ -v                    # Full test suite
python -m mypackage --version       # Smoke test
# Review any integration gaps
```

## Implementation Guidelines

### Using OpenClaw Sub-agents

For OpenClaw, the `sessions_spawn` tool enables parallel agent execution:

**Spawn engineer agents:**

```javascript
// For each task in Ready_Set, spawn an engineer
{
  "runtime": "subagent",
  "task": "<task specification with context>",
  "agentId": "<engineer-agent-id>",
  "mode": "run",
  "runTimeoutSeconds": 300
}
```

**Check progress:**

```javascript
// Poll for completion
{
  "action": "list"
}
```

### Worktree Synchronization

**When main advances, update worktrees:**

```bash
# Engineer pulls latest main before continuing
cd ../workspace-engineer-1
git fetch origin
git reset --hard origin/main  # Or rebase
```

This ensures engineers work from latest integrated state.

### Verification Intensity vs Efficiency Trade-off

From paper analysis (Section 4.4):

| Strategy | Pass Rate | Runtime | When to Use |
|----------|-----------|---------|-------------|
| Round-Manager Review | 60.2% | 3689s | Maximum correctness required |
| Engineer Self-Verification | 55.1% | 2244s | **Default - balanced** |
| Efficiency-Prioritized | 54.0% | 1909s | Time-critical, acceptable risk |

**Default:** Engineer self-verification without repeated manager review.

## Common Pitfalls & Solutions

| Pitfall | Solution |
|---------|----------|
| Using CAID as fallback after single-agent fails | Use from outset; sequential costs ~2x with minimal gain |
| Soft isolation (instruction-only) | Mandatory `git worktree` physical isolation |
| Too many engineers (>4-8) | Strict limits: 2 PaperBench, 4 Commit0, 8 absolute max |
| Skipping manager pre-setup | Always prepare runtime/stubs/entry points first |
| Skipping manager final review | Always do final verification before submission |
| Merge conflicts from concurrent edits | Group dependent files; engineer resolves own conflicts |
| Not cleaning up worktrees | Delete worktrees after completion/limit reached |
| Agents develop inconsistent views | Structured JSON only; no free-form dialog |
| Silent interference between agents | Explicit merge with test verification |
| Tasks not clearly defined | Build dependency graph before ANY delegation |
| Integration failures discovered late | Self-verification mandatory before commit |
| Context explosion | Use LLMSummarizingCondenser pattern |
| Missing restricted files | Mark `__init__.py`, configs as restricted |

## Cost/Runtime Expectations

**CAID trade-offs (vs single-agent):**
- **Higher API cost** — Multiple agents = more LLM calls
- **Similar or longer wall-clock time** — Integration is sequential/test-gated
- **Substantially higher accuracy** — +26.7% PaperBench, +14.3% Commit0

**When worth it:** Long-horizon shared-artifact tasks where correctness matters more than speed.

## Example Workflows

See [references/examples.md](references/examples.md) for concrete implementation examples including:
- Commit0-style library implementation
- PaperBench-style paper reproduction
- Bug fixing (single-file vs multi-file)
- Feature addition with API and frontend

## References

- Paper: "Effective Strategies for Asynchronous Software Engineering Agents" (arXiv:2603.21489v1)
- GitHub: https://github.com/JiayiGeng/async-swe-agents
- Built on OpenHands agent SDK principles