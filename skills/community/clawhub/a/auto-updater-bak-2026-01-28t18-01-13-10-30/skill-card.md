## Description:

Automatically update Clawdbot and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicoataiza](https://clawhub.ai/user/nicoataiza)

### License/Terms of Use:


## Use Case:

Developers and Clawdbot users use this skill to schedule daily checks that update Clawdbot and installed skills, then receive a concise report of updated components and errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A scheduled agent task can automatically update Clawdbot and every installed skill without per-update review.

Mitigation: Prefer dry-run or notification-only checks, pin or approve versions, and limit automatic updates to selected trusted skills before enabling the schedule.

Risk: The daily cron job changes installed software and skill files on an ongoing basis.

Mitigation: Confirm the cron configuration and write permissions, review each update summary, and verify that the cron job can be removed or disabled before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nicoataiza/skills/auto-updater-bak-2026-01-28t18-01-13-10-30)
- [Agent Implementation Guide](references/agent-guide.md)
- [Update Summary Examples](references/summary-examples.md)
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating)
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub)
- [Cron Jobs](https://docs.clawd.bot/cron)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup commands, update status summaries, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
