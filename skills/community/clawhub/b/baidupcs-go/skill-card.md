## Description:

Provides agent guidance for using BaiduPCS-Go to manage Baidu Netdisk accounts, files, transfers, shares, offline downloads, and configuration from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linauror](https://clawhub.ai/user/linauror)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and other command-line users use this skill to operate Baidu Netdisk through BaiduPCS-Go, including account management, upload, download, transfer, sharing, recycle bin, offline download, and configuration workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a BaiduPCS-Go executable whose path and build provenance are not verified by the evidence.

Mitigation: Use an executable from a trusted source, verify hashes when available, or build from source before allowing the agent to invoke commands.

Risk: Login flows may handle BDUSS, STOKEN, or cookie values that can grant account access.

Mitigation: Treat these values as passwords, avoid shell history and logs, and prefer secret-handling mechanisms outside visible prompts.

Risk: File-management commands can delete, overwrite, unshare, or broadly match paths.

Mitigation: Require explicit user confirmation before destructive operations, overwrite policies, unshare actions, and broad wildcard commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linauror/skills/baidupcs-go)
- [BaiduPCS-Go command reference](artifact/BaiduPCS-Go.md)
- [Skill usage notes](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that require an installed BaiduPCS-Go executable and an authenticated Baidu account.]

## Skill Version(s):

1.0.0 (source: evidence.release.version, artifact/package.json, artifact/commands.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
