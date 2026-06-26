## Description: <br>
Send push notifications to iOS devices via Bark when a user asks to send a notification, push to phone, or use Bark notify. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DeAntiWang](https://clawhub.ai/user/DeAntiWang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to send Bark notifications to an iOS device from an agent workflow or command line. It supports notification title, body, sound, badge, URL, group, level, image, and subtitle options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bark device keys are credentials that can send notifications to a user's device. <br>
Mitigation: Store the key in BARK_KEY or BARK_DEVICE_KEY, avoid exposing it in shared logs or prompts, and rotate it if it is disclosed. <br>
Risk: Notification text may include sensitive personal data or unintended inferred content. <br>
Mitigation: Avoid sending passwords or sensitive personal data, and confirm the message content before sending when it is inferred. <br>
Risk: URL-path curl examples can expose notification content and device keys in command history or logs. <br>
Mitigation: Prefer the POST-based shell or Node.js script flow for normal use. <br>


## Reference(s): <br>
- [Bark Push ClawHub page](https://clawhub.ai/DeAntiWang/bark-push) <br>
- [Bark API endpoint](https://api.day.app/{device_key}) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and command-line parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses BARK_KEY or BARK_DEVICE_KEY as the Bark device key credential.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
