## Description:

Queries server-side HTTP APIs for China A-share dividend and rights-issue data and Hong Kong stock dividend data, including dividend yield.

This skill is ready for commercial/non-commercial use.

## Publisher:

[funkygod](https://clawhub.ai/user/funkygod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer A-share and Hong Kong stock dividend questions by turning natural-language requests into read-only dividend API queries, then summarizing historical dividend records, dividend yield, and scope limitations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dividend data may be delayed, incomplete, or inaccurate because the skill relies on an external public stock-data service.

Mitigation: Use a verified API base URL, check returned dates and missing fields, and treat outputs as historical reference data.

Risk: Users may mistake historical dividend records or dividend yield summaries for investment advice or complete financial analysis.

Mitigation: Include clear caveats that historical dividends do not predict future payouts and that the skill does not provide financial statements, forecasts, or investment advice.

Risk: The artifact lists an HTTP API base URL, which can expose data integrity risks if used without transport verification.

Mitigation: Prefer configuring a verified HTTPS API base URL through STOCK_API_BASE_URL before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/funkygod/skills/cn-hk-dividend-fhpg-api)
- [ClawHub homepage metadata](http://clawhub.ai/FunkyGod/cn-hk-dividend-fhpg-api)
- [Configured stock dividend API base URL](http://vi-money.com/)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Markdown]

**Output Format:** [Markdown with concise text, bullet lists, and optional tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Usually Chinese-language answers; includes historical-data caveats and non-investment-advice warnings.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
