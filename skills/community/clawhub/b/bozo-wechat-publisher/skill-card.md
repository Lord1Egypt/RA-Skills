## Description: <br>
Publishes Markdown articles to WeChat Official Account drafts, with wenyan-cli formatting, custom card themes, and curl-based fallback publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bozoyan](https://clawhub.ai/user/bozoyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, operators, and developers use this skill to prepare and publish Markdown articles, metadata, cover images, and formatted HTML content into a WeChat Official Account draft workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires WeChat Official Account API credentials and may read them from environment variables, shell startup files, or TOOLS.md. <br>
Mitigation: Use a dedicated secret manager or per-run environment variables, avoid storing AppSecret in shared files, and rotate credentials after testing. <br>
Risk: Publishing workflows upload selected Markdown content, metadata, cover images, and generated article content to WeChat services. <br>
Mitigation: Review the exact Markdown, frontmatter, and image paths before publishing, and test with non-sensitive content first. <br>
Risk: Setup and publishing scripts may install global Node packages or run remote setup commands in some documented paths. <br>
Mitigation: Install Node and wenyan-cli manually from trusted sources, inspect shell commands before execution, and avoid curl-to-sudo-bash setup steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bozoyan/bozo-wechat-publisher) <br>
- [WeChat Official Account API documentation](https://developers.weixin.qq.com/doc/offiaccount/) <br>
- [wenyan-cli](https://github.com/caol64/wenyan-cli) <br>
- [Theme reference](references/themes.md) <br>
- [Troubleshooting reference](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces publishing instructions and command sequences that may upload selected Markdown content, metadata, and images to WeChat services.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
