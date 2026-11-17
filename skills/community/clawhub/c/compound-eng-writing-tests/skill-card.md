## Description:

Provides stack-agnostic guidance for writing discriminating tests with meaningful assertions, avoiding common test anti-patterns, and resisting weak rationalizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliaal](https://clawhub.ai/user/iliaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when writing tests, adding coverage, or fixing failing tests across languages and frameworks. It helps them select cases that prove observable behavior and catch plausible regressions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup guidance could lead to loss of database or volume data.

Mitigation: Review cleanup steps before acting, and run them only against isolated, disposable databases or volumes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iliaal/skills/compound-eng-writing-tests)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown guidance, test code, and test-running commands as appropriate to the request.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are tailored to the repository's test runner, contracts, and framework; the skill is not tied to one language.]

## Skill Version(s):

5.1.6 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
