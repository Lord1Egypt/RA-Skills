## Description: <br>
Use when securing Fastify API endpoints with JWT Bearer token validation, scope/permission checks, or stateless authentication using @auth0/auth0-fastify-api for REST APIs receiving access tokens from frontends or mobile apps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure JWT access-token validation for Fastify APIs, protect routes, check scopes, and avoid common Auth0 API setup mistakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency installation could use an unexpected npm package or registry source. <br>
Mitigation: Verify the npm package names and registry before installation, and use a lockfile for repeatable dependency resolution. <br>
Risk: Auth0 CLI operations could target the wrong tenant or API resource. <br>
Mitigation: Confirm the Auth0 CLI is logged into the intended tenant and create an Auth0 API resource, not an application, before applying the configuration. <br>
Risk: Access tokens, tenant details, or authorization headers could be exposed in logs or shared transcripts. <br>
Mitigation: Use placeholder tokens in examples, avoid pasting real bearer tokens into shared agent conversations, and redact sensitive values from logs. <br>


## Reference(s): <br>
- [Auth0 Agent Skills Homepage](https://github.com/auth0/agent-skills) <br>
- [Auth0 Fastify API Documentation](https://auth0.com/docs/quickstart/backend/fastify) <br>
- [Auth0 Fastify SDK Repository](https://github.com/auth0/auth0-fastify) <br>
- [Auth0 Access Tokens Guide](https://auth0.com/docs/secure/tokens/access-tokens) <br>
- [ClawHub Release Page](https://clawhub.ai/auth0/auth0-fastify-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Auth0 API configuration, Auth0 tenant domain, API audience, Node.js 20 or newer, Fastify 5 or newer, and access tokens for protected endpoint testing.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
