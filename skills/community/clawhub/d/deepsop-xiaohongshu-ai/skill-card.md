## Description:

小红书视频/图文自动上传 skill。当用户需要登录小红书、校验账号或上传内容时使用。基于 social-auto-upload 项目，OPclaw 自动准备运行环境，无需用户手动安装。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kukuoai](https://clawhub.ai/user/kukuoai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and operators use this skill to guide an agent through Xiaohongshu login checks and video or image-note publishing through the social-auto-upload CLI. It helps prepare the local runtime, choose the correct subcommand, and troubleshoot account, cookie, media, and scheduling issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First use can download and run third-party social-auto-upload code, dependencies, and a Chromium browser.

Mitigation: Use a pinned and verified upstream commit, install only from a trusted source, and avoid mirror or fork fallbacks unless they are explicitly trusted.

Risk: The skill can publish content through a user's Xiaohongshu account using local cookie or session state.

Mitigation: Confirm the exact account, media files, title, tags, and schedule before upload, and require the user to complete login locally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kukuoai/skills/deepsop-xiaohongshu-ai)
- [social-auto-upload upstream project](https://github.com/dreammis/social-auto-upload)
- [Runtime requirements](references/runtime-requirements.md)
- [CLI contract](references/cli-contract.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands and example code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account-specific command arguments, media paths, tags, schedule values, and troubleshooting steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
