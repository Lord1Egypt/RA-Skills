## Description: <br>
用投资大师的脑子、呼兰的嘴，帮你搞懂指数和市场。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pzc66momo](https://clawhub.ai/user/pzc66momo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to interpret Chinese financial news, market themes, and index directions. It maps events or questions to concise analysis, one to three watchlist indices, and compliance disclaimers without personalized holdings analysis, fund recommendations, forecasts, or buy/sell advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial analysis could be mistaken for personalized investment advice. <br>
Mitigation: The skill limits responses to market logic and index themes, avoids personal holdings analysis, fund recommendations, forecasts, and buy/sell instructions, and includes an investment-risk disclaimer. <br>
Risk: Static reference data can become stale or omit real-time prices. <br>
Mitigation: The skill states that it does not provide real-time quotes or same-day movements and directs users to market-data tools for current prices. <br>
Risk: The release includes a publishing helper script that can run Git and ClawHub publication commands when executed. <br>
Mitigation: Review commands before execution and use dry-run or skip flags unless intentionally publishing a release. <br>
Risk: Security telemetry was clean but advised review before installation. <br>
Mitigation: Review the skill text before deployment, especially any requests for credentials, external uploads, local file access, or automatic setup commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pzc66momo/finance-index-skill) <br>
- [README.md](README.md) <br>
- [投资大师思维框架](references/master_frameworks.md) <br>
- [指数目录](references/index_catalog.json) <br>
- [可信指数数据源](references/trusted_sources_index.json) <br>
- [可信财经媒体源](references/trusted_sources_media.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Concise Chinese Markdown or plain text with index watchlist items and an investment-risk disclaimer] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not provide real-time quotes, personal holdings analysis, fund recommendations, forecasts, or buy/sell/hold instructions.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
