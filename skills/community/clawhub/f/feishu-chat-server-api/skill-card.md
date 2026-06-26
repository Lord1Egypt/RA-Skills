## Description: <br>
Manage Feishu group chats through Feishu server APIs, including create, get details, list members, add members, remove members, and disband chats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wodenwang](https://clawhub.ai/user/wodenwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to route Feishu group-chat administration requests to the appropriate Feishu server API action for creating chats, reading chat details, listing members, adding members, removing members, or disbanding chats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can remove members from Feishu chats or disband chats using privileged credentials. <br>
Mitigation: Use a least-privilege Feishu app and require explicit confirmation after restating the target chat ID and affected member IDs before any remove-member or disband-chat action. <br>
Risk: Incorrect or guessed user identifiers could affect the wrong Feishu users or chats. <br>
Mitigation: Use only confirmed Feishu user_id or open_id values and avoid guessing identifiers from names, email addresses, or phone numbers. <br>
Risk: Local app credentials may expose privileged Feishu access if mishandled. <br>
Mitigation: Prefer scoped credentials, keep local config files private, and pass secrets only through the documented credential paths. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/wodenwang/feishu-chat-server-api) <br>
- [Project homepage](https://github.com/wodenwang/feishu-extension-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON argument examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials from explicit arguments, a local JSON config file, or FEISHU_APP_ID and FEISHU_APP_SECRET environment variables.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
