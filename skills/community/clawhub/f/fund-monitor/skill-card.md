## Description:

Queries China A-share public fund net values and daily changes, supports batch fund monitoring, and can summarize portfolio performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query individual or batches of China A-share public funds, monitor daily price movements, estimate portfolio performance, and prepare fund-report summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hardcoded Feishu credentials and a fixed document destination may expose data or give unintended write access.

Mitigation: Remove or rotate the embedded credentials before use and require users to configure their own Feishu app and document target.

Risk: Sensitive portfolio summaries can be published outside the local environment.

Mitigation: Review the export destination before running report-update scripts and prefer local-only monitoring unless publication is explicitly intended.

Risk: Fund data may be delayed and batch queries may be rate-limited.

Mitigation: Treat generated summaries as monitoring aids, verify values against authoritative sources, and avoid relying on the skill alone for financial decisions.

## Reference(s):

- [ClawHub fund-monitor skill page](https://clawhub.ai/hongjiahao371-pixel/skills/fund-monitor)
- [Eastmoney fund data endpoint](https://fund.eastmoney.com/pingzhongdata/{fund_code}.js)
- [Eastmoney fund page](https://fund.eastmoney.com/{fund_code}.html)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu document append API](https://open.feishu.cn/open-apis/docx/v1/documents/blocks/append)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Terminal text summaries and Markdown report content, with optional shell commands for running bundled scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include fund net values, daily changes, portfolio gain/loss estimates, and Feishu report content.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
