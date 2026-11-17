## Description:

Helps agents add Auth0 JWT Bearer validation to Express or Node.js APIs with express-oauth2-jwt-bearer middleware, RBAC, claim validation, and optional DPoP support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate Auth0 token validation into Express or Node.js API projects, including protected routes, Auth0 API setup, scope-based RBAC, claim validation, CORS handling, and verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automatic setup path can create Auth0 tenant resources using the active Auth0 CLI login.

Mitigation: Prefer manual setup when possible, or review the displayed change plan and active tenant before approving the bootstrap script.

Risk: The bootstrap path can edit the target project's .env file.

Mitigation: Review the generated AUTH0_DOMAIN and AUTH0_AUDIENCE values, keep production secrets out of shell commands, and ensure .env files are not committed.

Risk: The bootstrap path installs npm dependencies whose versions may resolve to newer mutable releases.

Mitigation: Pin or lock npm dependencies before use in controlled environments.

## Reference(s):

- [Auth0 Agent Skills Repository](https://github.com/auth0/agent-skills)
- [Setup Guide](references/setup.md)
- [Integration Patterns](references/integration.md)
- [API Reference and Testing](references/api.md)
- [express-oauth2-jwt-bearer on npm](https://www.npmjs.com/package/express-oauth2-jwt-bearer)
- [Auth0 Node.js API Quickstart](https://auth0.com/docs/quickstart/backend/nodejs/interactive)
- [RFC 6750 Bearer Token Usage](https://datatracker.ietf.org/doc/html/rfc6750)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript, shell, JSON, and environment-variable snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose edits to an Express or Node.js project and may guide optional Auth0 CLI bootstrap setup.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
