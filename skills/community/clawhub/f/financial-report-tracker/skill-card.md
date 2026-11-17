## Description:

Automatically track tech company financial reports and generate investment summaries. Supports retrieving earnings calendars, market expectation comparisons, key metric interpretation, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to track company earnings dates, compare market expectations with reported financial metrics, and generate Markdown summaries for financial report review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill prints investment-style recommendations based on market data that may be incomplete, delayed, or unsuitable for a user's financial situation.

Mitigation: Treat generated reports as informational summaries only and require human financial review before making trading or investing decisions.

Risk: The skill contacts public market-data services and depends on unpinned Python packages.

Mitigation: Run it in an isolated Python environment with reviewed pinned dependencies and expected outbound network access.

Risk: The --quarter option is accepted by the command line but may not produce true quarter-specific analysis.

Mitigation: Verify the reporting period manually when reviewing earnings output for a specific quarter.

## Reference(s):

- [Financial Report Tracker API Reference](references/api_reference.md)
- [yfinance Library](https://pypi.org/project/yfinance/)
- [Financial Modeling Prep API](https://site.financialmodelingprep.com/developer/docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with tables and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include unavailable-data markers, ratings, and investment-style recommendations derived from public market-data responses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
