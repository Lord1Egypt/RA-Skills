## Description: <br>
Use when securing ASP.NET Core Web API endpoints with JWT Bearer token validation, scope/permission checks, or stateless auth - integrates Auth0.AspNetCore.Authentication.Api for REST APIs receiving access tokens from frontends or mobile apps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add Auth0 JWT bearer authentication, authorization policies, and DPoP support to ASP.NET Core Web API applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auth0 CLI commands can create or modify API resources and local configuration in the selected tenant. <br>
Mitigation: Review commands before execution and confirm the target Auth0 tenant and API identifier. <br>
Risk: Client secrets, access tokens, and tenant configuration can be exposed through chat, terminal history, logs, or committed files. <br>
Mitigation: Keep real secrets and tokens out of shared prompts, command history, logs, and repositories; use user secrets or environment variables. <br>


## Reference(s): <br>
- [Setup Guide](references/setup.md) <br>
- [Integration Guide](references/integration.md) <br>
- [API Reference](references/api.md) <br>
- [Auth0 Agent Skills Homepage](https://github.com/auth0/agent-skills) <br>
- [Auth0 ASP.NET Core Web API Quickstart](https://auth0.com/docs/quickstart/backend/aspnet-core-webapi) <br>
- [Auth0 ASP.NET Core API SDK](https://github.com/auth0/aspnetcore-api) <br>
- [Auth0 ASP.NET Core API Documentation](https://auth0.github.io/aspnetcore-api) <br>
- [Auth0 Access Tokens Guide](https://auth0.com/docs/secure/tokens/access-tokens) <br>
- [Microsoft JWT Bearer Options](https://learn.microsoft.com/en-us/dotnet/api/microsoft.aspnetcore.authentication.jwtbearer.jwtbeareroptions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with C#, JSON, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Auth0 CLI commands and configuration changes for ASP.NET Core projects] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
