## Description: <br>
Provides positive motivation prompts and lightweight task progress tracking for agents using start, progress, milestone, focus, completion, and encouragement modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Linux2010](https://clawhub.ai/user/Linux2010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to generate supportive motivation text, track task progress, mark milestones, and summarize lightweight task status during agent work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task names and milestones are saved locally and may include sensitive project details if users enter them. <br>
Mitigation: Avoid putting secrets, customer data, or sensitive project details into task names or milestones. <br>


## Reference(s): <br>
- [Motivation Principles](references/motivation_principles.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Linux2010/agent-motivator) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text prompts and JSON task records from command-line scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores task progress locally under ~/.openclaw/agent-motivator/task_state.json when task tracking commands are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
