## Description:

Unified developer operations bridge connecting GitHub, CI/CD, Slack, Discord, and issue trackers into cross-tool automated workflows for notifications, review tracking, summaries, issue sync, flaky test detection, and repository health monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ariktulcha](https://clawhub.ai/user/ariktulcha)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to coordinate GitHub, CI/CD, messaging, and issue tracker activity across pull requests, build failures, review reminders, standup summaries, and deployment notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can connect repositories, CI/CD systems, messaging channels, and issue trackers, creating broad automation reach across development workflows.

Mitigation: Use explicit repository and channel allowlists; avoid granting access to all repositories with push permission unless that scope is intended.

Risk: Automatic posts, issue updates, CI reruns, merges, and recurring schedules can change external systems or broadcast sensitive context.

Mitigation: Require user confirmation before external posts, issue updates, reruns, merges, and recurring schedule creation.

Risk: CI logs, issue details, and pull request context may expose sensitive information when sent to chat systems.

Mitigation: Limit and redact CI logs and issue details before posting to Slack, Discord, Telegram, or other messaging channels.

Risk: Persistent team username mappings may expose or misuse developer identity links across tools.

Mitigation: Review mappings before storage and keep them scoped to the intended workspace or team.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ariktulcha/skills/devops-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and text with optional shell commands, JSON configuration snippets, and external tool action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce chat notifications, pull request and CI summaries, issue tracker updates, scheduled workflow suggestions, and team username mappings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
