## Description:

A meme skill that makes the assistant respond only with rotating sleep reminders and a fixed stop response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whooshinglander](https://clawhub.ai/user/whooshinglander)

### License/Terms of Use:

MIT-0

## Use Case:

Users invoke this joke skill when they intentionally want an assistant persona that refuses normal task assistance and responds with sleep reminders. It is suitable only for scoped, explicit use where interruption of normal agent work is expected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can override normal assistant replies while active.

Mitigation: Scope installation and invocation to sessions where the sleep-reminder behavior is explicitly desired.

Risk: Common stop words can stop the agent or produce a shutdown-style response.

Mitigation: Avoid enabling it in workflows where ordinary words such as stop, quit, or exit may appear as task content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whooshinglander/skills/claude-says-go-to-sleep)
- [WhooshingLander publisher profile](https://clawhub.ai/user/whooshinglander)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rotates through 24 predefined sleep-reminder lines; configured stop words produce a fixed goodnight response.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
