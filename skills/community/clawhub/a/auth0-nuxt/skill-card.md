## Description:

Use when implementing Auth0 authentication in Nuxt 3/4 applications, configuring session management, protecting routes with middleware, or integrating API access tokens - provides setup patterns, composable usage, and security best practices for the @auth0/auth0-nuxt SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement Auth0 authentication in Nuxt 3/4 applications, including SDK setup, server-side sessions, route and API protection, custom session stores, and API token access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy-ready authentication examples could lead to weak route or API authorization if used without server-side validation.

Mitigation: Validate sessions and authorization server-side, and treat client-side helpers such as useUser() as display or navigation aids only.

Risk: Stateful session store examples can expose session infrastructure or sensitive data if deployed without hardening.

Mitigation: Restrict database and Redis access, use TLS where applicable, manage credentials through environment-backed secret handling, and review storage of PII.

Risk: Impersonation and audit-log examples can introduce privacy, accountability, or privilege-escalation issues if adopted as-is.

Mitigation: Add explicit authorization checks, audit controls, approval boundaries, and privacy review before implementing impersonation or audit logging.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/auth0/skills/auth0-nuxt)
- [Auth0 Agent Skills Homepage](https://github.com/auth0/agent-skills)
- [Auth0 Nuxt GitHub](https://github.com/auth0/auth0-nuxt)
- [Auth0 Docs](https://auth0.com/docs)
- [Nuxt Modules](https://nuxt.com/modules)
- [Route Protection Patterns](references/route-protection.md)
- [Custom Session Stores](references/session-stores.md)
- [Common Patterns and Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with TypeScript, Vue, shell, YAML, SQL, and configuration code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces implementation patterns and draft examples that require security review before production use]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
