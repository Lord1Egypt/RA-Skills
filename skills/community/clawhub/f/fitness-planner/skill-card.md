## Description: <br>
Fitness Planner helps users generate training plans, track check-ins and weekly stats, manage periodized training and muscle-group progress, collect recovery feedback, and retrieve exercise explanations with video-learning searches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DeviosLang](https://clawhub.ai/user/DeviosLang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to plan workouts, receive daily training guidance, record completion and recovery feedback, and review progress summaries. It is intended for personal fitness planning support, not as medical or clinical advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video-search behavior can invoke shell commands for exercise-name lookups. <br>
Mitigation: Review or disable the video-search path before installation, and replace shell execution with a structured API call or strict allowlisted inputs. <br>
Risk: The daily reminder script can send workout details to a fixed WeChat recipient. <br>
Mitigation: Do not run scripts/daily_reminder.sh until the recipient and delivery channel are changed to approved values, or disable reminder delivery entirely. <br>
Risk: Fitness, recovery, plan, record, and video-cache data are stored locally in plaintext. <br>
Mitigation: Use restrictive local file permissions, avoid storing unnecessary sensitive health details, and delete local state files when the skill is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/DeviosLang/fitness-planner) <br>
- [Training Templates](references/templates.md) <br>
- [Exercise Library](references/exercises.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown-style conversational text, optional shell commands, and local JSON state files for configuration, plans, records, and statistics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores fitness, recovery, workout, and video-cache data locally in plaintext unless the runtime environment adds protection.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release metadata; package.json reports 1.4.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
