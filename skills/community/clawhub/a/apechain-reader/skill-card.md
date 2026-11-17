## Description:

Apechain Reader helps agents analyze EVM wallet addresses, smart contracts, transaction history, NFT holdings, and bot-like behavior across ApeChain and other supported chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luigi08001](https://clawhub.ai/user/luigi08001)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and agents use this skill to inspect public on-chain wallet and contract data, summarize NFT and transfer activity, and triage bot-like account behavior. Bot scores are heuristic signals for review and should not be treated as proof.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses, chain choices, and contract addresses are sent to public RPC services, CoinGecko, and optionally Alchemy.

Mitigation: Use only public or approved investigation targets, avoid private keys or seed phrases, and choose trusted RPC providers for sensitive workflows.

Risk: Bot detection results are heuristic and can misclassify accounts.

Mitigation: Treat scores as review cues, not as proof or the sole basis for financial, moderation, or access decisions.

Risk: ENS support is advertised in documentation but is unavailable in the inspected code.

Mitigation: Use hexadecimal wallet addresses until ENS resolution is implemented and verified.

## Reference(s):

- [Chain Details](references/CHAINS.md)
- [Bot Detection Scoring](references/bot-scoring.md)
- [Apechain Reader on ClawHub](https://clawhub.ai/luigi08001/skills/apechain-reader)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [JSON from scripts by default, with optional human-readable text summaries in pretty mode.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js v16+ and sends lookup inputs to public RPC services, CoinGecko, and optionally Alchemy.]

## Skill Version(s):

3.1.0 (source: server release evidence and target metadata; package.json declares 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
