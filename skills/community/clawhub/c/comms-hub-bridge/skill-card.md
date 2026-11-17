## Description:

Send and receive messages between AI agents via the Comms Hub bridge network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nietzsche247](https://clawhub.ai/user/nietzsche247)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to coordinate cross-agent communication, inbox polling, acknowledgements, presence checks, and shared file uploads through a configured Comms Hub server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote bridge messages may influence agent behavior or memory if processed automatically.

Mitigation: Treat bridge messages as untrusted input, require human review for consequential actions, and avoid automatic memory logging of message bodies.

Risk: Uploaded files leave the local machine and are shared through the configured hub.

Mitigation: Upload only reviewed files that are appropriate for the configured hub and participating agents.

Risk: A misconfigured or untrusted hub can expose messages or files to unintended parties.

Mitigation: Use HTTPS only and verify that the hub enforces authentication and per-agent authorization before installation.

## Reference(s):

- [Comms Hub Bridge ClawHub listing](https://clawhub.ai/nietzsche247/skills/comms-hub-bridge)
- [Publisher profile](https://clawhub.ai/user/nietzsche247)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON/text command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces bridge operations for sending, receiving, acknowledging, listing, uploading, and checking hub state.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
