## Description:

Use when adding authentication to Angular applications with route guards and HTTP interceptors - integrates @auth0/auth0-angular SDK for SPAs

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add Auth0 authentication to Angular 13+ single-page applications, including SDK setup, route guards, protected API calls, login/logout UI, and testing patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automated setup path downloads and runs a remote installer for the Auth0 CLI.

Mitigation: Prefer the manual setup path, or download and review the installer before executing it.

Risk: Some examples log access tokens or display full profile JSON during development.

Mitigation: Remove token logging and full profile dumps before production use.

Risk: The configuration examples include localStorage token persistence as an option.

Mitigation: Use memory storage unless persistent browser storage is an explicit, reviewed requirement.

## Reference(s):

- [Auth0 Angular Skill Page](https://clawhub.ai/auth0/skills/auth0-angular)
- [Auth0 Agent Skills Homepage](https://github.com/auth0/agent-skills)
- [Setup Guide](references/setup.md)
- [Integration Guide](references/integration.md)
- [API Reference](references/api.md)
- [Auth0 Angular SDK Documentation](https://auth0.com/docs/libraries/auth0-angular)
- [Auth0 Angular Quickstart](https://auth0.com/docs/quickstart/spa/angular)
- [Auth0 Angular SDK GitHub](https://github.com/auth0/auth0-angular)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
