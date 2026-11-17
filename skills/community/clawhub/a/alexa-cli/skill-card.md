## Description:

Controls Amazon Alexa devices and smart home functions through the `alexacli` CLI for announcements, device control, voice commands, and Alexa queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buddyh](https://clawhub.ai/user/buddyh)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to translate user requests into `alexacli` commands for Echo announcements, smart home controls, Alexa questions, audio playback, and Alexa history or conversation lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control real-world Alexa-linked devices, including locks, thermostats, lights, broadcasts, and media playback.

Mitigation: Use explicit device names and confirm lock, thermostat, broadcast, and other physical actions before running commands.

Risk: The skill can expose private Alexa activity, calendar, conversation history, or account data.

Mitigation: Retrieve or echo history, calendar, or conversation data only when the account owner clearly requested it.

Risk: The skill installs and invokes an unpinned third-party CLI that uses an unofficial Alexa API.

Mitigation: Install only when the third-party CLI is trusted, and prefer reviewed or pinned installation sources in managed environments.

## Reference(s):

- [Alexa CLI ClawHub release](https://clawhub.ai/buddyh/skills/alexa-cli)
- [Alexa CLI project homepage](https://github.com/buddyh/alexa-cli)
- [Go install module](https://github.com/buddyh/alexa-cli/tree/main/cmd/alexa)
- [Homebrew tap](https://github.com/buddyh/homebrew-tap)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optional JSON output flags for device, history, and Alexa response queries.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
