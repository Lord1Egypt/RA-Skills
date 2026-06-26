## Description: <br>
AI 行业资讯专家 + 小红书内容创作。检索 24 小时内最新 AI 资讯，生成小红书文案 + 3:4 比例 HTML 封面。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javastarboy](https://clawhub.ai/user/javastarboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, content operators, and agent users use this skill to collect recent AI industry news, summarize source links, and produce Xiaohongshu-ready copy plus a mobile 3:4 HTML cover. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated content can be based on untrusted, stale, or synthetic news data. <br>
Mitigation: Use trusted or sanitized search results, verify source freshness, and treat demo output as synthetic test content rather than current news. <br>
Risk: Documentation examples interpolate JSON into shell commands. <br>
Mitigation: Avoid copying unsafe shell-interpolation patterns; pass structured data through safer argument or file-based workflows where possible. <br>
Risk: The script can automatically open generated HTML and output directories. <br>
Mitigation: Review before running and disable or remove automatic browser and file-manager opening in managed environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/javastarboy/ai-news-xiaohongshu) <br>
- [OpenClaw integration guide](references/openclaw-integration.md) <br>
- [Search query reference](references/search-queries.md) <br>
- [User configuration](references/user-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, HTML, and source-summary files with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes xiaohongshu-copy.md, cover.html, news-summary.md, and sources.md under output/<date>; falls back to demo data when real news JSON is not provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
