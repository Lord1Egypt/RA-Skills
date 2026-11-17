## Description:

帮助用户整理投标资格与商务附件、逐条核对原文要求、复用企业资料并生成资料包。

This skill is ready for commercial/non-commercial use.

## Publisher:

[youteacher](https://clawhub.ai/user/youteacher)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要准备投标资格与商务附件的用户，整理招标要求和企业材料，展示逐项证据与待确认事项，并在人工确认后核验、组装 PDF 汇总件及保留原件的 ZIP 资料包。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 投标文件和企业材料可能含有敏感信息，分析时必要内容会传给平台及获授权的模型。

Mitigation: 仅处理用户有权使用的文件；在模型处理前说明传输范围并取得明确同意，保护密钥和证照原文。

Risk: 各付费阶段的实际费用可能变化，用户记录的预算不是服务端强制上限。

Mitigation: 每个付费阶段开始前查看当前最高费用并取得该阶段授权；没有当前费用依据时停在免费步骤。

Risk: 项目文件和产物按项目创建时间保留 30 天；资料库材料会保留到用户删除，删除资料库材料不会清除已有项目副本。

Mitigation: 按需要及时删除资料库材料和项目，并在清理前考虑已有项目副本仍按项目期限保留。

## Reference(s):

- [API 密钥配置与费用说明](https://ai-skills.open-idea.net/skill-docs/bid-document-checker/API-KEY.md)
- [HTTP 请求、计费、幂等与轮询](https://ai-skills.open-idea.net/skill-docs/bid-document-checker/HTTP-REQUESTS.md)
- [项目、资料库与阶段操作](https://ai-skills.open-idea.net/skill-docs/bid-document-checker/OPERATIONS.md)
- [隐私、证据和人工复核](https://ai-skills.open-idea.net/skill-docs/bid-document-checker/BEHAVIOR-RULES.md)

## Skill Output:

**Output Type(s):** [Guidance, PDF, ZIP archive, Markdown]

**Output Format:** [中文核对清单与复核建议；PDF 汇总件、含原件 ZIP、目录和页码表]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [按原文要求提供材料匹配与证据；未知项、未覆盖页、冲突及未解决问题保持可见，存在问题时资料包标为草稿。]

## Skill Version(s):

1.1.1 (source: release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
