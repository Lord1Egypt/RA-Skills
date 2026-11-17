## Description:

Allows a CEO-style coordinating agent to notify other agents through shared memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stingan](https://clawhub.ai/user/stingan)

### License/Terms of Use:


## Use Case:

Coordinators acting as a CEO use this skill to send short notifications to named agents so those agents can retrieve the messages later from shared notification logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses unsafe shell execution and persistent shared memory that can be abused.

Mitigation: Review before installing, avoid sensitive messages or privileged environments, and rewrite to use a constrained file or memory API.

Risk: Agent names and message content may be handled unsafely when writing notifications.

Mitigation: Validate agent names, pass message content as data rather than shell source, and label stored notifications as untrusted.

Risk: Stored notifications may persist longer than intended.

Mitigation: Provide retention or deletion controls for notification records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stingan/skills/ceo-notify-agents)

## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [Plain text confirmation with appended notification log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes per-agent and aggregate notification records to persistent shared memory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
