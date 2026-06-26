## Description: <br>
Real-time monitoring of Greek AADE tax authority systems for deadlines, rate changes, compliance updates, and file-based OpenClaw workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Accounting teams and OpenClaw users use this skill to monitor Greek AADE tax authority updates, deadlines, rate changes, and system availability, then prepare alerts, reports, calendar updates, and compliance summaries for review. <br>

### Deployment Geography for Use: <br>
Greece <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive AADE tax credentials. <br>
Mitigation: Use least-privileged AADE credentials, store secrets securely, and review the skill before installation. <br>
Risk: The skill describes client notifications, calendar updates, and submission-workflow delays that could affect compliance operations. <br>
Mitigation: Require human approval before sending client notifications or changing submission workflows, and approve recipients and data contents before enabling Slack, SMS, or calendar outputs. <br>
Risk: The skill depends on jq and curl for operation. <br>
Mitigation: Install jq and curl separately through a trusted administrator process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/satoshistackalotto/aade-api-monitor) <br>
- [AADE](https://www.aade.gr) <br>
- [TAXISnet](https://www1.aade.gr/taxisnet) <br>
- [myDATA API](https://mydatapi.aade.gr) <br>
- [EFKA](https://www.efka.gov.gr) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with command examples and structured configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq, curl, OPENCLAW_DATA_DIR, AADE_USERNAME, and AADE_PASSWORD; optional Slack, SMS, Google Calendar, and Outlook Calendar integrations are described.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
