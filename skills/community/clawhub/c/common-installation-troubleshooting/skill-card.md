## Description:

解决 OpenClaw 插件安装中常见 npm 包名错误、权限问题和安装验证的排查方法及最佳实践。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dawai2005](https://clawhub.ai/user/dawai2005)

### License/Terms of Use:


## Use Case:

OpenClaw users and developers use this skill to troubleshoot failed plugin or CLI installations, verify npm package names, and choose safer next steps for installation validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Forced global npm installation can overwrite global files or hide the actual lock, permission, or package-name issue.

Mitigation: Verify the exact package name, publisher, and source documentation first; use `--force` only after diagnosing the issue and confirming a rollback path.

Risk: Incorrect package names can lead users to install the wrong package or trust unsupported installation paths.

Mitigation: Check the registry entry and official documentation before running install commands, then validate the installed CLI or plugin version after installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dawai2005/skills/common-installation-troubleshooting)
- [ClawHub Documentation](https://docs.openclaw.ai/tools/clawhub)
- [npm Registry](https://www.npmjs.com/)
- [ClawHub Website](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Troubleshooting guidance may include npm package names and global install commands that require user verification before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
