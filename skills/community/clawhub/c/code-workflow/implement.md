# Implement (Step 4 — TDD by Default)

After plan approval and branch creation (Steps 0-3 in [steps.md](./steps.md)), implement the changes.

## Plan Acceptance Gate (MANDATORY — before any Edit/Write/commit)

Before the first Edit/Write/commit in Step 4, verify all 4 items:

1. **Plan exists**: a `plan-*.md` artifact is present in the configured `output-dir` (see [SKILL.md](./SKILL.md) Configuration — default `docs/generated/`)
2. **Plan posted (when linked to a GitHub issue/PR)**: the plan body has been posted via `github-flow/plan-to-issue` and the comment URL is recorded
3. **Explicit user approval recorded**: the user verbally, via AskUserQuestion option, or via a signed-off plan acceptance checklist signaled "approve / proceed / implement". A short prompt such as "keep going" / "continue task" / "next" / "go" does **not** satisfy this item alone — these are ambiguous verbs whose intent could be plan-acceptance, implement-entry, PR-creation, or resuming a pending task. An AskUserQuestion enumerating those branches is required first
4. **Plan acceptance checklist (when present in plan body)**: every `Plan acceptance checklist` / `Step 3 review items` line in the plan body is reviewed with the user

If any of 1-4 is unmet, **STOP**. Do not Edit/Write/commit. Issue an AskUserQuestion presenting the plan acceptance checklist items to the user. Only on explicit approval (item 3) may Step 4 proceed.

| # | Don't | Do |
|---|-------|-----|
| 1 | Interpret a short prompt ("keep going" / "continue task" / "next" / "go") as implement approval | Run the 4-item gate above. Short prompts trigger ambiguous-verb handling — AskUserQuestion is required |
| 2 | Treat a task description that lists "N. implement" as user approval | task description = work memo, not approval. Item 3 requires an explicit user signal |
| 3 | Plan posted to issue/PR comment + checklist unchecked → implement entry | Posted is not the same as accepted. AskUserQuestion presenting the checklist before Step 4 |
| 4 | Re-enter Step 4 across session resumes without re-checking items 1-4 | At each session entry the gate runs again — the prior session's task description alone does not carry approval forward |

**Violation case (2026-05-26)**: A plan for Skills-7-Phase3 was posted to issue #7 comment 4534769660 on 2026-05-25 (Phase 3 plan posted + plan acceptance checklist 0/6). The next-day session interpreted a short "continue task" prompt as implement approval, skipped the acceptance gate, and proceeded to publish.yml + verify-phase3.sh implementation, commit, push, and `github-flow pr` invocation. The user surfaced it as: "the plan is already posted — aren't you checking it?".

## Skill Invocation (Mandatory)

**Implementation skill invocation mandatory** — Direct Agent dispatch prohibited:
- `Skill("superpowers:subagent-driven-development")` or `Skill("superpowers:test-driven-development")`
- Manually substituting the skill because "you already know it" is a procedural violation

Once the plan is approved, implement using the **tdd skill's cycle topic** (Red→Green→Refactor).
After implementation, run tests using the **tdd skill's run topic** and report results.

## Test Level Selection (Mandatory judgment before starting TDD)

| Change Type | Test Level | Reason |
|-----------|-----------|------|
| Pure logic (utils, parsing, transformation) | Unit test | Mocks are sufficient |
| API Route branching/authentication | Integration test | Verify headers/cookies/redirects with actual HTTP requests |
| **External system integration** (Authentik, OAuth) | **Integration + E2E** | The actual request format of external systems (Basic Auth, etc.) cannot be reproduced with unit mocks |
| UI behavior/flow | E2E (Playwright) | Verify browser redirect chains |

**External integration bugs cannot be caught by unit tests** — Whether Authentik requests a token via Basic Auth or POST body can only be known by actually calling it. Integration tests must **reproduce the actual authentication method used by the external system**.

**E2E = Test Code (Not manual verification)** — "E2E" means writing Playwright test cases in `e2e/*.spec.ts`. "Manual verification with Playwright MCP after deployment" is not an E2E test. In TDD for external system integration changes, E2E test code **must be included in the implementation PR**.

## TDD Red-Green-Refactor

**TDD Red commit mandatory** — The test (unit + integration + E2E) must be **committed first without the implementation code** to record a failure (Red). Then commit the implementation code to pass (Green). Committing the test and implementation at the same time is not TDD.

- **Red commit failure verification mandatory**: After a Red commit, you must run `pnpm --filter <app> test` to **verify the failure**. If execution is not possible (environmental issues), verify in CI, but do not proceed to Green without confirming the failure
- **Red commit scope**: Only test files are included. If implementation code (`route.ts`, `lib/*.ts`, etc.) is included in the Red commit, it is a TDD violation

**TDD opt-out:** If the user specifies `--no-tdd`, implement without tests.

## Build & Commit

**Monorepo build verification**: In monorepo projects, run `pnpm build` (full build) before committing — not just `tsc --noEmit` on the changed package. Cross-package issues (e.g., Node.js-only imports leaking into browser bundles) are only caught by building downstream consumers. If full build is too slow, at minimum build the changed package + its direct dependents.

**Commit after implementation**: If build + tests pass, proceed to commit. Do not ask the user whether to commit. If a related existing commit exists, confirm whether to amend via `AskUserQuestion`.

**Commit Message Language (HARD STOP)**: Commit messages must match the primary language of the repository. Check the repository context (previous commits, issues, or README). If the repository uses a non-English primary language, write the commit message in that language. Defaulting to English in a non-English repository is a procedural violation.

## After Implementation

**After worktree/feature branch completion**: Once the commit is complete, call `Skill("superpowers:finishing-a-development-branch")` to review push + PR creation. If worked in a worktree, push+PR is the natural next step, so do not stop with "proceed when instructed".

**Pre-merge verification of Test Plan items requiring deployment**: If the Test Plan has deployment environment verification items, **pre-verify with the feature branch image on the verification/staging server**. CI-built images can be deployed directly to the verification server, allowing verification without merging. This resolves the deadlock of "verification required after deployment → merge required → cannot merge due to incomplete Test Plan".

## General Rules

- Mark completed tasks/steps as `[x]` in the project's task tracker
- Do not stop until all steps are complete
- Do not use `unknown` types
- Continuously run type checks during implementation (`pnpm typecheck` or `tsc --noEmit`)
- Do not introduce new type errors

## Mid-Implementation Discovery — Expand vs Split (HARD STOP)

When implementation reveals a new finding (a config refactor, a structural fix, a related bug, a missed dependency) that was not in the original plan:

1. **Default bias: expand the existing PR/issue** — see `github-flow/expand.md` for the decision matrix
2. **Do not defer** to "post-merge cleanup" or "follow-up PR" without justification — coherence loss
3. **Forbidden phrases that signal you should expand**:
   - "do X after PR merge"
   - "X in a follow-up PR"
   - "Stage A in this PR, Stage B as a separate issue"
   - "code only for now, cleanup later"
4. **If you decide to expand**, follow `github-flow/expand.md` Mandatory Procedure:
   - Commit to existing branch
   - Update PR/issue **title** with `gh pr edit --title` / `gh issue edit --title`
   - Update PR/issue **body** (Summary + Test Plan + Files to modify + Relates to)
   - Cross-link parent epic if scope shifted

Splitting is correct only when the new finding has **independent blast radius** (different reviewer, different release cadence, no shared verification). When in doubt, expand.

## When Going in the Wrong Direction

Do not patch over a bad approach — revert and restart with a narrower scope.

```bash
cmd /c git checkout -- <files>   # revert changes
```

Revise the plan and restart from step 3 (user review) in [steps.md](./steps.md).
