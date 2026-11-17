## Description:

Guides token swaps through Chord on eight EVM networks and Solana with token checks, route quotes, user confirmation, and wallet-signed transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuantqse90](https://clawhub.ai/user/tuantqse90)

### License/Terms of Use:

MIT-0

## Use Case:

People using an AI agent to compare token swap routes, review token checks and estimated costs, and prepare transactions for their own wallet to sign on supported EVM networks or Solana.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Solana flow sends wallet-signed transactions through Chord, despite the skill's claim that it only prepares unsigned transactions and never moves funds.

Mitigation: Review before installing; disclose the relay step and require explicit user control, or omit it and have users broadcast signed transactions through their own wallet.

## Reference(s):

- [ClawHub release](https://clawhub.ai/tuantqse90/skills/chord-swap)
- [Chord documentation](https://getchord.xyz/docs)
- [Solana swap flow](references/solana.md)
- [Errors and warnings](references/errors.md)
- [Swap examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Transaction data]

**Output Format:** [Markdown with swap summaries and transaction details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [EVM swaps provide unsigned transaction and approval details; the Solana flow can send a wallet-signed transaction through Chord.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
