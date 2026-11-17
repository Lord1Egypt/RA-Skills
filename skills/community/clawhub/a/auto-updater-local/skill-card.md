## Description:

Automatically update Clawdbot and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenlavril](https://clawhub.ai/user/wenlavril)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Clawdbot users use this skill to schedule local daily updates for Clawdbot and installed skills, then receive a concise status report. It is intended for Darwin and Linux environments where the user accepts automated changes to agent tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Daily unattended updates can modify Clawdbot and every installed skill without per-update review.

Mitigation: Prefer check-only or dry-run scheduling, pinned or allowlisted updates, and manual approval before applying core or skill changes.

Risk: The persistent cron job continues to run until the user disables or removes it.

Mitigation: Confirm the user knows how to list, disable, or remove the cron job before enabling automatic updates.

## Reference(s):

- [Agent Implementation Guide](references/agent-guide.md)
- [Update Summary Examples](references/summary-examples.md)
- [ClawHub Skill Page](https://clawhub.ai/wenlavril/skills/auto-updater-local)
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating)
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub)
- [Cron Jobs](https://docs.clawd.bot/cron)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cron schedules, update status summaries, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
