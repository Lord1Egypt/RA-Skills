## Description:

CLI tool for tracking Greek tax deadlines (AADE, EFKA). Real-time monitoring with configurable alerts via Slack, SMS, email, or local files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto)

### License/Terms of Use:


## Use Case:

Developers, operators, and accounting teams use this skill to monitor Greek tax, social security, municipal, and system-status deadlines through OpenClaw CLI workflows and generate deadline alerts or reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network alert and calendar integrations may send client or business deadline data outside the local machine.

Mitigation: Enable Slack, SMS, email, Google Calendar, or Outlook integrations only after approving what data can leave the environment and configuring only the required environment variables.

Risk: Background monitoring and scheduling can continue creating logs, caches, reports, or outbound alerts after initial setup.

Mitigation: Confirm scheduled monitors can be disabled and define cleanup procedures for generated logs, caches, reports, and alert state before deployment.

Risk: Setup examples include package installation patterns that may be unsafe if run with elevated privileges without review.

Mitigation: Use a pinned, trusted OpenClaw CLI and avoid sudo-based setup unless approved by an administrator.

Risk: The required local data directory can contain sensitive client compliance data.

Mitigation: Restrict filesystem permissions on OPENCLAW_DATA_DIR and related logs or reports to authorized users only.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/satoshistackalotto/skills/cli-deadline-monitor)
- [AADE status endpoint](https://www1.aade.gr/taxisnet/api/status)
- [AADE myDATA status endpoint](https://mydatapi.aade.gr/api/status)
- [EFKA status endpoint](https://www.efka.gov.gr/api/status)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON and YAML examples, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe local file reads, scheduled monitors, alert channels, report generation, and optional external notification or calendar integrations.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
