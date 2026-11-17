## Description:

Connects an agent to the AgentAlarm iPhone app to ring full-screen alarms for reminders and wake-ups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guyaluk](https://clawhub.ai/user/guyaluk)

### License/Terms of Use:

MIT-0

## Use Case:

People using an agent with the AgentAlarm iPhone app can pair their phone and request immediate or scheduled audible alarms for reminders and wake-ups they do not want to miss.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local pairing file contains a send token that can authorize alarms.

Mitigation: Keep the pairing file private and restrict access to the device running the agent.

Risk: Changing the relay setting redirects alarm delivery and its authorization token.

Mitigation: Use the default AgentAlarm relay or review and pin any relay override before pairing.

Risk: Alarms can ring audibly through silent mode, while scheduled alarms require an online gateway when due.

Mitigation: Confirm the user's intent and time zone; report delivery failures and send a normal reminder as a fallback.

## Reference(s):

- [AgentAlarm website](https://agentalarm.app)
- [AgentAlarm skill on ClawHub](https://clawhub.ai/guyaluk/skills/agentalarm)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides pairing and alarm instructions, scheduling commands, and status or failure guidance.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
