## Description:

Business intelligence dashboard for Greek accounting firms. Compliance status, alerts, deadline tracking, and financial metrics at a glance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto)

### License/Terms of Use:


## Use Case:

Accounting firm assistants use this skill to generate English-language dashboard views for Greek client compliance, deadlines, alerts, document queues, and financial reporting.

### Deployment Geography for Use:

Greece

## Known Risks and Mitigations:

Risk: The install path may pull mutable, unpinned OpenClaw packages and dependencies before the skill handles sensitive accounting data.

Mitigation: Pin the OpenClaw CLI and every skill dependency to reviewed versions before installation.

Risk: Accounting dashboards may expose client tax, payroll, banking, or compliance data to unauthorized recipients.

Mitigation: Enable email, Slack, or SMS alert delivery only after recipient allowlists, credential isolation, audit logging, and client access controls are configured.

Risk: Installing prerequisites with unnecessary privileges can increase operational risk.

Mitigation: Install jq through the organization's normal administrative process and avoid elevated privileges for skill setup unless required.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/satoshistackalotto/skills/dashboard-greek-accounting)
- [Publisher profile](https://clawhub.ai/user/satoshistackalotto)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured dashboard examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq and OPENCLAW_DATA_DIR; optional Slack, email, SMS, and Google Calendar settings enable external alert delivery.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
