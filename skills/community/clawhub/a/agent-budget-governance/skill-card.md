## Description:

Helps multi-agent OpenClaw teams audit daily token budgets, log threshold events, and flag or demote agents that exceed configured limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:


## Use Case:

Developers and operators running OpenClaw multi-agent teams use this skill to audit local BUDGET.json files, produce human-readable or JSON budget reports, and maintain governance logs for threshold events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be mistaken for a complete spend-control or privilege-revocation system.

Mitigation: Treat it as audit and reporting support unless separate OpenClaw gateway or openclaw.json enforcement is implemented.

Risk: Running the audit can update local BUDGET.json state and append governance log entries.

Mitigation: Restrict it to a dedicated agents directory and use backups or dry-run review before scheduling automated runs.

Risk: Malformed or replaced BUDGET.json files could make audit results unreliable.

Mitigation: Ensure agents cannot replace budget files with links or malformed JSON, and validate file ownership and structure before relying on results.

## Reference(s):

- [Agent Governance Framework](artifact/references/GOVERNANCE.md)
- [ClawHub Skill Page](https://clawhub.ai/nissan/skills/agent-budget-governance)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; script output is human-readable text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The audit script reads local agent BUDGET.json files, may update budget status fields, and appends governance log entries.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
