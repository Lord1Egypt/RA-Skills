## Description:

Automatically update Clawdbot and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pntrivedy](https://clawhub.ai/user/pntrivedy)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to configure an agent-managed daily update routine for Clawdbot and installed ClawHub skills, with a concise status report after each run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A daily unattended job can update Clawdbot and every installed skill without per-update review.

Mitigation: Run a dry-run or check-only command before enabling automatic updates, review available changes, pin or allowlist trusted components where possible, and confirm the cron job can be removed or disabled.

Risk: Update failures can leave Clawdbot or skills partially updated.

Mitigation: Require the update summary to report successes and errors clearly, then use the documented manual commands and troubleshooting steps to verify versions or repair failed updates.

## Reference(s):

- [Agent Implementation Guide](references/agent-guide.md)
- [Update Summary Examples](references/summary-examples.md)
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating)
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub)
- [Cron Jobs](https://docs.clawd.bot/cron)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup, verification, troubleshooting, and update-summary guidance for the agent.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
