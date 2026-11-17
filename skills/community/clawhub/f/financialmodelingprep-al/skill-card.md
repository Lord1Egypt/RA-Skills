## Description:

Guides an agent to retrieve, verify, cite, and safely present company financial data from Financial Modeling Prep.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to answer company-financial-data requests with FMP data while preserving ticker resolution, numeric traceability, API-key safety, quota awareness, and investment-advice boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial data may be stale, plan-restricted, delayed, or returned for the wrong ticker.

Mitigation: Resolve and confirm symbols before data pulls, cite endpoint, period, currency, filing date, and as-of time for every figure, and state when no data or plan limits prevent an answer.

Risk: FMP account credentials or quota could be exposed or misused.

Mitigation: Keep FMP_API_KEY in the environment, redact it from examples and logs, minimize calls, cache within a session, batch where possible, and back off on rate limits.

Risk: Users may treat model estimates or comparisons as investment advice.

Mitigation: Frame valuation outputs as informational data, avoid buy or sell recommendations, and include an independent-verification and not-investment-advice disclaimer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simonpierreboucher02/skills/financialmodelingprep-al)
- [FMP developer documentation](https://site.financialmodelingprep.com/developer/docs)
- [FMP endpoints reference](reference/endpoints.md)
- [FMP best practices](reference/best-practices.md)
- [FMP common errors](reference/common-errors.md)
- [FMP response fields](reference/response-fields.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API Calls, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with endpoint names, request examples, checklists, and cited-response patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FMP_API_KEY in the environment for agents or tools that query FMP; outputs should remain informational and cite FMP data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
