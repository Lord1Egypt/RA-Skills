## Description:

Taskqueue provides an in-memory FastAPI priority queue for agent workflows, allowing agents to create, claim, filter, complete, fail, and summarize tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run a lightweight local task queue for coordinating agent work through priority, tag, status, claim, completion, failure, and statistics endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated API clients can read or modify queued task data.

Mitigation: Run the service only in a trusted local environment, or add authentication and authorization before network exposure.

Risk: Arbitrary payloads and results are retained in memory without explicit size or retention limits.

Mitigation: Avoid secrets in task payloads and add request-size limits plus retention or deletion controls for longer-running use.

Risk: Task state changes are accepted without additional workflow validation.

Mitigation: Add valid state-transition checks before using the queue for shared or production workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mirni/skills/gh-taskqueue)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and curl examples; API responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Starts a local FastAPI service backed by in-memory task state.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
