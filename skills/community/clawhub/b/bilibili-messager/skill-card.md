## Description: <br>
Sends Bilibili direct messages, replies to existing conversations, and reads chat history through browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moroiser](https://clawhub.ai/user/moroiser) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Bilibili account operators use this skill to manage Bilibili direct-message conversations from a logged-in, dedicated OpenClaw browser profile. It supports sending confirmed messages, replying to existing conversations, and reading selected chat history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a logged-in Bilibili browser session, which gives browser automation access to private-message account capabilities. <br>
Mitigation: Use the dedicated openclaw browser profile, verify the active Bilibili account before use, and close or clear the Bilibili session when it is no longer needed. <br>
Risk: Reading chat history exposes private messages to the agent context. <br>
Mitigation: Read only conversations the user is willing to share with the agent, and avoid highly sensitive or non-voluntary private conversations. <br>
Risk: A send or reply action could contact the wrong recipient or send unintended content. <br>
Mitigation: Require explicit confirmation of the recipient and full message content before writing or sending any message. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moroiser/bilibili-messager) <br>
- [Bilibili private messages](https://message.bilibili.com/#/whisper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with browser commands and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a logged-in Bilibili session in the dedicated openclaw browser profile; send operations require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.4.8 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
