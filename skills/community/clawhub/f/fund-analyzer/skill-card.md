## Description:

Fund Analyzer helps agents query China-market fund net asset values, historical trends, rankings, comparisons, and holdings using fund data sources documented in the release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hl950825](https://clawhub.ai/user/hl950825)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents can use this skill to retrieve and compare fund information, screen fund rankings, and summarize holdings for investment research workflows. Users should verify any financial results against trusted sources before making investment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that documentation and implementation disagree about whether Alipay or Eastmoney/Tiantian Fund is the actual data source.

Mitigation: Treat the data source as Eastmoney/Tiantian Fund unless release evidence is updated, and disclose the mismatch during deployment review.

Risk: The security review notes cookie-based access guidance without adequate safety handling.

Mitigation: Do not paste, hardcode, log, or share Alipay cookies or other session data when using or extending the skill.

Risk: Fund data can be delayed, unavailable, or incorrect for investment decisions.

Mitigation: Verify outputs against trusted financial sources before acting on the analysis.

## Reference(s):

- [Fund Analyzer Guide](references/guide.md)
- [ClawHub skill page](https://clawhub.ai/hl950825/skills/fund-analyzer)
- [Eastmoney fund rankings](https://fund.eastmoney.com/data/fundranking.html)
- [Eastmoney fund data](https://fund.eastmoney.com/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown-style tables and lists, with optional JSON from selected scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill depends on network access to third-party fund data pages and may return delayed or incomplete market data.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
