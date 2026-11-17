## Description:

Guides agents through Facebook Page operations via Meta Business Suite, including role separation, scheduled DM and comment handling, moderation discipline, Page Quality-aware gating, and recovery playbooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexbloch-ia](https://clawhub.ai/user/alexbloch-ia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agencies managing Facebook brand Pages use this skill to configure cautious Meta Business Suite based automation for scheduled Page DMs, comment replies, moderation, state tracking, and recovery while preserving Page Quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Facebook Page or account restrictions may result from unauthorized or over-broad automation.

Mitigation: Use the skill only for Facebook Pages you own or are authorized to manage, review cron jobs before enabling them, and require manual review before expanding beyond Phase A.

Risk: Workspace memory files and webhook alerts may contain sensitive operational details.

Mitigation: Keep workspace memory files and webhook alert channels private, and use a dedicated browser profile for Facebook Page operations.

Risk: Moderation actions such as deleting comments, banning users, or increasing automation scope can create account-management and reputation risk.

Mitigation: Require manual review before deleting comments, banning users, or expanding automation, and follow the artifact's Page Quality checks and recovery playbooks.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/alexbloch-ia/skills/facebook-account-operations)
- [OpenClaw](https://openclaw.ai)
- [Claude Code](https://claude.ai/code)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with YAML configuration and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operating procedures, quotas, checklists, memory-file conventions, and recovery guidance; does not execute Facebook actions by itself.]

## Skill Version(s):

1.0.0 (source: server release metadata and README badge)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
