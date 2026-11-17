## Description:

基于明日DMP开放平台API，提供RTQ投放订单管理功能，支持创建、查询、修改投放订单，并通过标准化流程覆盖请求类型识别、凭证检查、参数引导、格式校验、参数确认和任务记录。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingri26](https://clawhub.ai/user/mingri26)

### License/Terms of Use:

MIT-0

## Use Case:

External advertisers and marketing operations teams use this skill to create, query, and modify Mingri DMP RTQ audience activation orders for targeted ad delivery. It guides credential setup, parameter collection, audience validation, user confirmation, and result reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live API and RTQ credentials may be exposed if pasted into chat, printed, or stored in local files.

Mitigation: Use scoped test credentials or an out-of-band secret mechanism, avoid sharing production keys in chat, and rotate any credentials that may have been exposed.

Risk: Order details and RTQ keys may persist in local credential or cache files such as ~/workspace/.order_cache.

Mitigation: Review local credential and order-cache contents after use, remove sensitive cache files when no longer needed, and keep file permissions restricted.

Risk: The skill can execute locally discovered auth or logger helper scripts.

Mitigation: Verify the exact mingdata-dmp-auth and task logger dependency paths and publishers before installation or execution.

Risk: The security verdict is suspicious because of credential handling and helper-script execution behavior.

Mitigation: Require review before deployment and run with least-privilege credentials in a controlled workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mingri26/skills/dmp-activation)
- [Mingri DMP auth dependency](https://clawhub.ai/mingri26/dmp-auth)
- [Mingri DMP task logger dependency](https://clawhub.ai/mingri26/dmp-skill-logger)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-like parameter examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute bundled Python scripts that call Mingri DMP APIs through an auth dependency and may write credential or order-cache files locally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
