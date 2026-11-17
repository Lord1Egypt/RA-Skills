## Description:

Binance Pro helps agents work with Binance account and market operations, including balances, prices, futures positions, spot and futures orders, stop-loss and take-profit orders, and PnL checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hybrid1labs](https://clawhub.ai/user/hybrid1labs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through Binance account queries and trading workflows. It is intended for users who intentionally want an agent-accessible Binance helper for balances, positions, prices, orders, stop-loss and take-profit operations, and related portfolio tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute real Binance spot and futures trading actions, including leveraged orders and position changes.

Mitigation: Use a dedicated Binance API key with withdrawals disabled, minimal permissions, IP restrictions, and explicit confirmation or dry-run safeguards before allowing funded trading actions.

Risk: The skill asks users to provide powerful Binance API credentials through environment variables or a local credentials file.

Mitigation: Store credentials securely, restrict file permissions, avoid sharing keys in prompts or logs, and rotate keys if they may have been exposed.

Risk: Incorrect symbols, quantities, leverage, or stop prices can create unintended financial exposure.

Mitigation: Review symbol, side, quantity, leverage, and risk controls before execution, and test workflows on Binance Testnet before using real funds.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hybrid1labs/skills/binance-pro-hybrid)
- [Binance API Documentation](https://binance-docs.github.io/apidocs/)
- [Binance Testnet](https://testnet.binance.vision/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and an accompanying Python CLI script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Binance API credentials. Documented shell examples require curl and jq; the Python CLI uses Binance REST API endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
