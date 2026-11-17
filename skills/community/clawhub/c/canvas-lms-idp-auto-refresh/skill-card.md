## Description:

Automatically refreshes Canvas LMS API tokens through institutional CAS/SAML IDP login with RSA-encrypted credentials and optional old-token cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[summers-tars](https://clawhub.ai/user/summers-tars)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents that integrate with Canvas LMS use this skill to recover from expired API tokens by running an institutional SSO login flow, creating a fresh token, and optionally cleaning up older purpose-matched tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles institutional login credentials and Canvas API tokens.

Mitigation: Use it only in an isolated local environment and avoid storing institutional passwords in plaintext where possible.

Risk: Debug artifacts may contain sensitive session data or diagnostic material.

Mitigation: Keep debug output opt-in, redacted, owner-only, and cleaned up; do not share debug_output.

Risk: Old-token cleanup can delete Canvas tokens that match the configured purpose.

Mitigation: Use cleanup dry-run or avoid cleanup until deletion behavior and token-purpose matching are confirmed.

## Reference(s):

- [IDP Adaptation Guide](artifact/references/idp-adaptation.md)
- [ClawHub Skill Page](https://clawhub.ai/summers-tars/skills/canvas-lms-idp-auto-refresh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit a NEW_TOKEN value when the bundled token refresh script succeeds.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
