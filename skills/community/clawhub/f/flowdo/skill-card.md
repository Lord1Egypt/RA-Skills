## Description: <br>
Task and workflow manager with kanban-style status tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and terminal users use Flowdo to keep a local task list, update task state, search entries, and export recorded work items from a shell workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task text and command history are stored locally under the FlowDo data directory, so sensitive notes could persist on disk. <br>
Mitigation: Avoid entering secrets or highly sensitive task details, and review or clear the local FlowDo data directory according to your retention needs. <br>
Risk: The artifact behavior is a basic local task-list shell utility and does not fully match the documented kanban workflow. <br>
Mitigation: Validate the installed commands in a test directory before relying on Flowdo for workflow tracking. <br>


## Reference(s): <br>
- [Flowdo on ClawHub](https://clawhub.ai/ckchzh/flowdo) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The installed utility writes task entries and command history to the local FlowDo data directory.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
