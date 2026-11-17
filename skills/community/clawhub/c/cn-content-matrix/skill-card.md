## Description:

CN Content Matrix generates Chinese platform-native content for Xiaohongshu, WeChat Official Account, Douyin, and Bilibili, supporting single-platform generation, full content matrices, and compliance review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fullstackcrew-alpha](https://clawhub.ai/user/fullstackcrew-alpha)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and marketing teams use this skill to turn one Chinese-language topic into platform-specific drafts and to review existing drafts against platform style, format, SEO, and sensitive-word rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied topics can be interpolated into Bash in a way that may execute unintended commands.

Mitigation: Fix the Bash topic handling before installation or restrict topics to trusted input until command construction is safely quoted and validated.

Risk: WebSearch can expose confidential or sensitive topic terms outside the local environment.

Mitigation: Avoid confidential topics or disable web research for sensitive work, and make disclosure expectations clear to users before generation.

Risk: The declared tool access is broader than necessary, including Agent, WebFetch, and Edit permissions.

Mitigation: Remove unneeded tool permissions and add scoped file-read and output controls before broad deployment.

Risk: The content-review flow reads user-specified local files.

Mitigation: Run reviews only on files intended for agent access and avoid sensitive local documents unless the user explicitly wants them reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fullstackcrew-alpha/skills/cn-content-matrix)
- [README](artifact/README.md)
- [Xiaohongshu Content Specification](artifact/references/xiaohongshu.md)
- [WeChat Official Account Content Specification](artifact/references/wechat-mp.md)
- [Douyin Script Specification](artifact/references/douyin.md)
- [Bilibili Column Specification](artifact/references/bilibili.md)
- [Content Core Template](artifact/references/content-core-template.md)
- [Sensitive Words Reference](artifact/references/sensitive-words.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown drafts and review reports with YAML frontmatter, plus shell compliance-check output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files are organized by date, topic slug, platform, and matrix overview when applicable.]

## Skill Version(s):

1.0.1 (source: server release metadata and target metadata; artifact metadata says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
