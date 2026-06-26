## Description: <br>
Use when adding authentication (login, logout, protected routes) to Fastify web applications - integrates @auth0/auth0-fastify for session-based auth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to add Auth0 session-based login, logout, callback handling, and protected routes to Fastify web applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auth0 client secrets and session secrets are required for setup. <br>
Mitigation: Keep AUTH0_CLIENT_SECRET and SESSION_SECRET out of source control and use production secret management where appropriate. <br>
Risk: Unreviewed npm dependency changes could alter authentication behavior. <br>
Mitigation: Pin or review npm dependency versions before deployment. <br>


## Reference(s): <br>
- [Auth0 Fastify Documentation](https://auth0.com/docs/quickstart/webapp/fastify) <br>
- [Auth0 Fastify SDK Repository](https://github.com/auth0/auth0-fastify) <br>
- [Auth0 Agent Skills Repository](https://github.com/auth0/agent-skills) <br>
- [ClawHub Skill Page](https://clawhub.ai/auth0/auth0-fastify) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses environment variables for Auth0 tenant settings, client credentials, and session secrets.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
