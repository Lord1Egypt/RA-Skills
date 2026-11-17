## Description:

Provides ArkCLI authentication guidance for SSO login, credential status and identity checks, API key selection, and non-interactive platform profile setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonstarlight](https://clawhub.ai/user/jasonstarlight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to initialize ArkCLI credentials, choose an appropriate login flow, check authentication status or identity, and troubleshoot credential issues. It also covers non-interactive setup for environments that already provide Volcengine credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authentication and credential-handling guidance may be used in environments where credentials are available; the security assessment reports medium confidence and partial coverage.

Mitigation: Review the skill's authentication and credential-handling guidance before installing it, especially in environments where credentials are available.

## Reference(s):

- [API key query and delivery](references/api-key-query.md)
- [Non-interactive Volcengine setup](references/arkcli-auth-init-volc.md)
- [ArkCLI authentication login](references/arkcli-auth-login.md)
- [Authentication status](references/arkcli-auth-status.md)
- [Identity checks](references/arkcli-auth-whoami.md)
- [Authentication modes](references/auth-modes.md)
- [Identity resolution](references/identity-resolution.md)
- [Real-name verification gate](references/realname-gate.md)
- [ClawHub skill page](https://clawhub.ai/jasonstarlight/skills/arkcli-auth)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
