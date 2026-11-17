## Description:

Automatically update Clawdbot and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiyuechuimeng](https://clawhub.ai/user/xiyuechuimeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Clawdbot users use this skill to configure a scheduled update routine for Clawdbot and installed skills, with a concise status report after each run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A recurring scheduled job can update Clawdbot and every installed skill without review before each change.

Mitigation: Use a dry-run or notification-only workflow where possible, restrict updates to trusted skills, and review version changes before applying them.

Risk: The updater may run with permissions broad enough to modify user skill directories and tool installations.

Mitigation: Run the job as a low-privilege user and keep a clear removal, rollback, and recovery plan for failed or unwanted updates.

## Reference(s):

- [Agent Implementation Guide](references/agent-guide.md)
- [Update Summary Examples](references/summary-examples.md)
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating)
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub)
- [Cron Jobs](https://docs.clawd.bot/cron)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Markdown, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup guidance and update-summary messaging; no structured API output.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
