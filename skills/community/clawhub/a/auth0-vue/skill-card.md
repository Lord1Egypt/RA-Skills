## Description:

Use when adding authentication to Vue.js 3 applications, including login, logout, user sessions, and protected routes, with the @auth0/auth0-vue SDK for SPAs built with Vite or Vue CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add Auth0 authentication to Vue 3 single-page applications, configure the Auth0 Vue SDK, protect routes, retrieve user profile data, and call protected APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance includes copy-paste commands for Auth0 CLI installation, including a downloaded Linux installer.

Mitigation: Prefer package-manager or pinned, verified Auth0 CLI installation steps, and do not run the downloaded installer automatically.

Risk: API examples attach access tokens to request headers.

Mitigation: Attach tokens only to fixed, trusted HTTPS API origins and review audience configuration before use.

Risk: Profile examples may display or dump full user objects.

Mitigation: Avoid dumping full user objects in UI or logs; display only fields required by the application.

Risk: Token storage choices can increase exposure if persistent storage is used casually.

Mitigation: Keep SDK token storage in memory unless persistent sessions are an explicit and reviewed requirement.

## Reference(s):

- [Setup Guide](references/setup.md)
- [Integration Guide](references/integration.md)
- [API Reference](references/api.md)
- [Auth0 Vue SDK Documentation](https://auth0.com/docs/libraries/auth0-vue)
- [Auth0 Vue Quickstart](https://auth0.com/docs/quickstart/spa/vuejs)
- [Auth0 Vue SDK GitHub Repository](https://github.com/auth0/auth0-vue)
- [Auth0 Agent Skills Homepage](https://github.com/auth0/agent-skills)
- [ClawHub Skill Page](https://clawhub.ai/auth0/skills/auth0-vue)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript, Vue, shell, and environment configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands and configuration changes that should be reviewed before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
