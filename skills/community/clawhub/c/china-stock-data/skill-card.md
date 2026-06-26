## Description: <br>
Provides China A-share market data workflows for quotes, order book snapshots, K-line history, announcements, research, fund flows, themes, watchlists, and financial news using multiple fallback data sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kekewater](https://clawhub.ai/user/kekewater) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to query and monitor China A-share market data, generate daily financial briefings, and retrieve company announcements or research without building separate integrations for each provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports an exposed third-party API token in the bundled stock-data workflow. <br>
Mitigation: Remove the bundled token before use and provide personal credentials through environment variables or a secret store. <br>
Risk: The security scan reports under-scoped guidance for bypassing provider limits and modifying browser-agent behavior. <br>
Mitigation: Avoid proxy or IP-rotation guidance, keep provider requests within published limits, and run optional browser/PDF workflows only with explicit download approval in a contained environment. <br>
Risk: The skill queries live financial data sources that can be delayed, rate limited, or unavailable. <br>
Mitigation: Treat results as informational data, verify important figures against primary sources, and do not use the skill for order placement or trading execution. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/kekewater/china-stock-data) <br>
- [CNINFO API Reference](references/cninfo-api.md) <br>
- [CNINFO PDF Extraction](references/cninfo-pdf-extraction.md) <br>
- [EastMoney Limitations](references/eastmoney-limitations.md) <br>
- [TDX Protocol Notes](references/tdx-protocol-notes.md) <br>
- [TDX Rate Limiting](references/tdx-rate-limiting.md) <br>
- [Tonghuashun Headlines API](references/tonghuashun-headlines-api.md) <br>
- [Tushare Pro](https://tushare.pro/) <br>
- [JoinQuant](https://www.joinquant.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some commands call external financial data providers and may require user-supplied credentials or provider-specific rate limits.] <br>

## Skill Version(s): <br>
1.7.0 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
