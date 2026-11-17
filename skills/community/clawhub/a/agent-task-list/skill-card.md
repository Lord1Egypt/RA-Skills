## Description:

Independent task list system that gives each agent its own prioritized task queue with task assignment, status updates, progress tracking, and history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wljmmx](https://clawhub.ai/user/wljmmx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create, prioritize, start, complete, fail, retry, query, and summarize per-agent task queues backed by local JSON state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted Agent IDs may escape the intended task storage folder and access or overwrite task-list files elsewhere.

Mitigation: Use only trusted Agent IDs without path separators or absolute paths, and review shared or multi-agent deployments until Agent ID validation is added.

Risk: Concurrent agents can update the same task files without robust atomic locking.

Mitigation: Avoid relying on this skill as an isolation or coordination boundary in shared environments until safer atomic locking is implemented.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Markdown guidance with command examples; the bundled CLI returns JSON and writes local task-list files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores task queues, indexes, and history under the OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
