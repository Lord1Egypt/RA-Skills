## Description:

Helps agents design end-to-end test automation strategies and produce examples for modern web, API, visual, accessibility, mobile, performance, and CI testing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to plan E2E coverage and generate test automation scaffolds, configurations, examples, and CI patterns for application testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable examples can wipe database tables without strong safety checks.

Mitigation: Use the examples only in isolated test environments and add explicit guards before any database reset.

Risk: Test examples may expose or reuse production or shared credentials if copied without review.

Mitigation: Avoid production and shared credentials; use isolated test secrets and review configuration before reuse.

Risk: Example Cypress and CI settings can weaken browser security or supply-chain controls if copied directly.

Mitigation: Keep Cypress browser security enabled unless narrowly justified and pin CI actions, npx tools, and container images.

## Reference(s):

- [E2e Test Specialist examples](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/mtsatryan/skills/ah-e2e-test-specialist)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include complete test automation frameworks, cross-browser/device configurations, CI examples, reporting setup, performance checks, and accessibility testing guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
