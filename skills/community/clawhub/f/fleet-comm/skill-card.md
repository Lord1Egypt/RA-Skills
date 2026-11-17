## Description:

Enables real-time text messaging and broadcasting between multiple OpenClaw nodes across machines for coordinated fleet operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dagangtj](https://clawhub.ai/user/dagangtj)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to coordinate multiple OpenClaw nodes by starting a lightweight fleet message bus, registering nodes, sending direct messages, broadcasting updates, and polling for task or result messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes unauthenticated network messaging and a writable dashboard.

Mitigation: Use only on localhost or a tightly trusted VPN/firewalled network, and avoid sending secrets or sensitive task results until authentication, authorization, escaping, size limits, and retention controls are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dagangtj/skills/fleet-comm)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON message examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Node.js command invocations and environment variable settings for fleet bus coordination.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
