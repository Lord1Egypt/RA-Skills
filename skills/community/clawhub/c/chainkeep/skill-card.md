## Description:

Store a file permanently onchain with ChainKeep and read it back, encrypted by default. Pay over x402 in USDC (signatures only, no gas) or in the chain's native coin. Use when the user asks to back up, archive or permanently keep a file or an agent's memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[web3senior](https://clawhub.ai/user/web3senior)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use ChainKeep to back up or archive files and agent memory permanently onchain, then retrieve and verify stored content when needed. The skill guides users through encrypted-by-default storage and payment approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploads are paid and permanent, and public files and their name and type metadata can be read by anyone.

Mitigation: Upload only content intended for permanent storage; use encryption by default and choose public storage only when explicitly intended.

Risk: Wallet credentials and recovery keys could be exposed or misused.

Mitigation: Review and pin the CLI version before providing secrets, use a minimally funded dedicated wallet, keep keys out of command history and logs, and store recovery keys securely.

Risk: An upload can incur unexpected payment if the amount is not reviewed first.

Mitigation: Show the quote and obtain explicit user approval before payment; never exceed the approved amount.

## Reference(s):

- [ChainKeep Documentation](https://chainkeep.online/docs)
- [ChainKeep ClawHub Release](https://clawhub.ai/web3senior/skills/chainkeep)

## Skill Output:

**Output Type(s):** [Shell commands, Files, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands; CLI responses in JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid storage is permanent; retrieving encrypted content requires its recovery key.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
