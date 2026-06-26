## Description: <br>
自动发布内容到小红书平台，支持图文发布、登录状态检查和登录二维码获取。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dragon015](https://clawhub.ai/user/dragon015) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content operators use this skill to prepare and publish image-and-text posts to Xiaohongshu through a local MCP service after confirming account login state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The external Xiaohongshu MCP executable controls the actual posting flow and receives access to the user's Xiaohongshu session. <br>
Mitigation: Install and run the executable only from a trusted source, test first with a non-production account, and keep the service local. <br>
Risk: Publishing commands can post unintended content or image paths to Xiaohongshu. <br>
Mitigation: Review every title, content body, tag list, and image path before running publish commands or bundled example scripts. <br>
Risk: The skill requires an authenticated Xiaohongshu account session. <br>
Mitigation: Confirm login status before publishing and avoid sharing the local environment or session files with untrusted users. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dragon015/dragon-xiaohongshu) <br>
- [Configuration guide](references/config.md) <br>
- [mcporter documentation](http://mcporter.dev) <br>
- [Xiaohongshu MCP project](https://github.com/xpzouying/xiaohongshu-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local publishing commands and configuration guidance; publishing itself is performed by the external Xiaohongshu MCP executable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
