## Description:

Helps users find robots for physical tasks, compare available matches, and learn how to rent one.

This skill is ready for commercial/non-commercial use.

## Publisher:

[getbodymd](https://clawhub.ai/user/getbodymd)

### License/Terms of Use:

MIT-0

## Use Case:

People in the US can ask an agent to search for robots to help with physical jobs, review available matches and prices, and decide whether to pursue a rental.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: A task search can send sensitive task, location, timing, or home-access details to GetBody before the user explicitly agrees.

Mitigation: Tell the user what details will be shared and obtain their consent before submitting a request, especially for residences, unattended property, or personal schedules.

Risk: An email address or a robot lease may be requested without the user's authorization.

Mitigation: Ask before sharing an email address, and confirm with the user before requesting, activating, or returning a lease.

## Reference(s):

- [GetBody skill listing](https://clawhub.ai/getbodymd/skills/getbody)
- [GetBody homepage](https://getbody.md)
- [GetBody documentation](https://getbody.md/llms.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with match summaries and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Match results may include robot type, area, availability, and asking price; a search does not book a robot.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
