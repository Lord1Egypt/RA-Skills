## Description:

Automates Binance USDS-M Futures trading with market analysis, technical indicators, dynamic risk management, and order execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kritsanan1](https://clawhub.ai/user/kritsanan1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading operators use this agent to connect to Binance USDS-M Futures, compute SMA, RSI, and MACD trading signals, and submit futures orders with configured leverage and position sizing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can operate as live automated leveraged-trading software without adequate live-trading guardrails.

Mitigation: Keep it on Binance Testnet or add a real dry-run gate, require explicit approval before order placement or leverage changes, and connect production credentials only after enforced stop-loss and position-size limits are in place.

Risk: Runtime authority is broader than the trading workflow needs.

Mitigation: Remove unrestricted shell access and run the agent with only the narrow tool and network permissions required for reviewed Binance API operations.

Risk: Trading credentials and account access can create financial loss if exposed or misconfigured.

Mitigation: Use environment variables or a secret manager for API keys, avoid storing secrets in source files, and verify testnet mode before any production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kritsanan1/skills/binance-trading-agent-openclaw-3)
- [Publisher Profile](https://clawhub.ai/user/kritsanan1)
- [Server-Resolved Source Repository](https://github.com/kritsanan1/binance-trading-agent-openclaw)
- [Server-Resolved Source Commit](https://github.com/kritsanan1/binance-trading-agent-openclaw/commit/e389c65c9763a00183befae24bcd9cf707c218f5)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, API calls]

**Output Format:** [Python modules, JSON configuration, shell commands, and runtime log text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit Binance Futures orders when configured with credentials; testnet is enabled by default in the artifact configuration.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
