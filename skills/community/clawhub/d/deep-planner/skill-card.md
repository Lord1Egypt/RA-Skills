## Description: <br>
Deep Planner is a meta-skill that helps an agent plan, execute, and reflect on complex multi-step tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jzw6](https://clawhub.ai/user/jzw6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users use Deep Planner to turn complex requests into visible step-by-step plans, coordinate other tools or skills, and pause for user confirmation when critical information is missing. It is useful for research, analysis, content creation, technical design, data processing, and multi-skill workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task descriptions and completed plans may persist locally under .todolist/ and could contain sensitive information if users include it. <br>
Mitigation: Avoid placing secrets or highly sensitive details in task descriptions, and periodically review or delete retained .todolist/ files. <br>
Risk: Planning output for unfamiliar or time-sensitive work may rely on assumptions or stale information. <br>
Mitigation: Flag uncertain steps, verify current claims with live sources when needed, and pause for user confirmation when missing information would change the execution path. <br>


## Reference(s): <br>
- [Task Type Templates](references/task-types.md) <br>
- [Deep Planner on ClawHub](https://clawhub.ai/jzw6/deep-planner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown task plans, status updates, and local .todolist Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists task state locally under .todolist/; completed plans are intentionally retained.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
