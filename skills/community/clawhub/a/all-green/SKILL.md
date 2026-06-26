---
name: all-green
description: Publish local changes to a GitHub pull request and keep working the PR until review feedback is addressed and required checks are green. Use when the user invokes /all-green, asks to create/open a PR and then monitor it, wants Codex to combine yeet-style publishing with GitHub review-comment handling, or wants an existing PR watched and fixed until comments and CI are clear.
---

# /all-green

Run an end-to-end PR readiness loop: review the user's intended local changes before publication, show the pre-publish review output to the user for approval, fix only the approved findings, publish the changes, open a PR automatically, inspect review feedback and CI, implement fixes, validate locally, and repeat until the PR has no actionable unresolved feedback and required checks are green.

## Core Workflow

1. Establish scope.
   - If the user provides an existing PR, resolve it and skip publishing unless local changes must be pushed.
   - If the user wants current changes published, inspect `git status -sb` and the diff, confirm intended files when the worktree is mixed, and identify the exact pre-publish diff to review.
   - Prefer opening PRs (not draft PRs) unless the user explicitly asks for a draft.
2. Run the pre-publish review gate.
   - Before staging, committing, pushing, or opening a PR, run Codex `/review` behavior on the intended local diff. If the `$commit` skill is available, use its Step 1 code-review behavior as the review gate, but do not run its Devin Review or PR-comment loop before a PR exists.
   - Present the review findings to the user before making any fixes. Lead with concrete findings, severity, file/line references, and the recommended action for each item.
   - Pause for the user's decision after showing the review output. The user may approve all findings, approve selected findings, reject findings, ask questions, request more investigation, or choose to continue without pre-publish fixes.
   - Fix only the findings the user approves. Apply those fixes locally in small batches, then rerun the relevant review pass or targeted checks for the approved items.
   - If a finding is ambiguous, scope-expanding, or product-sensitive, explicitly mark it as needing a user decision instead of fixing it automatically.
   - If the user explicitly asks to skip the pre-publish review, record that and continue with publishing.
3. Publish the reviewed changes.
   - Use `$github:yeet` semantics: create or keep the branch, stage only intended files, commit, push, and open a PR automatically.
   - If the pre-publish review produced fixes, include those fixes in the intended publish scope and mention them in the commit/PR summary.
4. Capture the PR target.
   - Record repository, PR number, PR URL, base branch, head branch, and current head SHA.
   - Use GitHub connector tools where available for PR metadata and patch context.
   - Use `gh` for exact CI status, PR discovery, and thread-aware review state when needed.
5. Inspect feedback.
   - Apply `$github:gh-address-comments` behavior for review comments: fetch unresolved review threads with thread-aware GraphQL data, cluster actionable items, ignore resolved/outdated/informational comments, and separate ambiguous comments from direct code requests.
   - Include top-level PR comments only as supporting context unless they are clearly actionable.
6. Inspect checks.
   - Apply `$github:gh-fix-ci` behavior for failing GitHub Actions checks: read exact-head status, then fetch only relevant failed jobs/logs.
   - Treat required checks as the readiness bar. Do not wait on ignored/non-required informational jobs unless the user asks.
7. Fix locally.
   - Implement actionable review and CI fixes in small traceable batches.
   - Preserve unrelated user changes. Do not silently stage mixed worktrees.
   - If a comment needs an explanation instead of code, draft the response for the user unless they explicitly authorize posting.
8. Validate.
   - Run the most relevant local checks before pushing fixes.
   - For OpenClaw, obey repo instructions: run `pnpm docs:list` first when working in the repo, use changed gates such as `pnpm check:changed` for code/runtime/config changes, and use targeted tests when appropriate.
9. Push and re-check.
   - Push fixes only after the user has authorized the publish/monitor loop or has explicitly asked `/all-green` to operate autonomously on the PR.
   - Re-read the exact PR head SHA after pushing.
   - Re-check unresolved actionable review threads and required checks.
   - Continue until both are clear, or stop on a blocker that needs user judgment.

## Safety Rules

- Do not merge, mark ready for review, request reviewers, resolve review threads, dismiss reviews, close issues, label, retitle, or post GitHub comments unless the user explicitly asks.
- Do not open a new PR from local changes until the pre-publish review gate has run and the user has approved the next step, unless the user explicitly skips it.
- Do not silently fix pre-publish `/review` findings. Show the review output first and wait for the user's selection or approval before editing.
- Do not treat a flat PR comment list as complete review-thread state. Use thread-aware reads for unresolved inline review work.
- Do not repeatedly poll forever. Use bounded polling, summarize pending checks, and continue only while progress is likely.
- If CI failure requires secrets, paid services, release credentials, or remote-only infrastructure, report the blocker and ask before using elevated or remote workflows.
- If review requests conflict or would create a regression, pause and present the tradeoff.
- If the PR belongs to a repo with its own AGENTS.md or scoped instructions, read and follow them before editing.

## Completion Criteria

Finish with a concise status containing:

- PR URL and final head SHA checked.
- Pre-publish review status: passed, skipped by request, or reviewed by the user with selected fixes applied before publication.
- Review feedback status: no actionable unresolved threads, or a list of remaining blockers.
- Required check status: green, pending with reason, or failed with the next actionable error.
- Local validation run and result.
- Commits pushed, if any.
