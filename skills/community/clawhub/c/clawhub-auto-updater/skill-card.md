## Description:

Automatically update Clawdbot and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kendrick-lu](https://clawhub.ai/user/kendrick-lu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Clawdbot users use this skill to configure scheduled update checks for Clawdbot and installed ClawHub skills, then receive concise update summaries after each run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Daily automatic updates can give a persistent scheduled job authority to change Clawdbot and every installed skill without per-update review.

Mitigation: Prefer check-and-report mode, limit updates to trusted or pinned skills, or require approval before applying core or skill changes.

Risk: Update failures may leave Clawdbot or skills partially updated.

Mitigation: Review the delivered summary after each run, inspect errors, and use the documented manual update commands when intervention is needed.

## Reference(s):

- [Agent Implementation Guide](references/agent-guide.md)
- [Update Summary Examples](references/summary-examples.md)
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating)
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub)
- [Cron Jobs](https://docs.clawd.bot/cron)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces cron setup instructions, update commands, verification steps, and user-facing update summaries.]

## Skill Version(s):

1.0.0 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
