## Description:

Query Bitcoin (BTC L1) blockchain data with USD pricing, including wallet balances, address information, transaction details, UTXO analysis, fee estimation, mempool statistics, and live network health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bronoman](https://clawhub.ai/user/bronoman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to retrieve read-only Bitcoin address, transaction, fee, mempool, block, network, and price data for dashboards, monitoring, research, and operational context. It does not execute transactions, access wallets, or provide financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet or address lookups can expose query metadata to the configured Bitcoin API provider.

Mitigation: Review before installing for wallet-query privacy, and use the default endpoint or a trusted HTTPS BITCOIN_API_URL.

Risk: An optional CoinGecko API key may be exposed through under-scoped network behavior.

Mitigation: Avoid setting COINGECKO_API_KEY for this skill until key handling is fixed.

Risk: Live blockchain, fee, and price data may be stale, unavailable, or rate-limited by third-party services.

Mitigation: Treat returned data as point-in-time context and verify independently before financial or operational decisions.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/bronoman/hermes/tree/main/skills/bitcoin)
- [ClawHub skill page](https://clawhub.ai/bronoman/skills/bitcoin-2)
- [Mempool.space REST API documentation](https://mempool.space/docs/api/rest)
- [Mempool.space API endpoint](https://mempool.space/api)
- [CoinGecko simple price API](https://api.coingecko.com/api/v3/simple/price)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text and Markdown guidance with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only live network lookups; outputs depend on Mempool.space, CoinGecko, and any configured BITCOIN_API_URL.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
