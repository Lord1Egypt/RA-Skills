## Description: <br>
Claw Markdown Gen converts webpage articles into styled Markdown posts for WeChat, Zhihu, Juejin, Xiaohongshu, and Toutiao, with rewriting, word-count control, image keywording, and optional AI image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[webkixi](https://clawhub.ai/user/webkixi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content creators use this skill through the ClawMarkDown Chrome extension to turn webpage articles into publishable Markdown posts in common Chinese platform styles. It supports light, medium, and heavy rewriting, image placement, image keyword annotations, and optional AI-generated images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webpage text, image metadata, and heavy-mode image prompts may be sent through the AI workflow or a configured image-generation API. <br>
Mitigation: Avoid using AI image generation on private dashboards, account pages, confidential documents, or other sensitive webpage content. <br>
Risk: Optional image generation depends on a user-provided API key and endpoint. <br>
Mitigation: Use a trusted image API endpoint, keep the API key scoped, and rotate or revoke the key if exposure is suspected. <br>
Risk: Rewriting and generated imagery can change tone, emphasis, or factual detail before publication. <br>
Mitigation: Review the final Markdown and any generated images before publishing or sharing externally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/webkixi/skills/claw-markdown-gen) <br>
- [Claw Markdown Gen repository](https://github.com/webkixi/claw-markdown-gen) <br>
- [ClawMarkDown main project](https://github.com/webkixi/clawmark) <br>
- [Image handling reference](artifact/references/image-handling.md) <br>
- [Humanized Chinese writing reference](artifact/references/ren-zh.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration] <br>
**Output Format:** [Markdown article content with image placeholders, keyword comments, and optional generated-image links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require IMAGE_API_KEY and IMAGE_API_URL for heavy-mode AI image generation.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
