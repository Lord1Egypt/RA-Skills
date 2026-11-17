## Description:

Crypto Alert monitors cryptocurrency prices from Binance and reports 24-hour changes with surge and drop alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dolphins1123](https://clawhub.ai/user/dolphins1123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents can use this skill to check major cryptocurrency prices and 24-hour movement summaries from the command line. It is suited for informational monitoring and alerting, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live requests to Binance for price data.

Mitigation: Install and run it only where outbound Binance API calls are acceptable.

Risk: Displayed prices and alerts could be mistaken for financial advice.

Mitigation: Treat the output as informational market data, not investment guidance.

Risk: The skill depends on the external requests package.

Mitigation: Use an isolated virtual environment and pin the requests dependency before deployment.

Risk: The skill presents output mainly in Traditional Chinese.

Mitigation: Confirm the target users can review and act on Traditional Chinese output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dolphins1123/skills/crypto-alert)
- [Binance API](https://api.binance.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-formatted text with CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live Binance API responses; primary output language is Traditional Chinese.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
