## Description: <br>
Sends private or group Feishu messages through the current agent's configured Feishu app, showing the configured bot name and handling app-isolated open_id values. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pikaqiuyaya](https://clawhub.ai/user/pikaqiuyaya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill in multi-agent Feishu workflows to send status updates, task results, or operational messages to authorized users or group chats from the executing agent's own bot identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can send Feishu private or group messages using local bot credentials, which could reach unintended recipients or disclose sensitive content. <br>
Mitigation: Install only where operators are authorized to use the Feishu bot credentials, verify recipients before sending, and avoid sending secrets or sensitive incident details unless explicitly permitted. <br>
Risk: Recipient IDs may be taken from gateway logs, increasing the chance of stale, mismatched, or overexposed contact identifiers. <br>
Mitigation: Prefer verified recipient sources where possible, restrict access to OpenClaw config files and gateway logs, and avoid unnecessary use of log-derived IDs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pikaqiuyaya/feishu-agent-messenger-v2) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Feishu text message results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq, curl, local Feishu app credentials, and a verified open_id or chat_id target.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
