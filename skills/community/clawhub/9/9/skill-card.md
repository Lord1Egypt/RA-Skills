## Description: <br>
Nine Skill provides 9-minute focus timers, 9-level task prioritization, number-nine math tricks, category-based organization, and quick answers for common planning and calculation tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skills](https://clawhub.ai/user/skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and productivity-focused users use this skill to manage short focus sessions, organize tasks by priority, apply simple number-nine math shortcuts, and structure common planning requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Timer reminders may use normal time and notification permissions. <br>
Mitigation: Review notification behavior in the host agent before enabling the skill in environments where reminders could be disruptive. <br>
Risk: Aggressive auto-matching could invoke the productivity workflow when it was not intended. <br>
Mitigation: Invoke the skill explicitly or tune agent routing so timer, priority, and calculation requests are matched intentionally. <br>
Risk: Task details entered into productivity workflows may include sensitive information. <br>
Mitigation: Avoid entering confidential task details unless the surrounding agent environment is trusted. <br>


## Reference(s): <br>
- [Nine Skill on ClawHub](https://clawhub.ai/skills/9) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Markdown or plain text responses, with timer and notification actions when invoked by the host agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use system time and notification permissions for focus timer reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
