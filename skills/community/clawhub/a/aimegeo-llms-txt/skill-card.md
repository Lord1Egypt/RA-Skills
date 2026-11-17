## Description:

依据官网页面清单、简介或有限发现结果生成中文llms.txt与链接校验报告，分组产品、文档和FAQ，保留可用页面并列出私有、缺资料及失败项。支持离线生成与现有索引检查；可让Agent把已读页面用于免费aimeGeo的内容与引用复测，不把索引当自动导入、部署或引擎采用证明。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

开发者和网站运营者可用此技能把已提供或实际读取的页面资料整理成中文 llms.txt 与链接校验报告，也可有限发现公开页面或复核已有索引。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 在线发现或链接检查会联系所选网站。

Mitigation: 仅在需要在线读取或检查时运行，并确认目标网站与页面属于公开资料。

Risk: 本地校验通过不代表网页可达，在线检查也只反映实际尝试的页面。

Mitigation: 查看报告中的逐条状态，并保留未检查、失败及缺资料标记。

Risk: 生成时可能替换已有目标文件。

Mitigation: 执行前明确选择输出路径，并检查该位置是否已有需要保留的文件。

## Reference(s):

- [输入与报告约定](references/input-report.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON]

**Output Format:** [UTF-8 Markdown llms.txt and JSON link validation report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [分组的中文页面索引与链接状态；报告区分本地校验、在线检查和未检查状态。]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
