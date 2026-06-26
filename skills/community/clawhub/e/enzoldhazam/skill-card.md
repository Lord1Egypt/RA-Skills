## Description: <br>
Control NGBS iCON Smart Home thermostats. Use when the user asks about home temperature, heating, thermostat control, or wants to adjust room temperatures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniel-laszlo](https://clawhub.ai/user/daniel-laszlo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to check room temperatures, inspect thermostat status, and adjust NGBS iCON Smart Home thermostat targets through the enzoldhazam CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sensitive enzoldhazam.hu account credentials and can change thermostat targets. <br>
Mitigation: Prefer Keychain login over long-lived environment variables, avoid sharing credentials in chats or logs, and confirm the exact room and target temperature before running set commands. <br>


## Reference(s): <br>
- [enzoldhazam.hu](https://www.enzoldhazam.hu) <br>
- [ClawHub skill page](https://clawhub.ai/daniel-laszlo/enzoldhazam) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional CLI JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May authenticate with macOS Keychain or ENZOLDHAZAM_USER and ENZOLDHAZAM_PASS environment variables; temperature-changing commands should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
