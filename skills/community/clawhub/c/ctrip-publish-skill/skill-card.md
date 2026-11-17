## Description:

携程内容中心全自动发布技能，支持从 Bing Images 搜索高清无版权图片、自动填写标题正文、自动上传图片、自动选择目的地、自动点击发布。适用于旅行攻略、美食推荐等图文笔记发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ansike](https://clawhub.ai/user/ansike)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators and operators use this skill to draft and automate Ctrip travel-note publishing workflows, including page navigation, title and body entry, image upload guidance, destination selection, and final publishing steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a logged-in Chrome session and affect a Ctrip publishing account.

Mitigation: Run it only in a browser profile intended for this workflow and review every title, body, image, destination, and publish action before completion.

Risk: Generated browser scripts and post content may be unsafe or incorrect when based on untrusted input.

Mitigation: Use trusted source material, inspect generated text and JavaScript before execution, and avoid pasting unreviewed content into an authenticated session.

Risk: Install-time dependency downloads can change the runtime environment.

Mitigation: Pin or preinstall dependencies in a controlled environment before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ansike/skills/ctrip-publish-skill)
- [Ctrip picture-text publishing page](https://we.ctrip.com/publish/publishPictureText)
- [Ctrip creator backend](https://we.ctrip.com/publish/publishHome)
- [Ctrip content management](https://we.ctrip.com/publish/contentManagement)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with Python, JavaScript, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser automation steps that affect a logged-in Ctrip account.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
