## Description:

Use when adding MFA, 2FA, TOTP, SMS codes, push notifications, passkeys, or when requiring step-up verification for sensitive operations or meeting compliance requirements with Auth0.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and identity engineers use this skill to add Auth0 multi-factor authentication, step-up verification, adaptive MFA, and backend MFA validation for applications that protect sensitive user actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auth0 CLI and Management API commands can change tenant MFA policies, deploy Actions, or delete authenticators.

Mitigation: Run commands only against an authorized Auth0 tenant and review proposed policy changes, Action deployments, and authenticator deletion commands before execution.

## Reference(s):

- [Auth0 publisher profile](https://clawhub.ai/user/auth0)
- [ClawHub skill page](https://clawhub.ai/auth0/skills/auth0-mfa)
- [Auth0 agent-skills homepage](https://github.com/auth0/agent-skills)
- [Auth0 MFA Documentation](https://auth0.com/docs/secure/multi-factor-authentication)
- [Step-Up Authentication](https://auth0.com/docs/secure/multi-factor-authentication/step-up-authentication)
- [MFA API](https://auth0.com/docs/secure/multi-factor-authentication/manage-mfa-auth0-apis)
- [acr_values Parameter](https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow/add-login-auth-code-flow#request-parameters)
- [Step-Up Examples](references/examples.md)
- [Backend Validation](references/backend.md)
- [Advanced Topics](references/advanced.md)
- [Reference Guide](references/api.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Auth0 CLI and Management API command examples that should be reviewed before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
