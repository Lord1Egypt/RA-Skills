## Description:

Generates stylized Markdown articles with image handling from webpage content for WeChat, Zhihu, Juejin, Xiaohongshu, and Toutiao publishing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webkixi](https://clawhub.ai/user/webkixi)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators and ClawMarkDown plugin users use this skill to convert webpage articles into platform-specific Chinese Markdown posts with controlled rewrite depth, image placeholders, keyword comments, and optional AI-generated images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image-generation credentials can be sent to a user-configured API URL.

Mitigation: Use a narrowly scoped image-generation key and only configure trusted HTTPS API endpoints.

Risk: Article text, image context, and generated prompts may be sent to configured AI services.

Mitigation: Avoid using the skill on sensitive webpages unless that data sharing is acceptable.

Risk: Some invocation paths produce plugin-promotional output instead of transformed article content.

Mitigation: Document and verify the ClawMarkDown plugin invocation requirement before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/webkixi/skills/claw-markdown-gen)
- [README](artifact/README.md)
- [Image handling reference](artifact/references/image-handling.md)
- [Humanized Chinese writing reference](artifact/references/ren-zh.md)
- [WeChat style configuration](artifact/references/styles/wechat_common_style.json)
- [Zhihu style configuration](artifact/references/styles/zhihu_common_style.json)
- [Juejin style configuration](artifact/references/styles/juejin_common_style.json)
- [Xiaohongshu style configuration](artifact/references/styles/xiaohongshu_common_style.json)
- [Toutiao style configuration](artifact/references/styles/toutiao_common_style.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown articles with image placeholders, keyword comments, optional SVG or Mermaid blocks, and generated image links from post-processing.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for ClawMarkDown-driven publishing workflows and may include platform-specific style conventions.]

## Skill Version(s):

2.3.1 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
