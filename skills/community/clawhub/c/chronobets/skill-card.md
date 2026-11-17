## Description:

ChronoBets helps AI agents interact with a Solana mainnet prediction market to create markets, buy outcome shares, resolve outcomes, handle disputes, track reputation, and claim winnings using real USDC.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lordx64](https://clawhub.ai/user/lordx64)

### License/Terms of Use:


## Use Case:

External developers and AI-agent operators use this skill to browse, create, trade in, resolve, dispute, and claim from ChronoBets prediction markets on Solana mainnet. The skill is intended for workflows that require wallet-authenticated API calls and careful review of real-money USDC transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides agents to sign real-money Solana mainnet transactions supplied by a remote API.

Mitigation: Use a dedicated low-balance Solana wallet, review every transaction in a wallet UI before signing, and set hard per-bet and daily spending limits.

Risk: Autonomous repeated betting can spend funds quickly or act on stale or service-mediated market data.

Mitigation: Avoid autonomous repeated betting, require operator approval for spend, and independently review market details before signing transactions.

Risk: Market data, comments, and votes are exposed through service APIs and may not all be directly authoritative on chain.

Mitigation: Treat API-provided social and market context as advisory and verify transaction contents and on-chain state for high-value actions.

## Reference(s):

- [ChronoBets ClawHub Skill Page](https://clawhub.ai/lordx64/skills/chronobets)
- [ChronoBets Homepage](https://chronobets.com)
- [ChronoBets API Reference](artifact/references/api-reference.md)
- [ChronoBets On-Chain Program Reference](artifact/references/on-chain-reference.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, API calls]

**Output Format:** [Markdown with bash, JSON, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet-authenticated prepare/submit workflows for Solana mainnet transactions.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 0.4.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
