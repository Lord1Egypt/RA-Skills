## Description:

Sync your AI coding stats to Code Card - beautiful, shareable developer profiles

This skill is ready for commercial/non-commercial use.

## Publisher:

[eibrahim](https://clawhub.ai/user/eibrahim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and run Code Card CLI syncs for AI coding session statistics from Claude Code, Codex, and OpenClaw, including optional recurring sync schedules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends executing an unpinned npm package with npx.

Mitigation: Pin and review the Code Card CLI version before use instead of relying on the latest published package.

Risk: The skill under-explains what local session data is uploaded during sync.

Mitigation: Confirm the exact data collected and uploaded by Code Card before syncing local coding sessions.

Risk: The recommended cron jobs create unattended recurring syncs.

Mitigation: Add recurring sync jobs only after accepting automated uploads on the configured schedule.

Risk: The setup check can reveal whether a Code Card API key is present in a local file.

Mitigation: Avoid printing or sharing the API key value and treat the local Code Card configuration as sensitive.

## Reference(s):

- [Code Card website](https://www.codecard.dev)
- [Code Card npm package](https://www.npmjs.com/package/code-card)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Code Card CLI setup, sync, stats, profile, and cron scheduling commands.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
