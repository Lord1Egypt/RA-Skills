## Description: <br>
中国A股实时盯盘技能，支持实时行情监控、价格和量比异动提醒、主力资金流向监测、消息面热点监测、多股并行、彩色提醒和可选企业微信推送。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[p4x1s](https://clawhub.ai/user/p4x1s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to monitor selected China A-share symbols, receive price or volume movement alerts, inspect main fund flow signals, and surface market news during trading sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Continuous monitoring can keep a local process active and make repeated network requests. <br>
Mitigation: Run it in a controlled terminal or session, review the configured stock list before starting, and stop the process when monitoring is no longer needed. <br>
Risk: Optional WeCom delivery can send alert content outside the local environment. <br>
Mitigation: Review WECHAT_WEBHOOK before starting and leave it unset when push notifications are not required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/p4x1s/a-stock-real-time-monitor) <br>
- [Sina Finance](https://finance.sina.com.cn/) <br>
- [Eastmoney market data endpoint](https://push2.eastmoney.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start a long-running local Python process that polls market data and optionally sends WeCom alerts.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
