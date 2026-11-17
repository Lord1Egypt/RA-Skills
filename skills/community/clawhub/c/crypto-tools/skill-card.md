## Description:

Access crypto data, monitor portfolios, detect scams, and navigate exchanges with real-time APIs and security tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers, analysts, and external users use this skill for cryptocurrency price lookups, portfolio calculations, exchange and on-chain data gathering, and scam-risk checks. It provides informational guidance and examples without making investment, legal, or tax recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake market, portfolio, or token-safety information for financial advice.

Mitigation: Keep responses informational, include the supplied investment disclaimer when relevant, avoid buy/sell/hold recommendations, and direct users to qualified professionals for personal decisions.

Risk: Wallet-transfer or dApp-interaction guidance can contribute to irreversible asset loss if automated or followed without review.

Mitigation: Do not let an agent execute wallet transfers automatically; require user review of addresses, chains, approvals, and transaction details before any action.

Risk: Tax and legal examples may be too generic for a user's jurisdiction or situation.

Mitigation: Present exports, formulas, and cost-basis examples as preparation aids only and recommend qualified tax or legal review for personal filings.

Risk: Public API data can be incomplete, rate-limited, stale, or unavailable.

Mitigation: Prefer official APIs, cite the data source and timestamp when possible, cache or retry within documented limits, and avoid presenting a single source as definitive.

## Reference(s):

- [Crypto Data Sources](artifact/sources.md)
- [Crypto Security & Scam Detection](artifact/security.md)
- [Crypto Utilities & Calculations](artifact/tools.md)
- [CoinGecko API price endpoint](https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd,eur)
- [CoinGecko market chart endpoint](https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=30)
- [DefiLlama protocols endpoint](https://api.llama.fi/protocols)
- [DefiLlama yields endpoint](https://yields.llama.fi/pools)
- [Etherscan gas oracle endpoint](https://api.etherscan.io/api?module=gastracker&action=gasoracle)
- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/crypto-tools)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with API endpoints, inline shell commands, code snippets, formulas, checklists, and CSV examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Informational crypto reference only; may rely on public data APIs and user-provided wallet or transaction context.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
