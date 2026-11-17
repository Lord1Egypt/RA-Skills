## Description:

Builds a multi-agent orchestration harness for OpenClaw or similar systems, including an orchestrator spec, agent tiers, routing rules, model assignment, memory limits, communication channels, and implementation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plbirrell](https://clawhub.ai/user/plbirrell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to design and hand off a documented agent-fleet orchestration setup. It is suited to teams that need an orchestrator, agent roster, routing rules, context controls, communication channels, and implementation steps for a multi-agent workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared context and agent memory templates can expose broad client or business information to more agents than necessary.

Mitigation: Partition shared memory by project or sensitivity, keep context narrowly scoped, and review generated files before deployment.

Risk: Slack tokens, logs, gateway services, and scheduled jobs require operational review before use.

Mitigation: Treat tokens and logs as secrets, rotate credentials on a schedule, and require explicit approval before enabling background services or cron workflows.

Risk: Generated orchestration guidance may create brittle routing, excessive context sharing, or inappropriate escalation paths if copied without adaptation.

Mitigation: Adapt the templates to the actual agent roster, tools, authority boundaries, and sensitive-decision rules before handing them to an orchestrator.

## Reference(s):

- [Read This First Template](references/read-this-first-template.md)
- [Harness Architecture Template](references/architecture-template.md)
- [Agent Profiles Template](references/agent-profiles-template.md)
- [System Prompt Template](references/system-prompt-template.md)
- [Implementation Guide Template](references/implementation-guide-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown document set with configuration snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces five handoff-oriented documents unless the user asks for a subset.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
