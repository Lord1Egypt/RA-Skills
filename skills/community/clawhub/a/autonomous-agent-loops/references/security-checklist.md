# Security Checklist — Run Before Any Autonomous Loop

> **If you can't tick every box below, do not run the loop.** A failed audit is cheaper than a leaked secret or a bot-merged production deploy.

## Pre-Flight (Required)

- [ ] **Repository owner has given explicit consent** for unattended PR creation, CI retry, and (if enabled) auto-merge. Verbal "yeah, automate the boring stuff" is not enough. Document the consent.
- [ ] **Loop is scoped to a non-production branch.** `main`, `master`, and any release branch are off-limits unless a human is reviewing every merge.
- [ ] **Credentials are least-privileged.** GitHub fine-grained PAT scoped to one repo, no `repo:admin`, no org-level scopes. Rotate after the loop ends.
- [ ] **Budget cap is set.** `--max-cost $X` AND `--max-duration Yh` AND `--max-runs N`. All three, not just one.
- [ ] **Loop output directory is sandboxed.** No `~`, no `..`, no shared scratch dirs. Use a dedicated `.loop/<run-id>/` inside the repo.
- [ ] **Secrets are redacted from inputs.** Specs, error logs, and directory listings piped into `claude -p` must be scrubbed for API keys, tokens, customer data, and internal URLs.

## Runtime (Required)

- [ ] **Loop emits a heartbeat.** Every N iterations, write a timestamp + status to `LOOP_STATUS.md`. If the heartbeat stops, kill the loop.
- [ ] **CI failure budget is bounded.** `--ci-retry-max 3` is the default. After 3 failures, stop and alert a human.
- [ ] **Auto-merge is OFF by default.** If you turn it on, require `--require-manual-merge-approval` so each merge asks for confirmation.
- [ ] **Session files are gitignored.** Anything written to `~/.claude/sessions/` must not be committed or synced to a shared drive.

## Post-Run (Required)

- [ ] **Review every commit the loop created.** Even with all the safety flags above, an LLM can produce plausible-looking nonsense. `git log main..HEAD` and read the diffs.
- [ ] **Rotate any credentials the loop touched.** Belt and suspenders.
- [ ] **Archive the run log.** `LOOP_STATUS.md` + `SHARED_TASK_NOTES.md` go into a dated folder. Useful for postmortems.

## What This Checklist Does NOT Cover

This checklist is for *accidental* damage (cost overruns, merge mistakes, secret leaks). It does not address *adversarial* inputs — prompts designed to subvert the loop. For that, see `references/adversarial-inputs.md` (coming soon).