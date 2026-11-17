## Description:

Archive or delete unused custom properties across all HubSpot object types (contacts, companies, deals). Identifies Salesforce sync properties, test/temp properties, and obsolete form fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomgranot](https://clawhub.ai/user/tomgranot)

### License/Terms of Use:

MIT-0

## Use Case:

HubSpot administrators, RevOps teams, and CRM developers use this skill to inventory custom properties, identify safe cleanup candidates, and plan archive or deletion steps while protecting active integrations and automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deleting HubSpot properties can permanently remove the property definition and associated data.

Mitigation: Archive properties first, wait 30 days, keep a cleanup log, and delete only after manual review confirms no issues.

Risk: Removing Salesforce sync, form, workflow, list, or calculated properties can break integrations, automation, reporting, or active data collection.

Mitigation: Use a least-privilege HubSpot API token, review candidates manually, verify dependencies, and get owner approval before changing those properties.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance with an inline Python code example]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes manual review checkpoints for HubSpot property dependencies before archive or deletion.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
