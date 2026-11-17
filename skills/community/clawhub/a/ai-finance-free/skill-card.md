## Description:

AI驱动金融分析 helps agents perform natural-language finance analysis, quantitative research, and structured report generation from user-provided or public financial data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and finance teams use this skill to request natural-language financial analysis, market sentiment review, metric extraction, portfolio research, and exportable analysis results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad tool access could allow unintended file changes or shell execution during finance-analysis workflows.

Mitigation: Run in a constrained agent environment, require human confirmation for writes and commands, and review generated actions before execution.

Risk: API keys and financial data could be exposed if credentials or sensitive datasets are used without platform controls.

Mitigation: Use only non-sensitive financial data unless credential protection, access control, and audit logging are independently enforced.

Risk: Recurring pushed results or trading-system integrations could act on unclear cadence, destination, permissions, or stop conditions.

Mitigation: Do not permit scheduled jobs, pushed results, or trading-system interactions unless those operating conditions are explicit and approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ai-finance-free)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe API-key configuration, file exports, and scheduled finance-analysis workflows.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
