---
name: fec-testing-strategy
description: Use when planning or reviewing a frontend testing strategy, selecting the right test layer by risk, mapping coverage across static checks, unit tests, component tests, integration tests, E2E, Storybook/visual regression, a11y, security, performance, or CI gates. Do not use to write individual component/E2E tests or merely run existing validation commands; Chinese triggers include test strategy, test layering, test plan, coverage matrix.
---

# Front-end testing strategy

## Purpose

Choose your testing approach by “closeness to code/level of risk coverage” to avoid cramming all risks into component tests or E2E.

## Procedure

1. Identify the type of change: pure logic, UI components, cross-module processes, browser capabilities, visual stability, dedicated quality risks, or release gates.
2. Establish a test level matrix, at least distinguish:
   - Static checking: TypeScript, ESLint, format, dependency security, build.
   - Unit testing: utils, hooks/composables, state logic, schema, pure functions.
   - Component testing: props/emits, user interaction, loading/error/empty, mock boundaries.
   - Lightweight integration testing: form + API mock + routing/Store/Provider context.
   - E2E: real browser, cross-page key journeys, authentication, payments, permissions, CI artifacts.
   - Visual/interactive documentation: Storybook interaction, Chromatic, visual regression baseline.
   - Special quality: a11y, security, performance, compatibility.
3. Allocate coverage by risk: high-frequency core paths prioritize E2E, complex component status prioritizes component testing, pure logic prioritizes unit testing, and lightweight integration testing is used for cross-provider collaboration.
4. Use the testing pyramid to control maintenance costs:
   - The closer to pure logic, the more tests, the faster, and the more stable it is.
   - E2E only covers key user journeys and real browser risks, not every branch.
   - Vision, a11y, safety and performance belong to dedicated quality layers and are not included in ordinary component tests.
5. Check whether commands, test frameworks, directory conventions, and CI gates already exist; use the current status of the project and do not introduce unnecessary tools to the policy document.
6. Plan failure evidence: Each high-risk item should describe how to locate it when it fails, such as assertions, screenshots, traces, coverage, logs, or reports.
7. Design test data and mock strategies: share fixtures to express business scenarios, and the test data builder only encapsulates noise fields to avoid handwriting random objects for each test.
8. Manage flaky risks: Mark time, network, animation, nonce, concurrency, and external services as sources of instability, and specify isolation, retries, and evidence artifacts.
9. Output the minimum executable test plan: what is covered by each layer, what is not covered, priority, recommended commands and responsibility skills.

## Constraints

- Don't write the test strategy as a general "write more tests"; each suggestion must correspond to a specific risk.
- All projects are not required to complete the complete testing pyramid; they are tailored according to business risks and team maintenance capabilities.
- Do not consider E2E as a replacement for unit/component testing; do not consider component testing as a guarantee of true browser compatibility.
- Do not force the introduction of new frameworks for small changes; give priority to reusing existing tools and scripts in the warehouse.
- Do not pursue coverage figures without risk explanation; coverage can only assist judgment and cannot replace scene coverage.
- Do not include random fixtures, shared global state, or tests that depend on execution order into trunk gates.

## Expected Output

Output test layering recommendations, mapping of risks to test layers, priorities, recommended commands, the scope of test files that need to be added or adjusted, and the specific skills or agents that need to be clearly diverted.
