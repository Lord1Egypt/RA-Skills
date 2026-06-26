## Description: <br>
Run and manage long-running OpenClaw or Clawdbot tasks asynchronously so agents can return immediately and push results after completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Enderfga](https://clawhub.ai/user/Enderfga) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill when a requested command, analysis, API call, or multi-step operation may exceed normal HTTP response timeouts. It guides the agent to start an async task, perform the work, and push a completion or failure result to the active OpenClaw or Clawdbot session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task results and session IDs may be sent to an OpenClaw or Clawdbot session or to a configured push endpoint. <br>
Mitigation: Use only trusted HTTPS endpoints and avoid including secrets in task descriptions, status updates, results, or failure messages. <br>
Risk: When multiple sessions are active, results may be pushed to the wrong session. <br>
Mitigation: Set OPENCLAW_SESSION explicitly when session routing matters. <br>
Risk: An async task can be started and then left incomplete, causing the user not to receive a final result. <br>
Mitigation: Pair every start command with done or fail, and use status checks when a task lifecycle is uncertain. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Enderfga/async-task) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and environment variable examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can emit CLI status messages, pushed task results, failure messages, and optional custom endpoint configuration.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
