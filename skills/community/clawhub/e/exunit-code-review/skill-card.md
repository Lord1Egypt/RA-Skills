## Description:

Reviews ExUnit test code for proper patterns, boundary mocking with Mox, and test adapter usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when reviewing Elixir ExUnit tests, test helpers, Mox boundaries, and test-adapter configuration for practical issues and false-positive-resistant findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The full intended workflow references a separate review-verification protocol that is not included in this package.

Mitigation: Make that protocol available to the reviewing agent or require equivalent full-block and usage verification before accepting findings.

Risk: Review guidance can still produce noisy or misleading findings if the evidence, false-positive, and cross-protocol gates are skipped.

Mitigation: Require each finding to cite concrete file lines and pass the skill's Valid Patterns and Context-Sensitive Rules before reporting it.

## Reference(s):

- [ExUnit Patterns](references/exunit-patterns.md)
- [Integration Tests](references/integration-tests.md)
- [Mox Boundaries](references/mox-boundaries.md)
- [Test Adapters](references/test-adapters.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review findings with file and line references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are intended to pass the skill's evidence, false-positive, and cross-protocol review gates before submission.]

## Skill Version(s):

1.2.1 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
