## Description:

Auto-rollback protection for config changes. Backs up before edit, sets a 5-minute system timer to restore if things go wrong. Works with any service config, not just OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2233admin](https://clawhub.ai/user/2233admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill before editing service configuration files to have an agent create a backup, schedule a rollback command, and provide cancellation steps after validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled host-level rollback commands can overwrite system configuration after the agent session ends.

Mitigation: Require the agent to show the exact file, backup path, service reload command, scheduled job ID, and cancellation check before applying the rollback timer.

Risk: Using rollback automation on SSH, firewall, DNS, or production configuration can still cause lockout or service disruption if no independent recovery path exists.

Mitigation: Avoid these targets unless there is a separate recovery channel and the operator has reviewed the planned restore command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2233admin/skills/config-rollback)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes backup paths, scheduled restore commands, scheduled job IDs, and cancellation checks when applied.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
