## Description: <br>
Professional finance news assistant that monitors A-share and Hong Kong stock news, gathers disclosed market data, and produces concise daily morning reports with anti-hallucination safeguards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gushenjie](https://clawhub.ai/user/gushenjie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and finance-focused agents use this skill to generate daily stock news reports, search recent news for tracked securities, and analyze likely market impact while separating sourced facts from analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can surface buy, sell, hold, target price, stop-loss, and position suggestions that may be mistaken for authoritative investment advice. <br>
Mitigation: Independently verify prices, news, and recommendations before acting, and treat the output as decision support rather than financial advice. <br>
Risk: The skill depends on a fixed stock API provider and a STOCK_API_TOKEN for market data and AI decision references. <br>
Mitigation: Install only if the API provider is trusted and use a scoped token with appropriate rotation and access controls. <br>
Risk: Optional Feishu delivery can send reports to unintended recipients if configured incorrectly. <br>
Mitigation: Configure Feishu recipient IDs deliberately and verify the destination before enabling automated delivery. <br>
Risk: Finance news summaries can be misleading if sources are stale, unsupported, or mixed across dates. <br>
Mitigation: Use the documented source whitelist, seven-day news window, explicit source labels, and anti-hallucination checks before publishing or acting on a report. <br>


## Reference(s): <br>
- [Finance News Assistant ClawHub page](https://clawhub.ai/gushenjie/finance-news-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/gushenjie) <br>
- [Anti-hallucination rules](references/anti-hallucination.md) <br>
- [Daily report format](references/daily-report-format.md) <br>
- [News source whitelist](references/news-sources.md) <br>
- [Known error log](references/error-log.md) <br>
- [Configuration example](assets/config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance, Configuration] <br>
**Output Format:** [Markdown reports with cited news items, market data summaries, risk notes, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Daily reports are constrained to five tracked securities, seven-day news windows, source attribution, and concise per-stock sections.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
