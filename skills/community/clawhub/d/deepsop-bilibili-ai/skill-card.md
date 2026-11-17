## Description:

Bilibili 视频自动上传 skill。当用户需要登录 Bilibili、校验账号或上传视频时使用。基于 social-auto-upload 项目，OPclaw 自动准备运行环境，无需用户手动安装。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kukuoai](https://clawhub.ai/user/kukuoai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and operators use this skill to have an agent prepare Bilibili upload tooling, check account status, guide local QR-code login, and upload selected videos with title, description, category, tags, and optional schedule metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically download and run external third-party upload software and fallback mirror sources.

Mitigation: Review the external project before use, prefer pinned reviewed commits or releases, verify checksums or signatures where available, and require approval before setup actions.

Risk: The workflow stores Bilibili login state locally and uploads selected files and metadata to Bilibili.

Mitigation: Use only intended account names and video files, inspect upload metadata before execution, protect local credential files, and require approval before upload actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kukuoai/skills/deepsop-bilibili-ai)
- [social-auto-upload project](https://github.com/dreammis/social-auto-upload)
- [Runtime requirements](artifact/references/runtime-requirements.md)
- [CLI contract](artifact/references/cli-contract.md)
- [Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and example script snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing workflow guidance and command invocations for Bilibili login, account validation, and video upload.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
