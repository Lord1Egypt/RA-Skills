## Description:

CrossData aggregates public ecommerce and social platform data for standardized competitor pricing, sales, and market analysis across multiple markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yayale-deng](https://clawhub.ai/user/yayale-deng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to request keyword-driven product data from supported commerce and social platforms, then compare prices, sales signals, ratings, and target-market summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact publishes a plaintext ClawHub token.

Mitigation: Revoke and remove the exposed token before installation, and supply credentials only through protected runtime configuration.

Risk: The skill describes real-time queries against third-party commerce and social platforms without clear usage warnings.

Mitigation: Confirm the queried platforms, terms of use, and rate limits before running keyword searches or refresh workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yayale-deng/skills/crossdata)
- [Publisher profile](https://clawhub.ai/user/yayale-deng)

## Skill Output:

**Output Type(s):** [text, JSON, CSV, guidance]

**Output Format:** [Structured JSON or CSV data summaries with product records and aggregate market metrics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports keyword, target market, price range, source platform, and result limit inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
