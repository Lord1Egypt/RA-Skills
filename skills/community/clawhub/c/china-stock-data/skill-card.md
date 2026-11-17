## Description:

中国A股综合数据源技能。集成通达信(TDX)实时行情+5档盘口+K线、腾讯财经PE/PB/市值/换手率、同花顺iFinD/热点、AKShare研报/公告、iWencai问财搜索、JQData聚宽量化、Tushare Pro公告、RiceQuant米筐。8大来源自动降级。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kekewater](https://clawhub.ai/user/kekewater)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users can use this skill to query China A-share market data, K-line history, announcements, research reports, sector rankings, topic signals, monitor alerts, and finance news summaries from multiple data sources. It is for data retrieval and analysis support, not order placement or trading execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports unsafe credential handling, including an embedded Tushare token.

Mitigation: Rotate or remove embedded tokens before use and provide credentials through user-controlled configuration or environment variables.

Risk: Security evidence reports insecure transport through plaintext endpoints such as the custom Tushare endpoint and CNINFO HTTP where HTTPS may be available.

Mitigation: Prefer HTTPS endpoints when supported and review any plaintext data-source connections before use in trusted environments.

Risk: Security evidence warns against running Chromium with --no-sandbox on trusted hosts.

Mitigation: Run browser-based PDF extraction only in an isolated environment or use a sandboxed browser configuration.

Risk: Security evidence flags proxy or IP-rotation evasion guidance.

Mitigation: Follow data-provider terms and rate limits instead of using proxy rotation to bypass access controls.

Risk: Security evidence says generated briefing images may be demo or static unless the data path is replaced with live verified sources.

Mitigation: Treat generated briefing images as illustrative until their inputs are connected to verified live data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kekewater/skills/china-stock-data)
- [CNINFO API Reference](references/cninfo-api.md)
- [CNINFO PDF Extraction Method](references/cninfo-pdf-extraction.md)
- [EastMoney Limitations](references/eastmoney-limitations.md)
- [TDX Protocol Notes](references/tdx-protocol-notes.md)
- [TDX Rate Limiting](references/tdx-rate-limiting.md)
- [Tonghuashun Headlines API](references/tonghuashun-headlines-api.md)
- [Using Claude Code to Build a Stable A-share Data Source](https://mp.weixin.qq.com/s/wWIJOYwfmzQ5EEIZQbby0Q)
- [A-share Data Platforms and Tools](https://mp.weixin.qq.com/s/SV2TGAppLlmhvQQYLWDRIw)
- [Finance AI Tools](https://mp.weixin.qq.com/s/M5wRDr1sIoYXRzBDIl6sWA)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON responses from bundled Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some commands require network access, installed Python dependencies, configured provider credentials, or available upstream market-data services.]

## Skill Version(s):

1.7.0 (source: server release metadata; artifact frontmatter declares 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
