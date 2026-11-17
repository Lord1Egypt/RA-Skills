## Description:

Automates cryptocurrency portfolio review, exchange balance checks, strategy execution, backtesting, sentiment analysis, monitoring, and emergency stop workflows for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nandichi](https://clawhub.ai/user/nandichi)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage cryptocurrency trading workflows, inspect balances and risk status, run strategy backtests, and operate paper or live trading strategies with exchange API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real-money trading safeguards are not reliably enforced in code.

Mitigation: Review trading safeguards before installation, keep paper or testnet mode enabled, use small limits, and do not enable live trading until a real live-mode authorization gate is implemented.

Risk: Exchange API keys and notification webhooks can expose trading access or sensitive account activity.

Mitigation: Use trade-only API keys with no withdrawal permission, enable IP allowlists where available, and tightly control notification webhook credentials.

Risk: Live-mode behavior may be unsafe because market-order valuation, fill or loss accounting, and PID or state-file handling need correction.

Mitigation: Require corrected valuation, reliable accounting, and safer state handling before using the skill with live funds.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nandichi/skills/crypto-trader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Structured JSON from tool scripts with human-readable Markdown summaries and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include balances, portfolio metrics, strategy status, trade history, sentiment labels, backtest metrics, risk state, and alert or emergency-stop results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
