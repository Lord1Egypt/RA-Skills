## Description:

Baidu Netdisk file management for OpenClaw - List, search, download, upload with OAuth 2.0 (百度网盘文件管理 - OAuth 一键授权).

This skill is ready for commercial/non-commercial use.

## Publisher:

[niukesi](https://clawhub.ai/user/niukesi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent authenticate with Baidu Netdisk, list and search cloud files, retrieve download links, and upload files through command-line workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling may expose Baidu API keys or tokens through local config files, shell history, terminal logs, or process listings.

Mitigation: Use OAuth with a strong ENCRYPTION_KEY, avoid passing secrets on the command line, protect local config and logs, and rotate any credentials previously configured this way.

Risk: The skill can perform Baidu Netdisk read and write operations, including uploads, after authorization.

Mitigation: Review the requested basic and netdisk scopes before use and run the skill only in environments where those file-management permissions are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/niukesi/skills/baidu-netdisk-skill)
- [Baidu Netdisk Open Platform console](https://pan.baidu.com/union/console)
- [Quickstart guide](docs/QUICKSTART.md)
- [Security notes](SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide execution of Baidu Netdisk CLI commands that read, search, download, upload, authenticate, and manage local configuration.]

## Skill Version(s):

1.0.10 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
