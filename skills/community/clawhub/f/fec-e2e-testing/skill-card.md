## Description: <br>
Guides developers through creating, maintaining, debugging, and reviewing Playwright or Cypress end-to-end tests for critical browser user journeys, CI reporting, flaky tests, visual regression, and payment or wallet scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to plan, implement, debug, and review real-browser E2E coverage for critical web application flows. It helps structure Playwright or Cypress tests, Page Object patterns, CI artifacts, visual regression checks, and safer handling of payment, wallet, and other high-risk scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: E2E examples for wallet, payment, or financial flows could be adapted to real accounts, production environments, or real funds. <br>
Mitigation: Use staging environments, mocks, seeded test accounts, and explicit production skips; keep real payments, private wallet keys, and production accounts out of E2E runs. <br>
Risk: CI screenshots, traces, videos, and reports can expose sensitive customer data or credentials if tests use realistic secrets or production data. <br>
Mitigation: Use sanitized fixtures and scoped test data, avoid secrets in browser-visible flows, and keep CI artifact retention narrow and deliberate. <br>
Risk: Flaky waits, random data, or order-dependent tests can create misleading E2E results. <br>
Mitigation: Prefer locator auto-waiting, network or visible-state assertions, repeatable seed data, teardown cleanup, trace review, and issue-linked isolation for flaky cases. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bovinphang/fec-e2e-testing) <br>
- [Playwright / Cypress E2E Patterns](references/playwright-patterns.md) <br>
- [E2E CI and Reporting](references/e2e-ci-reporting.md) <br>
- [E2E Special Scenarios](references/e2e-special-scenarios.md) <br>
- [E2E Visual Regression Testing](references/e2e-visual-regression.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with TypeScript, YAML, shell command, and report-template examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes testing workflow guidance, CI artifact recommendations, flaky-test debugging commands, and safer patterns for wallet, payment, and visual-regression scenarios.] <br>

## Skill Version(s): <br>
2.7.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
