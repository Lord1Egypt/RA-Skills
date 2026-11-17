## Description:

Complete a consent-preserving auth.md USER-CLAIMED signup OTP flow against any service that publishes the auth.md protocol, with the human confirming the OTP and the agent never auto-confirming.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webface](https://clawhub.ai/user/webface)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent complete consent-preserving auth.md user-claimed signup flows, including NoForm reference flows and compatible services that publish auth.md metadata. The skill guides discovery, anonymous registration, email OTP confirmation, scoped token storage, and token revocation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional persistent token storage can save active bearer tokens and email addresses without mandatory local file protections.

Mitigation: Leave AUTH_MD_TOKEN_STORE unset for session-only storage, or use a private file or secret store with strict permissions and revoke tokens if the file may have been exposed.

Risk: Signup binds an account to a human email address and can create scoped service credentials.

Mitigation: Require explicit user consent before registration, collect the email in-channel from the user, and wait for the user to provide the OTP before completing the claim.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/webface/skills/auth-md-signup)
- [Publisher profile](https://clawhub.ai/user/webface)
- [NoForm](https://noform.dev)
- [auth.md overview](https://workos.com/auth-md)
- [auth.md protocol](https://github.com/workos/auth.md)
- [OAuth 2.0 Protected Resource Metadata](https://datatracker.ietf.org/doc/html/rfc9728)
- [WorkOS auth.md docs](https://workos.com/auth-md/docs)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires human confirmation for consent and OTP completion; may use AUTH_MD_TOKEN_STORE for optional persistent scoped token storage.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
