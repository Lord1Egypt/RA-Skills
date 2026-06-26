## Description: <br>
CLI tool for tracking Greek tax deadlines (AADE, EFKA). Real-time monitoring with configurable alerts via Slack, SMS, email, or local files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and accounting teams use this skill to monitor Greek tax, social security, municipal, and license deadlines from local client data and configured public or notification channels. It helps produce status checks, alerts, exports, and compliance reports for deadline-driven workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan notes that the documented scope, data use, network integrations, and optional credentials are broader than the headline setup indicates. <br>
Mitigation: Review the full skill scope before installation, and enable only the Greek compliance features and data categories needed for the deployment. <br>
Risk: Optional Slack, SMS, SMTP, Google Calendar, and Outlook Calendar integrations may send compliance reminders through external providers. <br>
Mitigation: Configure only approved notification channels, protect the related credentials, and avoid entering broad business address, VAT, property, or permit data unless those features are required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/satoshistackalotto/cli-deadline-monitor) <br>
- [AADE deadline tracker endpoint](https://www.aade.gr/api/deadlines/current) <br>
- [AADE deadline announcements](https://www.aade.gr/epiheiriseis/forologikes-ypohreosieis) <br>
- [EFKA deadline tracker endpoint](https://www.efka.gov.gr/api/deadlines/monthly) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured JSON or YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq and OPENCLAW_DATA_DIR for core local-file deadline tracking; optional Slack, SMS, SMTP, Google Calendar, and Outlook Calendar environment variables enable external alerts.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
