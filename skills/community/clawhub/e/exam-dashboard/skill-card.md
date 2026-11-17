## Description:

期末试卷分析仪表盘融合成绩数据可视化、统计分析和微信公众号推文排版，帮助用户从 Excel 或 CSV 试卷数据生成交互式图表、分析报告和 HTML 发布稿。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuwenqi123123](https://clawhub.ai/user/liuwenqi123123)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, academic staff, and education analysts use this skill to analyze exam result spreadsheets, visualize score and item-level patterns, and prepare shareable reports or WeChat-ready HTML summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes student names, IDs, and exam scores.

Mitigation: Use trusted spreadsheets only and remove or pseudonymize student identifiers before creating reports that may be shared.

Risk: Generated HTML may be published or copied into a public channel.

Mitigation: Inspect generated HTML and charts before publication to confirm that private student data and unintended content are not exposed.

Risk: The skill depends on multiple Python packages for spreadsheet parsing, statistics, plotting, and document generation.

Mitigation: Install dependencies in a virtual environment with pinned versions where possible and review the environment before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuwenqi123123/skills/exam-dashboard)
- [Publisher profile](https://clawhub.ai/user/liuwenqi123123)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python-based report, chart, and HTML file generation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated artifacts may include PNG charts, interactive HTML chart files, a Markdown analysis report, and a WeChat-ready HTML article.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
