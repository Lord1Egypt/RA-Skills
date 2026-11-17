## Description:

Agent workspace for researching programmatic trading strategies through generative optimization with bounded files and fixed backtesting evaluator.

This skill is for research and development only.

## Publisher:

[lavapapa](https://clawhub.ai/user/lavapapa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and trading-system experimenters use this skill to set up a bounded coding-agent workspace for historical strategy backtesting, strategy iteration, and result notes. It is intended for research workflows, not live trading or financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The autonomous loop can run agent-written Python and shell-capable agents without strong containment.

Mitigation: Run it only in a disposable workspace or container, review generated strategy code before executing backtests, and keep run lengths short unless explicitly approved.

Risk: Credential or account exposure could occur if broker keys, cloud tokens, SSH credentials, or sensitive environment variables are present.

Mitigation: Use an environment with no broker keys, cloud tokens, SSH credentials, or sensitive environment variables available to the agent.

Risk: Backtest outputs can be misleading if treated as proof of future returns or as financial advice.

Mitigation: Present results as historical research leads only, avoid live-trading integration, and do not connect the workspace to real trading accounts.

## Reference(s):

- [AutoTradeResearch homepage](https://github.com/lavapapa/AutoTradeResearch)
- [AutoTradeResearch ClawHub page](https://clawhub.ai/lavapapa/skills/autotraderesearch)
- [AutoResearch inspiration](https://github.com/karpathy/autoresearch)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code and shell commands; generated workspace files include Python strategy code, TSV results, and Markdown reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are research artifacts from historical backtests and should not be treated as trading recommendations.]

## Skill Version(s):

0.2.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
