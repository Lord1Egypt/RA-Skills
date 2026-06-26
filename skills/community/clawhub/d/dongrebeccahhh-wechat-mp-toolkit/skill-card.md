## Description: <br>
Wechat Mp Toolkit helps WeChat public-account operators draft articles, generate cover images, analyze trending topics, and create WeChat draft posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongrebeccahhh-boop](https://clawhub.ai/user/dongrebeccahhh-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content operators and developers use this skill to automate WeChat public-account content workflows, including topic discovery, Markdown article creation, cover generation, and draft creation through WeChat APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled WeChat credentials could expose or misuse a public-account integration. <br>
Mitigation: Remove the bundled app secret, rotate it before use, and load credentials from a protected user-controlled source. <br>
Risk: The publishing workflow can upload media and create WeChat drafts without an explicit preview or confirmation step. <br>
Mitigation: Add a review gate that shows the article, cover, target account, and API action before any upload or draft creation. <br>
Risk: Absolute /root paths and external helper execution may fail or run unexpected local tooling in another environment. <br>
Mitigation: Replace hard-coded paths with configurable workspace paths and review helper commands before running the workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dongrebeccahhh-boop/dongrebeccahhh-wechat-mp-toolkit) <br>
- [WeChat Official Account API](https://api.weixin.qq.com) <br>
- [Sina News hotspot source](https://news.sina.com.cn) <br>
- [Baidu hotspot source](https://www.baidu.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON configuration, generated image files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local article and cover files, upload cover media, and create remote WeChat draft entries when configured and executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
