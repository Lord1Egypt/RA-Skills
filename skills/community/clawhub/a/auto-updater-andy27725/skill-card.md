## Description:

Automatically update Clawdbot and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andy27725](https://clawhub.ai/user/andy27725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Clawdbot users use this skill to configure daily update checks for Clawdbot core and installed skills, then receive a concise update summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a persistent daily cron job that updates Clawdbot and all installed skills without reviewing each update first.

Mitigation: Enable it only when unattended updates are intended; prefer dry-run or approval-based checks, pin or allowlist trusted components where possible, and confirm the removal command before deployment.

Risk: Automatic updates can fail because of permissions, network problems, or package conflicts.

Mitigation: Review delivered update summaries, keep logging enabled for the update routine, and use the documented manual commands to diagnose and rerun failed updates.

## Reference(s):

- [Agent Implementation Guide](references/agent-guide.md)
- [Update Summary Examples](references/summary-examples.md)
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating)
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub)
- [Cron Jobs](https://docs.clawd.bot/cron)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup guidance, cron commands, update-check commands, and human-readable update summaries.]

## Skill Version(s):

1.0.0 (source: server evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
