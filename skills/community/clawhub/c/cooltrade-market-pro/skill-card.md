## Description: <br>
获取中国 A 股、美股、全球大盘以及期市的行情与深度财务面分析，支持加密货币实时行情与买卖信号，AI 生成每日 A 股精华日报，并提供多通道（微信/Telegram）股价预警推送。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atvisions](https://clawhub.ai/user/atvisions) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to CoolTrade for market quotes, financial indicators, market news, AI daily reports, cryptocurrency signals, and stock price alert management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a CoolTrade API key in URL-based HTTP requests. <br>
Mitigation: Use a limited, rotateable key where possible and avoid sharing prompts or logs that expose credential-bearing request URLs. <br>
Risk: The skill can create or delete persistent stock price alerts and configure WeChat or Telegram notifications from chat requests. <br>
Mitigation: Review agent actions before alert changes and avoid enabling automatic alert management unless the notification behavior is acceptable. <br>
Risk: Market analysis, cryptocurrency signals, and trading references may be incorrect, stale, or unsuitable for a user's financial situation. <br>
Mitigation: Treat outputs as informational analysis, verify against trusted market sources, and do not rely on the skill as sole financial advice. <br>


## Reference(s): <br>
- [CoolTrade skill page](https://clawhub.ai/atvisions/cooltrade-market-pro) <br>
- [CoolTrade website](https://cooltrade.xyz) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, Guidance, Configuration] <br>
**Output Format:** [Markdown or text responses based on JSON data returned from CoolTrade HTTP endpoints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a CoolTrade API key and can create, list, or delete persistent stock price alerts.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
