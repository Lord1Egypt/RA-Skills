## Description:

Automatically analyze and improve code for performance, readability, security, and best practices in JavaScript, Python, Go, Rust, and Java.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fxm1618](https://clawhub.ai/user/fxm1618)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to ask an agent to review source files, identify optimization opportunities, and produce refactoring or improvement suggestions for supported programming languages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly tells agents to automatically modify code without clear confirmation or scope limits.

Mitigation: Ask for suggestion-only review or a diff before applying changes, especially for authentication, security, infrastructure, or production code.

Risk: Optimization or refactoring changes may alter behavior while trying to improve performance, readability, security, or best practices.

Mitigation: Review generated changes and run the relevant tests, linters, and security checks before merging or deploying the modified code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fxm1618/skills/ai-code-optimizer)

## Skill Output:

**Output Type(s):** [Code, Markdown, Guidance]

**Output Format:** [Markdown with code snippets, suggested changes, and before/after comparisons]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or apply source-code edits when the user requests optimization.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
