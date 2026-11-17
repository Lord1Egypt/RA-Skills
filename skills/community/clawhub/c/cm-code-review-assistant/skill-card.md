## Description:

AI-powered code review assistant that analyzes pull requests for bugs, security issues, performance problems, and style violations with actionable feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review pull requests, branches, staged changes, or patch files for correctness, security, performance, maintainability, style, and test coverage issues. It produces prioritized, line-specific findings with concrete fix suggestions and a summary of merge risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may inspect pull request contents, local diffs, file history, tests, issues, or prior reviews that are available through local GitHub, GitLab, or git credentials.

Mitigation: Install and use the skill only for repositories where that review context is appropriate for the agent to access.

Risk: Generated review findings and suggested fixes can be incorrect, incomplete, or misleading.

Mitigation: Treat output as reviewer assistance and have a qualified developer verify findings and proposed changes before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/cm-code-review-assistant)
- [Publisher profile](https://clawhub.ai/user/charlie-morrison)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown code review summary with severity-ranked findings, file and line references, and suggested fixes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review depth adapts to change size; large changes receive higher-level architectural review and spot checks of critical paths.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
