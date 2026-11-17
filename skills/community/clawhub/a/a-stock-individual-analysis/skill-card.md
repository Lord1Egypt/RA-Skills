## Description:

Analyzes individual A-share stocks with a five-module report covering fundamentals, price and volume trends, Serenity-style moat logic, recent market news, and summary views using a-stock-data and public market sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flynnliu](https://clawhub.ai/user/flynnliu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to produce structured, public-data-based deep-dive reports for individual A-share equities, including valuation, technical trend, capital flow, news, and risk-review sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may make external market-data and web requests while preparing stock analysis.

Mitigation: Review network access expectations and source reliability before deployment, and require users to treat the resulting report as analysis rather than investment advice.

Risk: The skill instructs agents to persist newly discovered data sources into its own instructions without explicit review.

Mitigation: Require human review before adding newly discovered endpoints to trusted future-use instructions.

Risk: Market data or news may be unavailable, stale, incomplete, or inconsistent across public sources.

Mitigation: Preserve the artifact behavior of marking unavailable data explicitly and avoid filling missing values with unsupported estimates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flynnliu/skills/a-stock-individual-analysis)
- [Tencent Finance quote endpoint](https://qt.gtimg.cn/)
- [Eastmoney data center API](https://datacenter-web.eastmoney.com/api/data/v1/get)
- [Eastmoney report API](https://reportapi.eastmoney.com/report/list)
- [Eastmoney quote API](https://push2.eastmoney.com/)
- [10jqka valuation page](https://basic.10jqka.com.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown report with embedded Python and shell-command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include stock metrics, valuation tables, risk notes, endpoint fallback notes, and investment disclaimers; outputs are analytical guidance and not financial advice.]

## Skill Version(s):

1.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
