## Description: <br>
AI 智能品牌营销工具：输入品牌名称，自动采集全网数据、分析当日热点、生成一篇小红书图文内容，支持一键自动发布。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongxiaoke](https://clawhub.ai/user/dongxiaoke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketers and brand operators use this skill to generate Xiaohongshu-ready brand marketing posts from a brand name, including topical analysis, post text, tags, image references, and optional publishing guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A billable Zeelin App-Key may be stored in a predictable local file. <br>
Mitigation: Use a limited or test App-Key when possible, avoid shared environments, and delete ~/.zeelin_config or .zeelin_config after use. <br>
Risk: The optional auto-publish flow can post publicly to Xiaohongshu and may trigger account enforcement. <br>
Mitigation: Prefer manual publishing, review generated content before posting, and use auto-publish only after explicitly accepting platform-account risk. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dongxiaoke/brandmarketing) <br>
- [Zeelin Skill platform](https://skills.zeelin.cn) <br>
- [Xiaohongshu creator center](https://creator.xiaohongshu.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, files, guidance] <br>
**Output Format:** [Markdown and plain text with generated post content, topic tags, image URLs or local image paths, and optional publishing status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated Xiaohongshu title, body, tags, downloaded image paths, balance information, and a published note link when the optional auto-publish flow is used.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
