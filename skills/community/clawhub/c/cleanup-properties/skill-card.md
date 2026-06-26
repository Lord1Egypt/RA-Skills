## Description: <br>
Archive or delete unused custom properties across all HubSpot object types (contacts, companies, deals). Identifies Salesforce sync properties, test/temp properties, and obsolete form fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomgranot](https://clawhub.ai/user/tomgranot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HubSpot administrators and operations teams use this skill to inventory custom CRM properties, identify cleanup candidates, and plan safe archive or deletion steps while checking forms, workflows, lists, Salesforce mappings, and calculated properties. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deleting HubSpot properties can permanently remove property definitions and associated data. <br>
Mitigation: Archive properties first, keep a cleanup log, wait through a review window, and require explicit user approval before irreversible deletion. <br>
Risk: Property cleanup can disrupt active forms, workflows, lists, Salesforce sync mappings, or calculated properties. <br>
Mitigation: Use a narrowly scoped HubSpot token and review those dependencies before proposing archive or deletion actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tomgranot/cleanup-properties) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline Python code and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied HubSpot access and review before any irreversible deletion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter version 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
