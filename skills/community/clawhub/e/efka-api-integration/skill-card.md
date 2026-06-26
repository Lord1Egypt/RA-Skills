## Description: <br>
Greek social security (EFKA) integration for employee records, contribution calculations, and APD declarations with human approval for submissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Payroll operators, accounting firms, and developers use this skill to manage Greek EFKA employee records, calculate social security contributions, prepare APD declarations, and coordinate compliance workflows with required human approval before submission. <br>

### Deployment Geography for Use: <br>
Greece <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive EFKA credentials and employee payroll data. <br>
Mitigation: Install only in environments where EFKA credentials and /data/efka/ are restricted to trusted payroll operators. <br>
Risk: Generated APD declarations, lifecycle files, or employee-record changes could be incorrect or submitted prematurely. <br>
Mitigation: Keep the four-eyes approval requirement mandatory and review generated APD and lifecycle files before upload. <br>
Risk: Optional notifications or calendar sync could expose employee personal information. <br>
Mitigation: Avoid sending PII to Slack or calendar integrations and limit notifications to non-sensitive status information. <br>
Risk: The setup guidance includes a sudo dependency installation command. <br>
Mitigation: Run privileged dependency installation only when it matches the organization's approved provisioning process. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/satoshistackalotto/efka-api-integration) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown with command examples and file-organization guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces EFKA workflow guidance, OpenClaw command references, and file-based payroll/compliance outputs for review before use.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
