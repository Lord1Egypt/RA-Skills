## Description: <br>
A股黑天鹅对冲策略监控日报。每天自动抓取市场数据，基于改进版塔勒布期权策略的建仓、退出及风控规则进行计算分析，生成监控日报并通过邮件和飞书发送。监控标的包括沪深300、上证50、中证500、创业板、科创50的期权隐含波动率，以及全市场融资余额变化。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frankski818](https://clawhub.ai/user/frankski818) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a daily A-share black swan hedging monitor that gathers market data, evaluates entry and exit signals, and generates operational monitoring reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill embeds an SMTP credential and sends reports to a fixed mailbox. <br>
Mitigation: Remove the built-in SMTP credential, rotate the exposed mail auth code, and replace email settings with user-provided secure configuration before installation. <br>
Risk: Automated report delivery may send market reports outside the intended environment. <br>
Mitigation: Confirm report recipients, Feishu webhook use, and scheduled execution policy before enabling automated runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/frankski818/blackswan-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/frankski818) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, terminal logs, configuration instructions, and notification text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local JSON state files and send generated reports by email or Feishu webhook when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
