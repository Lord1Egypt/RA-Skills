## Description:

Automates adding new CRM records to the Fractal CRM system by parsing customer or lead details from natural language and preparing browser-based form entry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangli123456](https://clawhub.ai/user/zhangli123456)

### License/Terms of Use:


## Use Case:

External users and CRM operators use this skill to turn natural-language customer or sales lead details into CRM record fields and browser actions for adding a record.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact exposes a CRM username and password.

Mitigation: Revoke or rotate the exposed credentials, remove secrets from files and command output, and use a dedicated least-privilege account for CRM automation.

Risk: The skill can submit records to an external CRM without clear safeguards.

Mitigation: Require a preview of the parsed CRM fields and explicit user confirmation before saving records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangli123456/skills/crm-add-record)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON parser output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces CRM field mappings such as phone, contact, region, and basic information from a single user input string.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
