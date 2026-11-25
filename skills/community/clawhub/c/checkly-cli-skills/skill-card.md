## Description:

Provides Checkly CLI guidance for Monitoring as Code, synthetic monitoring, tests, deployments, imports, account usage, and related workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vince-winkintel](https://clawhub.ai/user/vince-winkintel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to author, test, deploy, and manage synthetic checks and Monitoring as Code with the Checkly CLI. It also guides account access, usage, and operational workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deployment and file-writing examples can change Checkly resources or local project files, and unpinned CLI commands may run code while credentials are available.

Mitigation: Review deployment plans and file-writing examples, verify the CLI version before running commands with credentials, and inspect behavior beyond the partial scan coverage.

## Reference(s):

- [Checkly Documentation](https://www.checklyhq.com/docs/)
- [Checkly Usage API](https://www.checklyhq.com/docs/api-reference/usage/overview/)
- [Playwright Documentation](https://playwright.dev/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with shell commands and TypeScript/JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that deploy or change account resources and files; review proposed changes before execution.]

## Skill Version(s):

1.0.23 (source: server-resolved release metadata, artifact/VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
