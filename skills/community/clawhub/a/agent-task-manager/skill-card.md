## Description: <br>
Agent Task Manager helps agents define, persist, and run multi-step workflows with dependencies, recovery state, and rate-limit handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dobbybud](https://clawhub.ai/user/dobbybud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to structure stateful multi-agent workflows, resume interrupted tasks, and coordinate rate-limited actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Passing untrusted text into the cooldown shell wrapper could execute unintended commands. <br>
Mitigation: Review wrapped commands before execution and do not pass untrusted input to cooldown.sh as a command. <br>
Risk: Task definitions and workflow state may leave secrets or sensitive personal data on disk. <br>
Mitigation: Avoid storing secrets or sensitive personal data in task definitions because task_state.json and cooldown timestamp files persist locally. <br>


## Reference(s): <br>
- [Task Structure Schema](references/task_schema.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dobbybud/agent-task-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON task definitions, Python workflow code, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local task state and cooldown timestamp files when its scripts are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
