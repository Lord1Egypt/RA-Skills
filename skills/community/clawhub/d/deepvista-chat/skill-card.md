## Description: <br>
DeepVista Chat: Send messages to the AI agent and manage chat sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jingconan](https://clawhub.ai/user/jingconan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to send messages to DeepVista, start or continue chat sessions, list and search sessions, inspect session metadata, and delete sessions after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The +send command can create or update remote chat sessions and may trigger DeepVista agent actions. <br>
Mitigation: Require explicit user confirmation before running +send, especially when the requested message could create cards, search the web, or execute tools. <br>
Risk: The delete command removes remote chat data. <br>
Mitigation: Confirm the target chat ID and user intent before running delete. <br>
Risk: Authentication behavior is handled by the companion shared DeepVista skill. <br>
Mitigation: Review deepvista-shared before use so the agent understands profiles, authentication, and global flags. <br>


## Reference(s): <br>
- [DeepVista CLI homepage](https://cli.deepvista.ai) <br>
- [ClawHub skill page](https://clawhub.ai/jingconan/deepvista-chat) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and streamed NDJSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the deepvista CLI and companion deepvista-shared skill for authentication and global flags.] <br>

## Skill Version(s): <br>
0.1.0-alpha.21 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
