## Description:

Automatically update Clawdbot and all installed skills once daily by configuring scheduled update checks, applying available updates, and reporting what changed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelaner](https://clawhub.ai/user/kelaner)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Clawdbot users use this skill to set up daily automated maintenance for Clawdbot core and installed skills, with a delivered summary of updates and issues. It is intended for users who deliberately want recurring background updates rather than per-update manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended updates can change Clawdbot and all installed skills without per-update review.

Mitigation: Use dry-run notifications or review update summaries before enabling automatic application, and limit updates to trusted skills.

Risk: Scheduled update failures can leave Clawdbot or skills only partially updated.

Mitigation: Require clear error reporting, inspect the auto-update log after failures, and run manual recovery commands only after reviewing the specific failure.

Risk: Cron-based background execution may continue after the user no longer wants automatic updates.

Mitigation: Document and verify the cron removal command before enabling the updater.

## Reference(s):

- [Agent Implementation Guide](references/agent-guide.md)
- [Update Summary Examples](references/summary-examples.md)
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating)
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub)
- [Cron Jobs](https://docs.clawd.bot/cron)
- [Auto Updater.Tmp on ClawHub](https://clawhub.ai/kelaner/skills/auto-updater-tmp)
- [Publisher Profile](https://clawhub.ai/user/kelaner)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, JSON configuration snippets, optional shell script content, and update summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and maintenance instructions for cron-based updates; does not itself guarantee update safety.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
