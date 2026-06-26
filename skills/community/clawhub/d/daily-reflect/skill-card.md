## Description: <br>
Daily journaling prompts for meaningful reflection, morning intention-setting, and evening review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiajiaoy](https://clawhub.ai/user/jiajiaoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to receive morning journaling prompts and evening reflection questions, with optional reminders on supported chat channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Daily reminder scheduling can send prompts through supported chat platforms unexpectedly if channel authorization or cron handling is not configured as intended. <br>
Mitigation: Confirm reminder scheduling, channel authorization, and OpenClaw cron marker handling before enabling reminders. <br>
Risk: Broad journaling trigger words may activate the skill for generic journaling or writing-prompt requests. <br>
Mitigation: Narrow trigger words when using strict agent routing or when accidental activation would be disruptive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiajiaoy/daily-reflect) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated journaling prompt text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional reminder scheduling for telegram, feishu, slack, and discord channels] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
