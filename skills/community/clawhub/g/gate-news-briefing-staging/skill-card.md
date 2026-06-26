## Description: <br>
Generates crypto news briefings by aggregating recent Gate News events, top headlines, and social sentiment for broad market or coin-specific requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaixianggeng](https://clawhub.ai/user/gaixianggeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to produce concise cryptocurrency news briefings from recent events, ranked headlines, and social sentiment. It supports general market briefings and coin-specific headline updates while routing multi-dimension analysis to other skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Briefings depend on the availability and trustworthiness of the Gate News MCP server and its returned news, event, and sentiment data. <br>
Mitigation: Confirm the Gate News MCP server is the intended source before use, label degraded sections when feeds fail, and preserve source attribution for important items. <br>
Risk: Generated crypto briefings may be mistaken for investment advice or may overstate sentiment signals. <br>
Mitigation: Treat outputs as informational summaries, keep a neutral tone, avoid buy/sell guidance, and include the skill's investment-advice disclaimer when producing briefings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaixianggeng/gate-news-briefing-staging) <br>
- [Gate News Briefing Runtime Rules](references/gate-runtime-rules.md) <br>
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md) <br>
- [Gate News Briefing MCP Specification](references/mcp.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown briefing with source attribution, time range labels, event summaries, categorized headlines, social sentiment, and watch items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only output based on Gate News MCP results; degraded sections are labeled when a required feed is unavailable.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
