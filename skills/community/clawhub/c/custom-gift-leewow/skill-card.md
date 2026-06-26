## Description: <br>
Helps users browse customizable Leewow products, upload a design image, generate an AI product mockup, and send browse or preview results through Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yqxu](https://clawhub.ai/user/yqxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to browse customizable gifts, turn user-provided images or ideas into product mockups, and deliver product cards or preview results in Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send Feishu messages using app credentials and may continue deferred sends in a background process. <br>
Mitigation: Use a least-privilege Feishu app, restrict the receive target, and review whether deferred Feishu sending should be enabled before deployment. <br>
Risk: The skill uploads user-provided images and can generate COS access links. <br>
Mitigation: Avoid sensitive personal photos, keep image inputs within the intended workspace, and review COS presigned URL use and expiration settings. <br>
Risk: Changing LEEWOW_API_BASE could direct credentialed requests away from the official Leewow service. <br>
Mitigation: Keep LEEWOW_API_BASE on the official Leewow domain unless the deployment owner has explicitly approved another endpoint. <br>


## Reference(s): <br>
- [Custom Gift Leewow on ClawHub](https://clawhub.ai/yqxu/custom-gift-leewow) <br>
- [Skill homepage from ClawHub metadata](https://github.com/AIDiyTeams/claw-skill/tree/main/custom-gift-leewow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, API calls] <br>
**Output Format:** [JSON tool results and Markdown/Feishu card content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return finalAssistantReply=NO_REPLY after sending product cards or preview results directly to Feishu.] <br>

## Skill Version(s): <br>
1.0.24 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
