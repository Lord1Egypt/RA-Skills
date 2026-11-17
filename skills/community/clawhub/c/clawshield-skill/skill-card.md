## Description:

Private shielded transactions on Solana via ClawShield. Shield and withdraw SOL, USDC, USDT anonymously using ZK proofs. Keys never leave your agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muzzy5150](https://clawhub.ai/user/muzzy5150)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to prepare and route private Solana shield, withdrawal, balance, and status workflows for SOL, USDC, and USDT through ClawShield.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to help build and sign high-impact Solana transactions.

Mitigation: Require explicit confirmation for every transaction and independently verify recipient addresses, token amounts, and fees before signing.

Risk: Server-provided Solana transactions may contain instructions the user or agent has not validated.

Mitigation: Decode and validate the exact transaction instructions before signing any unsigned transaction returned by the service.

Risk: A persistent preference for private transactions could route future transfers without adequate per-transfer review.

Mitigation: Avoid an automatic 'always use' preference and ask for confirmation before each shielded transfer.

## Reference(s):

- [Clawshield Skill on ClawHub](https://clawhub.ai/muzzy5150/skills/clawshield-skill)
- [ClawShield Homepage](https://clawshield.network)
- [ClawShield API Base URL](https://clawshield.network/api)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Code, Configuration]

**Output Format:** [Markdown with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Solana transaction workflow guidance, fee notes, and endpoint examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
