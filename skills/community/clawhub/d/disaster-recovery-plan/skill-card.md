## Description:

Writes a disaster recovery plan for a service or system, including RPO/RTO targets, failure scenario runbooks, backup and restore procedures, DR testing cadence, and communication templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and on-call responders use this skill to draft DR plans, define RPO/RTO targets, document failover and recovery runbooks, and prepare disaster recovery game days.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated DR commands can affect production systems if copied and run without review.

Mitigation: Treat commands as operational templates; verify, adapt, and test them against the target infrastructure before use.

Risk: Untested or placeholder recovery values can make a DR plan misleading during an incident.

Mitigation: Replace placeholders with service-specific RPO/RTO targets, contacts, infrastructure details, and run tested DR exercises before relying on the plan.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mohitagw15856/skills/disaster-recovery-plan)
- [Skill Homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/disaster-recovery-plan.html)
- [AWS Health Status](https://health.aws.amazon.com/health/status)
- [Google Cloud Service Health](https://status.cloud.google.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown document with tables, checklists, communication templates, and inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes placeholders for service-specific values, contacts, infrastructure details, and recovery targets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
