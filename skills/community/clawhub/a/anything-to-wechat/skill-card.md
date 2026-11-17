## Description:

Converts files, folders, URLs, or briefs into WeChat-compatible HTML articles and publishes them to a WeChat Official Account draft box.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lutongsuo](https://clawhub.ai/user/lutongsuo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn documents, folders, URLs, or article ideas into WeChat Official Account drafts. It handles HTML generation, WeChat compatibility conversion, cover image preparation, and draft upload for later review in WeChat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install Python packages at runtime.

Mitigation: Review before installing and preinstall pinned dependencies in an isolated environment.

Risk: The publishing flow uses WeChat account credentials.

Mitigation: Use environment variables or a secret store, and avoid typing AppSecret into an echoed interactive prompt.

Risk: The skill can fetch arbitrary remote image URLs and upload images and content to WeChat.

Mitigation: Avoid untrusted HTML or remote image URLs and confirm exactly what content and images will be uploaded before creating a draft.

Risk: The workflow uploads to the WeChat draft box without a clear final consent boundary in the security evidence.

Mitigation: Run it only with the intended WeChat account and require operator review of the generated article before executing the publish step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lutongsuo/skills/anything-to-wechat)
- [Publisher profile](https://clawhub.ai/user/lutongsuo)
- [WeChat Official Account platform](https://mp.weixin.qq.com/)
- [WeChat Official Account API base](https://api.weixin.qq.com/cgi-bin)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a WeChat-ready HTML article, optional cover image, and WeChat draft media ID when publishing succeeds.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
