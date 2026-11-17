## Description:

Use when adding authentication (login, logout, protected routes) to Express.js web applications - integrates express-openid-connect for session-based auth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and engineers use this skill to add session-based Auth0 login, logout, callback handling, protected routes, and related Express.js authentication patterns to web applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions may install the Auth0 CLI through a downloaded shell installer.

Mitigation: Prefer a pinned and verified package manager or release; review any downloaded installer before execution and avoid administrator privileges unless necessary.

Risk: Environment-file setup writes Auth0 credentials and placeholders that may expose secrets if mishandled.

Mitigation: Require explicit confirmation before writing .env or .env.local, never read existing secret files into the agent context, replace placeholders manually, and confirm the file is ignored by version control.

Risk: Example routes may expose raw tokens or render user claims directly if copied without review.

Mitigation: Avoid returning raw access, ID, or refresh tokens to clients and escape or template user profile claims before rendering them.

## Reference(s):

- [Setup Guide](references/setup.md)
- [Integration Guide](references/integration.md)
- [API Reference](references/api.md)
- [OpenClaw homepage](https://github.com/auth0/agent-skills)
- [Express OpenID Connect Documentation](https://auth0.com/docs/libraries/express-openid-connect)
- [Auth0 Express Quickstart](https://auth0.com/docs/quickstart/webapp/express)
- [express-openid-connect GitHub Repository](https://github.com/auth0/express-openid-connect)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JavaScript, shell, and environment configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose package installation, Auth0 CLI setup, Express middleware changes, protected route examples, and environment variable configuration.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
