## Description:

Core trading skill for AION Market prediction market agents, covering setup, wallet binding, market search, pre-trade checks, risk-aware trading, order management, position monitoring, and settlement workflows on Polymarket and Kalshi via aion-sdk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssj124](https://clawhub.ai/user/ssj124)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to configure AION Market trading agents, connect wallets, inspect prediction markets, submit or cancel Polymarket and Kalshi orders, monitor positions, redeem settlements, and manage post-trade fee workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real-money prediction-market automation can approve spend, place trades, charge fees, or transfer funds with too much default authority.

Mitigation: Use a limited wallet, set strict allowance and trade caps, pause trading until limits are configured, and require explicit confirmation for every approval, trade, and fee transfer.

Risk: Wallet private keys, API keys, derived CLOB credentials, and Solana keys can expose user funds if logged, committed, or reused broadly.

Mitigation: Keep secrets in environment variables or an uncommitted .env file, avoid printing credentials, use pinned dependencies, and prefer a separate signer or hardware wallet for live trading.

Risk: Ambiguous SDK or venue responses can cause the agent to misreport whether an order, cancellation, settlement, or fee transfer succeeded.

Mitigation: Verify ambiguous outcomes through venue-specific order, trade, position, or transaction state before retrying or reporting final status.

## Reference(s):

- [AION Market documentation](https://docs.aionmarket.com/)
- [AION Market homepage](https://www.aionmarket.com/)
- [ClawHub skill page](https://clawhub.ai/ssj124/skills/aionmarket-trading)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides authenticated SDK calls and wallet-dependent trading workflows; it does not itself produce market predictions or strategy signals.]

## Skill Version(s):

1.0.7 (source: server release metadata; artifact metadata.version is 0.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
