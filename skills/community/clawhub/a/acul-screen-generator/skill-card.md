## Description:

Generates complete, branded Auth0 Advanced Custom Universal Login (ACUL) screen implementations using the React or Vanilla JS SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create, add, or modify Auth0 ACUL login screens with custom branding, social login, theming, and authentication-flow-specific behavior. It guides project setup, reference selection, component generation, and Auth0 CLI development commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vanilla JS outputs may include unsafe HTML construction in authentication pages.

Mitigation: Prefer the React path, or require Vanilla JS outputs to use DOM APIs/textContent and validated HTTPS icon URLs before use in real login flows.

Risk: Connected ACUL development mode can update an Auth0 tenant in real time.

Mitigation: Use connected mode only with stage or development tenants, and review generated changes before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/auth0/skills/acul-screen-generator)
- [Auth0 agent skills homepage](https://github.com/auth0/agent-skills)
- [ACUL React SDK reference](artifact/references/acul-react-sdk.md)
- [ACUL JS SDK reference](artifact/references/acul-js-sdk.md)
- [ACUL CLI commands](artifact/references/cli-commands.md)
- [ACUL screen catalog](artifact/references/screen-catalog.md)
- [Social providers](artifact/references/social-providers.md)
- [Theming patterns](artifact/references/theming-patterns.md)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces React or Vanilla JS ACUL screen code, theme files, and Auth0 CLI commands.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
