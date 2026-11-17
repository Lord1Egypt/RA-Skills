## Description:

Handle Google OAuth login, account linking, and session bootstrap for A2A market users and operators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luoqianchenguni-max](https://clawhub.ai/user/luoqianchenguni-max)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement Google OAuth authorization-code login, account linking, callback validation, and secure session bootstrap for A2A market users and operators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth runtime code referenced by the artifact may differ from the guidance in the skill.

Mitigation: Review the separate runtime implementation before production use and confirm it hashes, rotates, and scopes refresh tokens as described.

Risk: Incorrect state, nonce, issuer, or audience handling can weaken OAuth callback verification.

Mitigation: Validate state and nonce against server-side storage, reject mismatched issuer or audience values, and test callback failure paths before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with endpoint contracts, code paths, and security requirements]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
