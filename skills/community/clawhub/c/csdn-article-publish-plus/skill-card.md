## Description: <br>
将 Markdown 文章通过用户目录浏览器会话发布到 CSDN。支持保存草稿、预览排版、人工确认发布；默认保持浏览器打开并复用登录态。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[love254443233](https://clawhub.ai/user/love254443233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content authors use this skill to publish Markdown articles to CSDN through an existing Chrome or Edge browser session, with draft, preview, and publish modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill acts through a logged-in Chrome or Edge profile and can publish to CSDN as that user. <br>
Mitigation: Use a dedicated browser profile logged into only CSDN, start with draft-preview mode, and run publish mode only after reviewing the article. <br>
Risk: The skill automatically changes article content by normalizing Markdown and appending or replacing a WeChat QR section. <br>
Mitigation: Inspect the full CSDN preview, including the added QR section, before publishing. <br>
Risk: The browser may remain open and reuse session state by default. <br>
Mitigation: Set keep-open to false when session persistence is not needed, or close the dedicated browser profile after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/love254443233/csdn-article-publish-plus) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, json, markdown] <br>
**Output Format:** [JSON execution results with optional screenshot files and modified Markdown content submitted through the browser] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses browser session state and can keep the browser open after execution.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
