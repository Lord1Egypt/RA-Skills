## Description: <br>
Local-first execution queue for OpenClaw agents that turns follow-up commitments into workspace-scoped tasks, claims work during heartbeat, and can explicitly dispatch tasks to another registered agent workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoujiejun](https://clawhub.ai/user/zoujiejun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Agent Todo to convert promised follow-up work into executable queue items, let heartbeat claim runnable tasks, and track completion or blocking status. It is most useful for local-first OpenClaw workspaces that need structured background execution and optional multi-agent dispatch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reply content and scheduled hooks may create or claim executable tasks without enough user review. <br>
Mitigation: Enable hooks or cron only after reviewing the task-creation inputs, and require approval before dispatching or executing queued work. <br>
Risk: Persistent queue files and multi-agent dispatch can move work across agent workspaces. <br>
Mitigation: Keep queue files and workspaces scoped to trusted agents, and review target workspace identity before using dispatch. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoujiejun/agent-todo) <br>
- [README](README.md) <br>
- [Specification](SPEC.md) <br>
- [OpenClaw Hooks Integration Guide](references/openclaw-hooks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Text and Markdown guidance with inline shell commands; runtime queue data is stored as JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update workspace-local queue files and managed heartbeat configuration when the user enables those commands.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
