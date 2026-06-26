## Description: <br>
Douyin DMs and video/note comment assistant. 抖音私信与视频/图文评论助手；可读私信、分析评论区，评论/回复等写入前必须确认。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moroiser](https://clawhub.ai/user/moroiser) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to operate Douyin through a dedicated logged-in browser profile for reading DMs, reviewing chat history, searching videos or notes, reading comments, and preparing sentiment briefs. It may send DMs or perform comment, reply, like, or share actions only after explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a logged-in Douyin browser profile and can expose selected DMs or comments to the agent context. <br>
Mitigation: Use a dedicated openclaw profile, read only content the user is comfortable sharing with the agent, and clear the Douyin login when access should no longer be available. <br>
Risk: Messaging, commenting, replying, liking, or sharing can affect an external Douyin account. <br>
Mitigation: Before any write action, verify the visible account, target recipient or comment, and exact content, then require explicit user confirmation. <br>
Risk: Douyin web DOM details and card-style messages may be incomplete or change over time. <br>
Mitigation: Prefer visible browser confirmation and conservative parsing; mark unsupported or ambiguous cards as incomplete instead of inferring hidden details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moroiser/douyin-messager) <br>
- [Douyin](https://www.douyin.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown and browser-action guidance with inline JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a dedicated openclaw browser profile with an active Douyin login.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
