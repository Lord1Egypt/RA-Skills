---
name: adaptive-review
description: Adaptive code review that routes to haiku/sonnet/opus based on diff complexity signals. Use instead of requesting-code-review for cost-efficient reviews.
---

# Adaptive Code Review

Review code changes with model depth proportional to change complexity. No wasted opus tokens on trivial diffs.

## Step 1: Collect Signals

Run these commands to gather diff signals:

```bash
# Get diff stats (against HEAD~1 or origin/main, whichever makes sense)
BASE=$(git merge-base HEAD origin/main 2>/dev/null || echo "HEAD~1")
git diff --stat $BASE..HEAD
git diff --numstat $BASE..HEAD
```

Extract:
- **lines_changed**: total added + deleted
- **files_changed**: number of files
- **dirs_changed**: number of unique top-level directories touched (cross-module indicator)

Then scan for high-risk patterns — **only in code files** (exclude .md/.txt/.json/.yaml from grep):

```bash
git diff $BASE..HEAD -- '*.ts' '*.js' '*.py' '*.go' '*.rs' '*.java' '*.c' '*.cpp' '*.rb' '*.sh' | grep -ciE '(password|secret|token|auth|session|cookie|sql|inject|exec\(|eval\(|lock|mutex|semaphore|atomic|concurrent|unsafe)'
```

- **risk_hits**: count of matches (0 if only docs/config changed)

## Step 2: Route

| Condition | Depth | Model |
|-----------|-------|-------|
| lines_changed < 50 AND files_changed <= 1 AND risk_hits == 0 | **fast** | haiku |
| lines_changed < 200 AND dirs_changed <= 1 AND risk_hits <= 2 | **medium** | sonnet |
| Everything else (>200 lines OR dirs_changed >= 2 OR risk_hits > 2) | **deep** | opus |

Announce the routing decision:
```
Review depth: [fast|medium|deep] (N lines, N files, N dirs, N risk hits)
```

## Step 3: Dispatch

### Fast (haiku)
Spawn agent with `model: "haiku"`, subagent_type of your code-review agent:

Prompt focus: formatting, naming conventions, obvious bugs, unused imports. Skip architecture analysis. Keep it under 30 seconds.

### Medium (sonnet)
Spawn agent with `model: "sonnet"`, subagent_type of your code-review agent:

Standard code review: correctness, error handling, test coverage, code quality.

### Deep (opus)
Spawn agent with `model: "opus"`, subagent_type of your code-review agent:

Full review: architecture, security, performance, cross-module impact. If language-specific reviewers exist (python-reviewer, go-reviewer, database-reviewer), spawn them in parallel.

## Step 4: Report

Present results with depth label so the user knows what level of review was applied:

```
## Adaptive Review: [FAST|MEDIUM|DEEP]
Signals: {lines} lines, {files} files, {dirs} dirs, {risk_hits} risk hits

[reviewer output]
```

If fast review finds anything concerning, suggest upgrading: "Fast review flagged potential issues. Run `/adaptive-review --deep` for thorough analysis."

## Overrides

User can force depth:
- `/adaptive-review --fast` — force fast regardless of signals
- `/adaptive-review --deep` — force deep regardless of signals
- `/adaptive-review --medium` — force medium
