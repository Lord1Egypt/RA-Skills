## Description:

Trade stocks and crypto via Alpaca API. Use for market data (quotes, bars, news), placing orders (market, limit, stop), checking positions, portfolio management, and account info. Supports both paper and live trading. Use when user asks about stock prices, wants to buy/sell securities, check portfolio, or manage trades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vamzi](https://clawhub.ai/user/vamzi)

### License/Terms of Use:


## Use Case:

External developers and agent users use this skill to retrieve Alpaca market data, inspect account and portfolio state, and prepare or execute stock and crypto trading actions through Alpaca. It is suitable for paper trading workflows and can affect live accounts when live credentials are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place or cancel live financial orders, and confirmation behavior may be bypassed or incomplete.

Mitigation: Prefer paper trading, avoid --force in live mode, and require explicit review and confirmation of every generated order or cancel command.

Risk: Alpaca credentials grant trading account access if exposed or stored insecurely.

Mitigation: Store ~/.openclaw/credentials/alpaca.json with restrictive permissions and use environment or account controls appropriate for the deployment.

Risk: The skill depends on alpaca-py for account, market data, order, and streaming actions.

Mitigation: Install alpaca-py only from a trusted, reviewed version before enabling the skill.

## Reference(s):

- [Alpaca API Reference](references/api.md)
- [Alpaca Paper Trading API](https://paper-api.alpaca.markets)
- [Alpaca Live Trading API](https://api.alpaca.markets)
- [Alpaca Market Data API](https://data.alpaca.markets)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration snippets, and concise trading guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Alpaca CLI commands, API response interpretation, order guardrail guidance, and credential setup instructions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
