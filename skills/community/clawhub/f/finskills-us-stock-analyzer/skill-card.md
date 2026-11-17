## Description:

Perform institutional-grade analysis of any US-listed stock using real-time and fundamental data from the Finskills API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finskills](https://clawhub.ai/user/finskills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to research US-listed equities by ticker symbol, combining Finskills API market data with business quality, financial health, valuation, analyst consensus, earnings quality, and risk analysis. Outputs should be treated as research support rather than financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requested ticker symbols and related query parameters to the Finskills API.

Mitigation: Use a Finskills API key only when sharing those queries with Finskills is acceptable.

Risk: Generated ratings, price targets, and valuation judgments may be incomplete, stale, or incorrect.

Mitigation: Treat outputs as research support, verify data and assumptions independently, and do not rely on the report as financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/finskills/skills/finskills-us-stock-analyzer)
- [Publisher profile](https://clawhub.ai/user/finskills)
- [Source homepage](https://github.com/finskills/us-stock-analyzer)
- [Finskills API](https://finskills.net)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Structured Markdown investment research report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FINSKILLS_API_KEY and a US equity ticker symbol; optional depth and investment-horizon inputs affect report scope.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and README show 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
