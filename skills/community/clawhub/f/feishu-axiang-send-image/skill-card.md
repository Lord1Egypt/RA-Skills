## Description: <br>
Uses a user-configured Feishu app to upload and send a local image to a specified Feishu user or group chat, with PNG, JPG, GIF, and WEBP support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[icesumer-lgtm](https://clawhub.ai/user/icesumer-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and operators use this skill to send a selected local image to a Feishu user or group chat through their own configured Feishu app. It is useful for workflows that need to share generated screenshots, visual artifacts, or local images into Feishu conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally uploads the selected local image through the configured Feishu app, which can expose sensitive image content if the wrong file is chosen. <br>
Mitigation: Verify the file path and recipient before each send, and avoid sending sensitive images unless they are intended to be shared through Feishu. <br>
Risk: Feishu app credentials and the default target must be configured by the user, and hardcoded secrets can be leaked if committed or shared. <br>
Mitigation: Configure only your own AppID and AppSecret, keep credentials out of public repositories, and prefer environment variables or a private configuration file for production use. <br>
Risk: The documented allow-list is not an enforced control unless the user adds that enforcement. <br>
Mitigation: Do not rely on the allow-list documentation alone; add and test recipient validation if sends must be restricted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/icesumer-lgtm/feishu-axiang-send-image) <br>
- [Feishu tenant_access_token API](https://open.feishu.cn/document/ukTMukTMukTM/ukDNz4SO0MjL5QzM/auth-v3-auth/tenant_access_token_internal) <br>
- [Feishu image message API](https://open.feishu.cn/document/ukTMukTMukTM/uYjNwUjL2YDM14iN2ATN) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Text, Guidance] <br>
**Output Format:** [Markdown instructions with command examples and terminal status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local image path, user-provided Feishu app credentials, and an optional target user or chat identifier.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
