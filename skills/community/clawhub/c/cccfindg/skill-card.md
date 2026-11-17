## Description:

This skill helps an agent query an authenticated address book by organization path and job title, then return matching personnel contact details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blockcloud](https://clawhub.ai/user/blockcloud)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or authorized operators use this skill to locate personnel in an internal directory by organization and position when they are permitted to access and disclose the resulting contact information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can return employee identifiers and phone numbers from an authenticated internal directory.

Mitigation: Install only where users are authorized to access and disclose this data, and limit lookups to approved business purposes.

Risk: The public description and authorization boundaries are unclear for automatic approval.

Mitigation: Revise the skill description and manifest to disclose authenticated directory access and clarify authorization boundaries before deployment.

Risk: Returned mobile numbers or employee IDs may be unnecessary for some requests.

Mitigation: Avoid returning mobile numbers or employee IDs unless they are necessary for the approved use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blockcloud/skills/cccfindg)
- [ClawHub publisher profile](https://clawhub.ai/user/blockcloud)
- [Authenticated address book login](https://222.222china.com/address-book/login)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text or Markdown with one result per matching person.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include organization, position, employee ID, 222ID, name, landline, and mobile phone for each match.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
