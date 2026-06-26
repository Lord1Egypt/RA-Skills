## Description: <br>
Generates styled Chinese Markdown articles from webpage content for WeChat, Zhihu, Juejin, Xiaohongshu, and Toutiao formats, with optional rewriting and image handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[webkixi](https://clawhub.ai/user/webkixi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content creators use this skill to turn captured webpage text and image metadata into polished Markdown articles for common Chinese publishing platforms. It supports article rewriting, style-specific formatting, original-image placeholders, and optional AI image generation for heavy rewrite mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected webpage text, image metadata, nearby image context, and optional AI image prompts may be sent to configured model or image API services. <br>
Mitigation: Use approved pages and providers, avoid confidential dashboards or private content unless authorized, and configure a dedicated image API key. <br>
Risk: Generated Markdown may preserve sensitive context from the source article or image metadata. <br>
Mitigation: Review the generated article and keyword comments before publishing or sharing externally. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/webkixi/skills/claw-markdown-gen) <br>
- [Image Handling Reference](references/image-handling.md) <br>
- [Chinese Humanization Reference](references/ren-zh.md) <br>
- [WeChat Style Configuration](references/styles/wechat_common_style.json) <br>
- [Zhihu Style Configuration](references/styles/zhihu_common_style.json) <br>
- [Juejin Style Configuration](references/styles/juejin_common_style.json) <br>
- [Xiaohongshu Style Configuration](references/styles/xiaohongshu_common_style.json) <br>
- [Toutiao Style Configuration](references/styles/toutiao_common_style.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration] <br>
**Output Format:** [Markdown article content with image placeholders, keyword comments, and optional image-generation post-processing commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include IMAGE and AI_IMAGE placeholders, Markdown image links, keyword HTML comments, and a version-update notice when invoked by an older plugin version.] <br>

## Skill Version(s): <br>
2.2.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
