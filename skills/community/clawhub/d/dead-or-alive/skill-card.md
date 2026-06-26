## Description: <br>
Monitors user check-ins, sends daily Feishu reminders, and contacts an emergency phone contact after seven consecutive missed check-ins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jayhe](https://clawhub.ai/user/jayhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals or teams use this skill to set up a safety check-in workflow that sends daily Feishu reminders, records check-ins, and escalates to an emergency contact after seven missed days. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sets up ongoing automation and can automatically contact an emergency contact without enough visible user controls. <br>
Mitigation: Before installing, confirm how Feishu messages and phone calls are sent, who can check in, and how scheduled tasks can be stopped or deleted. <br>
Risk: The workflow stores emergency contact and check-in information and may call a third party after missed check-ins. <br>
Mitigation: Protect and periodically remove stored contact data as appropriate, and confirm the emergency contact has consented to automated calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jayhe/dead-or-alive) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, JSON configuration, and plain-text check-in and alert records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May set up recurring reminders and maintain check-in and alert history after user configuration.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
