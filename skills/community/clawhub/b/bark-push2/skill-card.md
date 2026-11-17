## Description:

Bark Push sends agent-supplied notification messages through the Bark push service using a LobeHub-style notification format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallersoup](https://clawhub.ai/user/smallersoup)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to send short Bark notifications from an agent or command-line workflow with a message and optional title.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Bark key may be read from the environment or from a parent USER.md file.

Mitigation: Prefer environment-based secret injection, avoid storing Bark keys in USER.md, and review or remove the file fallback before deployment.

Risk: Notification content and the Bark key are sent to an external Bark service.

Mitigation: Avoid sensitive notification messages and review outbound data handling before using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smallersoup/skills/bark-push2)
- [Bark API endpoint](https://api.day.app)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Text]

**Output Format:** [Command-line invocation with terminal status text and an outbound Bark HTTPS request]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a Bark key supplied through the runtime environment, an explicit key path, or the documented file fallback.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
