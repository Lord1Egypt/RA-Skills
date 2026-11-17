## Description:

金融客户分群分析 Skill。当用户上传银行客户数据表格（CSV/Excel）时自动触发，完成客户分层、特征提取和可视化输出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yukirang](https://clawhub.ai/user/yukirang)

### License/Terms of Use:

MIT-0

## Use Case:

Banking analysts, customer operations teams, and developers use this skill to segment customer records with RFM-style features, K-Means clustering, profile summaries, charts, and a Markdown analysis report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive banking customer data and persists generated CSV outputs.

Mitigation: Use only permitted data, prefer non-production or de-identified records, write outputs to a dedicated access-controlled directory, and treat generated CSV files as sensitive.

Risk: Exported customer identifiers and spreadsheet-compatible values can expose or amplify sensitive data handling risk.

Mitigation: Minimize exported fields, mask customer identifiers where possible, and sanitize formula-leading values before opening outputs in spreadsheet tools.

Risk: The artifact describes CSV/Excel uploads, while the security guidance notes that only CSV input is currently supported.

Mitigation: Document CSV-only operation for this release or convert Excel files through a reviewed workflow before processing.

## Reference(s):

- [RFM 模型参考](artifact/references/rfm-guide.md)
- [聚类分析参数参考](artifact/references/clustering-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated CSV, PNG, and Markdown report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces segmentation_results.csv, cluster_summary.csv, segmentation_charts.png, and segmentation_report.md when the bundled script is run.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
