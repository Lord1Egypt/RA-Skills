## Description:

快手视频/图文自动上传 skill。当用户需要登录快手、校验账号或上传内容时使用。基于 social-auto-upload 项目，OPclaw 自动准备运行环境，无需用户手动安装。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kukuoai](https://clawhub.ai/user/kukuoai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and operators use this skill to log in to Kuaishou, validate account cookies, and publish selected video or photo-note content through the social-auto-upload CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch and run mutable third-party uploader code before publishing media.

Mitigation: Review the upstream project before use and prefer a pinned, reviewed commit instead of an unpinned clone.

Risk: Mirror-sourced downloads and browser automation dependencies can expand supply-chain exposure.

Mitigation: Avoid unofficial mirrors where possible and use an isolated environment for setup and uploads.

Risk: The skill stores local Kuaishou session files and can publish selected media to the account.

Mitigation: Use an isolated account or media directory and require explicit confirmation before upload commands are run.

## Reference(s):

- [Runtime Requirements](references/runtime-requirements.md)
- [CLI Contract](references/cli-contract.md)
- [Troubleshooting](references/troubleshooting.md)
- [social-auto-upload](https://github.com/dreammis/social-auto-upload)
- [ClawHub Skill Page](https://clawhub.ai/kukuoai/skills/deepsop-kuaishou-ai)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Code]

**Output Format:** [Markdown with inline shell commands and example code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce login, cookie-check, video-upload, and photo-note upload commands for user-selected Kuaishou accounts and media files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
