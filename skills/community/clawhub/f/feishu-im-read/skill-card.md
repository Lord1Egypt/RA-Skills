## Description: <br>
Guides an agent through reading Feishu IM chat history, thread replies, cross-chat message search, and downloading message image or file resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a3152557994-ship-it](https://clawhub.ai/user/a3152557994-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill when they need an agent to retrieve Feishu group or direct-message history, inspect thread replies, search messages by filters, or fetch attached message resources under the user's Feishu authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the user's Feishu authorization to read chats and fetch message resources, which can expose sensitive conversations or files. <br>
Mitigation: Use narrow requests that specify the exact chat, person, keyword, date range, and whether attachments or thread replies should be included. <br>
Risk: Broad searches, pagination, or automatic thread expansion can retrieve more message content than the user intended. <br>
Mitigation: Confirm scope before expanding threads or continuing pagination when the user asks for a summary or a limited result set. <br>
Risk: Downloaded images, files, audio, or video may contain private or regulated information. <br>
Mitigation: Fetch resources only when the user explicitly needs them and keep the result handling aligned with the user's access permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a3152557994-ship-it/feishu-im-read) <br>
- [Publisher profile](https://clawhub.ai/user/a3152557994-ship-it) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Text, Markdown] <br>
**Output Format:** [Markdown guidance with JSON tool-call parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May retrieve Feishu messages, thread replies, search results, and message resources under the user's authorization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
