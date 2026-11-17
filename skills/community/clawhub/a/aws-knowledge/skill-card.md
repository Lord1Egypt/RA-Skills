## Description:

Openclaw provides AWS expertise by querying the AWS Knowledge MCP Server via mcporter for current documentation, best practices, SOPs, regional availability, architecture guidance, troubleshooting, cost optimization, security hardening, and infrastructure-as-code questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[w0yne](https://clawhub.ai/user/w0yne)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud engineers, and operators use this skill to answer AWS service, architecture, deployment, troubleshooting, security, cost, regional availability, CDK, and CloudFormation questions with source-backed AWS documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and depends on the current npm release of mcporter, which is not pinned to a reviewed version in the release evidence.

Mitigation: Use a restricted environment for installation, or independently review, verify, and pin the mcporter version before higher-assurance use.

## Reference(s):

- [AWS Query Patterns by Domain](references/query-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown responses with cited AWS documentation URLs and inline shell commands when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcporter and a configured aws-knowledge MCP server.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
