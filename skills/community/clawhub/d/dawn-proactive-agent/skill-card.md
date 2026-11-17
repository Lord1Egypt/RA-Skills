## Description:

Dawn Agent v1.5 self-evolution proactive architecture. P0-P4 framework for autonomous ETF trading agent with self-reflection, state machine, audit trail, multi-dimension scoring, and safety guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chen6896qqwee](https://clawhub.ai/user/chen6896qqwee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-agent operators use this skill to run and monitor an autonomous ETF rotation workflow for the A-share market, including market analysis, decision logging, state recovery, reflection, and optional trade execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect a trading account when run with execution enabled.

Mitigation: Use paper trading or dry-run mode first and require explicit user approval before any live order submission.

Risk: Advertised guardrails may not be enforced at every order-submission path.

Mitigation: Review the guardrail flow and protect order submission with enforced pre-trade checks before deployment.

Risk: The skill depends on external OpenClaw skills and network destinations for market data and trading operations.

Mitigation: Verify external skills, credentials, and allowed network destinations before installation or scheduled use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chen6896qqwee/skills/dawn-proactive-agent)
- [Publisher profile](https://clawhub.ai/user/chen6896qqwee)
- [Proactive demo trace](samples/proactive_demo.md)
- [Eastmoney market data endpoint](https://push2.eastmoney.com)
- [Zhangle API destination](https://api.zhangle.com)
- [Sina news destination](https://www.sina.com.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON files, Trading guidance]

**Output Format:** [Markdown and console text with JSON audit, state, and analysis files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit market orders when execution mode is enabled.]

## Skill Version(s):

1.5.0 (source: server release metadata and skill changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
