---
name: fec-e2e-testing
description: Use when creating, maintaining, debugging, or reviewing real-browser end-to-end tests with Playwright or Cypress, including Page Object models, CI artifacts, traces, flaky tests, cross-page visual regression, and critical user journeys such as login, payment, permissions, or CRUD. For layer planning or tests close to UI components, choose the matching testing workflow first; Chinese triggers include E2E, end-to-end testing, Playwright, Cypress.
---

# E2E Test Specification

## Purpose

Validate key user journeys with real browsers and uncover integration risks not covered by unit tests.

## Procedure

1. Clarify the key journeys: cross-page processes such as login, purchase, creation, search, permissions, payment, etc. are given priority; if you only choose the test level, do the test hierarchical planning first.
2. New projects will be given priority by Playwright; existing Cypress projects will continue to use Cypress and will not be migrated for the sake of migration.
3. Use Page Object or fixtures to encapsulate login, page locator and shared data, and avoid naked selectors in the spec.
4. Assert that the user can see the results, relying on Locator automatic waiting, network response or visible status, without using fixed sleep.
5. CI must upload HTML report, screenshots, trace or video; Flaky use cases must be isolated, reproduced, marked with sources and associated with issues.
6. When debugging fails, read the trace, console, network and screenshots first, and then change the test; do not misjudge real product defects as flaky.
7. Record the test environment, seed data and cleanup strategies for key browser capabilities, payment, permissions, uploads and real-time communication processes.
8. Test data must be repeatable: API seeds, database fixtures, test accounts or mock services are preferred; random data must have a unique prefix and be cleaned in teardown.

## Detailed reference

- Load [references/playwright-patterns.md](references/playwright-patterns.md) when you need directory structure, Page Object, spec organization, configuration, flaky debugging and production examples.
- Load [references/e2e-ci-reporting.md](references/e2e-ci-reporting.md) when you need CI examples and Markdown report templates.
- Load [references/e2e-special-scenarios.md](references/e2e-special-scenarios.md) when Web3/wallet flows or high-risk financial flows are required.
- When cross-page screenshots or visual regression configuration are required, load [references/e2e-visual-regression.md](references/e2e-visual-regression.md).

## Constraints

- Disable reliance on `sleep` / fixed `setTimeout` as primary synchronization means.
- Do not run real E2E in production environment.
- Avoid asserting component internal pixel-level styles in E2E; cross-page screenshots/visual regressions only cover key page states in the user journey.
- Failure must be able to be located by taking screenshots, traces or videos.
- Component internal contract testing is offloaded to component testing workflow.
- Do not bring unstable waits, random data, or dependent test order into CI.
- Do not treat the number of retries as flaky management; retries can only retain evidence, and the root cause still needs to be located.

## Expected Output

Key user journeys have stable E2E coverage, failed products can locate problems, and reports and traces in CI can be downloaded; flaky use cases include recurrence commands, isolation strategies, and follow-up issues.
