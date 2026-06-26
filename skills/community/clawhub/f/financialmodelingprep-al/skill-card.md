## Description: <br>
Guides an agent to retrieve, verify, and cite Financial Modeling Prep financial data while protecting API credentials and avoiding investment advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to guide agent calls to FMP for company profiles, quotes, statements, ratios, valuation references, historical prices, and earnings data. It emphasizes symbol resolution, traceable figures, freshness notes, API-key protection, and not-investment-advice disclaimers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release requires sensitive credentials for FMP API access. <br>
Mitigation: Read the key only from FMP_API_KEY, redact it from logs, examples, citations, and user-visible output, and do not send it to non-FMP endpoints. <br>
Risk: Server security evidence marks the release suspicious and notes broader authority than a review workflow needs. <br>
Mitigation: Install only if the publisher is trusted, review local commands and authenticated tool use before confirming them, and prefer no-yolo or full-sandbox opt-out settings unless full access is required. <br>
Risk: Financial data can be stale, plan-restricted, unavailable, or misattributed to the wrong ticker. <br>
Mitigation: Resolve symbols before retrieval, cite symbol, endpoint, period, filing date, currency, and as-of timestamp, handle 401/402/429 errors explicitly, and avoid personalized investment advice. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/simonpierreboucher02/financialmodelingprep-al) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [FMP endpoints reference](artifact/reference/endpoints.md) <br>
- [FMP best practices](artifact/reference/best-practices.md) <br>
- [FMP parameters reference](artifact/reference/parameters.md) <br>
- [FMP response fields reference](artifact/reference/response-fields.md) <br>
- [FMP common errors reference](artifact/reference/common-errors.md) <br>
- [Financial Modeling Prep developer docs](https://site.financialmodelingprep.com/developer/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown guidance with endpoint names, tool names, citations, and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FMP_API_KEY in the runtime environment; outputs should redact credentials, cite source fields, and include not-investment-advice disclaimers where relevant.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
