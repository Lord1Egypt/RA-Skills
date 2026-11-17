## Description:

Operate Binance Spot APIs through safe REST, WebSocket, and SDK workflows with signed requests, rate-limit control, and testnet-first execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to work with Binance Spot market data, signed account and trading requests, WebSocket reconciliation, rate-limit handling, and testnet-first validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Signed Binance examples can expose authentication material to a configured Binance base URL if the environment is misconfigured.

Mitigation: Use testnet first, set BINANCE_BASE_URL only to known Binance production or testnet hosts, avoid logging secrets, and use restricted API keys with withdrawals disabled and IP allowlisting.

Risk: Production trading requests can place or manage real Spot orders when valid account credentials are present.

Mitigation: Require explicit user confirmation before production orders and validate each new order payload with testnet and order/test flows first.

Risk: Incorrect timestamp, signature, symbol-filter, or rate-limit handling can cause failed requests, duplicate retries, temporary bans, or uncertain order state.

Mitigation: Sync Binance server time, rebuild canonical signatures per request, validate exchange filters locally, back off on 429 or 418 responses, and reconcile uncertain orders through REST and user-data events.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ivangdavila/skills/binance)
- [Skill homepage](https://clawic.com/skills/binance)
- [Setup - Binance API](artifact/setup.md)
- [Binance Quickstart](artifact/quickstart.md)
- [Binance Auth and Signing](artifact/auth-signing.md)
- [Binance Market Data Patterns](artifact/market-data.md)
- [Binance WebSocket Operations](artifact/websocket.md)
- [Binance Limits and Error Handling](artifact/errors-limits.md)
- [Binance Spot Testnet](artifact/testnet.md)
- [Binance Troubleshooting](artifact/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, JSON, Python, and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce signed Binance REST and WebSocket workflow guidance that depends on local environment variables and user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
