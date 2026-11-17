## Description:

Verification-first helper for proof checks and optional 0 ETH Base claim submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alphac007](https://clawhub.ai/user/alphac007)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to verify proof status, prepare an AAP claim payload, and optionally submit a user-confirmed 0 ETH proof transaction on Base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An on-chain proof transaction can publish proof data and incur Base gas costs.

Mitigation: Broadcast only when confirm_broadcast is true, show the exact transaction command first, and confirm the target wallet and 0 ETH value before execution.

Risk: Credential or signer context may be unavailable or unsafe if raw key material is requested.

Mitigation: Use user-managed GitHub auth or a least-privilege GH_TOKEN and user-managed cast signer context; never request raw private keys, seed phrases, or mnemonics.

## Reference(s):

- [AAP Agent Bounty Skill Page](https://clawhub.ai/alphac007/skills/aap-agent-bounty)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON status output and shell commands for user review]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only output; transaction broadcast remains pending unless confirm_broadcast is true.]

## Skill Version(s):

1.0.10 (source: package.json, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
