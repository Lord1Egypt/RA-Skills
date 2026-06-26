## Description: <br>
Generates complete, branded Auth0 Advanced Custom Universal Login (ACUL) screen implementations using the React or Vanilla JS SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, add, or modify Auth0 ACUL login screens with custom branding, social login, theming, and authentication-flow behavior. It guides project setup, reference selection, screen code generation, theme-file generation, and local or connected ACUL preview commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connected ACUL preview mode can update the active Auth0 tenant in real time. <br>
Mitigation: Use connected mode only with development or staging tenants, and review the active tenant before running connected commands. <br>
Risk: Generated Vanilla JS social-login examples may render provider data into HTML. <br>
Mitigation: Sanitize dynamic provider values or build social buttons with DOM APIs before using generated code in production. <br>
Risk: Exported ACUL configuration files may contain environment-specific tenant configuration. <br>
Mitigation: Review generated and exported ACUL config files and avoid committing sensitive or tenant-specific configuration. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/auth0/acul-screen-generator) <br>
- [Auth0 agent skills homepage](https://github.com/auth0/agent-skills) <br>
- [Auth0 ACUL samples](https://github.com/auth0-samples/auth0-acul-samples) <br>
- [Auth0 Universal Login SDK examples](https://github.com/auth0/universal-login) <br>
- [ACUL Screen Catalog](references/screen-catalog.md) <br>
- [Auth0 ACUL React SDK Reference](references/acul-react-sdk.md) <br>
- [Auth0 ACUL JS SDK Reference](references/acul-js-sdk.md) <br>
- [Auth0 ACUL CLI Commands Reference](references/cli-commands.md) <br>
- [Social Login Provider Patterns](references/social-providers.md) <br>
- [Theming Patterns for ACUL Screens](references/theming-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with TypeScript, JavaScript, CSS, JSON, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces ACUL screen components, theme files, CLI commands, and implementation guidance; connected-mode commands should be used only with development or staging tenants.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
