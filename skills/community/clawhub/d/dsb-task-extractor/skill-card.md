## Description:

Extracts, tracks, and verifies multiple actionable tasks from compound user messages so agents can avoid silently dropping requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dodge1218](https://clawhub.ai/user/dodge1218)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to decompose messages with several actionable asks, track status and evidence for each task, and reconcile completion before ending a run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent could propose or execute tasks that need approval or affect external systems.

Mitigation: Review individual tasks before execution and require explicit human approval for gated actions.

Risk: A task inventory can still include incorrect, extra, or misleading items if the original request is ambiguous.

Mitigation: Compare the extracted task list against the user message during reconciliation and surface dropped or blocked tasks clearly.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown task lists and status tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task status markers, evidence notes, dropped-task summaries, and approval gates for tasks that require human confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
