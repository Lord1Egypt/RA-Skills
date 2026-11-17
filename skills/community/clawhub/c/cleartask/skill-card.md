## Description:

Transform broad, ambiguous, or early-stage user requirements into executable work through Stage1 requirement understanding, Stage2 clarification, a required user confirmation gate, and Stage3 internal expert-guided task packaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhanghengjing2](https://clawhub.ai/user/zhanghengjing2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, product, design, testing, workflow, and general agent users use this skill to turn underspecified requests into confirmed requirements before downstream execution. It helps an agent ask targeted clarification questions, capture accepted defaults, pause for explicit confirmation, and then use expert-guided criteria to perform the confirmed task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: After explicit confirmation, the workflow may proceed to execute the confirmed task using the agent's normal tool access.

Mitigation: Review the requirement summary before confirming and rely on the skill's pause points for credentials, paid services, network actions, destructive operations, or unexpectedly broad changes.

Risk: Incorrect or incomplete clarification can lead the downstream agent to act on the wrong scope.

Mitigation: Use the confirmation gate to revise the requirement description or requirement details before allowing Stage3 and execution.

## Reference(s):

- [Clear Task Skill Page](https://clawhub.ai/zhanghengjing2/skills/cleartask)
- [Expert Roles and Acceptance Criteria](references/expert-roles-and-acceptance.md)
- [Stage1 Universal Process Model](references/stage1-universal-process-model.md)
- [Stage2 Clarification Handoff](references/stage2-clarification-handoff.md)
- [Stage3 Agent Task Guidance Package](references/stage3-agent-task-guidance-package.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown text with structured requirement summaries, clarification questions, and internal task guidance packages when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit confirmation before Stage3 execution and pauses before credentials, paid services, network actions, destructive operations, or unexpectedly broad changes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
