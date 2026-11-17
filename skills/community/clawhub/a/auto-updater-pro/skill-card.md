## Description:

Enhanced auto-updater with detailed logging, missed run recovery, and Gateway restart protection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newolf20000](https://clawhub.ai/user/newolf20000)

### License/Terms of Use:

MIT

## Use Case:

Developers and Clawdbot users use this skill to configure recurring update checks for Clawdbot and installed skills, with logging and status summaries for missed or failed runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a persistent daily job that updates Clawdbot and all installed skills without fresh review.

Mitigation: Prefer dry-run or notification-only update checks, or require manual approval before applying updates.

Risk: Updating all installed skills may pull changes from publishers the user does not currently trust.

Mitigation: Pin or approve versions manually and avoid update-all when only some publishers are trusted.

Risk: A recurring updater can continue running after the user no longer wants automatic changes.

Mitigation: Verify how to remove or disable the cron job and confirm where update logs are written.

## Reference(s):

- [Agent Implementation Guide](references/agent-guide.md)
- [Update Summary Examples](references/summary-examples.md)
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating)
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub)
- [Cron Jobs](https://docs.clawd.bot/cron)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May configure a recurring cron job and write update logs when the user proceeds with setup.]

## Skill Version(s):

1.1.0 (source: SKILL.md metadata, _meta.json, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
