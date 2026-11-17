## Description:

Scores a public crypto wallet's on-chain activity across Ethereum, Arbitrum, Base, Optimism, and Polygon using public JSON-RPC endpoints and returns a heuristic airdrop farming health score for single-wallet or multi-wallet comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to check whether public wallet addresses have enough multi-chain EVM activity to look active under common retroactive airdrop heuristics. It supports quick single-wallet scoring and side-by-side comparison of multiple wallets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public wallet addresses are sent to publicnode.com RPC endpoints during analysis.

Mitigation: Install and run the skill only when sharing public wallet addresses with those RPC endpoints is acceptable.

Risk: The score can be mistaken for a real airdrop eligibility prediction.

Mitigation: Treat the result as a rough activity indicator and verify project-specific criteria separately before making decisions.

Risk: The implementation does not verify account age, activity recency, bridge use, distinct contract interactions, social requirements, governance activity, or Sybil filters.

Mitigation: Use the output as one input in a broader review of wallet behavior and project rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssidharhubble/skills/airdrop-eligibility-tracker)
- [Ethereum public JSON-RPC endpoint](https://ethereum-rpc.publicnode.com)
- [Arbitrum One public JSON-RPC endpoint](https://arbitrum-one-rpc.publicnode.com)
- [Base public JSON-RPC endpoint](https://base-rpc.publicnode.com)
- [Optimism public JSON-RPC endpoint](https://optimism-rpc.publicnode.com)
- [Polygon public JSON-RPC endpoint](https://polygon-bor-rpc.publicnode.com)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Plain-text report or JSON from a command-line script, with Markdown usage guidance in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only wallet analysis; requires outbound HTTPS access to publicnode.com RPC endpoints and public wallet addresses only.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
