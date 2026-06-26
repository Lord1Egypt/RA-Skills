## Description: <br>
Queries server-side HTTP APIs for China A-share dividend and allotment data and Hong Kong stock dividend data, including dividend yield, when users ask about dividends, payouts, allotments, or related records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FunkyGod](https://clawhub.ai/user/FunkyGod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and agents use this skill to look up and summarize historical dividend, payout, allotment, and dividend-yield records for China A-share and Hong Kong stocks. It should not be used as a substitute for financial statements, forecasts, or investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The disclosed API base URL uses HTTP or may be overridden, which can expose users to an untrusted endpoint if not verified. <br>
Mitigation: Verify the API base URL before use and prefer HTTPS or a trusted STOCK_API_BASE_URL override. <br>
Risk: The skill does not provide financial-statement data, forecasts, or investment advice, so broader financial-analysis requests may exceed its data scope. <br>
Mitigation: Limit answers to dividend, allotment, and dividend-yield data, and add a verified financial-statement data source before answering revenue, profit, ROE, debt-ratio, forecast, or advice requests. <br>
Risk: Dividend records are historical disclosures and may be delayed, incomplete, or not predictive of future payouts. <br>
Mitigation: State the historical nature and any missing data in responses, and avoid presenting dividends as future commitments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FunkyGod/cn-hk-dividend-fhpg-api) <br>
- [Declared ClawHub homepage](http://clawhub.ai/FunkyGod/cn-hk-dividend-fhpg-api) <br>
- [Declared API base URL](http://vi-money.com/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Guidance] <br>
**Output Format:** [Chinese Markdown summary with concise prose, bullet lists, and optional tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only dividend and allotment data; dividend_yield values are decimals.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
