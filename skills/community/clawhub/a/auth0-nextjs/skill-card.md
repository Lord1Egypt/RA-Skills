## Description:

Use when adding authentication to Next.js applications (login, logout, protected pages, middleware, server components) - supports App Router and Pages Router with @auth0/nextjs-auth0 SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add Auth0 authentication to Next.js applications, including login, logout, protected pages, middleware, server components, Pages Router routes, and App Router routes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automated Linux setup downloads and runs a remote Auth0 CLI installer.

Mitigation: Prefer manual setup or a trusted package manager; if the installer path is used, inspect and pin or verify the script before execution and avoid unnecessary elevated privileges.

Risk: Setup guidance may write Auth0 credentials and secrets to environment files.

Mitigation: Confirm env-file changes before writing, do not expose existing env-file contents to the agent, keep env files out of version control, and rotate secrets when needed.

Risk: Examples show using Auth0 access tokens when calling external APIs.

Mitigation: Forward tokens only to trusted endpoints, request minimal scopes, and keep authentication and authorization checks on the server side.

## Reference(s):

- [Setup Guide](references/setup.md)
- [Integration Guide](references/integration.md)
- [API Reference](references/api.md)
- [Auth0 Next.js SDK Documentation](https://auth0.com/docs/libraries/nextjs-auth0)
- [Auth0 Next.js Quickstart](https://auth0.com/docs/quickstart/webapp/nextjs)
- [Auth0 Next.js SDK GitHub Repository](https://github.com/auth0/nextjs-auth0)
- [Auth0 Agent Skills Homepage](https://github.com/auth0/agent-skills)
- [ClawHub Skill Page](https://clawhub.ai/auth0/skills/auth0-nextjs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file placement guidance, environment variable configuration, Auth0 dashboard or CLI setup steps, and Next.js router-specific implementation snippets.]

## Skill Version(s):

1.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
