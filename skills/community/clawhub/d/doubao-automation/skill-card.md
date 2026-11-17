## Description:

豆包自动化操作技能基于 Playwright CDP 协议接管已登录 Edge 浏览器，实现豆包 AI 的自动化操作，支持批量生成图片、批量生成视频、文本对话和下载生成内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hitjcl](https://clawhub.ai/user/hitjcl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and automation developers use this skill to operate Doubao through an already logged-in Microsoft Edge browser for chat, image generation, video generation, image-to-video conversion, and downloading recent generated content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a logged-in Edge browser broadly and may disrupt or expose unrelated browser sessions.

Mitigation: Use a separate Edge profile dedicated to Doubao, close unrelated browser sessions first, avoid sensitive prompt files or image uploads, and stop the CDP-enabled browser after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hitjcl/skills/doubao-automation)
- [Publisher profile](https://clawhub.ai/user/hitjcl)
- [Doubao website](https://www.doubao.com/)
- [Doubao chat endpoint used by the skill](https://www.doubao.com/chat/)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and script-generated text or downloaded media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a logged-in Edge profile exposed through local CDP on port 9222.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
