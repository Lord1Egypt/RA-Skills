## Description:

AI-powered trading bot framework for OpenClaw that connects to crypto exchanges and prediction markets, provides strategy templates and risk management configuration, and supports paper-trading workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevojarvisai-star](https://clawhub.ai/user/stevojarvisai-star)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent builders use this skill to configure trading-bot workflows, run paper trades, inspect risk status, and evaluate built-in strategies for OpenClaw. Treat live-trading behavior as requiring independent review before use with real funds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill overstates live-trading safety features and kill-switch behavior.

Mitigation: Use it as a paper-trading or educational helper only until live behavior, stop-loss protection, drawdown protection, backtesting, multi-exchange automation, and emergency position closure are corrected and independently verified.

Risk: Live trading or trading-capable credentials could expose real funds to incorrect automation or incomplete safeguards.

Mitigation: Do not provide trading-capable API keys for live use; when testing connectivity, use least-privilege keys, disable withdrawals, and prefer sandbox or paper-trading accounts.

Risk: Strategy outputs and risk dashboards can produce incorrect or misleading financial guidance.

Mitigation: Require human review of strategy decisions and risk output before any financial action, and do not rely on the skill as financial advice.

## Reference(s):

- [Built-in Trading Strategies](artifact/references/strategies.md)
- [ClawHub Skill Page](https://clawhub.ai/stevojarvisai-star/skills/agent-trading-bot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference exchange API keys, local OpenClaw configuration files, paper-trading state, and trading logs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
