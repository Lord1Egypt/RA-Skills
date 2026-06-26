## Description: <br>
Control Amazon Alexa devices and smart home via the `alexacli` CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buddyh](https://clawhub.ai/user/buddyh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to install and operate `alexacli` for Alexa device control, smart-home commands, announcements, audio playback, and Alexa account queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad access to Alexa devices, smart-home controls, and Alexa account data. <br>
Mitigation: Install only for trusted use cases, require explicit confirmation before sensitive actions such as locks, thermostats, purchases, alarms, or all-device announcements, and review commands before execution. <br>
Risk: Alexa configuration and outputs can expose private account, calendar, history, or conversation information. <br>
Mitigation: Avoid shared machines, protect or remove `~/.alexa-cli/config.json` when finished, and treat Alexa responses and history as private. <br>


## Reference(s): <br>
- [Alexa CLI on ClawHub](https://clawhub.ai/buddyh/alexa-cli) <br>
- [Alexa CLI homepage](https://github.com/buddyh/alexa-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that return text or JSON from the `alexacli` CLI.] <br>

## Skill Version(s): <br>
1.3.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
