## Description: <br>
A股日报 + 持仓管家，自动推送盘前/收盘/夜间简报，监控持仓股动态及股吧舆情，支持周末资讯。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[torchesfrms](https://clawhub.ai/user/torchesfrms) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate scheduled A-share market briefings, portfolio tracking reports, announcements, research/news summaries, and stock-forum sentiment snapshots from configured holdings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured holdings and API credentials may be sent to external market-data APIs. <br>
Mitigation: Review configured holdings before use, use explicit environment-managed credentials, and document or disable vault credential access. <br>
Risk: Reports may include hard-coded or simulated financial figures that can mislead readers. <br>
Mitigation: Verify market data against authoritative sources and replace simulated values before using the reports for investment decisions. <br>
Risk: The artifact includes an unrelated parser that reads and writes fixed /tmp paths. <br>
Mitigation: Remove the parser or isolate it from normal skill execution before installation. <br>
Risk: A fallback API key is embedded in the scripts. <br>
Mitigation: Remove the embedded key and require user-provided credentials through a controlled secret mechanism. <br>


## Reference(s): <br>
- [Aastock Daily ClawHub release](https://clawhub.ai/torchesfrms/aastock-daily) <br>
- [Publisher profile: torchesfrms](https://clawhub.ai/user/torchesfrms) <br>
- [Eastmoney market data endpoint](http://push2.eastmoney.com) <br>
- [Eastmoney authenticated API endpoint](https://mkapi2.dfcfs.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Plain text and Markdown-style market reports emitted by shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports depend on configured holdings and external Eastmoney API responses; scripts may also write local log files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and changelog mention 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
