## Description: <br>
Use when adding authentication to Vue.js 3 applications (login, logout, user sessions, protected routes) - integrates @auth0/auth0-vue SDK for SPAs with Vite or Vue CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add Auth0 login, logout, user session handling, protected routes, and API token flows to Vue 3 single-page applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to write Auth0 tenant domain and client ID values into a .env file. <br>
Mitigation: Confirm the correct Auth0 tenant and application before setup, and require explicit user approval before creating or appending .env entries. <br>
Risk: The setup guide may download and run an Auth0 CLI installer script. <br>
Mitigation: Review the downloaded installer script before executing it. <br>
Risk: Example profile views and token flows can expose more identity or session data than intended if copied directly into production. <br>
Mitigation: Avoid displaying full user profile objects in production, validate access tokens on the backend, and prefer in-memory token storage unless persistent sessions are required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/auth0/auth0-vue) <br>
- [Auth0 agent skills repository](https://github.com/auth0/agent-skills) <br>
- [Auth0 Vue SDK documentation](https://auth0.com/docs/libraries/auth0-vue) <br>
- [Auth0 Vue quickstart](https://auth0.com/docs/quickstart/spa/vuejs) <br>
- [Auth0 Vue SDK repository](https://github.com/auth0/auth0-vue) <br>
- [Setup Guide](references/setup.md) <br>
- [Integration Guide](references/integration.md) <br>
- [API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Vue, TypeScript, bash, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose changes to Auth0 tenant settings, application callback URLs, .env entries, Vue plugin setup, router guards, and API token handling.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
