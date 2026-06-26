## Description: <br>
Bind a Feishu group chat to a specific OpenClaw agent, covering agent creation, workspace setup, binding configuration, session cleanup, and gateway restart. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Embracex1998](https://clawhub.ai/user/Embracex1998) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to route a Feishu group chat to a dedicated OpenClaw agent with an isolated workspace. It helps configure bindings, clean stale sessions, restart the gateway, and verify that messages reach the intended agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Editing OpenClaw routing configuration can bind the wrong Feishu group or account to an agent. <br>
Mitigation: Back up ~/.openclaw/openclaw.json first, confirm the exact Feishu account and chat IDs, and preserve existing bindings when editing. <br>
Risk: A group may continue using a stale session or an unintended shared workspace after routing changes. <br>
Mitigation: Use a dedicated workspace for the target agent, clean stale sessions for the chat ID, and restart the gateway before verifying the route. <br>
Risk: A group chat agent may process ordinary group messages when that is not intended. <br>
Mitigation: Consider setting requireMention:true for Feishu group configuration when the agent should only respond to explicit mentions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with bash, Python, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational checks for Feishu account IDs, group chat IDs, agent workspaces, session cleanup, and gateway restart.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
