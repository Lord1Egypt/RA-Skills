## Description: <br>
可转债打新助手提供 A 股可转债申购日历、新债分析、上市溢价预测、中签率查询、强赎和下修提醒。 <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[zhaoteng-qd](https://clawhub.ai/user/zhaoteng-qd) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External A-share convertible-bond users and developers can use this skill as a demonstration aid for subscription calendars, basic bond analysis, premium estimates, and redemption or downward-revision alerts. It should not be treated as a trading assistant; dates, prices, alerts, and investment decisions need verification against official exchange, broker, or issuer sources. <br>

### Deployment Geography for Use: <br>
China (A-share convertible-bond market) <br>

## Known Risks and Mitigations: <br>
Risk: The skill advertises actionable financial analysis while the security evidence reports mock data and broken code. <br>
Mitigation: Treat outputs as demonstration material only, and verify all dates, prices, alerts, and investment decisions against official exchange, broker, or issuer sources. <br>
Risk: Incomplete or broken data-source integrations may cause runtime failures or stale results. <br>
Mitigation: Review and test the Python modules before installation or execution, especially the data-fetching and parsing paths. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhaoteng-qd/convertible-bond-assistant) <br>
- [User Guide](references/USER_GUIDE.md) <br>
- [Data Source API Documentation](references/API.md) <br>
- [Eastmoney Convertible Bond Data](http://data.eastmoney.com/kzz/) <br>
- [Sina Finance Market Data API](http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php) <br>
- [CNINFO Announcements](http://www.cninfo.com.cn/) <br>
- [Jisilu Convertible Bond Data](https://www.jisilu.cn/data/cbnew/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Analysis, Guidance] <br>
**Output Format:** [Plain text CLI output and Markdown documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include financial analysis, subscription calendars, premium estimates, and alerts based on mock or externally sourced data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
