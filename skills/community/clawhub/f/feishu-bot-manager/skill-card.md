## Description: <br>
Manage Feishu bots in OpenClaw configuration with add, delete, update, list, and info operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiangxinag-princess](https://clawhub.ai/user/xiangxinag-princess) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage Feishu bot entries and bindings in an OpenClaw configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent OpenClaw configuration changes, including adding, updating, or deleting Feishu bot entries and bindings. <br>
Mitigation: Review intended changes before execution, confirm the target botId before update or delete operations, and keep the generated OpenClaw configuration backups. <br>
Risk: Feishu app secrets may be stored in ~/.openclaw/openclaw.json and its backups or exposed through shared chats and shell history. <br>
Mitigation: Use non-production Feishu credentials where possible, protect the OpenClaw config and backup files, and avoid pasting secrets into shared chats or shell history. <br>
Risk: New Feishu bot entries may allow broad access until allow lists are restricted. <br>
Mitigation: Restrict Feishu allow lists after adding a bot and restart the OpenClaw gateway only after reviewing the resulting configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiangxinag-princess/feishu-bot-manager) <br>
- [Publisher profile](https://clawhub.ai/user/xiangxinag-princess) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or terminal text with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may update OpenClaw configuration files and create backups when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
