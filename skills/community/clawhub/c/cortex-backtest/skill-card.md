## Description:

Cortex Backtest helps agents configure and run daily quantitative strategy backtests using JQData-style strategy code and Cortex CLI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnluicn](https://clawhub.ai/user/johnluicn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative strategy authors use this skill to set up Cortex backtesting scenarios, clarify JQData-compatible strategy requirements, generate or adapt strategy code, run daily backtests, and interpret generated reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask an agent to persist new lessons into future instruction files or modify shared workspace registration.

Mitigation: Require explicit user approval before file changes, review any appended experience entries before reuse, and prefer tenant- or workspace-local configuration.

Risk: The setup guidance includes privileged system configuration commands.

Mitigation: Do not run sudo automatically; prefer workspace or tenant-local setup unless an operator deliberately performs system-level configuration.

Risk: Strategy examples and APIs use order terminology that could be confused with live trading actions.

Mitigation: Confirm the tool is operating only in backtest or simulation mode before using order APIs or generated strategy examples.

## Reference(s):

- [Cortex API Reference](references/cortex-api-reference.md)
- [Cortex CLI Usage](references/cortex-cli-usage.md)
- [Cortex Experience](references/cortex-experience.md)
- [ClawHub Skill Page](https://clawhub.ai/johnluicn/skills/cortex-backtest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, configuration snippets, and backtest report summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference generated backtest files such as summary.json, account.csv, positions.csv, orders.json, and run.log.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
