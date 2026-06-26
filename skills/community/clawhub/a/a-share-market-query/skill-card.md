## Description: <br>
获取股票行情与新闻情报并结构化输出，支持个股或指数查询、新闻追踪和多源交叉验证。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnycpk](https://clawhub.ai/user/sunnycpk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market analysts use this skill to gather market quotes, historical price context, and market news, then produce structured market intelligence or optional strategy summaries with source status and timestamps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market and news queries may be sent to configured external providers. <br>
Mitigation: Use dedicated low-privilege API keys and avoid submitting confidential trading research unless the configured provider endpoints are trusted. <br>
Risk: Local cache entries may retain lookup history in the skill directory. <br>
Mitigation: Clear the local .cache directory when local query history should not persist. <br>
Risk: Optional strategy summaries can be mistaken for investment advice. <br>
Mitigation: Keep the skill's disclaimer visible and review outputs before acting on market or portfolio decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunnycpk/a-share-market-query) <br>
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Structured JSON from the execution script and Markdown market-intelligence briefs for agent responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include quote, history, news, source status, timestamps, strategy signals, risk level, and a disclaimer that outputs are not investment advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
