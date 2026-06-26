## Description: <br>
Claw Use lets AI agents control physical devices over HTTP with commands for screen reading, screenshots, input actions, app launch, navigation, notifications, and audio output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[4ier](https://clawhub.ai/user/4ier) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to connect an AI agent to a real device, inspect device state, and perform input, navigation, application, notification, screenshot, and audio actions through the Claw Use command interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over a physical device, including screen reading, screenshots, typing, app launch, URL opening, intents, notifications, and lock or unlock operations. <br>
Mitigation: Install only when device control is intended, use a dedicated test device when possible, and require explicit approval for sensitive actions such as unlocking, reading notifications, typing, launching apps, opening URLs, and invoking intents. <br>
Risk: Device screens and notifications may expose personal or confidential content to the agent. <br>
Mitigation: Avoid using devices with personal accounts or sensitive notifications unless the deployment has clear approval controls and data-handling boundaries. <br>
Risk: Automatic unlock behavior can allow commands to act on a device without a fresh user decision. <br>
Mitigation: Prefer configurations that disable or gate unlocking and require human confirmation before commands that change device state. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/4ier/claw-use) <br>
- [Publisher profile](https://clawhub.ai/user/4ier) <br>
- [claw-use-android implementation and API details](https://github.com/4ier/claw-use-android#api-details) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to issue device-control commands that read screen or notification content and perform actions on configured devices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
