## Description: <br>
为 AI Agent 提供多个主流互联网平台的数据访问能力，包括搜索、内容读取、字幕提取和社交内容检索。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nidhov01](https://clawhub.ai/user/nidhov01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to let an agent search and read web, social, video, RSS, and platform content, then return retrieved text, metadata, summaries, or setup guidance. It is suited for news lookup, content aggregation, transcript retrieval, and social discussion research where the user accepts the target platform terms and credential handling requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle account or browser session credentials for services such as Twitter/X, XiaoHongShu, and Bilibili. <br>
Mitigation: Use dedicated low-privilege accounts, avoid sending cookies or API keys through chat, encrypt stored cookies, rotate credentials, and remove saved configuration when access is no longer needed. <br>
Risk: Installation and setup can change the host environment by installing packages, creating scripts, and modifying shell configuration. <br>
Mitigation: Prefer a virtual environment or dry-run review, inspect install actions before execution, and review changes to ~/.bashrc and skill directories after setup. <br>
Risk: Real web access and platform scraping can trigger rate limits, account restrictions, or policy issues. <br>
Mitigation: Keep request volume low, respect target platform terms, use user-approved proxies only where appropriate, and review retrieved content before using it in downstream workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nidhov01/07) <br>
- [Security tools documentation](artifact/security/README.md) <br>
- [Integration guide](artifact/integration/README.md) <br>
- [Exa MCP endpoint](https://mcp.exa.ai/mcp) <br>
- [Xiaohongshu MCP project](https://github.com/xpzouying/xiaohongshu-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, Python examples, JSON-like records, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include retrieved platform content, URLs, authors, timestamps, subtitles, comments, metadata, configuration steps, and security guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
