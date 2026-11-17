## Description:

csgo monitors CSGO item prices through the CSQAQ API and helps users configure price alerts, market comparisons, and market summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pricnd](https://clawhub.ai/user/pricnd)

### License/Terms of Use:

MIT License

## Use Case:

CSGO item traders and operators use this skill to monitor item prices, compare marketplace gaps, receive alert notifications, and produce short market reports. Developers can configure API credentials, monitor thresholds, notification channels, and scheduled checks around those workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens and webhook URLs can expose credentials or notification endpoints if stored in committed configuration files.

Mitigation: Store the CSQAQ API token and DingTalk or Feishu webhook URLs in private local configuration or environment variables, and avoid committing them.

Risk: Alerts and monitoring data may be sent to external notification providers.

Mitigation: Enable notification channels only after reviewing what alert content is shared with each provider.

Risk: The 1.0.4 release evidence says runnable source files were removed, so the artifact may not provide an executable monitor.

Mitigation: Confirm required runtime files are present, or use a release that includes implementation files, before relying on automated monitoring.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/pricnd/skills/csgo-monitor)
- [Publisher profile](https://clawhub.ai/user/pricnd)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and text responses with configuration snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Current release evidence states that version 1.0.4 retains documentation only and does not include runnable source files.]

## Skill Version(s):

1.0.4 (source: server release evidence; artifact documentation lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
