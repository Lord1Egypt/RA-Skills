## Description: <br>
在微信视频号后台创建视频合集。触发场景：创建视频号合集、新建视频号合集、在视频号后台创建合集、创建视频合集。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[infiniteask](https://clawhub.ai/user/infiniteask) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and operators use this skill to guide an agent through creating a video collection in a logged-in WeChat Channels backend session. The skill focuses on navigation, tab awareness, form entry, confirmation, and post-creation checking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may operate the wrong logged-in WeChat Channels account or create a collection with an unintended title. <br>
Mitigation: Confirm the target account, exact collection title, and intended creation action before allowing browser actions. <br>
Risk: A broad trigger phrase may match requests that are not specifically about the WeChat Channels backend. <br>
Mitigation: Confirm that the user intends to create a collection in the WeChat Channels backend before proceeding. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/infiniteask/create-wechat-channel-collection-infinite) <br>
- [WeChat Channels backend](https://channels.weixin.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown instructions with browser-operation steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a logged-in WeChat Channels browser session and user confirmation of the target account, title, and creation action.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata); artifact frontmatter reports 1.0.0.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
