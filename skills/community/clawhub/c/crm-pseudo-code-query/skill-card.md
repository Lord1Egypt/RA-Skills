## Description:

Queries Tonghuashun CRM for pseudo-code values tied to supplied user IDs using mTLS certificate authentication and batch CRM detail-page retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenmiley](https://clawhub.ai/user/chenmiley)

### License/Terms of Use:

MIT-0

## Use Case:

Authorized CRM operators use this skill to prepare certificate-based login steps and batch query pseudo-code values for supplied CRM user IDs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles CRM credentials and client certificate private keys in unsafe, overbroad ways.

Mitigation: Use only with authorization and replace the workflow so it does not export all Keychain identities, write private keys or cookies to predictable /tmp files, pass passwords on command lines or URLs, or disable TLS verification.

## Reference(s):

- [CRM authentication flow](references/auth_flow.md)
- [ClawHub skill page](https://clawhub.ai/chenmiley/skills/crm-pseudo-code-query)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and Python script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied CRM credentials, mTLS certificate material, and CRM user IDs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
