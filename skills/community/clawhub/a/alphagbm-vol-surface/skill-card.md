## Description:

3D volatility surface analysis mapping implied volatility across strikes and expirations, showing whether options are cheap or expensive and returning surface grid data, ATM term structure, skew by expiry, and surface anomalies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and trading-research users use this skill to query AlphaGBM for option implied-volatility surfaces, term structure, skew, and anomaly analysis for optionable tickers. It supports research into volatility dynamics and potential mispricing without providing financial advice or automated trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is for financial research and may produce outputs that users could mistake for investment advice.

Mitigation: Present results as research context only and require human review before any trading or investment decision.

Risk: Live use requires an AlphaGBM API key and may send ticker queries to AlphaGBM's service.

Mitigation: Configure credentials through environment variables, avoid exposing secrets, and review provider costs, quotas, and data-use terms before use.

## Reference(s):

- [AlphaGBM](https://alphagbm.com)
- [AlphaGBM API Base URL](https://alphagbm.zeabur.app)
- [ClawHub Skill Page](https://clawhub.ai/clementgu/skills/alphagbm-vol-surface)
- [Publisher Profile](https://clawhub.ai/user/clementgu)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with API endpoint examples and JSON-shaped analysis outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ALPHAGBM_API_KEY for live API use; demo tickers may use mock data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
