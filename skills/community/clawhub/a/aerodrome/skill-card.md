## Description:

Use when creating, validating, backtesting, deploying, sizing, or troubleshooting Aerodrome/Base spot trading strategies through the Superior Trade API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superior-ai](https://clawhub.ai/user/superior-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading operators use this skill to build, validate, backtest, size, deploy, and troubleshoot Aerodrome spot AMM trading strategies on Base through Superior Trade. It focuses on Freqtrade-compatible configuration, strategy code, API workflows, wallet balance checks, and live deployment confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live deployment can trade with real funds through Superior Trade.

Mitigation: Require an explicit user confirmation before starting live trading, and review the strategy, stake size, wallet balances, gas balance, and deployment summary first.

Risk: Incorrect sizing or missing wallet balances can cause failed swaps or unintended balance exhaustion.

Mitigation: Check quote token, base token, and Base ETH gas balances before deployment, and size stake_amount times max_open_trades below available free balance with room for slippage, token fees, and gas.

Risk: Aerodrome is an AMM spot venue, so order-book, leverage, futures, margin, or shorting assumptions can produce invalid or unsafe configurations.

Mitigation: Use spot-only market orders, disable order-book pricing, avoid order-book API calls, and omit margin, leverage, futures, and short-entry fields.

Risk: The skill uses SUPERIOR_TRADE_API_KEY for external API access.

Mitigation: Load the API key from the environment and do not paste credentials, wallet private keys, or platform-injected exchange credentials into commands, files, or logs.

## Reference(s):

- [ClawHub Aerodrome Skill Page](https://clawhub.ai/superior-ai/skills/aerodrome)
- [Superior Trade API](https://api.superior.trade)
- [Base Mainnet RPC](https://mainnet.base.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown with JSON, Python, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Freqtrade strategy snippets, Aerodrome configuration, Superior Trade API commands, backtest result summaries, and live deployment checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
