## Description:

将 Markdown 文章通过用户目录浏览器会话发布到 CSDN。支持保存草稿、预览排版、人工确认发布；默认保持浏览器打开并复用登录态。

This skill is ready for commercial/non-commercial use.

## Publisher:

[love254443233](https://clawhub.ai/user/love254443233)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content publishers use this skill to save, preview, and publish Markdown articles to CSDN through an existing Edge or Chrome browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or save content through a logged-in CSDN browser session.

Mitigation: Use a dedicated browser profile and CSDN account you are comfortable granting publication access to.

Risk: The skill modifies article content before submission, including appending a configured WeChat QR section and replacing content after an existing matching heading.

Mitigation: Inspect the generated article and compare the draft before publishing.

Risk: The packaged WeChat QR configuration may not belong to the installing user.

Mitigation: Remove or replace the QR image URL and description in skill-config.json before use.

Risk: Publish mode can submit an article without a separate final confirmation step in the script.

Mitigation: Prefer draft-preview mode until explicit final confirmation and a non-destructive content diff are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/love254443233/skills/csdn-article-publish-plus)
- [CSDN Markdown editor](https://editor.csdn.net/md/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with command-line parameters and JSON execution results from the publishing script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser screenshots named csdn_<mode>_result.png in the current working directory.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
