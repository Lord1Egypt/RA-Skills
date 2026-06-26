## Description: <br>
加密货币行情分析：本技能自带 Binance 公开行情 + 指标脚本；资讯用 web_search/web_fetch。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luyao-inc](https://clawhub.ai/user/luyao-inc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to fetch public Binance spot market data, calculate common technical indicators, and combine the results with fetched news context for crypto market analysis. The skill is intended for analysis with explicit risk statements, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Python script with outbound access to Binance and news sites. <br>
Mitigation: Confirm outbound network access is acceptable in the target environment before installing or running the skill. <br>
Risk: Crypto market analysis can be mistaken for investment advice. <br>
Mitigation: Present outputs as informational analysis, include risk statements, and avoid treating generated conclusions as financial advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luyao-inc/crypto-market) <br>
- [Binance public REST API](https://api.binance.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown analysis with shell command examples and JSON market snapshots] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public Binance REST data, optional proxy environment variables, and fetched news sources; no API keys are requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
