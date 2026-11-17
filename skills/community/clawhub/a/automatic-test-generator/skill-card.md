## Description:

Automatically generate unit tests from functions with comprehensive coverage and edge cases

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelatamuk](https://clawhub.ai/user/michaelatamuk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate and refine unit tests for existing functions, classes, and modules across common testing frameworks. It is intended to accelerate coverage work while keeping generated tests subject to human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated tests may assert behavior the implementation does not actually provide, such as resilience or fallback semantics.

Mitigation: Review generated tests against the source behavior, adjust incorrect assertions, and run the tests before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/michaelatamuk/skills/automatic-test-generator)
- [Jest documentation](https://jestjs.io)
- [Vitest documentation](https://vitest.dev)
- [Pytest documentation](https://docs.pytest.org)
- [Testing Library guiding principles](https://testing-library.com/docs/guiding-principles/)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with code blocks and framework-specific test examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated tests should be reviewed, customized, and run before being relied on.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
