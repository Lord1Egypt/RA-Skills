---
name: e2e-verify
description: >-
    Verify a change end-to-end in a real browser, routed by one question — who needs this check to run again? Ephemeral checks run via Expect (millionco/expect) or browser-use (AI agent driving headless Chromium — references/browser-use.md) when installed, else Claude driving the browser directly; regression-critical flows (auth, money, signup, checkout, deletion) get durable Playwright tests under write-tests discipline. Evidence rule either way — an AI-walked flow yields "no issues found in the paths walked" with observations quoted, never "e2e passes". Safety gate: never production, never real user cookies. Use this skill whenever the user says "verify this in the browser", "test it end to end", "test my web app", "e2e test this", "write playwright tests", "run expect", "run browser-use", "smoke test the UI", or "/e2e-verify" — even if they don't name the skill. Not for native mobile (maestro-mobile-test), unit/integration authoring (write-tests), or debugging a failing e2e test (diagnose).
---

# E2E Verify

Close the loop between "the diff looks right" and "a user can actually do the thing." Every route through this skill drives a real browser against running code; what differs is durability. The routing question is not which tool — it's **who needs this check to run again?** Nobody (one-off confidence in this change) → ephemeral. CI, forever (a behavior whose silent regression is expensive) → durable Playwright test in the repo. Often both: smoke now, durable test as the deliverable.

## When to use this skill

- The user says "verify this in the browser", "test it end to end", "test my web app", "verify the web UI", "e2e test this", "write playwright tests", "run expect", "run browser-use", "smoke test the UI", "does it actually work", "/e2e-verify".
- A feature from `task-executor` is done and needs proof beyond unit tests; `code-review` or `ship-it` wants runtime evidence.

Do **not** auto-trigger for native mobile apps (`maestro-mobile-test`), unit/integration authoring (`write-tests`), debugging an already-failing e2e test (`diagnose`), or general browser automation that isn't testing.

## The safety gate — before any browser opens

1. **Confirm the target URL is local or staging.** State it in the report. If the only available URL is production, stop and ask — never assume.
2. **No real user cookies or accounts.** Expect extracts system-browser cookies by default — pass `--no-cookies` unless the user explicitly opts in for a non-prod target. Flows that mutate data (payments, deletion, invites that email people) run only against seeded/throwaway data; if none exists, that's a blocker to surface, not a reason to "carefully" test on real data.
3. **Confirm something is listening.** Load the base URL and observe a real response before walking any flow. If nothing answers, start the dev server the repo's own way (its dev script / launch config) and confirm it's up — a dead port produces "every flow is broken", which is a false report about the app. Distinguish "the app failed" from "the app wasn't running" in everything you report.

## Route the request

| Signal | Route |
|---|---|
| "Does my change work?", pre-merge confidence, exploratory | **A: Ephemeral** |
| The flow is money/auth/signup/checkout/data-loss, or user says "add e2e tests", or the same flow has now been manually re-verified twice | **B: Durable** |
| Feature just built and it's a critical flow | **A now, then B** — the smoke run's steps become the test's spec |

## Route A: ephemeral verification

Pick the engine by what's installed — the discipline is identical across engines:

1. **Expect** (`expect-cli` / `/expect` on PATH): run with an explicit `--url` (the confirmed non-prod target), `--no-cookies` by default, `--target` matching the change scope. Its report is input, not verdict — extract which flows its subagents walked and what they observed.
2. **browser-use** (`python -c "import browser_use"` succeeds, or the user names it): an AI agent drives headless Chromium from natural-language task scripts — strongest for exploratory walking where the agent *finds* broken flows. Setup, task-writing guidance, structured-output schemas, red-proof discipline, and troubleshooting live in [references/browser-use.md](references/browser-use.md); one-time install via `scripts/browser-use/setup.sh`. Its report is input, not verdict — same claim shape as every engine.
3. **Claude drives the browser** (Playwright MCP, claude-in-chrome, preview tools — whatever this session has): enumerate the user-visible flows the diff touches (from the diff, not imagination), walk each one as a user would, and at each step verify via DOM/accessibility state for text and behavior (screenshots only for layout questions). After each flow: check the browser console for errors and the network log for failed requests — a page that looks right while logging exceptions is a finding, not a pass.
4. **None available — offer the install, never dead-end and never install silently.** One `AskUserQuestion` with the real options: (a) install Playwright locally (`npm init playwright@latest` — standard tooling, Claude then drives it), (b) install browser-use (`scripts/browser-use/setup.sh` — creates a local venv, needs an LLM API key), (c) install Expect (state plainly what its init does: runs a third-party script that adds a skill + hooks into the agent — third-party init scripts require an explicit yes), or (d) skip. Only if the user skips, report `e2e: not verified — no browser tooling` and stop. Never substitute code-reading for observation, and never report "verified" after a skipped install.

**Reporting rule (the core of the skill):** an AI-simulated user is a fallible verifier — same epistemics as any model output. The honest claim shape:
- ❌ "Ran Expect — e2e tests pass ✅"
- ✅ "Walked 3 flows against localhost:3000 (seeded account): login → dashboard (observed: redirect + username rendered), create invoice (observed: row appears, total 107.10, console clean), delete invoice (observed: 409 on double-delete — **finding**, quoted below). Not walked: mobile viewport, payment path (no test Stripe key). "
Every flow walked is enumerated; every "works" is backed by a named observation; everything not walked is listed. Zero findings across enumerated flows is a valid outcome.

## Route B: durable Playwright tests

`write-tests` discipline applied to the browser — plus the e2e-specific rules that keep suites from rotting:

1. **Match the repo first.** Grep for `playwright.config`, `cypress.config`, an `e2e/` dir. Extend the existing setup and imitate its strongest test; only scaffold fresh (`npm init playwright@latest`) if nothing exists, and say so.
2. **Ration e2e tests by risk.** Each one is 100× a unit test's cost in time and flake surface. Test through the UI only what is *about* the flow: the user journey, the wiring, the redirect. Business-logic variations (12 discount cases) belong in unit tests — write the one journey here and note the push-down. A handful of journeys is a suite; fifty is a liability.
3. **Selectors users would recognize:** `getByRole`, `getByLabel`, `getByTestId` — never CSS chains or `nth-child`, which weld the test to today's DOM.
   - ❌ `page.locator('div.card > button:nth-child(2)')` — breaks on any restyle, catches nothing a user cares about.
   - ✅ `page.getByRole('button', { name: 'Submit order' })` — breaks only when the user's world breaks.
4. **No sleeps.** Web-first assertions (`await expect(locator).toBeVisible()`) auto-wait; `waitForTimeout` is flake by construction. If a step genuinely needs polling, poll a condition.
5. **Independent tests, cheap setup.** Each test arranges its own world — seed state via API calls or fixtures, not by clicking through the UI (UI setup means test 3 fails because of the flow test 1 owns). Auth via a `storageState` fixture created once, not a login walk per test.
6. **Prove red-capable** (non-negotiable, per `write-tests`): break the behavior or the assertion target, run, quote the red; revert, quote the green. An e2e test never seen red is the most expensive decoration there is.
7. **Run the suite and quote the summary line.** A result you didn't observe is `not run`, never "passed".

## Examples

### Example 1: post-feature smoke → durable

**User:** "I just finished the invoice feature — verify it end to end."

**Claude:** Confirms target (localhost:3000, seeded user), no Expect installed → drives the browser: walks create/edit/void flows from the diff's touched routes, quotes observations per flow, catches a console 500 on void (finding). After the fix: "void is a money path — want the durable test?" → writes one Playwright journey extending the existing `e2e/` config, `getByRole` selectors, proves it red against the reverted fix, quotes both runs.

### Example 2: "run expect"

**User:** "Run expect on my branch."

**Claude:** Confirms the dev URL, runs `expect --target branch --url http://localhost:3000 --no-cookies`, then translates its output into the claim shape: flows walked + observations + findings + not-walked list — and flags that the checkout flow wasn't in Expect's generated plan despite being in the diff, walking it manually to close the gap.

## Anti-patterns

- ❌ Reporting an Expect or browser-walk green as "e2e tests pass" — the verifier is a model; the claim is "no issues found in the paths walked", paths listed.
- ❌ Trusting the generated test plan to cover the diff — diff-to-plan is lossy; check the plan against the diff's touched routes and walk what it missed.
- ❌ Verifying against production, or letting Expect's default cookie extraction ride along silently.
- ❌ Visual-only verification — a rendered page with console exceptions and failed XHRs is a finding.
- ❌ Writing an e2e test for every case a unit test could cover — ration by journey, push logic down the pyramid.
- ❌ Shipping an e2e test never seen red, or "fixing" a flaky one by adding `waitForTimeout`.
- ❌ Scaffolding a fresh Playwright setup when the repo already has one (or has Cypress — extend what's there).
- ❌ Running Expect's init script (or any third-party installer) without an explicit yes — offering the install is required, running it unasked is not consent.
- ✅ Route by who-needs-it-again → safety gate → observations quoted per flow → durable tests proven red-capable → not-walked list always present.

## Notes

- Engines are swappable; the discipline isn't. If Expect changes licensing (FSL, hosted version coming) or a better ephemeral tool appears, only Route A's engine list changes.
- Manual re-verification of the same flow twice is the signal to graduate it to Route B — the third time is a test.
- Apply `think-like-fable`: flows chosen by risk, every "works" re-derived by observation, the not-walked list is the labeled-assumption discipline, and the report leads with findings, not the tour.
