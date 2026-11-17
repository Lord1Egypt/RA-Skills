## Description:

One-word trigger for next bus arrival to your destination

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhayjb](https://clawhub.ai/user/abhayjb)

### License/Terms of Use:


## Use Case:

External users in Singapore use this skill to check the next arrival time, load, and origin stop for a configured bus service and destination.

### Deployment Geography for Use:

Singapore

## Known Risks and Mitigations:

Risk: The configured bus stop and service are sent to the Arrivelah2 API when the skill is invoked.

Mitigation: Confirm the configured route is acceptable to share with the public API before installing or invoking the skill.

Risk: A one-word trigger may run the lookup when the user's intent is ambiguous.

Mitigation: Change the trigger or invoke it only when the request is explicit if accidental activation would be a concern.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abhayjb/skills/arrivelah)
- [Arrivelah2 API](https://arrivelah2.busrouter.sg/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text bus arrival status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local configuration for bus stop, service, destination, and API endpoint.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
