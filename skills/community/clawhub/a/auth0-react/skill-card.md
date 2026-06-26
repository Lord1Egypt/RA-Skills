## Description: <br>
Use when adding authentication to React applications (login, logout, user sessions, protected routes) - integrates @auth0/auth0-react SDK for SPAs with Vite or Create React App. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add Auth0 authentication to React single-page applications, including login, logout, session handling, protected routes, API token usage, and MFA patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup guidance may install the Auth0 CLI, create or modify Auth0 applications, and append Auth0 values to a .env file. <br>
Mitigation: Review setup commands before running them, confirm tenant and application changes explicitly, and inspect .env changes without exposing existing secrets. <br>
Risk: Token-handling examples can expose bearer tokens too casually, including an access-token console log. <br>
Mitigation: Remove token logging before use and avoid copying examples that display or persist bearer tokens unnecessarily. <br>
Risk: Using localStorage for token storage can increase exposure if the application has cross-site scripting weaknesses. <br>
Mitigation: Prefer in-memory token storage unless persistent storage is required and the application has strong XSS protections. <br>


## Reference(s): <br>
- [Setup Guide](references/setup.md) <br>
- [Integration Guide](references/integration.md) <br>
- [API Reference](references/api.md) <br>
- [Auth0 React SDK Documentation](https://auth0.com/docs/libraries/auth0-react) <br>
- [Auth0 React Quickstart](https://auth0.com/docs/quickstart/spa/react) <br>
- [Auth0 React SDK Repository](https://github.com/auth0/auth0-react) <br>
- [Auth0 Agent Skills Homepage](https://github.com/auth0/agent-skills) <br>
- [Auth0 React on ClawHub](https://clawhub.ai/auth0/auth0-react) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript, shell, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Auth0 CLI commands and React SDK configuration examples that require user review before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
