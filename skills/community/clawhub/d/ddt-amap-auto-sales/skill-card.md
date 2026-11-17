## Description:

跑店销售的目标门店筛选、拜访优先级与周边竞对判断，可将高德地图中复制出的地点名称和地址文本作为地点输入，并基于店店通已发布门店快照生成可核验结论。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

External sales and operations users use this skill to screen automotive after-market store targets, prioritize visits, compare nearby competitors, and produce constrained, evidence-backed sales attack analysis from 店店通's published store snapshot data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a bearer token for 店店通's automotive-service API.

Mitigation: Protect and rotate DDT_API_KEY as an API credential, and never write real keys into chats, logs, skill files, or version control.

Risk: Requests should only send credentials to the trusted API host.

Mitigation: Keep DDT_OPEN_BASE set to the official HTTPS endpoint at https://gotoshop-ai.com/ddtclaw/ and avoid execution contexts where untrusted code can modify environment variables.

Risk: Store and market conclusions can be misleading when API coverage is incomplete or preview results are truncated.

Mitigation: Use only API-returned metrics, label uncovered data as unavailable, and narrow queries when preview.truncated is true.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-amap-auto-sales)
- [店店通开放平台](https://gotoshop-ai.com/ddtclaw/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API call examples and concise business analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include conclusions, 3-6 key metrics, coverage and data-version notes, only explicitly requested limited store previews, and uncovered items.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
