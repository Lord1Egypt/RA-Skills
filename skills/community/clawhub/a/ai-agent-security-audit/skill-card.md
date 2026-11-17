## Description:

Performs a comprehensive security audit of AI agents, detecting vulnerabilities, assessing risks, and providing prioritized remediation and compliance reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engsathiago](https://clawhub.ai/user/engsathiago)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and compliance teams use this skill to review AI agents before deployment, during tool or MCP integrations, and for recurring security or compliance audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit may require access to tools, MCP servers, plugins, or credential-leak paths.

Mitigation: Give the agent a clear target scope and avoid granting access to production secrets or broad systems unless that access is intentionally part of the review.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with risk scores, categorized findings, remediation steps, and compliance status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces human-reviewable security audit guidance and does not bundle executable code.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
