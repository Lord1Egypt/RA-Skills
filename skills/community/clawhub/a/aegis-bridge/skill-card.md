## Description: <br>
Orchestrate Claude Code sessions via Aegis HTTP/MCP bridge for coding tasks, issue implementation, PR review, CI fixes, batch tasks, and multi-agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onestepat4time](https://clawhub.ai/user/onestepat4time) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to spawn, monitor, communicate with, and clean up local Claude Code sessions through an Aegis server. It supports supervised coding automation workflows such as implementing issues, reviewing pull requests, fixing CI, and coordinating parallel agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can drive local Claude Code sessions that may request bash execution or other high-impact permissions. <br>
Mitigation: Review permission and bash prompts manually, reject unsafe actions, and restrict workDir values to trusted repositories. <br>
Risk: The heartbeat and workflow examples normalize auto-approving agent actions. <br>
Mitigation: Avoid auto-approval loops unless running in a tightly sandboxed environment with an explicit allowlist. <br>
Risk: The skill depends on a local Aegis server controlling sessions in the user's environment. <br>
Mitigation: Install only when local Aegis orchestration is intended, prefer project-scoped MCP setup, and verify the server with the provided health check before use. <br>


## Reference(s): <br>
- [Aegis Bridge ClawHub listing](https://clawhub.ai/onestepat4time/aegis-bridge) <br>
- [API Quick Reference](references/api-quick-ref.md) <br>
- [Agent Template](references/agent-template.md) <br>
- [Heartbeat Template](references/heartbeat-template.md) <br>
- [Workflow Examples](references/workflow-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown] <br>
**Output Format:** [Markdown guidance with inline bash commands, JSON request examples, and MCP tool references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Aegis service and Claude Code CLI; examples may create, approve, interrupt, or terminate local agent sessions.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
