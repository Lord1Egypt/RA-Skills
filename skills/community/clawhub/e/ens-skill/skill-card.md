## Description:

Resolve ENS names (.eth) to Ethereum addresses and vice versa, including ENS profile lookup and guidance for registering, renewing, or managing .eth names.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fabriziogianni7](https://clawhub.ai/user/fabriziogianni7)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to resolve ENS names and Ethereum addresses, inspect ENS profile records, and receive guided steps for registering, renewing, or managing .eth names on Ethereum mainnet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ENS name and wallet lookups may disclose user activity to third-party services.

Mitigation: Review third-party lookup use before installation and disclose or restrict lookup behavior where privacy expectations require it.

Risk: Stored ENS identity data may persist in user strategy or memory.

Mitigation: Require explicit approval before storing ENS names, preferences, profile details, or transaction narratives.

Risk: The raw Node.js fallback command can be unsafe with untrusted ENS names.

Mitigation: Use a fixed script or argument-based resolver instead of interpolating untrusted names into a node -e command.

Risk: ENS-changing transactions can affect ownership, renewals, or profile records.

Mitigation: Require explicit user approval and show the resolved address, chain, contract action, cost, and target name before any transaction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fabriziogianni7/skills/ens-skill)
- [ENS documentation](https://docs.ens.domains/)
- [ENS Manager App](https://ens.app/myname.eth)
- [web3.bio profile API](https://api.web3.bio/profile/vitalik.eth)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON examples, and transaction guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ENS names, Ethereum addresses, profile fields, contract addresses, registration or renewal steps, and user-specific storage guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
