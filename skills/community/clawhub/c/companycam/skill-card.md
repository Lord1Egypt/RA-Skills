## Description:

Helps agents manage CompanyCam projects, photos, documents, users, and webhooks through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Contractors and teams use this skill to find and organize CompanyCam project documentation, including photos and related records. With explicit approval, an agent can update records or configure webhooks and automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creating, updating, deleting, or uploading CompanyCam records can change business documentation.

Mitigation: Default to reading records and obtain explicit approval for each write.

Risk: Webhooks and automations can continuously send project or photo event data to an external destination.

Mitigation: Confirm the exact destination and intended data with the user before creating or changing a webhook, function, or trigger; remove it when no longer needed.

Risk: CompanyCam responses can include personal or sensitive project details.

Mitigation: Return only the requested fields and avoid exposing full responses or credentials in logs and shared destinations.

## Reference(s):

- [CompanyCam skill release](https://clawhub.ai/byungkyu/skills/companycam)
- [CompanyCam API documentation](https://docs.companycam.com)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Maton homepage](https://maton.ai)
- [API gateway skill](https://clawhub.ai/byungkyu/api-gateway)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON]

**Output Format:** [Markdown guidance, shell commands, and structured API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and an authorized CompanyCam connection; writes require explicit user approval.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
