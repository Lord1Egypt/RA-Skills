## Description: <br>
In-memory priority task queue for AI agents. Create tasks with priorities and tags, claim the next highest-priority task, mark tasks complete or failed, filter by status or tag, and get queue statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate lightweight task handoff through a local priority queue API. It supports creating, claiming, completing, failing, filtering, and summarizing tasks for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The queue stores task state in process memory, so restarts or crashes can lose pending, running, completed, and failed task records. <br>
Mitigation: Use it for transient workflow coordination, or add durable storage before relying on it for persistent or audit-sensitive work. <br>
Risk: The API exposes task creation and state-changing endpoints without documented authentication. <br>
Mitigation: Bind the service to trusted local interfaces or add authentication before using it on shared or networked hosts. <br>
Risk: Task payloads, results, and errors may contain sensitive workflow data. <br>
Mitigation: Keep credentials scoped, avoid placing secrets in task payloads, and review commands before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mirni/gh-taskqueue) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions] <br>
**Output Format:** [JSON API responses and Markdown usage examples with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local FastAPI service backed by in-memory task state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
