---
name: code-workflow
metadata:
  author: es6kr
  version: "0.1.2"
depends-on:
  - github-flow
  - tdd
  - web-browser
description: |
  4-stage code-change workflow: research → plan → user review → implement (TDD). Topics — steps (Step 0-3: resume + research + plan + review + branch), implement (Step 4: TDD + build + commit), pr (capture + PR with image/GIF/video). For issue implementation, tracked tasks, new features. TDD default (opt out --no-tdd). github-flow auto-companion on GitHub repos. Use when: "coding workflow", "research plan implement", "write plan", "plan md", "user review", "code plan", "code changes", "PR with screenshots", "pull request", "capture and PR".
---

# Coding Workflow

A **Research → Plan → User Review → Implement** 4-stage procedure for code change tasks.

## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `output-dir` | `docs/generated/` | Directory for research/plan files. Set per project (e.g., `.ralph/docs/generated/`) |

Set via project CLAUDE.md or skill invocation argument:

```text
/code-workflow --output-dir docs/generated/
```

Trivial tasks such as simple configuration changes or 1~2 line edits may skip this workflow.

## Topics

| Topic | Description | Guide |
|-------|-------------|-------|
| implement | Step 4: TDD cycle, test level selection, build & commit | [implement.md](./implement.md) |
| pr | Capture + PR creation with visual attachments | [pr.md](./pr.md) |
| steps | Steps 0-3: resume check, research, plan, user review, branch | [steps.md](./steps.md) |

## Topic Dependencies

```text
code-workflow (steps 0-4)
  ├─→ steps Step 0: GitHub repo detection → loads github-flow as default companion
  ├─→ steps Step 0: github-flow/dependencies (blockedBy precondition check on linked issue)
  ├─→ tdd/cycle (step 4: TDD implementation)
  ├─→ tdd/run (step 4: test execution after implementation)
  ├─→ github-flow/plan-to-issue (auto-trigger when task has linked issue number)
  ├─→ github-flow/dependencies (auto-trigger when plan frontmatter has `chain:`)
  ├─→ github-flow/pr (optional: create PR with visual attachments)
  │     └─→ web-browser (capture via Playwright)
  └─→ github-flow/merge (after PR ready: gates CI/Review/Test Plan/blockedBy)
```

- Steps 0-4 are always executed (unless trivial)
- **GitHub repo auto-load** (Step 0): When `git remote get-url origin` contains `github.com`, `github-flow` becomes the default companion — issue/PR/merge ops route through its topics. Non-GitHub remotes fall back to manual `gh`/`git`
- **blockedBy precondition** (Step 0): Linked issue's `blockedBy` is queried. OPEN predecessors → switch task or BLOCKED report
- `github-flow/plan-to-issue`: converts plans to GitHub issues. **Auto-trigger when the task has a linked issue number** (e.g., Issue #176). Manual trigger when user explicitly requests issue registration
- `github-flow/dependencies`: applies `chain:` frontmatter as native Issue Dependencies. **Auto-trigger when plan has `chain:` array**. Skipped for single-issue plans
- `github-flow/pr` (optional, **opt-in only**): creates PRs. Invoke ONLY when the user explicitly requests PR creation (e.g., "create PR", "open PR"). Never auto-trigger from Step 4 completion
- `github-flow/merge` (after PR ready): pre-merge gates include `blockedBy` open-predecessors check (see `dependencies.md` and `merge.md` step 3.5)
- `tdd` is applied by default in step 4. Opt-out with `--no-tdd`

## Quick Reference

### Steps (Research → Plan → Review → Branch)

1. **Step 0**: Resume check — read existing research/plan files before starting
2. **Step 1**: Research — deep codebase reading, write to `research-<N>-<slug>.md`
3. **Step 2**: Plan — detailed plan with 6 mandatory sections (including human review questions)
4. **Step 3**: User review — report BLOCKED, wait for approval, then create branch/worktree

See [steps.md](./steps.md).

### Implement (TDD)

- Select test level (unit/integration/E2E) based on change type
- TDD Red commit (test only) → Green commit (implementation) → Refactor
- Monorepo full build verification before commit
- After completion: **report only** — do NOT auto-trigger push or PR. `push` and `github-flow/pr` require **explicit user instruction** (e.g., "push", "create PR"). PR creation is publish to GitHub and cannot be silently undone; reporting completion does not authorize it (HARD STOP).

See [implement.md](./implement.md).

### PR (with Visual Evidence)

- Capture screenshots/GIF/video after implementation
- Attach to PR body (before/after comparison)
- Opt-out with `--no-capture`

See [pr.md](./pr.md).

## Applicability by Task Complexity

| Task Complexity | Scope |
|----------------|-------|
| trivial (1~2 line edits, config value changes) | Can be skipped — implement directly |
| moderate (3~10 files, logic changes) | Start from step 2 (plan) |
| complex (10+ files, new features, architecture changes) | Perform all steps from step 1 (research) |

**Cases where skipping is prohibited even if the line count is small (HARD STOP)**:
- **Regression issues** — when something that previously worked is broken. **Executable test code (no manual curl/ssh)** must be included in the Plan and the issue.
- **Primary Branch Integrity (HARD STOP)** — every working branch must be cut from the project's **latest primary branch (origin/master, origin/main, or origin/develop)**. `git fetch origin` and primary-branch confirmation are required before branch creation.
- **External system integration changes** (Authentik, OAuth, external APIs) — Plan + integration tests are mandatory regardless of line count.
- **Authentication/security-related changes** — Mandatory to specify test strategy (unit/integration/E2E level) in the plan.
- **proxy.ts/middleware branching changes** — Affects multiple cases. Mandatory to specify impact scope + GUARD comment strategy in the plan.
