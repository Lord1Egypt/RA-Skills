## Description: <br>
结构化规划模式 — 在执行复杂任务前先做系统性规划。借鉴 Claude Code 的 Plan Agent。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jobzhao15](https://clawhub.ai/user/jobzhao15) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to make the agent plan before complex or multi-step work. It guides the agent to restate requirements, inspect relevant context, identify risks, produce a structured plan, and wait for user confirmation before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plans for sensitive or production repositories may contain incorrect or misleading guidance. <br>
Mitigation: Review the generated plan before approving edits, especially when the task affects sensitive or production code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jobzhao15/enhance-plan-mode) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown plan with sections, bullets, and validation checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill asks for user confirmation before execution on complex work.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
