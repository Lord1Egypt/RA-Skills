## Description: <br>
Manages a local CSV-based CRM with pipeline tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and business operators use this skill to maintain a lightweight local CRM, add and update contacts, track deal stages, and review follow-up reminders from a CSV file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CRM contact details, notes, deal values, and backup files are stored in local workspace files. <br>
Mitigation: Use the skill only in approved workspaces and handle crm.csv plus dated backups as sensitive business records. <br>
Risk: Bulk CRM operations can change many contact or deal records at once. <br>
Mitigation: Review proposed bulk changes and preserve the generated crm-backup-YYYY-MM-DD.csv file before accepting updates. <br>
Risk: Promoted skills and context-pack links are separate items from this CRM skill. <br>
Mitigation: Evaluate those linked items independently before installing them or relying on their content. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/1kalin/afrexai-crm-updater) <br>
- [README](artifact/README.md) <br>
- [CRM CSV template](artifact/crm-template.csv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown summaries and CSV file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates a local crm.csv file and may create dated CSV backups before bulk operations.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
