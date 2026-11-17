## Description:

Produces Chinese-language A-share limit-up and Dragon-Tiger List research reports with screening frameworks, market analysis, risk checks, and HTML or PDF deliverables.

This skill is for research and development only.

## Publisher:

[yjkj999999](https://clawhub.ai/user/yjkj999999)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and developers use the skill to prepare structured reports on Chinese A-share market activity, screen candidates, and document assumptions, risks, and data gaps. The outputs are research aids and do not constitute investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a medium-confidence suspicious verdict, citing possible mismatches with stated WATCH-only limits and weaknesses in financial screening and report-data safeguards; its analysis was partial.

Mitigation: Hold off installing until an independent review checks the financial safeguards, publication behavior, and outputs against the stated WATCH-only limits; do not treat partial scanner coverage as evidence that unreviewed content is safe.

Risk: Reports may fall back to bundled sample data that is a dated snapshot rather than current market data.

Mitigation: Check the report's stated data source, date, and delay, and verify current market inputs before using the analysis.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/yjkj999999/skills/a-share-dragon-tiger-report)
- [Project repository](https://github.com/yjkj999999/a-share-dragon-tiger-strategy)
- [SEC filing reference](https://www.sec.gov/Archives/edgar/data/2130357/000162828026067168/anthropicpbc-sx1.htm)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, HTML, PDF, JSON, Guidance]

**Output Format:** [Structured research reports and supporting data; HTML and PDF are the documented report formats.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market-data availability affects report freshness; bundled sample data is marked as a dated snapshot and should not be treated as current market data.]

## Skill Version(s):

4.0.5 (source: server-resolved release and metadata.openclaw.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
