## Description: <br>
抖音创作者平台视频上传发布。触发条件：用户要求上传视频到抖音、发布抖音视频、自动上传视频到抖音创作者平台 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[l1angjy](https://clawhub.ai/user/l1angjy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and operators use this skill to guide an agent through uploading a local video to Douyin Creator Platform, setting a title and visibility, and publishing only after explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global, subject to Douyin Creator Platform availability and account eligibility. <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates a logged-in Douyin Creator session and can publish content after confirmation. <br>
Mitigation: Use the dedicated douyin-profile or sandbox mode, review the file name, title, and visibility, and confirm only the intended upload. <br>
Risk: Using a real browser profile could expose unrelated cookies, accounts, or settings. <br>
Mitigation: Avoid profile="user" and use the isolated douyin-profile or sandbox configuration described by the artifact. <br>
Risk: Saved visibility preferences may not match the intended audience for a specific upload. <br>
Mitigation: Check the selected visibility before confirming each publication and override the saved preference when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/l1angjy/douyin-auto-publish) <br>
- [Publisher profile](https://clawhub.ai/user/l1angjy) <br>
- [Douyin Creator Platform](https://creator.douyin.com/creator-micro/home) <br>
- [Douyin upload page](https://creator.douyin.com/creator-micro/content/upload) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Browser actions] <br>
**Output Format:** [Markdown instructions with inline shell commands and browser action examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided video path, title, visibility choice, logged-in Douyin Creator session, and explicit confirmation before publishing.] <br>

## Skill Version(s): <br>
2.2.7 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
