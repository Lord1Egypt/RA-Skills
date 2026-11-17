## Description:

Summarizes due, active, in-review, and blocked GetItDone tasks by workspace or project without changing them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

GetItDone users review their workspace or project workload, identify urgent and blocked tasks, and choose next actions without modifying tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workload summaries can expose workspace, project, task, blocker, note, attachment, and dependency information.

Mitigation: Connect only when comfortable granting access to that information; limit summaries to the workspace or project requested.

Risk: Generic workload requests may trigger GetItDone when the user means another task list.

Mitigation: Clarify whether the user means GetItDone before accessing its data when the request is ambiguous.

## Reference(s):

- [Reviewing Workload on ClawHub](https://clawhub.ai/devino/skills/getitdone-reviewing-workload)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only workload summary with up to three suggested next actions.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
