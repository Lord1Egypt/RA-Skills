## Description:

生成上市公司可比公司分析报告，当用户请求分析某家公司的竞争对手、可比公司、同业对比、竞品分析或对标公司分析时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wxai-space](https://clawhub.ai/user/wxai-space)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial analysts use this skill to produce structured A-share comparable-company analysis reports for a target listed company, including business review, peer selection, peer comparison, financial metrics, and conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial analysis may become stale because company fundamentals, valuation metrics, and market prices are time-sensitive.

Mitigation: Verify that the report uses the latest available financial period and current valuation data before relying on the output.

Risk: The generated report could be mistaken for investment advice.

Mitigation: Keep the report positioned as research support, preserve the disclaimer, and have qualified reviewers assess conclusions before use.

Risk: The workflow depends on financial-data and news/search tools whose coverage or freshness may vary.

Mitigation: Review cited data sources, check missing values explicitly, and rerun data collection when key financial or business-progress fields are incomplete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wxai-space/skills/comparable-company-analysis-simple)
- [Publisher profile](https://clawhub.ai/user/wxai-space)

## Skill Output:

**Output Type(s):** [markdown, guidance]

**Output Format:** [Markdown report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report content is based on current financial data and news/search results, so outputs should be reviewed for source quality, timeliness, and investment-advice risk.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
