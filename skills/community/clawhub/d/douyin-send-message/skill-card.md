## Description: <br>
在抖音网页版发送私信消息，适用于发送抖音私信、提醒续火花，或与人物关系管理技能配合使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[calvin-dean](https://clawhub.ai/user/calvin-dean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to have an agent send a Douyin web private message to a named contact from a logged-in browser session. It supports direct contact names or names resolved through a separate relationship-management skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send Douyin private messages from an existing logged-in browser session without a clear final confirmation step. <br>
Mitigation: Require explicit confirmation of the resolved recipient, active account context, and exact message text before sending; consider using an isolated browser profile or fresh login. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/calvin-dean/douyin-send-message) <br>
- [Douyin chat page](https://www.douyin.com/chat) <br>
- [Douyin self profile page](https://www.douyin.com/user/self) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code] <br>
**Output Format:** [Markdown instructions with browser automation steps and JavaScript/Playwright snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces private-message automation guidance for a specified contact and message.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
