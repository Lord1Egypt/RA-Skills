## Description:

基于明日DMP开放平台API，提供人群同步管理功能。支持获取广告账户、创建同步任务、查询同步状态。采用10步标准化工作流程，包含请求类型识别、凭证检查、参数引导、格式校验、参数确认、任务记录等完整流程。适用于将DMP人群包同步到各大广告平台（小红书/腾讯/字节等）进行精准投放。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingri26](https://clawhub.ai/user/mingri26)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing and operations users use this skill to synchronize Mingri DMP audience packages to supported advertising platforms, retrieve available ad accounts, and check sync task status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill workflow asks users to provide Mingri DMP Access Key and Secret Key values in chat.

Mitigation: Use a secure secret manager or a tightly permissioned local credential file, and avoid pasting AK/SK secrets into chat.

Risk: Helper scripts locate and execute authentication code from broad local skill directories, which can be spoofed if untrusted skills are present.

Mitigation: Install only verified dependencies, confirm publisher, version, and integrity before use, and avoid running the skill in environments with untrusted skills in searched directories.

Risk: Audience synchronization can affect advertising activation and relies on lawful source data and valid user authorization.

Mitigation: Require explicit user confirmation before creating sync tasks and confirm that audience data usage is authorized and compliant before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mingri26/skills/dmp-audience-sync)
- [Mingri DMP auth dependency](https://clawhub.ai/mingri26/mingdata-dmp-auth)
- [DMP skill logger dependency](https://clawhub.ai/mingri26/dmp-skill-logger)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API results from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes confirmation tables, credential-setup prompts, task IDs, sync status summaries, and error guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
