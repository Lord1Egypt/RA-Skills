## Description:

Fetch real-time prices, 24h statistics, K-line charts, and market information for Binance spot trading pairs using the Binance API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[torchesfrms](https://clawhub.ai/user/torchesfrms)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query public Binance spot-market data, including prices, 24-hour statistics, trading volume, and candlestick data for selected trading pairs.

### Deployment Geography for Use:

Global, subject to Binance API availability and regional access restrictions.

## Known Risks and Mitigations:

Risk: Market-data queries are sent to Binance and most scripts route requests through a local proxy at 127.0.0.1:1082.

Mitigation: Install only if this network behavior is acceptable, verify the proxy endpoint before use, and avoid running it with sensitive proxy settings.

Risk: The scripts depend on local command-line tools such as curl, jq, and bc.

Mitigation: Confirm required tools are installed and review command output before relying on the returned market data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/torchesfrms/skills/binance-exchange)
- [Publisher Profile](https://clawhub.ai/user/torchesfrms)
- [Binance Spot API Base URL](https://api.binance.com/api/v3)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON or text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public Binance market-data endpoints; most scripts expect curl, jq, bc, and a local HTTP proxy at 127.0.0.1:1082.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
