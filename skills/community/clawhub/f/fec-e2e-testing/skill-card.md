## Description:

Helps developers create, maintain, and debug real-browser end-to-end tests with Playwright or Cypress, including CI reporting and visual regression.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Developers and test engineers use this skill to build and debug repeatable browser tests for critical user journeys and collect actionable CI failure evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Test traces, reports, screenshots, videos, or visual baselines may expose sensitive data.

Mitigation: Run against staging or sanitized test data and review artifacts before sharing or committing them.

Risk: Tests covering payments or financial flows could execute real transactions.

Mitigation: Use staging or mocks and do not run real financial transactions in production.

## Reference(s):

- [Playwright and Cypress patterns](references/playwright-patterns.md)
- [E2E CI and reporting](references/e2e-ci-reporting.md)
- [Special E2E scenarios](references/e2e-special-scenarios.md)
- [Visual regression](references/e2e-visual-regression.md)
- [Project homepage (listed in package metadata)](https://github.com/bovinphang/frontend-craft)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with code and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include test reports and instructions for reviewing CI traces, screenshots, and videos.]

## Skill Version(s):

2.9.0 (source: release evidence, package.json, metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
