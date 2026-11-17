## Description:

Report local OpenClaw token usage to ClawRank (clawrank.dev), the AI agent leaderboard, when the user asks to submit, sync, report, upload usage stats, get ranked, or set up automated ingestion via cron.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hansenliang](https://clawhub.ai/user/hansenliang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to aggregate local agent session usage, submit daily leaderboard facts to ClawRank, and optionally configure recurring daily submissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends aggregate OpenClaw usage, GitHub username, and GitHub activity metrics to ClawRank.

Mitigation: Install and run it only if that sharing is acceptable; use dry-run mode first when reviewing what it will aggregate.

Risk: Auto-setup can send the user's GitHub CLI token to ClawRank in exchange for a ClawRank API token.

Mitigation: Prefer manually generating and configuring a ClawRank API token unless the user explicitly trusts the ClawRank auto-setup flow.

Risk: Endpoint overrides can redirect submissions to a non-default service.

Mitigation: Use the default ClawRank endpoint unless the user intentionally provides and trusts an alternate endpoint.

Risk: Recurring ingestion submits metrics daily after being enabled.

Mitigation: Enable the recurring job only after explicit user consent and provide the documented cron removal command when setting it up.

## Reference(s):

- [ClawRank on ClawHub](https://clawhub.ai/hansenliang/skills/clawrank)
- [ClawRank](https://clawrank.dev)
- [ClawRank Registration](https://clawrank.dev/register)
- [GitHub CLI](https://cli.github.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and script output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit JSON payloads to the configured ClawRank API endpoint when run in live mode.]

## Skill Version(s):

2.5.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
