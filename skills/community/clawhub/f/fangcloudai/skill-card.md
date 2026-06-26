## Description: <br>
亿方云 (Fangcloud) AI 能力集成 Skill。支持文件管理（列表、上传、下载、分享）、协作邀请、知识库对话 (DeepSeek) 以及智能体交互。当用户需要操作亿方云文件、查询最近文档或创建分享链接时，使用此 Skill。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiema123](https://clawhub.ai/user/jiema123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business users use this skill to work with Fangcloud files, sharing workflows, collaboration invitations, knowledge-base chat, and agent interactions through the Fangcloud API and CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use powerful Fangcloud user and admin tokens for file, sharing, collaboration, and tenant-level API operations. <br>
Mitigation: Use least-privilege, short-lived user tokens and provide FANGCLOUD_ADMIN_TOKEN only when tenant administration is deliberately required. <br>
Risk: Documentation includes bearer-token examples that may be mistaken for usable credentials. <br>
Mitigation: Treat any documented bearer tokens as exposed secrets and rotate them if they were ever valid. <br>
Risk: The release workflow downloads and runs remote CLI binaries from the Fangcloud release channel. <br>
Mitigation: Install only when the publisher and release channel are trusted, and prefer signed or checksum-verified binaries before deployment. <br>


## Reference(s): <br>
- [Fangcloud AI Skill on ClawHub](https://clawhub.ai/jiema123/fangcloudai) <br>
- [Fangcloud API Endpoint Analysis](artifact/references/openapi.md) <br>
- [Fangcloud CLI Release Guide](artifact/cli/release/README.md) <br>
- [Fangcloud CLI Release Channel](https://app.fangcloud.com/sync/vv25/knowclaw/release/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, API endpoints, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Fangcloud API requests, CLI commands, file-management guidance, share links, and Markdown summaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
