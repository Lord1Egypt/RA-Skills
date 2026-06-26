## Description: <br>
Personal CRM for managing contacts, relationships, follow-ups, reminders, search, and import/export workflows using local markdown files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xz-cn](https://clawhub.ai/user/xz-cn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers use this skill to maintain a personal relationship database, track interactions, schedule follow-ups, and move contact data through markdown, CSV, vCard, and LinkedIn-export workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Contact and relationship information is stored in local agent memory where it can be searched. <br>
Mitigation: Avoid storing secrets or highly sensitive notes, and review what contact data is added to memory. <br>
Risk: Import, export, and output-path workflows can create or disclose contact files. <br>
Mitigation: Review import/export files and destination paths before running scripts, and use dry-run mode for imports. <br>
Risk: Heartbeat reminder checks can create recurring CRM notifications. <br>
Mitigation: Enable HEARTBEAT reminder checks only when recurring follow-up notifications are desired. <br>


## Reference(s): <br>
- [CRM Schema Reference](references/schema.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/xz-cn/clawdbot-crm-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local CRM files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create, update, index, import, export, and query local markdown CRM records plus CSV, vCard, and reminder files.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
