## Description: <br>
A股智能投资助手 helps agents fetch A-share market data, calculate technical indicators, monitor watchlists, generate holding reports, and configure scheduled Feishu or WeChat notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzhaofeng-max](https://clawhub.ai/user/wangzhaofeng-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market-focused agent users use this skill to retrieve A-share quotes and K-line data, compute MACD, KDJ, RSI, Bollinger Bands, and moving averages, generate watchlist alerts and holding reports, and configure scheduled notification workflows. The skill is informational and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts external market-data services, so results may be delayed, unavailable, or affected by network and provider behavior. <br>
Mitigation: Review the configured data sources, handle provider failures, and treat market data as informational rather than authoritative trading advice. <br>
Risk: Scheduled reports and alerts can send market information to Feishu or WeChat channels when configured. <br>
Mitigation: Confirm notification schedules and webhook or channel credentials before enabling scheduled pushes, and disable them when no longer needed. <br>
Risk: Technical indicators, backtests, and generated signals can be mistaken for investment recommendations. <br>
Mitigation: Use outputs for analysis support only, review assumptions manually, and avoid relying on generated signals as financial advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangzhaofeng-max/akshare-finance-pro) <br>
- [Eastmoney K-line market data endpoint](https://push2his.eastmoney.com/api/qt/stock/kline/get) <br>
- [Eastmoney quote site](https://quote.eastmoney.com) <br>
- [Eastmoney real-time market data endpoint](https://push2.eastmoney.com/api/qt/clist/get) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python, JSON, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires akshare, pandas, and ta; may contact external market-data services and configured notification channels.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
