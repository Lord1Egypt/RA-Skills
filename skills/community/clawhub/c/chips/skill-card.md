## Description:

Connect this OpenClaw to Chips, a messaging app for chatting with your agents from a Mac, iPhone or iPad. Use when someone asks to set up or connect Chips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chipschat](https://clawhub.ai/user/chipschat)

### License/Terms of Use:

MIT-0

## Use Case:

External users running OpenClaw on macOS or Linux use this skill to connect their agents to Chips for messaging, or disconnect the bridge when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill also provides a command that disconnects OpenClaw from Chips and removes the bridge from the machine.

Mitigation: Use the disconnect command only when the person explicitly asks to disconnect, and describe its effect before running it.

Risk: The Chips join link grants access to join the person's Chips and should be treated like a password.

Mitigation: Check the link against the documented pattern, use it only for the connection command, and do not store or share it.

## Reference(s):

- [Chips for OpenClaw](https://chipschat.ai/openclaw/)
- [Chips setup](https://chipschat.ai/setup/)
- [Chips ClawHub release](https://clawhub.ai/chipschat/skills/chips)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: ClawHub server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
