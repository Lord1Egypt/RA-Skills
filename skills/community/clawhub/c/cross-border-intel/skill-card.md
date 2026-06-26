## Description: <br>
面向跨境卖家的选品与竞品情报助手，自动监控 Amazon ASIN 动态并追踪 TikTok 爆品趋势 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xifengzhu](https://clawhub.ai/user/xifengzhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External cross-border e-commerce sellers and operators use this skill to monitor Amazon ASIN price, BSR, review, and listing changes, track TikTok product trend signals, manage watchlists, trigger scans, and generate daily or weekly market reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Watchlist entries, TikTok keywords, and marketplace observations may be sent to a configured external Intel API backend. <br>
Mitigation: Install only when the publisher and backend are trusted, and use a least-privilege OpenClaw gateway token where available. <br>
Risk: Local SQLite storage may contain sensitive commerce monitoring data, including raw Amazon and TikTok response data. <br>
Mitigation: Periodically inspect, protect, or clear the local database when monitored ASINs, keywords, alerts, or reports are sensitive. <br>
Risk: The security verdict requires review before normal deployment. <br>
Mitigation: Review the ClawHub security summary and configured backend before enabling automated scans or scheduled reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xifengzhu/cross-border-intel) <br>
- [README](artifact/README.md) <br>
- [OpenClaw local testing guide](artifact/docs/OPENCLAW_TESTING.md) <br>
- [Historical architecture reference](artifact/docs/architecture.md) <br>
- [Default Intel API endpoint](https://api.haixia.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, TypeScript API usage examples, shell commands, and locally stored report data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores watchlists, snapshots, TikTok hits, alerts, reports, jobs, and configuration in a local SQLite database.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
