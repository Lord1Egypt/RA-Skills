## Description:

Automatically update Clawdbot and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[make453](https://clawhub.ai/user/make453)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure daily Clawdbot and installed-skill update checks, apply updates, and receive concise update summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended daily jobs can change Clawdbot and every installed skill without a fresh approval step.

Mitigation: Use check-only or dry-run mode first, review exact versions before enabling installation, and limit automatic updates to trusted skills.

Risk: A cron schedule can run at an unexpected time if the timezone or cadence is wrong.

Mitigation: Confirm the cron expression and timezone before enabling the job, and document the removal command.

Risk: Update failures can leave Clawdbot or installed skills only partially updated.

Mitigation: Report partial success and errors clearly, then provide manual update or rollback guidance for failed components.

## Reference(s):

- [Auto Updater Backup on ClawHub](https://clawhub.ai/make453/skills/auto-updater-backup)
- [Agent Implementation Guide](references/agent-guide.md)
- [Update Summary Examples](references/summary-examples.md)
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating)
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub)
- [Cron Jobs](https://docs.clawd.bot/cron)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Markdown, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cron schedules, update commands, setup checks, troubleshooting steps, and user-facing update summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json; artifact frontmatter metadata lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
