## Description:

Generates concise earnings-analysis reports for specified stocks, covering recent financial metrics, quality signals, institutional views, and the next expected reporting date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dzy11650](https://clawhub.ai/user/dzy11650)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial analysts use this skill to request Chinese-language earnings reports for individual stocks or upcoming report candidates. It summarizes revenue, profit, cash flow, quality signals, valuation fit, institutional views, and reporting-calendar information without giving buy or sell recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can activate during casual earnings discussion if a stock symbol and earnings-related terms are mentioned.

Mitigation: Use explicit stock symbols and clear analysis requests to reduce accidental activation.

Risk: Reports are saved in the workspace and important results may be added to IMA notes.

Mitigation: Review generated reports and notes for sensitive financial context before sharing or retaining them.

Risk: Financial metrics and institutional views may be incomplete, stale, or misleading if source data is unavailable or inaccurate.

Mitigation: Treat outputs as analytical signals, verify material figures against authoritative filings or data sources, and avoid using the report as buy or sell advice.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dzy11650/skills/earnings-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files, Guidance]

**Output Format:** [Markdown report saved as an .md file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-stock reports are capped at 600 characters; batch reports are capped at 300 characters per stock.]

## Skill Version(s):

1.0.0 (source: server release evidence and README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
