## Description:

Track BTC self-custody metrics - COLDCARD Q vault health, mempool fee estimation, UTXO management, and on-chain verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1beekeeper](https://clawhub.ai/user/1beekeeper)

### License/Terms of Use:

MIT-0

## Use Case:

Bitcoin self-custody users and operators use this skill to check watch-only wallet balances, current fee conditions, UTXO health, chain tip status, and COLDCARD Q vault status without handling private keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A documented UTXO command uses a misspelled lookalike domain and could disclose a watch-only Bitcoin address to an unintended third party.

Mitigation: Correct the endpoint to mempool.space or use a configured local node, Electrum server, or self-hosted mempool API before checking real addresses.

Risk: Public fee, balance, and price APIs can reveal address-monitoring behavior or become unavailable due to rate limits.

Mitigation: Prefer local or self-hosted services for sensitive address checks, and review external API use before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1beekeeper/skills/btc-sovereign-tracker)
- [Publisher profile](https://clawhub.ai/user/1beekeeper)
- [ZK-Bankir project homepage](https://gitlab.com/1Beekeeper/zk-bankir)
- [mempool.space fee API](https://mempool.space/api/v1/fees/recommended)
- [CoinGecko simple price API](https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,eur,sek)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only guidance that may call public blockchain, fee, price, or configured local vault-status APIs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
