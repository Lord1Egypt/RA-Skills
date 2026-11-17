## Description:

Automatically update Clawdbot and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninwonk](https://clawhub.ai/user/ninwonk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure recurring Clawdbot and skill updates, then receive concise update summaries after each run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended recurring updates can change Clawdbot and installed skills without per-update approval.

Mitigation: Configure dry-run or notify-only behavior first and review proposed versions before allowing automatic application.

Risk: Automatic updates may introduce regressions or incompatible skill changes.

Mitigation: Keep a rollback path and record versions before and after each update.

Risk: A persistent cron job can continue modifying the installation after the user no longer wants automatic updates.

Mitigation: Remove the cron job or disable cron when recurring agent sessions are no longer intended.

## Reference(s):

- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating)
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub)
- [Cron Jobs](https://docs.clawd.bot/cron)
- [Agent Implementation Guide](references/agent-guide.md)
- [Update Summary Examples](references/summary-examples.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Markdown, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup steps, cron configuration, update commands, and human-readable update summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
