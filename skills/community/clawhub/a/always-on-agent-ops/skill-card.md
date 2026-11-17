## Description:

Helps OpenClaw operators keep unattended agents observable with queue preflight checks, scheduled jobs, event dispatch, OAuth-expiry alerts, and log retention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexbloch-ia](https://clawhub.ai/user/alexbloch-ia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor and dispatch work on an OpenClaw host they control, detect expiring authentication, and manage scheduled log cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queue credentials or private payloads could be exposed through stored files or notifications.

Mitigation: Use a read-only queue token in a 600/400-permission file outside the workspace; keep secrets and private payloads out of notification channels.

Risk: Unattended jobs could execute with broader permissions than intended.

Mitigation: Review each cron before enabling it and keep runtime execution permissions as narrow as possible.

Risk: Log cleanup can delete retained files when armed.

Mitigation: Review purge dry-run output before setting PURGE_DRY_RUN=0.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/alexbloch-ia/skills/always-on-agent-ops)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with shell and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes status-line conventions and JSON status examples.]

## Skill Version(s):

1.3.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
