## Description:

Use when adding authentication (login, logout, protected routes) to Fastify web applications with @auth0/auth0-fastify for session-based auth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add Auth0 login, logout, callback, session, and protected-route behavior to Fastify web applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authentication setup requires sensitive values such as AUTH0_CLIENT_SECRET and SESSION_SECRET.

Mitigation: Store secrets in a local secret store or uncommitted .env file, generate a strong session secret, and avoid hardcoding credentials in application code.

Risk: Incorrect callback URLs or application base URLs can break the login flow or misroute authentication callbacks.

Mitigation: Verify Auth0 callback URLs and APP_BASE_URL against each deployment environment before production use.

Risk: Generated authentication routes and protected-route logic may need application-specific review before deployment.

Mitigation: Review the generated Fastify auth routes, session checks, and redirects before using them in production.

## Reference(s):

- [Auth0 Fastify Documentation](https://auth0.com/docs/quickstart/webapp/fastify)
- [Auth0 Fastify SDK Repository](https://github.com/auth0/auth0-fastify)
- [Auth0 Agent Skills Repository](https://github.com/auth0/agent-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes environment variable names, Fastify route examples, Auth0 plugin configuration, and common setup checks.]

## Skill Version(s):

1.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
