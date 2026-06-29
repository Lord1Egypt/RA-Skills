## Description: <br>
在抖音网页版发送私信消息。当用户想发送抖音私信、提醒续火花、或者提到“抖音发消息”、“发抖音私信”、“douyin send message”时触发，支持独立使用或配合人物关系管理技能使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[calvin-dean](https://clawhub.ai/user/calvin-dean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to send a Douyin private message to a named contact from Douyin Web. It can use a manually supplied Douyin nickname or a nickname resolved by an optional person-relation-manager skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send Douyin messages from a logged-in browser session without a final confirmation. <br>
Mitigation: Require the agent to confirm the exact recipient and message before sending. <br>
Risk: The automation can expose or use an existing browser profile during message sending. <br>
Mitigation: Use only a dedicated Douyin automation browser profile and avoid sensitive messages. <br>
Risk: The optional person-relation-manager install changes the dependency set for the workflow. <br>
Mitigation: Treat that install as a separate dependency decision and review it before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/calvin-dean/skills/douyin-send-message) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands] <br>
**Output Format:** [Markdown instructions with inline JavaScript, browser actions, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Takes a contact name and message content; browser automation may act in a logged-in Douyin session.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
