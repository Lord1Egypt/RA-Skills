## Description: <br>
AI 智能写作助手 - 支持多平台内容创作，包括公众号、小红书、知乎、LinkedIn 等风格。提供 AI 查重、SEO 优化、改写润色等功能，一键生成高质量内容。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-wuxl](https://clawhub.ai/user/ryan-wuxl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and business users use this skill to generate and adapt Markdown articles or social posts for WeChat, Xiaohongshu, Zhihu, LinkedIn, Twitter/X, Weibo, and Douyin styles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted topic value can be executed as a shell command when hot-topic search runs. <br>
Mitigation: Only use fully trusted topic values and replace shell-string execution with argument-array process spawning before broader deployment. <br>
Risk: Topic searches may send user-provided subjects to Tavily. <br>
Mitigation: Avoid confidential topics and clearly disclose the external search data flow to users. <br>
Risk: The skill depends on a Tavily search helper and inherited environment variables. <br>
Mitigation: Declare the Tavily dependency explicitly and minimize inherited environment variables. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryan-wuxl/ai-content-writer) <br>
- [Homepage declared by artifact](https://github.com/openclaw/ai-writing-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown article or social-post content with optional command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated Markdown content to a user-specified output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
