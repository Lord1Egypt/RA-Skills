## Description: <br>
Track lab equipment calibration dates and send maintenance reminders for pipettes, balances, centrifuges, and other instruments. Validates date formats and supports update/delete operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Lab staff, compliance owners, and developers use this skill to maintain local equipment calibration records, check overdue or upcoming maintenance, and generate audit-oriented reminder reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Equipment names, calibration dates, intervals, and locations are stored locally on the user's machine. <br>
Mitigation: Use the skill only when local storage of equipment and location metadata is acceptable, and protect or delete ~/.openclaw/equipment_log.json when that metadata is sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/equipment-maintenance-log-1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON compliance reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local equipment records are stored in ~/.openclaw/equipment_log.json by the packaged script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
