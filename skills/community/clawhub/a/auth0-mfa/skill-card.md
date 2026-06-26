## Description: <br>
Use when adding MFA, 2FA, TOTP, SMS codes, push notifications, passkeys, or when requiring step-up verification for sensitive operations or meeting compliance requirements (HIPAA, PCI-DSS) - covers adaptive and risk-based authentication with Auth0. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to configure Auth0 MFA, implement step-up authentication for sensitive operations, and validate MFA status in frontend and backend applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auth0 admin commands can change tenant-wide MFA factors, policies, and Actions. <br>
Mitigation: Confirm the target tenant and review generated Auth0 CLI/API commands before execution. <br>
Risk: Management API tokens or tenant credentials could be exposed if placed in prompts, logs, or command history. <br>
Mitigation: Use least-privilege credentials and keep real tokens out of prompts and logs. <br>
Risk: Tenant-wide MFA policies or Auth0 Actions can disrupt sign-in flows if tested directly in production. <br>
Mitigation: Validate MFA policy and Action changes outside production before rollout. <br>


## Reference(s): <br>
- [Auth0 MFA skill page](https://clawhub.ai/auth0/auth0-mfa) <br>
- [Auth0 agent skills homepage](https://github.com/auth0/agent-skills) <br>
- [Step-Up Examples](references/examples.md) <br>
- [Backend Validation](references/backend.md) <br>
- [Advanced Topics](references/advanced.md) <br>
- [Reference Guide](references/api.md) <br>
- [Auth0 MFA Documentation](https://auth0.com/docs/secure/multi-factor-authentication) <br>
- [Step-Up Authentication](https://auth0.com/docs/secure/multi-factor-authentication/step-up-authentication) <br>
- [MFA API](https://auth0.com/docs/secure/multi-factor-authentication/manage-mfa-auth0-apis) <br>
- [Authorization Code Flow request parameters](https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow/add-login-auth-code-flow#request-parameters) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets and Auth0 CLI/API commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Auth0 CLI for command-based tenant configuration; examples include frontend, backend, and Auth0 Action patterns.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
