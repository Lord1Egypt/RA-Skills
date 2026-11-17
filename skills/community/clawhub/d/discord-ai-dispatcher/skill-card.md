## Description:

Routes Discord notifications with deterministic rules and local AI formatting, supports message updates to reduce channel clutter, and provides guidance for resilient webhook-based dispatch pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bhupendrafire-ai](https://clawhub.ai/user/bhupendrafire-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to design Discord webhook notification dispatchers that route alerts by deterministic identifiers, deduplicate sequential updates, format messages with local AI, and keep dashboard-style channels current.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent background notification tasks can continue running after reboot.

Mitigation: Run under a low-privilege account and document how to disable and remove any scheduled task or cron entry.

Risk: Webhook URLs and configuration secrets are stored locally.

Mitigation: Restrict local file permissions and keep webhook secrets out of source control and logs.

Risk: Automatic state reset or replay can resend recent notifications during recovery.

Mitigation: Require manual approval for state resets or replay and review delivery logs before recovery actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bhupendrafire-ai/skills/discord-ai-dispatcher)
- [Artifact README](artifact/readme.md)
- [Artifact Skill Guide](artifact/skill.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with implementation patterns, configuration examples, and command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational recommendations for schedulers, state files, webhook configuration, deduplication logic, and recovery workflows.]

## Skill Version(s):

1.7.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
