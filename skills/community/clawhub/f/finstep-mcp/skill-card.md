## Description:

财跃星辰金融数据服务。提供实时行情、板块数据、公司信息、宏观经济、研报新闻等全方位金融数据。触发条件：用户查询股票行情、板块涨跌、公司财务、宏观数据、研报公告等金融信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fa1c0n4826](https://clawhub.ai/user/fa1c0n4826)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve financial-market data from FinStep, including stock quotes, sector information, company financials, macroeconomic indicators, research reports, announcements, and trading-calendar data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: FinStep credentials are sent in URL query strings, which can expose secrets through logs, proxies, browser history, or telemetry.

Mitigation: Use a limited FinStep credential, rotate it regularly, and prefer an updated implementation that sends the signature outside query strings.

Risk: Generic web search and URL parsing features can disclose full queries or URLs to FinStep.

Mitigation: Avoid sending sensitive company, personal, or confidential information in search terms or URLs; gate these features where stronger data-control requirements apply.

Risk: Financial data and API responses can be incomplete, rate-limited, unavailable, or affected by endpoint-specific issues.

Mitigation: Review returned data before using it for analysis or decisions, handle API errors explicitly, and cross-check important results against authoritative sources.

## Reference(s):

- [FinStep product site](https://product.finstep.cn/)
- [FinStep MCP API base endpoint](https://fintool-mcp.finstep.cn)
- [ClawHub skill page](https://clawhub.ai/fa1c0n4826/skills/finstep-mcp)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the FINSTEP_SIGNATURE secret plus bash, curl, jq, and date; API responses may be subject to FinStep rate limits and endpoint behavior.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
