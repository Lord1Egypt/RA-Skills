## Description:

Use when securing FastAPI API endpoints with JWT Bearer token validation, scope and permission checks, or stateless authentication using auth0-fastapi-api, including DPoP proof-of-possession token binding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add Auth0 JWT access-token validation to FastAPI APIs, protect routes, enforce scopes, configure DPoP, and test authentication behavior. It is intended for APIs that receive access tokens from SPAs, mobile apps, or service clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may propose Auth0 tenant changes such as creating API resources or changing authentication settings.

Mitigation: Review the proposed tenant changes before execution and confirm that identifiers, domains, scopes, and DPoP settings match the intended API.

Risk: Auth0 client secrets, access tokens, test tokens, or environment files could be exposed if pasted into the agent conversation.

Mitigation: Avoid sharing real secrets or tokens in chat, do not read `.env` contents into context, and use placeholders or local environment management where possible.

Risk: Dependency drift could change auth0-fastapi-api behavior because the artifact notes the SDK is beta.

Mitigation: Prefer pinned dependencies or a lock file and review SDK release notes before upgrading.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/auth0/skills/auth0-fastapi-api)
- [Publisher Profile](https://clawhub.ai/user/auth0)
- [Auth0 Agent Skills Homepage](https://github.com/auth0/agent-skills)
- [Setup Guide](references/setup.md)
- [Integration Guide](references/integration.md)
- [API Reference](references/api.md)
- [auth0-fastapi-api GitHub](https://github.com/auth0/auth0-fastapi-api)
- [auth0-fastapi-api on PyPI](https://pypi.org/project/auth0-fastapi-api/)
- [Auth0 FastAPI API Quickstart](https://auth0.com/docs/quickstart/backend/fastapi)
- [FastAPI Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [Auth0 Access Tokens Guide](https://auth0.com/docs/secure/tokens/access-tokens)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python, bash, JSON, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Auth0 tenant setup steps and environment-variable configuration; users should review changes before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
