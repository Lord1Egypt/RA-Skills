---
name: create-pr
description: End-to-end pull-request flow with a review gate — reviews the branch BEFORE publishing (code-review skill's branch scope if installed; blockers must be fixed or explicitly waived), pushes with user approval, creates one PR per repo for multi-repo work items with house defaults from config (title pattern, target branch, required reviewers, auto-complete, work-item link), cross-references sibling PRs with deploy-order coupling, verifies every setting after creation, and reports the URLs. Detects the provider from the git remote (Azure DevOps via the azure-devops skill, GitHub via gh). Use this skill whenever the user says "create a PR", "open a pull request", "publish the branch and create a PR", "PR this", "ship this branch", "create the PRs for this task", or "raise a PR" — even if they don't explicitly say "create-pr skill". For reviewing someone else's PR (not creating one), use a review skill instead.
---

# Create PR

The full flow from "the branch is ready" to "verified PRs exist" — with the review gate where it belongs: **before** anyone else sees the code.

## When to use this skill

- "create a PR" / "open a pull request" / "raise a PR"
- "publish the branch and create a PR" / "ship this branch"
- "create the PRs for this task" (multi-repo)

Do **not** use for reviewing an existing PR (use `code-review`'s branch scope) or for local-only git work.

## Workflow

### 0. Anchor

State in one line: work item/ticket id, branch name, and every repo the change touches. The id comes from the branch name or the commit subjects you read this session (`git log --oneline <target>..HEAD`) — never from memory of the conversation, and never a number mentioned earlier for different work. If neither carries one, ask — it drives the PR title, the work-item link, and the sibling grouping; an invented id links the PR to someone else's ticket. Multi-repo detection: a change described as one task with commits carrying the same `#<id>` across repos is ONE work item → one PR **per repo**, never one PR spanning repos and never several PRs in one repo for the same id.

### 1. Preflight

- Working tree clean? Uncommitted changes are either committed (per the project's subject convention) or explicitly left out — ask, don't guess.
- Commit subjects on the branch follow the configured pattern (e.g. `#<id> (<SCOPE>) <description>`). Fix outliers only with user approval (rewriting pushed history needs explicit consent).
- **Green on the exact tree you publish.** The review gate (step 2) runs the suite; if anything changes after it — a blocker fix, a squash, a rebase — re-run and quote the summary line before pushing. A green run on an earlier tree proves nothing about this one. Red → stop; the flow resumes after green.
- **Confirm the base.** The configured target branch is the default, but verify it's what this branch actually forked from (`git merge-base`, the branch's upstream, or the work item). Mismatch → ask "this branch split from `<X>` — target `<X>` or the configured `<Y>`?" A PR against the wrong base reviews commits that aren't yours and is expensive to redo.

### 2. Review gate — before publishing, not after

- Run the `code-review` skill in branch scope on the branch if installed (grouped by task id); otherwise perform a focused diff review of the branch against its **configured target** (`git diff <targetBranch>...HEAD`) — a diff against the wrong base reviews commits that aren't yours or misses ones that are.
- If SQL files changed, also run `sql-review` if installed.
- If the branch renames a symbol, changes a default or signature, or touches shared state (schema, config, flags, events), also run `regression-hunt` if installed; a `confirmed` regression is a blocking finding.
- **Blocking findings stop the flow** — but "blocker" carries a burden of proof: name the concrete failure scenario in one sentence ("user does X → wrong Y"). No scenario → it's a suggestion, and suggestions don't stop the flow. Each real blocker is either fixed, or explicitly waived by the user — a waiver is recorded in the PR description ("Known issue: X — accepted because Y"). Zero findings is a valid outcome; proceed.
- ❌ "Reviewed — looks good" with no findings listed and no diff quoted → that's recognition, not review.
- ✅ "branch review: 0 blocking, 2 suggestions (deferred, listed in PR body). Proceeding."

### 3. Publish

`git push -u origin <branch>` per repo — **only with user approval; never push unasked.** One approval can cover all repos of the same work item if the user says so. A rejected push means the remote moved: fetch and investigate; **never force-push** on your own initiative — only on the user's explicit request, and never to a shared branch.

### 4. Create — provider detected from the remote URL

Detect from `git remote get-url origin` output you ran this session — the remote decides, not the tooling installed (`gh` being on PATH doesn't make this a GitHub repo).

- **Azure DevOps** (`dev.azure.com` / `visualstudio.com`): follow the `azure-devops` skill — house defaults from `.claude/azure-devops.json` (target branch, title pattern, required reviewers, auto-complete, work-item link).
- **GitHub** (`github.com`): follow the [`github`](../github/SKILL.md) skill — house defaults from `.claude/github.json` (target branch, title pattern, reviewers, auto-merge, issue link via closing keyword).
- PR description template — intent, not a diff restatement:
  1. **What & why** — one paragraph, the user-visible outcome.
  2. **Work item** — id + link.
  3. **Testing done** — only observed results, quoted ("integration suite: 84 passed"). A check you didn't run is listed as `not run`, never omitted.
  4. **Deploy order / coupling** — for multi-repo: which PR merges/deploys first and why (e.g. DB schema before API, API before client).
  5. **Sibling PRs** — links to the other repos' PRs for this work item.
- Multi-repo sequencing: create all PRs first, then edit each description to add the sibling links (they don't exist until created).
- **When a push or create call fails:** read the full error, change exactly one thing it names, retry once. A second failure on the same call = stop and report the exact error — never retry verbatim, never move to the next repo as if it succeeded. A partial multi-repo state ("2 of 3 PRs created; repo X failed on: <quoted error>") is reported as exactly that, never rounded up to done.

### 5. Verify — a setting you didn't check is not set

Re-read each PR after creation: required reviewers actually marked required, work item actually linked, auto-complete actually on, target branch correct. Quote the verification. Then report a table: repo → PR URL → status.

## Examples

### Example 1: single-repo PR

**User:** "PR this"

**Claude:** anchors (id `#4711`, branch `feature/4711-rate-limits`, one repo), runs the review gate (0 blockers), asks approval to push, creates the PR with configured defaults, verifies reviewers + work-item link + auto-complete, reports the URL.

### Example 2: multi-repo work item

**User:** "publish the branches and create the PRs"

**Claude:** finds three repos with `#4711` commits, review-gates each, pushes all with one approval, creates three PRs, updates each body with the two sibling links and the deploy order (DB → API → client), verifies all three, reports a table of URLs.

### Example 3: review gate finds a blocker

**User:** "create a PR"

**Claude:** review gate flags a missing null check with a concrete failure scenario. Stops. Presents the finding: fix now, or waive? User says fix → applies the fix, re-runs the gate, then continues the flow.

## Anti-patterns

- ❌ Creating the PR first and reviewing after — the gate exists to keep unreviewed code out of reviewers' queues.
- ❌ Pushing or creating PRs without explicit approval for the push.
- ❌ One PR spanning multiple repos, or omitting configured reviewers / auto-complete / work-item link "to save time".
- ❌ Reporting "PR created with required reviewers" without re-reading the PR to confirm — creation calls can partially fail.
- ❌ Guessing the work item id from conversation memory — branch and commits are the source of truth; neither has it → ask.
- ❌ Calling a finding a blocker with no failure scenario attached — no scenario, no stop.
- ❌ Rounding a partial multi-repo result up to success — "2 of 3 created" is the honest report.
- ❌ PR bodies that narrate the diff file-by-file instead of stating intent, testing, and coupling.
- ✅ Review gate → approved push → per-repo PRs with verified house defaults → cross-referenced siblings → URL table.
