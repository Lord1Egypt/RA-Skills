## Description: <br>
Complete an auth.md USER-CLAIMED signup (OTP flow) against any service that publishes the auth.md protocol, with the human confirming the OTP instead of the agent auto-confirming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[webface](https://clawhub.ai/user/webface) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent complete consent-preserving auth.md user-claimed signup, obtain a scoped service credential, store it for later use, and revoke it when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles scoped service tokens and can persist them when AUTH_MD_TOKEN_STORE is configured. <br>
Mitigation: Use persistent token storage only when acceptable for the deployment, keep the token store protected, and rely on session-only storage when persistence is not needed. <br>
Risk: The signup flow asks the user for an email address and OTP to bind an account. <br>
Mitigation: Require explicit user confirmation before registration, never auto-confirm the OTP, and stop when the human is not present to provide the code. <br>
Risk: The skill follows service-published auth.md metadata and posts to discovered endpoints. <br>
Mitigation: Validate fetched endpoints against the expected service domain or NoForm host before posting claim data or credentials. <br>


## Reference(s): <br>
- [NoForm homepage](https://noform.dev) <br>
- [auth.md protocol overview](https://workos.com/auth-md) <br>
- [auth.md specification](https://github.com/workos/auth.md) <br>
- [OAuth 2.0 Protected Resource Metadata (RFC 9728)](https://datatracker.ietf.org/doc/html/rfc9728) <br>
- [WorkOS auth.md documentation](https://workos.com/auth-md/docs) <br>
- [ClawHub skill page](https://clawhub.ai/webface/auth-md-signup) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request user email and OTP in-channel; may persist scoped service tokens when AUTH_MD_TOKEN_STORE is configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
