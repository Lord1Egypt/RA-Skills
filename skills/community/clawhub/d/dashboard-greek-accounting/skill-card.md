## Description: <br>
Business intelligence dashboard for Greek accounting firms. Compliance status, alerts, deadline tracking, and financial metrics at a glance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Accounting firm assistants use this skill to monitor Greek client portfolios, deadlines, compliance status, financial metrics, and alert queues from local OpenClaw data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated dashboard reports can contain sensitive accounting and client financial data. <br>
Mitigation: Restrict access to OPENCLAW_DATA_DIR and generated report directories to approved accounting staff. <br>
Risk: Optional Slack, email, SMS, and calendar delivery can expose alerts or reports to unintended recipients if misconfigured. <br>
Mitigation: Enable delivery channels only for approved recipients and review webhook, SMTP, SMS, and calendar settings before use. <br>
Risk: Email alerting may require credentials. <br>
Mitigation: Use dedicated low-privilege SMTP credentials or app passwords rather than a primary account password. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/satoshistackalotto/dashboard-greek-accounting) <br>
- [Publisher profile](https://clawhub.ai/user/satoshistackalotto) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured dashboard summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq and OPENCLAW_DATA_DIR; optional Slack, email, SMS, and Google Calendar settings enable delivery channels.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
