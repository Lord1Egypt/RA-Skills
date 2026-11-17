## Description:

Use when securing ASP.NET Core Web API endpoints with JWT Bearer token validation, scope and permission checks, stateless auth, and DPoP proof-of-possession token binding with Auth0.AspNetCore.Authentication.Api.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add Auth0 JWT bearer authentication to ASP.NET Core Web APIs, configure API audience and tenant settings, protect endpoints, enforce scopes, and test access-token validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation examples omit an explicit NuGet package version.

Mitigation: Pin Auth0.AspNetCore.Authentication.Api to a reviewed version and use trusted package sources before applying the setup.

Risk: Token and client-secret examples can encourage accidental exposure of sensitive values.

Mitigation: Keep real client secrets out of source code, logs, screenshots, and prompts; use environment variables or a secret store for sensitive configuration.

Risk: Misconfigured Auth0 domain, audience, middleware order, or scopes can leave endpoints inaccessible or improperly protected.

Mitigation: Review the generated configuration against the Auth0 API settings, keep authentication before authorization middleware, and test both public and protected endpoints.

## Reference(s):

- [Setup Guide](artifact/references/setup.md)
- [Integration Guide](artifact/references/integration.md)
- [API Reference](artifact/references/api.md)
- [Auth0 ASP.NET Core Web API Quickstart](https://auth0.com/docs/quickstart/backend/aspnet-core-webapi)
- [Auth0 ASP.NET Core API SDK](https://github.com/auth0/aspnetcore-api)
- [Auth0 ASP.NET Core API Documentation](https://auth0.github.io/aspnetcore-api)
- [Auth0 Access Tokens Guide](https://auth0.com/docs/secure/tokens/access-tokens)
- [ClawHub Publisher Profile](https://clawhub.ai/user/auth0)
- [ClawHub Skill Page](https://clawhub.ai/auth0/skills/auth0-aspnetcore-api)
- [ClawHub Source Homepage](https://github.com/auth0/agent-skills)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, JSON, and C# code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts for manual or automated Auth0 API setup before giving setup steps that may change application configuration.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
