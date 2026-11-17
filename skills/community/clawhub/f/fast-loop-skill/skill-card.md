## Description:

Trade Polymarket BTC 5-minute and 15-minute fast markets using Binance momentum signals, enhanced with TradingAgents pipeline, 50-persona swarm consensus, ACTA receipts, and Cedar governance

This skill is ready for commercial/non-commercial use.

## Publisher:

[zombie760](https://clawhub.ai/user/zombie760)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators use this skill to run an automated fast-market BTC trading loop that combines Binance momentum data, Polymarket market filters, consensus checks, and configured position sizing. Because it can submit authenticated trade requests, it should be audited and constrained before use near funds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated trade requests may be sent by the skill while documentation describes paper-trading and safety controls that the code does not fully enforce.

Mitigation: Audit the trading path before installation, require explicit dry-run/live gates, and keep live credentials unavailable until controls are verified.

Risk: Credentials and endpoint configuration can direct trading requests to a configured Simmer API service.

Mitigation: Use narrowly scoped credentials, restrict SIMMER_API_URL to a trusted HTTPS endpoint, and rotate keys after testing.

Risk: Automated market selection and position sizing can create financial exposure if run against a live trading backend.

Mitigation: Set strict account-level limits, review position-size settings, monitor executions, and run in an isolated account first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zombie760/skills/fast-loop-skill)
- [Publisher profile](https://clawhub.ai/user/zombie760)
- [Simmer API endpoint referenced by artifact](https://api.simmer.markets)
- [Binance klines API endpoint referenced by artifact](https://api.binance.com/api/v3/klines)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Text logs, JSON-like API responses, Python code behavior, and environment-variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trade results, PnL, position size, market decisions, and operational logs.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
