## Description: <br>
A 股全流程量化决策系统 guides an agent through A-share market data collection, technical indicator analysis, position monitoring, scheduled market checks, and structured trading review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZooAgentPM](https://clawhub.ai/user/ZooAgentPM) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent gather A-share market data, calculate indicators, prepare buy/sell/hold analysis, monitor positions, and produce daily trading reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce buy, sell, hold, stop-loss, and position-management analysis that may be mistaken for automated financial advice. <br>
Mitigation: Treat trading output as decision-support analysis only and require human review before any market action. <br>
Risk: Recurring cron or heartbeat tasks can continue market monitoring and persist portfolio or conversation-derived notes after registration. <br>
Mitigation: Register only the schedules needed, disable unused recurring tasks, and review stored portfolio memory and learning files regularly. <br>
Risk: Datasaver tokens and Eastmoney cookies are sensitive personal credentials that may leak through shared terminals, repositories, or logs. <br>
Mitigation: Keep credentials out of shared environments and source control, use short-lived tokens or cookies where possible, and rotate them after exposure. <br>
Risk: Market data can be stale, malformed, rate-limited, or affected by non-trading days, which can distort analysis. <br>
Mitigation: Run sanity checks on API responses, verify dates and price units, and confirm market-open status before acting on generated analysis. <br>


## Reference(s): <br>
- [数据采集 API 手册](references/data-api.md) <br>
- [技术指标判断手册](references/indicators.md) <br>
- [盯盘定时任务配置手册](references/watchdog.md) <br>
- [每日复盘模板](references/review-template.md) <br>
- [报错处理手册](references/error-handling.md) <br>
- [Datasaver 安装与配置指南](references/datasaver-setup.md) <br>
- [推荐阅读 & 扩展资源](references/further-reading.md) <br>
- [Datasaver official setup document](https://docs.qq.com/doc/DT3FZT09Zd254c1Bv) <br>
- [InStock open-source quantitative system](https://github.com/myhhub/stock) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell, JSON, and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include scheduled cron payloads, portfolio-memory updates, and credential-handling guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
