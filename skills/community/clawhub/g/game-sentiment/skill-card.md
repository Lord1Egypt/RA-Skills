## Description:

Automated game sentiment monitoring skill for mobile and PC games that scans public feedback across channels, classifies issues, assesses severity and ownership, and generates actionable reports with P1 alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robin9plus1](https://clawhub.ai/user/robin9plus1)

### License/Terms of Use:

MIT-0

## Use Case:

Game operations, product, QA, community, and PR teams use this skill to monitor player sentiment for a specific game, detect negative spikes or post-update issues, and turn public feedback into prioritized action recommendations. It is intended for structured game sentiment reporting rather than one-off searches or non-game brand monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use stored NGA credentials and a YouTube API key.

Mitigation: Use a separate secret manager or dedicated low-privilege accounts, avoid pasting real passwords or API keys into chat, and remove credential paths for channels that are not needed.

Risk: The skill browses many public sites and can send Feishu summaries.

Mitigation: Confirm the enabled channels, scan scope, and Feishu destination before each run, and limit collection to the platforms needed for the monitoring task.

Risk: The skill writes reports, state, and configuration files and security evidence notes that runtime changes can persist into instruction files.

Mitigation: Keep runtime data under the workspace data directory, review generated file changes, and do not allow automated updates to skill source or reference files without human review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/robin9plus1/skills/game-sentiment)
- [Channel Strategy](references/channel-strategy.md)
- [Config Schema](references/config-schema.md)
- [Report Templates](references/report-template.md)
- [Severity Rules](references/severity-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance, Files]

**Output Format:** [Markdown reports and alert summaries, JSON configuration and state files, and browser/API collection commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include channel status, sampling notes, source-backed evidence, P1/P2/P3 severity labels, suggested owners, and recommended actions.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
