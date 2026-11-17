## Description:

Monitors the FC Online official website for new activity announcements, season-card updates, gift packs, and version changes, then reports relevant updates to the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flaxenhair](https://clawhub.ai/user/flaxenhair)

### License/Terms of Use:

MIT-0

## Use Case:

Players and OpenClaw users use this skill to monitor FC Online website activity pages and receive concise notices when new game events or important updates appear. Developers can also use it as a configurable website-monitoring utility with command-line and OpenClaw integration paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation may perform privileged system changes and create persistence.

Mitigation: Review the installer before running it, use an unprivileged account where possible, and enable the systemd service only when boot-time monitoring is required.

Risk: Configuration, state, and logs may be stored in shared temporary paths.

Mitigation: Move runtime files to a private, user-owned configuration or state directory for any serious deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flaxenhair/skills/fco-monitor)
- [FC Online official site](https://fco.qq.com/main.shtml)
- [FC Online version news page](https://fco.qq.com/webplat/info/news_version3/33965/34617/38284/m22646/list_1.shtml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown or plain-text status reports with command examples and optional JSON output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network-dependent monitoring output; local configuration, state, and logs are used by the artifact scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
