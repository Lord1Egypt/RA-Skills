## Description: <br>
Coordinates multi-agent Feishu group chats with mention-priority routing, task assignment, and relevance-based response rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tazio7](https://clawhub.ai/user/Tazio7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to coordinate several agents in a Feishu group chat, route messages by @ mention or keywords, assign collaborative subtasks, and reduce duplicate agent responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill broadly changes when agents respond in group chat and may override local group-chat rules. <br>
Mitigation: Review local chat policies before installation and allow the skill to override response rules only in approved groups. <br>
Risk: The release contains environment-specific Feishu chat and user identifiers, and the sample configuration gives multiple agents the same identity. <br>
Mitigation: Replace Feishu IDs with private configuration and give each agent a distinct identity before use. <br>
Risk: Keyword-based routing can trigger ambiguous or unnecessary agent responses. <br>
Mitigation: Narrow keyword triggers or require explicit @ mentions for sensitive or high-traffic chats. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Tazio7/collaboration-manager) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Configuration](artifact/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, markdown, shell commands] <br>
**Output Format:** [Markdown instructions with JSON configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Feishu group-chat routing rules, agent role guidance, task-status message templates, and troubleshooting commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
