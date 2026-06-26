## Description: <br>
Chat and ask functionality for OpenClaw. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[xander-art](https://clawhub.ai/user/xander-art) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users can use this skill for simple local chat, question answering, and chat-history inspection during demos or lightweight experimentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts may be printed to local stderr logs. <br>
Mitigation: Avoid sending secrets, credentials, or sensitive personal data through the chat and ask tools. <br>
Risk: Chat history is local, in-memory, and sample data may be generated for empty history reads. <br>
Mitigation: Do not treat chat_history output as a durable audit trail or source of record. <br>
Risk: Responses are simple canned or echo-style outputs rather than validated external knowledge. <br>
Mitigation: Use the skill for basic demos and verify important answers with authoritative sources. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/xander-art/chat-ask) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [JSON objects containing chat responses, answers, chat history, summaries, or error status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful responses include status and tool fields; chat and ask responses also include timestamps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
