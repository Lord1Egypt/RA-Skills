## Description:

Converts files such as PDF, Word, Excel, PowerPoint, images, audio, and web pages into Markdown, generates WeChat-compatible article HTML, creates a cover image, and publishes the result to a WeChat Official Account draft box.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lutongsuo](https://clawhub.ai/user/lutongsuo)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, operators, and developers use this skill to turn common document, media, and web inputs into draft WeChat Official Account articles for review and publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-selected documents and can upload derived content to WeChat using Official Account credentials.

Mitigation: Use it only with documents intended for publication, keep account credentials in environment variables, and review the generated draft in WeChat before publishing.

Risk: The security summary notes that the skill can send content to external services and has cloud fallback behavior.

Mitigation: Prefer local conversion and keep cloud fallbacks disabled unless the user explicitly approves sending content to the external conversion service.

Risk: The security summary notes unpinned runtime package installation.

Mitigation: Install dependencies in a pinned, pre-reviewed Python environment before running the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lutongsuo/skills/file-to-wechat)
- [Publisher Profile](https://clawhub.ai/user/lutongsuo)
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown instructions, shell commands, generated Markdown files, WeChat-compatible HTML, cover image files, and WeChat draft publication status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read user-selected files, generate derived article assets, and use WeChat Official Account credentials to upload drafts.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
