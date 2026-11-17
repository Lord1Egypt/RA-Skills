## Description:

Posts content to WeChat Official Account through API or Chrome browser workflows, including markdown or HTML articles and image-text posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nengnengz](https://clawhub.ai/user/nengnengz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to prepare, convert, and publish WeChat Official Account articles or image-text posts from local content. It supports API-based drafts and browser-based workflows for accounts configured by the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article content and image references can expose local files, internal URLs, or sensitive diagram content during rendering or publishing.

Mitigation: Use only trusted Markdown, HTML, and image files; avoid sensitive PlantUML diagrams; reject references to internal URLs or arbitrary local paths before publishing.

Risk: WeChat credentials may be handled in plaintext configuration.

Mitigation: Prefer environment variables or a secret manager, keep credentials out of shared project files, and review account-specific configuration before use.

Risk: Browser-based publishing uses an authenticated Chrome profile and can affect the active WeChat account.

Mitigation: Use a dedicated restricted Chrome profile for this skill, isolate profiles per account, and confirm the selected account and draft before submitting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nengnengz/skills/baoyu-post-to-wechat-2)
- [Project homepage](https://github.com/JimLiu/baoyu-skills#baoyu-post-to-wechat)
- [Article posting guide](artifact/references/article-posting.md)
- [Image-text posting guide](artifact/references/image-text-posting.md)
- [First-time setup guide](artifact/references/config/first-time-setup.md)
- [WeChat Official Account platform](https://mp.weixin.qq.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and publication status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local TypeScript scripts to convert content, upload media, create drafts, or automate a browser session.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.56.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
