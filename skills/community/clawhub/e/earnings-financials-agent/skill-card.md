## Description:

An autonomous agent for monitoring corporate earnings and analyzing financial statements using yfinance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[assix](https://clawhub.ai/user/assix)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to retrieve public earnings calendar data and quarterly financial metrics for stock tickers. The results support earnings summaries, company comparisons, ratio checks, cash-flow review, growth trend analysis, and dividend health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unpinned yfinance dependency can change behavior across installs or introduce unexpected dependency changes.

Mitigation: Install the skill in an isolated virtual environment and pin yfinance to a reviewed version before use.

Risk: Financial data retrieval and summaries can be incomplete, delayed, or misread as investment advice.

Mitigation: Treat outputs as analysis support only and review important financial conclusions against authoritative filings or market data sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/assix/skills/earnings-financials-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON from the local Python tool calls, with agent-facing prose or Markdown guidance for setup and analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and pip; uses yfinance for public market data retrieval.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
