## Description:

HEARTBEAT.md framework for continuous business monitoring — sites, services, inbox, payments, processes, and revenue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeytbuilds](https://clawhub.ai/user/joeytbuilds)

### License/Terms of Use:

MIT-0

## Use Case:

Operators, founders, and support teams use this skill to create a HEARTBEAT.md routine for recurring business monitoring. It helps an agent check production sites, services, customer support queues, payments, revenue, and background processes while documenting escalation tiers and daily notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives agents broad authority over production recovery and process termination.

Mitigation: Use explicit allowlists, least-privilege read-only access by default, and human approval before production changes, process termination, or restarts.

Risk: The skill includes customer replies and payment retries in monitored workflows.

Mitigation: Require approval gates for customer-facing messages and payment retries, with clear logging, retry limits, and rollback procedures.

Risk: The security verdict is suspicious because the monitoring template lacks enough scoping and approval gates.

Mitigation: Review and tailor the skill before installing it in a real business environment, then document alert channels, escalation thresholds, and audit logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joeytbuilds/skills/business-heartbeat-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown templates and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a HEARTBEAT.md monitoring template, nightly review template, setup checklist, and autonomy-tier guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
