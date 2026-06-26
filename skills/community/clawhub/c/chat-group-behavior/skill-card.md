## Description: <br>
How to join, participate in, and leave group conversations on messaging platforms (WhatsApp, Signal, Telegram, etc.). Use when the owner tags the agent into a group chat, when the agent needs to open or close the participation gate, or as a reference for correct group chat behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanblanchfield](https://clawhub.ai/user/seanblanchfield) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agent operators and developers use this skill to let an agent temporarily participate in owner-approved group chats, respond with appropriate group etiquette, and leave or extend participation on request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes live messaging access controls so an agent can receive messages from all members of an allowed group while active. <br>
Mitigation: Require owner approval, scope access to the specific group and duration, validate configuration changes, and restore the previous settings when the session closes. <br>
Risk: The skill includes session recovery guidance that can delete conversation transcripts. <br>
Mitigation: Use a supported recovery path when available, require explicit approval before deleting transcripts, and preserve a backup or rollback path. <br>
Risk: The skill depends on scheduled close actions to reduce group access after the participation window ends. <br>
Mitigation: Confirm the close schedule with the owner and verify that access has been closed after the scheduled time. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seanblanchfield/chat-group-behavior) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline configuration paths, commands, and message examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose temporary messaging configuration changes, scheduled close actions, and concise group chat responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
