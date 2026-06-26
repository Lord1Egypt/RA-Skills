## Description: <br>
提供从QMT行情数据获取、因子构建、回测分析到多智能体协作与实盘交易的全流程AI量化交易指导。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haohanyang92](https://clawhub.ai/user/haohanyang92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, quant traders, and technically skilled retail investors use this skill to build an AI-assisted A-share quant workflow covering QMT data access, factor research, QuestDB storage, Backtrader analysis, OpenClaw multi-agent orchestration, Feishu notifications, and gated live-trading execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live automated trading can place unintended orders or create financial exposure. <br>
Mitigation: Use paper or simulated trading first, require explicit human approval before live orders, and enforce hard exposure, position, and order-size limits. <br>
Risk: QMT and Feishu credentials can be exposed through chats, repositories, logs, or shared configuration. <br>
Mitigation: Keep credentials out of prompts and source control, store them in local secret/configuration stores, and rotate any credential that may have been disclosed. <br>
Risk: Remote installers and plugin commands may execute code from external sources. <br>
Mitigation: Verify installer and plugin sources before running them, pin trusted versions where practical, and run setup in an isolated environment first. <br>
Risk: Bot integrations and multi-agent routing can expand operational permissions. <br>
Mitigation: Grant the minimum Feishu and trading-bot permissions needed, separate research and execution roles, and review generated actions before execution. <br>
Risk: Backtest results may not carry over to live markets because of slippage, liquidity, fees, future-function errors, or changing market regimes. <br>
Mitigation: Validate with out-of-sample tests, include transaction costs and slippage, avoid same-day factor lookahead, and monitor live performance before scaling capital. <br>


## Reference(s): <br>
- [Skill overview](artifact/SKILL.md) <br>
- [QMT setup guide](artifact/references/qmt-setup.md) <br>
- [Factor research methods](artifact/references/factor-research.md) <br>
- [Backtest methods](artifact/references/backtest.md) <br>
- [OpenClaw deployment guide](artifact/references/openclaw-deploy.md) <br>
- [Multi-agent architecture](artifact/references/multi-agent.md) <br>
- [QuestDB guide](artifact/references/questdb.md) <br>
- [OpenClaw skills system](artifact/references/skills-system.md) <br>
- [QMT API example](artifact/examples/qmt-api-example.py) <br>
- [Backtest example](artifact/examples/backtest-example.py) <br>
- [Factor calculation example](artifact/examples/factor-calculation.py) <br>
- [ClawHub release page](https://clawhub.ai/haohanyang92/ai-quant-master) <br>
- [Publisher profile](https://clawhub.ai/user/haohanyang92) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python, SQL, JSON, JavaScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local files such as factor tables, signal CSVs, backtest reports, portfolio JSON, risk reports, trading logs, and Feishu-ready summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
