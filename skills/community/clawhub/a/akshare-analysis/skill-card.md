## Description:

Analyzes Hong Kong and A-share stocks using akshare data to produce informational BUY, HOLD, or SELL signals with confidence scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coxlong](https://clawhub.ai/user/coxlong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to evaluate Chinese equities by ticker or company name, retrieve market and news data, and generate informational stock-analysis outputs for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may execute untrusted report content or unverified runtime code.

Mitigation: Review report inputs before rendering, avoid untrusted ai_analysis.md or unexpected upstream data, escape HTML, add a CSP, and pin or integrity-check browser scripts.

Risk: Stock signals and market data may be delayed, incomplete, or unsuitable as financial advice.

Mitigation: Treat outputs as informational decision support only and verify findings against authoritative market and financial sources before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coxlong/skills/akshare-analysis)

## Skill Output:

**Output Type(s):** [text, JSON, HTML files, shell commands, guidance]

**Output Format:** [Plain text, JSON, and generated HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create report directories containing data.json, chart_data.json, and index.html; outputs include an informational disclaimer.]

## Skill Version(s):

1.1.2 (source: server-resolved release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
