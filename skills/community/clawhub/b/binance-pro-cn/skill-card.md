## Description:

Binance Pro Cn provides Binance integration guidance for spot and futures trading, leverage, staking, balances, prices, open orders, cancellations, and trade history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate Binance API credential setup guidance and command examples for market data, account reads, spot orders, futures orders, leverage changes, and order management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use Binance API keys for live account reads and trade execution.

Mitigation: Use a dedicated, least-privilege Binance API key with withdrawals disabled, restrict source IPs where possible, and protect credential files with restrictive permissions.

Risk: The skill includes commands for spot orders, futures orders, leverage changes, and cancellations.

Mitigation: Prefer Binance testnet first and require explicit confirmation before every order, leverage change, or cancellation.

Risk: Security evidence flags broad triggers and weak safeguards for market-trading commands.

Mitigation: Review prompts and generated commands before deployment, and constrain activation to intentional Binance trading requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/guohongbin-git/skills/binance-pro-cn)
- [OpenClaw Metadata Source](https://clawhub.ai)
- [Binance API Documentation](https://binance-docs.github.io/apidocs/)
- [Binance Testnet](https://testnet.binance.vision/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes executable Binance API command examples that may read live account data or submit trading actions when populated with valid credentials.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
