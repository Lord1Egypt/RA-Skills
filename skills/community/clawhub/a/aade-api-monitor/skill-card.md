## Description:

Real-time monitoring of Greek AADE tax authority systems, including deadlines, rate changes, compliance updates, announcements, and system status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto)

### License/Terms of Use:


## Use Case:

External accounting teams and developers use this skill to monitor Greek AADE tax authority updates, detect deadline or rate changes, track system outages, and prepare alerts, reports, and compliance dashboard data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive AADE credentials are required for monitoring.

Mitigation: Run the skill only where credentials can be isolated, and use least-privilege or dedicated AADE credentials if available.

Risk: External notification and calendar integrations may send client or compliance information outside the local environment.

Mitigation: Enable Slack, SMS, email, and calendar integrations only after confirming what data is sent, who receives it, and whether client notifications require manual approval.

Risk: Compliance alerts or generated client communications may be incorrect or incomplete.

Mitigation: Review detected changes, alert drafts, and client notifications before acting on them or sending them externally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/satoshistackalotto/skills/aade-api-monitor)
- [AADE main website](https://www.aade.gr)
- [TAXISnet portal](https://www1.aade.gr/taxisnet)
- [AADE myDATA API](https://mydatapi.aade.gr)
- [AADE press releases](https://www.aade.gr/deltia-typou)
- [AADE legislation](https://www.aade.gr/nomothesia)
- [EFKA portal](https://www.efka.gov.gr)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON files, guidance]

**Output Format:** [Markdown guidance with shell commands, YAML and JSON configuration examples, JSON exports, and Greek-language alert and report text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq, curl, OPENCLAW_DATA_DIR, AADE_USERNAME, and AADE_PASSWORD; optional Slack, SMS, Google Calendar, and Outlook Calendar integrations may affect delivery behavior.]

## Skill Version(s):

0.1.0 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
