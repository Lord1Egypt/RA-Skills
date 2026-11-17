## Description:

Adds Auth0 authentication to Vanilla JS, Svelte, SolidJS, and other framework-agnostic single-page applications using the @auth0/auth0-spa-js SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add Auth0 login/logout, token retrieval, SPA application configuration, and build verification to browser-based single-page applications that are not using framework-specific Auth0 wrappers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path can execute unverified remote installer code for the Auth0 CLI.

Mitigation: Install the Auth0 CLI through a trusted package manager or verified release, and review any downloaded installer before execution.

Risk: Bootstrap/setup can make persistent Auth0 tenant changes and update project .env configuration.

Mitigation: Run setup only in the intended project, confirm the displayed Auth0 tenant changes, and inspect or back up existing .env before allowing updates.

## Reference(s):

- [Auth0 SPA JS Setup Guide](references/setup.md)
- [Auth0 SPA JS Integration Patterns](references/integration.md)
- [Auth0 SPA JS API Reference & Testing](references/api.md)
- [Auth0 SPA JS SDK Documentation](https://auth0.com/docs/libraries/auth0-spa-js)
- [Auth0 Vanilla JS Quickstart](https://auth0.com/docs/quickstart/spa/vanillajs)
- [Auth0 SPA JS SDK Repository](https://github.com/auth0/auth0-spa-js)
- [Auth0 SPA JS API Documentation](https://auth0.github.io/auth0-spa-js/)
- [Auth0 Agent Skills Repository](https://github.com/auth0/agent-skills)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript snippets, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose project file edits, Auth0 CLI commands, and .env updates that require user confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
