## Description: <br>
Searches local WhatsApp and chat conversations stored in the openclaw_audit PostgreSQL database so an agent can find, quote, or reply to past messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers or operators running a local OpenClaw WhatsApp audit database use this skill to help an agent search prior conversations, retrieve context, and reference messages by message_id. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad database access can expose private messages and unrelated telemetry. <br>
Mitigation: Use a dedicated read-only database role limited to the messages table and scope each lookup by chat, date, person, or keyword. <br>
Risk: Conversation searches can reveal sensitive personal content beyond the user's immediate request. <br>
Mitigation: Require explicit user authorization for each lookup and avoid broad private conversation dumps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/netanel-abergel/chat-history-local) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/netanel-abergel) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with SQL examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should keep database searches scoped by chat, date, person, or keyword and use LIMIT when querying.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
