## Description: <br>
Launch and manage Cursor Cloud Agents via the official API v0. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[siaslfs](https://clawhub.ai/user/siaslfs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill to delegate coding tasks to Cursor Cloud Agents, monitor progress, send follow-up instructions, and collect PR or status output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Cursor API key that can operate on repositories authorized for the Cursor account. <br>
Mitigation: Use the least-privileged Cursor and repository access available, store the key with restricted file permissions, and rotate it if exposed. <br>
Risk: The create command may launch paid Cursor Cloud Agent work and can request automatic PR creation. <br>
Mitigation: Confirm the repository, branch or ref, task prompt, and auto-PR setting before running create; use --no-direct for tasks that need human review before code changes. <br>
Risk: Configured Feishu notifications can send task details, status, and possible conversation excerpts outside the local environment. <br>
Mitigation: Leave CURSOR_NOTIFY_TARGET and --notify unset unless that disclosure path is intended and approved. <br>
Risk: The background watcher embeds the Cursor API key in a spawned process while it polls. <br>
Mitigation: Avoid shared machines for long-running watchers, limit local process inspection access, and prefer short polling windows when possible. <br>


## Reference(s): <br>
- [Cursor Cloud Agent API documentation](https://cursor.com/docs/cloud-agent/api/endpoints) <br>
- [Cursor Dashboard](https://cursor.com/dashboard) <br>
- [How to Get Your Cursor Cloud Agent API Key](references/get-token.md) <br>
- [ClawHub release page](https://clawhub.ai/siaslfs/cursor-cloud-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, Markdown guidance, and JSON responses from Cursor API commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may call Cursor API v0, open agent URLs, poll agent status, and print summaries or fallback PR commands.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
