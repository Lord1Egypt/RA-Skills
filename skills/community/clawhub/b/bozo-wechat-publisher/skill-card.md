## Description:

Publishes Markdown articles to a WeChat Official Account draft box with wenyan-cli formatting, theme support, image upload handling, and a curl fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bozoyan](https://clawhub.ai/user/bozoyan)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and content operators use this skill to convert Markdown posts into formatted WeChat Official Account drafts, choose themes or code highlighting, upload article images, and troubleshoot publishing failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires WeChat Official Account credentials and can publish drafts using those credentials.

Mitigation: Provide AppID and AppSecret only for the specific publishing command or session, and install only when you accept that account access.

Risk: Setup guidance may encourage unsafe shell installation and persistent credential storage.

Mitigation: Avoid curl-to-sudo-bash setup paths and do not store AppSecret in shell startup files.

Risk: Markdown content, cover images, and embedded images may be sent to WeChat during publishing.

Mitigation: Review article content and cover/image paths before running publish commands.

Risk: Global package installation can pull the current wenyan-cli behavior rather than a reviewed version.

Mitigation: Prefer a pinned, manually installed wenyan-cli version that has been reviewed in the target environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bozoyan/skills/bozo-wechat-publisher)
- [wenyan-cli GitHub](https://github.com/caol64/wenyan-cli)
- [WeChat Official Account API documentation](https://developers.weixin.qq.com/doc/offiaccount/)
- [Wenyan documentation](https://wenyan.yuzhi.tech)
- [Themes reference](references/themes.md)
- [Troubleshooting guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce publishing commands that send article content and images to WeChat; requires WeChat AppID/AppSecret credentials and IP allowlisting.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
