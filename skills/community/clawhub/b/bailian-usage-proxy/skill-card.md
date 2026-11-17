## Description:

Bailian Usage Proxy helps deploy an OpenAI-compatible proxy for Alibaba Bailian/DashScope shared accounts with per-user token usage tracking, call counting, quota management, and usage reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bjmfjoy](https://clawhub.ai/user/bjmfjoy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform administrators use this skill to deploy and operate a shared-account proxy for Alibaba Bailian/DashScope, issue internal API keys, track token usage by user and model, enforce quotas, and export usage reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Admin and credential-management endpoints may expose paid API usage controls if reachable by untrusted users.

Mitigation: Add authentication and authorization to all admin routes before deployment and restrict admin access to trusted networks.

Risk: Plaintext environment secrets, internal API keys, and default service credentials can be exposed or reused.

Mitigation: Use a managed secret store where possible, protect or hash issued user API keys, and replace all default database and application secrets.

Risk: Unreviewed dependencies and deployment defaults can increase operational risk for a shared paid API proxy.

Mitigation: Review and scan the release before deployment, pin or lock dependencies with hashes, and expose only the required service ports.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bjmfjoy/skills/bailian-usage-proxy)
- [API Documentation](references/api.md)
- [Architecture Documentation](references/architecture.md)
- [Database Documentation](references/database.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code blocks and deployment commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include environment variable guidance, Docker or shell commands, API examples, and usage reporting instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata and app package version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
