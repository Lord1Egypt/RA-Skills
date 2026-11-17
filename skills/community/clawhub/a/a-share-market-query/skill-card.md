## Description:

获取股票行情与新闻情报并结构化输出。用户要求查询个股/指数、新闻追踪或多源交叉验证时调用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnycpk](https://clawhub.ai/user/sunnycpk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to gather multi-source stock quotes, historical market data, news, and concise market-intelligence briefs. It supports information-only summaries and strategy-oriented analysis with clear source attribution and risk notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Custom news endpoints may receive user queries and optional API tokens, including through non-HTTPS URLs.

Mitigation: Configure BOCHA_BASE_URL and MINIMAX_BASE_URL only with trusted HTTPS endpoints, and avoid enabling custom sources when sensitive market queries or credentials are involved.

Risk: API credentials for market and news services can be exposed through shared execution environments.

Mitigation: Keep TAVILY_API_KEY, SERPAPI_API_KEY, BRAVE_API_KEY, BOCHA_API_KEY, MINIMAX_API_KEY, and TUSHARE_TOKEN out of environments shared with untrusted tools.

Risk: Market data or news source failures can produce incomplete intelligence.

Mitigation: Review per-source ok/error fields and fallback_source_used before relying on an output, and treat strategy-mode results as informational rather than investment advice.

## Reference(s):

- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills)
- [ClawHub Skill Page](https://clawhub.ai/sunnycpk/skills/a-share-market-query)
- [Publisher Profile](https://clawhub.ai/user/sunnycpk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON command output and Markdown market-intelligence briefs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include timestamps, per-source ok/error status, fallback source markers, optional strategy signals, and an investment-advice disclaimer.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
