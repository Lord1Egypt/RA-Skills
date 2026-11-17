## Description:

AI 智能写作助手 - 支持多平台内容创作，包括公众号、小红书、知乎、LinkedIn 等风格。提供 AI 查重、SEO 优化、改写润色等功能，一键生成高质量内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-wuxl](https://clawhub.ai/user/ryan-wuxl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to generate platform-specific Chinese marketing and social content for WeChat, Xiaohongshu, Zhihu, LinkedIn, Twitter/X, Weibo, and Douyin. It can combine topic prompts, writing style, tone, keywords, and optional Tavily-backed trend search into Markdown article drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The trend-search path can execute a shell command built from user-supplied topic text.

Mitigation: Use only trusted topic input until the publisher replaces string-based shell execution with argument-array process execution or a direct Tavily API client.

Risk: The skill runs an external local Tavily search script and inherits environment variables.

Mitigation: Verify or remove the external local-skill dependency and pass only the required environment variables before enabling TAVILY_API_KEY.

Risk: Some advertised rewrite, SEO, and deduplication commands are not backed by artifact scripts in this release.

Mitigation: Do not rely on those advertised commands unless the corresponding scripts are added and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryan-wuxl/skills/ai-writer-pro)
- [Publisher profile](https://clawhub.ai/user/ryan-wuxl)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown article drafts and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated output may be printed to stdout or written to a user-specified file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
