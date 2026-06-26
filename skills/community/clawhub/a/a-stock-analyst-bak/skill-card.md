## Description: <br>
A Stock Analyst.Bak is an A-share market research assistant for stock quotes, fundamentals, screening, watchlist management, news monitoring, and alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaohaixin](https://clawhub.ai/user/zhaohaixin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to analyze China A-share equities, screen stocks by financial or technical criteria, inspect watchlists, and prepare stock research summaries. The skill can call Eastmoney data services and related dependent skills to gather market, fundamental, news, and alert information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Eastmoney/Miaoxiang credentials. <br>
Mitigation: Use a dedicated API key where possible and avoid sharing credentials outside the intended agent environment. <br>
Risk: Stock queries and watchlist operations may be sent to Eastmoney services and can involve account-linked data. <br>
Mitigation: Assume market queries and watchlist actions are transmitted to Eastmoney, and review account or portfolio-sensitive prompts before use. <br>
Risk: The skill can manage watchlists and monitoring rules. <br>
Mitigation: Confirm additions, removals, and monitoring changes before execution. <br>
Risk: The skill auto-installs dependent skills from the publisher ecosystem. <br>
Mitigation: Install only when the publisher and dependent skills are trusted for the intended workflow. <br>
Risk: Market data may be delayed or limited, and generated analysis is not investment advice. <br>
Mitigation: Validate time-sensitive market information against authoritative trading sources and treat outputs as informational. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaohaixin/a-stock-analyst-bak) <br>
- [Publisher profile](https://clawhub.ai/user/zhaohaixin) <br>
- [Eastmoney Miaoxiang API endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown analysis summaries with structured API responses when tools are called] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require an Eastmoney/Miaoxiang API key and auto-installed dependent skills for live data, watchlist, screening, search, and monitoring workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
