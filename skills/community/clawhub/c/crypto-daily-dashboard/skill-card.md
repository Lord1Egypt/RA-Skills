## Description:

All-in-one crypto dashboard showing Binance portfolio, BTC/ETH/SOL prices, Fear & Greed index, top funding rates, and economic tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dagangtj](https://clawhub.ai/user/dagangtj)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can use this skill to run a terminal crypto dashboard that summarizes Binance balances, major coin prices, market sentiment, funding rates, and optional economic status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional ECONOMIC_TRACKER_PATH setting can cause local command execution if it points to an untrusted path or is controlled by an untrusted environment.

Mitigation: Do not set ECONOMIC_TRACKER_PATH unless the target script and launch environment are fully controlled; fix the shell execution path before scheduled or unattended use.

Risk: Binance credentials are used to read account balances.

Mitigation: Use read-only Binance API keys and avoid trading or withdrawal permissions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dagangtj/skills/crypto-daily-dashboard)
- [dagangtj ClawHub Publisher Profile](https://clawhub.ai/user/dagangtj)
- [Binance API Endpoint](https://api.binance.com)
- [Binance Futures API Endpoint](https://fapi.binance.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text output with configuration instructions and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; Binance balances require read-only API credentials in environment variables.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
