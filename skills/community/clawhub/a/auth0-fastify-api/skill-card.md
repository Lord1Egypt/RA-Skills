## Description:

Use when securing Fastify API endpoints with JWT Bearer token validation, scope and permission checks, or stateless authentication using Auth0.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add Auth0 JWT access-token validation to Fastify REST APIs, protect routes, configure audience and domain values, and test public and protected endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Auth0 CLI example can create an API resource in an Auth0 tenant.

Mitigation: Review the CLI command, tenant context, API name, and identifier before running it.

Risk: Installing npm packages introduces external dependencies into the Fastify API project.

Mitigation: Review the listed packages and lockfile changes before deploying the resulting API.

Risk: Using this guidance outside an API that validates Auth0 JWT access tokens can lead to the wrong authentication pattern.

Mitigation: Use this skill only for Fastify REST APIs that receive Auth0 access tokens, and choose a session-based or frontend SDK for other application types.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/auth0/skills/auth0-fastify-api)
- [Auth0 Agent Skills Homepage](https://github.com/auth0/agent-skills)
- [Auth0 Fastify API Documentation](https://auth0.com/docs/quickstart/backend/fastify)
- [Auth0 Fastify SDK Repository](https://github.com/auth0/auth0-fastify)
- [Auth0 Access Tokens Guide](https://auth0.com/docs/secure/tokens/access-tokens)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes package installation commands, Auth0 CLI examples, environment variable examples, Fastify plugin setup, protected route snippets, and testing commands.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
