## Description:

Reviews the health of existing doDomain connections and queues DNS rechecks after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

Teams managing custom domains use this skill to identify broken connections, review recent check times and DNS providers, and request a recheck of a specific connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The doDomain connector can access team app and domain connection metadata.

Mitigation: Connect only when that access is acceptable to the team.

Risk: A queued recheck may be mistaken for a healthy connection.

Mitigation: Confirm the specific connection before rechecking and read its updated status later.

## Reference(s):

- [Checking Domain Connections on ClawHub](https://clawhub.ai/devino/skills/dodomain-checking-domain-connections)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports connection status and check times; an accepted recheck is queued, not proof of domain health.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
