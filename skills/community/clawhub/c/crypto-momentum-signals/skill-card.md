## Description:

Provides pay-per-request momentum metrics for CoinGecko-listed cryptocurrencies, including moving-average trend, RSI, volatility, and price changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perria080925-bot](https://clawhub.ai/user/perria080925-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users can screen cryptocurrencies for momentum and add quantitative context to market commentary. Each data request incurs a USDC payment and should be approved before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to make x402 USDC payments without requiring explicit approval or a spending cap.

Mitigation: Before payment, show and obtain approval for the exact amount, asset, network, recipient, endpoint, and request count; set a spending cap for multi-coin screening.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/perria080925-bot/skills/crypto-momentum-signals)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Text or Markdown with momentum metrics and source citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-coin market snapshot; underlying lookup costs $0.0005 USDC per request.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
