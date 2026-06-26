## Description: <br>
Sends Feishu text reports from local agent-specific credentials to a specified open_id or chat_id. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pikaqiuyaya](https://clawhub.ai/user/pikaqiuyaya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents in multi-agent workflows use this skill to send completion reports to Feishu users or group chats under an agent-specific Feishu bot identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use local Feishu bot credentials to send messages as a caller-selected agent. <br>
Mitigation: Restrict permissions on ~/.openclaw configuration files and use least-privilege Feishu apps for each agent. <br>
Risk: Callers choose the open_id or chat_id destination, which can send reports to unintended users or groups. <br>
Mitigation: Pre-approve allowed destinations and validate target IDs before agents invoke the script. <br>
Risk: Task output or message content may include secrets or sensitive information, and the script echoes message details to stdout. <br>
Mitigation: Redact secrets and sensitive task output before sending messages, and avoid logging sensitive message content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pikaqiuyaya/feishu-auto-report) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text, guidance] <br>
**Output Format:** [Shell command invocation with plain text status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and local Feishu app credentials in ~/.openclaw/openclaw-{agentId}.json.] <br>

## Skill Version(s): <br>
5.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
