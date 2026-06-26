# SWARM.md — Agent Swarm Protocol

How the Friday Budgeting Pro repo gets built by a swarm of AI agents.
Read this before doing any PM or worker activity.

## Roles

### PM (one persistent Opus agent)
- Long-lived session keyed `session:friday-bp-pm`
- Triggered by a cron job every 30 minutes
- Never writes code. Only: triages tickets, spawns workers, reviews PRs, merges.
- Adheres strictly to [ARCHITECTURE.md](./ARCHITECTURE.md) — if a worker's PR violates it, request changes.
- **Only the PM may merge.** Workers never self-merge.

### Workers (up to 5 concurrent agents)
- One per ticket
- Spawned by the PM via `sessions_spawn` (mode=`run`, isolated context)
- Implements the ticket, runs interactive sanity checks, opens a PR, then **stays alive** waiting for PM review
- If the PM requests changes: worker addresses every comment, re-runs tests + interactive checks, re-pushes, and comments "Ready for re-review" on the PR
- Worker exits only after the PM has **approved and merged** the PR — or after being killed
- **Model selection (cost-aware):**
  - **Haiku** (cheapest) for: docs-only tickets, single-file stubs, schema or config-only changes, smoke tests, any `good-first-issue` labeled ticket
  - **Sonnet** for everything else — default worker model
  - **Opus** is reserved for the PM. Workers do not use it.

## PM Tick Loop (every 30 min)

On every tick, the PM does this in order:

### 1. Health check on running workers
- `subagents action=list recentMinutes=90`
- If any worker has been running >90 min with no PR opened, **kill it** and post a comment on the issue: "Worker timed out, re-queueing."
- If a worker opened a PR and has been idle >60 min waiting for review, that's fine — the PM will review it this tick.
- If a worker errored out, kill it and re-queue.

### 2. Review open PRs
For each open PR (`gh pr list --state open`):
- Read the PR body + the linked issue
- Check CI status (`gh pr checks`) — if CI is still running, skip this PR until next tick
- If CI is failing: post a `request-changes` review with the exact failure. Worker must fix it.
- If CI is green, review the diff against:
  - The linked issue's scope (no scope creep)
  - ARCHITECTURE.md (no design violations)
  - CONTRIBUTING.md anti-patterns
  - Interactive check line present in PR body (required for UI + MCP tickets)
- **Documentation check:** verify the PR updates ARCHITECTURE.md, README.md, and the route overview comment where relevant. If docs are missing, request changes — do not merge undocumented behaviour changes.
- **SKILL.md check:** if the PR adds, removes, or renames any `@mcp.tool` in `server/main.py`, verify SKILL.md is updated in the same commit. The `skill-md-sync` CI job catches this automatically — a green CI badge is sufficient; reject if it's red.
- **Decide:**
  - ✅ Looks good + CI green → `gh pr review --approve`, then `gh pr merge --squash --delete-branch`
  - ❌ Issues → `gh pr review --request-changes --body "<specific feedback>"`, leave PR open. Worker will fix and re-push.
  - ⚠️ Borderline → comment with suggestions but approve if the spirit is right. Workers are AI — don't nitpick.

### 3. Spawn next worker(s) (if room)
- Concurrency: **at most 5 active workers at a time** (workers waiting on review count toward this limit).
- Workers must work on **non-overlapping tickets** (different files where possible) to avoid merge conflicts. If only conflicting tickets are eligible, run them serially.
- Find eligible tickets:
  - Open, labeled `task`, no assignee, no linked open PR
  - All dependencies (listed in the issue body's "Depends on") are closed/merged
- Prefer tickets in this order: phase-1, phase-2, phase-3, ..., infra, then good-first-issue across phases as filler
- Pick the cheapest model that can do the job (see Model selection above).
- Spawn each worker:
  ```
  sessions_spawn(
    runtime="subagent",
    mode="run",
    model="haiku" | "sonnet",  // never opus
    label=f"friday-bp-worker-{issue_number}",
    task="""You are a worker agent for Friday Budgeting Pro.
Repo: /Users/hal9000/.openclaw/workspace/bank-transactions

1. Read CONTRIBUTING.md, ARCHITECTURE.md, and issue #{n}.
2. Follow the Worker Loop in SWARM.md exactly.
3. Open a PR with 'Closes #{n}' in the body.
4. STAY ALIVE after opening the PR — poll for PM review every 10 minutes using:
   gh pr view <PR_NUM> --json reviewDecision,reviews,comments
5. If the PM requests changes: fix every comment, re-run tests + interactive checks, re-push, comment 'Ready for re-review'.
6. Exit ONLY after the PM has approved and the PR is merged (gh pr view shows 'MERGED').
""",
    cwd="/Users/hal9000/.openclaw/workspace/bank-transactions",
    cleanup="keep",
    runTimeoutSeconds=7200  // 2hr hard cap (allows for review cycles)
  )
  ```
- Self-assign each issue: `gh issue edit <n> --add-assignee @me`
- Comment on each issue: "Assigned to worker `friday-bp-worker-<n>`. Worker will stay live through review and merge."

### 4. Log the tick
- Append a short summary to `~/.friday-bp-swarm/pm.log`:
  ```
  2026-05-23T18:30 — reviewed 2 PRs (merged #11, requested changes on #12). Spawned workers for #13, #14. Active workers: 3.
  ```

### 5. Done
- Yield. Next tick happens via cron in 30 min.

## Worker Loop

1. Read CONTRIBUTING.md, ARCHITECTURE.md, the linked issue.
2. Check `gh pr list` for an existing PR on this issue — if one exists, abort (don't double-work).
3. `git checkout main && git pull && git checkout -b agent/<issue-num>-<slug>`.
4. Implement strictly within the ticket's scope.
5. Run tests locally (`python3 -m pytest -q --ignore=tests/test_plaid_e2e.py`). Must be green.
6. **Interactive sanity check (mandatory for UI and MCP tickets — do not skip):**
   - **UI tickets:** Start the UI server (`python3 -m uvicorn ui.server:app --host 0.0.0.0 --port 6789`) and use Peekaboo browser automation to verify the affected page loads, key elements are present, and the core flow works. Kill the server after.
   - **MCP tickets:** Call the new/changed tools directly in Python and confirm they return real output — not `{'status': 'not_implemented'}` or unhandled exceptions.
   - **Other tickets (infra, docs, schema):** pytest is sufficient, no interactive check needed.
7. `git add . && git commit -m "..."` with a clear message.
8. `git push -u origin <branch>`.
9. Open PR:
   ```
   gh pr create \
     --title "[Pn] <ticket title>" \
     --body "Closes #<n>

   <short summary of what was implemented>

   **Interactive check:** <one line — what was tested and that it passed, or 'N/A (infra/docs)'>

   **CI:** will update automatically"
   ```
10. **Stay alive.** Poll every 10 min: `gh pr view <PR_NUM> --json state,reviewDecision,reviews`.
    - If `state=MERGED` → exit cleanly.
    - If PM posted `request-changes`: read all comments, fix them, re-run tests + interactive checks, re-push, comment "Ready for re-review."
    - If `state=CLOSED` (without merge) → exit. PM decided to abandon.
    - If stuck >2hr total → exit with a comment on the PR explaining the timeout.

## Communication

- Workers communicate with the PM only via GitHub (PR comments, CI status). No direct messaging.
- PM does NOT interrupt running workers mid-implementation. If steering is needed, it kills + re-spawns.
- All decisions are visible in GitHub history — for human auditability.
- **Only the PM merges.** Workers push and request review. Never `gh pr merge` from a worker.

## Stopping the Swarm

```bash
# Remove the cron job (stops new ticks)
cron remove a72347e9-5108-44e3-bf51-b6637d234e40

# Kill active workers
subagents action=kill target=friday-bp-worker-<n>
```

Or tell the main HAL session: "pause the friday budgeting swarm."

## Honest Limits

- AI workers will sometimes get stuck or write nonsense. The PM kills + retries; if a ticket fails 3 times, the PM labels it `human-needed` and moves on.
- Some tickets need real Plaid credentials — workers mock those. E2E (#28) is manual (run by the user).
- **The user still does:** final manual E2E test, Plaid Production setup, `clawhub publish`.
