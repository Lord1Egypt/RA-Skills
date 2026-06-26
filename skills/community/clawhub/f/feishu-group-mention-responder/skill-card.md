## Description: <br>
Responds automatically in Feishu group chats when the bot is mentioned or receives a direct message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lorpha](https://clawhub.ai/user/Lorpha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure an agent to detect Feishu group mentions or direct messages and reply in the same chat. It is intended for Feishu bots that need to recognize their own identity, address the sender, and avoid duplicate or looping replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bot reads relevant Feishu chat events and can send replies as the bot. <br>
Mitigation: Limit Feishu app permissions and group access to intended chats before enabling the skill. <br>
Risk: Mention detection or reply handling could produce unexpected or repeated replies. <br>
Mitigation: Test mention handling, direct-message handling, bot identity matching, and duplicate-reply prevention before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lorpha/feishu-group-mention-responder) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown with JSON and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Feishu message handling guidance includes mention detection, sender extraction, reply construction, and bot permission considerations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
