## Description:

把一份境内基金资料整理成八项逐字资料卡，每项附来源定位，并将缺失信息和需人工判断的事项明确标出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT

## Use Case:

面向需要阅读境内基金公开资料的读者，将产品资料概要、招募说明书节选或销售页面中的基金名称、投资范围、基准、费用、经理、风险与分红信息逐字整理并标注出处；不提供投资建议或收益预测。

### Deployment Geography for Use:

中国大陆

## Known Risks and Mitigations:

Risk: 使用可选 Cue 服务处理资料时，API 凭据或私人、带批注的文件可能涉及服务端隐私与计费条件。

Mitigation: 处理私人或带批注的文件时使用用户直供文本模式；启用 Cue 前核实接收 API key 的 HTTPS 地址，并查看解析服务的隐私和计费条款。不要把密钥放入聊天内容。

## Reference(s):

- [基金文件层级与三要素记法](artifact/references/fund-layers.md)
- [Cue MCP 配置文档](https://cuecue.cn/hub/mcp)
- [Cue Omni Reader 配置文档](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown 基金资料卡，含逐字引文、来源定位、缺数清单和待人工事项]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [围绕单只基金及所提供资料；缺失条目明确标为未检索到。]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
