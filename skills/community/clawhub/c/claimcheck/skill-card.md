## Description:

Sanitize PII/secrets (FEIN, SSN, names, credentials) from text or files with the local ClaimCheck CLI before anything leaves the machine; reversible via the local encrypted vault.

This skill is ready for commercial/non-commercial use.

## Publisher:

[normandmickey](https://clawhub.ai/user/normandmickey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use ClaimCheck to replace sensitive values in client-adjacent text and files with reversible placeholders before sharing them with an AI provider, then restore values locally when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release may overstate which traffic is protected and when stored secrets are encrypted.

Mitigation: Pin and review the release, set SANITIZE_VAULT_PASSWORD on Linux or macOS, and confirm the client is using the scrubbed endpoint.

Risk: Sanitized output may still contain sensitive values.

Mitigation: Inspect sanitized output before sharing sensitive material, especially for high-stakes use.

Risk: Installation may configure a startup service or logon task that keeps running continuously.

Mitigation: Review the disclosed startup service or logon task and its behavior before installation.

## Reference(s):

- [ClaimCheck homepage](https://claimcheck.saasclaw.ai)
- [ClaimCheck source repository](https://github.com/saasclawai-org/ClaimCheck)
- [ClaimCheck ClawHub release](https://clawhub.ai/normandmickey/skills/claimcheck)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, JSON]

**Output Format:** [Text and JSON produced by the ClaimCheck CLI, with shell commands and configuration guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sanitized values use stable placeholders; the local vault supports restoration.]

## Skill Version(s):

1.1.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
