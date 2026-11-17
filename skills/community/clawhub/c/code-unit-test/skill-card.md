## Description:

Compare branch diffs and produce simulated unit-test-style case tables for changed code paths without generating test code by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[extraskittles](https://clawhub.ai/user/extraskittles)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to compare a working branch with master or main, identify changed code paths, and produce concise simulated unit-test tables with inputs, dependency assumptions, execution paths, and expected results. It is intended for static unit-test analysis and does not create test files unless the user explicitly asks for code generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads repository status, diffs, and relevant changed source code to prepare its analysis.

Mitigation: Use it only in repositories where exposing changed code to the agent is acceptable.

Risk: Simulated unit-test tables may be incomplete or differ from runtime behavior when code depends on unknown data, external services, databases, cache, RPC, HTTP, or time.

Mitigation: Label uncertain results clearly, model external dependencies as assumptions, and run the smallest meaningful compile or test command when validation is useful.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/extraskittles/skills/code-unit-test)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown tables, usually in Chinese unless another language is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces static simulated test-case analysis; it may recommend focused validation commands when useful, but does not replace automated unit tests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
