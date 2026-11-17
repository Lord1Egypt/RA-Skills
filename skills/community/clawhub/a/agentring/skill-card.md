## Description:

Reach the user on their phone through agentring — send a message, wait for their reply, or call them (a voice AI talks to them for you and returns the transcript). Use when you need the user's decision or attention and they may be away from the screen, when a long task finishes or fails, or when the user asks you to message or call them. Also use when the user asks to set up, install or connect agentring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mutonby](https://clawhub.ai/user/mutonby)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users use this skill to reach the user on their Android phone by sending a message, collecting a reply, or placing a voice AI call. Developers can also use it to connect agentring to supported agent harnesses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agentring API key grants access to the user's phone, and voice provider keys can expose provider accounts.

Mitigation: Have the user enter and store credentials themselves; keep API keys out of messages and call context, and store voice provider keys in the designated local environment file.

Risk: Messages and calls can interrupt or reach the user at inappropriate times.

Mitigation: Use messages for routine contact, reserve calls for urgent needs or a user request, and treat silence as no consent.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/mutonby/skills/agentring)
- [agentring website](https://agentring.io)
- [Android app](https://play.google.com/store/apps/details?id=dev.agentring.app)
- [Setup guide for self-hosted relays](https://github.com/mutonby/agentring/blob/main/docs/setup.md)
- [Voice provider setup](https://github.com/mutonby/agentring/blob/main/docs/voice.md#providers)

## Skill Output:

**Output Type(s):** [API calls, Text, Shell commands, Configuration instructions]

**Output Format:** [Messages, replies, and call transcripts; Markdown setup guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Phone contact and call outcomes depend on user setup and availability; setup uses user-provided credentials.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
