---
name: gh-pr-review-loop
description: Drive a GitHub pull request through an iterative review-and-fix loop. Use when Codex needs to create a PR if none exists for the current branch, inspect review comments, decide whether each comment is valid, implement fixes, maintain the branch in the history shape the user requested such as a single amended commit on top of the latest remote `main`, push the branch, resolve fixed review threads, watch GitHub Actions, and keep polling until an automated reviewer gives a final thumbs-up reaction or the user explicitly changes the stop condition.
metadata: {"openclaw":{"requires":{"bins":["git"],"anyBins":["gh"],"env":["GITHUB_TOKEN"]},"primaryEnv":"GITHUB_TOKEN","env":[{"name":"GITHUB_TOKEN","description":"Optional GitHub token for gh/git when host GitHub MCP or existing git credentials are not used. Scope it to the target repository and branch where possible.","required":false,"sensitive":true}]},"clawdbot":{"requires":{"bins":["git"],"anyBins":["gh"],"env":["GITHUB_TOKEN"]},"primaryEnv":"GITHUB_TOKEN"}}
---

# GitHub PR Review Loop

## Goal

Take ownership of the full post-PR loop. Create the PR if it does not exist yet, then keep iterating until the stop condition is met instead of stopping after a single fix or a single green CI run.

## Access And Safety

- Use only GitHub access already provided by the host environment, such as the configured `github` MCP server, `gh` CLI auth, or the local git credential helper. Do not ask the user to paste tokens into chat, and do not read secret files.
- Before any edit, push, PR mutation, or review-thread resolution, verify that the repository, PR, active branch, and intended history strategy match the user's request.
- Treat missing GitHub permissions, missing git remote auth, or an ambiguous target repository/branch as a real blocker and report it instead of guessing.
- Limit history rewrites and force pushes to the active PR head branch. Never force-push a default, base, protected, or unrelated branch.
- Only use this skill for explicit PR review-loop work, such as handling review comments, keeping a PR branch green, or waiting for reviewer approval.

## Start

- Identify the repository, PR number, active branch, and any user constraints before editing anything.
- Check whether a PR already exists for the current branch. If not, create one before entering the review loop.
- Check whether the user wants a single commit, `--amend`, separate commits, rebasing onto latest `main`, or a waiting window such as "poll every 10 minutes".
- If the user says the branch must stay as one squashed commit, interpret that strictly: keep exactly one commit on top of the current remote base, use `git commit --amend --no-edit` for follow-up fixes, and avoid creating extra local commits unless you are about to squash them away immediately.
- If the user says the branch must stay based on the latest `main`, treat `origin/main` as the source of truth. Fetch it before each history rewrite that will be pushed, then rebase or rebuild the branch so the published head still sits on top of the latest remote `main`.
- Assume automated review is triggered by the repository itself unless the user explicitly says to summon it. Do not post `@codex review` or similar reviewer-ping comments by default.
- Check the current git state before rewriting history. Do not overwrite unrelated work.
- Prefer non-interactive git commands. Use `--force-with-lease` when rewriting published history.
- Default to persistence only after the target repo, PR, branch, and history strategy are clear. Once the loop starts, do not stop midstream to ask whether to continue watching for reviews unless you hit a real blocker that cannot be resolved from local or remote context.

## Source Of Truth

Do not rely on one surface only. Review state is usually split across multiple places.

- Use GitHub review threads as the primary source for unresolved inline comments.
- Use PR conversation comments and review summaries to catch top-level bot reviews.
- Use PR reactions to detect automated reviewer status markers such as `eyes` or final `+1`.
- Use `gh pr checks` and `gh run watch` for required CI state.

If review threads say everything is resolved but the bot keeps commenting, re-check both the review timeline and reactions. Inline-only polling is not enough.

## Work Loop

1. Find or create the PR for the current branch.
2. Fetch current review state, unresolved threads, conversation comments, reactions, and CI status.
3. Pick the next actionable comment and inspect the exact file and code path before changing anything.
4. Decide whether the comment is a real bug, a partial truth that needs a broader hardening pass, or a false alarm.
5. Implement the fix and add regression tests when behavior changes.
6. Run targeted validation first, then the broader checks required by the repository or the user.
7. Update git history in the form the user asked for.
8. Push the branch.
9. Resolve the review thread only after the fix is actually on the remote branch.
10. Watch CI until the latest required run finishes.
11. Wait and poll again for new feedback until the stop condition is met.

## Fixing Review Comments

- Read the exact comment text and the cited file/line range. Do not infer a narrower issue than the reviewer actually reported.
- When multiple comments share the same root cause, prefer a single stronger fix over a sequence of tiny patches.
- If a comment looks questionable, verify it against the current code and tests before dismissing it.
- When the user asked for review handling, do the implementation work directly instead of only summarizing a plan.

## Validation

- Start with the smallest test slice that proves the fix.
- Run lint and type checks for the edited scope.
- Run the larger suite required by repo policy when practical.
- If CI has known flakes, confirm they are the same flaky failures before rerunning them.
- When reporting status, mention the concrete failing or passing check name and run id if relevant.

## Git And PR Updates

- Respect the user's history preference.
- If there is no PR for the current branch, create one instead of waiting for the user to ask.
- If the user wants one commit, keep amending that single commit.
- If the user wants a clean branch based on latest remote `main`, rebase or rebuild onto `origin/main` before the final push.
- If you discover the branch is not based on the latest remote base branch, immediately fetch and rebase onto that latest remote branch before continuing the PR loop.
- If the user wants both, enforce both on every iteration: fetch `origin/main`, rewrite the branch onto that tip, keep the branch as a single commit, then push with `--force-with-lease`.
- When a temporary commit is unavoidable during local repair work, squash it back into the single published commit before pushing. Do not leave multiple commits on the branch between review-loop iterations.
- Push after local validation, then re-check the PR state from the remote, not from local assumptions.
- Resolve threads that are fixed. Leave unresolved anything that still needs proof or follow-up.
- Do not ping or `@` the reviewer unless the user explicitly asks for that. This includes automated reviewers such as `@codex`.

## Waiting And Polling

- Treat `eyes` from an automated reviewer as "still processing", not done.
- Assume the automated reviewer will start on its own when the repository is configured that way; do not try to kick it manually unless the user explicitly asks.
- Treat a final `+1` or thumbs-up reaction from the automated reviewer as the default completion signal for this skill unless the user explicitly changes the stop condition.
- If the user asked for a waiting window, keep polling on that cadence instead of stopping after one green pass.
- While waiting for comments, also make sure the latest CI run stays green.
- Do not stop after green CI, resolved threads, or a quiet PR if the automated reviewer has not yet produced its final thumbs-up reaction.
- Do not pause mid-loop to ask the user whether to keep monitoring. Keep polling until the stop condition is met or you hit a real blocker such as missing permissions, missing GitHub access, or a reviewer system that is unavailable.

## Stop Condition

Stop only when the requested completion condition is satisfied. Default completion criteria for this skill are:

- No unresolved actionable review threads remain.
- The latest required CI checks are passing.
- The automated reviewer has stopped producing new feedback.
- The automated reviewer has added a final thumbs-up reaction.

Do not treat "no new comments yet" as completion. Do not stop merely to ask whether to continue waiting. Only stop early if the user explicitly changes the stop condition or a hard blocker prevents further progress.

## Useful Commands

```powershell
git fetch origin main
gh pr checks <pr-number> --repo <owner/repo>
gh run watch <run-id> --repo <owner/repo> --exit-status --interval 30
gh run rerun <run-id> --repo <owner/repo>
git commit --amend --no-edit
git push --force-with-lease
```

## Reporting Back

- State what was fixed, what was validated, and what the current PR/CI/review state is.
- Include exact PR numbers, run ids, and commit SHAs when they matter.
- If you are still in the waiting loop, say that explicitly instead of sounding finished.
- During the loop, give status updates without asking whether to continue unless a real blocker requires user intervention.
