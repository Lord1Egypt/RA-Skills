## Description:

Automatically collects weekly competitor activity, analyzes trends, generates structured reports, and distributes them to configured team channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Product, marketing, and strategy teams use this skill to monitor competitor activity across configured platforms and receive weekly Markdown reports with trends, highlights, and suggested actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable installers and dependent skills may change behavior after installation.

Mitigation: Review and pin the installer and dependent skill versions before installing.

Risk: Scheduled report forwarding may send competitor intelligence to unapproved channels.

Mitigation: Confirm Feishu, DingTalk, email, and n8n destinations are approved before enabling automated distribution.

Risk: Automatically generated reports may contain misleading or sensitive findings.

Mitigation: Add a human review step before scheduled reports are sent automatically.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/skills/competitor-monitor-weekly)
- [Publisher profile](https://clawhub.ai/user/zlszhonglongshen)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON workflow data, YAML configuration, and installation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can be scheduled weekly or triggered manually and may be sent to Feishu, email, DingTalk, or n8n workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
