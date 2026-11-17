## Description:

Automatically update Clawdbot and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[make453](https://clawhub.ai/user/make453)

### License/Terms of Use:

MIT-0

## Use Case:

ClawHub users and agents use this skill to configure scheduled update checks for Clawdbot and installed skills, apply available updates, and report what changed or failed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled auto-updates can change Clawdbot and installed skill behavior without per-update review.

Mitigation: Enable the skill only when automatic changes are acceptable, and prefer dry-run or notification-only workflows where available.

Risk: Updating every installed skill broadens the impact of a bad, unexpected, or untrusted release.

Mitigation: Pin or allowlist trusted skills where possible and review updates before applying them in sensitive environments.

Risk: A recurring cron job may continue applying updates after the user no longer wants automatic changes.

Mitigation: Keep the cron job name and removal command available, and remove or disable the scheduled job before changing update policy.

## Reference(s):

- [Agent Implementation Guide](artifact/references/agent-guide.md)
- [Update Summary Examples](artifact/references/summary-examples.md)
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating)
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub)
- [Cron Jobs](https://docs.clawd.bot/cron)
- [ClawHub Skill Page](https://clawhub.ai/make453/skills/auto-updater-bak2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cron schedules, update commands, troubleshooting steps, and update summary text.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
