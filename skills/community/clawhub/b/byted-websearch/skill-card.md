## Description: <br>
火山引擎联网搜索 API，返回网页/图片结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve current web or image search results from Volcengine when answers need live facts, source links, verification, or recent information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be exposed if users paste credentials into chat. <br>
Mitigation: Configure WEB_SEARCH_API_KEY through a protected skill setting, secret store, or local environment variable, and rotate any key already shared in a transcript. <br>
Risk: Search queries are sent to Volcengine as an external provider. <br>
Mitigation: Install and use the skill only when external query sharing is acceptable for the workspace and data involved. <br>
Risk: Broad search triggers may send vague questions or recommendations externally sooner than expected. <br>
Mitigation: Limit when the skill may search, especially for vague, recommendation-oriented, or sensitive prompts. <br>


## Reference(s): <br>
- [Skill release page](https://clawhub.ai/volcengine-skills/byted-websearch) <br>
- [Publisher profile](https://clawhub.ai/user/volcengine-skills) <br>
- [Volcengine Web Search API](https://www.volcengine.com/docs/85508/1650263) <br>
- [Volcengine API reference](https://www.volcengine.com/docs/87772/2272953) <br>
- [Volcengine product introduction](https://www.volcengine.com/docs/87772/2272949) <br>
- [Volcengine billing documentation](https://www.volcengine.com/docs/87772/2272951) <br>
- [Docs index](references/docs-index.md) <br>
- [Setup guide](references/setup-guide.md) <br>
- [Product docs gap review](references/product-docs-gap.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text search results with source URLs, snippets, image links, and setup or troubleshooting guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports web and image search, result-count limits, time-range filters, authority filtering, and query rewrite options.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
