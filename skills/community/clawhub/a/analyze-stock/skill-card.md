## Description:

股票分析技能，提供买卖点判断、仓位管理、基本面分析。使用当用户需要分析股票投资价值时。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxsadc2025](https://clawhub.ai/user/zxsadc2025)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to analyze Chinese stock codes, generate valuation zones, position sizing guidance, fundamentals summaries, market-sentiment notes, and benefit-risk factors. The generated report is for reference only and does not constitute investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-like values are exposed in the release report evidence.

Mitigation: Remove the exposed values from release documentation and rotate any keys that were ever real before installing or redistributing the skill.

Risk: Helper search processes receive a broad copied environment.

Mitigation: Pass only the required environment variables to child processes, especially TUSHARE_TOKEN, BAIDU_API_KEY, and any optional search or LLM keys.

Risk: External financial data, search results, and LLM analysis may be incomplete, stale, or misleading.

Mitigation: Keep the report disclaimer visible, make external data and model use clear to users, and require human review before investment decisions.

Risk: TUSHARE_API_URL can redirect financial-data requests if set incorrectly.

Mitigation: Validate the API URL against the intended Tushare endpoint or leave it unset to use the official default.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zxsadc2025/skills/analyze-stock)
- [Tushare](https://tushare.pro)
- [Tavily](https://tavily.com)
- [Fundamental analysis framework](references/fundamental_analysis.md)
- [Position management strategy](references/position_management.md)
- [Valuation zone method](references/valuation_zones.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [JSON object containing stock metadata, a Markdown analysis report, market sentiment, benefit-risk analysis, and model label]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a stock_code input and supports conservative, balanced, or aggressive analysis style.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
