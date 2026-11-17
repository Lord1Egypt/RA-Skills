## Description:

Review a public GitHub repository or a code snippet for security and quality issues, through AIProx (aiprox.dev): one POST /api/orchestrate with capability code-execution, 50 sats, paid in Bitcoin Lightning (L402 or a LightningProx spend token). Returns findings with severities, a score and a summary. Use it when the user asks to audit specific code and agrees to pay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to request a paid security and quality review of a public repository or code snippet. It returns findings with severity labels, a score, and a summary for the agent to present and discuss.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted task text and code are sent to AIProx and its model provider; remote retention and service behavior are not established by this artifact review.

Mitigation: Submit only code the user may share, exclude secrets and personal data, and review the provider's privacy terms.

Risk: Each audit costs 50 sats, and an optional spend token is a bearer credential.

Mitigation: Get user approval before a paid call, keep the token minimally funded, never expose or log it, and limit each request to one call.

## Reference(s):

- [AIProx](https://aiprox.dev)
- [AIProx documentation](https://aiprox.dev/docs.html)

## Skill Output:

**Output Type(s):** [Analysis, Text]

**Output Format:** [Audit findings with severity labels, a 1–10 score, and a summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One code source per call; each paid call costs 50 sats.]

## Skill Version(s):

2.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
