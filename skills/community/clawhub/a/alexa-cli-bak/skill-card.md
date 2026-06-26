## Description: <br>
Control Amazon Alexa devices and smart-home features through the `alexacli` CLI for Echo announcements, device control, voice commands, and Alexa queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[knochen666](https://clawhub.ai/user/knochen666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate Amazon Alexa devices and connected smart-home features through `alexacli`. It is suited for requested announcements, device lookup, Alexa questions, audio playback, and smart-home commands when the user has authorized the local CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can issue broad Alexa and smart-home commands, including announcements, thermostat changes, and lock commands. <br>
Mitigation: Require explicit user confirmation before sensitive actions such as locks, thermostat changes, alarms, purchases, and all-device announcements. <br>
Risk: Commands can retrieve Alexa history, calendar details, and conversation fragments. <br>
Mitigation: Avoid history, calendar, and conversation retrieval unless the user specifically requests it and understands the privacy impact. <br>
Risk: Local Alexa credentials are stored in `~/.alexa-cli/config.json` after authentication. <br>
Mitigation: Protect the local config file and remove credentials with `alexacli auth logout` when access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/knochen666/alexa-cli-bak) <br>
- [alexa-cli project homepage](https://github.com/buddyh/alexa-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that operate Alexa devices and smart-home endpoints; security guidance calls for explicit user confirmation for sensitive actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
