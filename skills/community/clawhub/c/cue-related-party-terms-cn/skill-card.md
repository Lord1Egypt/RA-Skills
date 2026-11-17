## Description:

从一份A股关联交易公告或协议提取八项逐字条款卡，并为每项保留原文和来源锚点。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

面向A股研究、法务和治理审阅人员，将单笔关联交易公告或协议整理为八项带原文和定位锚点的条款速读卡。缺失信息会明确标出，公允性和审议结果等判断留给人工。

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: 安全证据将技能标记为可疑，并指出外部服务发现、凭据和文档处理方面需要审查。

Mitigation: 启用前确认外部目录与解析服务及其数据去向符合预期；未确认前使用用户直供文本，不配置可选 CUE_API_KEY 或提交敏感文件。

Risk: 安全证据指出提取校验可能把未解析的数字当作完整结果；扫描分析部分未完成，因此结论并不充分。

Mitigation: 将金额、价格和年度额度逐项对照披露原文及锚点，并人工检查缺数清单，不把自动校验通过视为数字已核实。

## Reference(s):

- [关联交易条款速查](references/rpt-terms.md)
- [CUE 数据通道配置](https://cuecue.cn/hub/mcp)
- [CUE 附件解析配置](https://cuecue.cn/hub/omni-reader)
- [ClawHub release page](https://clawhub.ai/huhoo/skills/cue-related-party-terms-cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [中文 Markdown 条款卡，包含逐字引文、来源锚点、缺项清单和待人工判断项]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [八项固定结构；缺失内容标为「未检索到」；公允性、利益输送及审议结果等结论标为「待人工」。]

## Skill Version(s):

0.1.1 (source: artifact frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
