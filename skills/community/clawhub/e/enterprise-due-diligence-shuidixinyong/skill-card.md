## Description:

基于公开招投标数据和可核验的公开信息，生成合作前的企业轻尽调报告或双公司对比报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragonzu](https://clawhub.ai/user/dragonzu)

### License/Terms of Use:

MIT-0

## Use Case:

供采购、销售和合作决策人员在签约或授信前了解企业的业务活动、客户与供应商、投标表现及公开风险；支持单家公司分析和两家公司对比。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review flagged hidden request-control instructions in the skill.

Mitigation: Review the skill's instructions and requested network actions before enabling it.

Risk: The skill can store a Zhiliaobiaoxun API key in ~/.zlbx/config.json.

Mitigation: Protect the credential file and avoid including API keys in reports or conversations.

Risk: Optional automatic registration sends platform, architecture and a hashed MAC address to the vendor.

Mitigation: Preconfigure ZLBX_API_KEY to avoid the device registration flow, or explicitly approve it after reviewing the data shared.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dragonzu/skills/enterprise-due-diligence-shuidixinyong)
- [知了标讯 Skill 文档](https://ai.zhiliaobiaoxun.com/docs/skill)
- [API quick reference](artifact/references/api-quick.md)
- [Due-diligence workflow](artifact/references/workflow.md)
- [Report template](artifact/references/report-template.md)
- [Optional registration guidance](artifact/references/auto-register.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, HTML report]

**Output Format:** [Markdown report and shareable HTML file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source links, data-coverage caveats, and optional side-by-side company comparison.]

## Skill Version(s):

1.0.7 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
