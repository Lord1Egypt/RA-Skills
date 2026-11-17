## Description:

Institutional-grade execution playbook for the published `duola` Polymarket copy-trading CLI in lobster-agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duolaamengweb3](https://clawhub.ai/user/duolaamengweb3)

### License/Terms of Use:


## Use Case:

External operators and developers use this skill to install and operate the `duola` Polymarket copy-trading CLI, onboard leaders, sync trades, run backtests and diagnostics, start or stop autopilot, and return structured risk and performance summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and operates a mutable trading CLI that can control live automated trading.

Mitigation: Install only after independently trusting the `duola` package and publisher, prefer a pinned and verified local install, and use staged rollout through sync, backtest, doctor checks, and limited live cycles before detached autopilot.

Risk: The workflow handles financial secrets, wallet private keys, and SkillPay credentials.

Mitigation: Use a dedicated low-value wallet, provide private keys through stdin rather than shell history, protect SkillPay credentials, and monitor or stop detached live-trading processes promptly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duolaamengweb3/skills/duola-quant-copy-engine)
- [SkillPay](https://skillpay.me)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and structured JSON-style summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include leader, sync, backtest, doctor, autopilot, billing, risk, and performance fields.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
