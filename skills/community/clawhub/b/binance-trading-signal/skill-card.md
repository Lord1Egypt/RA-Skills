## Description:

Subscribe to and retrieve on-chain Smart Money trading signals, including buy/sell activity, trigger price, current price, max gain, and exit rate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viktor-huang](https://clawhub.ai/user/viktor-huang)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to fetch Binance Web3 on-chain Smart Money trading signals for BSC and Solana. It supports monitoring token activity, signal direction, pricing context, and historical performance indicators for informational trading analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading signals are speculative, time-sensitive, and may be incomplete or stale.

Mitigation: Treat outputs as informational only, confirm prices and signal status independently, and avoid relying on this skill alone for trading decisions.

Risk: Users may mistake summarized signal data for financial advice.

Mitigation: Present signal summaries with clear caveats and encourage independent due diligence before any investment action.

## Reference(s):

- [Binance Web3 Smart Money Signal API Endpoint](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/web/signal/smart-money)
- [ClawHub Skill Page](https://clawhub.ai/viktor-huang/skills/binance-trading-signal)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with optional curl examples and summarized JSON signal data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are informational, time-sensitive, and depend on live public trading-signal data.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
