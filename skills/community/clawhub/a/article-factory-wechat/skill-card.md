## Description: <br>
微信公众平台文章全流程生产工具，涵盖选题、调研、撰写、去AI味、生成配图、HTML排版及提交草稿七个标准步骤。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beneclaw](https://clawhub.ai/user/beneclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, editors, and marketing teams use this skill to produce WeChat public-account articles from topic discovery through research, drafting, image generation, HTML layout, review, and draft submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The draft submission workflow can save a live WeChat access token in draft.json. <br>
Mitigation: Remove or tightly protect draft.json after use, and avoid running the submission step with confidential or unapproved content. <br>
Risk: The skill can upload article content and images to external services such as WeChat and Feishu. <br>
Mitigation: Require explicit user confirmation before document creation, media upload, or draft submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/beneclaw/article-factory-wechat) <br>
- [Publisher profile](https://clawhub.ai/user/beneclaw) <br>
- [HTML style guide](references/html-style-guide.md) <br>
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, HTML article layouts, image files, JSON draft metadata, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are organized under a dated article directory and may include article.md, article.html, generated images, and draft.json.] <br>

## Skill Version(s): <br>
1.3.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
