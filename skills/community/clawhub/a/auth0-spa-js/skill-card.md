## Description: <br>
Use when adding authentication to Vanilla JS, Svelte, or any framework-agnostic single-page applications - integrates @auth0/auth0-spa-js SDK for SPAs without framework-specific wrappers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add Auth0 authentication to browser-based single-page applications that do not use framework-specific Auth0 wrappers. It provides SDK setup guidance, Auth0 tenant configuration steps, login and logout patterns, token retrieval examples, and verification checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated setup can create or update Auth0 applications, database connections, and project environment configuration. <br>
Mitigation: Review the proposed Auth0 tenant and file changes before approval, and use the manual setup path when automated changes are not appropriate. <br>
Risk: Installer guidance includes a curl-to-shell Auth0 CLI installation path. <br>
Mitigation: Prefer Homebrew, Scoop, or a verified Auth0 CLI release, and inspect installer commands before running them. <br>
Risk: Updating an existing .env file can expose or alter sensitive local configuration. <br>
Mitigation: Do not let the agent read existing .env contents unless explicitly intended; confirm before any environment file update and review the resulting keys. <br>


## Reference(s): <br>
- [Setup Guide](references/setup.md) <br>
- [Integration Patterns](references/integration.md) <br>
- [API Reference and Testing](references/api.md) <br>
- [Auth0 SPA JS SDK Documentation](https://auth0.com/docs/libraries/auth0-spa-js) <br>
- [Auth0 Vanilla JS Quickstart](https://auth0.com/docs/quickstart/spa/vanillajs) <br>
- [Auth0 SPA JS SDK Repository](https://github.com/auth0/auth0-spa-js) <br>
- [Auth0 SPA JS API Documentation](https://auth0.github.io/auth0-spa-js/) <br>
- [Auth0 Agent Skills Homepage](https://github.com/auth0/agent-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JavaScript, shell commands, and environment configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce project file edits, Auth0 CLI commands, and build verification steps when used by an agent with filesystem and shell access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
