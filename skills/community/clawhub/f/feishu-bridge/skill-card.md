## Description: <br>
Connects a Feishu or Lark bot to Clawdbot over WebSocket long-connection so developers can use Feishu as a messaging channel without a public server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AlexAnys](https://clawhub.ai/user/AlexAnys) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to set up, run, troubleshoot, and manage a Feishu/Lark bot bridge that forwards messages to a local Clawdbot Gateway and posts the agent's replies back to Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured Feishu bot can send chat text to the local Clawdbot agent and post replies back to Feishu. <br>
Mitigation: Install only on trusted machines, protect the Feishu secret and Clawdbot configuration, and restrict the bot to intended chats. <br>
Risk: The optional macOS LaunchAgent can keep the bridge running in the background. <br>
Mitigation: Load the LaunchAgent only when persistent operation is desired and unload it when the bridge should not run. <br>
Risk: Group chat behavior may forward unintended messages if response rules are too broad. <br>
Mitigation: Review and tune the group-response rules before adding the bot to shared chats. <br>


## Reference(s): <br>
- [Feishu Open Platform](https://open.feishu.cn/app) <br>
- [ClawHub Skill Page](https://clawhub.ai/AlexAnys/feishu-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with bash command snippets and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include macOS launchd service steps, Feishu bot configuration, environment variables, and diagnostic commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
