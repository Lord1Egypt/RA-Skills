## Description:

基于akshare-one的MCP服务器，提供中国股票市场数据的全面接口，包括历史数据、实时数据、新闻数据和财务报表等金融信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and financial-data users use this skill to retrieve China stock market data through XiaoBenYang-backed tools, including historical prices, real-time quotes, news, financial statements, insider trading data, financial metrics, and trading-day time information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill saves the XiaoBenYang API key as plaintext in a local .env file.

Mitigation: Use an isolated workspace, keep .env out of version control, and rotate the API key if it may have been exposed.

Risk: Mismatched school/gaokao configuration can affect where credentials are sent.

Mitigation: Check for unexpected XBY_GAOKAO_BASE_URL and related .env settings before using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/akshare-one)
- [XiaoBenYang API key site](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, JSON, Guidance]

**Output Format:** [Markdown or text summaries derived from raw JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool responses include success, raw, and message fields; use requires a XiaoBenYang API key.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
