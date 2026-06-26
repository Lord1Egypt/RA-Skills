## Description: <br>
Use when adding authentication (login, logout, protected routes) to Express.js web applications - integrates express-openid-connect for session-based auth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add Auth0-backed, session-based login, logout, protected routes, and API-token usage patterns to Express.js web applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A setup path downloads and runs an Auth0 CLI installer without a complete verification step. <br>
Mitigation: Prefer a trusted package manager, or verify the downloaded installer before execution. <br>
Risk: The skill can append Auth0 credentials and secrets to env files. <br>
Mitigation: Require explicit user confirmation before env-file writes, avoid reading env-file contents, and keep env files out of version control. <br>
Risk: Some examples return raw tokens or full profile data. <br>
Mitigation: Use those examples only for local testing, minimize returned user data, and never expose ID tokens, access tokens, refresh tokens, or full profile objects in production responses. <br>


## Reference(s): <br>
- [Setup Guide](references/setup.md) <br>
- [Integration Guide](references/integration.md) <br>
- [API Reference](references/api.md) <br>
- [Auth0 Express OpenID Connect Documentation](https://auth0.com/docs/libraries/express-openid-connect) <br>
- [Auth0 Express Quickstart](https://auth0.com/docs/quickstart/webapp/express) <br>
- [Express OpenID Connect SDK Repository](https://github.com/auth0/express-openid-connect) <br>
- [Auth0 Agent Skills Homepage](https://github.com/auth0/agent-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript, shell, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Auth0 CLI commands and env-file configuration steps that require user confirmation before writing credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
