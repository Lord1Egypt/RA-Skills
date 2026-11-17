## Description:

Provides Auth0 CLI command guidance for managing Auth0 applications, APIs, users, roles, organizations, actions, logs, custom domains, Universal Login, Terraform export, raw Management API calls, and JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to plan and run Auth0 CLI workflows for tenant administration, application setup, API registration, RBAC, organizations, Actions, logging, custom domains, Universal Login branding, Terraform export, and direct Management API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact Auth0 tenant administration, including deletes, raw API writes, Action deployment, and log streaming.

Mitigation: Require explicit approval before running destructive commands, raw API POST/PATCH/DELETE calls, Action deployments, log streaming, or commands that reveal sensitive values.

Risk: Some workflows accept or reveal client secrets, private keys, user data, or other tenant credentials.

Mitigation: Avoid pasting real secrets into chat or command lines unless the environment masks and protects them, and prefer secure secret handling for CI/CD workflows.

## Reference(s):

- [Full CLI Reference](references/cli.md)
- [Auth0 Agent Skills Repository](https://github.com/auth0/agent-skills)
- [Auth0 CLI Documentation](https://auth0.github.io/auth0-cli/)
- [Auth0 Management API v2](https://auth0.com/docs/api/management/v2)
- [Auth0 Documentation](https://auth0.com/docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON, and jq examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands assume an authenticated Auth0 CLI session and may require tenant-specific IDs, domains, scopes, and explicit approval for high-impact operations.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
