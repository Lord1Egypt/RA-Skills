## Description: <br>
Delete contacts with no email address from a HubSpot CRM instance using the HubSpot CRM Search and Batch Archive APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomgranot](https://clawhub.ai/user/tomgranot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
CRM operators, revenue operations teams, and developers use this skill to find, review, export, delete, and verify HubSpot contacts that lack email addresses and cannot be used for outreach. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can bulk-delete HubSpot contacts that do not have email addresses. <br>
Mitigation: Review the before-state CSV, confirm the deletion count, keep the safety threshold aligned with the expected count, and require explicit confirmation before running deletion. <br>
Risk: The skill requires a HubSpot private app token with contact read and write access. <br>
Mitigation: Use a least-privilege token, store it only in the local environment file needed for execution, and rotate or revoke it after the cleanup if appropriate. <br>
Risk: Generated CSV audit files may contain CRM contact identifiers and contact metadata. <br>
Mitigation: Store audit files in an appropriate protected location and remove or retain them according to the organization's data handling policy. <br>
Risk: Contacts can reappear if an integration, form, sync, or import process continues creating records without email addresses. <br>
Mitigation: Investigate the source of no-email contacts before deletion and run the after-state verification script after cleanup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tomgranot/delete-no-email-contacts) <br>
- [Publisher profile](https://clawhub.ai/user/tomgranot) <br>
- [HubSpot CRM API endpoint](https://api.hubapi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python scripts, shell setup commands, CSV audit files, and terminal status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a HubSpot private app access token and writes before-state and deletion audit CSV files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
