## Description: <br>
A-Stock Radar monitors and analyzes China A-share market conditions, including index moves, sector rankings, macro snapshots, short-term sentiment, core company quotes, and position-style market commentary with an investment-advice disclaimer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gold3bear](https://clawhub.ai/user/gold3bear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market analysts use this skill to gather public A-share market snapshots, sector movement, macro indicators, sentiment signals, and concise research-oriented commentary. It supports research workflows and explicitly warns that its outputs are not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market commentary and position-style suggestions could be mistaken for investment advice. <br>
Mitigation: Treat outputs as research only, preserve the skill's investment-advice disclaimer, and have a qualified human review any trading decision. <br>
Risk: The skill fetches public market data over the network and may return stale, incomplete, or unavailable data when upstream sources fail. <br>
Mitigation: Review scripts and dependencies before running with network access, and verify important data against authoritative market sources before acting on it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gold3bear/a-stock-radar) <br>
- [Publisher profile](https://clawhub.ai/user/gold3bear) <br>
- [Eastmoney market data](https://quote.eastmoney.com/) <br>
- [Sina Finance market data](http://finance.sina.com.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal text summaries with market indicators, tables, and commentary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public market data fetched from Sina Finance, Eastmoney, and akshare-backed sources; outputs include disclaimers that they are not investment advice.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
