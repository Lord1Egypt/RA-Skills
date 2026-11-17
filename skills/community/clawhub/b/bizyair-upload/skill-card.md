## Description:

BizyAir 文件上传助手。当用户需要将本地图片、音频、视频等资源上传到 BizyAir 服务器时使用此技能。支持快速上传并获取可访问的 URL。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bozoyan](https://clawhub.ai/user/bozoyan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to upload selected local image, audio, video, or other files to BizyAir and receive URLs that can be used in BizyAir workflows. It can also list previously uploaded BizyAir input resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected local files are uploaded to BizyAir/OSS and resulting URLs may be usable outside the user's machine.

Mitigation: Upload only files intended for BizyAir use and handle returned URLs as externally accessible resource links.

Risk: BizyAir API keys can be exposed if pasted into chat or passed directly with --api-key.

Mitigation: Use BIZYAIR_API_KEY or a secret manager, use narrowly scoped keys, and avoid sharing keys in prompts or command-line history.

Risk: Runtime dependencies are installed from Python packages.

Mitigation: Install dependencies in a virtual environment and pin package versions before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bozoyan/skills/bizyair-upload)
- [BizyAir upload API tutorial](https://docs.bizyair.cn/api/upload-tutorial.html)
- [BizyAir API key console](https://bizyair.cn/user/api-key)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and upload result URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return uploaded resource URLs, object keys, resource IDs, list results, and actionable error messages.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
