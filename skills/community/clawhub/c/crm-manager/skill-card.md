## Description: <br>
Manages a local CSV-based CRM with pipeline tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, operators, and small-business users use this skill to manage contacts, pipeline stages, deal values, follow-up reminders, and CRM summaries in a local CSV file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local CRM files can contain private contact, deal, and follow-up data. <br>
Mitigation: Install only in workspaces where the CRM data belongs, keep crm.csv and backup files private, and avoid storing secrets or unusually sensitive notes. <br>
Risk: CRM mutations can change customer records or pipeline state. <br>
Mitigation: Review important CRM changes before accepting them and rely on the skill's backup behavior before bulk operations. <br>


## Reference(s): <br>
- [CRM Manager on ClawHub](https://clawhub.ai/1kalin/crm-manager) <br>
- [Context Packs](https://afrexai-cto.github.io/context-packs/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, configuration, guidance] <br>
**Output Format:** [Markdown summaries and tables with CSV file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates crm.csv and date-stamped backup files for bulk operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
