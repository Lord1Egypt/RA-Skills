## Description: <br>
Automatically sends personalized daily greetings from OpenClaw agents to their bound channels, including preferred-language messages and relevant status updates via BOOT.md or OpenClaw cron triggers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shz2050](https://clawhub.ai/user/shz2050) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to configure agents to send scheduled, personalized greetings and status updates into bound messaging channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically send context-derived greetings to every bound channel on a recurring schedule. <br>
Mitigation: Review channel bindings and enable the schedule only for intended channels before deployment. <br>
Risk: Greetings may include status summaries or history-based inferences that expose sensitive work context. <br>
Mitigation: Disable or narrow status summaries and history-based inference where channels may contain sensitive work. <br>
Risk: BOOT.md and cron entries can trigger unattended execution after installation. <br>
Mitigation: Review BOOT.md and cron entries before enabling the skill and after uninstalling it. <br>


## Reference(s): <br>
- [Daily Greeting on ClawHub](https://clawhub.ai/shz2050/daily-greeting) <br>
- [Installation guide](https://raw.githubusercontent.com/shz2050/daily-greeting/main/guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Text messages with Markdown and bash setup instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run on startup or a weekday cron schedule; writes local state to prevent duplicate greetings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
