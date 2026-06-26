## Description: <br>
Cancel a user-created OpenAnt task and reclaim escrowed funds after checking task status, reward details, and explicit user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ant-1984](https://clawhub.ai/user/ant-1984) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenAnt users use this skill when they need an agent to help cancel their own task, remove it from the marketplace, and verify any escrow refund. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cancellation is irreversible and may affect escrowed funds or assigned workers. <br>
Mitigation: Verify the task ID, title, status, reward amount, assignee state, and refund details, then require explicit user confirmation before running the cancel command. <br>
Risk: The user may try to cancel a task that is submitted, completed, already cancelled, refunded, or owned by someone else. <br>
Mitigation: Check the task status and creator authority first, and avoid cancellation paths that the OpenAnt task state does not allow. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are expected to use JSON output for status checks, cancellation, and refund verification.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
