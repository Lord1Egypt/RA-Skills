## Description:

Agent Workflow is a structured OpenClaw plugin that guides agents through brainstorming, planning, execution, verification, and delivery with persistent multi-project workflow state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kangyishuai](https://clawhub.ai/user/kangyishuai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this plugin to manage structured work sessions, persist workflow progress, branch between sequential and subagent execution, and load bundled workflow skills at the right step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflow state can include project names, progress, notes, and outputs stored on disk.

Mitigation: Install only where local persistence of this information is acceptable, and avoid recording sensitive information in workflow notes or outputs.

Risk: Clawscan reports a path-handling flaw that could let tool callers reach JSON files outside the workflow storage area.

Mitigation: Do not expose the agent_workflow tool to untrusted prompts or callers until workflowId validation and path containment are fixed.

Risk: The security guidance calls for clearer retention or cleanup controls for persisted workflow data.

Mitigation: Review and remove persisted workflow files as needed, and prefer deployments that add explicit retention or cleanup controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kangyishuai/skills/agent-workflow)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON tool responses and Markdown skill guidance with shell and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workflow names, progress, notes, and outputs may be persisted on disk by the plugin.]

## Skill Version(s):

1.1.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
