## Description:

Automatically update Clawdbot and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kellanlab](https://clawhub.ai/user/kellanlab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Clawdbot users use this skill to configure daily automated checks that update Clawdbot and installed skills, then receive a concise update summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a persistent daily cron job that updates Clawdbot and installed skills without per-update approval.

Mitigation: Run a dry run first, review update changelogs, limit automatic updates to trusted skills where possible, and confirm the cron job schedule before enabling it.

Risk: Automatic updates can change every installed skill and may introduce unexpected behavior.

Mitigation: Keep a record of installed versions, review the delivered update summary after each run, and remove the `Daily Auto-Update` cron job if unexpected changes occur.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kellanlab/skills/auto-updater-bak)
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating)
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub)
- [Cron Jobs](https://docs.clawd.bot/cron)
- [Agent Implementation Guide](references/agent-guide.md)
- [Update Summary Examples](references/summary-examples.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup, verification, troubleshooting, and summary-reporting guidance for an agent.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
