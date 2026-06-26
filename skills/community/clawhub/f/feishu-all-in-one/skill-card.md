## Description: <br>
Feishu All In One helps agents configure Feishu bot messaging, send text, image, file, and interactive-card messages, handle card callbacks, and transcribe voice content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ArvenWang](https://clawhub.ai/user/ArvenWang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to Feishu workflows for bot messaging, file delivery, interactive cards, callback handling, and voice-to-text support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send Feishu messages and upload selected local files. <br>
Mitigation: Install it only for agents that should have Feishu messaging and file-upload capability, and review selected file paths before use. <br>
Risk: Feishu App Secret and OpenClaw configuration are required for operation. <br>
Mitigation: Keep FEISHU_APP_SECRET and ~/.openclaw/openclaw.json private, and avoid committing credentials to shared repositories. <br>
Risk: Card callback handling can forward full interaction data to a configurable OpenClaw Gateway. <br>
Mitigation: Disable gateway forwarding with gateway.enabled=false or remove the gateway token unless forwarding raw callback data is intended. <br>
Risk: The release security verdict is suspicious because gateway forwarding is not fully scoped in the user-facing documentation. <br>
Mitigation: Review the callback server behavior, gateway settings, and dependency versions before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ArvenWang/feishu-all-in-one) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [README.md](README.md) <br>
- [Confirmation Card Template](references/confirmation-card.json) <br>
- [Form Card Template](references/form-card.json) <br>
- [Poll Card Template](references/poll-card.json) <br>
- [Todo Card Template](references/todo-card.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, code, JSON] <br>
**Output Format:** [Markdown guidance with inline command, code, and JSON configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, node, Feishu app credentials, and an OpenClaw configuration file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and _meta.json; artifact SKILL.md lists a newer frontmatter version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
