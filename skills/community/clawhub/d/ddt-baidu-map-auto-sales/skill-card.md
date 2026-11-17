## Description:

帮助汽服跑店销售使用百度地图复制的地点名称和地址文本，基于店店通已发布门店快照筛选目标门店、排列拜访优先级并判断周边竞对。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

External sales and operations teams use this skill to evaluate automotive aftermarket brand coverage, prioritize store visits, and compare nearby competitive presence from published 店店通 store snapshots. It is intended for bounded lead analysis and visit planning, not exhaustive market enumeration or sales outcome prediction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send DDT_API_KEY to an endpoint inherited through DDT_OPEN_BASE.

Mitigation: Set DDT_API_KEY only in a controlled environment and keep DDT_OPEN_BASE unset or exactly the trusted service origin before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-baidu-map-auto-sales)
- [Skill homepage](https://gotoshop-ai.com/ddtclaw/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with concise metrics, limited previews, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should avoid API keys, internal fields, supplier details, and unsupported metrics.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
