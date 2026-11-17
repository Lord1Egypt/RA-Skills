## Description:

欧洲VAT申报预检工具。卖家上传申报表草稿和平台对账单后，逐项检查税率适用、供应地判定、OSS/IOSS注册匹配、B2B/B2C分类、申报周期和币种换算六类高频错误，输出结构化预检报告。当用户提到'VAT预检''VAT申报检查''申报前自查''欧洲增值税'等时触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[snowhola](https://clawhub.ai/user/snowhola)

### License/Terms of Use:

MIT-0

## Use Case:

面向在欧洲销售的跨境卖家，帮助其在提交前核对 VAT 申报草稿与平台对账单中的常见问题，并整理需进一步确认的事项。

### Deployment Geography for Use:

European Union and United Kingdom

## Known Risks and Mitigations:

Risk: 参考规则经过简化且可能过时，纠正成本估算也缺少来源；不完整或过多的业务数据可能影响判断并暴露无关信息。

Mitigation: 仅提供检查所需数字并遮盖无关客户或业务信息；核对税局最新公告，并在采取行动前与税务代表确认。

## Reference(s):

- [VAT rule table](references/rule-table.md)
- [Filing periods and deadlines](references/deadlines.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [结构化 Markdown 预检报告，包含风险摘要、逐项检查表和优先级建议。]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [初步核对结果；不构成合规结论，也不生成可提交的正式申报表。]

## Skill Version(s):

0.1.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
