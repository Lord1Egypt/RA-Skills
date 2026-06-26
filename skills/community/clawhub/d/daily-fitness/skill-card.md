## Description: <br>
Daily Fitness generates 5-15 minute no-equipment bodyweight routines with instructions, interactive timing, optional reminders, and streak tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiajiaoy](https://clawhub.ai/user/jiajiaoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate short bilingual no-equipment workout plans for home, office, or travel. It can also set up optional morning and evening reminders for supported messaging channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional push setup creates scheduled morning and evening runs to the selected channel. <br>
Mitigation: Enable push only when scheduled reminders are intended, and use the documented off command to remove them. <br>
Risk: Generated HTML includes placeholder ad slots that could later host third-party content. <br>
Mitigation: Review the generated HTML before opening or sharing it if third-party ad content is added. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiajiaoy/daily-fitness) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance, shell commands, and a single-file HTML artifact] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional scheduled morning and evening reminders for telegram, feishu, slack, or discord.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
