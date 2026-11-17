## Description:

Comprehensive code review assistant that analyzes code quality, identifies bugs, suggests improvements, and ensures adherence to best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoshamin](https://clawhub.ai/user/guoshamin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review pull requests, audit code quality, find security and performance issues, and produce actionable review feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill allows Bash during code review, so command use may affect the workspace if an agent chooses to run commands.

Mitigation: Apply normal workspace command safeguards and user oversight, and review proposed commands before execution.

Risk: Code review feedback may be incomplete or misleading if treated as a substitute for human review.

Mitigation: Use the skill to support review, then verify findings, suggested fixes, and risk severity before acting on them.

## Reference(s):

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Clean Code Principles](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [Google Style Guides](https://google.github.io/styleguide/)
- [Effective Code Review](https://google.github.io/eng-practices/review/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown review feedback with code examples and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prioritized findings, file and line references, suggested fixes, and test coverage notes.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
