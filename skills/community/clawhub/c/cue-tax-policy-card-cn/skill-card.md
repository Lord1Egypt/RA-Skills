## Description:

把一份中国境内税务文件整理为含原句和来源锚的八项速读卡，并明确标出缺项与需人工判断事项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT

## Use Case:

面向需要快速核对中国境内税务文件的财务、税务及业务人员，用于提取文件机关与文号、税种、税率、计税依据、日期期限、过渡安排及优惠条件的逐字内容和来源锚。测算、适用判断和申报办理留给人工处理。

### Deployment Geography for Use:

中国

## Known Risks and Mitigations:

Risk: 启用可选外部数据或解析服务时，税务文件内容可能被发送至外部服务。

Mitigation: 未授权外部处理时可直接使用用户提供的文本；启用服务前核实凭据目的地，并查看文件共享、保留和计费条款。

Risk: 引用、日期、税率或来源层级的误读可能造成不完整或误导性的卡片。

Mitigation: 对照原始文件核验引文、税率、日期和来源锚，标明地方口径或解读件的层级，并将适用判断和测算留给人工。

## Reference(s):

- [税务文件层级与来源锚速查](references/tax-layers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [中文五段式税务口径卡，含八项逐字条目、来源锚、缺数清单及待人工事项]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [税率、金额及日期按原文记录；缺失信息明确标注；测算、适用判断及申报办理标为待人工。]

## Skill Version(s):

0.1.0 (source: server-resolved release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
