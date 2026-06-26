## Description: <br>
Helps developers secure FastAPI API endpoints with Auth0 JWT bearer token validation, scope and permission checks, stateless authentication, and DPoP proof-of-possession token binding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Auth0-backed authentication for FastAPI APIs, including API resource setup, environment configuration, route protection, scope enforcement, and token validation patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated setup may use an existing Auth0 CLI session and write tenant-specific API configuration. <br>
Mitigation: Ask the user to choose automated setup before running CLI commands, then confirm the tenant domain and audience before writing or using .env values. <br>
Risk: Secrets, access tokens, client secrets, or .env contents could be exposed if pasted into the agent conversation. <br>
Mitigation: Do not request or display real secrets or tokens; use placeholders and instruct the user to keep sensitive values local. <br>
Risk: Copied cache or deployment examples may be inappropriate for shared or production infrastructure. <br>
Mitigation: Review cache adapters, TTLs, and deployment settings against the target environment before applying them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/auth0/auth0-fastapi-api) <br>
- [Auth0 Agent Skills Homepage](https://github.com/auth0/agent-skills) <br>
- [auth0-fastapi-api GitHub](https://github.com/auth0/auth0-fastapi-api) <br>
- [auth0-fastapi-api on PyPI](https://pypi.org/project/auth0-fastapi-api/) <br>
- [Auth0 FastAPI API Quickstart](https://auth0.com/docs/quickstart/backend/fastapi) <br>
- [FastAPI Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/) <br>
- [Access Tokens Guide](https://auth0.com/docs/secure/tokens/access-tokens) <br>
- [Setup Guide](references/setup.md) <br>
- [Integration Guide](references/integration.md) <br>
- [API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python, bash, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Auth0 CLI commands, FastAPI dependency code, .env configuration keys, and testing commands for JWT-protected APIs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
