## Description: <br>
CloudPlus helps an agent operate the CloudPlus enterprise messaging app to send messages and files, search contacts, groups, files, messages, and light apps, retrieve chat history and saved content, open links and apps, and launch CloudPlus. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billyang1222](https://clawhub.ai/user/billyang1222) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and their agents use this skill to operate CloudPlus for workplace messaging tasks, including sending messages or files, finding people and groups, searching chat content, retrieving chat history, and opening CloudPlus resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send CloudPlus messages or files on the user's behalf. <br>
Mitigation: Confirm recipients, message text, and file paths before sending or opening shared content. <br>
Risk: Search and chat-history commands can expose sensitive workplace communications. <br>
Mitigation: Use specific queries and date ranges, and retrieve chat history only when needed for the user's request. <br>
Risk: Commands depend on local CloudPlus tooling and may fail if the desktop client or command-line dependency is unavailable. <br>
Mitigation: Check Node.js, npm, mcp-cloudplus, and the CloudPlus desktop client before running requested operations. <br>


## Reference(s): <br>
- [CloudPlus ClawHub release](https://clawhub.ai/billyang1222/cloudplus) <br>
- [Node.js](https://nodejs.org) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Natural-language guidance with shell commands and parsed JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npm, the mcp-cloudplus command, and a running CloudPlus desktop client for some operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
