## Description: <br>
Feishu Task Workbench lets an agent manage multiple Feishu/OpenClaw task workstreams from one chat, with separate task sessions and a local task registry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawnhan98](https://clawhub.ai/user/shawnhan98) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a task workbench inside Feishu/OpenClaw, creating, switching, continuing, summarizing, closing, and archiving task-specific workstreams without mixing their context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task titles, summaries, and session keys are stored in a local registry and may expose sensitive work context. <br>
Mitigation: Avoid putting highly sensitive information in task titles or summaries, and keep registries isolated per Feishu account and contact. <br>
Risk: Cross-session task routing depends on host session tools and can fail or mix work if those tools are missing or misconfigured. <br>
Mitigation: Review host settings before use and keep the documented capability gate for sessions_spawn, sessions_send, and sessions_history before creating or updating tasks. <br>


## Reference(s): <br>
- [Feishu Task Workbench Implementation](references/implementation.md) <br>
- [Single-Entry Multi-Task Workbench Protocol](references/protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown task replies with shell commands and configuration snippets when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Task replies should include the active task header when routed to a concrete task.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
