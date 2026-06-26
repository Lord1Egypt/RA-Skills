## Description: <br>
Feishu Cli Chat helps agents browse Feishu chats, retrieve group or direct-message history, inspect message details, add reactions, pin or unpin messages, delete messages, and manage group chat information and members through feishu-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GISwilson](https://clawhub.ai/user/GISwilson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents assisting authorized Feishu users use this skill to inspect recent chat context, search conversations, summarize group activity, and perform chat-management actions through feishu-cli. It is intended for workflows where the user can provide explicit chat names, chat IDs, message IDs, keywords, or time ranges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a logged-in Feishu account to access private chats and broad chat history. <br>
Mitigation: Use explicit chat names, chat IDs, message IDs, keywords, and time ranges; avoid broad exports of chat history. <br>
Risk: The skill includes message and group-management actions such as delete, update, pin, unpin, reactions, and member changes. <br>
Mitigation: Require manual confirmation before performing destructive or state-changing actions. <br>
Risk: Chat history may be saved temporarily as JSON during pagination or analysis. <br>
Mitigation: Remove temporary JSON files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/GISwilson/feishu-cli-chat) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON-oriented outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a logged-in Feishu CLI user token for core chat browsing and management commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
