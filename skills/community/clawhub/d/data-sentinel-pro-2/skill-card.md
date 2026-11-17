## Description:

Monitors webpages, product prices, and competitor pages around the clock and alerts when monitored content changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anson125chen](https://clawhub.ai/user/anson125chen)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operations teams use this skill to monitor selected URLs for price or content changes, store local change state, and receive change alerts when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches monitored URLs and can run repeatedly through cron, which may create network, privacy, or policy exposure if pointed at sensitive targets.

Mitigation: Monitor only URLs the user is authorized to access, avoid private dashboards, account pages, internal hosts, and cloud metadata URLs, and apply network controls for recurring jobs.

Risk: Configured Telegram alerts may send monitored URL details and change summaries outside the local machine.

Mitigation: Review notification destinations and alert text before enabling Telegram, and keep credentials in environment variables or local configuration outside version control.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anson125chen/skills/data-sentinel-pro-2)
- [Project Documentation](https://github.com/anson125chen/data-sentinel-pro)
- [Publisher Website](https://asmartglobal.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local monitoring state and optional notification text when executed with user-provided URLs and alert settings.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
