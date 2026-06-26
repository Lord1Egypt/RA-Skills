## Description: <br>
Transform broad, ambiguous, or early-stage user requirements into executable work through Stage1 requirement understanding, Stage2 clarification, a required user confirmation gate, and Stage3 internal expert-guided task packaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhanghengjing2](https://clawhub.ai/user/zhanghengjing2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, coding agents, writing agents, product agents, design agents, testing agents, and workflow-building agents use this skill to clarify ambiguous requests, confirm requirements with the user, and then execute with an internal expert-guided task package. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide downstream work that changes files or interacts with external systems after confirmation. <br>
Mitigation: Review the confirmation summary before approving execution, and ask to inspect the internal package when more visibility is needed. <br>
Risk: Ambiguous requirements can lead to incorrect downstream execution if the confirmation handoff is approved too quickly. <br>
Mitigation: Revise the requirement description or details at the confirmation gate until scope, deliverables, constraints, defaults, and assumptions are clear. <br>


## Reference(s): <br>
- [Clear Task ClawHub Page](https://clawhub.ai/zhanghengjing2/cleartask) <br>
- [Expert Roles and Acceptance Criteria](references/expert-roles-and-acceptance.md) <br>
- [Stage1 Universal Process Model](references/stage1-universal-process-model.md) <br>
- [Stage2 Clarification Handoff](references/stage2-clarification-handoff.md) <br>
- [Stage3 Agent Task Guidance Package](references/stage3-agent-task-guidance-package.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured requirement summaries, internal guidance packages, and downstream execution artifacts as needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before Stage3 packaging and execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
