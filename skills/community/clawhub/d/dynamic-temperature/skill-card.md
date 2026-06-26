## Description: <br>
Dynamic LLM temperature selection based on task type for scheduling, communication, creative writing, and irreversible actions, balancing precision where needed with warmth where appropriate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent builders and operators use this guidance to choose task-appropriate model temperatures for deterministic actions, scheduling, analysis, routine communication, briefings, and creative writing. It is especially relevant when configuring agent defaults or documenting per-skill temperature expectations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Temperature guidance may be missed when treated as a triggered skill even though the artifact says the behavior should apply broadly. <br>
Mitigation: Review whether the rules should live in a core identity or configuration file before relying on the skill for global behavior. <br>
Risk: Incorrect temperature choices can reduce precision for irreversible or sensitive actions such as sending messages, posting, deleting data, or destructive commands. <br>
Mitigation: Use deterministic settings for irreversible actions and require confirmation before sending, posting, deleting, or executing destructive operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/netanel-abergel/dynamic-temperature) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration] <br>
**Output Format:** [Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; does not install code, request secrets, or perform actions on its own.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
