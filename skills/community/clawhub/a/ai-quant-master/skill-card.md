## Description:

Provides end-to-end AI quant trading guidance for QMT market data, factor construction, QuestDB storage, Backtrader analysis, OpenClaw multi-agent workflows, Feishu integration, and live trading operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haohanyang92](https://clawhub.ai/user/haohanyang92)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, quant traders, and agent builders use this skill to assemble a Chinese A-share quant workflow covering data collection, factor research, backtesting, agent coordination, reporting, and QMT execution planning. It is most useful as implementation guidance that should be adapted and reviewed before any paper-trading or live-trading deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill normalizes live automated trading and QMT order execution.

Mitigation: Run first in an isolated paper-trading environment and require explicit human approval before any live order is sent.

Risk: Deployment guidance includes remote installer and administrator or global installation patterns.

Mitigation: Do not pipe remote installers directly into a shell; pin and verify dependencies and avoid administrator or global installs where possible.

Risk: QMT, Feishu, model-provider, and database credentials can be exposed or reused insecurely.

Mitigation: Keep secrets out of command history and source files, rotate exposed credentials, and change default database credentials before connecting real systems.

## Reference(s):

- [AI全栈量化 Master on ClawHub](https://clawhub.ai/haohanyang92/skills/ai-quant-master)
- [QMT configuration guide](references/qmt-setup.md)
- [Factor research methods](references/factor-research.md)
- [Backtesting methods](references/backtest.md)
- [QuestDB usage guide](references/questdb.md)
- [OpenClaw deployment guide](references/openclaw-deploy.md)
- [Multi-agent architecture](references/multi-agent.md)
- [OpenClaw skills system](references/skills-system.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python, SQL, shell, JSON, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe CSV, JSON, and text report files for quant research, risk review, and trading workflow handoffs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
