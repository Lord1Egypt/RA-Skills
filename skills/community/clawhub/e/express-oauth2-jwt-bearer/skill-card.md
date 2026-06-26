## Description: <br>
Helps developers add Auth0 JWT Bearer token validation to Express or Node.js APIs using the express-oauth2-jwt-bearer SDK, including endpoint protection, RBAC, claim checks, and optional DPoP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate Auth0 access-token validation into Express or Node.js APIs, configure Auth0 API audience and issuer settings, and add protected routes, RBAC checks, and verification steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional bootstrap can create an Auth0 API in the active tenant and update a .env file in the target project. <br>
Mitigation: Review the generated change plan before applying it, run bootstrap only in the intended tenant and project directory, and inspect .env changes afterward. <br>
Risk: M2M client secrets used to request test tokens are sensitive credentials. <br>
Mitigation: Keep client secrets server-side, avoid exposing them in shell history or logs, and never commit them to source control. <br>
Risk: Incorrect audience, issuer, CORS order, or RBAC claim configuration can cause failed authorization or unintended access behavior. <br>
Mitigation: Use the documented setup and testing checklist to verify 401, 403, and successful-token paths before deployment. <br>


## Reference(s): <br>
- [Setup Guide](references/setup.md) <br>
- [Integration Patterns](references/integration.md) <br>
- [API Reference & Testing](references/api.md) <br>
- [Auth0 agent-skills homepage](https://github.com/auth0/agent-skills) <br>
- [express-oauth2-jwt-bearer on npm](https://www.npmjs.com/package/express-oauth2-jwt-bearer) <br>
- [Auth0 node-oauth2-jwt-bearer repository](https://github.com/auth0/node-oauth2-jwt-bearer) <br>
- [Auth0 Node.js API Quickstart](https://auth0.com/docs/quickstart/backend/nodejs/interactive) <br>
- [Auth0 APIs Dashboard](https://manage.auth0.com/#/apis) <br>
- [RFC 6750 Bearer Token Usage](https://datatracker.ietf.org/doc/html/rfc6750) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JavaScript, TypeScript, shell, JSON, and environment-variable examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write .env configuration during optional bootstrap when the user approves Auth0 setup changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
