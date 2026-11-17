## Description:

Provides a standardized code review workflow that checks code quality, security, maintainability, and performance, then produces a structured review report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bobbhchen](https://clawhub.ai/user/bobbhchen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review files, commits, or pull request diffs for technical quality, security concerns, maintainability, and performance issues. It returns specific findings with locations, severity, and suggested fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect code, commits, or pull request diffs that contain sensitive material.

Mitigation: Only point the agent at repositories or diffs whose contents are appropriate for the active agent environment.

Risk: Review findings and suggested fixes may be incomplete or incorrect.

Mitigation: Have a qualified reviewer validate findings and scan proposed changes before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bobbhchen/skills/enterprise-code-review)
- [ClawHub publisher profile](https://clawhub.ai/user/bobbhchen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown structured code review report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes review target, review date, overall rating, issue table, strengths, and summary recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
