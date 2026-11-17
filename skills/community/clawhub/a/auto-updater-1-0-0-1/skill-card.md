## Description:

Automatically update Clawdbot and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gwsq](https://clawhub.ai/user/gwsq)

### License/Terms of Use:


## Use Case:

Developers and Clawdbot users use this skill to configure scheduled checks that update Clawdbot and installed skills, then receive a concise status summary. It is intended for users who deliberately want unattended daily updates and understand the operational risk of changing installed tooling without per-update review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent daily updater can change Clawdbot and all installed skills without per-update review.

Mitigation: Use the skill only when unattended updates are intentional; prefer dry-run or notify-only checks, pin or review versions where possible, and keep the cron job easy to disable.

Risk: Update commands may modify user tooling with permissions that are broader than needed.

Mitigation: Run the updater without elevated privileges and ensure the Gateway user has only the write access required for the intended skill directories.

Risk: Update summaries can disclose installed skill names, versions, errors, or operational details to external delivery providers.

Mitigation: Review delivery settings before enabling provider delivery and avoid sending update summaries to third-party messaging providers unless that disclosure is acceptable.

## Reference(s):

- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating)
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub)
- [Cron Jobs](https://docs.clawd.bot/cron)
- [Agent Implementation Guide](artifact/references/agent-guide.md)
- [Update Summary Examples](artifact/references/summary-examples.md)
- [ClawHub Skill Page](https://clawhub.ai/gwsq/skills/auto-updater-1-0-0-1)
- [Publisher Profile](https://clawhub.ai/user/gwsq)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cron setup commands, update status summaries, troubleshooting guidance, and disablement instructions.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
