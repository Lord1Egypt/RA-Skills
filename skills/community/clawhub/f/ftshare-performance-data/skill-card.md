## Description:

Routes agent requests to FT Tech A-share earnings alerts, forecasts, cash flow statements, income statements, and balance sheets for single stocks or full-market reporting periods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawn92](https://clawhub.ai/user/shawn92)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route A-share financial performance questions to the appropriate FT Tech market data lookup and return financial report data for a single stock or a reporting period across the market.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Large or stalled FT Tech API responses may delay or fail a request.

Mitigation: Use bounded page sizes, paginate intentionally, and handle failed or slow responses before relying on the output.

Risk: Returned financial data can be incomplete, stale, or unsuitable as investment advice.

Mitigation: Treat outputs as informational and verify important figures against authoritative filings or other trusted financial sources before making decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shawn92/skills/ftshare-performance-data)
- [FT Tech market data API base URL](https://market.ft.tech)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [JSON from bundled Python scripts, usually summarized by the agent as Markdown tables or bullet points]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries may return paginated financial records with stock identifiers, reporting periods, dates, and numeric statement fields.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
