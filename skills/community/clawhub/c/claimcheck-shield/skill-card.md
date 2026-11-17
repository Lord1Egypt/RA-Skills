## Description:

ClaimCheck detects and replaces sensitive values with reversible placeholders and supports local vault restoration; its documentation also describes a proxy that forwards sanitized requests and API authentication to an external provider.

This skill is ready for commercial/non-commercial use.

## Publisher:

[normandmickey](https://clawhub.ai/user/normandmickey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use ClaimCheck to identify and pseudonymize credentials and personal data before sharing project text with an LLM, then restore placeholders locally when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local-only privacy promises conflict with proxy instructions that forward requests and API authentication to an external provider; missed sensitive values may also leave the machine.

Mitigation: Choose the intended provider and matching credentials, inspect sanitized output, and verify the external release before enabling the Windows startup task.

## Reference(s):

- [ClaimCheck on ClawHub](https://clawhub.ai/normandmickey/skills/claimcheck-shield)
- [ClaimCheck website](https://claimcheck.saasclaw.ai)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Guidance]

**Output Format:** [JSON summaries and findings, sanitized text or file content, and restored file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sensitive values are replaced with reversible placeholders; restoration uses the local vault. Verify sanitized output before high-stakes sharing.]

## Skill Version(s):

1.1.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
