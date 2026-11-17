## Description:

AirnodeHub crypto skill to explain public wallet balances, history, NFTs, and live token prices via attested dRPC/CoinGecko POST reads; never request keys or transact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metobom](https://clawhub.ai/user/metobom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request read-only explanations of public crypto wallet balances, transaction history, NFTs, and token prices. It helps agents keep wallet analysis privacy-conscious, scoped to documented POST lookups, and clear about uncertainty.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public wallet addresses and lookup parameters may be sent to the named dRPC and CoinGecko proxy services.

Mitigation: Minimize repetition of public addresses, do not persist them, and disclose the lookup scope before using third-party services.

Risk: Users may provide secrets, signatures, wallet connection approvals, or transaction approvals that are outside the skill's read-only purpose.

Mitigation: Reject seed phrases, private keys, signatures, wallet connections, and transaction approvals; keep all activity strictly informational and read-only.

Risk: Wallet and pricing results can be affected by spam tokens, unpriced assets, stale metadata, indexing gaps, pagination limits, unsupported chains, and valuation volatility.

Mitigation: Separate facts from interpretation, state currency and timestamp, disclose coverage limits, and avoid financial, legal, tax, ownership, identity, or intent conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/metobom/skills/crypto-wallet-explainer)
- [Airnode dRPC documentation](https://airnode-drpc.fly.dev/)
- [Airnode CoinGecko documentation](https://airnode-coingecko.fly.dev/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown text with concise wallet analysis, documented read-only lookup guidance, timestamps, limitations, and informational disclaimers.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize public wallet balances, transaction history, NFTs, token prices, data provenance, unsupported chains, stale metadata, unpriced assets, and volatility caveats.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
