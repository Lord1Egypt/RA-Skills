## Description:

Safety-first Bitcoin and crypto trading on Bitstamp via CLI for checking crypto prices, viewing account balances, placing buy or sell orders, managing open orders, checking trade history, and monitoring Bitstamp markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhen08](https://clawhub.ai/user/zhen08)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to operate a Bitstamp trading CLI that retrieves market and account data, simulates trades by default, and can place live spot orders only when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real Bitstamp trades with the user's API key.

Mitigation: Run dry-run commands first, require explicit live execution and confirmation, and use trade-only API keys with withdrawals disabled and IP allowlisting enabled.

Risk: The security review reports material weaknesses in the daily cap, kill switch, cancellation reporting, and numeric validation controls.

Mitigation: Do not rely on the built-in guardrails alone; keep conservative limits, monitor account state directly, and fix or review those controls before using live trading.

Risk: The skill depends on CCXT and external Bitstamp API behavior for account and order operations.

Mitigation: Pin and review the ccxt dependency, test public and account-read commands before live trading, and verify Bitstamp responses before acting on them.

## Reference(s):

- [Bitstamp Trader Skill Page](https://clawhub.ai/zhen08/skills/bitstamp-trader)
- [Bitstamp API Reference](references/api-reference.md)
- [Safety Architecture](references/safety.md)
- [Bitstamp API Settings](https://www.bitstamp.net/settings/api/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live exchange actions require Bitstamp API credentials and an explicit live execution flag.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
