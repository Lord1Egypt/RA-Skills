## Description: <br>
AI task reminder using priority, Ebbinghaus intervals, gamification, and active time tracking for effective task management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wukai8289](https://clawhub.ai/user/wukai8289) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to manage local tasks, reminder summaries, Ebbinghaus review intervals, gamification stats, and hourly activity learning through a Python CLI and agent-triggered commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores task content, completion statistics, and hourly activity patterns as local JSON files in the skill folder. <br>
Mitigation: Use it only in a trusted local workspace, avoid entering sensitive task content, and protect or delete the generated JSON state files when needed. <br>
Risk: Generic task and completion triggers may cause unintended add or complete actions in shared or multi-skill agent environments. <br>
Mitigation: Narrow the triggers and require user confirmation before automatic add, complete, or cancel actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wukai8289/caring-memory) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown-style reminder summaries, CLI status text, and cron command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local JSON state files for tasks, stats, and activity history in the skill folder.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
