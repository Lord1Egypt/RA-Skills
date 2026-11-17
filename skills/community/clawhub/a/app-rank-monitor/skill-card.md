## Description:

Monitors Apple and Diandian app ranking data, generates daily Markdown reports, and sends DingTalk notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cfans731](https://clawhub.ai/user/cfans731)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to collect app-store ranking data, generate daily ranking summaries, and distribute reports through DingTalk. It is intended for recurring app-market monitoring workflows that need Apple RSS and Diandian data sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes real DingTalk credentials and default notification targets.

Mitigation: Remove committed secrets, rotate exposed credentials, and ship only example configuration files.

Risk: Diandian credentials and cookies may be stored in plaintext configuration or session files.

Mitigation: Store credentials and cookies in a protected secret store with least-privilege access and regular rotation.

Risk: Persistent browser automation and long-lived CDP sessions increase exposure if the host session is compromised.

Mitigation: Run browser automation only when needed, isolate browser profiles, and close remote debugging sessions after use.

Risk: Scheduled execution can keep collecting data and sending notifications after a user expects the workflow to stop.

Mitigation: Make scheduling opt-in and document clear disable and uninstall steps for launchd or OpenClaw cron jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cfans731/skills/app-rank-monitor)
- [Artifact README](artifact/README.md)
- [Diandian monitoring guide](artifact/README_DIANDIAN.md)
- [Scheduled task configuration](artifact/docs/定时任务配置说明.md)
- [Platform mapping notes](artifact/docs/平台映射说明.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown reports, CLI text output, DingTalk messages, and downloaded spreadsheet files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured ranking data sources and notification credentials.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
