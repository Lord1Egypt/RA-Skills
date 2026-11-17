## Description:

Control Amazon Alexa devices and smart home via the `alexacli` CLI for speaking or announcing on Echo devices, controlling smart-home devices, sending voice commands, and querying Alexa.

This skill is ready for commercial/non-commercial use.

## Publisher:

[knochen666](https://clawhub.ai/user/knochen666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation-focused users use this skill to operate Alexa-enabled Echo and smart-home devices through `alexacli` commands. It helps agents propose authentication, device discovery, text-to-speech, smart-home control, Alexa+ conversation, playback, and history commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose commands that affect locks, thermostats, plugs, alarms, or other smart-home devices.

Mitigation: Require explicit user confirmation before physical-device actions and use only accounts and devices approved for agent control.

Risk: Alexa queries and history commands can expose personal account data such as calendar entries, conversation fragments, or recent activity.

Mitigation: Avoid logging returned personal data and limit queries to information the user explicitly requested.

Risk: The release installs an unofficial, unpinned `alexacli` dependency.

Mitigation: Prefer a pinned or otherwise verified `alexacli` release before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/knochen666/skills/alexa-cli-bak)
- [Alexa CLI upstream project](https://github.com/buddyh/alexa-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks and command reference tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that control Alexa and smart-home devices or query Alexa account data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
