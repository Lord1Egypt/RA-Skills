## Description:

Automatically update Clawdbot and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tigertamvip](https://clawhub.ai/user/tigertamvip)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClawHub users use this skill to configure daily unattended updates for Clawdbot and installed skills, then receive concise status summaries after each run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates a persistent daily job that can change Clawdbot and every installed skill without fresh approval each time.

Mitigation: Install only when unattended updates are intended; run a dry run first, limit updates to trusted skills or approved versions, use a least-privileged account, and confirm how to inspect and remove the cron job.

## Reference(s):

- [Agent Implementation Guide](references/agent-guide.md)
- [Update Summary Examples](references/summary-examples.md)
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating)
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub)
- [Cron Jobs](https://docs.clawd.bot/cron)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce cron commands, updater script snippets, dry-run checks, and concise update summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
