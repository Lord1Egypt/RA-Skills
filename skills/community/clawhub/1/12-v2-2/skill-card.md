## Description: <br>
AI量化交易系统，8因子信号系统、多数据源容错、实时行情分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nidhov01](https://clawhub.ai/user/nidhov01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze stocks, generate multi-factor trading signals, run backtests, monitor market conditions, and configure optional notifications. Outputs should be treated as research signals rather than investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading alerts can send sensitive financial signals to external notification services. <br>
Mitigation: Disable notification channels unless explicitly needed, review recipients and webhook destinations, and confirm what messages may leave the machine before adding credentials. <br>
Risk: SMTP, webhook, Telegram, and AI API credentials may be placed in configuration. <br>
Mitigation: Use environment variables or local secret handling, avoid committing real credentials, and remove channels that are not required. <br>
Risk: Trading recommendations may be incorrect, stale, or unsuitable for real capital. <br>
Mitigation: Treat outputs as research signals, validate with backtesting or paper trading, and apply independent review before trading. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nidhov01/12-v2-2) <br>
- [V2.2 complete deployment and usage guide](artifact/docs/V2.2完整部署与使用指南.md) <br>
- [V2.2 integration architecture design](artifact/docs/V2.2集成架构设计.md) <br>
- [File index](artifact/docs/文件索引.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets plus YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce stock analysis summaries, signal scores, backtest metrics, notification setup guidance, and risk alerts.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; artifact system version: 2.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
